#!/usr/bin/env python
"""ollama_sunucu.ipynb defterini uretir - Colab GPU'sunu uzak dil modeli yapar.

NE ISE YARIYOR

Sunum kullanicinin dizustunde yapilacak. Orada GTX 1650 (4 GB) var; 7B model
ancak yari yariya GPU'ya siginiyor ("50%/50% CPU/GPU") ve bir cevap 320-376
saniye suruyor. Canli soru sormak imkansiz.

Bu defter Colab'in T4'unde Ollama calistirip disariya bir adres aciyor. Yerel
makinedeki servis yalnizca URETIMI oraya gonderiyor; arsiv, arama, sorgu
isleme, kapilar ve atif onarimi YERELDE kaliyor. Yani gosterilen sistem
olculen sistemin ayni; degisen tek sey modelin hangi karti kullandigi.

NE GITMIYOR, NE GIDIYOR
  yerelde kalir : chunk'lar, gomme vektorleri, Qdrant, esikler, kapilar
  disari gider  : soru metni + baglama giren kaynak parcalari
Kilavuz metinleri acik kaynak oldugu icin sunum baglaminda sakincasiz. Hasta
verisi iceren bir kurulumda bu tercih ayrica degerlendirilmeli.

Calistirma:
    python _work/colab/ollama_sunucu_defter.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CIKTI = os.path.join(ROOT, "_work", "colab", "ollama_sunucu.ipynb")

H = []


def md(metin):
    H.append({"cell_type": "markdown", "metadata": {},
              "source": metin.strip().splitlines(keepends=True)})


def kod(metin):
    H.append({"cell_type": "code", "metadata": {}, "execution_count": None,
              "outputs": [], "source": metin.strip().splitlines(keepends=True)})


md("""
# Colab'ı uzak dil modeli sunucusu yap

**Neden:** sunum dizüstünde yapılacak. Orada GTX 1650 (4 GB) var ve 7B model
ancak yarı yarıya GPU'ya sığıyor — bir cevap 320-376 saniye sürüyor. Aynı
model Colab T4'te 10-30 saniyede bitiyor.

**Ne değişiyor:** yalnızca modelin çalıştığı yer. Arşiv, arama, sorgu işleme,
kapılar ve atıf onarımı yerel makinede kalıyor. Gösterilen sistem ölçülen
sistemin aynısı.

**Dışarı ne gidiyor:** soru metni ve bağlama giren kaynak parçaları. Kılavuz
metinleri açık kaynak olduğu için sunum bağlamında sakıncası yok; hasta verisi
işleyen bir kurulumda bu ayrıca değerlendirilmeli.

**Sıra:** 1 GPU, 2 Ollama kurulumu, 3 model, 4 tünel, 5 doğrulama.
Sunum boyunca bu sekme **açık kalmalı**.
""")

kod("""
# 1) GPU. T4 yeterli; 7B dort bitte ~5 GB.
!nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
""")

kod("""
# 2) Ollama kurulumu. ~1 dakika.
!curl -fsSL https://ollama.com/install.sh | sh

# Arka planda baslat. OLLAMA_HOST=0.0.0.0 sart: varsayilan 127.0.0.1 yalnizca
# Colab makinesinin icinden erisilebilir olurdu, tunel disaridan baglanamazdi.
import subprocess, time, os
os.environ['OLLAMA_HOST'] = '0.0.0.0:11434'
subprocess.Popen(['ollama', 'serve'],
                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(5)
!curl -s http://localhost:11434
""")

kod("""
# 3) Model. 4,7 GB, ~2 dakika. Yereldekiyle AYNI model olmali - baska bir
#    model kosturmak, olctugumuz sistemden baska bir seyi gostermek olurdu.
!ollama pull qwen2.5:7b
!ollama list
""")

kod("""
# 4) Tunel. cloudflared kayit istemiyor, tek komutla https adresi veriyor.
#    Adres her calistirmada DEGISIYOR; sunumdan hemen once acmak en iyisi.
!wget -q -O cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
!chmod +x cloudflared

import subprocess, re
p = subprocess.Popen(['./cloudflared', 'tunnel', '--url',
                      'http://localhost:11434', '--no-autoupdate'],
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                     text=True, bufsize=1)

ADRES = None
for satir in p.stdout:
    e = re.search(r'https://[-\\w]+\\.trycloudflare\\.com', satir)
    if e:
        ADRES = e.group(0)
        break
print('\\nADRES:', ADRES)
""")

kod("""
# 5) Calisiyor mu? Buradan cevap gelmiyorsa yerel makine de baglanamaz.
import json, urllib.request, time
t0 = time.time()
veri = json.dumps({'model': 'qwen2.5:7b', 'stream': False,
                   'options': {'temperature': 0},
                   'messages': [{'role': 'user',
                                 'content': 'Tek kelimeyle cevapla: 2+2 kac?'}]
                   }).encode()
r = urllib.request.Request(ADRES + '/api/chat', data=veri,
                           headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(r, timeout=300) as y:
    print(json.load(y)['message']['content'], f'({time.time()-t0:.0f} sn)')

print('\\n' + '=' * 64)
print('YEREL MAKINEDE _web/backend/.env DOSYASINA SU SATIRI EKLE:')
print(f'OLLAMA_URL={ADRES}')
print('=' * 64)
print('Sonra servisi yeniden baslat (Ctrl+C, tekrar uvicorn).')
""")

md("""
## Sunum boyunca

Bu sekme açık kalmalı. Colab boşta kalırsa oturumu düşürüyor; arada bir
hücreye tıklamak yeterli.

Bağlantı koparsa: 4. hücreyi tekrar çalıştır, **yeni adresi** `.env` içine
yaz, servisi yeniden başlat. Adres her tünelde değişiyor.

Yedek plan: `.env` içinden `OLLAMA_URL` satırını sil, servis yerel Ollama'ya
döner. Yavaş ama çalışır — önbellekteki demo soruları yine anında gelir.
""")

json.dump({"cells": H,
           "metadata": {"accelerator": "GPU",
                        "colab": {"provenance": []},
                        "kernelspec": {"display_name": "Python 3",
                                       "name": "python3"}},
           "nbformat": 4, "nbformat_minor": 0},
          open(CIKTI, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(H)} hucre -> {CIKTI}")
