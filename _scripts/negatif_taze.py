#!/usr/bin/env python
"""Taze negatif kume ile alan kapisi olcumu - dil modeli kosmadan.

NEDEN AYRI BIR SCRIPT

Ilk negatif kumedeki N14 ("KOAH alevlenmesinde sistemik steroid"), sinif
sozlugunde ciplak "steroid" kelimesinin deksametazona eslesmesi yuzunden alan
ici sanilmisti. Hatayi duzelttik, ama N14 OLCUM yarisindaydi: duzeltmeden
sonraki rakam, sinavi gordukten sonra verilmis bir nottur. Bu yuzden 15 taze
negatif yazildi (N16-N30) ve kapinin esikleri DONDURULDU. Buradaki rakam
kirlenmemis tek rakamdir.

NE OLCULUYOR

Uretim sirasi: (1) arama skoru kapisi, (2) alan kapisi, (3) dil modeli,
(4) dayanak kapisi. Ilk iki kapi modeli hic cagirmadan calisiyor, yani
GPU'suz olculebiliyor. Burada olculen sey: taze negatiflerden kaci ilk iki
kapiyi asip modele ulasiyor. Bu sayi UYDURMA ICIN UST SINIRDIR - dorduncu
kapi bunlarin bir kismini daha eleyebilir. Kapiya takilan soru ise kesin
olarak uydurma uretemez, cunku model hic cagrilmiyor.

Calistirma:
    python _scripts/negatif_taze.py
    python _scripts/negatif_taze.py --sorular _work/eval/negative_queries.json
"""
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))

import pipeline as P
import qdrant_index as QI
import query_processing as QP

TAZE = os.path.join(ROOT, "_work", "eval", "negative_queries_v2.json")
RAPOR = os.path.join(ROOT, "_logs", "negatif_taze.json")

# A yarisindan secilmis, artik DONDURULMUS esikler. Bu dosya bunlari
# degistirmiyor; degistirseydi olcum yine kirlenmis olurdu.
ARAMA_ESIGI = 0.50
ALAN_KURAL = "varlik|hast75"


def alan_gecti(varlik, hast, kural=ALAN_KURAL):
    if kural == "kapali":
        return True
    if kural == "varlik":
        return varlik
    if kural == "hast75":
        return hast >= 0.75
    if kural == "varlik|hast100":
        return varlik or hast >= 1.0
    return varlik or hast >= 0.75          # varlik|hast75


def olc(sorular, k=4, istemci=None):
    # Colab'da bu fonksiyon defter surecinin ICINDEN cagriliyor: Qdrant yerel
    # modda depo klasorunu kilitliyor, yani defterde acik bir istemci varken
    # alt surec ayni depoyu acamiyor. Acik istemci varsa o kullaniliyor.
    kapat = istemci is None
    istemci = istemci or QI.ac()
    kayit = []
    try:
        for i, s in enumerate(sorular, start=1):
            analiz = QP.analiz(s["soru"])
            vek = P._sorgu_vektoru(s["soru"])
            noktalar = QI.ara(istemci, vek, k=P.ADAY, ilac=analiz["ilac"])
            if analiz["ilac"]:
                hedefli = QI.ara(istemci, vek, k=k, zorunlu_ilac=analiz["ilac"])
                varolan = {p.id for p in hedefli}
                noktalar = hedefli + [p for p in noktalar
                                      if p.id not in varolan]

            en_iyi = max((p.score for p in noktalar), default=0.0)
            secili = P.tekrar_ayikla(P.baglam_sec(noktalar,
                                                  analiz["ilac"]))[:k]
            hast = round(sum(1 for x in secili
                             if (x["nokta"].payload.get("disease") or []))
                         / max(1, len(secili)), 3)
            varlik = P.alan_skoru(s["soru"], analiz)["varlik"]

            arama_ok = en_iyi >= ARAMA_ESIGI
            alan_ok = alan_gecti(varlik, hast)
            gecti = arama_ok and alan_ok
            kayit.append({
                "id": s["id"], "soru": s["soru"],
                "zorluk": s.get("zorluk", ""),
                "arama_skoru": round(en_iyi, 3),
                "alan_varlik": varlik, "alan_hast": hast,
                "taninan": {t: analiz[t] for t in
                            ("ilac", "hastalik", "rejim", "sinif")
                            if analiz[t]},
                "arama_kapisi": "gecti" if arama_ok else "durdurdu",
                "alan_kapisi": "gecti" if alan_ok else "durdurdu",
                "modele_ulasti": gecti,
            })
            print(f"  {i}/{len(sorular)} {s['id']} skor {en_iyi:.2f} "
                  f"varlik {int(varlik)} hast {hast:.2f} "
                  f"{'MODELE ULASTI' if gecti else 'durduruldu'}", flush=True)
    finally:
        if kapat:
            istemci.close()
    return kayit


def ozetle(kayit, cikti=None, sorular_adi="negative_queries_v2.json"):
    """Ozet basar ve raporu yazar. main() ile defter hucresi ortak kullaniyor."""
    ulasan = [x for x in kayit if x["modele_ulasti"]]
    arama = [x for x in kayit if x["arama_kapisi"] == "durdurdu"]
    alan = [x for x in kayit if x["arama_kapisi"] == "gecti"
            and x["alan_kapisi"] == "durdurdu"]
    print(f"\nTOPLAM {len(kayit)} taze negatif")
    print(f"  arama kapisi durdurdu : {len(arama)}")
    print(f"  alan kapisi durdurdu  : {len(alan)}")
    print(f"  MODELE ULASAN         : {len(ulasan)}  (uydurma ust siniri)")
    for x in ulasan:
        print(f"    {x['id']} [{x['zorluk']}] skor {x['arama_skoru']} "
              f"taninan {x['taninan']}")

    veri = {"esikler": {"arama": ARAMA_ESIGI, "alan": ALAN_KURAL},
            "sorular": sorular_adi,
            "ozet": {"toplam": len(kayit), "arama_durdurdu": len(arama),
                     "alan_durdurdu": len(alan), "modele_ulasan": len(ulasan)},
            "kayitlar": kayit}
    if cikti:
        os.makedirs(os.path.dirname(cikti), exist_ok=True)
        json.dump(veri, open(cikti, "w", encoding="utf-8"), indent=1,
                  ensure_ascii=False)
        print(f"\nrapor: {cikti}")
    return veri


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sorular", default=TAZE)
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--cikti", default=RAPOR)
    a = ap.parse_args()

    sorular = json.load(open(a.sorular, encoding="utf-8"))
    print(f"{len(sorular)} taze negatif soru, esikler donduruldu "
          f"(arama {ARAMA_ESIGI}, alan '{ALAN_KURAL}'):")
    kayit = olc(sorular, a.k)
    ozetle(kayit, a.cikti, os.path.basename(a.sorular))


if __name__ == "__main__":
    main()
