# Miyelom-RAG

Multipl miyelom tedavisine dair Türkçe soruları klinik kılavuz, ruhsat ve geri ödeme belgelerine dayanarak cevaplayan, her cümlesini kaynağına bağlayan bir RAG sistemi.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![Qdrant](https://img.shields.io/badge/Qdrant-gömülü_mod-DC244C)
![Model](https://img.shields.io/badge/LLM-Qwen2.5--7B-7B61FF)

> **163 belge · 14.532 parça · 3 katman · 78 altın soru · arşiv dışı 15 soruda 0 uydurma**

---

## Problem

Bir hematolog bir tedavi rejimi düşündüğünde art arda üç soru sorar. Kanıt bu rejimi destekliyor mu? Bu ilaç Türkiye'de ruhsatlı mı? SGK bunun bedelini ödüyor mu?

Üç sorunun cevabı üç ayrı belge kümesinde duruyor. Kanıt NCCN, ESMO, ASCO ve NCI PDQ kılavuzlarında, ruhsat bilgisi TİTCK Kısa Ürün Bilgilerinde ve FDA ile EMA etiketlerinde, geri ödeme kuralları da SUT ile eklerinde. İkisi İngilizce, biri Türkçe ve hiçbiri diğerine atıf yapmıyor. Miyelom-RAG bu üç katmanı tek bir arşivde birleştiriyor ve soruyu Türkçe sorup cevabı künyeli kaynaklarıyla almayı mümkün kılıyor.

## Arşiv

Arşive yalnızca birincil ve resmî kaynaklar girdi. Üçüncü taraf prospektüs siteleri bilerek kullanılmadı, çünkü bir doz bilgisinin izlenebilir olması kolay bulunmasından daha önemliydi.

| Katman | İçerik |
|---|---|
| **1. Klinik kanıt** | NCCN, EHA-ESMO, ASCO, NCI PDQ kılavuzları ve beş meta-analiz |
| **2. Ruhsat** | 18 FDA etiketi, 17 EMA EPAR, 108 Türkçe TİTCK KÜB |
| **3. Geri ödeme** | SGK Sağlık Uygulama Tebliği ve EK-4 listeleri |

Alınamayan belgeler de kayıt altında. ASCO kılavuzu bot engeline takıldığı için elle indirildi, tam NCCN PDF'i üyelik duvarının arkasında kaldı, dört KÜB de taranmış görüntü olduğu için OCR bekliyor. Belgelerin tam listesi, sürümleri ve kaynak adresleri [`00_INDEX.md`](00_INDEX.md) ile [`DATA_CATALOG.csv`](DATA_CATALOG.csv) dosyalarında.

## Mimari

```
soru
 │
 ├─ sorgu işleme     ilaç, rejim ve sınıf tanıma · marka → etken madde
 ├─ gömme            BGE-M3 · 1024 boyut · çok dilli
 ├─ arama            Qdrant · 30 aday (+ ilaç tanındıysa filtreli ikinci arama)
 │
 ├─ KAPI 1           arama skoru < 0,50 ise cevap yok, model çağrılmaz
 ├─ KAPI 2           alan kapısı · kapsam dışıysa model çağrılmaz
 ├─ bağlam           4 parça, özetleme yok
 │
 ├─ üretim           Qwen2.5-7B · sıcaklık 0 · katı istem
 ├─ atıf onarımı     atıfsız cümleye anlamsal eşleşmeyle kaynak atanır
 ├─ KAPI 3           dayanaklılık < 0,20 ise cevap gizlenir
 │
 └─ yanıt            cevap + künyeli kaynaklar + güven + uyarılar
```

Kullanıcıya sayısal bir güven puanı gösterilmiyor, yüksek, orta ve düşük diye üç kategori gösteriliyor. Kalibrasyon verisi olmadan "yüzde 87 doğru" demek doğrulanamayan bir kesinlik üretmek olurdu.

## En önemli bulgu

> **Arşiv dışı 15 sorunun 15'i de benzerlik skoru kapısını geçti.**
>
> Arşiv dışı soruların skorları 0,53 ile 0,72 arasında çıktı, geçerli soruların skorları 0,63 ile 0,72 arasında. İki bant tamamen iç içe olduğu için eşiği yükseltmek hiçbir şeyi çözmüyor.

Gömme modeli bir sorunun tıbbi metne ne kadar benzediğini ölçüyor ve sorunun bu arşivin konusu olup olmadığını ayırt edemiyor. Sorular da bilerek zor seçildi. Akut lösemi, ITP, Hodgkin lenfoma, hemofili ve talasemi, miyelom arşiviyle aynı kelime dünyasını paylaşıyor.

Reddetmeyi sağlayan şey parçaların metadata yapısına dayanan **alan kapısı** oldu. Bölümleme aşamasında her parçaya etiket yazmak için harcanan emek, sonunda sistemin güvenlik özelliğine dönüştü. Alan kapısı devredeyken arşiv dışı bir soru dil modeline hiç ulaşmadan yaklaşık bir saniyede reddediliyor.

## Ölçümü dürüst tutmak

Eşikler ilk başta dört demo cevabına bakılarak seçilmişti. Bu, sınav kâğıdını gördükten sonra geçme notunu belirlemeye benziyordu.

Bunun üzerine 78 soru A ve B diye iki yarıya bölündü. **Eşikler yalnızca A yarısına bakılarak seçildi ve donduruldu. Raporlanan her rakam, eşiklerin hiç görmediği B yarısından geliyor.** Aynı ayrım dil modeli seçiminde de uygulandı.

Kurgu ilk denemede haklı çıktı. Eşik, seçildiği yarıda sıfır uydurma verirken görmediği yarıda bir uydurmayı geçirdi. Bütün kümeye bakılsaydı "sistem hiç uydurmuyor" diye yanlış bir cümle kurulacaktı.

## Sonuçlar

**B yarısı, eşiklerin görmediği 39 soru:**

| Ölçü | Sonuç |
|---|---|
| Cevaplanan | 33 / 39 |
| Doğru kaynağa dayanan | 22 / 39 |
| Atıf isabeti (onarım öncesi → sonrası) | 28 → 31 |
| Cümlelerin kaynağa dayanma oranı | %94 |
| Haksız reddetme | 6 |

**Taze arşiv dışı küme:** 15 soruda 13 red ve **0 uydurma**. Cevaplanan iki soru (del(5q) MDS'de lenalidomid, mantle hücreli lenfomada bortezomib) doğru çıktı, çünkü konuları gerçekten arşivde. Tam ürün bilgisi belgeleri bir ilacın bütün endikasyonlarını taşıyor. Soru yanlış etiketlenmişti ve sistem doğru davrandı.

**Arama yöntemleri, 78 soru:**

| Yöntem | recall@5 | recall@10 | MRR |
|---|---|---|---|
| BM25 | 0,59 | 0,68 | 0,512 |
| **Dense (BGE-M3)** | **0,82** | **0,87** | **0,714** |
| Hibrit (RRF) | 0,77 | 0,85 | 0,615 |

**Beş dil modeli, aynı koşullar (A yarısı):**

| Model | Cevaplanan | Hedef | Haksız red | Süre |
|---|---|---|---|---|
| Meta-Llama-3.1-8B | 32/39 | 22 | 7 | 15,4 sn |
| Qwen2.5-14B | 32/39 | 22 | 7 | 18,5 sn |
| **Qwen2.5-7B (seçilen)** | 31/39 | 21 | 8 | **11,1 sn** |
| Turkish-Llama-8B | 32/39 | 22 | 7 | 34,8 sn |
| Qwen3.6-27B | 26/39 | 21 | 13 | 38,3 sn |

Beş modelin hepsi aynı bantta kaldı ve 39 soruda bir soruluk fark gürültü sayılır. Seçim bu yüzden hız ve donanım gereksinimine göre yapıldı. En büyük modelin en çok haksız reddi yapması da ilginç bir sonuç. Model kaynağı kendi cümleleriyle yeniden yazıyor, anlamsal bağ zayıflıyor ve dayanaklılık kapısı cevabı kapatıyor.

## Yol boyunca yakalanan hatalar

Projenin en öğretici kısmı ölçümün kendisini sorgulamak oldu.

**Sessizce kaybolan kontrendikasyon.** Doğrulayıcı, SARCLISA belgesinde bir kontrendikasyon cümlesinin silindiğini yakaladı. Boş gövdeli bölümler atlanırken başlığın içindeki içerik de kayboluyordu. Sistem hata vermiyor, yalnızca eksik bilgiyle cevap üretiyordu.

**Sahte alarm.** Doğrulayıcı 909 "bölünmüş tablo" raporladı. Hata ölçütteydi, çünkü uzak tablo tekrarlarını bölünme sayıyordu. Ölçüt düzeltilince sayı 23'e indi. Düşük skor görünce önce ölçütü sorgulamak, projede iki kez daha işe yarayan bir ders oldu.

**En tehlikeli hata.** "Teklistamab için basamaklı doz şeması nedir?" sorusuna sistem elranatamab bilgisi getiriyordu. İki ilaç da BCMA hedefli bispesifik antikor, ikisi de basamaklı doz kullanıyor ve doz değerleri farklı. Soru Türkçe, belge İngilizce olduğu için "basamaklı doz şeması" ifadesi "step-up dosing" başlıklı bölüme Türkçe yazılmış başka belgelerden daha uzak düşüyordu. Çözüm, marka adını etken maddeye çeviren, İngilizce INN ve ATC koduyla genişleten ve ilaç tanındığında yalnızca o etken madde içinde ikinci bir arama yapan sorgu işleme katmanı oldu.

**Ölçüt krizi.** İlk sonuçlar sistemi aşırı ihtiyatlı gösteriyordu. Dayanaklılık ölçütü cevap ile kaynağın ortak kelimelerine bakıyordu ve iki dilli bir arşivde ortak kelime çıkmıyordu. Kaynakta "administer 27 mg/m² on days 1, 2, 8, 9" yazarken cevap "27 mg/m² dozunda 1, 2, 8 ve 9. günlerde uygulanır" diyordu. Ölçülen dayanaklılığın medyanı hem doğru hem uydurma cevaplarda 0,00 çıktı. Ölçüt anlamsal benzerliğe çevrildiğinde tablo tersine döndü ve sistemin aslında aşırı cömert olduğu görüldü.

## Tasarım kararları

**PDF ayrıştırıcıları yarıştırıldı.** LlamaParse, Docling ve Unstructured aynı belgede karşılaştırıldı. En çok metni Unstructured çıkardı ama sıfır tablo satırı üretti ve dört kat uzun sürdü. Docling akış şemalarını atladı. Arşiv sonunda tek bir araca bağlı kalmadan ayrıştırıldı. Bazı belgeler LlamaParse ile işlendi, geri kalanında sayfa başına metin yoğunluğuna göre `pymupdf4llm` ya da Docling'in yerleşim modeli kullanıldı. Kötü çıkarılmış bir tablo sistemi sessizce zehirler, bu yüzden sistemin tavanı bu aşamada belirleniyor.

**Bölümleme yapıyı takip ediyor.** Parça sınırı sabit uzunluk yerine başlık. Tavan 800 token, tablolar hiç bölünmüyor, dipnot gövdesine bağlı kalıyor ve örtüşme yalnızca düz metinde uygulanıyor. NCCN akış şemaları bilerek IF/THEN kurallarına çevrilmedi. Uydurma bir karar kuralı üretmek eksik kural bırakmaktan daha tehlikeli.

**Yeniden sıralayıcı ölçüldü ve kullanılmıyor.** `bge-reranker-v2-m3` sıralamayı gerçekten iyileştiriyor (20 soruda recall@5 0,75'ten 0,85'e) ama GPU gerektiriyor. Yerel işlemcide yalnızca yüklenmesi 574 saniye sürüyor. Donanım gereksinimini ikiye katlamak ölçülen kazanca değmedi. GPU'lu bir sunucuda açılabilir.

**Doğrulayıcı "bakacak bir şey bulamadım" ile "baktım, temiz" ayrımını yapıyor.** Kapsamı olmayan bir kontrol sessizce "temiz" raporu vermiyor.

## Klasör yapısı

| Yol | İçerik |
|---|---|
| `_scripts/` | Boru hattı. Ayrıştırma, onarım, zenginleştirme, bölümleme, gömme, indeksleme, cevap katmanı ve değerlendirme |
| `_scripts/pipeline.py` | Cevap katmanının tek giriş noktası. Demo, değerlendirme ve web servisi aynı fonksiyonu çağırıyor |
| `_web/backend/` | FastAPI servisi |
| `_web/frontend/` | React (Vite) arayüzü |
| `_work/eval/` | 78 altın soru ve arşiv dışı soru kümeleri |
| `_work/colab/` | Ölçümleri GPU'da tekrarlayan Colab defterleri |
| `_logs/KARAR_KAYDI.md` | **Bugün geçerli olan kararlar ve rakamlar**, geçersiz sayılan rakamların listesiyle birlikte |
| `_logs/DURUM.md` | Kronolojik proje günlüğü. Hangi hatanın nasıl bulunduğu burada yazılı |
| `_logs/*.json` | Ölçümlerin ham çıktıları |
| `docs/sunum.pptx` | Proje sunumu |

Aynı fonksiyonun her yerden çağrılması bilinçli bir tercih. İki ayrı yol yazılsaydı ölçülen sistemle gösterilen sistem birbirinden ayrışırdı ve bu fark hiç fark edilmezdi.

## Kurulum

Depoda kaynak PDF'ler ve onlardan türetilen veri (ayrıştırılmış metin, parçalar, gömme matrisi, Qdrant deposu) bulunmuyor. Klinik kılavuzların bir kısmı yayınevi telifi taşıyor ve türetilmiş veri yaklaşık 300 MB tutuyor. Modeller de depoda yok. BGE-M3 ilk çalıştırmada Hugging Face'ten, Qwen2.5-7B Ollama üzerinden iniyor.

**1. Belgeleri indir.** `DATA_CATALOG.csv` içindeki her belgeyi, `yol` sütununda yazan konuma yerleştir.

**2. Boru hattını çalıştır.**

```bash
python _scripts/batch_docling.py      # PDF → markdown (pymupdf4llm + Docling)
python _scripts/run_bakeoff.py        # ayrıştırıcı karşılaştırması (LlamaParse için .env'de LLAMA_CLOUD_API_KEY gerekir)
python _scripts/repair_parsed.py      # bozuk dönüşümleri onar
python _scripts/enrich_sections.py    # bölüm omurgasını kur
python _scripts/chunk.py              # yapı farkında bölümleme
python _scripts/embed_chunks.py       # BGE-M3 gömme (GPU önerilir, CPU'da ~8 saat)
python _scripts/qdrant_index.py       # Qdrant deposunu kur
```

**3. Servisi ve arayüzü başlat.**

```bash
pip install -r _web/backend/requirements.txt
cp _web/backend/.env.ornek _web/backend/.env
ollama pull qwen2.5:7b

cd _web/backend && uvicorn app:uygulama --host 127.0.0.1 --port 8000 --workers 1
cd _web/frontend && npm install && npm run dev
```

`--workers 1` zorunlu, çünkü Qdrant gömülü modda depo klasörünü tek bir sürece kilitliyor. Ayrıntılı kurulum ve sorun giderme için [`_web/KURULUM.md`](_web/KURULUM.md) dosyasına bakabilirsin.

Arayüz sistemin iç durumunu saklamıyor. Bir atfa tıklandığında kaynağın tam metni açılıyor, bağlama girip kullanılmayan kaynaklar da listeleniyor ve bir soru reddedildiğinde hangi kapının kapattığı yazıyor.

## Bilinen eksikler

- **Klinik doğrulama yapılmadı.** Ölçülen şey kaynağa dayanma ve atıf isabeti. Cevapları bir hematolog gözden geçirmedi.
- Şapkasız Türkçe yazım alan kapısını aşabiliyor.
- Geri ödeme tabloları (EK-4A'da 8.334, TİTCK ruhsat listesinde 22.965 satır) yapılandırılmış veri olarak eklenmedi.
- Kimlik doğrulama katmanı yok. Sistem dışarıya açılacaksa önüne bir kimlik doğrulama katmanı konmalı.
- Dört belge taranmış görüntü olduğu için OCR bekliyor.

## Yol haritası

Yakın vadede en önemli iş hematolog doğrulaması. Bu yapılmadan sistem doğrulanmış sayılmamalı. Orta vadede geri ödeme tabloları kesin sorgu dalı olarak eklenecek, taranmış belgeler OCR'dan geçecek ve kimlik doğrulama gelecek. Uzun vadede GPU'lu sunucuda yeniden sıralayıcı açılabilir, akış şemaları uzman gözetiminde kurallara çevrilebilir ve kaynak güncellemeleri otomatik izlenebilir.

---

Bu proje staj sürecinde geliştirildi. Ortaya çıkan şey, ne kadar çalıştığı ölçülmüş bir sistem. Her rakamın hangi kümede, hangi eşiklerle ve hangi varsayımlarla alındığı yazılı, geçersiz sayılan rakamlar da ayrıca listelenmiş durumda. Klinik bir karar-destek sisteminde bu izlenebilirlik doğruluk iddiasının kendisinden önce gelir.

> ⚠️ Miyelom-RAG bir araştırma ve karar-destek prototipidir. Klinik kararın yerine geçmez.
