#!/usr/bin/env python
"""Chunk'lari gomer (dense vektor uretir).

Model: BAAI/bge-m3. Cok dilli olmasi bu arsiv icin zorunlu - sorular Turkce,
NCCN kilavuzu Ingilizce. BM25 taban cizgisi tam bu yuzden 20 soruda
recall@5=0.20'de kaldi: leksik eslesme Turkce sorguyla Ingilizce basligi
birlestiremiyor.

Model onbellegi D: surucusunde (HF_HOME); C: dar.

Cikti: _work/embeddings/<model>.npy (float32, satir sirasi chunks.json ile ayni)
       + <model>.meta.json (model adi, boyut, chunk sayisi, tarih)

Calistirma:
    _env/parse/Scripts/python.exe _scripts/embed_chunks.py
    ... --limit 200 --batch 8        (once kucuk parti dene)
"""
import argparse, json, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))

os.environ.setdefault("HF_HOME", "D:/hf_cache")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

from plog import log

CHUNKS = os.path.join(ROOT, "_work", "chunks", "chunks.json")
CIKTI_DIZIN = os.path.join(ROOT, "_work", "embeddings")

MODEL = "BAAI/bge-m3"
AZAMI_UZUNLUK = 1024      # chunk'larin %90'i 787 token; 8192 gereksiz ve cok yavas


def gomulecek_metin(c):
    """Gomme girdisi = baslik baglami + icerik.

    Ciplak icerik yetmiyor: bir dozaj tablosu chunk'inin kendi metninde hangi
    ilaca ait oldugu yazmayabiliyor. Belge etiketi ve bolum basligi eklenince
    chunk kendi basina anlamli hale geliyor.
    """
    m = c["metadata"]
    bas = " / ".join(str(x) for x in
                     [m.get("document_label"), m.get("section_number"),
                      m.get("section_title")] if x)
    return (bas + "\n" + c["content"]).strip()


HEDEF_TAVAN = 40           # tek bir sorunun hedefi tum kumeyi doldurmasin


def altkume_sec(chunks, boyut, tohum=17):
    """Golden query hedeflerini kapsayan + celdirici iceren orneklem.

    Neden: tum arsivi gommeden once "BGE-M3 bu arsivde ise yariyor mu" sorusunu
    ucuza cevaplamak icin. Kucuk kumede celdirici az oldugundan recall dogal
    olarak yuksek cikar - rakam tam arsivin rakami DEGILDIR. Karsilastirma
    adil kalsin diye BM25 de ayni kume uzerinde olculur.
    """
    import random
    from retrieval_eval import hedef_uyar
    sorular = json.load(open(os.path.join(ROOT, "_work", "eval",
                                          "golden_queries.json"), encoding="utf-8"))
    rnd = random.Random(tohum)
    secili = set()
    for s in sorular:
        uyan = [i for i, c in enumerate(chunks)
                if any(hedef_uyar(c["metadata"], h) for h in s["hedef"])]
        # Cok genis hedefler (ornegin bolum belirtmeyen SUT sorusu) binlerce
        # chunk tutuyor; ornekleme yapilmazsa kume tek soruyla doluyor.
        secili.update(uyan if len(uyan) <= HEDEF_TAVAN
                      else rnd.sample(uyan, HEDEF_TAVAN))
    kalan = [i for i in range(len(chunks)) if i not in secili]
    celdirici = rnd.sample(kalan, min(max(0, boyut - len(secili)), len(kalan)))
    return sorted(secili | set(celdirici)), len(secili)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--altkume", type=int, default=0,
                    help="tum arsiv yerine bu boyutta orneklem gom")
    a = ap.parse_args()

    import numpy as np
    from sentence_transformers import SentenceTransformer

    chunks = json.load(open(CHUNKS, encoding="utf-8"))
    idx = None
    if a.altkume:
        idx, hedef_say = altkume_sec(chunks, a.altkume)
        chunks = [chunks[i] for i in idx]
        print(f"alt kume: {len(idx)} chunk ({hedef_say} hedef + "
              f"{len(idx)-hedef_say} celdirici)", flush=True)
    elif a.limit:
        chunks = chunks[:a.limit]
    metinler = [gomulecek_metin(c) for c in chunks]

    t0 = time.time()
    print(f"model yukleniyor: {a.model}  (onbellek {os.environ['HF_HOME']})",
          flush=True)
    model = SentenceTransformer(a.model, cache_folder=os.environ["HF_HOME"])
    model.max_seq_length = AZAMI_UZUNLUK
    print(f"  yuklendi {time.time()-t0:.0f}sn, "
          f"boyut {model.get_sentence_embedding_dimension()}", flush=True)

    t1 = time.time()
    vek = model.encode(metinler, batch_size=a.batch, show_progress_bar=True,
                       normalize_embeddings=True, convert_to_numpy=True)
    sure = time.time() - t1

    os.makedirs(CIKTI_DIZIN, exist_ok=True)
    ad = a.model.replace("/", "_") + (".altkume" if a.altkume else "")
    np.save(os.path.join(CIKTI_DIZIN, ad + ".npy"), vek.astype("float32"))
    # altkume_idx: vektor satiri -> chunks.json'daki sira. Kaydedilmezse
    # vektorlerin hangi chunk'a ait oldugu geri kurtarilamaz.
    json.dump(dict(model=a.model, boyut=int(vek.shape[1]), chunk=int(vek.shape[0]),
                   azami_uzunluk=AZAMI_UZUNLUK, saniye=round(sure, 1),
                   altkume_idx=idx,
                   tarih=time.strftime("%Y-%m-%d %H:%M:%S")),
              open(os.path.join(CIKTI_DIZIN, ad + ".meta.json"), "w",
                   encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{vek.shape[0]} vektor x {vek.shape[1]} boyut, {sure:.0f}sn "
          f"({vek.shape[0]/max(1,sure):.1f} chunk/sn)")
    log("gomme", "embed", f"{a.model}: {vek.shape[0]} chunk, {sure:.0f}sn")


if __name__ == "__main__":
    main()
