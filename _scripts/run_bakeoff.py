#!/usr/bin/env python
"""NCCN PDF uzerinde 4 parser karsilastirmasi.

Girdi : _work/parse_bakeoff/input/nccn_myeloma_v5_2026.pdf
Cikti : _work/parse_bakeoff/output/<parser>/nccn.md
        _work/parse_bakeoff/metrics.json

Calistirma (izole venv ile):
    _env/parse/Scripts/python.exe _scripts/run_bakeoff.py
    _env/parse/Scripts/python.exe _scripts/run_bakeoff.py --only docling
"""
import os, re, sys, json, time, argparse, traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))
from plog import log

PDF = os.path.join(ROOT, "_work", "parse_bakeoff", "input", "nccn_myeloma_v5_2026.pdf")
OUT = os.path.join(ROOT, "_work", "parse_bakeoff", "output")
MET = os.path.join(ROOT, "_work", "parse_bakeoff", "metrics.json")

# NCCN akis semalarinin (MYEL-*) icinde gecen, duz metin cikariminda kaybolan
# karakteristik ifadeler. Ground truth olarak bunlarin yakalanmasina bakiyoruz.
FLOW_TERMS = [
    "Primary Therapy", "Maintenance", "Smoldering", "Solitary Plasmacytoma",
    "Active Myeloma", "Workup", "Follow-Up", "Relapse", "Transplant",
    "Preferred Regimens", "Other Recommended", "Useful in Certain Circumstances",
]


def metrics(md, sure, parser, hata=""):
    md = md or ""
    return dict(
        parser=parser,
        sure_sn=round(sure, 1),
        hata=hata,
        karakter=len(md),
        baslik_sayisi=len(re.findall(r"(?m)^#{1,6}\s+\S", md)),
        tablo_satiri=len(re.findall(r"(?m)^\s*\|.*\|\s*$", md)),
        tablo_ayraci=len(re.findall(r"(?m)^\s*\|[\s:|-]+\|\s*$", md)),
        html_tablo=len(re.findall(r"<table", md, re.I)),
        myel_kodu=len(set(re.findall(r"MYEL-[0-9A-Z]+", md))),
        myel_toplam=len(re.findall(r"MYEL-[0-9A-Z]+", md)),
        akis_terimi=sum(1 for t in FLOW_TERMS if t.lower() in md.lower()),
        figur_altyazi=len(re.findall(r"(?im)^\s*.{0,8}Figure\s+\d+[.:]", md)),
        dipnot_isareti=len(re.findall(r"(?m)^\s*[a-z]\)\s|\bFootnote", md)),
        referans_no=len(re.findall(r"\[\d{1,3}\]|\b\d{1,3}\.\s+[A-Z][a-z]+ [A-Z]", md)),
    )


def save(parser, md):
    d = os.path.join(OUT, parser)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "nccn.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write(md or "")
    return p


def run_docling():
    from docling.document_converter import DocumentConverter
    conv = DocumentConverter()
    res = conv.convert(PDF)
    return res.document.export_to_markdown()


def run_marker():
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.output import text_from_rendered
    conv = PdfConverter(artifact_dict=create_model_dict())
    rendered = conv(PDF)
    txt, _, _ = text_from_rendered(rendered)
    return txt


def run_unstructured():
    from unstructured.partition.pdf import partition_pdf
    els = partition_pdf(filename=PDF, strategy="hi_res", infer_table_structure=True)
    parts = []
    for e in els:
        cat = type(e).__name__
        txt = (e.text or "").strip()
        if cat == "Title":
            parts.append(f"## {txt}")
        elif cat == "Table":
            html = getattr(e.metadata, "text_as_html", None)
            parts.append(html or txt)
        elif txt:
            parts.append(txt)
    return "\n\n".join(parts)


def run_llamaparse():
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT, ".env"))
    key = os.getenv("LLAMA_CLOUD_API_KEY")
    if not key:
        raise RuntimeError("LLAMA_CLOUD_API_KEY yok - .env dosyasina ekleyin")
    from llama_parse import LlamaParse
    p = LlamaParse(api_key=key, result_type="markdown")
    docs = p.load_data(PDF)
    return "\n\n".join(d.text for d in docs)


RUNNERS = {"docling": run_docling, "marker": run_marker,
           "unstructured": run_unstructured, "llamaparse": run_llamaparse}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=list(RUNNERS))
    a = ap.parse_args()

    if not os.path.exists(PDF):
        sys.exit(f"girdi yok: {PDF}")

    sonuc = []
    if os.path.exists(MET):
        sonuc = json.load(open(MET, encoding="utf-8"))
    sonuc = [r for r in sonuc if r["parser"] not in a.only]

    for name in a.only:
        if name not in RUNNERS:
            continue
        log(f"{name} calistiriliyor", "parse-bakeoff", os.path.basename(PDF))
        t0 = time.time()
        try:
            md = RUNNERS[name]()
            sure = time.time() - t0
            p = save(name, md)
            m = metrics(md, sure, name)
            log(f"{name} bitti", "parse-bakeoff",
                f"{m['sure_sn']}sn, {m['karakter']} krk, {m['baslik_sayisi']} baslik, "
                f"{m['tablo_satiri']} tablo satiri, {m['myel_kodu']} MYEL kodu -> {p}")
        except Exception as e:
            sure = time.time() - t0
            hata = f"{type(e).__name__}: {e}"
            m = metrics("", sure, name, hata[:300])
            log(f"{name} HATA", "parse-bakeoff", hata[:200])
            traceback.print_exc()
        sonuc.append(m)
        json.dump(sonuc, open(MET, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(json.dumps(m, ensure_ascii=False, indent=1))

    print("\n=== OZET ===")
    kolon = ["parser", "sure_sn", "karakter", "baslik_sayisi", "tablo_satiri",
             "html_tablo", "myel_kodu", "akis_terimi", "dipnot_isareti", "hata"]
    print(" | ".join(kolon))
    for r in sorted(sonuc, key=lambda x: x["parser"]):
        print(" | ".join(str(r.get(k, ""))[:28] for k in kolon))


if __name__ == "__main__":
    main()
