# Web katmanı — kurulum ve çalıştırma

İki senaryo var ve **kod ikisinde de aynı**; fark yalnızca
`_web/backend/.env` dosyasında.

| | Sunum (senin makinen) | Üretim (kurumun sunucusu) |
|---|---|---|
| Dil modeli | Ollama, GTX 1650 (yarı GPU) | transformers, GPU 4-bit |
| Cevap süresi | 60-380 sn (ölçüldü) | 10-30 sn |
| Önbellek | açık | kapalı |
| Erişim | yalnızca localhost | dışarıya servis |

---

## Sunum kurulumu (tek seferlik)

### 1. Ollama

[ollama.com/download](https://ollama.com/download) adresinden Windows sürümünü
kur. **Kurulumdan önce** model dizinini D: sürücüsüne al — model 4,7 GB ve C:
sürücüsünde 30 GB kaldı:

```powershell
setx OLLAMA_MODELS "D:\ollama"
```

Terminali kapatıp aç, sonra modeli indir:

```powershell
ollama pull qwen2.5:7b
ollama list          # qwen2.5:7b görünmeli
```

### 2. Python paketleri — **bu adım yapıldı**

Sanal ortam kurmuyoruz. Sistem Python'unda (3.14.3) torch, numpy, fastapi,
uvicorn ve dotenv zaten vardı; yeni bir ortam kurmak torch'u sıfırdan
indirtirdi (~2,5 GB) ve ilk denemede takılan yer büyük olasılıkla burasıydı.

Eksik iki paket kuruldu, bir de sürüm çakışması giderildi:

```powershell
python -m pip install sentence-transformers qdrant-client
python -m pip install --upgrade protobuf
```

**protobuf neden yükseltildi:** `qdrant-client`, protobuf'un C++ hızlandırıcısını
yüklemeye çalışıyor; protobuf 4.25'in o eklentisi Python 3.14 ile uyumsuz ve
`TypeError: Metaclasses with custom tp_new are not supported` hatası veriyor.
Hata paket kurulurken değil **ilk sorguda** çıkıyor, bu yüzden sinsi. 7.35 ile
düzeldi.

Ayarları kopyala:

```powershell
cd C:\Users\Tunahan\Desktop\myeloma\_web\backend
copy .env.ornek .env
```

`.env` varsayılan haliyle sunum senaryosuna ayarlı, değiştirmene gerek yok.

Kurulumu doğrula — bu komut arşivi açıp bir soru sorar, dil modeli gerekmez:

```powershell
cd C:\Users\Tunahan\Desktop\myeloma
python -c "import sys; sys.path.insert(0,'_scripts'); import pipeline as P, qdrant_index as Q; c=Q.ac(); r=P.cevapla('Karfilzomib hangi dozda uygulanir?', istemci=c); print('skor', r['guven']['arama_skoru'], '| kaynak', len(r['kaynaklar'])); c.close()"
```

`skor 0.737 | kaynak 4` benzeri bir satır görüyorsan arama katmanı çalışıyor.
İlk çalıştırma ~80 saniye sürer, gömme modeli belleğe yükleniyor.

### 3. Arayüz

```powershell
cd ..\frontend
npm install
```

---

## Çalıştırma

İki terminal gerekiyor.

**Terminal 1 — servis:**

```powershell
cd C:\Users\Tunahan\Desktop\myeloma\_web\backend
python -m uvicorn app:uygulama --host 127.0.0.1 --port 8000 --workers 1
```

**Neden `python -m` var:** paketler sistem Python'una kurulduğu için
`uvicorn.exe` dosyasının bulunduğu `Scripts` klasörü PATH'e eklenmemiş. Düz
`uvicorn` yazınca *"The term 'uvicorn' is not recognized"* alırsın. `python -m
uvicorn` aynı programı çalıştırır, PATH'e ihtiyaç duymaz.

İlk açılış 30-60 saniye sürer: gömme modeli (BGE-M3, ~2,3 GB) belleğe
yükleniyor. `hazir: ollama/qwen2.5:7b, 13857 chunk...` satırını görünce hazır.

**`--workers 1` şart.** Qdrant gömülü modda depo klasörünü işletim sistemi
kilidiyle tutuyor; ikinci bir işçi açılırsa *"already accessed by another
instance"* hatası verir.

**Terminal 2 — arayüz:**

```powershell
cd C:\Users\Tunahan\Desktop\myeloma\_web\frontend
npm run dev
```

Tarayıcıda `http://localhost:5173`.

---

## Sunum öncesi ısıtma

Cevaplar önbelleğe yazılıyor ve çözümleme açgözlü (`temperature 0`), yani aynı
soru aynı cevabı veriyor. Sunumdan önce beş örnek soruyu bir kez çalıştır;
sunum sırasında hepsi anında gelir.

Önbellekten gelen cevap arayüzde **"önbellekten"** rozetiyle işaretleniyor. Bu
bilerek böyle: klinik bir sistemde "bu cevap şimdi mi üretildi" sorusunun
cevabı gizlenmemeli. Canlı üretimi göstermek istersen önbellekte olmayan bir
soru sor.

Önbelleği temizlemek için `_work/onbellek.json` dosyasını sil.

---

## Üretime taşırken

`.env` içindeki üretim bloğunu aç, sunum bloğunu kapat. Ek olarak üç şey:

**Qdrant sunucu moduna geçmeli.** Gömülü mod tek işlem kilidi yüzünden tek
işçiyle sınırlı. Eşzamanlı kullanıcı gerekiyorsa Qdrant'ı Docker ile ayağa
kaldırıp `_scripts/qdrant_index.py` içindeki `ac()` fonksiyonunu adrese
bağlamak yeterli — kalan kod değişmiyor.

**CORS kökeni.** `.env` içindeki `KOKEN` değerini arayüzün gerçek adresiyle
değiştir. Yıldız (`*`) kullanma.

**Kimlik doğrulama yok.** Şu an servis açık; dışarıya açılacaksa kurumun kimlik
doğrulama katmanı önüne konmalı. Bu bilinçli bir eksik, sunumda da böyle
söylenmeli.

---

## Sorun giderme

**`already accessed by another instance`** — başka bir Python süreci Qdrant
deposunu tutuyor. Açık Colab/terminal oturumlarını kapat, `--workers 1`
kullandığından emin ol.

**Arayüz açılıyor ama cevap gelmiyor** — servis terminaline bak. `/api/saglik`
adresini tarayıcıda aç; JSON dönmüyorsa servis ayakta değil.

**Ollama bağlanamıyor** — `ollama list` çalışıyor mu? Ollama servisi Windows'ta
arka planda çalışır; kapalıysa `ollama serve` ile başlat.

**Cevap çok yavaş** — 4 GB'lık kartta beklenen davranış, hata değil.
`qwen2.5:3b` ile hızlanırdı ama ölçümlerimiz 7B ile yapıldı; küçük modele
inmek gösterilen sistemi ölçülenden ayırırdı. Bilerek yapılmadı.

---

## Hız: yerel GPU ve beklenen süreler

Bu makinede GTX 1650 var (4 GB). Ollama GPU'yu kullanıyor ama model 5,1 GB
olduğu için ancak yarısı sığıyor — `ollama ps` çıktısı `50%/50% CPU/GPU`
diyor. Ölçülen süreler:

| durum | süre |
|---|---|
| önbellekteki soru | anında |
| arşiv dışı soru (alan kapısı) | ~1 sn, model hiç çağrılmıyor |
| kısa cevap | 60-130 sn |
| uzun cevap (doz şeması, çok kaynaklı) | 200-380 sn |

**Karar: her şey yerelde kalıyor.** Colab'a taşıma ve daha küçük modele inme
seçenekleri değerlendirildi, ikisi de bırakıldı. Bekleme kabul edildi; buna
karşılık gösterilen sistem ölçülen sistemin **birebir aynısı** oluyor —
raporlanan rakamlar Qwen2.5-7B ile alındı ve demoda koşan da o.

Beklerken ekranda geçen saniye sayacı görünüyor, yani sistemin donmadığı belli
oluyor. Anlatılacak şey de hazır: arşivden getirilen kaynaklar o sırada zaten
listede duruyor.

*(İsteğe bağlı, kullanılmıyor: `.env` içindeki `OLLAMA_URL` satırı üretimi uzak
bir Ollama sunucusuna yönlendirebiliyor. Karar gereği boş bırakıldı.)*

---

## Sunum kontrol listesi

- [ ] Ollama açık (`http://localhost:11434` → "Ollama is running")
- [ ] `http://localhost:5173` açılıyor
- [ ] Beş örnek soru önbellekte (rozetle görünür)
- [ ] Hazırladığın `.txt` sorularından ikisi önceden denendi
- [ ] Arşiv dışı soru denendi — reddetme **1 saniyede** geliyor, model hiç
      çağrılmıyor. Bekleme olmadığı için canlı göstermeye en uygun senaryo bu.
