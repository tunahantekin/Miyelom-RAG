#!/usr/bin/env python
"""Level 2 - Golden Retrieval Test.

Level 1 (chunk_validation.py) "belgeyi bozduk mu" sorusunu cevapliyor.
Bu script farkli bir soruyu cevapliyor: "chunk'lar dogru bilgiyi getiriyor mu".
Ikisi bagimsiz - belgeyi hic bozmadan ise yaramaz chunk uretmek mumkun.

TASARIM

- Hedef, chunk_id ile DEGIL belge + bolum ile tanimlanir. chunk_id her yeniden
  uretimde degisiyor; bolum referansi chunking stratejisinden bagimsiz kaliyor.
  Boylece ayni soru kumesi farkli stratejileri (800 vs 400 token, context satiri
  var/yok) karsilastirabilir.
- Sorular chunk'lara BAKILARAK yazilmamali. Yazilirsa test kendini dogrular.
  Kaynak klinik olmali: kilavuz karar noktalari, KUB doz bolumleri, SUT kosullari.
- Baseline arama BM25 (leksik). Gomme modeli sonra eklenecek; BM25 hem bagimlilik
  gerektirmiyor hem de gomme kazanci varsa onu olcebilecegimiz taban cizgisi.

Olcut:
  recall@k  dogru bolum ilk k sonucta var mi (klinik karar destegi icin kritik
            olan bu: dogru chunk listeye hic girmiyorsa LLM'in kurtarma sansi yok)
  MRR       dogru bolumun sirasi

Calistirma:
    python _scripts/retrieval_eval.py
    python _scripts/retrieval_eval.py --k 10 --detay
"""
import argparse, json, math, os, re, sys, time, unicodedata
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))

CHUNKS = os.path.join(ROOT, "_work", "chunks", "chunks.json")
SORULAR = os.path.join(ROOT, "_work", "eval", "golden_queries.json")
RAPOR = os.path.join(ROOT, "_logs", "retrieval_eval.json")

K1, K2 = 5, 10

RERANK_MODEL = "BAAI/bge-reranker-v2-m3"
HAVUZ = 50                 # reranker'a giren aday sayisi


def sadelestir(s):
    s = s.replace("İ", "i").replace("I", "ı").lower().replace("ı", "i")
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


def kelimele(s):
    return re.findall(r"[a-z0-9]+", sadelestir(s))


class BM25:
    """Kucuk, bagimliliksiz BM25. 15 bin chunk icin fazlasiyla yeterli."""

    def __init__(self, belgeler, k1=1.5, b=0.75):
        self.k1, self.b = k1, b
        self.belgeler = [Counter(d) for d in belgeler]
        self.uzunluk = [sum(d.values()) for d in self.belgeler]
        self.ort = sum(self.uzunluk) / max(1, len(self.uzunluk))
        df = Counter()
        for d in self.belgeler:
            df.update(d.keys())
        n = len(self.belgeler)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}
        self.gecen = defaultdict(list)
        for i, d in enumerate(self.belgeler):
            for t in d:
                self.gecen[t].append(i)

    def ara(self, sorgu, k=10):
        puan = defaultdict(float)
        for t in sorgu:
            if t not in self.idf:
                continue
            idf = self.idf[t]
            for i in self.gecen[t]:
                f = self.belgeler[i][t]
                pay = f * (self.k1 + 1)
                payda = f + self.k1 * (1 - self.b + self.b * self.uzunluk[i] / self.ort)
                puan[i] += idf * pay / payda
        return sorted(puan.items(), key=lambda x: -x[1])[:k]


def hedef_uyar(meta, hedef):
    """Bir chunk beklenen hedefe uyuyor mu?

    belge: document_name icinde gecmesi yeterli (dosya adlari uzun ve degisken).
    bolum: section_number birebir ya da onek (4.2 hedefi 4.2.1'i de tutar).
    """
    if hedef.get("belge") and sadelestir(hedef["belge"]) not in sadelestir(
            str(meta.get("document_name"))):
        return False
    b = hedef.get("bolum")
    if b:
        s = str(meta.get("section_number") or "")
        if not (s == b or s.startswith(b + ".") or sadelestir(b) == sadelestir(s)):
            return False
    return True


def chunk_uyar(c, hedef):
    """Getirilen chunk hedefi karsiliyor mu? Metadata VEYA icerik uzerinden.

    Yalnizca metadata'ya bakmak testi haksiz kiliyordu: ayni NCCN kilavuzu
    arsivde uc surumde var (elle hazirlanmis dosya, parse edilmis PDF, dergi
    makalesi) ve dogru bilgiyi yanlis surumden getirmek "kacirdi" sayiliyordu.
    Ayni sekilde tek bir markanin KUB'unu hedef yazmak, ayni etken maddenin
    baska markasini getirmeyi hata gosteriyordu.

    Bu yuzden hedefte 'icerik' verilebiliyor: listedeki TUM desenler chunk
    metninde geciyorsa chunk dogru sayilir - "bilgi geldi mi" sorusunun cevabi.
    """
    kimlik = hedef.get("belge") or hedef.get("bolum")
    if hedef.get("icerik"):
        if not all(re.search(d, c["content"], re.I) for d in hedef["icerik"]):
            return False
        # Ayni hedefte hem belge hem icerik varsa IKISI de saglanmali. Once
        # icerik eslesmesi tek basina yeterli sayiliyordu; o zaman "SUT'ta
        # lenalidomid kosulu" sorusu, arsivde lenalidomid gecen 4.336 chunk'in
        # herhangi birini dogru kabul ediyordu. Bir hedefte belge YAZMAK
        # daraltmak demektir, genisletmek degil.
        return hedef_uyar(c["metadata"], hedef) if kimlik else True
    if kimlik:
        return hedef_uyar(c["metadata"], hedef)
    return False


def rrf(siralar_listesi, k=60):
    """Reciprocal Rank Fusion.

    BM25 puani ile kosinus benzerligi farkli olceklerde; dogrudan toplamak icin
    normalize etmek gerekir ve normalizasyon sorgudan sorguya kayar. RRF yalnizca
    SIRAYA bakar, bu yuzden olcek sorunu yasamaz.
    """
    puan = defaultdict(float)
    for siralar in siralar_listesi:
        for sira, idx in enumerate(siralar, start=1):
            puan[idx] += 1.0 / (k + sira)
    return sorted(puan.items(), key=lambda x: -x[1])


class Reranker:
    """Cross-encoder yeniden siralayici.

    Bi-encoder (BGE-M3) sorgu ile chunk'i AYRI AYRI vektore ceviriyor; ikisi
    birbirini hic gormuyor. Cross-encoder ciftin ikisini de ayni girdide
    okuyor, bu yuzden "bu metin bu sorunun cevabini iceriyor mu" sorusuna
    daha isabetli cevap veriyor. Bedeli: her aday icin ayri model cagrisi,
    yani tum arsive uygulanamaz. Bu yuzden once hibrit ile HAVUZ kadar aday
    toplanip yalnizca onlar yeniden siralaniyor.
    """

    def __init__(self, ad=RERANK_MODEL):
        os.environ.setdefault("HF_HOME", "D:/hf_cache")
        from sentence_transformers import CrossEncoder
        t0 = time.time()
        self.m = CrossEncoder(ad, max_length=512,
                              cache_folder=os.environ["HF_HOME"])
        print(f"reranker yuklendi ({ad}) {time.time()-t0:.0f}sn", flush=True)

    def sirala(self, soru, adaylar, metinler, k):
        ciftler = [(soru, metinler[i]) for i in adaylar]
        puan = self.m.predict(ciftler, batch_size=16, show_progress_bar=False)
        sirali = sorted(zip(adaylar, puan), key=lambda x: -x[1])
        return [i for i, _ in sirali[:k]]


def dense_yukle(model_ad):
    """(vektorler, chunks.json indeksleri, meta) - yoksa (None, None, None)."""
    import numpy as np
    ad = model_ad.replace("/", "_")
    for son in (".altkume", ""):
        p = os.path.join(ROOT, "_work", "embeddings", ad + son + ".npy")
        m = p[:-4] + ".meta.json"
        if os.path.exists(p) and os.path.exists(m):
            meta = json.load(open(m, encoding="utf-8"))
            return np.load(p), meta.get("altkume_idx"), meta
    return None, None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=K2)
    ap.add_argument("--detay", action="store_true")
    ap.add_argument("--mod", default="bm25",
                    choices=["bm25", "dense", "hibrit", "rerank", "gpusuz",
                             "hepsi"],
                    help="gpusuz: reranker haric uc mod (yerel makinede kosar)")
    ap.add_argument("--model", default="BAAI/bge-m3")
    ap.add_argument("--rerank-model", default=RERANK_MODEL)
    ap.add_argument("--havuz", type=int, default=HAVUZ)
    ap.add_argument("--depo", default="numpy", choices=["numpy", "qdrant"],
                    help="dense arama nerede kossun")
    ap.add_argument("--sorular", default=SORULAR,
                    help="alternatif golden query dosyasi")
    ap.add_argument("--qp", action="store_true",
                    help="sorgu isleme: varlik tespiti + BM25 genisletme + "
                         "ilac uyumuna gore yeniden siralama")
    a = ap.parse_args()

    chunks = json.load(open(CHUNKS, encoding="utf-8"))
    sorular = json.load(open(a.sorular, encoding="utf-8"))

    modlar = {"hepsi":  ["bm25", "dense", "hibrit", "rerank"],
              "gpusuz": ["bm25", "dense", "hibrit"]}.get(a.mod, [a.mod])
    vek, altkume, meta = (None, None, None)
    if set(modlar) & {"dense", "hibrit", "rerank"}:
        vek, altkume, meta = dense_yukle(a.model)
        if vek is None:
            print(f"gomme bulunamadi ({a.model}) - once embed_chunks.py calistir")
            return

    # Alt kume varsa TUM modlar ayni kume uzerinde olculur; yoksa karsilastirma
    # adil olmaz (BM25 tum arsivde, dense 1200 chunk'ta aranmis olur).
    if altkume:
        chunks = [chunks[i] for i in altkume]
        print(f"alt kume modu: {len(chunks)} chunk uzerinde olculuyor "
              f"(tam arsiv degil - celdirici az oldugu icin skorlar iyimser)")

    # Her sorunun hedefi bu kumede GERCEKTEN var mi? Yoksa test bozuktur ve
    # dusuk skor retriever'in degil soru kumesinin sorunudur.
    cozulmeyen = []
    for s in sorular:
        s["_aday"] = sum(1 for c in chunks
                         if any(chunk_uyar(c, h) for h in s["hedef"]))
        if s["_aday"] == 0:
            cozulmeyen.append(s["id"])

    dizin = BM25([kelimele(c["content"] + " " +
                           str(c["metadata"].get("section_title") or "") + " " +
                           str(c["metadata"].get("document_name") or ""))
                  for c in chunks])

    sorgu_vek = None
    if vek is not None:
        os.environ.setdefault("HF_HOME", "D:/hf_cache")
        from sentence_transformers import SentenceTransformer
        import numpy as np
        m = SentenceTransformer(a.model, cache_folder=os.environ["HF_HOME"])
        m.max_seq_length = 512
        sorgu_vek = m.encode([s["soru"] for s in sorular],
                             normalize_embeddings=True, convert_to_numpy=True)

    # Sorgu isleme bir kez yapilir, tum modlar ayni analizi paylasir. Boylece
    # modlar arasindaki fark yine retriever'dan gelir, analiz farkindan degil.
    qp = None
    if a.qp:
        import query_processing as QP
        qp = [QP.analiz(s["soru"]) for s in sorular]
        bulan = sum(1 for r in qp if r["ilac"])
        print(f"sorgu isleme acik: {bulan}/{len(sorular)} soruda ilac tespit edildi")

    qc = QI = None
    if a.depo == "qdrant":
        if altkume:
            print("qdrant deposu tam arsivi tutuyor; alt kume ile birlestirilemez")
            return
        import qdrant_index as QI
        qc = QI.ac()
        print(f"qdrant: {qc.count(QI.KOLEKSIYON).count} nokta")

    rr, rr_metin = None, None
    if "rerank" in modlar:
        from embed_chunks import gomulecek_metin
        rr_metin = [gomulecek_metin(c) for c in chunks]
        rr = Reranker(a.rerank_model)

    ozet, tum = {}, {}
    for mod in modlar:
        sonuc, r1, r2, mrr = [], 0, 0, 0.0
        t_mod = time.time()
        for qi, s in enumerate(sorular):
            if s["_aday"] == 0:
                continue
            derin = max(a.k, a.havuz)
            # BM25 genisletilmis sorguyla calisir (Turkce soru + Ingilizce INN +
            # ATC + kisaltma acilimi); dense ham soruyla calisir, cunku gomme
            # modeli dogal cumleyle egitildi.
            bm_soru = QP.genislet(s["soru"], qp[qi]) if qp else s["soru"]
            bm = [i for i, _ in dizin.ara(kelimele(bm_soru), derin)]

            # Yeniden siralama her kesme adimindan ONCE uygulaniyor: dogru
            # ilacin chunk'i k'nin ya da havuzun altinda kalirsa reranker onu
            # zaten kurtaramaz.
            def bst(liste):
                return (QP.boost_uygula(liste, chunks, qp[qi]["ilac"])
                        if qp else liste)

            bm = bst(bm)
            if mod == "bm25":
                bulunan = bm[:a.k]
            else:
                if qc is not None:
                    # Qdrant nokta id'si chunks.json satir indeksi ile ayni,
                    # bu yuzden sonuc dogrudan kullanilabiliyor. Boost burada
                    # da arama SONRASI uygulaniyor - numpy yoluyla birebir ayni
                    # kalsin diye. Filtreyi sorgunun icine tasimak mumkun ama
                    # o zaman iki yol karsilastirilamaz hale gelirdi.
                    ds = bst([p.id for p in QI.ara(qc, sorgu_vek[qi], derin)])
                else:
                    import numpy as np
                    skor = vek @ sorgu_vek[qi]
                    ds = bst([int(x) for x in np.argsort(-skor)[:derin]])
                if mod == "dense":
                    bulunan = ds[:a.k]
                else:
                    havuz = bst([i for i, _ in rrf([bm, ds])])
                    # rerank: hibrit havuzunu cross-encoder ile yeniden sirala.
                    # Hibrit recall@10'da 0.90'a ulasmisti ama MRR dusuktu -
                    # yani dogru chunk listeye giriyor, ust siraya cikmiyordu.
                    # Reranker'in duzeltmesi beklenen yer tam burasi.
                    bulunan = (bst(rr.sirala(s["soru"], havuz[:a.havuz],
                                             rr_metin, a.k))
                               if mod == "rerank" else havuz[:a.k])

            siralar = [i + 1 for i, idx in enumerate(bulunan)
                       if any(chunk_uyar(chunks[idx], h) for h in s["hedef"])]
            ilk = siralar[0] if siralar else None
            r1 += 1 if ilk and ilk <= K1 else 0
            r2 += 1 if ilk and ilk <= K2 else 0
            mrr += 1 / ilk if ilk else 0
            sonuc.append(dict(id=s["id"], soru=s["soru"], ilk_dogru_sira=ilk,
                              aday=s["_aday"],
                              getirilen=[chunks[i]["metadata"]["document_label"] +
                                         " / " + str(chunks[i]["metadata"]
                                                     ["section_number"])
                                         for i in bulunan[:3]]))
        n = max(1, len(sonuc))
        ozet[mod] = dict(recall_5=r1 / n, recall_10=r2 / n, mrr=mrr / n,
                         kacan=sum(1 for x in sonuc if not x["ilk_dogru_sira"]),
                         saniye=round(time.time() - t_mod, 1))
        tum[mod] = sonuc

    print(f"{len(tum[modlar[0]])} soru degerlendirildi "
          f"({len(cozulmeyen)} soru hedefi kumede yok)")
    if cozulmeyen:
        print("  hedefi bulunamayan:", ", ".join(cozulmeyen))
    print(f"  {'mod':8s} {'recall@5':>9s} {'recall@10':>10s} {'MRR':>7s} "
          f"{'kacan':>6s} {'sn':>7s}")
    for mod in modlar:
        o = ozet[mod]
        print(f"  {mod:8s} {o['recall_5']:9.2f} {o['recall_10']:10.2f} "
              f"{o['mrr']:7.3f} {o['kacan']:6d} {o['saniye']:7.1f}")

    if a.detay:
        for mod in modlar:
            print(f"\n  --- {mod} kacanlar")
            for x in tum[mod]:
                if not x["ilk_dogru_sira"]:
                    print(f"    {x['id']}: {x['soru'][:60]}")
                    print(f"       geldi: {x['getirilen']}")

    json.dump(dict(ozet=ozet, altkume=bool(altkume), kume_boyut=len(chunks),
                   model=a.model, havuz=a.havuz, qp=a.qp, depo=a.depo,
                   cozulmeyen=cozulmeyen, sonuc=tum),
              open(RAPOR, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"  -> {RAPOR}")


if __name__ == "__main__":
    main()
