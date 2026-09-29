#!/usr/bin/env python
"""Chunk kumesini kaynak belgelere karsi dogrular.

"Chunk'lar hazir" demek icin uretici calismis olmasi yetmez. Burada olculen sey
chunk'larin ANLAMI degil - o ground truth ister - fakat anlamin kaybolmasina yol
acan yapisal kosullardir. Hepsi deterministik: ayni girdi, ayni sonuc.

Kontroller:
  kapsam            kaynak metnin ne kadari en az bir chunk'ta yer aliyor
                    (dusuk kapsam = sessiz icerik kaybi)
  tekrar            chunk toplam boyutu / kaynak boyutu
                    (ortusme ve birlestirmeden gelen kacinilmaz fazlalik)
  yarim_cumle       cumle ortasinda biten chunk
  dipnot_kopuk      chunk bir dipnota atif yapiyor ama tanimi chunk'ta yok,
                    oysa belge o dipnotu tanimliyor -> kosul bilgisi koptu
  tablo_bolunmus    ayni tablo satiri birden fazla chunk'ta
  sahipsiz_parent   parent_id var ama o kimlikte chunk yok

Calistirma:
    python _scripts/chunk_validation.py
"""
import json, os, re, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))

CHUNKS = os.path.join(ROOT, "_work", "chunks", "chunks.json")
GIRDI = os.path.join(ROOT, "_work", "enriched")
NCCN_ELLE = os.path.join(ROOT, "layer1_clinical", "nccn", "nccn_myeloma_manual.md")
RAPOR = os.path.join(ROOT, "_logs", "chunk_validation.json")

DIPNOT_ISARET = re.compile(r"\[\^([^\]]+)\]")
DIPNOT_TANIM = re.compile(r"(?m)^\s*[-*]?\s*\[\^([^\]]+)\]\s*:")
BITIS = re.compile(r"[.!?:;»\"')\]}]\s*$")


def norm(s):
    """Bosluklari sadelestir, bastaki liste isaretini at.

    Dipnot tanimi kaynakta "- [^a]: ..." biciminde, chunk icinde "[^a]: ..."
    biciminde duruyor. Liste isaretini atmayan karsilastirma bunlari icerik
    kaybi sayiyordu (tek basina 132 sahte bulgu).
    """
    return re.sub(r"^[-*•]\s+", "", re.sub(r"\s+", " ", s).strip())


def kaynak_metinler():
    d = {}
    for f in sorted(os.listdir(GIRDI)):
        if f.endswith(".md"):
            d[f] = open(os.path.join(GIRDI, f), encoding="utf-8",
                        errors="replace").read()
    d[os.path.basename(NCCN_ELLE)] = open(NCCN_ELLE, encoding="utf-8",
                                          errors="replace").read()
    return d


def belge_adi(ad):
    """chunk.py ile AYNI benzersiz kimlik uretilmeli; yoksa gruplama kayar."""
    p = ad[:-3].split("__")
    return "__".join(p[1:]) if len(p) > 1 else p[0]


def main():
    chunks = json.load(open(CHUNKS, encoding="utf-8"))
    kaynak = kaynak_metinler()

    gruplu = defaultdict(list)
    for c in chunks:
        gruplu[c["metadata"]["document_name"]].append(c)

    kimlikler = {c["chunk_id"] for c in chunks}
    sahipsiz = sorted({c["parent_id"] for c in chunks
                       if c["parent_id"] and c["parent_id"] not in kimlikler})

    bulgular, toplam_kaynak, toplam_chunk = [], 0, 0
    kapsam_dusuk = []
    for dosya, metin in kaynak.items():
        ad = belge_adi(dosya)
        cs = gruplu.get(ad, [])
        if not cs:
            bulgular.append(dict(tur="chunk_uretilmedi", belge=ad))
            continue

        kaynak_sat = {norm(x) for x in metin.split("\n") if len(norm(x)) > 25}
        chunk_sat = set()
        for c in cs:
            chunk_sat |= {norm(x) for x in c["content"].split("\n")}
        eksik = {x for x in kaynak_sat if x not in chunk_sat}
        # Alt bolme cumle bazina indiginde satir birebir eslesmeyebilir;
        # ikinci tur olarak alt dize aramasi yapilir.
        if eksik:
            # Iki taraf da normalize edilmeli: kaynak satirinda cift bosluk
            # varken chunk metni ham hali koruyor, ham karsilastirma satiri
            # "kayip" gosteriyordu. 909 sahte bulgunun kaynagi buydu.
            birlesik = norm("\n".join(c["content"] for c in cs))
            eksik = {x for x in eksik if x not in birlesik}
        kapsam = 1 - len(eksik) / max(1, len(kaynak_sat))
        if kapsam < 0.995:
            kapsam_dusuk.append((ad, round(kapsam, 4), len(eksik), len(kaynak_sat)))

        toplam_kaynak += len(metin)
        toplam_chunk += sum(len(c["content"]) for c in cs)

        tanimli = set(DIPNOT_TANIM.findall(metin))
        for c in cs:
            govde = c["content"].split("### ASSOCIATED FOOTNOTES:")[0]
            ekli = set(DIPNOT_TANIM.findall(c["content"]))
            for h in set(DIPNOT_ISARET.findall(govde)):
                if h in tanimli and h not in ekli:
                    bulgular.append(dict(tur="dipnot_kopuk", belge=ad,
                                         chunk=c["chunk_id"], isaret=h))

    # Tablo bolunmesi = AYNI satirin ARDISIK iki chunk'ta gecmesi. Ayni satirin
    # belgenin uzak yerlerinde tekrar etmesi bolunme degildir; tablo basliklari
    # ve "Note: All recommendations are category 2A" gibi satirlar kaynakta
    # zaten defalarca geciyor. Bu ayrimi yapmayan olcum 909 sahte bulgu uretti.
    tablo_yer = defaultdict(list)
    for i, c in enumerate(chunks):
        for s in {norm(x) for x in c["content"].split("\n")
                  if x.lstrip().startswith("|") and len(norm(x)) > 30}:
            tablo_yer[(c["metadata"]["document_name"], s)].append(i)
    bolunmus = sum(1 for v in tablo_yer.values()
                   if len(v) > 1 and any(b - a == 1 for a, b in zip(v, v[1:])))

    yarim = [c["chunk_id"] for c in chunks
             if not BITIS.search(c["content"].rstrip())
             and "CONTAINS_TABLE" not in c["metadata"]["parsing_flags"]
             and not c["content"].rstrip().endswith(("-", "•"))]

    print(f"{len(chunks)} chunk / {len(kaynak)} belge")
    print(f"  tekrar orani      : {toplam_chunk/max(1,toplam_kaynak):.3f} "
          f"(1.0 = kaynakla ayni hacim)")
    print(f"  kapsami <99.5% olan belge: {len(kapsam_dusuk)}")
    for a, k, e, t in sorted(kapsam_dusuk, key=lambda x: x[1])[:8]:
        print(f"      {k:.3f}  {e:4d}/{t:4d} satir eksik  {a[:46]}")
    print(f"  dipnot kopuk      : {sum(1 for b in bulgular if b['tur']=='dipnot_kopuk')}")
    print(f"  tablo bolunmus    : {bolunmus}")
    print(f"  yarim cumle biten : {len(yarim)} ({len(yarim)/len(chunks):.1%})")
    print(f"  sahipsiz parent_id: {len(sahipsiz)}")
    print(f"  chunk uretilmeyen : {sum(1 for b in bulgular if b['tur']=='chunk_uretilmedi')}")

    json.dump(dict(chunk=len(chunks), kapsam_dusuk=kapsam_dusuk,
                   sahipsiz_parent=len(sahipsiz), tablo_bolunmus=bolunmus,
                   yarim_cumle=len(yarim), bulgular=bulgular[:500]),
              open(RAPOR, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"  -> {RAPOR}")


if __name__ == "__main__":
    main()
