#!/usr/bin/env python
"""Qdrant vektor deposu - boru hattinin 6. adimi.

NEDEN GOMULU KIP

Qdrant genelde Docker konteyneri olarak calisiyor. Burada qdrant-client'in
gomulu (local) kipini kullaniyoruz: sunucu yok, veri _work/qdrant altinda bir
klasor. Sebebi tek bir kodun hem bu makinede hem Colab'da degismeden kosmasi.
Docker'a baglansaydik Colab tarafinda ayri bir kurgu gerekirdi ve ayni sistemin
iki farkli yolu olurdu - hangisini olctugumuz belirsizlesirdi.

API ayni; sunucuya gecmek gerekirse tek satir degisiyor (path yerine url).

NEDEN NUMPY YETMIYORDU

Hiz degil. 14.532 vektorde numpy carpimi zaten milisaniye suruyor. Uc sey icin:
  - Metadata filtresi aramanin ICINDE calisiyor. Simdiye kadar ilac uyumuna
    gore yeniden siralamayi arama bittikten SONRA Python'da yapiyorduk.
  - Kalicilik. .npy dosyasi surecin bellegine yukleniyordu; belge eklendiginde
    tamami yeniden uretiliyordu.
  - Payload ile vektor ayni yerde duruyor, ikisini elle hizali tutmak gerekmiyor.

Calistirma:
    _env/parse/Scripts/python.exe _scripts/qdrant_index.py           (kurar)
    _env/parse/Scripts/python.exe _scripts/qdrant_index.py --dogrula
"""
import argparse, json, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))

CHUNKS = os.path.join(ROOT, "_work", "chunks", "chunks.json")
VEKTOR = os.path.join(ROOT, "_work", "embeddings", "BAAI_bge-m3.npy")
DEPO = os.path.join(ROOT, "_work", "qdrant")
KOLEKSIYON = "myeloma"

# Payload'a tasinacak metadata alanlari. Hepsini tasimiyoruz: parsing_flags gibi
# alanlar aramada islevsiz, depoyu buyutmekten baska ise yaramaz.
ALANLAR = ["document_name", "document_label", "section_number", "section_title",
           "page_number", "source_type", "drug_names", "atc_codes", "disease",
           "version"]


def ac(yol=DEPO):
    from qdrant_client import QdrantClient
    return QdrantClient(path=yol)


def kur(yenile=False):
    import numpy as np
    from qdrant_client import models

    chunks = json.load(open(CHUNKS, encoding="utf-8"))
    vek = np.load(VEKTOR)
    # Satir sirasi bozulursa vektorler baska chunk'lara baglanir ve sistem hata
    # vermeden yanlis cevap uretir. Bu yuzden burada duruyoruz.
    assert vek.shape[0] == len(chunks), \
        f"vektor {vek.shape[0]} != chunk {len(chunks)}"

    c = ac()
    varsa = c.collection_exists(KOLEKSIYON)
    if varsa and not yenile:
        print(f"koleksiyon zaten var ({c.count(KOLEKSIYON).count} nokta). "
              f"yeniden kurmak icin --yenile")
        c.close()
        return
    if varsa:
        c.delete_collection(KOLEKSIYON)

    c.create_collection(
        KOLEKSIYON,
        vectors_config=models.VectorParams(size=int(vek.shape[1]),
                                           distance=models.Distance.COSINE))

    t0 = time.time()
    PARTI = 512
    for bas in range(0, len(chunks), PARTI):
        son = min(bas + PARTI, len(chunks))
        noktalar = []
        for i in range(bas, son):
            m = chunks[i]["metadata"]
            yuk = {a: m.get(a) for a in ALANLAR}
            yuk["chunk_id"] = chunks[i]["chunk_id"]
            yuk["content"] = chunks[i]["content"]
            noktalar.append(models.PointStruct(id=i, vector=vek[i].tolist(),
                                               payload=yuk))
        c.upsert(KOLEKSIYON, noktalar)
        print(f"  {son}/{len(chunks)}", end="\r", flush=True)

    n = c.count(KOLEKSIYON).count
    print(f"\n{n} nokta yuklendi, {time.time()-t0:.0f}sn -> {DEPO}")
    c.close()


def ara(c, vektor, k=10, ilac=None, katman=None, zorunlu_ilac=None):
    """Filtreli arama.

    ilac verilirse SERT filtre uygulanmiyor - o chunk'lar oncelikli getiriliyor
    ama etiketsizler de listede kaliyor. Sebebi query_processing.py'de
    anlatildi: chunk'larin %39'unda ilac etiketi yok ve sert filtre onlari
    toptan eler, bos liste dondurup "bilgi yok" izlenimi verir.
    """
    from qdrant_client import models
    kosul = []
    if zorunlu_ilac:
        # Sert filtre - yalnizca bu etken maddeye ait chunk'lar. Genel aramanin
        # yerine gecmiyor, YANINDA kullaniliyor: Turkce soru ile Ingilizce urun
        # bilgisi arasindaki mesafe yuzunden dogru belge ilk 30'a hic
        # giremeyebiliyor. Filtreli ikinci arama o belgeyi garantiliyor.
        kosul.append(models.FieldCondition(
            key="drug_names", match=models.MatchAny(any=list(zorunlu_ilac))))
    if katman:
        kosul.append(models.FieldCondition(key="source_type",
                                           match=models.MatchAny(any=katman)))
    filtre = models.Filter(must=kosul) if kosul else None

    sonuc = c.query_points(KOLEKSIYON, query=vektor.tolist(), limit=k,
                           query_filter=filtre, with_payload=True).points
    if not ilac:
        return sonuc
    hedef = set(ilac)
    a, b, d = [], [], []
    for p in sonuc:
        etiket = set(p.payload.get("drug_names") or [])
        (a if etiket & hedef else b if not etiket else d).append(p)
    return a + b + d


def dogrula():
    """Qdrant sonuclari numpy ile ayni mi?

    Tasima sirasinda satir sirasi kaymasi ya da normalize farki sessizce
    yanlis sonuc uretir. Ayni sorgu vektoruyle iki tarafi karsilastiriyoruz.
    """
    import numpy as np
    vek = np.load(VEKTOR)
    rnd = np.random.default_rng(17)
    c = ac()
    ayni, DENEME = 0, 20
    for _ in range(DENEME):
        q = vek[rnd.integers(0, len(vek))]
        np_ilk = [int(x) for x in np.argsort(-(vek @ q))[:10]]
        qd_ilk = [p.id for p in c.query_points(KOLEKSIYON, query=q.tolist(),
                                               limit=10).points]
        ayni += 1 if np_ilk == qd_ilk else 0
        if np_ilk != qd_ilk:
            print("  fark:", np_ilk[:5], "vs", qd_ilk[:5])
    print(f"{ayni}/{DENEME} sorguda ilk 10 birebir ayni")
    c.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--yenile", action="store_true")
    ap.add_argument("--dogrula", action="store_true")
    a = ap.parse_args()
    if a.dogrula:
        dogrula()
    else:
        kur(a.yenile)
