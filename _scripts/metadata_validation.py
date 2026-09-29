#!/usr/bin/env python
"""Metadata Validation - chunk METADATA'sinin kendisini denetler.

Level 1 (chunk_validation.py) icerigin bozulup bozulmadigina bakiyor. Bu script
farkli bir soruyu soruyor: chunk'in UZERINDEKI etiketler dogru mu? Ikisi
bagimsiz - icerigi kusursuz bir chunk, bolum numarasi "**<u>Klinik</u>**" ise
filtrelemede de alintida da ise yaramaz.

Kontroller ve siddet (kararlastirildi):
  section_number   ERROR   belge sinifinin kanonik kumesinde mi
  version          ERROR   surumsuz klinik bilgi kullanilmamali
  page_number      WARN    alinti (Level 4) icin gerekli
  layer / source   ERROR   kaynak dosyadan turetilenle tutarli mi
  atc_codes        REVIEW  belgenin kendi etken maddesi disinda kod tasiyor mu

Belge duzeyinde olan kontroller (version, layer, source) chunk basina degil
BELGE basina raporlanir; yoksa tek bir eksik alan 14 bin bulgu uretir.

Bu script hicbir dosyayi degistirmez, yalnizca olcer.

Calistirma:
    python _scripts/metadata_validation.py
    python _scripts/metadata_validation.py --detay --limit 20
"""
import argparse, json, os, re, sys, unicodedata
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))

CHUNKS = os.path.join(ROOT, "_work", "chunks", "chunks.json")
ENRICHED = os.path.join(ROOT, "_work", "enriched")
NCCN_ELLE = os.path.join(ROOT, "layer1_clinical", "nccn", "nccn_myeloma_manual.md")
RAPOR = os.path.join(ROOT, "_logs", "metadata_validation.json")

# --- Kanonik bolum kumeleri ---------------------------------------------------

EU_SMPC = ({str(i) for i in range(1, 11)} |
           {f"4.{i}" for i in range(1, 10)} |
           {f"5.{i}" for i in range(1, 4)} |
           {f"6.{i}" for i in range(1, 7)})

FDA_UST = {str(i) for i in range(1, 18)}
FDA_ALT = re.compile(r"^(1[0-7]|[1-9])\.[1-9]$")
NCCN_KOD = re.compile(r"^(MYEL|MGNS|MGCS|SP)-[0-9A-Z]+$", re.I)
SUT_MADDE = re.compile(r"^\d+(\.\d+)*[.\-]?[A-Za-z]?$")

# source_type -> beklenen katman dizini
KATMAN = {
    "NCCN": "layer1_clinical",
    "TITCK_KUB": "layer2_regulatory",
    "FDA_SMPC": "layer2_regulatory",
    "EMA_SMPC": "layer2_regulatory",
    "SUT": "layer3_reimbursement",
}

# Belge surumunu tasiyan kaliplar. Bulunamazsa surum yok demektir.
SURUM = [
    re.compile(r"Version\s+(\d+\.\d{4})", re.I),                    # NCCN 5.2026
    re.compile(r"KÜB'?ÜN\s+YENİLENME\s+TARİHİ[^\d]{0,80}(\d{2}[./]\d{2}[./]\d{4})", re.I),
    re.compile(r"Revised:?\s*(\d{1,2}/\d{4})", re.I),               # FDA
    re.compile(r"(\d{2}[./]\d{2}[./]\d{4})\s*tarihli", re.I),       # SUT
]


def sade(s):
    s = str(s).replace("İ", "i").replace("I", "ı").lower().replace("ı", "i")
    return "".join(c for c in unicodedata.normalize("NFKD", s)
                   if not unicodedata.combining(c))


def kaynak_indeks():
    """document_name -> (dosya adi, katman, klasor, etken madde)"""
    d = {}
    for f in sorted(os.listdir(ENRICHED)):
        if not f.endswith(".md"):
            continue
        p = f[:-3].split("__")
        ad = "__".join(p[1:]) if len(p) > 1 else p[0]
        etken = p[3] if len(p) >= 5 and p[1] == "titck" and p[2] == "kub" else None
        d[ad] = (f, p[0], p[1] if len(p) > 1 else None, etken)
    d["nccn_myeloma_manual"] = (os.path.basename(NCCN_ELLE), "layer1_clinical",
                                "nccn", None)
    return d


def bolum_gecerli(tur, s):
    if s is None:
        return False
    s = str(s).strip()
    if tur in ("TITCK_KUB", "EMA_SMPC"):
        return s in EU_SMPC
    if tur == "FDA_SMPC":
        return s in FDA_UST or bool(FDA_ALT.match(s))
    if tur == "NCCN":
        return bool(NCCN_KOD.match(s))
    if tur == "SUT":
        return bool(SUT_MADDE.match(s))
    return True                       # semasi olmayan belge: kontrol edilemez


def surum_bul(metin):
    for k in SURUM:
        m = k.search(metin)
        if m:
            return m.group(1)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--detay", action="store_true")
    ap.add_argument("--limit", type=int, default=10)
    a = ap.parse_args()

    chunks = json.load(open(CHUNKS, encoding="utf-8"))
    idx = kaynak_indeks()

    # Ilac sozlugunu chunk.py'den odunc al: etken madde -> ATC eslemesi orada.
    import chunk as C
    etken_atc = {}
    for inn, (varyant, kod) in C.ILAC.items():
        for v in varyant:
            etken_atc[sade(v)] = kod

    belge_bulgu, chunk_bulgu = [], []
    belgeler = sorted({c["metadata"]["document_name"] for c in chunks})

    # --- Belge duzeyi: version, layer, source ---
    surumler = {}
    for ad in belgeler:
        kay = idx.get(ad)
        if not kay:
            belge_bulgu.append(dict(seviye="ERROR", tur="kaynak_bulunamadi", belge=ad))
            continue
        dosya, katman, klasor, etken = kay
        yol = (NCCN_ELLE if ad == "nccn_myeloma_manual"
               else os.path.join(ENRICHED, dosya))
        s = next((c["metadata"].get("version") for c in chunks
                  if c["metadata"]["document_name"] == ad), None)
        surumler[ad] = s
        if not s:
            belge_bulgu.append(dict(seviye="ERROR", tur="version_yok", belge=ad))

        turler = {c["metadata"]["source_type"] for c in chunks
                  if c["metadata"]["document_name"] == ad}
        for t in turler:
            bekl = KATMAN.get(t)
            if bekl and bekl != katman:
                belge_bulgu.append(dict(seviye="ERROR", tur="layer_uyumsuz", belge=ad,
                                        detay=f"source_type {t} -> beklenen {bekl}, "
                                              f"dosya {katman}"))
        if len(turler) > 1:
            belge_bulgu.append(dict(seviye="ERROR", tur="source_tutarsiz", belge=ad,
                                    detay=f"ayni belgede {sorted(turler)}"))

    # --- Chunk duzeyi: section_number, page_number, atc ---
    for c in chunks:
        m = c["metadata"]
        ad, tur = m["document_name"], m["source_type"]
        if not bolum_gecerli(tur, m.get("section_number")):
            chunk_bulgu.append(dict(seviye="ERROR", tur="section_number_gecersiz",
                                    belge=ad, chunk=c["chunk_id"],
                                    detay=repr(m.get("section_number"))[:60]))
        if not m.get("page_number"):
            chunk_bulgu.append(dict(seviye="WARN", tur="page_number_yok",
                                    belge=ad, chunk=c["chunk_id"]))
        kay = idx.get(ad)
        etken = kay[3] if kay else None
        if etken and m.get("atc_codes"):
            bekl = etken_atc.get(sade(etken))
            yabanci = [k for k in m["atc_codes"] if k != bekl]
            if bekl and yabanci:
                chunk_bulgu.append(dict(seviye="REVIEW", tur="atc_yabanci",
                                        belge=ad, chunk=c["chunk_id"],
                                        detay=f"belge etken maddesi {bekl}, "
                                              f"chunk'ta ayrica {yabanci}"))

    # --- Rapor ---
    hepsi = belge_bulgu + chunk_bulgu
    sev = Counter(b["seviye"] for b in hepsi)
    tip = Counter(b["tur"] for b in hepsi)
    print(f"{len(chunks)} chunk / {len(belgeler)} belge")
    print(f"  ERROR {sev['ERROR']} | WARN {sev['WARN']} | REVIEW {sev['REVIEW']}")
    for t, n in tip.most_common():
        print(f"    {t:26s} {n}")

    kotu = defaultdict(int)
    for b in chunk_bulgu:
        if b["tur"] == "section_number_gecersiz":
            kotu[b["belge"]] += 1
    print(f"\n  gecersiz section_number tasiyan belge: {len(kotu)}")
    for ad, n in sorted(kotu.items(), key=lambda x: -x[1])[:a.limit]:
        print(f"    {n:5d}  {ad[:60]}")

    tur_bazli = defaultdict(lambda: [0, 0])
    for c in chunks:
        t = c["metadata"]["source_type"]
        tur_bazli[t][0] += 1
        if bolum_gecerli(t, c["metadata"].get("section_number")):
            tur_bazli[t][1] += 1
    print("\n  kaynak turune gore gecerli section_number orani:")
    for t, (n, ok) in sorted(tur_bazli.items()):
        print(f"    {t:12s} {ok:6d}/{n:6d}  {ok/n:.1%}")

    print(f"\n  surumu bulunan belge: {sum(1 for v in surumler.values() if v)}"
          f"/{len(surumler)}")
    if a.detay:
        for b in hepsi[:60]:
            print("   ", b)

    json.dump(dict(ozet=dict(sev), turler=dict(tip),
                   surumler=surumler, bulgular=hepsi[:2000]),
              open(RAPOR, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"  -> {RAPOR}")


if __name__ == "__main__":
    main()
