#!/usr/bin/env python
"""Level 3 / Level 4 - cevap ve atif degerlendirmesi.

NE OLCUYOR

Level 1 "belgeyi bozduk mu", Level 2 "dogru parca geliyor mu" diye soruyordu.
Bu script uctaki soruyu soruyor: uretilen cevap kaynaga dayaniyor mu, ve
arsivde olmayan bir sey soruldugunda sistem duruyor mu.

Klinik DOGRULUK olculmuyor - onun icin hematolog gerekir ve yok. Olculen sey
dayanaklilik ve atif isabeti; ikisi de uzman gerektirmeden olculebilir ve
klinik bir sistemde belki daha kritik. Yanlis cevap tartisilir; kaynagi
uydurulmus yanlis cevap tehlikelidir.

ASIRI UYUM ONLEMI

Dayanaklilik esigi (0,40) ilk dort demo cevabina bakilarak secilmisti. Dort
noktadan turetilen bir esigin genelde dogru yerde durdugu iddia edilemez -
sinavi gordukten sonra gecme notu belirlemek gibi. Bu yuzden:

    78 pozitif soru -> A (esik secimi) ve B (olcum), donusumlu bolunuyor
    15 negatif soru -> NA (esik secimi) ve NB (olcum)

Esik YALNIZCA A ve NA'ya bakilarak seciliyor. Raporlanan rakam B ve NB'den
geliyor, yani esigin hic gormedigi sorulardan. Rapor ikisini ayri yaziyor.

TEK KOSU, COK ESIK

Dil modeli bir kez kosuyor; kapilar kapali (esikler 0). Esikler sonradan ham
kayitlara uygulaniyor. Aksi halde her esik denemesi butun kumeyi yeniden
urettirirdi - T4'te ~40 dakika.

Calistirma:
    python _scripts/answer_eval.py --llm sahte            (borulari test eder)
    python _scripts/answer_eval.py --llm transformers     (Colab, GPU)
"""
import argparse, json, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))

import pipeline as P
import qdrant_index as QI
from retrieval_eval import chunk_uyar

POZITIF = os.path.join(ROOT, "_work", "eval", "golden_queries.json")
NEGATIF = os.path.join(ROOT, "_work", "eval", "negative_queries.json")
CHUNKS = os.path.join(ROOT, "_work", "chunks", "chunks.json")
RAPOR = os.path.join(ROOT, "_logs", "level3_eval.json")

# Esik taramasi. Arama esigi dar tutuldu: gecerli sorular 0,63'e kadar
# inebiliyor, yani 0,60'in uzerine cikmak dogru sorulari elemeye baslar.
ARAMA_ADAY = [0.50, 0.55, 0.60]
DAYANAK_ADAY = [round(0.20 + 0.05 * i, 2) for i in range(13)]   # 0,20 - 0,80


def bol(liste):
    """Donusumlu bolme: A = cift indeks, B = tek indeks.

    Rastgele bolmuyoruz. Sorular katmana gore sirali (klinik, duzenleyici,
    geri odeme) ve rastgele bolme bir katmani tek tarafa yigabilir. Donusumlu
    bolme her katmani iki tarafa da esit dagitiyor, ustelik tekrarlanabilir.
    """
    return liste[0::2], liste[1::2]


def ham_kos(llm, sorular, istemci, chunk_haritasi, k, pozitif=True):
    """Kapilar KAPALI tek kosu. Her soru icin ham olcumler kaydediliyor."""
    kayit = []
    for i, s in enumerate(sorular, start=1):
        t0 = time.time()
        # Alan kapisi da kapatiliyor: bu kosunun amaci HAM olcum toplamak,
        # esikler sonradan kayitlara uygulaniyor. Kapi acik kosarsa esik
        # taramasi kendi sectigi kuralin sonucunu olcmus olurdu.
        # atif_onarim=False: HAM model ciktisi saklanmali. Onarim cevapla()
        # icine baglandiktan sonra ilk bakeoff kosusunda "onarim oncesi ->
        # sonrasi" sutunu her modelde ayni cikti (27->27), cunku kaydedilen
        # cevap zaten onarilmisti ve ikinci gecis idempotent. Onarimin katkisi
        # ancak ham cikti saklanirsa olculebilir.
        r = P.cevapla(s["soru"], llm=llm, istemci=istemci, k=k,
                      reddet_esigi=0.0, dayanak_esigi=0.0, alan_kural="kapali",
                      atif_onarim=False)
        g = r["guven"]

        # Atif isabeti: modelin ATIF VERDIGI parcalar golden hedefi tutuyor mu?
        # Getirilen parcaya degil, atif verilene bakiyoruz - cevabin dayandigi
        # yer orasi. Getirilene bakmak Level 2'yi tekrar olcmek olurdu.
        tuttu = False
        if pozitif:
            atifli = [x for x in (g.get("tum_kaynaklar") or [])
                      if x["no"] in r["kullanilan"]]
            for x in atifli:
                c = chunk_haritasi.get(x["chunk_id"])
                if c and any(chunk_uyar(c, h) for h in s["hedef"]):
                    tuttu = True
                    break

        kayit.append({
            "id": s["id"], "soru": s["soru"],
            "arama_skoru": g["arama_skoru"], "dayanaklilik": g["dayanaklilik"],
            "atif_sayisi": len(r["kullanilan"]),
            "hedef_tuttu": tuttu, "cevap": r["cevap"],
            "saniye": round(time.time() - t0, 1),
        })
        print(f"  {i}/{len(sorular)} {s['id']} "
              f"skor {g['arama_skoru']:.2f} dayanak {g['dayanaklilik']:.2f}"
              f"{' HEDEF' if tuttu else ''}", flush=True)
    return kayit


def yeniden_puanla(kayit_yolu, k=4, cikti=None, istemci=None):
    """Kaydedilmis cevaplari YENIDEN puanlar - dil modeli kosmadan.

    NEDEN GEREKTI

    Ilk olcumde dayanakliligin medyani hem pozitiflerde hem negatiflerde tam
    olarak 0,0 cikti. Buna karsilik atif veren cevap 73/78 ve atif verilen
    parca golden hedefi 49/78 tutuyordu. Yani dogru kaynagi gosteren
    cevaplarin ucte ikisi "dayanaksiz" sayiliyordu. Boyle bir dagilim sistemin
    degil olcutun imzasidir.

    Sebep: dayanaklilik SOZCUK ORTUSMESIYLE olculuyordu. Cevap Turkce, kaynak
    NCCN ise Ingilizce. Turkce bir cumlenin Ingilizce paragrafla sozcuk
    ortusmesi, cumle o paragraftan alinmis olsa bile sifira yakin. BM25'in
    basina gelenin aynisi: leksik yontem iki dilli arsivde calisamaz.

    UC DUZELTME

    1. Anlamsal karsilastirma: cumle ve parca BGE-M3 ile gomulup kosinus
       benzerligine bakiliyor. Model cok dilli, Turkce cumleyle Ingilizce
       paragrafi ayni uzayda bulusturuyor. Leksik kontrol hizli yol olarak
       kaliyor; tutmazsa anlamsal kontrole dusuluyor.
    2. Toplu atif bicimi ([K1, K2, K3]) artik taniniyor.
    3. Olcut ikiye ayriliyor:
         kanit_orani - cumle VERILEN kaynaklarin herhangi birinde var mi?
                       Guvenlik sorusu bu: uydurma var mi yok mu.
         atif_orani  - cumle GOSTERILEN kaynakta var mi? Atif dogrulugu, yani
                       Level 4. Yanlis numara vermek can yakmaz, uydurmak yakar;
                       bu yuzden kapi kanit_orani'ni kullaniyor.

    Dil modeli yeniden kosmuyor: cevaplar kayitli ve arama belirlenimci, ayni
    soru ayni parcalari getiriyor. Yalnizca cumle vektorleri uretiliyor.
    """
    import numpy as np

    veri = json.load(open(kayit_yolu, encoding="utf-8"))
    sorular = {s["id"]: s for s in json.load(open(POZITIF, encoding="utf-8"))}
    chunk_haritasi = {c["chunk_id"]: c
                      for c in json.load(open(CHUNKS, encoding="utf-8"))}
    # Parca vektorleri zaten diskte. Qdrant nokta numarasi chunks.json satir
    # sirasiyla ayni oldugu icin yeniden gommeye gerek yok.
    vek = np.load(os.path.join(ROOT, "_work", "embeddings", "BAAI_bge-m3.npy"))
    P._sorgu_vektoru("isitma")          # modeli bir kez yukle

    # Qdrant yerel modda depo klasorunu kilitliyor: defterde acik bir istemci
    # varken ikincisini acmak "already accessed by another instance" veriyor.
    # Acik istemci verilmisse onu kullaniyoruz ve kapatmiyoruz.
    kapat = istemci is None
    istemci = istemci or QI.ac()
    try:
        for tur in ("pozitif", "negatif"):
            kayitlar = veri["kayitlar"][tur]
            for i, kayit in enumerate(kayitlar, start=1):
                analiz = P.QP.analiz(kayit["soru"])
                qv = P._sorgu_vektoru(kayit["soru"])
                noktalar = QI.ara(istemci, qv, k=30, ilac=analiz["ilac"])
                if analiz["ilac"]:
                    hedefli = QI.ara(istemci, qv, k=k,
                                     zorunlu_ilac=analiz["ilac"])
                    varolan = {p.id for p in hedefli}
                    noktalar = hedefli + [p for p in noktalar
                                          if p.id not in varolan]
                secili = P.tekrar_ayikla(
                    P.baglam_sec(noktalar, analiz["ilac"]))[:k]

                govde = [(x["nokta"].id,
                          P._imza(x["nokta"].payload.get("content") or ""))
                         for x in secili]
                gv = np.stack([vek[nid] for nid, _ in govde]) if govde else None

                cumleler = [c.strip()
                            for c in P.CUMLE.split(kayit["cevap"].strip())
                            if len(c.strip()) > 15]
                skorlar = []
                if cumleler and gv is not None:
                    duz = [P.ATIF.sub("", c) for c in cumleler]
                    cv = P._MODEL.encode(duz, normalize_embeddings=True,
                                         convert_to_numpy=True)
                    for j, c in enumerate(cumleler):
                        nolar = set(P.atif_nolari(c))
                        im = P._imza(duz[j])
                        lek = [len(im & g) / max(1, len(im)) for _, g in govde]
                        sem = list(gv @ cv[j])
                        ai = [x - 1 for x in nolar if 1 <= x <= len(govde)]
                        skorlar.append({
                            "lek_hepsi": round(max(lek), 3),
                            "sem_hepsi": round(float(max(sem)), 3),
                            "lek_atif": round(max([lek[x] for x in ai],
                                                  default=0.0), 3),
                            "sem_atif": round(float(max([sem[x] for x in ai],
                                                        default=0.0)), 3),
                        })

                kayit["cumle_skorlari"] = skorlar
                # Alan kapisi sinyalleri. Leksik kapsam ise yaramadi: KUB'lerin
                # etkilesim bolumleri yuzlerce baska ilaci aniyor, o yuzden
                # "metformin" de "propranolol" de arsivde geciyor. Isleyen iki
                # sinyal: sorguda miyelom alanina ait bir varlik taninmasi, ve
                # getirilen parcalarin hastalik etiketi tasimasi.
                kayit["alan_varlik"] = P.alan_skoru(kayit["soru"], analiz)["varlik"]
                kayit["alan_hast"] = round(
                    sum(1 for x in secili
                        if (x["nokta"].payload.get("disease") or []))
                    / max(1, len(secili)), 3)
                # ATIF ONARIMI. Onarim deterministik: ayni cevap ve ayni
                # parcalar ayni sonucu veriyor. Bu yuzden dil modelini yeniden
                # kosturmadan, KAYITLI cevaplar uzerinde olculebiliyor - Level 4
                # kazancini 40 dakikalik bir GPU kosusu olmadan gorebiliyoruz.
                onarilmis, sayac = P.atif_onar(kayit["cevap"], secili)
                kayit["atif_onarimi"] = sayac
                kayit["cevap_onarilmis"] = onarilmis

                # Hedef tutma da yeniden hesaplaniyor: atif ayiklama duzeldi,
                # onceden toplu atif veren cevaplar "atifsiz" sayiliyordu.
                if tur == "pozitif":
                    def hedefi_tutuyor(metin):
                        for x in set(P.atif_nolari(metin)):
                            if not (1 <= x <= len(secili)):
                                continue
                            cid = secili[x - 1]["nokta"].payload.get("chunk_id")
                            c = chunk_haritasi.get(cid)
                            if c and any(chunk_uyar(c, h)
                                         for h in sorular[kayit["id"]]["hedef"]):
                                return True
                        return False
                    kayit["hedef_tuttu_onarim"] = hedefi_tutuyor(onarilmis)

                    tuttu = False
                    for x in set(P.atif_nolari(kayit["cevap"])):
                        if not (1 <= x <= len(secili)):
                            continue
                        cid = secili[x - 1]["nokta"].payload.get("chunk_id")
                        c = chunk_haritasi.get(cid)
                        if c and any(chunk_uyar(c, h)
                                     for h in sorular[kayit["id"]]["hedef"]):
                            tuttu = True
                            break
                    kayit["hedef_tuttu"] = tuttu
                kayit["atif_sayisi"] = len(set(P.atif_nolari(kayit["cevap"])))
                print(f"  {tur} {i}/{len(kayitlar)} {kayit['id']}   ",
                      end="\r", flush=True)
            print()
    finally:
        if kapat:
            istemci.close()

    json.dump(veri, open(cikti or kayit_yolu, "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    return veri


def oranlar(kayit, sem_esigi, lek_esigi=0.40):
    """Bir cevabin (kanit_orani, atif_orani) ikilisi."""
    s = kayit.get("cumle_skorlari") or []
    if not s:
        return 0.0, 0.0
    kanit = sum(1 for x in s
                if x["lek_hepsi"] >= lek_esigi or x["sem_hepsi"] >= sem_esigi)
    atif = sum(1 for x in s
               if x["lek_atif"] >= lek_esigi or x["sem_atif"] >= sem_esigi)
    return kanit / len(s), atif / len(s)


def gecti(k, arama_esigi, dayanak_esigi):
    """Kayit iki kapidan da geciyor mu?"""
    return (k["arama_skoru"] >= arama_esigi
            and k["dayanaklilik"] >= dayanak_esigi)


def puanla(poz, neg, arama_esigi, dayanak_esigi):
    cevaplanan = [k for k in poz if gecti(k, arama_esigi, dayanak_esigi)]
    uydurma = [k for k in neg if gecti(k, arama_esigi, dayanak_esigi)]
    return {
        "pozitif": len(poz),
        "cevaplanan": len(cevaplanan),
        # Cevaplanip hedefi tutan: sistemin gercekten ise yaradigi durum.
        "hedef_tutan": sum(1 for k in cevaplanan if k["hedef_tuttu"]),
        # Haksiz reddetme: bilgi arsivde var (butun pozitiflerin var) ama
        # sistem cevap vermedi. Guvenli tarafta kalmanin bedeli.
        "haksiz_red": len(poz) - len(cevaplanan),
        "ort_dayanaklilik": round(
            sum(k["dayanaklilik"] for k in poz) / max(1, len(poz)), 3),
        "negatif": len(neg),
        # Uydurma gecti: arsivde olmayan soruya cevap uretildi. SIFIR olmali.
        "uydurma_gecti": len(uydurma),
        "uydurma_idler": [k["id"] for k in uydurma],
    }


def esik_sec(poz_a, neg_a):
    """Esigi YALNIZCA A kumesinden sec.

    Oncelik sirasi: once uydurma sifir olmali (klinik sistemde pazarlik konusu
    degil), sonra hedef tutan sayisi en yuksek, esitlikte esik dusuk kalsin -
    gereksiz katilik haksiz reddetme uretir.
    """
    en_iyi, en_iyi_skor = None, None
    for a in ARAMA_ADAY:
        for d in DAYANAK_ADAY:
            p = puanla(poz_a, neg_a, a, d)
            skor = (p["uydurma_gecti"] == 0, p["hedef_tutan"], -d, -a)
            if en_iyi_skor is None or skor > en_iyi_skor:
                en_iyi_skor, en_iyi = skor, (a, d, p)
    return en_iyi


SEM_ADAY = [0.50, 0.55, 0.60, 0.65]

# Alan kapisi kural adaylari. "kapali" = kapi yok (karsilastirma tabani).
ALAN_KURAL = {
    "kapali":        lambda x: True,
    "varlik":        lambda x: x.get("alan_varlik", True),
    "varlik|hast75": lambda x: x.get("alan_varlik", True) or x.get("alan_hast", 1) >= 0.75,
    "varlik|hast100": lambda x: x.get("alan_varlik", True) or x.get("alan_hast", 1) >= 1.0,
    "hast75":        lambda x: x.get("alan_hast", 1) >= 0.75,
}


def puanla_yeni(poz, neg, arama_esigi, kanit_esigi, sem_esigi, alan="kapali"):
    kural = ALAN_KURAL[alan]

    def gec(x):
        kanit, _ = oranlar(x, sem_esigi)
        return (x["arama_skoru"] >= arama_esigi and kanit >= kanit_esigi
                and kural(x))

    cevaplanan = [x for x in poz if gec(x)]
    uydurma = [x for x in neg if gec(x)]
    atif_dogru = [x for x in cevaplanan if oranlar(x, sem_esigi)[1] >= 0.5]
    return {
        "pozitif": len(poz), "cevaplanan": len(cevaplanan),
        "hedef_tutan": sum(1 for x in cevaplanan if x["hedef_tuttu"]),
        # Level 4: cevaplananlarin kacinda atiflar dogru kaynagi gosteriyor.
        "atif_dogru": len(atif_dogru),
        "haksiz_red": len(poz) - len(cevaplanan),
        "ort_kanit": round(sum(oranlar(x, sem_esigi)[0] for x in poz)
                           / max(1, len(poz)), 3),
        "negatif": len(neg), "uydurma_gecti": len(uydurma),
        "uydurma_idler": [x["id"] for x in uydurma],
    }


def esik_sec_yeni(poz_a, neg_a):
    """Esikleri ve alan kuralini YALNIZCA A kumesinden sec.

    Siralama: once uydurma az olsun, sonra hedef tutan cok olsun. Uydurmayi
    kesin sifir sartina baglamiyoruz cunku ilk taramada hicbir kombinasyon
    sifir veremedi ve o zaman secim rastgele bir kombinasyona dusuyordu;
    negatif sayisini dogrudan kucultmek daha bilgilendirici.
    """
    en_iyi, en_iyi_skor = None, None
    for alan in ALAN_KURAL:
        for a in ARAMA_ADAY:
            for sem in SEM_ADAY:
                for d in DAYANAK_ADAY:
                    p = puanla_yeni(poz_a, neg_a, a, d, sem, alan)
                    skor = (-p["uydurma_gecti"], p["hedef_tutan"], -d, -a)
                    if en_iyi_skor is None or skor > en_iyi_skor:
                        en_iyi_skor, en_iyi = skor, (a, d, sem, alan, p)
    return en_iyi


def yeniden_rapor(kayit_yolu, k, istemci=None):
    veri = yeniden_puanla(kayit_yolu, k=k, istemci=istemci,
                          cikti=os.path.join(ROOT, "_logs",
                                             "level3_yeniden.json"))
    kp, kn = veri["kayitlar"]["pozitif"], veri["kayitlar"]["negatif"]
    pa, pb = bol(kp)
    na, nb = bol(kn)
    a, d, sem, alan, secim = esik_sec_yeni(pa, na)
    olcum = puanla_yeni(pb, nb, a, d, sem, alan)

    print("\nALAN KAPISI KARSILASTIRMASI (B kumesi, digerleri sabit):")
    for ad in ALAN_KURAL:
        t = puanla_yeni(pb, nb, a, d, sem, ad)
        print(f"  {ad:16s} cevaplanan {t['cevaplanan']:2d}/{t['pozitif']} "
              f"hedef {t['hedef_tutan']:2d} uydurma {t['uydurma_gecti']}/{t['negatif']}")

    print(f"\nESIK (yalnizca A kumesinden): arama {a}, kanit {d}, "
          f"anlamsal {sem}, alan kurali '{alan}'")
    print(f"KAPIDAN BAGIMSIZ: atif verilen parca hedefi tuttu "
          f"{sum(1 for x in kp if x['hedef_tuttu'])}/{len(kp)}")

    # LEVEL 4 - atif onarimi oncesi/sonrasi. Ikisi de ayni cevaplar uzerinde
    # olculuyor, yani fark tamamen atif atamasindan geliyor.
    onarimli = [x for x in kp if "hedef_tuttu_onarim" in x]
    if onarimli:
        ek = sum(x["atif_onarimi"]["eklenen"] for x in onarimli)
        dz = sum(x["atif_onarimi"]["duzeltilen"] for x in onarimli)
        br = sum(x["atif_onarimi"]["biraklan"] for x in onarimli)
        print(f"ATIF ONARIMI     : {ek} cumleye atif eklendi, {dz} duzeltildi, "
              f"{br} dayanaksiz birakildi")
        print(f"  onarim ONCESI  : {sum(1 for x in onarimli if x['hedef_tuttu'])}"
              f"/{len(onarimli)}")
        print(f"  onarim SONRASI : "
              f"{sum(1 for x in onarimli if x['hedef_tuttu_onarim'])}"
              f"/{len(onarimli)}")
        ob = [x for x in pb if "hedef_tuttu_onarim" in x]
        print(f"  B kumesi (esigin gormedigi): "
              f"{sum(1 for x in ob if x['hedef_tuttu'])} -> "
              f"{sum(1 for x in ob if x['hedef_tuttu_onarim'])} / {len(ob)}")
    for ad, s in (("SECIM (A - esigin gordugu)", secim),
                  ("OLCUM (B - esigin gormedigi)", olcum)):
        print(f"\n{ad}   pozitif {s['pozitif']}, negatif {s['negatif']}")
        print(f"  cevaplanan     {s['cevaplanan']:3d} / {s['pozitif']}")
        print(f"  hedefi tutan   {s['hedef_tutan']:3d} / {s['pozitif']}")
        print(f"  atifi dogru    {s['atif_dogru']:3d} / {s['cevaplanan']}")
        print(f"  haksiz red     {s['haksiz_red']:3d}")
        print(f"  ort kanit      {s['ort_kanit']}")
        print(f"  UYDURMA GECTI  {s['uydurma_gecti']:3d} / {s['negatif']}"
              f"  {s['uydurma_idler'] or ''}")
    veri["esik"] = {"arama": a, "kanit": d, "anlamsal": sem, "alan": alan}
    veri["secim_kumesi"], veri["olcum_kumesi"] = secim, olcum
    json.dump(veri, open(os.path.join(ROOT, "_logs", "level3_yeniden.json"),
                         "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("\n-> _logs/level3_yeniden.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--yeniden", default=None,
                    help="kayitli cevaplari yeniden puanla (json yolu)")
    ap.add_argument("--llm", default="sahte",
                    choices=["sahte", "ollama", "transformers"])
    ap.add_argument("--model", default=None)
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0, help="ilk N soru (deneme)")
    a = ap.parse_args()

    if a.yeniden:
        yeniden_rapor(a.yeniden, a.k)
        return

    poz = json.load(open(POZITIF, encoding="utf-8"))
    neg = json.load(open(NEGATIF, encoding="utf-8"))
    if a.limit:
        poz, neg = poz[:a.limit], neg[:max(2, a.limit // 5)]

    chunk_haritasi = {c["chunk_id"]: c
                      for c in json.load(open(CHUNKS, encoding="utf-8"))}

    llm = P.llm_kur(a.llm, a.model)
    istemci = QI.ac()
    try:
        print(f"pozitif {len(poz)} soru:")
        kp = ham_kos(llm, poz, istemci, chunk_haritasi, a.k, pozitif=True)
        print(f"negatif {len(neg)} soru:")
        kn = ham_kos(llm, neg, istemci, chunk_haritasi, a.k, pozitif=False)
    finally:
        istemci.close()

    pa, pb = bol(kp)
    na, nb = bol(kn)
    arama, dayanak, secim = esik_sec(pa, na)
    olcum = puanla(pb, nb, arama, dayanak)

    print(f"\nESIK (yalnizca A kumesinden secildi): "
          f"arama {arama}, dayanaklilik {dayanak}")
    for ad, s in (("SECIM  (A - esigin gordugu)", secim),
                  ("OLCUM  (B - esigin gormedigi)", olcum)):
        print(f"\n{ad}   pozitif {s['pozitif']}, negatif {s['negatif']}")
        print(f"  cevaplanan     {s['cevaplanan']:3d} / {s['pozitif']}")
        print(f"  hedefi tutan   {s['hedef_tutan']:3d} / {s['pozitif']}")
        print(f"  haksiz red     {s['haksiz_red']:3d}")
        print(f"  ort dayanak    {s['ort_dayanaklilik']}")
        print(f"  UYDURMA GECTI  {s['uydurma_gecti']:3d} / {s['negatif']}"
              f"  {s['uydurma_idler'] or ''}")

    json.dump({"llm": a.llm, "model": a.model, "k": a.k,
               "esik": {"arama": arama, "dayanaklilik": dayanak},
               "secim_kumesi": secim, "olcum_kumesi": olcum,
               "kayitlar": {"pozitif": kp, "negatif": kn}},
              open(RAPOR, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"\n-> {RAPOR}")


if __name__ == "__main__":
    main()
