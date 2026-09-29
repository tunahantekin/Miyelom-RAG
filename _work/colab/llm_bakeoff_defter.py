#!/usr/bin/env python
"""llm_bakeoff.ipynb defterini uretir.

Defteri elle JSON olarak yazmak yerine buradan uretiyoruz: hucre metinleri
Python dizesi olarak okunakli duruyor, tek yerden degistirilebiliyor ve
bozuk JSON riski kalmiyor.

Calistirma:
    python _work/colab/llm_bakeoff_defter.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CIKTI = os.path.join(ROOT, "_work", "colab", "llm_bakeoff.ipynb")

H = []


def md(metin):
    H.append({"cell_type": "markdown", "metadata": {},
              "source": metin.strip().splitlines(keepends=True)})


def kod(metin):
    H.append({"cell_type": "code", "metadata": {}, "execution_count": None,
              "outputs": [], "source": metin.strip().splitlines(keepends=True)})


md("""
# Dil modeli karşılaştırması — eleme fazı

**Ne yapar:** Aynı arşiv, aynı arama, aynı istem ve aynı eşiklerle farklı
üretici modelleri koşturur. Değişen tek şey model; böylece sonuçtaki fark
modele atfedilebilir.

**Neden A yarısında:** model seçmek de bir tür eşik ayarıdır. Modelleri
deneyip B yarısında en iyisini seçersek B artık "görülmemiş veri" olmaz.
Kazanan model sonra B'de **tek kez** ölçülecek.

**Oturum koparsa:** her model kendi dosyasına yazıyor ve sonuç Drive'a
kopyalanıyor. Defteri baştan çalıştır; biten modeller atlanır.

**Sıra:** 1-2 kurulum, 3 Drive, 4 proje dosyaları, 5 Qdrant, 6 model listesi,
7 koşu, 8 karşılaştırma.
""")

kod("""
# 1) GPU. Model listesi buna gore suzulecek: 27B model T4'e sigmiyor.
!nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
import torch
VRAM = (round(torch.cuda.get_device_properties(0).total_memory / 1e9, 1)
        if torch.cuda.is_available() else 0)
print('cuda:', torch.cuda.is_available(), '| VRAM (GB):', VRAM)
""")

kod("""
# 2) Kurulum. 2-3 dakika.
!pip install -q sentence-transformers qdrant-client transformers accelerate bitsandbytes
import transformers, sentence_transformers
print('transformers', transformers.__version__)
""")

md("""
## Drive neden ve ne için

Model önbelleğini Drive'a koymak **işe yaramıyor**: Hugging Face indirmesi
Colab'da çok hızlı, Drive okuması ise binlerce küçük dosyada tıkanıyor. 5 GB'lık
bir modeli Drive'dan yüklemek yeniden indirmekten uzun sürer.

Drive'ın değerli olduğu yer başka: her oturumda elle yüklediğin proje dosyaları
(chunks 30 MB + gömmeler 57 MB) ve **sonuçlar**. Oturum koptuğunda saatlerce
süren koşunun çıktısı kaybolmasın diye her model bittiğinde Drive'a yazılıyor.
""")

kod("""
# 3) Drive'i bagla. Proje dosyalari ve sonuclar burada duracak.
from google.colab import drive
drive.mount('/content/drive')

import os
DRIVE = '/content/drive/MyDrive/myeloma_bakeoff'
os.makedirs(f'{DRIVE}/dosyalar', exist_ok=True)
os.makedirs(f'{DRIVE}/sonuclar', exist_ok=True)
KOK = '/content/myeloma'
print('drive:', DRIVE)
""")

kod("""
# 4) Proje dosyalari. Drive'da varsa oradan kopyalanir (saniyeler), yoksa bir
#    kez elle yuklenir ve Drive'a yazilir - bir daha yuklemek gerekmez.
import shutil, glob

YER = {
    'chunks.json':           '_work/chunks',
    'golden_queries.json':   '_work/eval',
    'negative_queries.json': '_work/eval',
    'BAAI_bge-m3.npy':       '_work/embeddings',
    'BAAI_bge-m3.meta.json': '_work/embeddings',
    'pipeline.py':           '_scripts',
    'answer_eval.py':        '_scripts',
    'llm_bakeoff.py':        '_scripts',
    'qdrant_index.py':       '_scripts',
    'query_processing.py':   '_scripts',
    'chunk.py':              '_scripts',
    'plog.py':               '_scripts',
    'embed_chunks.py':       '_scripts',
    'retrieval_eval.py':     '_scripts',
}

shutil.rmtree(f'{KOK}/_scripts', ignore_errors=True)
for d in set(YER.values()) | {'_logs/bakeoff'}:
    os.makedirs(f'{KOK}/{d}', exist_ok=True)

eksik = [a for a in YER if not os.path.exists(f'{DRIVE}/dosyalar/{a}')]
if eksik:
    print('Drive\\'da eksik:', eksik)
    print('-> myeloma\\\\1 klasorunden bu dosyalari sec (hepsini secebilirsin)')
    from google.colab import files
    for ad in files.upload():
        temiz = ad
        for ek in (' (1)', ' (2)', ' (3)'):
            temiz = temiz.replace(ek, '')
        if temiz in YER:
            shutil.copy(temiz if os.path.exists(temiz) else ad,
                        f'{DRIVE}/dosyalar/{temiz}')
            print('  drive\\'a yazildi:', temiz)

for a, d in YER.items():
    kaynak = f'{DRIVE}/dosyalar/{a}'
    if os.path.exists(kaynak):
        shutil.copy(kaynak, f'{KOK}/{d}/{a}')

hala = [a for a, d in YER.items() if not os.path.exists(f'{KOK}/{d}/{a}')]
print('eksik:', hala or 'yok')
assert not hala, 'eksik dosya var - hucreyi tekrar calistir'

# Onceki oturumlarin sonuclarini geri getir (kaldigi yerden devam icin).
for y in glob.glob(f'{DRIVE}/sonuclar/*.json'):
    shutil.copy(y, f'{KOK}/_logs/bakeoff/{os.path.basename(y)}')
print('drive\\'dan donen sonuc:', len(glob.glob(f'{KOK}/_logs/bakeoff/*.json')))
""")

kod("""
# 5) Qdrant koleksiyonu. ~70 saniye. Depoyu Drive'a koymuyoruz: 169 MB ve
#    Drive uzerinden okumak aramayi yavaslatir, yeniden kurmak daha hizli.
%env HF_HOME=/content/hf_cache
import sys
sys.path.insert(0, f'{KOK}/_scripts')
os.chdir(KOK)

import qdrant_index as QI
if not os.path.exists(f'{KOK}/_work/qdrant/meta.json'):
    QI.kur(yenile=True)
istemci = QI.ac()
print('koleksiyon hazir')
""")

kod("""
# 6) Bu GPU'ya sigan modeller. Sigmayani calistirip OOM beklemek yerine
#    bastan eliyoruz - saatlerce suren kosu bellek hatasiyla comesin.
import llm_bakeoff as LB

uygun = LB.uygun_modeller(VRAM)
print(f'VRAM {VRAM} GB icin uygun modeller:')
for m in uygun:
    print(f"  {m['ad']:48s} ~{m['gb']} GB   {m['not']}")
for m in [x for x in LB.MODELLER if x not in uygun]:
    print(f"  ATLANIYOR {m['ad']} (~{m['gb']} GB gerekiyor)")
print('\\n27B modeli denemek istersen: Runtime > Change runtime type > L4 GPU')
""")

kod("""
# 7) KOSU. Model basina ~5 GB indirme + 47 soru. T4'te model basina 20-30 dk.
#    Her model bitince sonuc Drive'a yaziliyor: oturum koparsa kayip olmuyor.
import importlib, json, gc, torch
import pipeline as P, answer_eval as AE
for m in (P, AE, LB):
    importlib.reload(m)

for i, mm in enumerate(uygun, 1):
    model = mm['ad']
    yol = f"{KOK}/_logs/bakeoff/eleme_{LB.kisa_ad(model)}.json"
    if os.path.exists(yol) and json.load(open(yol, encoding='utf-8')).get('ozet'):
        print(f'[{i}] {model} - zaten var, atlaniyor')
        continue
    print(f'\\n[{i}/{len(uygun)}] {model}', flush=True)
    try:
        yol = LB.kos(model, 'eleme', k=4, istemci=istemci)
        s = LB.puanla(yol, k=4, istemci=istemci)
        print(f"  cevaplanan {s['cevaplanan']}/{s['pozitif']}  "
              f"hedef {s['hedef_tutan']}  "
              f"atif {s['atif_onarimsiz']}->{s['atif_onarimli']}  "
              f"uydurma {s['uydurma_gecti']}/{s['negatif']}  "
              f"ort {s['ort_saniye']}sn", flush=True)
        shutil.copy(yol, f'{DRIVE}/sonuclar/{os.path.basename(yol)}')
    except Exception as e:
        # Bir model yuklenemezse digerleri devam etsin - saatlerce suren kosu
        # tek modelin hatasiyla comeyi hak etmiyor.
        print(f'  HATA ({type(e).__name__}): {e}')
        gc.collect(); torch.cuda.empty_cache()
""")

kod("""
# 8) Karsilastirma tablosu ve indirme.
LB.karsilastir('eleme')
shutil.make_archive('/content/bakeoff', 'zip', f'{KOK}/_logs/bakeoff')
from google.colab import files
files.download('/content/bakeoff.zip')
""")

md("""
## 9) Tek modeli yeniden koşturmak (isteğe bağlı)

Bir modelin sonucu geçersiz çıktıysa (ölçüm hatası, script düzeltmesi) yalnızca
onu yeniden koşturmak için bu hücreyi kullan. Diğer modellerin sonuçlarına
dokunmuyor.

**Qwen3.6-27B için gerekçe:** ilk koşuda model düşünme sürecini düz metin
olarak cevaba yazdı ("Here's a thinking process: ... Rules: 1. Only use
provided source texts"). `<think>` etiketi kullanmadığı için ayıklayıcı
yakalayamadı; 39 cevabın 39'u böyleydi. `pipeline.py` artık sohbet şablonunu
`enable_thinking=False` ile çağırıyor.

Bu hücre güncel `pipeline.py` ve `answer_eval.py` dosyalarını **yeniden
istiyor**, çünkü Drive'daki kopyalar eski. `1` klasöründen o ikisini seç.
""")

kod("""
# 9) TEK MODEL YENIDEN KOSU.
MODEL = 'Qwen/Qwen3.6-27B'      # kosturulacak model
import importlib, shutil, os, json
from google.colab import files

print('Guncel pipeline.py ve answer_eval.py sec:')
for ad in files.upload():
    temiz = ad
    for ek in (' (1)', ' (2)', ' (3)'):
        temiz = temiz.replace(ek, '')
    if temiz in ('pipeline.py', 'answer_eval.py', 'llm_bakeoff.py'):
        shutil.copy(ad, f'{DRIVE}/dosyalar/{temiz}')     # Drive da guncellensin
        shutil.copy(ad, f'{KOK}/_scripts/{temiz}')
        print('  guncellendi:', temiz)

import pipeline as P, answer_eval as AE, llm_bakeoff as LB
for m in (P, AE, LB):
    importlib.reload(m)

# Duzeltmeler yuklu mu? Degilse kosmanin anlami yok - ikisi de True olmali.
import inspect
print('enable_thinking yamasi :',
      'enable_thinking' in inspect.getsource(P.TransformersLLM.uret))
print('ham cikti saklama yamasi:',
      'atif_onarim=False' in inspect.getsource(AE.ham_kos))

# Eski sonucu sil, yoksa 7. hucredeki gibi "zaten var" diye atlanir.
yol = f"{KOK}/_logs/bakeoff/eleme_{LB.kisa_ad(MODEL)}.json"
for y in (yol, f"{DRIVE}/sonuclar/{os.path.basename(yol)}"):
    if os.path.exists(y):
        os.remove(y)
        print('silindi:', y)

import gc, torch
try:
    del llm
except NameError:
    pass
gc.collect(); torch.cuda.empty_cache()

yol = LB.kos(MODEL, 'eleme', k=4, istemci=istemci)
s = LB.puanla(yol, k=4, istemci=istemci)
shutil.copy(yol, f'{DRIVE}/sonuclar/{os.path.basename(yol)}')
print(f"\\ncevaplanan {s['cevaplanan']}/{s['pozitif']}  hedef {s['hedef_tutan']}  "
      f"atif {s['atif_onarimsiz']}->{s['atif_onarimli']}  "
      f"uydurma {s['uydurma_gecti']}/{s['negatif']}  "
      f"kanit {s['ort_kanit']}  ort {s['ort_saniye']}sn")

# Duzeldi mi? Ilk kosuda ortalama 1772 karakter ve 39/39 sizinti vardi.
import statistics as st
kp = json.load(open(yol, encoding='utf-8'))['kayitlar']['pozitif']
print('ort cevap uzunlugu :', int(st.mean(len(x['cevap']) for x in kp)))
print('dusunme sizan cevap:',
      sum(1 for x in kp if 'thinking process' in x['cevap'].lower()))

LB.karsilastir('eleme')
""")

md("""
## Bittikten sonra

`bakeoff.zip` dosyasını `_logs\\bakeoff\\` içine aç ve tabloyu bana yapıştır.

Okuma kılavuzu: **cevap** kapılardan geçip cevaplanan soru sayısı, **hedef**
golden hedefi tutan, **atıf** onarım öncesi → sonrası, **uydurma** negatif
kümede cevap üretilen (düşük iyi), **boş** 20 karakterden kısa cevap, **sn**
soru başına süre.

Süre sütunu teslim kararı için kritik: sistem hastanede CPU'da çalışacaksa
buradaki farklar on katına çıkar.
""")

json.dump({"cells": H,
           "metadata": {"accelerator": "GPU",
                        "colab": {"provenance": []},
                        "kernelspec": {"display_name": "Python 3",
                                       "name": "python3"}},
           "nbformat": 4, "nbformat_minor": 0},
          open(CIKTI, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(H)} hucre -> {CIKTI}")
