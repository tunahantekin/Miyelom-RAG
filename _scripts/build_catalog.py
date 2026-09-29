#!/usr/bin/env python
"""Data Catalog uretici.

Arsivdeki her belge icin: isim, surum, tarih, kaynak, hastalik, dil, format
(+ katman, alt_kaynak, sayfa, boyut_kb, yol) cikarir.

Tarihler nereden geliyor:
  - TITCK KUB      -> titck.gov.tr KUB/KT servisinden "confirmationDateKub"
  - FDA etiketleri -> PDF metninden "Revised: MM/YYYY"
  - EMA / kilavuz  -> asagidaki CURATED tablosundan (elle dogrulanmis)

Calistirma:  python _scripts/build_catalog.py
"""
import os, re, csv, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))
from plog import log

UNK = "?"

# --- elle dogrulanmis meta (otomatik cikarilamayanlar) ---------------------
CURATED = {
    "jnccn-article-e260001.pdf": dict(
        isim="NCCN Guidelines Insights: Multiple Myeloma", surum="Version 5.2026",
        tarih="2026-01-01", kaynak="NCCN / JNCCN", hastalik="multipl miyelom", dil="en"),
    "myeloma.pdf": dict(
        isim="NCCN Clinical Practice Guidelines in Oncology: Multiple Myeloma (tam kilavuz, MYEL-1..MYEL-L)",
        surum="Version 5.2026", tarih="2026-01-09", kaynak="NCCN (nccn.org, uyelik gerekli)",
        hastalik="multipl miyelom", dil="en"),
    "esmo.pdf": dict(
        isim="Multiple Myeloma: EHA-ESMO Clinical Practice Guidelines", surum="EHA-ESMO CPG",
        tarih=UNK, kaynak="EHA + ESMO (Annals of Oncology)", hastalik="multipl miyelom", dil="en"),
    "NCI_PDQ_myeloma_HP_2026.pdf": dict(
        isim="Plasma Cell Neoplasms (Including MM) Treatment - PDQ Health Professional",
        surum="PDQ HP", tarih="2026-08-04", kaynak="NCI / cancer.gov",
        hastalik="plazma hucre neoplazmlari", dil="en"),
    "SUT.pdf": dict(
        isim="Saglik Uygulama Tebligi (SUT)", surum="guncel metin", tarih=UNK,
        kaynak="SGK", hastalik="genel (tum endikasyonlar)", dil="tr"),
    "appendix_fda.pdf": dict(
        isim="Orange Book Appendix A - Product Name Index", surum="Haziran 2026",
        tarih="2026-06-01", kaynak="FDA Orange Book", hastalik="genel (tum endikasyonlar)", dil="en"),
}

EK_ADLARI = {
    "EK-4A":  "Bedeli Odenecek Ilaclar Listesi",
    "EK-4B":  "Hastaliga Ozel (Dogustan Metabolik) Urunler Listesi",
    "EK-4-D": "Hasta Katilim Payindan Muaf Ilaclar Listesi",
    "EK-4-E": "Sistemik Antimikrobik ve Diger Ilaclarin Receteleme Kurallari",
    "EK-4-F": "Ayakta Tedavide Saglik Raporu ile Verilebilecek Ilaclar Listesi",
    "EK-4-G": "Sadece Yatan Hastalarda Bedeli Odenecek Ilaclar Listesi",
    "EK-4H":  "Hastanelerce Temini Zorunlu Kemoterapi Ilaclari Listesi",
}

KAYNAK = {
    "layer1_clinical/nccn": "NCCN / JNCCN",
    "layer1_clinical/esmo": "EHA + ESMO",
    "layer1_clinical/nci_pdq": "NCI / cancer.gov",
    "layer1_clinical/asco": "ASCO / JCO",
    "layer1_clinical/pubmed_meta": "PubMed Central (acik erisim)",
    "layer2_regulatory/fda/labels": "FDA (DailyMed / NLM)",
    "layer2_regulatory/fda/orange_book": "FDA Orange Book",
    "layer2_regulatory/ema": "EMA (ema.europa.eu)",
    "layer2_regulatory/titck/kub": "TITCK (titck.gov.tr)",
    "layer2_regulatory/titck/ruhsat_listesi": "TITCK (titck.gov.tr)",
    "layer3_reimbursement/sut": "SGK",
    "layer3_reimbursement/ek4": "SGK",
}


def pdf_meta(path):
    """sayfa sayisi ve ilk sayfa metni"""
    try:
        from pypdf import PdfReader
        r = PdfReader(path)
        return len(r.pages), (r.pages[0].extract_text() or "")
    except Exception:
        return UNK, ""


def fda_revision(text):
    m = re.search(r"Revised:\s*(\d{1,2})/(\d{4})", text)
    if m:
        return f"{m.group(2)}-{int(m.group(1)):02d}-01", f"rev-{m.group(2)}-{int(m.group(1)):02d}"
    m = re.search(r"Initial U\.S\. Approval:\s*(\d{4})", text)
    if m:
        return UNK, f"ilk onay {m.group(1)}"
    return UNK, UNK


def titck_dates():
    """KUB dosya adi -> (onay tarihi, firma, etken madde). Ag yoksa bos doner."""
    out = {}
    try:
        import requests
    except ImportError:
        return out
    try:
        s = requests.Session()
        s.headers.update({"User-Agent": "Mozilla/5.0"})
        h = s.get("https://www.titck.gov.tr/kubkt", timeout=60).text
        tok = re.search(r'_token:\s*"([^"]+)"', h).group(1)
        cols = ["name", "element", "firmName", "confirmationDateKub",
                "confirmationDateKt", "documentPathKub", "documentPathKt"]
        terms = ["daratumumab", "isatuximab", "karfilzomib", "carfilzomib", "iksazomib",
                 "lenalidomid", "pomalidomid", "bortezomib", "selineksor", "talidomid",
                 "elranatamab", "melfalan", "zoledronik", "denosumab"]
        for t in terms:
            d = {"_token": tok, "draw": 1, "start": 0, "length": 200,
                 "search[value]": t, "search[regex]": "false",
                 "order[0][column]": 0, "order[0][dir]": "asc"}
            for i, c in enumerate(cols):
                d[f"columns[{i}][data]"] = c
                d[f"columns[{i}][name]"] = ""
                d[f"columns[{i}][searchable]"] = "true"
                d[f"columns[{i}][orderable]"] = "true"
                d[f"columns[{i}][search][value]"] = ""
                d[f"columns[{i}][search][regex]"] = "false"
            rows = s.post("https://www.titck.gov.tr/getkubktviewdatatable", data=d,
                          headers={"X-Requested-With": "XMLHttpRequest",
                                   "Referer": "https://www.titck.gov.tr/kubkt"},
                          timeout=60).json().get("data", [])
            for r in rows:
                m = re.search(r'href="([^"]+\.pdf)"', r.get("documentPathKub") or "")
                if not m:
                    continue
                el = re.sub(r"[^A-Za-z0-9]+", "_", (r.get("element") or "NA"))[:30]
                nm = re.sub(r"[^A-Za-z0-9]+", "_", (r.get("name") or "NA"))[:60]
                key = f"{el}__{nm}_KUB.pdf"
                dt = (r.get("confirmationDateKub") or "").strip()
                iso = UNK
                if re.match(r"\d{2}/\d{2}/\d{4}", dt):
                    g, a, y = dt.split("/")
                    iso = f"{y}-{a}-{g}"
                out[key] = (iso, (r.get("firmName") or "").strip(),
                            (r.get("element") or "").strip())
    except Exception as e:
        log("TITCK tarih cekimi basarisiz", "katalog", str(e)[:150])
    return out


def main():
    log("Data Catalog uretimi basladi", "katalog")
    tdates = titck_dates()
    log("TITCK KUB tarihleri cekildi", "katalog", f"{len(tdates)} kayit")

    rows = []
    for dirpath, _, files in os.walk(ROOT):
        rel = os.path.relpath(dirpath, ROOT).replace("\\", "/")
        if rel.startswith(("_env", "_logs", "_scripts", "_work", ".")):
            continue
        for fn in sorted(files):
            if not fn.lower().endswith((".pdf", ".xlsx")):
                continue
            full = os.path.join(dirpath, fn)
            relpath = os.path.relpath(full, ROOT).replace("\\", "/")
            katman = rel.split("/")[0] if rel != "." else "kok"
            alt = "/".join(rel.split("/")[1:]) or "-"
            fmt = fn.rsplit(".", 1)[-1].lower()
            boyut = round(os.path.getsize(full) / 1024)

            sayfa, first = (UNK, "")
            if fmt == "pdf":
                sayfa, first = pdf_meta(full)

            c = CURATED.get(fn)
            if c:
                isim, surum, tarih = c["isim"], c["surum"], c["tarih"]
                kaynak, hastalik, dil = c["kaynak"], c["hastalik"], c["dil"]
            elif rel.endswith("fda/labels"):
                marka = fn.replace("FDA_", "").replace("_PI.pdf", "").replace("_", " ")
                tarih, surum = fda_revision(first)
                isim = f"{marka} - FDA Prescribing Information"
                kaynak, hastalik, dil = KAYNAK[rel], "multipl miyelom", "en"
            elif rel.endswith("/ema"):
                marka = fn.replace("EMA_", "").replace("_PI.pdf", "").capitalize()
                isim = f"{marka} - EMA EPAR Product Information"
                surum, tarih = "guncel EPAR", UNK
                kaynak, hastalik, dil = KAYNAK[rel], "multipl miyelom", "en"
            elif rel.endswith("titck/kub"):
                d = tdates.get(fn, (UNK, "", ""))
                etken = d[2] or fn.split("__")[0].replace("_", " ")
                urun = fn.split("__", 1)[-1].replace("_KUB.pdf", "").replace("_", " ")
                isim = f"{urun} - Kisa Urun Bilgisi (KUB)"
                surum = f"KUB onay {d[0]}" if d[0] != UNK else "KUB"
                tarih = d[0]
                kaynak = KAYNAK[rel] + (f" / {d[1]}" if d[1] else "")
                destek = any(x in etken.lower() for x in ("zoledron", "denosumab"))
                hastalik = "miyelom kemik hastaligi (destek)" if destek else "multipl miyelom"
                dil = "tr"
            elif rel.endswith("titck/ruhsat_listesi"):
                isim = "Ruhsatli Beseri Tibbi Urunler Listesi"
                surum, tarih = "31.07.2026", "2026-07-31"
                kaynak, hastalik, dil = KAYNAK[rel], "genel (tum endikasyonlar)", "tr"
            elif rel.endswith("/asco"):
                isim = "Treatment of Multiple Myeloma: ASCO Living Guideline"
                m = re.search(r"version-(\d{4})-(\d+)-(\d+)", fn)
                surum = f"Version {m.group(1)}.{m.group(2)}.{m.group(3)}" if m else "Living Guideline"
                tarih = "2026-01-06"
                kaynak, hastalik, dil = KAYNAK[rel], "multipl miyelom", "en"
            elif rel.endswith("pubmed_meta"):
                isim = fn.replace("PUBMED_META_", "").replace(".pdf", "").replace("_", " ")
                surum, tarih = "meta-analiz", UNK
                kaynak, hastalik, dil = KAYNAK[rel], "multipl miyelom", "en"
            elif rel.endswith("ek4"):
                key = next((k for k in EK_ADLARI if fn.startswith(k)), None)
                isim = EK_ADLARI.get(key, fn)
                surum, tarih = "guncel liste", UNK
                kaynak, hastalik, dil = KAYNAK[rel], "genel (tum endikasyonlar)", "tr"
            else:
                isim, surum, tarih = fn, UNK, UNK
                kaynak, hastalik, dil = KAYNAK.get(rel, UNK), UNK, UNK

            rows.append(dict(isim=isim, surum=surum, tarih=tarih, kaynak=kaynak,
                             hastalik=hastalik, dil=dil, format=fmt, katman=katman,
                             alt_kaynak=alt, sayfa=sayfa, boyut_kb=boyut, yol=relpath))

    cols = ["isim", "surum", "tarih", "kaynak", "hastalik", "dil", "format",
            "katman", "alt_kaynak", "sayfa", "boyut_kb", "yol"]
    with open(os.path.join(ROOT, "DATA_CATALOG.csv"), "w", newline="",
              encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    with open(os.path.join(ROOT, "DATA_CATALOG.md"), "w", encoding="utf-8") as f:
        f.write(f"# Data Catalog\n\nUretim: {datetime.datetime.now():%Y-%m-%d %H:%M}  |  "
                f"Toplam belge: **{len(rows)}**\n\n")
        for kat in ["layer1_clinical", "layer2_regulatory", "layer3_reimbursement", "kok"]:
            sub = [r for r in rows if r["katman"] == kat]
            if not sub:
                continue
            f.write(f"\n## {kat} ({len(sub)} belge)\n\n")
            f.write("| isim | surum | tarih | kaynak | hastalik | dil | format | sayfa |\n")
            f.write("|---|---|---|---|---|---|---|---|\n")
            for r in sub:
                v = {k: str(x).replace("|", "/") for k, x in r.items()}
                f.write("| {isim} | {surum} | {tarih} | {kaynak} | {hastalik} | {dil} | "
                        "{format} | {sayfa} |\n".format(**v))

    tarihli = sum(1 for r in rows if r["tarih"] != UNK)
    log("Data Catalog uretildi", "katalog",
        f"{len(rows)} belge, {tarihli} tanesinde tarih -> DATA_CATALOG.csv + .md")
    print(f"OK: {len(rows)} belge kataloglandi ({tarihli} tarihli). "
          f"Cikti: DATA_CATALOG.csv, DATA_CATALOG.md")


if __name__ == "__main__":
    main()
