#!/usr/bin/env python
"""Colab'a yuklenecek dosyalari tek klasorde toplar.

NEDEN VAR

Dosyalar bir kez elle toplanmisti. Sonra _scripts/retrieval_eval.py guncellendi
ama toplama klasorundeki kopya eski halinde kaldi. Colab o eski surumu calistirdi
ve sonuc gecerli gorundu: rakamlar makuldu, sadece sorgu isleme hic devreye
girmemisti. Olcum sistemlerinde en sinsi hata tipi bu - yanlis sonuc degil,
DOGRU ama BASKA bir konfigurasyona ait sonuc.

Bu script kopyalamayi tek komuta indiriyor. Her Colab kosusundan ONCE calistir.

Calistirma:
    _env/parse/Scripts/python.exe _scripts/colab_paketle.py
"""
import os, shutil, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEDEF = os.path.join(ROOT, "1")

DOSYALAR = [
    "_scripts/retrieval_eval.py",
    "_scripts/pipeline.py",
    "_scripts/qdrant_index.py",
    "_scripts/embed_chunks.py",
    "_scripts/query_processing.py",
    "_scripts/chunk.py",
    "_scripts/plog.py",
    "_work/chunks/chunks.json",
    "_scripts/answer_eval.py",
    "_work/eval/golden_queries.json",
    "_work/eval/negative_queries.json",
    "_scripts/negatif_taze.py",
    "_scripts/llm_bakeoff.py",
    # Level 4 atif onarimi olcumu kayitli cevaplar uzerinde kosuyor.
    "_logs/level3_yeniden.json",
    "_work/eval/negative_queries_v2.json",
    # arsiv_sozluk.json bilerek yok: pipeline yoksa chunks.json'dan uretiyor.
    "_work/embeddings/BAAI_bge-m3.npy",
    "_work/embeddings/BAAI_bge-m3.meta.json",
]


def main():
    os.makedirs(HEDEF, exist_ok=True)
    eksik = []
    for gorece in DOSYALAR:
        kaynak = os.path.join(ROOT, gorece)
        if not os.path.exists(kaynak):
            eksik.append(gorece)
            continue
        shutil.copy2(kaynak, os.path.join(HEDEF, os.path.basename(kaynak)))
        st = os.stat(kaynak)
        print(f"  {os.path.basename(kaynak):24s} {st.st_size:>10,d} B  "
              f"{time.strftime('%Y-%m-%d %H:%M', time.localtime(st.st_mtime))}")

    if eksik:
        print("\nEKSIK:", ", ".join(eksik))
        sys.exit(1)

    # Colab'daki 4. hucre bu bayragi ariyor; burada da bakiyoruz ki hata
    # Colab'a kadar tasinmasin.
    kaynak = open(os.path.join(HEDEF, "retrieval_eval.py"), encoding="utf-8").read()
    print(f"\n{len(DOSYALAR)} dosya -> {HEDEF}")
    print("--qp destegi:", "var" if "--qp" in kaynak else "YOK (kopyalama bozuk)")


if __name__ == "__main__":
    main()
