#!/usr/bin/env python
"""Arsivdeki tum PDF'leri Docling ile markdown'a cevirir.

Structural Validation markdown uzerinde calisiyor; arsivde 159 PDF var.
Bu script o on kosulu saglar. Yerel ve ucretsiz calisir, dis servise gitmez.

Devam edebilir: uretilmis .md dosyalarini atlar, yarida kesilirse kaldigi
yerden surer. Ilerleme _work/parsed/_batch_state.json icine yazilir.

Calistirma:
    TORCHDYNAMO_DISABLE=1 _env/parse/Scripts/python.exe _scripts/batch_docling.py
    ... --limit 20        (once kucuk bir parti dene)
"""
import argparse, json, os, subprocess, sys, time, traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))
from plog import log

KATMAN = ["layer1_clinical", "layer2_regulatory", "layer3_reimbursement"]
CIKTI = os.path.join(ROOT, "_work", "parsed")
DURUM = os.path.join(CIKTI, "_batch_state.json")


def hedefler():
    p = []
    for k in KATMAN:
        for kok, _, fs in os.walk(os.path.join(ROOT, k)):
            p += [os.path.join(kok, f) for f in fs if f.lower().endswith(".pdf")]
    return sorted(p)


def cikti_adi(pdf):
    rel = os.path.relpath(pdf, ROOT)
    return os.path.join(CIKTI, rel.replace(os.sep, "__")[:-4] + ".md")


METIN_ESIGI = 200          # sayfa basina karakter: uzerindeyse metin katmani var


def metin_yogunlugu(pdf):
    import fitz
    d = fitz.open(pdf)
    return sum(len(p.get_text()) for p in d) / d.page_count if d.page_count else 0.0


def tek_donustur(pdf):
    """Alt surecte tek bir PDF cevirir.

    Iki yol:
      - metin katmani olan PDF (KUB, FDA/EMA etiketi gibi sablonlu belgeler)
        -> pymupdf4llm. Hizli, bellek dostu, yapiyi markdown olarak verir.
      - metin katmani olmayan / cizim agirlikli PDF -> Docling layout modeli.

    Docling'i her belgeye uygulamak 48/104 belgede std::bad_alloc uretti:
    metin PDF'ine OCR duzeyinde layout analizi hem gereksiz hem bellek yiyor.
    Alt surec izolasyonu ayrica bir cokmenin partiyi dusurmesini engelliyor.
    """
    yog = metin_yogunlugu(pdf)
    if yog >= METIN_ESIGI:
        import pymupdf4llm
        md = pymupdf4llm.to_markdown(pdf, show_progress=False)
        yol = "pymupdf4llm"
    else:
        from docling.document_converter import DocumentConverter
        md = DocumentConverter().convert(pdf).document.export_to_markdown()
        yol = "docling"
    with open(cikti_adi(pdf), "w", encoding="utf-8") as f:
        f.write(md)
    print(f"KRK {len(md)} YOL {yol} YOGUNLUK {round(yog)}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="0 = hepsi")
    ap.add_argument("--tek", help="alt surec modu: tek PDF cevir")
    ap.add_argument("--zaman-asimi", type=int, default=900)
    a = ap.parse_args()

    os.makedirs(CIKTI, exist_ok=True)
    if a.tek:
        tek_donustur(a.tek)
        return

    pdfs = hedefler()
    if a.limit:
        pdfs = pdfs[:a.limit]
    log("docling toplu donusum basladi", "parse-batch", f"{len(pdfs)} PDF")

    ok = hata = atla = 0
    for i, pdf in enumerate(pdfs, 1):
        out = cikti_adi(pdf)
        ad = os.path.basename(out)
        if os.path.exists(out) and os.path.getsize(out) > 0:
            atla += 1
            continue
        t0 = time.time()
        try:
            r = subprocess.run([sys.executable, os.path.abspath(__file__),
                                "--tek", pdf],
                               capture_output=True, text=True,
                               encoding="utf-8", errors="replace",
                               timeout=a.zaman_asimi, cwd=ROOT)
            if r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 0:
                ok += 1
                print(f"[{i}/{len(pdfs)}] OK {round(time.time()-t0,1)}sn {ad}",
                      flush=True)
            else:
                hata += 1
                son = (r.stderr or r.stdout or "").strip().splitlines()
                print(f"[{i}/{len(pdfs)}] HATA rc={r.returncode} {ad} :: "
                      f"{son[-1][:120] if son else 'cikti yok'}", flush=True)
        except subprocess.TimeoutExpired:
            hata += 1
            print(f"[{i}/{len(pdfs)}] ZAMAN ASIMI {ad}", flush=True)

        with open(DURUM, "w", encoding="utf-8") as f:
            json.dump(dict(toplam=len(pdfs), islenen=i, ok=ok, hata=hata, atla=atla,
                           son=ad, guncelleme=time.strftime("%Y-%m-%d %H:%M:%S")),
                      f, indent=1, ensure_ascii=False)
        if i % 25 == 0:
            log("docling ilerleme", "parse-batch",
                f"{i}/{len(pdfs)} ok={ok} hata={hata} atla={atla}")

    log("docling toplu donusum bitti", "parse-batch",
        f"ok={ok} hata={hata} atla={atla}")
    print(f"BITTI ok={ok} hata={hata} atla={atla}")


if __name__ == "__main__":
    main()
