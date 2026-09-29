#!/usr/bin/env python
"""Bozuk donusumleri duz metin cikaricisiyla yeniden uretir.

Neden: pymupdf4llm bazi KUB'lerde metni ikileyip bozuyor. Ornek (REVLIMID):
    "### **4.5 4.5 D er t urunler runler ile etkile ile mler ve ve er etkile ekilleri**"
Bu bir baslik sorunu degil, ICERIK bozulmasi - harfler dusuyor ve blok
tekrarlaniyor. Ayni PDF'te duz `page.get_text()` tertemiz cikiyor, cunku
markdown donusturucunun span birlestirme adimi ust uste binen metin
katmanlarinda cuvalliyor.

Bu yuzden bozuk belgeler icin yol degistirilir: yapiyi zenginlestirme adimi
zaten kanonik bolum sozlugunden kuruyor, dolayisiyla markdown'in kendi baslik
tahminine ihtiyac yok. Duz metin daha guvenli.

Ek kazanc: sayfa siniri `<!-- sayfa N -->` olarak isaretlenir; chunk'larin
page_number alani buradan gelir.

Calistirma:
    _env/parse/Scripts/python.exe _scripts/repair_parsed.py --tespit
    _env/parse/Scripts/python.exe _scripts/repair_parsed.py --uygula
"""
import argparse, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))
from plog import log
import structural_validation as V

PARSED = os.path.join(ROOT, "_work", "parsed")
RAPOR = os.path.join(ROOT, "_logs", "enrich_report.json")
ESIK_EKSIK = 3             # bu kadar zorunlu bolumu kayip olan belge suphelidir


def ikilenme_orani(t):
    """Ard arda tekrarlanan kelime orani. "4.5 4.5 Doz Doz" kalibini yakalar."""
    k = re.findall(r"\w+", t[:200000])
    if len(k) < 200:
        return 0.0
    return sum(1 for i in range(1, len(k)) if k[i] == k[i - 1]) / len(k)


def adaylar():
    rap = json.load(open(RAPOR, encoding="utf-8"))
    idx = V.KAYNAK_INDEKS()
    import fitz
    out = []
    for r in rap:
        if len(r["eksik"]) < ESIK_EKSIK:
            continue
        pdf = idx.get(r["dosya"])
        if not pdf:
            continue
        d = fitz.open(pdf)
        ham = sum(len(p.get_text()) for p in d)
        if ham < 500:
            continue           # taranmis belge: OCR isi, bu scriptin kapsami disi
        md = open(os.path.join(PARSED, r["dosya"]), encoding="utf-8",
                  errors="replace").read()
        out.append(dict(dosya=r["dosya"], pdf=pdf, eksik=len(r["eksik"]),
                        sayfa=d.page_count, kaynak_krk=ham, md_krk=len(md),
                        ikilenme=round(ikilenme_orani(md), 3)))
    return out


def yeniden_yaz(pdf, hedef):
    import fitz
    d = fitz.open(pdf)
    parca = [f"<!-- sayfa {i + 1} -->\n" + p.get_text("text")
             for i, p in enumerate(d)]
    metin = "\n".join(parca)
    with open(hedef, "w", encoding="utf-8") as f:
        f.write(metin)
    return len(metin)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tespit", action="store_true")
    ap.add_argument("--uygula", action="store_true")
    a = ap.parse_args()

    ad = adaylar()
    print(f"{len(ad)} metin katmanli belge, {ESIK_EKSIK}+ zorunlu bolumu eksik\n")
    for x in sorted(ad, key=lambda x: -x["ikilenme"]):
        print(f"  eksik {x['eksik']:2d} | {x['sayfa']:3d}s | kaynak {x['kaynak_krk']:7d} "
              f"-> md {x['md_krk']:7d} | ikilenme {x['ikilenme']:.3f} | "
              f"{x['dosya'].split('__')[-1][:34]}")

    if not a.uygula:
        return
    for x in ad:
        n = yeniden_yaz(x["pdf"], os.path.join(PARSED, x["dosya"]))
        print(f"  yeniden yazildi {n:7d} krk  {x['dosya'].split('__')[-1][:44]}")
    log("bozuk donusum onarimi", "repair",
        f"{len(ad)} belge duz metin cikaricisiyla yeniden uretildi")


if __name__ == "__main__":
    main()
