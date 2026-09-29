#!/usr/bin/env python
"""olcum_b.ipynb defterini uretir - kazanan modelin B yarisinda TEK KEZ olcumu.

NEDEN AYRI DEFTER

llm_bakeoff.ipynb eleme fazi icin: bes modeli A yarisinda yaristiriyor. Bu
defter tek is yapiyor - kazanani B yarisinda kosturuyor. Ayri tutmanin sebebi
disiplin: B kumesi bir kez kullanilir. Ayni defterde durursa "bir daha
deneyelim" demek kolaylasir ve o an B'nin gorulmemis olma ozelligi biter.

Calistirma:
    python _work/colab/olcum_b_defter.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CIKTI = os.path.join(ROOT, "_work", "colab", "olcum_b.ipynb")

H = []


def md(metin):
    H.append({"cell_type": "markdown", "metadata": {},
              "source": metin.strip().splitlines(keepends=True)})


def kod(metin):
    H.append({"cell_type": "code", "metadata": {}, "execution_count": None,
              "outputs": [], "source": metin.strip().splitlines(keepends=True)})


md("""
# Ölçüm fazı — kazanan model, B yarısı, tek koşu

**Ne yapar:** Eleme fazını kazanan Qwen2.5-7B-Instruct'ı, eşiklerin hiç
görmediği 39 pozitif + 7 negatif soruda koşturur. Rapora girecek nihai rakam
budur.

**Neden tek kez:** eşikler A yarısına bakılarak seçildi, model de A yarısında
seçildi. B'nin değeri görülmemiş olmasından geliyor; ikinci kez koşturup
"daha iyi olanı" almak o değeri yok eder.

**Süre:** ~25 dakika (46 soru, T4 yeter — 27B gerekmiyor).

**Bağlantı koparsa:** defteri baştan çalıştır. Proje dosyaları Drive'dan
geliyor, sonuç da Drive'a yazılıyor.
""")

kod("""
# 1) GPU kontrolu. Bu defter icin T4 yeterli.
!nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
import torch
print('cuda:', torch.cuda.is_available())
""")

kod("""
# 2) Kurulum. 2-3 dakika.
!pip install -q sentence-transformers qdrant-client transformers accelerate bitsandbytes
import transformers
print('transformers', transformers.__version__)
""")

kod("""
# 3) Drive. Proje dosyalari ve sonuclar burada.
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
# 4) Proje dosyalari. Veri Drive'da varsa oradan geliyor (saniyeler).
#    SCRIPTLER HER SEFERINDE ISTENIYOR: yerelde duzeltme yapildiginda Drive'daki
#    kopya eskir ve sessizce ESKI KOD kosar - bu hata bir kez oldu.
import shutil, glob

VERI = {
    'chunks.json':           '_work/chunks',
    'golden_queries.json':   '_work/eval',
    'negative_queries.json': '_work/eval',
    'BAAI_bge-m3.npy':       '_work/embeddings',
    'BAAI_bge-m3.meta.json': '_work/embeddings',
}
SCRIPT = ['pipeline.py', 'answer_eval.py', 'llm_bakeoff.py', 'qdrant_index.py',
          'query_processing.py', 'chunk.py', 'plog.py', 'embed_chunks.py',
          'retrieval_eval.py']

shutil.rmtree(f'{KOK}/_scripts', ignore_errors=True)
for d in set(VERI.values()) | {'_scripts', '_logs/bakeoff'}:
    os.makedirs(f'{KOK}/{d}', exist_ok=True)

eksik_veri = [a for a in VERI if not os.path.exists(f'{DRIVE}/dosyalar/{a}')]
print('Veri Drive\\'da:', 'tamam' if not eksik_veri else f'EKSIK {eksik_veri}')
print('\\nSimdi dosya sec. GEREKENLER:')
print('  scriptler (her zaman):', ', '.join(SCRIPT))
if eksik_veri:
    print('  veri (ilk kurulum) :', ', '.join(eksik_veri))
print('  -> myeloma\\\\1 klasorunden hepsini secebilirsin (Ctrl+A)')

from google.colab import files
for ad in files.upload():
    temiz = ad
    for ek in (' (1)', ' (2)', ' (3)'):
        temiz = temiz.replace(ek, '')
    if temiz in SCRIPT:
        shutil.copy(ad, f'{DRIVE}/dosyalar/{temiz}')
        shutil.copy(ad, f'{KOK}/_scripts/{temiz}')
    elif temiz in VERI:
        shutil.copy(ad, f'{DRIVE}/dosyalar/{temiz}')

for a, d in VERI.items():
    if os.path.exists(f'{DRIVE}/dosyalar/{a}'):
        shutil.copy(f'{DRIVE}/dosyalar/{a}', f'{KOK}/{d}/{a}')
for a in SCRIPT:
    if (not os.path.exists(f'{KOK}/_scripts/{a}')
            and os.path.exists(f'{DRIVE}/dosyalar/{a}')):
        shutil.copy(f'{DRIVE}/dosyalar/{a}', f'{KOK}/_scripts/{a}')

hala = ([a for a, d in VERI.items() if not os.path.exists(f'{KOK}/{d}/{a}')]
        + [a for a in SCRIPT if not os.path.exists(f'{KOK}/_scripts/{a}')])
print('\\neksik:', hala or 'yok')
assert not hala, 'eksik dosya var - hucreyi tekrar calistir'
""")

kod("""
# 5) Qdrant koleksiyonu (~70 sn) ve YAMA KONTROLU.
#    Uc satir da True olmali; degilse eski script kosuyor demektir ve olcum
#    bastan gecersiz olur.
%env HF_HOME=/content/hf_cache
import sys, inspect
sys.path.insert(0, f'{KOK}/_scripts')
os.chdir(KOK)

import qdrant_index as QI
if not os.path.exists(f'{KOK}/_work/qdrant/meta.json'):
    QI.kur(yenile=True)
istemci = QI.ac()

import pipeline as P, answer_eval as AE, llm_bakeoff as LB
print('ham cikti saklama :', 'atif_onarim=False' in inspect.getsource(AE.ham_kos))
print('anlamsal dayanak  :', 'sem_esigi' in inspect.getsource(P.dayanaklilik))
print('alan kapisi bagli :', 'alan_gecti' in inspect.getsource(P.cevapla))
print('esikler:', P.REDDET_ESIGI, P.DAYANAK_ESIGI, P.SEM_ESIGI, P.ALAN_KURAL)
""")

md("""
## Koşu

Aşağıdaki hücre B yarısını koşturuyor. Eşikler `pipeline.py` içinde
dondurulmuş; bu defter onları **değiştirmiyor** ve yeniden seçmiyor.
""")

kod("""
# 6) OLCUM KOSUSU. 39 pozitif + 7 negatif, ~25 dakika.
MODEL = 'Qwen/Qwen2.5-7B-Instruct'      # eleme fazinin kazanani

import json, shutil
yol = f"{KOK}/_logs/bakeoff/olcum_{LB.kisa_ad(MODEL)}.json"
if os.path.exists(yol) and json.load(open(yol, encoding='utf-8')).get('ozet'):
    print('Bu olcum ZATEN yapilmis. B kumesi bir kez kullanilir;')
    print('tekrar kosturmak icin dosyayi bilerek sil:', yol)
else:
    yol = LB.kos(MODEL, 'olcum', k=4, istemci=istemci)
    s = LB.puanla(yol, k=4, istemci=istemci)
    shutil.copy(yol, f'{DRIVE}/sonuclar/{os.path.basename(yol)}')
    print('\\nkaydedildi:', yol)
""")

kod("""
# 7) NIHAI RAKAMLAR. Rapora girecek olan bunlar.
import json, statistics as st
v = json.load(open(f"{KOK}/_logs/bakeoff/olcum_{LB.kisa_ad(MODEL)}.json",
                   encoding='utf-8'))
s, kp = v['ozet'], v['kayitlar']['pozitif']

print('OLCUM FAZI - B yarisi (esiklerin hic gormedigi)')
print(f"  model              {v['model']}")
print(f"  cevaplanan         {s['cevaplanan']}/{s['pozitif']}")
print(f"  hedefi tutan       {s['hedef_tutan']}/{s['pozitif']}")
print(f"  atif isabeti       {s['atif_onarimsiz']} -> {s['atif_onarimli']}"
      f"   (onarim oncesi -> sonrasi)")
print(f"  haksiz red         {s['haksiz_red']}")
print(f"  ort kanit orani    {s['ort_kanit']}")
print(f"  uydurma            {s['uydurma_gecti']}/{s['negatif']}"
      f"   <- bu kume KIRLENMIS, gecerli rakam taze kumeden 0/15")
print(f"  soru basina        {s['ort_saniye']} sn")
print(f"  ort cevap uzunlugu {int(st.mean(len(x['cevap']) for x in kp))} karakter")

o = {k: sum(x['atif_onarimi'][k] for x in kp)
     for k in ('eklenen', 'duzeltilen', 'biraklan')}
print(f"  atif onarimi       {o['eklenen']} eklendi, {o['duzeltilen']} duzeltildi, "
      f"{o['biraklan']} dayanaksiz birakildi")

from google.colab import files
files.download(f"{KOK}/_logs/bakeoff/olcum_{LB.kisa_ad(MODEL)}.json")
""")

md("""
## Bittikten sonra

İnen `olcum_Qwen2_5-7B-Instruct.json` dosyasını `_logs\\bakeoff\\` içine koy ve
ekran çıktısını yapıştır.

Bu rakamlar `_logs\\KARAR_KAYDI.md` ve `_logs\\SUNUM_METNI.md` içine işlenecek.
Ondan sonra ölçüm işi kapanıyor, FastAPI + React katmanına geçiliyor.

**Uydurma sütununa dikkat:** bu koşudaki 7 negatif ilk kümeden geliyor ve o
küme kirlenmiş (N14 düzeltmesi o kümeyi görerek yapılmıştı). Uydurma için
raporlanacak rakam taze kümeden: 15 soruda 13 red, 0 uydurma.
""")

json.dump({"cells": H,
           "metadata": {"accelerator": "GPU",
                        "colab": {"provenance": []},
                        "kernelspec": {"display_name": "Python 3",
                                       "name": "python3"}},
           "nbformat": 4, "nbformat_minor": 0},
          open(CIKTI, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(H)} hucre -> {CIKTI}")
