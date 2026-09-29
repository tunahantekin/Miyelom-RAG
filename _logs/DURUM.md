# Durum ve Devir Notu — Multipl Miyelom Karar-Destek Arşivi
Son güncelleme: 2026-08-05

Bu dosya, oturum sıkıştırıldığında kaybolacak kararları ve açık işleri tutar.
Kronolojik olay kaydı için `_logs/PROJECT_LOG.md`, belge envanteri için `00_INDEX.md`.

---

## Sistem kapsamı (karar verildi)

Birinci sürüm **Türkiye odaklı**: hedef, "bugün Türkiye'de yazılabilir ve
uygulanabilir" karar desteği. Global bilgi (FDA etiketi, NCCN kategorisi) silinmez
ama **bağlamsal destek** olarak sunulur, birincil öneri olarak değil.

Pratik sonucu: Türkiye'de ruhsatı olmayan etken maddeler (elotuzumab, teklistamab,
talkuetamab, belantamab, idekabtajen, siltakabtajen, pleriksafor) yanıtlarda
"Türkiye'de ruhsatsız — ithal/endikasyon dışı yolu gerekir" etiketiyle görünmeli.
Bu ayrımı taşıyacak alan, ruhsat durumu; kaynağı TİTCK ruhsat listesi (22.965 satır).

## Doğrulama mimarisi (karar verildi)

İki katman, birbirine karıştırılmamalı:

- **Structural Validation** — ground truth gerektirmez, deterministik, tüm arşive
  ölçeklenir. `_scripts/structural_validation.py`. Üç şiddet: `ERROR` (kesin hata),
  `WARN` (büyük ihtimalle hata), `REVIEW` (deterministik tespit, olasılıksal yorum).
  Kaynak güncellendiğinde regresyon testi olarak tekrar koşar.
- **Semantic Validation** — ground truth ve insan hakemi ister, ölçeklenmez.
  `_scripts/clinical_recall.py` + `_work/parse_bakeoff/truth/myel1_truth.json`.

**Çözülen tasarım sorunu:** validator artık "bakacak bir şey bulamadım" ile
"baktım, temiz" arasını ayırıyor. Her rapora `kapsam` alanı eklendi; arşiv
özetinde her kontrol için kaç belgede malzeme bulunduğu yazıyor. Dipnot ve
iç-bağ kontrolleri dönüştürülmüş belgelerde hâlâ 0/159 malzeme buluyor — bu
artık sessizce "temiz" diye raporlanmıyor, açıkça "kapsam dışı" deniyor.

## Boru hattı (üç aşama)

```
layer*/**.pdf  ──batch_docling.py──▶  _work/parsed/    (ham dönüşüm)
                                          │
                                enrich_sections.py
                                          ▼
                                    _work/enriched/    (bölüm omurgası — kanonik aşama)
                                          │
                              structural_validation.py
                                          ▼
                              _logs/structural_validation.json
```

Parser yolu metin yoğunluğuna göre seçilir: sayfa başına ≥200 karakter →
`pymupdf4llm`, altı → Docling layout modeli. Her belge ayrı alt süreçte çevrilir.
LlamaParse birincil sayılmıştı ama gerçek kılavuzda MYEL-1'in karar dalı sütununu
düşürdü ve dipnot harflerini kaydırdı; toptan yeniden parse gerekçesi yok.

## Zenginleştirme (bitti)

`_scripts/enrich_sections.py`: SmPC/PI bölüm numaralarını markdown başlığına
çevirir (`## 4`, `### 4.2`). Kanonik sözlük tabanlı — numara tek başına yetmez,
başlığın kanonik bölüm adıyla eşleşmesi şart. Bu sayede "1. Flakonu buzdolabından
çıkarın" gibi talimat listeleri başlık olmuyor.

Sonuç: 3.746 başlık terfi ettirildi (108 KÜB, 18 FDA PI, 17 EMA). Yol boyunca iki
gerçek parser kusuru bulundu ve tarayıcı ikisini de kapsayacak şekilde yazıldı:
iki başlığın tek satıra yapışması (`## 4 KLİNİK ÖZELLİKLER 4.1 Terapötik...`) ve
başlığın sayfa altbilgisine gömülmesi (`> **Belge Doğrulama Kodu: ... 6. FARMASÖTİK**`).

Asıl kazanç: kanonik küme bilindiği için **eksik bölüm** tespit edilebiliyor.
"4.2 Pozoloji yok" bulgusu hacim oranından çok daha keskin — belge açılır,
uzunluğu makul görünür, ama doz bölümü kayıptır.

## Arşiv durumu

- 159 PDF → `_work/parsed/` → `_work/enriched/` (159 belge; şeması olmayan 16'sı
  olduğu gibi kopyalanır ki doğrulama arşivin tamamını görsün).
- Hacim kaybı 0. Bulgusuz belge 131/160.
- Açık `ERROR`: 18 belgede eksik zorunlu bölüm (Document Quality Backlog).
- 4 Excel (EK-4A 8.334 satır, EK-4B, EK-4H 281 satır, TİTCK ruhsat listesi
  22.965 satır) henüz işlenmedi — bunlar RAG'e değil SQLite'a girmeli.

## `layer1_clinical/nccn/nccn_myeloma_manual.md`

Harici kaynaktan gelen, elle hazırlanmış NCCN transkripsiyonu (43 bölüm, 18 MYEL kodu).
Doğrulanan: MYEL-1 → 43/43 clinical recall. MYEL-F/G → 57 rejim çapraz doğrulandı,
**uydurma rejim yok**. MYEL-G 5of5 → PDF ile birebir.

Düzeltilenler:
- MYEL-G 4of5 sütun karışması (3 rejim eklendi, sayfaya ait olmayan 5 satır çıkarıldı).
- MYEL-G 2of5 dipnot **yanlış harfle** tanımlıydı: PDF'te `k` olan metin `h` olarak
  duruyordu (sayfada f/g/h dipnotu yok). Harf düzeltildi, tanımsız `j` eklendi.
- MYEL-I'nin dipnot bloğu hiç yoktu; `a b c d` kaynaktan eklendi.
- MYEL-E `[^l]` tanımında iki nokta eksikti.

**Kritik dipnot kalmadı.** MYEL-E'de "7 eksik işaret" sanılan durum validator
kusuruymuş: tanımların tamamı "3 of 3" sayfasında, işaretler önceki sayfalarda
kullanılıyor. Validator artık çok sayfalı MYEL kodlarını kardeş sayfa olarak
görüyor (çift tanım kontrolü sayfa bazında kalıyor, eksik kontrolü kardeşlere bakıyor).

### Document Quality Backlog — klinik risk taşımayan kusurlar

| Yer | Kusur |
|---|---|
| MYEL-1 | `h` `i` tanımı var, iki nokta eksik (biçimsel) |
| MYEL-2 | `i` tanımsız |
| MYEL-3 | `b` tanımsız |
| MYEL-B (1 of 2) | `1` `2` `3` literatür atfı, tanımsız |
| MYEL-J (1 of 2) | `a` tanımsız |
| MGNS-1 | `a` tanımsız |
| İçindekiler | `SP-1` ve `MGCS-1` bağı var, bölümü yazılmamış |
| 18 KÜB/etiket | eksik zorunlu SmPC bölümü — `_logs/enrich_report.json` |

Eksik bölümü en ağır olanlar: ALKERAN 2 mg (5'ten sonrası yok), REVLIMID 25/5 mg
(metin ikileniyor, 278k karakter), ERIOLAN, OSTEOZOLEN, CAFİZO, PLAZOL, ZOLTASTA,
ACLABON. Çoğu taranmış zoledronik asit KÜB'ü; kaynak PDF'in yeniden indirilmesi
gerekebilir.

---

## BİLİNEN SINIRLAMA — `section_number` metadata kalitesi

**Karar: bu iterasyonda düzeltilmeyecek, kayıt altına alınıp geçilecek.**

Chunker her `##`/`###` başlığını bölüm sayıyor. Ama parser (pymupdf4llm) kalın
yazılmış herhangi bir metni de başlığa çeviriyor, dolayısıyla `section_number`
alanına `**<u>Klinik</u>**`, `_Yeni`, `None` gibi değerler düşüyor. Kanonik
kümeye göre ölçüm (`_scripts/metadata_validation.py`):

| Kaynak | Geçerli `section_number` |
|---|---|
| TITCK_KUB | %82,6 |
| EMA_SMPC | %78,5 |
| FDA_SMPC | %22,5 |
| NCCN | %13,9 |
| SUT | %11,1 |

Bu bir chunker hatası değil, parser çıktısının sınırı: kalın metin ile başlık
arasındaki ayrım kaynakta zaten kaybolmuş durumda. Düzeltmek ya kanonik olmayan
başlıkları bölüm saymamayı (bilgi kaybı riski) ya da her belge sınıfı için ayrı
başlık sezgisi yazmayı gerektirir.

**Sonuçları:** bölüm bazlı filtreleme yalnızca KÜB ve EMA'da güvenilir; alıntı
gösteriminde `section_number` tek başına kullanılmamalı, `document_label` +
`page_number` ile birlikte verilmeli. Retrieval değerlendirmesinde hedefler
bölüm numarasına dayandığı için düşük skorların bir kısmı bu sınırlamadan
kaynaklanabilir — yorumlarken hesaba katılmalı.

## Metadata durumu (2026-08-05)

`_scripts/metadata_validation.py` yazıldı; chunk metadata'sını denetliyor,
hiçbir dosyayı değiştirmiyor. Rapor `_logs/metadata_validation.json`.

- `layer` / `source`: temiz, sıfır uyumsuzluk.
- `version`: otomatik dolduruldu (NCCN sürüm satırı, FDA "Revised", KÜB ruhsat
  tarihi, SUT Resmî Gazete tarihi). 160 belgenin 121'inde bulundu, 39'unda yok.
- `document_name`: benzersiz hale getirildi (katman öneki atılıp gerisi
  korunuyor). Önceden 160 belge 150 kimliğe düşüyordu. Kısa ad için ayrı
  `document_label` alanı eklendi.
- `page_number`: 14.095 chunk'ta yok — mevcut tasarım kapsamında kabul edildi.
- `atc_codes`: 1.739 chunk kendi etken maddesi dışında kod taşıyor (kombinasyon
  rejimleri) — mevcut tasarım kapsamında kabul edildi.

## Chunking (bitti)

`_scripts/chunk.py` → `_work/chunks/chunks.json`, **14.532 chunk / 160 belge**.
Kurallar: sınır = başlık; >800 token bölümler paragraf sınırından alt bölünür
(cümle ortasından asla); tablolar atomik ve bağlam satırı eklenir; dipnot asla
tek başına chunk olmaz, atıf yapan chunk'ın sonuna `### ASSOCIATED FOOTNOTES:`
altında eklenir; örtüşme sadece ardışık metin parçaları arasında ~40 token,
tabloda yasak; 120 token altı ardışık metin chunk'ları birleştirilir.

Akış şemaları IF/THEN kuralına **çevrilmedi** — anlam çıkarımı gerektiriyor,
uydurma karar kuralı üretmek eksik kural bırakmaktan tehlikeli. Dal kalıbı
taşıyan 43 chunk `REQUIRES_FLOWCHART_REVIEW` ile işaretli.

## Doğrulama katmanları (üçü de yazıldı)

| Script | Ne ölçer | Son durum |
|---|---|---|
| `structural_validation.py` | belge bütünlüğü | 131/160 bulgusuz |
| `chunk_validation.py` | chunk ↔ kaynak bütünlüğü | kapsam ≥0.97, sahipsiz parent 0, tablo bölünmesi 23 |
| `metadata_validation.py` | metadata doğruluğu | layer/source temiz, version 121/160 |

Bulunan **gerçek** hatalar: SARCLISA'da kontrendikasyon cümlesinin sessizce
silinmesi (boş gövdeli bölüm atlanınca başlıktaki içerik kayboluyordu), 1.370
sahipsiz `parent_id`, MYEL-G 2of5'te yanlış harfle tanımlı dipnot,
REVLIMID/ERIOLAN'da bozuk dönüşüm.

Bulunan **sahte** bulgular (ölçüm kusuru, düzeltildi): 909 "bölünmüş tablo"
(uzak tekrarları bölünme sayıyordu), 132 "kayıp dipnot satırı" (liste işareti
farkı), 7 "eksik MYEL-E dipnotu" (kardeş sayfa görülmüyordu).
**Ders: düşük skor gördüğünde önce ölçütü sorgula.**

## Embedding ve retrieval (Level 2 — ilk benchmark alındı)

Model **BAAI/bge-m3** (çok dilli zorunlu: sorular Türkçe, NCCN İngilizce).
Gömme girdisi = `document_label / section_number / section_title` + içerik;
`normalize_embeddings=True`; `max_seq_length=1024`.

- Yerel CPU: 0,6 chunk/sn → tam arşiv ~8 saat. Colab T4: 2.240 sn (37 dk).
- `_work/embeddings/BAAI_bge-m3.npy` = 14.532 × 1024, `chunks.json` ile hizalı.
- Alt küme ölçümünün dosyaları `_work/embeddings/altkume/` altında saklandı.
- Colab notebook'u: `_work/colab/embed_bge_m3.ipynb` (yeniden koşturulabilir).

**Tam arşivde 20 golden query sonucu (reranker YOK):**

| mod | recall@5 | recall@10 | MRR | kaçan |
|---|---|---|---|---|
| BM25 | 0.60 | 0.70 | 0.469 | 6 |
| dense (BGE-M3) | **0.85** | 0.85 | **0.660** | 3 |
| hibrit (RRF) | 0.70 | **0.90** | 0.569 | **2** |

**Yorum:** hibrit ağı genişletiyor, dense daha iyi sıralıyor. İkisi rakip değil;
hibrit ile geniş aday havuzu + reranker ile sıralama doğru kurgu.

**Golden set uyarısı:** hedefler artık "şu dosya" değil "şu bilgi" — chunk
metninde beklenen klinik işaretlerin hepsi geçiyorsa doğru sayılıyor
(`chunk_uyar`). Bu ölçüt eskisinden müsamahakâr; konuyu sadece anan bir chunk
doğru sayılabiliyor. Gerçek performans bu rakamların biraz altında.

## Pipeline'a göre neredeyiz

Referans şema: `C:\Users\Tunahan\Desktop\TheBlueRed\pipeline.jpeg` (13 adım).

Biten: 1 kaynaklar, 2 ingestion, 3 layout parsing → structured document,
4 chunking, 5 embedding, 6'nın metadata+versioning kısmı, 8 hybrid retrieval.
Yan sütundaki evaluation harness planlanandan erken kuruldu (doğru sapma).

**Atlanan ve geri dönülmesi gereken:** adım 7 **Query Processing** (yeniden
yazma / genişletme / sınıflandırma). BM25'in Türkçe soruyla İngilizce kaynağı
bulamaması tam olarak bu adımın çözdüğü problem — yani hibrit ölçümü eksik bir
hatta yapıldı.

**Şemada olmayan ama gereken üç şey:** Excel/tablo verisi için SQLite dalı
(vektör araması değil kesin sorgu), etken madde normalizasyon katmanı
(INN → Türkçe varyant → ATC → ruhsat durumu), ve evaluation'ın yan sütunda
değil adımlar arası **kapı** olması.

---

## Sıradaki iş

1. **Reranker (adım 9).** Cross-encoder ile hibritin topladığı havuzu sırala.
   Reranker'sız taban çizgisi yukarıdaki tabloda; kazanç bunun üstüne ölçülecek.
   **Kullanıcı bu adımı seçti, sıradaki iş bu.**
2. **Query Processing (adım 7).** Atlandı, geri dönülecek.
3. **Vektör DB (adım 6).** pgvector imajı zaten kurulu (`pgvector/pgvector:pg16`),
   Qdrant ~200 MB indirme. Şu ölçekte numpy yeterli; DB kalıcılık ve üretim için.
4. **Excel'ler → SQLite.** EK-4A 8.334 satır, EK-4B, EK-4H 281 satır, TİTCK
   ruhsat listesi 22.965 satır.
5. **Etken madde normalizasyon sözlüğü.** Çekirdeği `chunk.py` içindeki `ILAC`
   sözlüğü (28 etken madde, Türkçe/ticari varyantlar + ATC). Büyüyünce ayrı modül.
6. **Erişimde çeşitlilik.** Aynı etken maddenin farklı markaları ilk k sonucu
   dolduruyor (Q07'de ilk üç sonuç aynı ürünün üç dozu). Ölçüldü, düzeltilmedi.
7. **Document Quality Backlog.** 4 taranmış zoledronik asit KÜB'ü OCR bekliyor;
   CAFİZO'nun kaynağı yanlış numaralandırılmış.

## Ortam notları

- Python: `_env/parse/Scripts/python.exe` (torch CPU, sentence-transformers 5.6.1).
- HF model önbelleği **D:** sürücüsünde (`HF_HOME=D:/hf_cache`); C: dardı,
  Docker sanal diski sıkıştırılarak 33 GB açıldı (kullanılmayan vllm imajı silindi).
- GPU yok; ağır gömme işleri Colab'da.

## Çalışma tarzı (kullanıcı geri bildirimi)

Kendi başına ileri gitme. Her aşamada ölçümü ver, yorumu kısa tut, sıradaki
adımı kullanıcı seçsin. Uzun çıktı istenmiyor.


## Sorgu isleme (7. adim) - eklendi 2026-08-06

Q18 dort modun dordunde de kacmisti: soru teklistamab, gelen elranatamab.
Ayni sinif, ayni doz semasi, ayni CRS uyarisi; ayirt eden tek sey ozel isim.
Gomme konuyu agirliklandiriyor, ismi degil. Reranker duzeltemedi cunku dogru
chunk havuza hic girmemisti.

_scripts/query_processing.py: ILAC sozlugu chunk.py'den geliyor (tek kaynak).
Ek olarak REJIM (22 kisaltma -> bilesen INN), SINIF (8 ilac sinifi), KISALTMA
(20 klinik kisaltma, TR+EN acilim), SITOGENETIK (6 desen).

Karar: sert metadata filtresi DEGIL, yeniden siralama. drug_names chunk'larin
%61'inde dolu; sert filtre etiketsiz %39'u (genel kilavuz metni, SUT, tani
algoritmalari) elerdi ve bos liste dondurebilirdi. Bunun yerine uc kume:
ilac uyan / etiketsiz / baska ilac. Hicbir aday atilmiyor.

SINIF sozlugu zorunlu parca: Q05 "bisfosfonat mi denosumab mi" sorusunda
yalnizca Denosumab tespit edilseydi zoledronik asit asagi itilir, karsilastirma
sorusunun yarisi kaybolurdu.

Olcum (--qp, tam arsiv, 20 soru):
  mod      recall@5      recall@10     MRR             kacan
  bm25     0.60 -> 0.65  0.70 -> 0.70  0.469 -> 0.618  6 -> 6
  dense    0.85 -> 0.90  0.85 -> 0.90  0.660 -> 0.713  3 -> 2
  hibrit   0.70 -> 0.75  0.90 -> 0.95  0.569 -> 0.679  2 -> 1

Kalan kacanlar: Q06 (VTE profilaksisi, uc modda da), Q07 (bobrek, dense).

Reranker + qp olcumu Colab'da: _work/colab/rerank_eval.ipynb (dokuz dosya
yukleniyor, 5. hucre dort mod, 6. hucre qp'siz ve havuz 20/100 karsilastirmasi).
Rapora artik havuz ve qp alanlari yaziliyor.


## Golden set 78 soruya cikarildi (2026-08-06)

golden_queries.json artik 78 soru: 38 klinik, 31 duzenleyici, 9 geri odeme.
Eski 20 soruluk kume golden_queries_v1.json olarak duruyor.
Hicbir sorunun hedefi bos degil (arsivde karsiligi var).

Olcut duzeltmesi: chunk_uyar icinde ayni hedefte hem belge hem icerik varsa
artik IKISI de saglanmali. Onceden icerik eslesmesi tek basina yetiyordu ve
"SUT'ta lenalidomid kosulu" sorusu lenalidomid gecen 4.336 chunk'in herhangi
birini dogru sayiyordu.

Olcum (tam arsiv, 78 soru, recall@5 / recall@10 / MRR / kacan):
  mod      qp yok                    qp var
  bm25     0.45 / 0.59 / 0.368 / 32  0.59 / 0.68 / 0.512 / 25
  dense    0.78 / 0.85 / 0.679 / 12  0.82 / 0.87 / 0.714 / 10
  hibrit   0.76 / 0.81 / 0.554 / 15  0.77 / 0.85 / 0.615 / 12

Skorlar 20 soruluk kumeye gore dustu; yeni sorular arsivin seyrek kosherine
dokunuyor (plazma hucreli losemi, hiperviskozite, belantamab okuler toksisite,
SUT ilac bazli kosullar). Rakam daha dusuk ama daha durust.
Bir soru artik %1,3 ediyor; onceden %5 idi.

## ACIK EKSIK: klinik dogrulama yok

Golden set'in 78 sorusunu ben yazdim ve hedefleri kilavuz metnine dayandirdim.
Hicbir hematolog gozden gecirmedi. Kullanici 2026-08-06'da bunu acikca belirtti:
"medikal olarak tam bilgiye sahip degilim".

Retrieval olcumu icin bu kabul edilebilir - orada olculen sey "dogru belge
geliyor mu", ve hedefler kaynak metinden turetildi. AMA Level 3'e (LLM'in
urettigi cevabin klinik dogrulugu) gecildiginde yetmez; orada uzman onayi
gerekir. Sistem bu haliyle "dogrulanmis" sayilmamali.


## Qdrant kuruldu (2026-08-07) - boru hattinin 6. adimi

Docker DEGIL, qdrant-client gomulu kip. Sebep: ayni kod hem yerelde hem
Colab'da degismeden kossun. Docker'a baglansaydik Colab icin ayri kurgu
gerekirdi ve ayni sistemin iki yolu olurdu. Sunucuya gecmek gerekirse
QdrantClient(path=...) yerine QdrantClient(url=...) - tek satir.

_scripts/qdrant_index.py: kur() / ara() / dogrula()
Depo: _work/qdrant (169 MB), koleksiyon "myeloma", 14.532 nokta, kosinus.
Payload: chunk_id, content + 10 metadata alani (drug_names, atc_codes,
section_number, source_type, version vb.)
Yukleme suresi 68 sn.

DOGRULAMA: 20 rastgele sorguda numpy ile Qdrant ilk 10 sonucu BIREBIR ayni.
Tasima sirasinda satir kaymasi olsaydi sistem hata vermeden yanlis cevap
uretecekti; bu yuzden parite kontrolu script icinde --dogrula olarak duruyor.

Karar: reranker mimariye DAHIL EDILMEDI (GPU bagimliligi). Olculmus secenek
olarak kodda ve raporda duruyor.
Karar: LLM Colab'da kosacak - yerelde GPU yok, CPU'da 8B model demo edilemez.
Karar: Ollama kurulmadi. Docker kurulu ama servisi kapali; gomulu kip sayesinde
gerekmedi.

Ortam: C: 32,1 GB bos, D: 55,4 GB bos.

Uctan uca parite (78 soru, --qp, --depo qdrant): numpy ile BIREBIR ayni.
  bm25 0.59/0.68/0.512 | dense 0.82/0.87/0.714 | hibrit 0.77/0.85/0.615
Sure: dense 78 sorguda numpy 1.2 sn, qdrant 7.7 sn (~100 ms/sorgu). Gomulu kip
diske dayali oldugu icin yavas ama kullanici deneyiminde fark edilmez.
retrieval_eval.py artik --depo numpy|qdrant aliyor; rapora depo alani yaziliyor.


## Cevap katmani kuruldu (2026-08-07) - _scripts/pipeline.py

Tek giris noktasi: cevapla(soru) -> {cevap, kaynaklar, guven, reddedildi}.
Demo da bunu cagiracak, Level 3 degerlendirmesi de. Iki ayri yol yazilsaydi
olctugumuz sistemle gosterdigimiz sistem farkli olurdu.

Akis: sorgu isleme -> Qdrant (genel + ilaca filtreli ikinci arama) ->
baglam daraltma -> tekrar ayiklama -> baglam kurma -> LLM -> denetim -> guven.

Arka uc degistirilebilir: SahteLLM (model yok, borulari test eder),
OllamaLLM, TransformersLLM (Colab). Iskelet GPU beklemeden test edildi.

KARARLAR VE GEREKCELERI
- Sikistirma = tekrar ayiklama, ozetleme DEGIL. Ozet yeniden yazmaktir;
  "kreatinin klerensi 30'un altinda" ifadesi "bobrek yetmezliginde" oluverir.
- Guven kategorik (yuksek/orta/dusuk), sayisal olasilik degil. Kalibrasyon
  verisi yok; "%87 dogru" demek uydurma kesinlik verir.
- Reddetme: en iyi skor < 0.55 ise model HIC cagrilmiyor.
- Baglam daraltma aramadan DAHA SERT: aramada uc kume (uyan/etiketsiz/baska
  ilac) hicbiri atilmiyordu; baglamda baska ilaca ait parcalar hic alinmiyor.

BULUNAN VE DUZELTILEN IKI SORUN
1. Etiketsiz sanilan parcalar aslinda baska ilacin KUB'undan geliyordu
   ("Doz azaltma basamaklari" tablosu REVLIMID belgesinde, metninde
   lenalidomid yazmiyor). Belge adindan ilac cozuluyor artik.
2. Kunye satiri cirkin: "s.None surum None", bolum alaninda "**<u>Doz</u>**".
   temiz_baslik() + BOLUM_NO dogrulamasi eklendi; metne dokunulmuyor,
   yalnizca gosterim sadelestiriliyor.

ACIK KALAN
TECVAYLI artik baglama giriyor (ilaca filtreli ikinci arama sayesinde) ama
DOGRU BOLUM degil - farmakokinetik bolumu geliyor, basamakli doz bolumu degil.
Reranker olcumde tam bunu duzeltiyordu. Colab demosunda reranker acilabilir.

Test: kedi mamasi sorusu -> skor 0.487, reddedildi. Karfilzomib sorusu ->
uc kaynak da karfilzomib KUB 4.4, surum tarihleri dogru.


## Ilk gercek cevaplar (2026-08-07, Colab T4, Qwen2.5-7B-Instruct 4bit)

Sonuclar _logs/cevap_demo.json. Sure: soru basina 12-51 sn (k=4, 4 bit).

BULUNAN DORT SORUN

1. REDDETME CALISMADI - en kritik. Apandisit sorusu (arsivde yok) 0,565 skorla
   0,55 esigini kil payi gecti; model kendi bilgisinden cevap uydurdu
   (klindamisin, sefalosporin) ve sonuna "Bu bilgi arsivde bulunamadi" ekleyip
   kendisiyle celisti. Skor esigini yukseltmek cozum degil: gecerli teklistamab
   sorusu 0,63 aliyor, pencere cok dar.
   COZUM: ikinci kapi. DAYANAK_ESIGI=0.40 - cevap URETILDIKTEN sonra
   dayanaklilik olculuyor, altindaysa cevap gosterilmiyor. Uyduran model
   dayanamaz cunku dayanacak kaynak yoktur.

2. ATIF YOK - teklistamab cevabinda hicbir atif yok, oysa EMA_tecvayli_PI 4.2
   (Posology) kaynaklar arasindaydi. Model dogru sayilari verdi (0,06/0,3/1,5
   mg/kg) ama kaynaktan mi kendi bilgisinden mi belli degil.
   COZUM: istem kurali 7-8 eklendi (her cumleye atif, sonuc cumlesi yasak).

3. CUMLE AYIRICI HATASI - kendi olcumumde. Turkcede sira sayilari noktayla
   yaziliyor ("1. ve 2. gunlerinde") ve ayirici bunlari cumle sonu saniyordu;
   parcalanan cumleler atifsiz kalip dayanakli bir cevabi 0,2 gosteriyordu.
   Ilk duzeltme de yanlisti: (?<![0-9])(?<=[.!?]) iki ileriye-bakis AYNI
   karaktere bakiyor, nokta rakam olmadigi icin kontrol hep geciyordu.
   Dogrusu: (?<![0-9]\.)(?<=[.!?])\s+

4. RETRIEVAL BOLUM SECIMI - karfilzomib dozu 5.1 Farmakodinamik bolumunden
   geldi, 4.2 Pozoloji'den degil. Cevap dogru ama kaynak bolumu yanlis.

DUZELTMELERDEN SONRA (ayni dort cevap yeniden puanlandi)
  karfilzomib   0.50 GECER    (once yanlis olculuyordu)
  teklistamab   0.00 REDDET   (atif yok - dogru davranis)
  lenalidomid   0.67 GECER
  apandisit     0.00 REDDET   (kritik hata kapandi)

BELLEK: T4'te 8 parcalik baglam tasti (dikkat hesabi dizi uzunlugunun
karesiyle buyuyor). BAGLAM_PARCA 8->5, uretim 700->500 token, BGE-M3 CPU'ya
alindi (GPU'da 2,3 GB yiyordu). cevapla() varsayilanlari artik govdede
okunuyor - imzadaki varsayilan tanim aninda sabitlendigi icin calisma aninda
degistirilemiyordu.

TRANSFORMERS SURUM TUZAGI: apply_chat_template(return_tensors="pt") artik
tensor degil BatchEncoding donduruyor, generate() icinde .shape patliyor.
Once tokenize=False ile metne cevirip sonra tokenlemek her surumde calisiyor.


## Ikinci kosu - duzeltmeler tuttu (2026-08-07)

_logs/cevap_demo (1).json

  soru          arama  dayanak  sonuc     not
  karfilzomib   0.748  0.500    GECTI     dozlar birebir aktarilmis (20/56 mg/m2,
                                          gun 1,2,8,9,15,16) - doz sadakati tamam
  teklistamab   0.630  0.000    REDDEDILDI  YANLIS reddetme (asagi bak)
  lenalidomid   0.627  0.667    GECTI     uc maddenin ucu de atifli
  apandisit     0.565  0.333    REDDEDILDI  kritik acik kapandi

Apandisit: model bu sefer uydurmadi, SUT'un genel antibiyotik receteleme
kurallarina dayanip duzgun atif yapti - ama yanlis alandan. Kapi yine tuttu
cunku sonuc cumlesi dayanaksizdi. DIKKAT: 0.333 esige yakin. Diligent bir model
alakasiz kaynaklara duzgun atif yaparsa kapiyi gecebilir. Alan kapisi (getirilen
chunk'larin miyelomla ilgisi) hala yok - bilinen acik.

YANLIS REDDETME (teklistamab): bilgi arsivde VAR (EMA_tecvayli_PI 4.2 kaynaklar
arasindaydi), model dogru semayi da verdi (0,06/0,3/1,5 mg/kg) ama hicbir atif
yapmadi ve yasakladigimiz ozet cumlesini yine yazdi. 7B model kural listesini
eksik takip ediyor. COZUM DENENDI: isteme dogru/yanlis bicim ORNEGI eklendi -
bu boyuttaki modeller kuraldan cok ornekten ogreniyor. Sonraki kosuda olculecek.

KALAN SORUNLAR
- Karfilzomib dozu 5.1 Farmakodinamik bolumunden geliyor, 4.2 Pozoloji'den degil.
- SUT chunk basligi "fff) Daratumumab" ama icerik lenalidomid kosullari:
  SUT'ta chunk sinirlari madde basliklariyla hizali degil.
- Alan kapisi yok (yukarida).


## Level 3 sonucu ve olcut krizi (2026-08-07)

ILK OLCUM YANILTICIYDI. Rapor: B kumesinde 3/39 cevaplandi, 36 haksiz red,
0 uydurma. "Sistem asiri ihtiyatli" gorunuyordu. Yanlisti.

Kapidan BAGIMSIZ sayi bunu ele verdi: atif verilen parca golden hedefi 49/78
tutuyordu ve bunlarin 31'i dayanaklilikta 0,0 almisti. Dayanakliligin medyani
hem pozitifte hem negatifte tam 0,0 idi - bu sistemin degil olcutun imzasi.

SEBEP: dayanaklilik SOZCUK ORTUSMESIYLE olculuyordu. Cevap Turkce, NCCN
Ingilizce. BM25'in basina gelenin aynisi; leksik yontem iki dilli arsivde
calisamaz. Ilk dort demo cevabinin 0,5-0,667 almasi sansti - kaynaklari SUT ve
Turkce KUB'lerdi.

UC DUZELTME (answer_eval.yeniden_puanla)
1. Anlamsal dayanaklilik: cumle ve parca BGE-M3 ile gomulup kosinus.
2. Toplu atif bicimi [K1, K2, K3] taniniyor (49 -> 52 hedef tutan).
3. Olcut ikiye ayrildi: kanit_orani (verilen kaynaklarda var mi = guvenlik) ve
   atif_orani (gosterilen kaynakta var mi = Level 4).

OLCUT DUZELINCE TABLO TERSINE DONDU
  B kumesi, kapi yok: 39/39 cevaplandi, 28 hedef tuttu, UYDURMA 6/7.
Sistem asiri ihtiyatli degil, asiri comertmis.

Esik taramasi hicbir kombinasyonda sifir uydurma bulamadi. Yapisal sebep:
dayanaklilik "iddia kaynaklarda var mi" diye soruyor, "kaynaklar soruyla
ilgili mi" diye degil. Apandisit cevabi SUT'un genel antibiyotik kurallarina
GERCEKTEN dayaniyordu.

## Alan kapisi (2026-08-07)

Leksik kapsam CALISMADI: 15 negatifin 10'unda eksik terim yok. KUB'lerin
etkilesim/yan etki bolumleri yuzlerce baska ilaci aniyor - metformin,
propranolol, levotiroksin, metotreksat hepsi arsivde geciyor. Arsiv sozlugu
19.511 kok, _work/arsiv_sozluk.json.

Isleyen iki sinyal:
  varlik  (sorguda ilac/hastalik/rejim/sinif taninmasi): poz 59/78, neg 1/15
  hast    (getirilen parcalarin hastalik etiketi orani): poz 0.55, neg 0.17

A kumesinden secilen kural: varlik|hast75
B kumesi (esigin gormedigi) karsilastirma:
  kapali           39/39 cevap, 28 hedef, uydurma 6/7
  varlik           31/39 cevap, 21 hedef, uydurma 1/7
  varlik|hast75    33/39 cevap, 22 hedef, uydurma 1/7   <- secilen
  hast75           16/39 cevap,  9 hedef, uydurma 0/7

SECILEN KURULUM (B kumesi, esigin gormedigi veri):
  cevaplanan 33/39 | hedefi tutan 22/39 | atifi dogru 13/33 | haksiz red 6
  UYDURMA 1/7
Kapidan bagimsiz atif isabeti: 52/78.

KALAN UYDURMA (N14) VE KIRLENME UYARISI
N14 "KOAH alevlenmesinde sistemik steroid" gecti; SINIF sozlugunde ciplak
"steroid" deseni deksametazon/prednizona esleşiyordu. Bu gercek bir sozluk
hatasi ve duzeltildi (artik kortikosteroid|glukokortikoid).
AMA N14 OLCUM (B) yarisindaydi. Yani duzeltmeden sonra cikacak "0/7" rakami
KIRLENMISTIR - o negatifi gorerek duzelttik. Raporda basligi "1/7" kalmali;
duzeltmenin gercek etkisi ancak YENI bir negatif kumede olculebilir.

TAZE NEGATIF KUME (N16-N30) - 2026-08-07
Kirlenme uyarisina cevap olarak 15 yeni negatif yazildi:
_work/eval/negative_queries_v2.json. Kume bilerek ZOR: 13 soru miyelom disi
hematoloji (AML 7+3, ITP, KML/imatinib, Hodgkin/ABVD, DVT/warfarin, demir
eksikligi, orak hucre, hemofili, aplastik anemi, KLL/ibrutinib, AIHA,
polisitemia vera, talasemi), 2 soru tuzak: del(5q) MDS'de lenalidomid ve
mantle hucreli lenfomada bortezomib - ilac arsivde var, endikasyon yok.

Esikler DONDURULDU (arama 0.50, alan kurali varlik|hast75). Yeni kumeye
bakarak esik degistirmek olcumu yine kirletirdi.

Olcum scripti: _scripts/negatif_taze.py. Dil modeli kosturmuyor; ilk iki
kapiyi (arama skoru + alan) olcuyor. Modele ulasan soru sayisi UYDURMA UST
SINIRI; kapiya takilan soru kesin uydurma uretemez.

YEREL ON SONUC (varlik sinyali, GPU gerektirmiyor):
  eski kume  varlik taniyan 0/15
  taze kume  varlik taniyan 2/15  -> yalnizca N25, N26 (bilerek konan tuzaklar)
Leksik kapsam yine ayirt etmiyor: taze kumenin 13'unde kapsam 1.00.
Kalan olcum (alan_hast + arama skoru) Colab'i bekliyor - cevap_demo.ipynb
son hucre, GPU gerektirmiyor, 1-5. hucreler yeterli.

TAZE NEGATIF SONUCU (2026-08-07, kirlenmemis)
Esikler dondurulmus (arama 0.50, alan varlik|hast75), 15 taze negatif:
  arama kapisi durdurdu : 0 / 15
  alan kapisi durdurdu  : 11 / 15
  modele ulasan         : 4 / 15   (N21, N25, N26, N30)

EN ONEMLI BULGU: ARAMA SKORU KAPISI ALAN DISI SORULARI HIC AYIRT ETMIYOR.
15 sorunun 15'i de esigi gecti; skorlar 0,533 - 0,724 arasinda, yani gecerli
miyelom sorularinin araligiyla (0,63 - 0,72) tamamen ic ice. Gomme modeli
"tibbi soru <-> tibbi metin" benzerligini olcuyor, "bu arsivin konusu mu"
sorusunu degil. Ilk kurulumda tek guvenlik kapisi buydu; tek basina calissa
15 uydurma uretirdi. Alan kapisi bu yuzden zorunlu, opsiyonel degil.

MODELE ULASAN DORT SORU
  N25 lenalidomid / del(5q) MDS   - tuzak, varlik=1 (ilac arsivde var)
  N26 bortezomib / mantle lenfoma - tuzak, varlik=1
  N21 demir eksikligi anemisi     - hast 0,75, sinirdan gecti
  N30 talasemi demir selasyonu    - hast 1,00
Tuzaklarin gecmesi beklenen davranis ve sistemin bilinen siniri: "arsivdeki
ilac, arsiv disi endikasyon" ayrimini varlik tanima yapamaz. N21/N30 ise
arsivdeki anemi ve demir icerigi uzerinden geciyor.
Bu dort sayi UST SINIR: dorduncu kapi (dayanaklilik) bir kismini eleyebilir.

KAPILAR URETIME BAGLANDI (pipeline.py)
Onceki durum: secilen esikler yalnizca degerlendirmede yasiyordu, cevapla()
hala eski kirlenmis degerlerle ve BOZUK leksik dayanaklilikla kosuyordu.
  REDDET_ESIGI  0,55 -> 0,50
  DAYANAK_ESIGI 0,40 -> 0,20   (olcut degisti, degerler kiyaslanamaz)
  SEM_ESIGI     0,50           (yeni: cumle-parca BGE-M3 kosinusu)
  ALAN_KURAL    varlik|hast75  (yeni ucuncu kapi, uretim oncesi)
dayanaklilik() artik anlamsal; parca vektorleri BAAI_bge-m3.npy'den nokta
id ile okunuyor (yeniden kodlama yok - aramadakinden farkli vektor uretme
riski olurdu). answer_eval.ham_kos artik alan_kural="kapali" ile cagiriyor,
yoksa esik taramasi kendi sectigi kuralin sonucunu olcerdi.

UCTAN UCA TAZE NEGATIF KOSUSU (2026-08-07) - KAPILAR BAGLI HALDE
15 taze negatif, gercek dil modeli, uretim esikleri:
  alan kapisi durdurdu   : 11
  dayanak kapisi durdurdu:  2   (N21 demir eksikligi, N30 talasemi)
  cevap uretildi         :  2   (N25 lenalidomid/del(5q) MDS, N26 bortezomib/MCL)
  UYDURMA                :  0

N21 ve N30'da model zaten kendiliginden "Bu bilgi arsivde bulunamadi" dedi;
dayanak kapisi bunu tuttu. Iki katmanin ust uste calistigi yer burasi.

IKI "TUZAK" SORU GECERSIZ CIKTI
N25 ve N26'nin negatif sayilmasi benim hatamdi. Varsayim: "ilac arsivde var
ama endikasyon yok". Arsiv dogrulandi, varsayim yanlis:
  ema__EMA_revlimid_PI 4.1/4.2  -> del(5q) MDS endikasyonu + 10 mg baslangic
  fda__labels__FDA_REVLIMID_PI  -> ayni doz
  ema__EMA_velcade_PI           -> MCL endikasyonu + VcR-CAP (75 chunk)
Sistemin verdigi iki cevap da DOGRU, KAYNAKLI ve atifli. Uydurma degil.
Ders: tam KUB/PI belgeleri ilacin BUTUN endikasyonlarini tasir. Bu arsivin
kapsami "multipl miyelom" diye tanimlansa da, icerdigi belgeler miyelom disi
endikasyonlari da iceriyor. Sunumda kapsam boyle anlatilmali.

RAPORLANABILIR RAKAM (kirlenmemis, esikler dondurulmus):
  15 taze negatif -> 13 reddedildi, 2 dogru cevaplandi, 0 uydurma.
Eski kume rakami (1/7) bu olcumun yerini almiyor; o kume kirlenmisti ve
sorulari kolaydi (baska branslar). Sunumda taze kume rakami kullanilmali.

## Level 4 - atif dogrulugu (2026-08-07)

TESHIS: SORUN YANLIS NUMARA DEGIL, EKSIK ATIF
273 cumle uzerinde:
  atif dogru parcayi gosteriyor : 116
  atif YOK                      : 144
  atif var ama numara yanlis    :   4
  hicbir parcada karsiligi yok  :   9
Cevap bazinda: 78 cevabin 30'unda hicbir atif yok, 37'si kismi atifli,
yalnizca 11'i her cumlede atif veriyor. Modelin aliskanligi dort cumle yazip
sonuna tek [K2] koymak.

ISTEM SIKILASTIRMA IKI KEZ DENENDI VE TUTMADI
Kural 7 ("her cumlenin ve her madde isaretinin sonunda atif olmali"), kural 8
(ozet cumlesi yasak) ve dogru/yanlis BICIM ORNEGI istemde zaten vardi; Level 3
kosusu bu istemle yapildi. 7B model bicim disiplinini tutturamiyor. Ucuncu bir
istem turu yerine yapisal cozume gecildi.

COZUM: URETIM SONRASI ATIF ONARIMI (pipeline.atif_onar)
Atif numarasi modelden istenmiyor, cumle-parca kosinusuyle ATANYOR:
  - atifsiz cumle, en yakin parca >= 0,50 ise o parcanin numarasini alir
  - model numara yazmissa dokunulmuyor; yalnizca gosterdigi parca esigin
    altindayken VE baska bir parca esigi gecerken duzeltiliyor
  - hicbir parca esigi gecmiyorsa cumle ATIFSIZ birakiliyor (uydurma kaynak
    takmaktansa dayanaksiz gorunmesi dogru; dayanaklilik kapisi zaten yakalar)
Donen sayac: {eklenen, duzeltilen, biraklan}. guven["model_atifi"] ile modelin
kendi verdigi numaralar da saklaniyor - onarim gizlenmiyor.

cumlelere_bol() eklendi: satir sonlari da sinir. Cevaplarin ucte ikisi madde
listesi iceriyor ve madde satirlari nokta ile bitmiyordu; eski bolme butun
listeyi tek "cumle" sayiyordu. Uzunluk esigi 15 -> 10 (klinik madde satirlari
kisa: "- 1,3 mg/m2 IV" 14 karakter).

OLCUM GPU GEREKTIRMIYOR
Onarim deterministik, bu yuzden KAYITLI 78 cevap uzerinde olculebiliyor -
dil modeli yeniden kosmuyor. answer_eval.yeniden_puanla artik her kayit icin
atif_onarimi, cevap_onarilmis ve hedef_tuttu_onarim uretiyor; yeniden_rapor
onarim oncesi/sonrasi Level 4 rakamini yan yana basiyor.
Colab hucresi: _work/colab/atif_onarim_hucre.py

ATIF ONARIMI ILK SONUC (2026-08-07)
238 cumleye atif eklendi, 3 duzeltildi, 18 dayanaksiz birakildi.
Level 4 (atif verilen parca golden hedefi tutuyor mu):
  tum kume  52/78 -> 59/78
  A yarisi  24/39 -> 27/39
  B yarisi  28/39 -> 32/39   <- esigin gormedigi, raporlanacak olan
Kaybedilen soru yok (onarim hicbir dogru atifi bozmadi).
Kazanilanlar: Q10, Q11, Q14, Q15, Q23, Q32, Q48.

NOT - METRIK DAIRESELLIGI: onarim sonrasi "cumle bazinda atif dogru" orani
olculmemeli. Onarim atifi zaten anlamsal benzerlige gore atiyor, yani o olcuye
gore tanimi geregi %100 dogru cikardi. Bagimsiz olcu golden hedef, yukaridaki
52 -> 59 rakami odur.

CUMLE BOLME YAPAYLIGI - ILK TESHIS KISMEN YANLISTI
Model atifi cogu zaman noktadan SONRA yaziyor ("... yapilmalidir. [K3]").
Bolucu noktada boldugu icin [K3] ayri parcaya dusuyor, kisa oldugu icin
eleniyor, cumle ATIFSIZ gorunuyordu. Duzeltildi (_SADECE_ATIF ile geri
yapistirma). Kayitli 78 cevapta olculen fark:
  eski bolucu: 129/273 birimde atif var (%47), hic atifsiz cevap 30/78
  yeni bolucu: 185/333 birimde atif var (%55), hic atifsiz cevap  2/78
Yani "78 cevabin 30'unda hicbir atif yok" ifadesi yanlisti; dogrusu 2/78.
Model atif YAPIYOR, ama cumlelerin yaklasik yarisinda. Onarim yine gerekli
(148 birim atifsiz), ama baslangic noktasi raporlanandan iyiydi.
Level 4 rakamlari (52 -> 59) bu hatadan ETKILENMEDI: onlar cevabin tamamindaki
atif numaralarina bakiyor, cumle bolmeye degil.
YENIDEN OLCUM GEREKIYOR: onarim artik mevcut atiflari gorecegi icin daha az
mudahale edecek; 59/78 rakami yeni bolucuyle tekrar hesaplanmali.

ATIF ONARIMI - DUZELTILMIS BOLUCUYLE YENIDEN OLCUM (2026-08-07, kesin)
136 cumleye atif eklendi, 6 duzeltildi, 12 dayanaksiz birakildi.
(Ilk kosuda 238 eklenmisti; fark bolucu yapayligindan geliyordu - mevcut
atiflar goruluyor artik, cift atif uretilmiyor.)
Level 4, golden hedefe gore:
  tum kume  52/78 -> 57/78
  A yarisi  24/39 -> 26/39
  B yarisi  28/39 -> 31/39   <- RAPORLANACAK RAKAM
Kaybedilen soru yok. Kazanilan: Q14, Q15, Q23, Q32, Q48.
Kalan 8 soru (B'de) atif hedefi tutmuyor; bunlarin bir kisminda hedef parca
zaten baglama girmemis, yani sorun Level 4 degil Level 2.

B kumesi kapili olcum ozeti (esikler A'dan): cevaplanan 33/39, hedefi tutan
22/39, haksiz red 6, ort kanit orani 0,94.
NOT: ayni ozetteki "uydurma 0/7" KIRLENMISTIR (N14 duzeltmesi bu kumeyi
gorerek yapildi). Uydurma icin gecerli rakam TAZE kumeden: 0/15.

## Dil modeli karsilastirmasi (2026-08-08)

ISTEK: paydaslarin tekrarlanan talebi - "baska LLM'ler de deneyin, sonuclara
bakin". Web teslimatindan ONCE yapiliyor, cunku secilen model sunucunun
donanim gereksinimini de belirliyor.

KURGU
Degisen tek sey uretici model. Sabit kalanlar: chunk'lar, BGE-M3, Qdrant
aramasi, sorgu isleme, baglam secimi, istem, esikler, atif onarimi. Fark
modele atfedilebilsin diye.

ASIRI UYUM: model secmek de bir esik ayaridir. Bu yuzden iki faz var:
  ELEME  A yarisi (39 pozitif + 8 negatif) - butun modeller
  OLCUM  B yarisi (39 pozitif + 7 negatif) - yalnizca kazanan, TEK KEZ
Esikler her model icin yeniden SECILMIYOR; dondurulmus degerler kullaniliyor.
Yoksa her modele kendi sinavini yazdirmis olurduk.

ADAY MODELLER (hepsi acik erisim - gated depo HF tokeni ister, teslim
edilecek sistemde ek bagimlilik olurdu):
  Qwen/Qwen2.5-7B-Instruct                      (mevcut temel)
  Qwen/Qwen2.5-14B-Instruct                     (4 bitte ~9,5 GB, T4'e sigar)
  ytu-ce-cosmos/Turkish-Llama-8b-Instruct-v0.1  (Turkce odakli)
  unsloth/Meta-Llama-3.1-8B-Instruct            (Llama 3.1 kapisiz ayna)

OLCULEN: cevaplanan, golden hedefi tutan, atif isabeti (onarim oncesi/sonrasi),
uydurma, haksiz red, 20 karakterden kisa cevap sayisi, soru basina saniye.

Script: _scripts/llm_bakeoff.py   Colab hucresi: _work/colab/llm_bakeoff_hucre.py
Her model kendi dosyasina yaziyor (_logs/bakeoff/eleme_<model>.json); oturum
koparsa hucre bitmis modelleri atliyor, bastan baslamak gerekmiyor.

MODEL LISTESI - ISTENEN IKI EKLEME (2026-08-08)
Qwen3.6-27B: gercekten var (22 Nisan 2026, Apache 2.0), dort bitte ~16,8 GB.
T4'un 16 GB'ina SIGMIYOR; L4 (24 GB) veya A100 gerekiyor. Listeye eklendi ama
uygun_modeller() GPU'ya gore otomatik suzuyor, yani T4'te sessizce atlaniyor.

DeepSeek V4: eklenMEDI, cunku kucuk acik surumu yok. Iki varyant var - V4-Pro
1,6 trilyon, V4-Flash 284 milyar (13B aktif MoE). Flash bile dort bitte 150
GB'in uzerinde, Colab'in hicbir GPU'suna sigmiyor. Tek yol API; o da klinik
sorulari ve KUB metinlerini disariya gondermek demek. Teknik degil veri
yonetisimi karari - kurum onayi gerekir, karar verilirse eklenir.

DRIVE KARARI
Model onbellegi Drive'a KONMUYOR: HF indirmesi Colab'da hizli, Drive okumasi
binlerce kucuk dosyada tikaniyor; 5 GB'lik modeli Drive'dan yuklemek yeniden
indirmekten uzun suruyor. Drive iki is icin kullaniliyor:
  1. proje dosyalari (chunks 30 MB + gommeler 57 MB + scriptler) - bir kez
     yuklenip Drive'a yaziliyor, sonraki oturumlar oradan kopyaliyor
  2. sonuclar - her model bitince Drive'a yaziliyor, oturum koparsa kayip yok
Qdrant deposu da Drive'a konmuyor (169 MB, Drive uzerinden okumak aramayi
yavaslatir; yeniden kurmak 70 saniye).

Yapistirma hucresi yerine defter: _work/colab/llm_bakeoff.ipynb
Defteri ureten script: _work/colab/llm_bakeoff_defter.py (hucre metinleri
Python dizesi olarak duruyor, bozuk JSON riski yok).
Eski llm_bakeoff_hucre.py silindi.

DEEPSEEK KARARI - NIHAI (2026-08-08)
V4 eklenemedi (yukarida gerekcesi). Yerine ayni aileden calistirilabilir model
eklendi: deepseek-ai/DeepSeek-R1-Distill-Qwen-14B, MIT, dort bitte ~9,5 GB,
T4'e sigiyor.

DUSUNEN MODEL ICIN IKI DUZELTME (pipeline.TransformersLLM)
R1 turevleri cevaptan once <think> blogu uretiyor. Onlemler:
  1. DUSUNCE regex'i blogu ayikliyor. Kapanis etiketi hic gelmeyebilir (token
     butcesi biterse), o yuzden desen acilisi da temizliyor.
  2. azami_token model adina gore: dusunen modelde 1400, digerlerinde 500.
     Yoksa butun butce ic konusmada biter, model haksiz yere "bos cevap
     veriyor" gorunurdu.
Ayrim model adindan yapiliyor ("r1", "distill", "think" gecenler).
Bu bir olcum adaleti duzeltmesi: modeli kendi calisma bicimine izin vermeden
olcup "kotu" demek, olctugumuz seyi degil kurulumumuzu raporlamak olurdu.

T4 icin uygun liste artik 5 model (~2,5-3 saat), L4 icin 6.

## Dil modeli karsilastirmasi - ELEME SONUCU (2026-08-09, A yarisi 39+8)

model                          cevap  hedef  atif  uydurma  red  kanit    sn
Meta-Llama-3.1-8B-Instruct     32/39     22    27      1/8    7   1.00  15.4
Qwen2.5-14B-Instruct           32/39     22    25      1/8    7   0.93  18.5
Qwen2.5-7B-Instruct            31/39     21    25      0/8    8   0.93  11.1
Turkish-Llama-8b-v0.1          32/39     22    26      1/8    7   0.97  34.8
Qwen3.6-27B                    31/39     25    31      1/8    8   0.36 103.0  <- GECERSIZ

QWEN3.6-27B SONUCU GECERSIZ
39 cevabin 39'unda modelin dusunme sureci DUZ METIN olarak cevaba karisti:
"Here's a thinking process: 1. Analyze User Input - Role: Clinical decision
support assistant... Rules: 1. Only use provided source texts". <think>
etiketi kullanmadigi icin DUSUNCE ayiklayicisi yakalayamadi.
Belirtiler: ortalama cevap 1772 karakter (Qwen2.5-7B'de 439), 614 cumle
dayanaksiz, kanit orani 0,36, soru basina 103 saniye.
"En yuksek hedef (25) ve en yuksek atif (31)" rakamlari yetenek degil, cok
yazmanin yan urunu: uzun cevapta her sey bir yerlere degiyor.
DUZELTME: apply_chat_template artik enable_thinking=False ile cagriliyor
(taninmayan sablonlarda TypeError'a geri adim var). Model yeniden
kosulmadan bu satir rapora girmemeli.

ATIF ONARIMI SUTUNU BU KOSUDA OLCULEMEDI
Her modelde "onarim oncesi -> sonrasi" ayni cikti (27->27, 25->25). Sebep:
onarim cevapla() icine baglandi, yani kaydedilen cevap ZATEN onarilmisti ve
ikinci gecis idempotent. DUZELTME: answer_eval.ham_kos artik
atif_onarim=False ile cagiriyor, ham cikti saklaniyor.
Onarimin katkisi zaten ayri olculmustu (78 soruda 52 -> 57).

GECERLI DORT MODELIN KARSILASTIRMASI
Hedef tutma 21-22 arasinda, yani DORT MODEL DE AYNI. 39 soruda 1 soruluk fark
gurultudur (binom %95 araligi kabaca +-6 soru). Bu kumede model secimi
dogruluk farki YARATMIYOR.
Ayrisma baska yerlerde:
  hiz    Qwen2.5-7B 11,1 sn  <  Llama-3.1 15,4  <  Qwen2.5-14B 18,5
         <  Turkish-Llama 34,8
  uslup  Qwen2.5-7B en kisa (439 karakter), Turkish-Llama en uzun (1625)
  dayanak Turkish-Llama 270 cumleye atif eklenmesi gerekti (cok yaziyor),
         Qwen2.5-7B yalnizca 22
  uydurma Qwen2.5-7B 0/8, digerleri 1/8

KARAR (oneri): Qwen2.5-7B kalsin.
Dogrulukta fark yok, en hizli, en az gevezelik, tek sifir uydurma. Teslim
acisindan da en iyisi: en kucuk donanim. 14B'ye gecmek soru basina %66 daha
uzun sure ve iki kat bellek karsiliginda olculebilir bir kazanc getirmiyor.
Kazanan B yarisinda TEK KEZ olculecek, rapora o rakam girecek.

QWEN3.6-27B YENIDEN KOSU - DUZELTILMIS (2026-08-09)
enable_thinking=False ile dusunme sizintisi tamamen kesildi:
  ort cevap uzunlugu 1772 -> 583 karakter
  dusunme sizan cevap 39/39 -> 0/39
  kanit orani 0,36 -> 0,68
  sure 103 -> 38,3 sn
Turkcesi listedeki en akici olani (ornek: "Nakil adayi olan hastalarda
birincil tedavi icin standart olarak 4 ilacli rejimler tercih edilir").

AMA OLCUMDE ONDE DEGIL, GERIDE:
  cevaplanan 26/39 (digerleri 31-32)
  haksiz red 13     (digerleri 7-8)
  hedef      21     (digerleri 21-22 - ayni bant)
Arama ayni oldugu icin fazladan reddetmeler DAYANAK kapisindan geliyor:
model kaynagi kendi cumlesiyle yeniden yaziyor, anlamsal baglanti zayifliyor,
kapi kapatiyor. Yani akici Turkce burada bir dezavantaj: klinik bir sistemde
istedigimiz sey guzel ifade degil, kaynaga yapisik ifade.
Ilk kosudaki "hedef 25" rakami da boylece aciklandi - yetenek degil, uzun
cevabin her seye degmesiydi. Duzeltilince 21'e, yani banda dustu.

NIHAI ELEME TABLOSU (A yarisi, 39 pozitif + 8 negatif)
model                          cevap  hedef  atif  uydurma  red  kanit    sn
Meta-Llama-3.1-8B-Instruct     32/39     22    27      1/8    7   1.00  15.4
Qwen2.5-14B-Instruct           32/39     22    25      1/8    7   0.93  18.5
Qwen2.5-7B-Instruct            31/39     21    25      0/8    8   0.93  11.1
Turkish-Llama-8b-v0.1          32/39     22    26      1/8    7   0.97  34.8
Qwen3.6-27B                    26/39     21    23      0/8   13   0.68  38.3

KARAR: Qwen2.5-7B-Instruct.
Hedef tutmada bes model de ayni bantta (21-22/39); 39 soruda bir soruluk fark
gurultudur. Ayrisma hizda ve donanimda: 7B 11,1 sn ve ~5 GB, 27B 38,3 sn ve
24 GB GPU. Buyuk model ne dogruluk ne guvenlik kazandirdi; aksine daha cok
haksiz reddetti. Teslim edilecek sunucunun gereksinimini bu karar belirliyor.

## KARAR_KAYDI.md olusturuldu (2026-08-09)

Bu dosya (DURUM.md) kronolojik: ne zaman ne oldugunu anlatiyor ve icinde
sonradan gecersizlesmis satirlar var. Yeni _logs/KARAR_KAYDI.md farkli bir
soruya cevap veriyor: bugun dogru olan nedir, hangi rakama dayaniyor, ham
verisi nerede. Bolumleri: dondurulmus kararlar, olcum kaydi, KIRLENMIS VE
GECERSIZ RAKAMLAR, dosya envanteri, bilinen eksikler, yeniden uretim.

Rapor/sunum yazarken KARAR_KAYDI.md esas alinmali. DURUM.md tarihce olarak
kalir - hangi hatanin nasil bulundugu orada duruyor ve sunumun "olcum
disiplini" bolumu icin degerli.

BU SIRADA BULUNAN SESSIZ HATA
_logs/level3_yeniden.json eski surumu tutuyordu: Colab'dan inen iki dosyadan
(1) kanonik isme kopyalanmisti, oysa duzeltilmis cumle bolucusuyle kosan (2)
idi. Fark: 238 ekleme / 52->59 (eski) yerine 136 ekleme / 52->57 (dogru).
Duzeltildi, (1) silindi. Rapora giren rakam: 52 -> 57 (tum kume), 28 -> 31 (B).
Tam da "bilgi kaybolmasin" denen seyin ornegi: dosya duruyordu ama yanlis
surumu duruyordu.

## OLCUM FAZI KAPANDI (2026-08-09) - Qwen2.5-7B, B yarisi

  cevaplanan     33/39
  hedefi tutan   22/39
  atif isabeti   28 -> 31   (onarim: 66 eklendi, 3 duzeltildi, 4 birakildi)
  haksiz red     6
  ort kanit      0,941
  ort uzunluk    492 karakter
  soru basina    26,7 sn

DIKKAT - BU BIR TEKRAR URETIM, YENI KANIT DEGIL
39 cevabin 39'u onceki level3 kosusuyla BIREBIR AYNI cikti. Sasirtici degil:
ayni model, ayni sorular, do_sample=False (aclık kod cozme). Yani bu kosu
"ikinci bir bagimsiz olcum" degil.
Kanitladigi sey baska ve yine degerli: level3 rakamlari eski kod yolundan
uretilmis cevaplarin sonradan puanlanmasiyla cikmisti; bu kosu ise DONDURULMUS
URETIM YOLUNDAN uctan uca gecti (anlamsal dayanaklilik, duzeltilmis cumle
bolucu, cevapla() icine bagli alan kapisi, ham cikti saklama). Ayni rakamlarin
cikmasi = yapilan refaktorler davranisi bozmadi. Regresyon yok, uretilebilirlik
tam.

SURE FARKI DONANIMDAN: eleme fazinda ayni model 11,1 sn/soru idi, burada 26,7.
Model ayni, fark GPU'dan (eleme kosusu 27B'yi de kaldiran daha guclu bir
karttaydi). Teslim planlamasinda sure rakami donanima bagli okunmali.

UYDURMA sutunu bu kosuda 0/7 cikti ama KULLANILMAMALI - o negatif kume
kirlenmis. Gecerli rakam taze kumeden: 15 soruda 13 red, 0 uydurma.

## Web katmani kuruldu (2026-08-10) - _web/

GEREKSINIM: sunum kullanicinin kendi makinesinde (GPU YOK), uretim kurumun
sunucusunda disariya servis. Kod ikisinde de AYNI; fark yalnizca .env'de.
  sunum   : LLM_ARKA=ollama,       CPU,  onbellek acik,  yalniz localhost
  uretim  : LLM_ARKA=transformers, GPU,  onbellek kapali, dis erisim

YEREL ORTAM: node v24.13.1, npm 11.8.0 var. Ollama YOK (kurulmasi gerek).
C: 30 GB bos (94% dolu), D: 56 GB bos -> Ollama modeli D:'ye alinmali
(setx OLLAMA_MODELS "D:\ollama"), model 4,7 GB.

DOSYALAR
  _web/backend/app.py          FastAPI servisi
  _web/backend/requirements.txt
  _web/backend/.env.ornek      iki senaryo yan yana, yorumla acilip kapaniyor
  _web/frontend/               Vite + React 18 (npm run build DOGRULANDI)
  _web/KURULUM.md              kurulum, calistirma, uretime tasima, sorun giderme

TASARIM KARARLARI
1. TEK ISCI ZORUNLU (uvicorn --workers 1). Qdrant gomulu modda depo klasorunu
   isletim sistemi kilidiyle tutuyor. Es zamanlilik gerekirse Qdrant sunucu
   moduna gecilir; yalnizca qdrant_index.ac() degisir, kalan kod ayni.
2. MODEL BIR KEZ YUKLENIR (lifespan). BGE-M3 ~2,3 GB; her istekte yuklemek
   30 saniye eklerdi.
3. ONBELLEK. Cozumleme acgozlu oldugu icin ayni soru ayni cevabi veriyor;
   sunum sirasinda beklememek icin cevaplar _work/onbellek.json'a yaziliyor.
   Anahtara model ve esikler de giriyor - yapilandirma degisince eski cevabi
   dondurmek degisikligi gormemek olurdu.
   ONBELLEKTEN GELEN CEVAP ARAYUZDE ISARETLENIYOR. Klinik bir sistemde "bu
   cevap simdi mi uretildi" sorusunun cevabi gizlenemez.
4. GUVEN NESNESI OLDUGU GIBI ARAYUZE GIDIYOR: hangi kapi kapatti, hangi cumle
   dayanaksiz, atif onarildi mi. Saklamak sistemi oldugundan emin gostermek
   olurdu.
5. ATIFLAR TIKLANABILIR, tam chunk metnini aciyor (/api/kaynak/{chunk_id}).
   Ozetlenmis kaynak dogrulanamayan kaynaktir.
6. Baglama giren ama ATIF VERILMEYEN kaynaklar da listeleniyor (soluk). Haksiz
   reddetme ile gercek bilgi yoklugunu ayirt etmenin tek yolu bu.

PIPELINE'DA IKI KUCUK DUZELTME (Ollama arka ucu ilk kez kullaniliyor)
  temperature 0,1 -> 0 ve num_predict=500: transformers arka ucuyla
  (do_sample=False) ayni davranmasi ve onbellegin anlamli olmasi icin.
  <think> ayiklama Ollama yolunda da devreye alindi.
Bu degisiklikler hicbir olcumu etkilemiyor: butun olcumler transformers
arka uucuyla yapildi.

BILINCLI EKSIK: kimlik dogrulama yok. Sunum icin gereksiz, disariya acilirken
kurumun kimlik katmani onune konmali. Sunumda da boyle soylenmeli.

## Web kurulumu - yerel ortam sorunlari ve iki bulgu (2026-08-10)

KURULUM: sanal ortam KURULMADI. Sistem Python'unda (3.14.3) torch 2.11+cpu,
numpy, fastapi, uvicorn, dotenv zaten vardi. Yeni venv torch'u sifirdan
indirtirdi (~2,5 GB) ve kullanicinin ilk denemesi muhtemelen orada takildi.
Kurulan: sentence-transformers 5.7.0, qdrant-client 1.19.0.

PROTOBUF TUZAGI: qdrant-client, protobuf'un C++ hizlandiricisini yuklemeye
calisiyor; protobuf 4.25'in eklentisi Python 3.14 ile uyumsuz:
  TypeError: Metaclasses with custom tp_new are not supported
Hata PAKET KURULURKEN DEGIL ILK SORGUDA cikiyor. protobuf 7.35.1'e yukseltince
duzeldi. PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python ise ISE YARAMIYOR -
hata, eklentiyi yoklama sirasinda cikiyor, kullanma sirasinda degil.

YEREL DOGRULAMA (dil modeli olmadan):
  qdrant acilis 6,4 sn | BGE-M3 yukleme 79 sn | sorgu 2,6-4,8 sn
Arama katmani GPU'suz makinede sorunsuz.

BULGU 1 - BAGLAM_PARCA UYUMSUZLUGU (duzeltildi)
Uretim 5 parca kullaniyordu, oysa BUTUN olcumler k=4 ile yapildi. Alan
kapisinin hastalik-etiketi orani secilen parca sayisina bagli oldugu icin bu
sessiz bir fark yaratirdi: raporladigimiz rakamlar gosterdigimiz sistemi tarif
etmezdi. BAGLAM_PARCA 5 -> 4.

BULGU 2 - TURKCE KARAKTERSIZ YAZIM ALAN KAPISINI ASIYOR (acik)
  "Akut miyeloid lösemide 7+3 indüksiyon rejimi nasıl uygulanır?"
      hastalik orani 0,25 -> kapi DURDURUYOR (dogru)
  "Akut miyeloid losemide 7+3 indüksiyon nasil uygulanir?"
      hastalik orani 0,75 -> kapi GECIRIYOR (yanlis)
Ayni soru, yalnizca sapkasiz yazilmis. Gomme vektoru degisiyor, farkli
chunk'lar geliyor, hastalik etiketi orani esigi asiyor.
ONEMLI: hekimler Turkce karakter kullanmadan yazar. Bu gercek bir acik.
Olculen 13/15 reddetme orani, sorularin duzgun yazildigi varsayimina dayaniyor.
Cozum secenekleri (henuz uygulanmadi): sorguyu sapkali-sapkasiz iki varyantla
aramak ve daha yuksek hastalik oranini almak; ya da varlik sozluklerini
sapkasiz eslesmeye acmak (ilac adlari icin zaten calisiyor, hastalik adlari
icin degil). Sunum oncesi karar verilmeli, en azindan bilinen eksik olarak
yazilmali.

## Web katmani AYAGA KALKTI (2026-08-10) - ve iki bulgu

DURUM: Ollama kurulu ve calisiyor (D:\ollama, qwen2.5:7b 4,7 GB), FastAPI
127.0.0.1:8000, Vite 5173. Uctan uca gercek cevap alindi.

KRITIK SORUN - SURE: CPU'da bir cevap 320-376 SANIYE. Sunumda canli soru
sormak mumkun degil. Olcumlerdeki 11-27 sn rakamlari GPU'luydu.
Cozum: demo sorulari onbellege isitiliyor (cevaplar deterministik).
Onbellekten gelen cevap arayuzde rozetle isaretleniyor.
Secenekler (karar bekliyor): (a) yalniz onbellek, (b) qwen2.5:3b - ~2,5 kat
hizli ama olculen sistemden farkli, (c) num_predict 500->300 ve k 4->3,
kabaca yariya iner ama yine olculen yapilandirmadan sapar, (d) sunum icin
GPU'lu makine.

BULGU 3 - CHUNK_ID TEKRARI (yeni)
chunks.json 14.532 satir, ama benzersiz chunk_id 13.857. 269 id tekrarli;
bir id 75 kez geciyor. Tekrarlar birebir ayni icerik (ornek:
nccn__jnccn-article-e260001 icinde ayni bolum defalarca).
ETKI: chunk_id ile sozluk kuran her yer (web /api/kaynak, answer_eval
chunk_haritasi) tekrarlari eziyor - 675 satir sozlukte gorunmuyor.
Qdrant tarafi ETKILENMIYOR: nokta id'si satir numarasi, hepsi indeksli.
Olcumler de bu ayni sozlugu kullandigi icin tutarli, ama chunk_id'nin
benzersiz OLMADIGI kayda gecmeli - ileride birincil anahtar sayilmamali.

BULGU 4 - KAYNAK METINDE HTML KALINTISI
Cevaplarda "20 mg/m<sup>2</sup>" gibi etiketler goruluyor. Kaynak Markdown'a
cevrilmis PDF ve model dozu oldugu gibi aktariyor - ki dogru davranis.
Temizlik GORUNTULEME katmaninda yapildi (App.jsx sadelestir()); cevap metnine
dokunulmadi ki olculen sey ile gosterilen sey ayni kalsin.

## KARAR: her sey yerelde (2026-08-10)

Sunum kullanicinin dizustunde, Colab yok, kucuk modele inilmiyor. Bekleme
kabul edildi ("200 sn civari bekliyoruz ve bu sorun degil").

OLCULEN SURELER (GTX 1650 4 GB, qwen2.5:7b, ollama ps = 50%/50% CPU/GPU):
  onbellekteki soru            aninda
  arsiv disi soru (alan kapisi) ~1 sn   <- model hic cagrilmiyor
  kisa cevap                   60-130 sn
  uzun cevap (doz semasi)      200-380 sn

DEGERLENDIRILEN VE BIRAKILAN IKI SECENEK
1. Colab'a tunel (T4, 10-30 sn). Altyapisi yazildi ve calisir durumda
   (_work/colab/ollama_sunucu.ipynb + pipeline.llm_kur icinde OLLAMA_URL
   destegi), ama KULLANILMIYOR - kullanici yerel istedi. Kod kaliyor: zararsiz,
   varsayilani localhost.
2. qwen2.5:3b (karta tam sigar, ~10 kat hizli). BIRAKILDI cunku butun olcumler
   7B ile yapildi; kucuk modele inmek sunumda GOSTERILEN sistemi OLCULEN
   sistemden ayirirdi. Bu, projenin bastan beri kacindigi hatanin ta kendisi.

Bu karar aslinda savunulabilir bir tercih: bekleme suresi pahasina, raporlanan
her rakam demoda kosan sistemi tarif ediyor.

SISTEM DURUMU: backend 127.0.0.1:8000 ayakta, arayuz 5173 ayakta, 6 cevap
onbellekte (5 demo sorusu + karfilzomib).
