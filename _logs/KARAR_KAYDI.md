# Karar ve Ölçüm Kaydı

`DURUM.md` kronolojik bir günlük: ne zaman ne olduğunu anlatıyor, ama içinde
sonradan geçersizleşmiş satırlar da var. Bu dosya farklı bir soruya cevap
veriyor: **bugün doğru olan nedir, hangi rakama dayanıyor, ham verisi nerede.**

Son güncelleme: 2026-08-09

---

## 1. Dondurulmuş kararlar

Aşağıdakiler ölçülerek seçildi ve değiştirilmemeli. Değiştirilirse ilgili
ölçümün tekrarlanması gerekir.

**Bölümleme.** Başlık sınırlarına saygılı, tabloları bölmeyen, dipnotu
gövdesine bağlayan yapı farkında bölümleme. Tavan 800 token, yalnızca düz metin
arasında 40 token örtüşme. Gerekçe: yapı farkında olmayan bölümlemede 909
"bölünmüş tablo" bulgusu vardı, bu kurallarla 23'e indi. *(`_scripts/chunk.py`,
ölçüm `_logs/chunk_validation.json`)*

**Gömme modeli.** BAAI/bge-m3, 1024 boyut, çok dilli. Arşiv İngilizce, sorular
Türkçe — tek dilli bir model bu boşluğu geçemezdi.

**Arama.** Qdrant gömülü mod, yoğun arama + ilaç varlığı tanınırsa filtreli
ikinci arama. Gerekçe: TECVAYLI ürün bilgisi genel aramada ilk 30'a giremiyordu
(soru Türkçe, belge İngilizce). *(`_scripts/qdrant_index.py`)*

**Sorgu işleme.** Marka→etken madde normalizasyonu, BM25 için İngilizce INN ve
ATC ile genişletme, üç kovalı yumuşak yeniden sıralama. Sert filtre
kullanılmıyor çünkü chunk'ların yalnızca %61'i `drug_names` taşıyor.
*(`_scripts/query_processing.py`)*

**Yeniden sıralayıcı kullanılmıyor.** Ölçüldü, sıralamayı iyileştiriyor, ama
GPU bağımlılığı getiriyor. Bu bir eksik değil, ölçülmüş bir tercih.

**Eşikler** — A yarısında seçildi, B yarısı görülmeden:

| sabit | değer | anlamı |
|---|---|---|
| `REDDET_ESIGI` | 0,50 | en iyi parça skoru bunun altındaysa cevap yok |
| `DAYANAK_ESIGI` | 0,20 | dayanaklı cümle oranı eşiği |
| `SEM_ESIGI` | 0,50 | bir cümlenin "kaynakta var" sayılma eşiği |
| `ALAN_KURAL` | `varlik\|hast75` | alan kapısı kuralı |

**Üretici model: Qwen2.5-7B-Instruct.** Beş model karşılaştırıldı, hedef
tutmada hepsi aynı bantta (21-22/39). Seçim doğruluk için değil hız ve donanım
için: 11,1 sn ve ~5 GB, alternatifi 38,3 sn ve 24 GB GPU.

---

## 2. Ölçüm kaydı

Her satır: ne ölçüldü, hangi kümede, sonuç, ham veri nerede.

**Level 1 — yapısal.** Ground truth yok, iç tutarlılık ölçülüyor: bölünmüş
tablo, sahipsiz parent, yarım cümle. Bölünmüş tablo 909 → 23.
*(`_logs/structural_validation.json`, `_logs/chunk_validation.json`)*

**Level 2 — getirme.** 78 golden soru, dört yöntem karşılaştırıldı (BM25,
yoğun, hibrit, yeniden sıralayıcı). Sorgu işleme ilaç karışmasını çözdü:
teklistamab sorulduğunda elranatamab gelmesi bu aşamada düzeldi.
*(`_logs/retrieval_eval_78soru_gpusuz_qp.json`, `retrieval_eval_rerank_*.json`)*

**Level 3 — cevap.** 78 pozitif, A/B dönüşümlü bölünmüş. Eşikler A'dan, rakam
B'den. **B yarısı: 33/39 cevaplandı, 22 hedefi tuttu, 6 haksız red, ortalama
kanıt oranı 0,94, ortalama cevap 492 karakter, soru başına 26,7 sn.**
*(`_logs/level3_yeniden.json` ve `_logs/bakeoff/olcum_Qwen2_5-7B-Instruct.json`)*

**Level 4 — atıf.** Atıf onarımı öncesi/sonrası, golden hedefe göre:
**tüm küme 52 → 57 / 78, B yarısı 28 → 31 / 39.** Kaybedilen soru yok.
Onarım B yarısında 66 cümleye atıf ekledi, 3'ünü düzeltti, 4'ünü dayanaksız
bıraktı.

**Ölçüm fazı koşusu bir tekrar üretimdir, ikinci bir kanıt değildir.** 39
cevabın 39'u önceki koşuyla birebir aynı çıktı — aynı model, aynı sorular,
açgözlü kod çözme. Kanıtladığı şey başka: Level 3 rakamları eski kod yolundan
üretilmiş cevapların sonradan puanlanmasıyla çıkmıştı; bu koşu dondurulmuş
üretim yolundan uçtan uca geçti (anlamsal dayanaklılık, düzeltilmiş cümle
bölücü, `cevapla()` içine bağlı alan kapısı). Aynı rakamların çıkması
refaktörlerin davranışı bozmadığını gösteriyor.

**Süre rakamları donanıma bağlıdır.** Aynı model eleme fazında 11,1 sn/soru,
ölçüm fazında 26,7 sn/soru verdi; fark GPU'dan. Teslim planlamasında bu sayı
hedef donanıma göre yeniden ölçülmeli.

**Reddetme — taze negatif küme.** 15 arşiv dışı soru (miyelom dışı hematoloji),
eşikler dondurulmuş: **13 reddedildi, 2 cevaplandı, 0 uydurma.** Cevaplanan
ikisi (del(5q) MDS'de lenalidomid, MCL'de bortezomib) geçersiz negatif çıktı —
konu gerçekten arşivde. *(`_logs/negatif_taze.json`,
`_logs/negatif_uctan_uca.json`)*

**En önemli tek bulgu:** benzerlik skoru kapısı 15 arşiv dışı sorunun
**hiçbirini** durduramadı; skorlar 0,53-0,72, geçerli soruların 0,63-0,72
aralığıyla tamamen iç içe. Reddetmeyi sağlayan şey skor değil, metadata'ya
dayanan alan kapısı.

**Dil modeli karşılaştırması.** A yarısı, 39 pozitif + 8 negatif:

| model | cevap | hedef | atıf | uydurma | red | kanıt | sn |
|---|---|---|---|---|---|---|---|
| Meta-Llama-3.1-8B | 32/39 | 22 | 27 | 1/8 | 7 | 1,00 | 15,4 |
| Qwen2.5-14B | 32/39 | 22 | 25 | 1/8 | 7 | 0,93 | 18,5 |
| **Qwen2.5-7B** | 31/39 | 21 | 25 | 0/8 | 8 | 0,93 | **11,1** |
| Turkish-Llama-8b | 32/39 | 22 | 26 | 1/8 | 7 | 0,97 | 34,8 |
| Qwen3.6-27B | 26/39 | 21 | 23 | 0/8 | 13 | 0,68 | 38,3 |

*(`_logs/bakeoff/eleme_*.json`)*

---

## 3. Kirlenmiş ve geçersiz rakamlar — kullanılmamalı

Bunlar dosyalarda duruyor ama rapora girmemeli.

**`level3_yeniden.json` özetindeki "uydurma 0/7".** Kirlenmiş. O rakamı
düzelten sözlük hatası (çıplak "steroid" deseninin deksametazona eşleşmesi)
ölçüm yarısındaki N14 sorusu görülerek düzeltildi. Uydurma için geçerli rakam
taze kümeden: **0/15**.

**İlk Level 3 koşusunun dayanaklılık rakamları** (`level3_eval*.json`, eşik
`dayanaklilik 0,65`). Ölçüt leksikti; iki dilli arşivde doğru cevaplarda bile
ortak sözcük çıkmıyordu, medyan hem doğru hem uydurma cevaplarda 0,00 idi.
Ölçüt anlamsala çevrildi, eski eşik yeniyle kıyaslanamaz.

**İlk atıf teşhisi: "78 cevabın 30'unda hiç atıf yok".** Yanlış, doğrusu 2/78.
Model atıfı noktadan sonra yazıyordu, cümle bölücü `[K3]`'ü ayırıp eliyordu.
Düzeltildi.

**İlk Qwen3.6-27B koşusu** (hedef 25, atıf 31). Geçersiz: model düşünme
sürecini düz metin olarak cevaba yazdı, 39 cevabın 39'unda. Yüksek rakamlar
yetenek değil, uzun cevabın her şeye değmesiydi. Düzeltilmiş koşuda 21'e düştü.

**Bakeoff tablosundaki "atıf onarım öncesi→sonrası" sütunu** (27→27 gibi).
Ölçülemedi: onarım `cevapla()` içine bağlıydı, kaydedilen cevap zaten
onarılmıştı. `ham_kos` artık ham çıktı saklıyor; sonraki koşularda ölçülebilir.

---

## 4. Dosya envanteri

**Güncel ve kanonik:**

- `_logs/level3_yeniden.json` — Level 3+4, düzeltilmiş bölücü, 136 atıf
  eklemesi, 52→57
- `_logs/negatif_taze.json` — taze negatif, kapı ölçümü (11 durduruldu)
- `_logs/negatif_uctan_uca.json` — taze negatif, uçtan uca (13 red, 0 uydurma)
- `_logs/bakeoff/eleme_*.json` — beş modelin sonucu (27B düzeltilmiş sürüm)
- `_work/eval/golden_queries.json` — 78 soru (eski 20'lik küme `_v1` olarak)
- `_work/eval/negative_queries.json` — ilk 15 negatif (kirlenmiş, N14)
- `_work/eval/negative_queries_v2.json` — taze 15 negatif (N25/N26 geçersiz
  işaretli)

**Aşılmış, referans için duruyor:**

- `_logs/level3_eval*.json` — leksik ölçütlü ilk koşular
- `_logs/cevap_demo*.json` — dört soruluk erken demolar
- `_logs/level3_yeniden (2).json` — kanonik dosyanın kopyası

---

## 5. Bilinen eksikler

**Klinik doğrulama yok.** Sorular kılavuz metinlerine dayanılarak hazırlandı,
bir hematolog gözden geçirmedi. Ölçülen şey kaynağa dayanma ve atıf isabeti;
klinik doğruluk değil. Bu ayrım her raporda açıkça durmalı.

**Kapsam sınırı.** Arşiv tam KÜB/PI belgelerinden oluşuyor, bu belgeler ilacın
bütün endikasyonlarını taşıyor. Sistem "miyelom arşivi" değil, "miyelom
ilaçlarının tam ürün bilgisi arşivi".

**Geri ödeme tabloları sistemde değil** — EK-4A 8.334 satır, TİTCK ruhsat
listesi 22.965 satır yapılandırılmış veri olarak eklenmedi.

**Dört zoledronik asit KÜB'ü taranmış görüntü**, metin katmanı yok, OCR gerekli.

**SUT chunk başlıkları kayık:** "fff) Daratumumab" başlığı altında lenalidomid
koşulları görülebiliyor.

**Karfilzomib dozu 5.1 Farmakodinamik'ten geliyor**, 4.2 Pozoloji'den değil.

---

## 6. Yeniden üretim

Ölçümlerin hepsi Colab'da, `_work/colab/` altındaki defterlerle tekrarlanabilir:

- `cevap_demo.ipynb` — Level 3 koşusu ve taze negatif ölçümü
- `llm_bakeoff.ipynb` — dil modeli karşılaştırması (9. hücre tek model yeniden
  koşturur)
- `_scripts/colab_paketle.py` — yüklenecek dosyaları `myeloma\1` altında toplar

Qdrant gömülü modda depo klasörünü tek sürece kilitliyor: defterde açık istemci
varken alt süreç çalıştırılamaz, ilgili fonksiyonlar `istemci` parametresi alır.
