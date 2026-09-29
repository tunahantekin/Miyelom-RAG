#!/usr/bin/env python
"""Dil modeli karsilastirmasi - ayni arsiv, ayni arama, farkli uretici model.

NOT: _scripts/run_bakeoff.py ile karistirma - o PDF PARSER karsilastirmasi.
Bu dosya cevabi ureten DIL MODELINI karsilastiriyor.

NE DEGISIYOR, NE SABIT

Sabit: chunk'lar, gomme modeli, arama, sorgu isleme, baglam secimi, istem,
esikler, atif onarimi. Degisen TEK sey cevabi ureten dil modeli. Bu yuzden
sonuclardaki fark modele atfedilebilir - baska turlu "hangi degisiklik neyi
yapti" sorusu cevapsiz kalirdi.

ASIRI UYUM ONLEMI - BURASI KRITIK

Model secmek de bir tur esik ayaridir. Dort modeli deneyip B kumesinde en
iyisini secersek B artik "esigin gormedigi veri" olmaz; sinavi dort kez
cozup en yuksek notu raporlamis oluruz. Bu yuzden:

    ELEME  : yalnizca A yarisinda (39 pozitif + 8 negatif), butun modeller
    OLCUM  : kazanan model, B yarisinda (39 pozitif + 7 negatif), TEK KEZ

--faz eleme ile A'da, --faz olcum ile B'de kosuyor. Karistirmamak icin rapor
dosyasi da faza gore isimleniyor.

Esikler her model icin YENIDEN SECILMIYOR. Zaten dondurulmus degerler
kullaniliyor; her modele kendi esigini secmek, her ogrenciye kendi sinavini
yazdirmak olurdu.

MALIYET

Model basina A yarisinda 47 soru, T4'te kabaca 20-30 dakika ve ~5 GB indirme.
Her modelden sonra GPU bellegi bosaltiliyor, yoksa ikincisi yuklenirken tasar.

Calistirma (Colab):
    python _scripts/llm_bakeoff.py --faz eleme --hepsi
    python _scripts/llm_bakeoff.py --faz olcum --model Qwen/Qwen2.5-7B-Instruct
    python _scripts/llm_bakeoff.py --karsilastir
"""
import argparse, gc, json, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))

import pipeline as P
import qdrant_index as QI
import answer_eval as AE

POZITIF = os.path.join(ROOT, "_work", "eval", "golden_queries.json")
NEGATIF = os.path.join(ROOT, "_work", "eval", "negative_queries.json")
CHUNKS = os.path.join(ROOT, "_work", "chunks", "chunks.json")
RAPOR_DIZIN = os.path.join(ROOT, "_logs", "bakeoff")

# Aday modeller. Hepsi acik erisim - kapili (gated) depolar HF tokeni istiyor
# ve teslim edilecek bir sistemde bu ek bir bagimlilik olurdu.
# Turkce agirlikli bir model bilerek listede: arsiv Ingilizce, sorular ve
# cevaplar Turkce, yani modelin Turkcesi dogrudan cevap kalitesine giriyor.
MODELLER = [
    {"ad": "Qwen/Qwen2.5-7B-Instruct", "gb": 7, "not": "mevcut temel"},
    {"ad": "Qwen/Qwen2.5-14B-Instruct", "gb": 12, "not": "4 bitte ~9,5 GB"},
    {"ad": "ytu-ce-cosmos/Turkish-Llama-8b-Instruct-v0.1", "gb": 8,
     "not": "Turkce odakli"},
    {"ad": "unsloth/Meta-Llama-3.1-8B-Instruct", "gb": 8,
     "not": "Llama 3.1 kapisiz ayna"},
    # DeepSeek ailesinden calistirilabilir tek secenek. MIT, 14B, dort bitte
    # ~9,5 GB. "Dusunen" model: cevaptan once <think> blogu uretiyor. O blok
    # TransformersLLM icinde ayiklaniyor ve token butcesi artiriliyor.
    {"ad": "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B", "gb": 12,
     "not": "DeepSeek ailesi, dusunen model"},
    # Qwen3.6-27B (22 Nisan 2026, Apache 2.0) dort bitte ~16,8 GB. T4'un 16
    # GB'ina SIGMAZ; L4 (24 GB) veya A100 gerekir. Liste otomatik suzuluyor.
    {"ad": "Qwen/Qwen3.6-27B", "gb": 22, "not": "L4/A100 gerekir"},
]

# DeepSeek V4 bilerek listede YOK. En kucuk acik surumu V4-Flash: 284 milyar
# parametre (13B aktif MoE), dort bitte 150 GB'in uzerinde - Colab'in hicbir
# GPU'suna sigmiyor. Tek erisim yolu API, o da klinik sorulari ve KUB
# metinlerini disari gondermek demek. Bu teknik degil veri yonetisimi
# kararidir ve kurumun onayi gerekir. Yerine ayni aileden R1-Distill-14B var.


def uygun_modeller(vram_gb):
    """Bu GPU'ya sigan modeller. Sigmayani calistirip OOM beklemek yerine
    bastan eliyoruz - iki saatlik kosu bir bellek hatasiyla comesin."""
    return [m for m in MODELLER if m["gb"] <= vram_gb]


def kisa_ad(model):
    return model.split("/")[-1].replace(".", "_")


def kume(faz):
    """A = eleme, B = olcum. answer_eval.bol ile ayni donusumlu bolme."""
    poz = json.load(open(POZITIF, encoding="utf-8"))
    neg = json.load(open(NEGATIF, encoding="utf-8"))
    pa, pb = AE.bol(poz)
    na, nb = AE.bol(neg)
    return (pa, na) if faz == "eleme" else (pb, nb)


def kos(model, faz, k=4, istemci=None, limit=0):
    poz, neg = kume(faz)
    if limit:
        poz, neg = poz[:limit], neg[:max(2, limit // 5)]
    chunk_haritasi = {c["chunk_id"]: c
                      for c in json.load(open(CHUNKS, encoding="utf-8"))}

    t0 = time.time()
    llm = P.llm_kur("transformers", model)
    yukleme = time.time() - t0
    print(f"  model yuklendi {yukleme:.0f}sn", flush=True)

    kapat = istemci is None
    istemci = istemci or QI.ac()
    try:
        kp = AE.ham_kos(llm, poz, istemci, chunk_haritasi, k, pozitif=True)
        kn = AE.ham_kos(llm, neg, istemci, chunk_haritasi, k, pozitif=False)
    finally:
        if kapat:
            istemci.close()

    os.makedirs(RAPOR_DIZIN, exist_ok=True)
    yol = os.path.join(RAPOR_DIZIN, f"{faz}_{kisa_ad(model)}.json")
    json.dump({"model": model, "faz": faz, "k": k,
               "yukleme_saniye": round(yukleme, 1),
               "kayitlar": {"pozitif": kp, "negatif": kn}},
              open(yol, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    # Modeli bellekten dus: ikinci model yuklenirken T4 tasiyor.
    del llm
    gc.collect()
    try:
        import torch
        torch.cuda.empty_cache()
    except Exception:
        pass
    return yol


def puanla(yol, k=4, istemci=None):
    """Kayitli cevaplari puanlar: anlamsal dayanaklilik + atif onarimi."""
    veri = AE.yeniden_puanla(yol, k=k, istemci=istemci)
    kp, kn = veri["kayitlar"]["pozitif"], veri["kayitlar"]["negatif"]
    s = AE.puanla_yeni(kp, kn, P.REDDET_ESIGI, P.DAYANAK_ESIGI, P.SEM_ESIGI,
                       P.ALAN_KURAL)
    onar = [x for x in kp if "hedef_tuttu_onarim" in x]
    s["atif_onarimsiz"] = sum(1 for x in kp if x["hedef_tuttu"])
    s["atif_onarimli"] = sum(1 for x in onar if x["hedef_tuttu_onarim"])
    s["ort_saniye"] = round(
        sum(x.get("saniye", 0) for x in kp + kn) / max(1, len(kp) + len(kn)), 1)
    # Bos ya da tek cumlelik cevap: bazi modeller istemi takip edemeyip
    # sadece "Bu bilgi arsivde bulunamadi" yaziyor. Ortalamalarda gorunmez,
    # ayrica sayilmasi lazim.
    s["bos_cevap"] = sum(1 for x in kp if len(x["cevap"].strip()) < 20)
    veri["ozet"] = s
    json.dump(veri, open(yol, "w", encoding="utf-8"), indent=1,
              ensure_ascii=False)
    return s


def karsilastir(faz):
    """Kayitli butun model sonuclarini tek tabloda basar."""
    if not os.path.isdir(RAPOR_DIZIN):
        print("henuz sonuc yok:", RAPOR_DIZIN)
        return
    satirlar = []
    for ad in sorted(os.listdir(RAPOR_DIZIN)):
        if not ad.startswith(f"{faz}_") or not ad.endswith(".json"):
            continue
        veri = json.load(open(os.path.join(RAPOR_DIZIN, ad), encoding="utf-8"))
        if veri.get("ozet"):
            satirlar.append((veri["model"], veri["ozet"]))

    if not satirlar:
        print(f"'{faz}' fazi icin puanlanmis sonuc yok")
        return

    print(f"\n{faz.upper()} KARSILASTIRMASI  "
          f"(esikler sabit: arama {P.REDDET_ESIGI}, kanit {P.DAYANAK_ESIGI}, "
          f"anlamsal {P.SEM_ESIGI}, alan '{P.ALAN_KURAL}')")
    print(f"{'model':42s} {'cevap':>7s} {'hedef':>6s} {'atif':>10s} "
          f"{'uydurma':>9s} {'red':>4s} {'bos':>4s} {'sn':>6s}")
    for model, s in satirlar:
        print(f"{model[:42]:42s} "
              f"{s['cevaplanan']:3d}/{s['pozitif']:<3d} "
              f"{s['hedef_tutan']:6d} "
              f"{s['atif_onarimsiz']:3d}->{s['atif_onarimli']:<5d} "
              f"{s['uydurma_gecti']:4d}/{s['negatif']:<4d} "
              f"{s['haksiz_red']:4d} {s['bos_cevap']:4d} {s['ort_saniye']:6.1f}")
    print("\nokuma: cevap = kapilardan gecip cevaplanan soru | hedef = golden "
          "hedefi tutan\natif = onarim oncesi -> sonrasi | uydurma = negatif "
          "kumede cevap uretilen (dusuk iyi)\nbos = 20 karakterden kisa cevap")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--faz", default="eleme", choices=["eleme", "olcum"])
    ap.add_argument("--model", default=None)
    ap.add_argument("--hepsi", action="store_true")
    ap.add_argument("--karsilastir", action="store_true")
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0, help="ilk N soru (deneme)")
    a = ap.parse_args()

    if a.karsilastir:
        karsilastir(a.faz)
        return

    if a.hepsi:
        modeller = [m["ad"] for m in MODELLER]
    else:
        modeller = [a.model or MODELLER[0]["ad"]]
    istemci = QI.ac()
    try:
        for i, model in enumerate(modeller, 1):
            print(f"\n[{i}/{len(modeller)}] {model}  ({a.faz})", flush=True)
            yol = kos(model, a.faz, k=a.k, istemci=istemci, limit=a.limit)
            s = puanla(yol, k=a.k, istemci=istemci)
            print(f"  cevaplanan {s['cevaplanan']}/{s['pozitif']}  "
                  f"hedef {s['hedef_tutan']}  "
                  f"atif {s['atif_onarimsiz']}->{s['atif_onarimli']}  "
                  f"uydurma {s['uydurma_gecti']}/{s['negatif']}  "
                  f"ort {s['ort_saniye']}sn", flush=True)
    finally:
        istemci.close()

    karsilastir(a.faz)


if __name__ == "__main__":
    main()
