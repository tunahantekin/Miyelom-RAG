#!/usr/bin/env python
"""Clinical Recall: parser ciktisi MYEL-1'deki klinik karar bilgisini koruyor mu?

Ground truth: _work/parse_bakeoff/truth/myel1_truth.json
  (sayfa PNG'ye render edilip gozle cikarildi, hicbir parser ciktisi kullanilmadi)

Iki olcum uretilir:
  recall          -> madde belgenin HERHANGI bir yerinde bulunuyor mu
  pencere_recall  -> madde tek bir 8000 karakterlik pencerede TOPLU bulunuyor mu
                     (makale govde metni sema icerigini taklit edebilir; pencere
                      kisiti "sema blok halinde korunmus mu" sorusunu olcer)

Calistirma:
    _env/parse/Scripts/python.exe _scripts/clinical_recall.py
    _env/parse/Scripts/python.exe _scripts/clinical_recall.py --md yol/x.md --etiket nccn141
"""
import os, re, sys, json, bisect, argparse, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))
from plog import log

BAKE = os.path.join(ROOT, "_work", "parse_bakeoff")
TRUTH = os.path.join(BAKE, "truth", "myel1_truth.json")
OUTJS = os.path.join(BAKE, "truth", "clinical_recall.json")
PENCERE = 8000
ADIM = 500

# Govde metni sema icerigini taklit edebiliyor (or. FISH sitogenetik listesi hem
# MYEL-1 kutusunda hem "Cytogenetics" paragrafinda gecer), bu yuzden belge-geneli
# recall yaniltici. Baslik capasi denendi ama belgeden belgeye kaydi; bunun yerine
# maddelerin EN COK bir arada durdugu BLOK penceresi olcut aliniyor: sema blok
# halinde korunduysa maddeler tek pencereye sigar, dagildiysa sigmaz.
BLOK = 6000


def normalize(t):
    """Parser bicim farklarini silip icerigi karsilastirilabilir hale getirir."""
    t = unicodedata.normalize("NFKD", t)
    t = t.replace("–", "-").replace("—", "-").replace("−", "-")
    t = re.sub(r"<[^>]+>", " ", t)           # html etiketleri (unstructured tablolari)
    t = t.replace("&amp;", "&").replace("&nbsp;", " ")
    t = re.sub(r"-\s*\n\s*", "", t)          # satir sonu tirelemesi: immuno-\nfixation
    t = t.lower()
    t = re.sub(r"[*#>_`|]", " ", t)          # markdown suslemesi
    t = re.sub(r"\s+", " ", t)
    return t


def konumlar(metin, desen):
    try:
        rx = re.compile(desen)
    except re.error:
        rx = re.compile(re.escape(desen))
    return [m.start() for m in rx.finditer(metin)]


def _aralikta(konum, bas, son):
    i = bisect.bisect_left(konum, bas)
    return i < len(konum) and konum[i] < son


def en_yogun_blok(metin, maddeler, idx, genislik):
    """Maddelerin en cok bir arada durdugu pencereyi bulur -> (baslangic, id_kumesi)."""
    en_iyi, bas_iyi, set_iyi = 0, 0, set()
    for bas in range(0, max(1, len(metin) - genislik + 1), ADIM):
        son = bas + genislik
        s = {m["id"] for m in maddeler
             if all(_aralikta(k, bas, son) for k in idx[m["id"]])}
        if len(s) > en_iyi:
            en_iyi, bas_iyi, set_iyi = len(s), bas, s
    return bas_iyi, set_iyi


def degerlendir(ham, maddeler):
    metin = normalize(ham)
    idx = {}                                  # madde id -> [her desenin konum listesi]
    sonuc = []
    for m in maddeler:
        konum = [konumlar(metin, d) for d in m["desenler"]]
        idx[m["id"]] = konum
        eksik = [d for d, k in zip(m["desenler"], konum) if not k]
        sonuc.append(dict(id=m["id"], grup=m["grup"], agirlik=m["agirlik"],
                          etiket=m["etiket"], bulundu=not eksik, eksik_desen=eksik))

    blok_bas, blok_set = en_yogun_blok(metin, maddeler, idx, BLOK)
    genis_bas, genis_set = en_yogun_blok(metin, maddeler, idx, PENCERE)
    for r in sonuc:
        r["figurde"] = r["id"] in blok_set
        r["pencerede"] = r["id"] in genis_set
    return sonuc, genis_bas, len(metin), (blok_bas, blok_bas + BLOK)


def ozet(parser, sonuc, pencere_bas, uzunluk, figur):
    krit = [r for r in sonuc if r["agirlik"] == "kritik"]

    def orn(xs, alan):
        return round(sum(1 for r in xs if r[alan]) / len(xs), 3) if xs else 0.0

    gruplar = {}
    for r in sonuc:
        g = gruplar.setdefault(r["grup"], [0, 0, 0])
        g[2] += 1
        g[0] += 1 if r["bulundu"] else 0
        g[1] += 1 if r["figurde"] else 0
    return dict(
        parser=parser, uzunluk=uzunluk, toplam=len(sonuc),
        yakalanan=sum(1 for r in sonuc if r["bulundu"]),
        recall=orn(sonuc, "bulundu"),
        figur_yakalanan=sum(1 for r in sonuc if r["figurde"]),
        figur_recall=orn(sonuc, "figurde"),
        figur_kritik_yakalanan=sum(1 for r in krit if r["figurde"]),
        figur_kritik_recall=orn(krit, "figurde"),
        figur_aralik=list(figur),
        kritik_toplam=len(krit),
        kritik_yakalanan=sum(1 for r in krit if r["bulundu"]),
        kritik_recall=orn(krit, "bulundu"),
        pencere_yakalanan=sum(1 for r in sonuc if r["pencerede"]),
        pencere_recall=orn(sonuc, "pencerede"),
        pencere_baslangic=pencere_bas,
        grup_recall={k: f"belge {v[0]}/{v[2]}, figur {v[1]}/{v[2]}"
                     for k, v in gruplar.items()},
        kacan=[dict(id=r["id"], etiket=r["etiket"], eksik_desen=r["eksik_desen"])
               for r in sonuc if not r["bulundu"]],
        figur_kacan=[dict(id=r["id"], etiket=r["etiket"], belgede=r["bulundu"])
                     for r in sonuc if not r["figurde"]],
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", nargs="*", default=None, help="tekil markdown dosyalari")
    ap.add_argument("--etiket", nargs="*", default=None, help="--md ile ayni sirada isimler")
    a = ap.parse_args()

    truth = json.load(open(TRUTH, encoding="utf-8"))
    maddeler = truth["maddeler"]

    hedefler = []
    if a.md:
        for i, p in enumerate(a.md):
            ad = a.etiket[i] if a.etiket and i < len(a.etiket) else os.path.basename(p)
            hedefler.append((ad, p))
    else:
        for parser in sorted(os.listdir(os.path.join(BAKE, "output"))):
            p = os.path.join(BAKE, "output", parser, "nccn.md")
            if os.path.exists(p) and os.path.getsize(p) > 0:
                hedefler.append((parser, p))

    ozetler, detay = [], {}
    for ad, p in hedefler:
        ham = open(p, encoding="utf-8", errors="replace").read()
        sonuc, pb, uz, fig = degerlendir(ham, maddeler)
        o = ozet(ad, sonuc, pb, uz, fig)
        ozetler.append(o)
        detay[ad] = sonuc
        log(f"clinical recall: {ad}", "clinical-recall",
            f"belge {o['yakalanan']}/{o['toplam']} (recall {o['recall']}), "
            f"figur {o['figur_yakalanan']}/{o['toplam']} (recall {o['figur_recall']}), "
            f"figur-kritik {o['figur_kritik_yakalanan']}/{o['kritik_toplam']}")

    json.dump(dict(kaynak=truth["kaynak"], pencere=PENCERE, ozet=ozetler, detay=detay),
              open(OUTJS, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    print("\n=== CLINICAL RECALL (MYEL-1) ===")
    print("belge_* = belgenin herhangi bir yerinde (govde metni de sayilir)")
    print("figur_* = MYEL-1 figur blogunun icinde (asil olcut)\n")
    kol = ["parser", "toplam", "yakalanan", "recall", "kritik_recall",
           "figur_yakalanan", "figur_recall", "figur_kritik_yakalanan",
           "kritik_toplam", "figur_kritik_recall"]
    print(" | ".join(kol))
    for o in ozetler:
        print(" | ".join(str(o[k]) for k in kol))

    for o in ozetler:
        print(f"\n-- {o['parser']} grup bazinda: {o['grup_recall']}")
        if o["figur_kacan"]:
            print(f"   FIGURDE YOK ({len(o['figur_kacan'])}):")
            for k in o["figur_kacan"]:
                nerede = "govdede var, semada yok" if k["belgede"] else "hic yok"
                print(f"     {k['id']} {k['etiket'][:66]}  <- {nerede}")
    print(f"\nayrinti: {OUTJS}")


if __name__ == "__main__":
    main()
