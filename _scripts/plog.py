#!/usr/bin/env python
"""Proje log yardimcisi. Bundan sonraki her adim buradan loglanir.

Kullanim:
    python _scripts/plog.py "olay metni"
    python _scripts/plog.py --faz parse "docling calistirildi" --detay "27 sayfa, 412 sn"

Iki yere birden yazar:
    _logs/PROJECT_LOG.md    -> insan okur (append-only, markdown)
    _logs/project_log.jsonl -> makine okur (her satir bir JSON kaydi)
"""
import argparse, json, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGD = os.path.join(ROOT, "_logs")
MD   = os.path.join(LOGD, "PROJECT_LOG.md")
JL   = os.path.join(LOGD, "project_log.jsonl")


def log(olay, faz="genel", detay=""):
    os.makedirs(LOGD, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rec = {"ts": ts, "faz": faz, "olay": olay, "detay": detay}

    with open(JL, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    if not os.path.exists(MD):
        with open(MD, "w", encoding="utf-8") as f:
            f.write("# Proje Log - Multipl Miyelom Karar-Destek Arsivi\n\n"
                    "Append-only. Her satir `_scripts/plog.py` ile eklenir.\n\n"
                    "| Zaman | Faz | Olay | Detay |\n|---|---|---|---|\n")
    with open(MD, "a", encoding="utf-8") as f:
        d = detay.replace("|", "\\|").replace("\n", " ")
        o = olay.replace("|", "\\|").replace("\n", " ")
        f.write(f"| {ts} | {faz} | {o} | {d} |\n")
    return rec


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("olay")
    ap.add_argument("--faz", default="genel")
    ap.add_argument("--detay", default="")
    a = ap.parse_args()
    r = log(a.olay, a.faz, a.detay)
    print(f"[{r['ts']}] ({r['faz']}) {r['olay']}" + (f" - {r['detay']}" if r["detay"] else ""))
