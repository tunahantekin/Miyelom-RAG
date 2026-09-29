# Proje Log - Multipl Miyelom Karar-Destek Arsivi

Append-only. Her satir `_scripts/plog.py` ile eklenir.

| Zaman | Faz | Olay | Detay |
|---|---|---|---|
| 2026-08-04 11:34:59 | kurulum | Proje baslatildi - 3 katmanli miyelom karar-destek arsivi | Layer1 klinik / Layer2 ruhsat / Layer3 geri odeme |
| 2026-08-04 11:34:59 | kaynak-toplama | Mevcut 12 belge envanteri cikarildi | NCCN v5.2026, ESMO, SUT, EK-4 serisi, TITCK ruhsat listesi, Orange Book |
| 2026-08-04 11:34:59 | kaynak-toplama | EMA EPAR Product Information indirildi | 17/17 basarili - ema.europa.eu |
| 2026-08-04 11:34:59 | kaynak-toplama | FDA Prescribing Information indirildi | 18/18 basarili - DailyMed/NLM (.gov) |
| 2026-08-04 11:34:59 | kaynak-toplama | PubMed/PMC meta-analizleri indirildi | 5 adet - Europe PMC render (PMC dogrudan PDF engelli) |
| 2026-08-04 11:34:59 | kaynak-toplama | NCI PDQ Health Professional surumu PDF'e donusturuldu | cancer.gov HTML -> reportlab, 55 sayfa |
| 2026-08-04 11:34:59 | kaynak-toplama | TITCK KUB/KT servisi cozuldu ve Turkce KUB'ler indirildi | 108 adet - Laravel CSRF token + DataTables POST |
| 2026-08-04 11:34:59 | kaynak-toplama | ASCO kilavuzu ALINAMADI | ascopubs.org Cloudflare 403; manuel indirme gerekiyor (JCO-26-01139) |
| 2026-08-04 11:34:59 | analiz | NCCN algoritma sayfalari dogrulandi | Figure 1-9 = MYEL-1/4/5/B/F/G, vektorel gomulu; duz metin cikariminda kayboluyor |
| 2026-08-04 11:34:59 | yapilandirma | Klasor yapisi katman bazli yeniden duzenlendi | 161 dosya tasindi -> layer1_clinical / layer2_regulatory / layer3_reimbursement |
| 2026-08-04 11:34:59 | parse | Parser bake-off icin izole venv kuruldu | _env/parse - ana ortamin torch 2.11'ine dokunulmadi |
| 2026-08-04 11:35:00 | katalog | Data Catalog uretimi basladi |  |
| 2026-08-04 11:35:03 | katalog | TITCK KUB tarihleri cekildi | 108 kayit |
| 2026-08-04 11:35:16 | katalog | Data Catalog uretildi | 161 belge, 113 tanesinde tarih -> DATA_CATALOG.csv + .md |
| 2026-08-04 11:42:04 | parse-bakeoff | docling calistiriliyor | nccn_myeloma_v5_2026.pdf |
| 2026-08-04 11:49:37 | parse-bakeoff | docling HATA | ConversionError: Conversion failed for: nccn_myeloma_v5_2026.pdf with status: failure. Errors: InvalidCxxCompiler: Compiler: cl is not found.  Set TORCHDYNAMO_VERBOSE=1 for the internal stack trace (p |
| 2026-08-04 11:50:20 | parse-bakeoff | docling calistiriliyor | nccn_myeloma_v5_2026.pdf |
| 2026-08-04 11:50:29 | parse-bakeoff | Docling ilk denemede basarisiz | torch.compile MSVC 'cl' arayip dustu; TORCHDYNAMO_DISABLE=1 ile yeniden calistirildi |
| 2026-08-04 11:51:17 | parse-bakeoff | docling bitti | 57.1sn, 180295 krk, 80 baslik, 19 tablo satiri, 9 MYEL kodu -> C:\Users\Tunahan\Desktop\myeloma\_work\parse_bakeoff\output\docling\nccn.md |
| 2026-08-04 11:51:17 | parse-bakeoff | marker calistiriliyor | nccn_myeloma_v5_2026.pdf |
| 2026-08-04 11:51:17 | parse-bakeoff | marker HATA | ModuleNotFoundError: No module named 'marker' |
| 2026-08-04 11:51:17 | parse-bakeoff | unstructured calistiriliyor | nccn_myeloma_v5_2026.pdf |
| 2026-08-04 11:53:32 | parse-bakeoff | unstructured HATA | TesseractNotFoundError: tesseract is not installed or it's not in your PATH. See README file for more information. |
| 2026-08-04 12:00:44 | parse-bakeoff | Bake-off ilk tur sonuclari | docling BASARILI 57sn; marker wheel build hatasi (py3.14+MSVC yok); unstructured tesseract binary yok; llamaparse API anahtari yok |
| 2026-08-04 12:21:27 | katalog | Data Catalog uretimi basladi |  |
| 2026-08-04 12:21:33 | katalog | TITCK KUB tarihleri cekildi | 108 kayit |
| 2026-08-04 12:21:45 | kaynak-toplama | ASCO Living Guideline v2026.1.1 arsive eklendi | kullanici manuel indirdi -> layer1_clinical/asco/; katalog yenilendi |
| 2026-08-04 12:21:45 | kaynak-toplama | Gercek NCCN kilavuzu alinamadi | nccn.org/professionals/physician_gls/pdf/myeloma.pdf login sayfasi donuyor (HTML, 79KB); uyelik gerekli |
| 2026-08-04 12:33:29 | parse-bakeoff | unstructured calistiriliyor | nccn_myeloma_v5_2026.pdf |
| 2026-08-04 12:33:30 | katalog | Data Catalog uretimi basladi |  |
| 2026-08-04 12:33:34 | katalog | TITCK KUB tarihleri cekildi | 108 kayit |
| 2026-08-04 12:33:46 | katalog | Data Catalog uretildi | 163 belge, 114 tanesinde tarih -> DATA_CATALOG.csv + .md |
| 2026-08-04 12:37:33 | parse-bakeoff | unstructured bitti | 244.0sn, 187471 krk, 72 baslik, 0 tablo satiri, 15 MYEL kodu -> C:\Users\Tunahan\Desktop\myeloma\_work\parse_bakeoff\output\unstructured\nccn.md |
| 2026-08-04 12:38:21 | parse-bakeoff | Unstructured akis semalarini OCR ile kurtardi | 244sn, 15/18 MYEL kodu, sema icerigi HTML tablo olarak cikti; docling ayni semalari <!-- image --> diye atmisti |
| 2026-08-04 12:39:01 | parse-bakeoff | llamaparse calistiriliyor | nccn_myeloma_v5_2026.pdf |
| 2026-08-04 12:39:57 | parse-bakeoff | llamaparse bitti | 55.7sn, 133384 krk, 79 baslik, 40 tablo satiri, 14 MYEL kodu -> C:\Users\Tunahan\Desktop\myeloma\_work\parse_bakeoff\output\llamaparse\nccn.md |
| 2026-08-04 12:40:56 | parse-bakeoff | marker calistiriliyor | nccn_myeloma_v5_2026.pdf |
| 2026-08-04 12:41:19 | parse-bakeoff | LlamaParse basarili - semalari temiz markdown tabloya cevirdi | 55.7sn, 14 MYEL kodu, 40 tablo satiri, ust simge ve madde isaretleri korunmus, OCR gurultusu yok |
| 2026-08-04 12:41:19 | parse-bakeoff | Marker py3.10 venv'de kuruldu ve calistirildi | _env/marker310 - py3.14'te wheel derlemesi cokmustu |
| 2026-08-04 12:45:08 | parse-bakeoff | marker HATA | SpawnError: docker run failed: failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine; check if the path is correct and if the daemon is running: open //./pipe/dockerDesktopL |
| 2026-08-04 12:45:56 | parse-bakeoff | Marker calistirilamadi - Docker daemon kapali | 251sn sonra SpawnError: docker run failed (dockerDesktopLinuxEngine npipe); Docker Desktop baslatilirsa tekrar denenebilir |
| 2026-08-04 12:45:56 | parse-bakeoff | Bake-off karari: birincil LlamaParse, ikincil Docling | LlamaParse semalari temiz markdown tabloya ceviriyor + dipnot yakalayan tek parser; Docling sema disi belgeler icin yerel/ucretsiz |
| 2026-08-04 13:06:08 | parse-bakeoff | marker calistiriliyor | nccn_myeloma_v5_2026.pdf |
| 2026-08-04 13:22:32 | parse-bakeoff | marker calistiriliyor | nccn_myeloma_v5_2026.pdf |
| 2026-08-04 13:23:22 | parse-bakeoff | marker calistiriliyor | nccn_myeloma_v5_2026.pdf |
| 2026-08-04 13:25:55 | parse-bakeoff | marker HATA | Timeout: The file lock 'C:\Users\Tunahan\.cache\datalab\surya\vllm_server.lock' could not be acquired. |
| 2026-08-04 13:33:31 | parse-bakeoff | marker calistiriliyor | nccn_myeloma_v5_2026.pdf |
| 2026-08-04 13:47:02 | parse-bakeoff | marker HATA | SpawnError: docker run failed: Unable to find image 'vllm/vllm-openai:v0.20.1' locally v0.20.1: Pulling from vllm/vllm-openai 69a63953ef53: Pulling fs layer 7004d81d8e4c: Pulling fs layer f0a83977e9b8 |
| 2026-08-04 13:47:18 | parse-bakeoff | marker calistiriliyor | nccn_myeloma_v5_2026.pdf |
| 2026-08-04 13:50:04 | parse-bakeoff | marker calistiriliyor | nccn_myeloma_v5_2026.pdf |
| 2026-08-04 13:52:39 | parse-bakeoff | marker HATA | Timeout: The file lock 'C:\Users\Tunahan\.cache\datalab\surya\vllm_server.lock' could not be acquired. |
| 2026-08-04 14:02:29 | parse-bakeoff | marker HATA | SpawnError: docker run failed: Unable to find image 'vllm/vllm-openai:v0.20.1' locally v0.20.1: Pulling from vllm/vllm-openai 7004d81d8e4c: Pulling fs layer af34a897ee01: Pulling fs layer 95d070e75511 |
| 2026-08-04 14:03:52 | parse-bakeoff | Parse bake-off adimi kapatildi | Kazanan: LlamaParse (birincil), Docling (ikincil, sema disi belgeler). Marker test edilemedi - py3.14 wheel + Docker + dosya kilidi. Unstructured elendi - OCR gurultusu, 4x yavas. |
| 2026-08-04 14:40:00 | clinical-recall | clinical recall: docling | 20/43 madde (recall 0.465), kritik 14/35, pencere 9/43 |
| 2026-08-04 14:40:00 | clinical-recall | clinical recall: llamaparse | 40/43 madde (recall 0.93), kritik 33/35, pencere 40/43 |
| 2026-08-04 14:40:00 | clinical-recall | clinical recall: unstructured | 38/43 madde (recall 0.884), kritik 30/35, pencere 33/43 |
| 2026-08-04 14:43:30 | clinical-recall | clinical recall: docling | belge 20/43 (recall 0.465), figur 5/43 (recall 0.116), figur-kritik 4/35 |
| 2026-08-04 14:43:30 | clinical-recall | clinical recall: llamaparse | belge 40/43 (recall 0.93), figur 38/43 (recall 0.884), figur-kritik 31/35 |
| 2026-08-04 14:43:30 | clinical-recall | clinical recall: unstructured | belge 38/43 (recall 0.884), figur 31/43 (recall 0.721), figur-kritik 26/35 |
| 2026-08-04 14:44:05 | parse-full | llamaparse 141 sayfa basladi | layer1_clinical/nccn/myeloma.pdf |
| 2026-08-04 14:44:09 | katalog | Data Catalog uretimi basladi |  |
| 2026-08-04 14:44:12 | katalog | TITCK KUB tarihleri cekildi | 108 kayit |
| 2026-08-04 14:44:29 | katalog | Data Catalog uretildi | 163 belge, 115 tanesinde tarih -> DATA_CATALOG.csv + .md |
| 2026-08-04 14:45:16 | parse-full | llamaparse 141 sayfa bitti | 70.6sn, 492388 karakter, 141 parca |
| 2026-08-04 14:56:22 | clinical-recall | clinical recall: nccn141_llamaparse | belge 42/43 (recall 0.977), figur 20/43 (recall 0.465), figur-kritik 15/35 |
| 2026-08-04 15:04:04 | clinical-recall | clinical recall: docling | belge 20/43 (recall 0.465), figur 6/43 (recall 0.14), figur-kritik 4/35 |
| 2026-08-04 15:04:04 | clinical-recall | clinical recall: llamaparse | belge 40/43 (recall 0.93), figur 23/43 (recall 0.535), figur-kritik 17/35 |
| 2026-08-04 15:04:04 | clinical-recall | clinical recall: unstructured | belge 38/43 (recall 0.884), figur 8/43 (recall 0.186), figur-kritik 4/35 |
| 2026-08-04 15:04:04 | clinical-recall | clinical recall: nccn141_llamaparse | belge 42/43 (recall 0.977), figur 19/43 (recall 0.442), figur-kritik 14/35 |
| 2026-08-04 15:05:21 | clinical-recall | clinical recall: docling | belge 20/43 (recall 0.465), figur 7/43 (recall 0.163), figur-kritik 5/35 |
| 2026-08-04 15:05:21 | clinical-recall | clinical recall: llamaparse | belge 40/43 (recall 0.93), figur 39/43 (recall 0.907), figur-kritik 32/35 |
| 2026-08-04 15:05:21 | clinical-recall | clinical recall: unstructured | belge 38/43 (recall 0.884), figur 33/43 (recall 0.767), figur-kritik 27/35 |
| 2026-08-04 15:05:21 | clinical-recall | clinical recall: nccn141_llamaparse | belge 42/43 (recall 0.977), figur 37/43 (recall 0.86), figur-kritik 29/35 |
| 2026-08-04 15:06:29 | clinical-recall | MYEL-1 clinical recall olculdu | Ground truth 43 madde (35 kritik), sayfa PNG render + gozle cikarildi. Makale PDF: docling belge 0.47/blok 0.16, llamaparse 0.93/0.91, unstructured 0.88/0.77. Gercek 141 sayfalik kilavuz (llamaparse): belge 0.98, blok 0.86; MYEL-1 sayfasinda CLINICAL FINDINGS dal sutunu tamamen kayip, dipnot harfleri c'den itibaren kaymis, dipnot d ve i sayfada yok. |
| 2026-08-04 15:06:29 | parse-full | 141 sayfalik NCCN kilavuzu LlamaParse ile parse edildi | 70.6 sn, 492388 karakter -> _work/parse_full/nccn141.md; DATA_CATALOG yeniden uretildi (163 belge, 115 tarihli) |
| 2026-08-04 15:50:56 | clinical-recall | clinical recall: elle_myeloma | belge 43/43 (recall 1.0), figur 43/43 (recall 1.0), figur-kritik 35/35 |
| 2026-08-04 15:50:56 | clinical-recall | clinical recall: elle_mmyeloma | belge 2/43 (recall 0.047), figur 1/43 (recall 0.023), figur-kritik 0/35 |
| 2026-08-04 15:50:56 | clinical-recall | clinical recall: llamaparse141 | belge 42/43 (recall 0.977), figur 37/43 (recall 0.86), figur-kritik 29/35 |
| 2026-08-04 16:19:42 | dogrulama | Elle hazirlanmis nccn_myeloma.md dogrulandi (MYEL-1/F/G) | MYEL-1: 43/43 clinical recall, dipnot harfleri ve ust simge baglantilari dogru, karar dallari tam. MYEL-F/G: 57 rejim capraz dogrulandi (LlamaParse 141 sayfa ciktisiyla), uydurma rejim YOK. 2 gercek eksik: Bortezomib/Liposomal Doxorubicin/Dexamethasone (category 1) ve Carfilzomib/Cyclophosphamide/Thalidomide/Dexamethasone. nccn_mmyeloma.md = NCCN Guidelines for Patients v4.2026, hasta brosuru, katman1'e uygun degil. |
| 2026-08-04 17:33:39 | dogrulama | structural validation | _work\parse_full\nccn141.md: ERROR 1, WARN 68, REVIEW 9 |
| 2026-08-04 17:33:39 | dogrulama | structural validation | layer1_clinical\nccn\nccn_myeloma_manual.md: ERROR 30, WARN 43, REVIEW 18 |
| 2026-08-04 17:39:23 | dogrulama | structural validation | _work\parse_full\nccn141.md: ERROR 1, WARN 4, REVIEW 9 |
| 2026-08-04 17:39:23 | dogrulama | structural validation | layer1_clinical\nccn\nccn_myeloma_manual.md: ERROR 30, WARN 97, REVIEW 18 |
| 2026-08-04 17:39:59 | dogrulama | structural validation | _work\parse_full\nccn141.md: ERROR 1, WARN 4, REVIEW 9 |
| 2026-08-04 17:39:59 | dogrulama | structural validation | layer1_clinical\nccn\nccn_myeloma_manual.md: ERROR 30, WARN 83, REVIEW 32 |
| 2026-08-04 17:40:14 | dogrulama | Structural Validation katmani kuruldu | _scripts/structural_validation.py: dipnot butunlugu (bolum-kapsamli), capraz atif, tablo, hiyerarsi kokusu; ERROR/WARN/REVIEW. Manual dosya: 30 ERROR (27 missing_footnote, 2 broken_link, 1 table_no_separator), 83 WARN, 32 REVIEW. LlamaParse 141sf: 1 ERROR, 4 WARN, 9 REVIEW. Ayrica MYEL-G 4of5'te sutun karismasi tespit edildi (Useful/Other Recommended listeleri birbirine gecmis). |
| 2026-08-04 17:47:08 | parse-batch | docling toplu donusum basladi | 159 PDF |
| 2026-08-04 17:50:30 | parse-batch | docling toplu donusum basladi | 159 PDF |
| 2026-08-04 17:51:57 | parse-batch | docling toplu donusum basladi | 4 PDF |
| 2026-08-04 17:52:53 | parse-batch | docling toplu donusum bitti | ok=1 hata=2 atla=1 |
| 2026-08-04 17:53:23 | parse-batch | docling toplu donusum basladi | 159 PDF |
| 2026-08-04 17:55:10 | duzeltme | MYEL-G 4of5 duzeltildi | PDF sayfa goruntusunden yeniden yazildi. 3 eksik rejim eklendi (Bortezomib/Liposomal Doxorubicin/Dex cat1, KCTd, XKd), sayfaya ait olmayan 5 satir kaldirildi (bendamustin x3, High-dose cyclophosphamide, Carfilzomib weekly). MYEL-G 5of5 kontrol edildi - PDF ile birebir, degisiklik gerekmedi. |
| 2026-08-04 17:55:34 | dogrulama | structural validation | layer1_clinical\nccn\nccn_myeloma_manual.md: ERROR 30, WARN 83, REVIEW 32 |
| 2026-08-04 18:06:11 | parse-batch | docling ilerleme | 25/159 ok=19 hata=4 atla=2 |
| 2026-08-04 18:19:26 | parse-batch | docling ilerleme | 50/159 ok=43 hata=5 atla=2 |
| 2026-08-04 18:30:22 | parse-batch | docling ilerleme | 75/159 ok=54 hata=19 atla=2 |
| 2026-08-04 18:35:50 | parse-batch | docling ilerleme | 100/159 ok=54 hata=44 atla=2 |
| 2026-08-05 08:42:09 | parse-batch | docling toplu donusum basladi | 159 PDF |
| 2026-08-05 08:47:08 | parse-batch | docling ilerleme | 75/159 ok=19 hata=0 atla=56 |
| 2026-08-05 08:56:53 | parse-batch | docling ilerleme | 100/159 ok=44 hata=0 atla=56 |
| 2026-08-05 09:00:30 | parse-batch | docling ilerleme | 125/159 ok=66 hata=0 atla=59 |
| 2026-08-05 09:06:33 | parse-batch | docling ilerleme | 150/159 ok=91 hata=0 atla=59 |
| 2026-08-05 09:09:21 | parse-batch | docling toplu donusum bitti | ok=100 hata=0 atla=59 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer1_clinical__asco__banerjee-et-al-2026-treatment-of-multiple-myeloma-asco-living-guideline-version-2026-1-1.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer1_clinical__esmo__esmo.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer1_clinical__nccn__jnccn-article-e260001.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer1_clinical__nccn__myeloma.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer1_clinical__nci_pdq__NCI_PDQ_myeloma_HP_2026.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_dara_backbone_regimens.md: ERROR 0, WARN 1, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_dara_quad_vs_triplet_2025.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_dara_transplant_ineligible_2025.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_daratumumab_efficacy_safety.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_quadruplet_TE_NDMM_2025.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_abecma_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_blenrep_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_carvykti_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_darzalex_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_elrexfio_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_empliciti_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_imnovid_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_kyprolis_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_lynozyfic_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_nexpovio_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_ninlaro_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_pepaxti_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_revlimid_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_sarclisa_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_talvey_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_tecvayli_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_velcade_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_ABECMA_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_CARVYKTI_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_DARZALEX_FASPRO_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_DARZALEX_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_ELREXFIO_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_EMPLICITI_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_KYPROLIS_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_LYNOZYFIC_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_NINLARO_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_POMALYST_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_REVLIMID_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_SARCLISA_ESCENA_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_SARCLISA_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_TALVEY_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_TECVAYLI_PI.md: ERROR 0, WARN 0, REVIEW 4 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_THALOMID_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_VELCADE_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_XPOVIO_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__orange_book__appendix_fda.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOMIB__BORCADE_3_5_MG_IV_SC_ENJEKSIYONLUK_ZELTI_HAZ_RLAMAK_IN_LIYOF_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOMIB__BORT_REL_1_MG_I_V_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOMIB__BORT_REL_3_5_MG_IV_SC_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOM_B__BORACTIB_3_5_MG_IV_SC_ENJEKSIYONLUK_ZELTI_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOM_B__B_EM_B_3_5_MG_IV_SC_ENJEKS_YONLUK_ZELT_N_TOZ_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOM_B__VELCADE_3_5_MG_IV_SC_ENJEKS_YONLUK_ZELT_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOM_B__VELTEZO_3_5_MG_IV_SC_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_100_MG_5_ML_NF_ZYONLUK_ZELTI_HAZ_RLAMAK_IN_KONSANTR_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_1800_MG_SC_ENJEKSIYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_400_MG_20_ML_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DENOSUMAB__PROL_A_60_MG_ML_SC_ENJEKSIYONLUK_ZELTI_EREN_KULLAN_MA_HAZ_R__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DENOSUMAB__XGEVA_120_MG_SC_ENJEKS_YONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ELRANATAMAB__ELREXFIO_44_MG_1_1_ML_ENJEKSIYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ELRANATAMAB__ELREXFIO_76_MG_1_9_ML_ENJEKSIYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__IKSAZOMIB_SITRAT__NINLARO_3_MG_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__IKSAZOMIB_SITRAT__NINLARO_4_MG_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__IKSAZOMIB__NINLARO_2_3_MG_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ISATUXIMAB__SARCLISA_100_MG_5_ML_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ISATUXIMAB__SARCLISA_500_MG_25_ML_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARFILZOMIB__KARFILIB_60_MG_I_V_ENJEKSIYONLUK_ZELTI_HAZ_RLAMAK_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARFILZOMIB__KARZOM_60_MG_IV_NF_ZYONLUK_ZELTI_HAZ_RLAMAK_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARFILZOMIB__KYPROL_S_10_MG_IV_INF_ZYONLUK_ZELTI_HAZ_RLAMAK_I_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARFILZOMIB__KYPROL_S_30_MG_IV_INF_ZYONLUK_ZELTI_HAZ_RLAMAK_I_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARF_LZOM_B__CAF_ZO_60_MG_I_V_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARF_LZOM_B__KYPROLIS_60_MG_IV_ENJEKS_YONLUK_ZELT_N_TOZ_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARF_LZOM_B__KYPROL_S_60_MG_IV_ENJEKS_YONLUK_ZELT_N_TOZ_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__KOMPL_A_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__KOMPL_A_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__KOMPL_A_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__KOMPL_A_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENATU_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENATU_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENATU_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENATU_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENOM_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENOM_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENOM_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__RELIV_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__RELIV_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__RELIV_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__RELIV_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__REVL_M_D_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__R_VEL_ME_20_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__R_VEL_ME_2_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__R_VEL_ME_7_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENAL_DOM_D__R_VEL_ME_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENAL_DOM_D__R_VEL_ME_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENAL_DOM_D__R_VEL_ME_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENAL_DOM_D__R_VEL_ME_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__MELFALAN_H_DROKLOR_R__ERIOLAN_50_MG_ENJEKSIYONLUK_NF_ZYONLUK_ZELTI_IN_LIYOFILIZE_T_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__MELFALAN__ALKERAN_2_MG_FILM_TABLET_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMALIDOMID__POMAVID_1_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMALIDOMID__POMAVID_2_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMALIDOMID__POMAVID_3_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMALIDOMID__POMAVID_4_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_1_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_2_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_3_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_4_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D___MNOV_D_1_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D___MNOV_D_2_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D___MNOV_D_3_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D___MNOV_D_4_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__SELINEKSOR__NEXPOVIO_20_MG_FILM_KAPLI_TABLET_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__TALIDOMIDE__THALIDOMIDE_BMS_50_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ACLASTA_5_MG_100_ML_IV_NF_ZYON_ZELTISI_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__BONZOLEN_4_MG_5_ML_I_V_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__KALIKSIR_4MG_5ML_I_V_NF_ZYONLUK_KONSANTRE_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__LUSIMA_5MG_100ML_IV_NF_ZYON_ZELTISI_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__OSTEOZOLEN_4_MG_5_ML_I_V_NFUZYON_IN_KONSANTRE_ZELTI_EREN_FLA_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZOLCURE_5_MG_100_ML_V_INF_ZYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZOLDR_A_4MG_5ML_IV_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZOLON_K_4_MG_5_ML_I_V_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZORONIC_4MG_5ML_IV_NF_ZYON_IN_KONSANTRE_ZELTI_EREN_FLAKON__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOH_DRAT__OSTEZOLEN_4MG_5ML_IV_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_SUSUZ_ZOLEDRON__ATAZOL_4_MG_5_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ACLASTA_5MG_100_ML_NF_ZYON_ZELTISI_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__BONEDRO_4MG_5ML_V_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN_FLAKO_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__CEM_X_5G_100ML_IV_NF_ZYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__RON_DRO_5_MG_100_ML_I_V_INF_ZYON_ZELTISI_I_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__VERTEBZOL_5_MG_100_ML_I_V_NF_ZYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOLEGEN_4_MG_5_ML_I_V_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN_F_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOLENAT_IV_4MG_5_ML_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN_FLA_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOLTONAR_5_MG_100_ML_V_INF_ZYON_ZELTISI_I_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOMEBON_4MG_5ML_INF_ZYON_I_IN_KONSANTRE_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__BONDREX_4MG_5_ML_IV_NF_ZYON_N_KONSANTRE_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__LAN_CZOL_5_MG_100_ML_IV_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__OSS_4_MG_5_ML_I_V_KONSANTRE_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__PLAZOL_4_MG_5_ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__RON_X_4_MG_5_ML_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLESTO_5_MG_100_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLKA_5MG_100ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLOPOROZ_5MG_100ML_V_NF_ZYON_N_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLTASTA_4MG_5ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ACLABON_5MG_100ML_NF_ZYON_ZELT_S_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__MULTIFLEX_ACLAVER_5_MG_100_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__XENDRO_5_MG_100_ML_IV_NF_ZYON_N_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ZOD_NAS_L_5_MG_100_ML_V_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ZOLTASTA_4MG_5ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__Zoledronik_Asit_Monohidrat__Metarzu_4_mg_5_ml_V_nf_zyon_in_Konsantre_zelti_eren_Flakon_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__Zoledronik_asit_monohidrat__Xolarex_5_mg_100_ml_IV_nf_zyonluk_zelti_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__ek4__EK-4-D.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__ek4__EK-4-E.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__ek4__EK-4-F.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__ek4__EK-4-G.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:10:26 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__sut__SUT.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:20:04 | dogrulama | structural validation | layer1_clinical\nccn\nccn_myeloma_manual.md: ERROR 30, WARN 83, REVIEW 32 |
| 2026-08-05 09:22:41 | parse-batch | docling toplu donusum basladi | 159 PDF |
| 2026-08-05 09:26:12 | parse-batch | docling ilerleme | 25/159 ok=16 hata=0 atla=9 |
| 2026-08-05 09:31:06 | parse-batch | docling ilerleme | 50/159 ok=40 hata=0 atla=10 |
| 2026-08-05 09:32:36 | parse-batch | docling toplu donusum bitti | ok=51 hata=0 atla=108 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer1_clinical__asco__banerjee-et-al-2026-treatment-of-multiple-myeloma-asco-living-guideline-version-2026-1-1.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer1_clinical__esmo__esmo.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer1_clinical__nccn__jnccn-article-e260001.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer1_clinical__nccn__myeloma.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer1_clinical__nci_pdq__NCI_PDQ_myeloma_HP_2026.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_dara_backbone_regimens.md: ERROR 0, WARN 1, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_dara_quad_vs_triplet_2025.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_dara_transplant_ineligible_2025.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_daratumumab_efficacy_safety.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_quadruplet_TE_NDMM_2025.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_abecma_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_blenrep_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_carvykti_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_darzalex_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_elrexfio_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_empliciti_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_imnovid_PI.md: ERROR 0, WARN 0, REVIEW 3 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_kyprolis_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_lynozyfic_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_nexpovio_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_ninlaro_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_pepaxti_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_revlimid_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_sarclisa_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_talvey_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_tecvayli_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_velcade_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_ABECMA_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_CARVYKTI_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_DARZALEX_FASPRO_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_DARZALEX_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_ELREXFIO_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_EMPLICITI_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_KYPROLIS_PI.md: ERROR 0, WARN 0, REVIEW 2 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_LYNOZYFIC_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_NINLARO_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_POMALYST_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_REVLIMID_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_SARCLISA_ESCENA_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_SARCLISA_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_TALVEY_PI.md: ERROR 0, WARN 0, REVIEW 5 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_TECVAYLI_PI.md: ERROR 0, WARN 0, REVIEW 5 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_THALOMID_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_VELCADE_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_XPOVIO_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__orange_book__appendix_fda.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOMIB__BORCADE_3_5_MG_IV_SC_ENJEKSIYONLUK_ZELTI_HAZ_RLAMAK_IN_LIYOF_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOMIB__BORT_REL_1_MG_I_V_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOMIB__BORT_REL_3_5_MG_IV_SC_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOM_B__BORACTIB_3_5_MG_IV_SC_ENJEKSIYONLUK_ZELTI_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOM_B__B_EM_B_3_5_MG_IV_SC_ENJEKS_YONLUK_ZELT_N_TOZ_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOM_B__VELCADE_3_5_MG_IV_SC_ENJEKS_YONLUK_ZELT_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOM_B__VELTEZO_3_5_MG_IV_SC_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_100_MG_5_ML_NF_ZYONLUK_ZELTI_HAZ_RLAMAK_IN_KONSANTR_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_1800_MG_SC_ENJEKSIYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_400_MG_20_ML_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DENOSUMAB__PROL_A_60_MG_ML_SC_ENJEKSIYONLUK_ZELTI_EREN_KULLAN_MA_HAZ_R__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DENOSUMAB__XGEVA_120_MG_SC_ENJEKS_YONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ELRANATAMAB__ELREXFIO_44_MG_1_1_ML_ENJEKSIYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ELRANATAMAB__ELREXFIO_76_MG_1_9_ML_ENJEKSIYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__IKSAZOMIB_SITRAT__NINLARO_3_MG_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__IKSAZOMIB_SITRAT__NINLARO_4_MG_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__IKSAZOMIB__NINLARO_2_3_MG_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ISATUXIMAB__SARCLISA_100_MG_5_ML_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ISATUXIMAB__SARCLISA_500_MG_25_ML_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARFILZOMIB__KARFILIB_60_MG_I_V_ENJEKSIYONLUK_ZELTI_HAZ_RLAMAK_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARFILZOMIB__KARZOM_60_MG_IV_NF_ZYONLUK_ZELTI_HAZ_RLAMAK_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARFILZOMIB__KYPROL_S_10_MG_IV_INF_ZYONLUK_ZELTI_HAZ_RLAMAK_I_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARFILZOMIB__KYPROL_S_30_MG_IV_INF_ZYONLUK_ZELTI_HAZ_RLAMAK_I_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARF_LZOM_B__CAF_ZO_60_MG_I_V_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARF_LZOM_B__KYPROLIS_60_MG_IV_ENJEKS_YONLUK_ZELT_N_TOZ_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARF_LZOM_B__KYPROL_S_60_MG_IV_ENJEKS_YONLUK_ZELT_N_TOZ_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__KOMPL_A_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__KOMPL_A_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__KOMPL_A_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__KOMPL_A_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENATU_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENATU_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENATU_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENATU_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENOM_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENOM_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENOM_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__RELIV_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__RELIV_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__RELIV_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__RELIV_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__REVL_M_D_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__R_VEL_ME_20_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__R_VEL_ME_2_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__R_VEL_ME_7_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENAL_DOM_D__R_VEL_ME_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENAL_DOM_D__R_VEL_ME_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENAL_DOM_D__R_VEL_ME_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENAL_DOM_D__R_VEL_ME_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__MELFALAN_H_DROKLOR_R__ERIOLAN_50_MG_ENJEKSIYONLUK_NF_ZYONLUK_ZELTI_IN_LIYOFILIZE_T_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__MELFALAN__ALKERAN_2_MG_FILM_TABLET_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMALIDOMID__POMAVID_1_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMALIDOMID__POMAVID_2_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMALIDOMID__POMAVID_3_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMALIDOMID__POMAVID_4_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_1_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_2_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_3_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_4_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D___MNOV_D_1_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D___MNOV_D_2_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D___MNOV_D_3_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D___MNOV_D_4_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__SELINEKSOR__NEXPOVIO_20_MG_FILM_KAPLI_TABLET_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__TALIDOMIDE__THALIDOMIDE_BMS_50_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ACLASTA_5_MG_100_ML_IV_NF_ZYON_ZELTISI_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__BONZOLEN_4_MG_5_ML_I_V_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__KALIKSIR_4MG_5ML_I_V_NF_ZYONLUK_KONSANTRE_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__LUSIMA_5MG_100ML_IV_NF_ZYON_ZELTISI_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__OSTEOZOLEN_4_MG_5_ML_I_V_NFUZYON_IN_KONSANTRE_ZELTI_EREN_FLA_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZOLCURE_5_MG_100_ML_V_INF_ZYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZOLDR_A_4MG_5ML_IV_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZOLON_K_4_MG_5_ML_I_V_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZORONIC_4MG_5ML_IV_NF_ZYON_IN_KONSANTRE_ZELTI_EREN_FLAKON__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOH_DRAT__OSTEZOLEN_4MG_5ML_IV_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_SUSUZ_ZOLEDRON__ATAZOL_4_MG_5_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ACLASTA_5MG_100_ML_NF_ZYON_ZELTISI_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__BONEDRO_4MG_5ML_V_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN_FLAKO_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__CEM_X_5G_100ML_IV_NF_ZYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__RON_DRO_5_MG_100_ML_I_V_INF_ZYON_ZELTISI_I_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__VERTEBZOL_5_MG_100_ML_I_V_NF_ZYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOLEGEN_4_MG_5_ML_I_V_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN_F_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOLENAT_IV_4MG_5_ML_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN_FLA_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOLTONAR_5_MG_100_ML_V_INF_ZYON_ZELTISI_I_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOMEBON_4MG_5ML_INF_ZYON_I_IN_KONSANTRE_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__BONDREX_4MG_5_ML_IV_NF_ZYON_N_KONSANTRE_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__LAN_CZOL_5_MG_100_ML_IV_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__OSS_4_MG_5_ML_I_V_KONSANTRE_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__PLAZOL_4_MG_5_ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__RON_X_4_MG_5_ML_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLESTO_5_MG_100_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLKA_5MG_100ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLOPOROZ_5MG_100ML_V_NF_ZYON_N_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLTASTA_4MG_5ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ACLABON_5MG_100ML_NF_ZYON_ZELT_S_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__MULTIFLEX_ACLAVER_5_MG_100_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__XENDRO_5_MG_100_ML_IV_NF_ZYON_N_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ZOD_NAS_L_5_MG_100_ML_V_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ZOLTASTA_4MG_5ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__Zoledronik_Asit_Monohidrat__Metarzu_4_mg_5_ml_V_nf_zyon_in_Konsantre_zelti_eren_Flakon_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__Zoledronik_asit_monohidrat__Xolarex_5_mg_100_ml_IV_nf_zyonluk_zelti_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__ek4__EK-4-D.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__ek4__EK-4-E.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__ek4__EK-4-F.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__ek4__EK-4-G.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:34:09 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__sut__SUT.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer1_clinical__asco__banerjee-et-al-2026-treatment-of-multiple-myeloma-asco-living-guideline-version-2026-1-1.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer1_clinical__esmo__esmo.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer1_clinical__nccn__jnccn-article-e260001.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer1_clinical__nccn__myeloma.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer1_clinical__nci_pdq__NCI_PDQ_myeloma_HP_2026.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_dara_backbone_regimens.md: ERROR 0, WARN 1, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_dara_quad_vs_triplet_2025.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_dara_transplant_ineligible_2025.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_daratumumab_efficacy_safety.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_quadruplet_TE_NDMM_2025.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_abecma_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_blenrep_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_carvykti_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_darzalex_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_elrexfio_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_empliciti_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_imnovid_PI.md: ERROR 0, WARN 0, REVIEW 3 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_kyprolis_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_lynozyfic_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_nexpovio_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_ninlaro_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_pepaxti_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_revlimid_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_sarclisa_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_talvey_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_tecvayli_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_velcade_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_ABECMA_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_CARVYKTI_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_DARZALEX_FASPRO_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_DARZALEX_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_ELREXFIO_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_EMPLICITI_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_KYPROLIS_PI.md: ERROR 0, WARN 0, REVIEW 2 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_LYNOZYFIC_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_NINLARO_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_POMALYST_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_REVLIMID_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_SARCLISA_ESCENA_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_SARCLISA_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_TALVEY_PI.md: ERROR 0, WARN 0, REVIEW 5 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_TECVAYLI_PI.md: ERROR 0, WARN 0, REVIEW 5 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_THALOMID_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_VELCADE_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_XPOVIO_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__orange_book__appendix_fda.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOMIB__BORCADE_3_5_MG_IV_SC_ENJEKSIYONLUK_ZELTI_HAZ_RLAMAK_IN_LIYOF_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOMIB__BORT_REL_1_MG_I_V_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOMIB__BORT_REL_3_5_MG_IV_SC_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOM_B__BORACTIB_3_5_MG_IV_SC_ENJEKSIYONLUK_ZELTI_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOM_B__B_EM_B_3_5_MG_IV_SC_ENJEKS_YONLUK_ZELT_N_TOZ_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOM_B__VELCADE_3_5_MG_IV_SC_ENJEKS_YONLUK_ZELT_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOM_B__VELTEZO_3_5_MG_IV_SC_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_100_MG_5_ML_NF_ZYONLUK_ZELTI_HAZ_RLAMAK_IN_KONSANTR_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_1800_MG_SC_ENJEKSIYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_400_MG_20_ML_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DENOSUMAB__PROL_A_60_MG_ML_SC_ENJEKSIYONLUK_ZELTI_EREN_KULLAN_MA_HAZ_R__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DENOSUMAB__XGEVA_120_MG_SC_ENJEKS_YONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ELRANATAMAB__ELREXFIO_44_MG_1_1_ML_ENJEKSIYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ELRANATAMAB__ELREXFIO_76_MG_1_9_ML_ENJEKSIYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__IKSAZOMIB_SITRAT__NINLARO_3_MG_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__IKSAZOMIB_SITRAT__NINLARO_4_MG_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__IKSAZOMIB__NINLARO_2_3_MG_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ISATUXIMAB__SARCLISA_100_MG_5_ML_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ISATUXIMAB__SARCLISA_500_MG_25_ML_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARFILZOMIB__KARFILIB_60_MG_I_V_ENJEKSIYONLUK_ZELTI_HAZ_RLAMAK_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARFILZOMIB__KARZOM_60_MG_IV_NF_ZYONLUK_ZELTI_HAZ_RLAMAK_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARFILZOMIB__KYPROL_S_10_MG_IV_INF_ZYONLUK_ZELTI_HAZ_RLAMAK_I_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARFILZOMIB__KYPROL_S_30_MG_IV_INF_ZYONLUK_ZELTI_HAZ_RLAMAK_I_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARF_LZOM_B__CAF_ZO_60_MG_I_V_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARF_LZOM_B__KYPROLIS_60_MG_IV_ENJEKS_YONLUK_ZELT_N_TOZ_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARF_LZOM_B__KYPROL_S_60_MG_IV_ENJEKS_YONLUK_ZELT_N_TOZ_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__KOMPL_A_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__KOMPL_A_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__KOMPL_A_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__KOMPL_A_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENATU_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENATU_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENATU_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENATU_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENOM_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENOM_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENOM_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__RELIV_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__RELIV_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__RELIV_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__RELIV_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__REVL_M_D_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__R_VEL_ME_20_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__R_VEL_ME_2_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__R_VEL_ME_7_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENAL_DOM_D__R_VEL_ME_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENAL_DOM_D__R_VEL_ME_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENAL_DOM_D__R_VEL_ME_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENAL_DOM_D__R_VEL_ME_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__MELFALAN_H_DROKLOR_R__ERIOLAN_50_MG_ENJEKSIYONLUK_NF_ZYONLUK_ZELTI_IN_LIYOFILIZE_T_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__MELFALAN__ALKERAN_2_MG_FILM_TABLET_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMALIDOMID__POMAVID_1_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMALIDOMID__POMAVID_2_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMALIDOMID__POMAVID_3_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMALIDOMID__POMAVID_4_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_1_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_2_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_3_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_4_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D___MNOV_D_1_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D___MNOV_D_2_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D___MNOV_D_3_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D___MNOV_D_4_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__SELINEKSOR__NEXPOVIO_20_MG_FILM_KAPLI_TABLET_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__TALIDOMIDE__THALIDOMIDE_BMS_50_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ACLASTA_5_MG_100_ML_IV_NF_ZYON_ZELTISI_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__BONZOLEN_4_MG_5_ML_I_V_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__KALIKSIR_4MG_5ML_I_V_NF_ZYONLUK_KONSANTRE_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__LUSIMA_5MG_100ML_IV_NF_ZYON_ZELTISI_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__OSTEOZOLEN_4_MG_5_ML_I_V_NFUZYON_IN_KONSANTRE_ZELTI_EREN_FLA_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZOLCURE_5_MG_100_ML_V_INF_ZYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZOLDR_A_4MG_5ML_IV_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZOLON_K_4_MG_5_ML_I_V_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZORONIC_4MG_5ML_IV_NF_ZYON_IN_KONSANTRE_ZELTI_EREN_FLAKON__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOH_DRAT__OSTEZOLEN_4MG_5ML_IV_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_SUSUZ_ZOLEDRON__ATAZOL_4_MG_5_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ACLASTA_5MG_100_ML_NF_ZYON_ZELTISI_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__BONEDRO_4MG_5ML_V_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN_FLAKO_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__CEM_X_5G_100ML_IV_NF_ZYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__RON_DRO_5_MG_100_ML_I_V_INF_ZYON_ZELTISI_I_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__VERTEBZOL_5_MG_100_ML_I_V_NF_ZYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOLEGEN_4_MG_5_ML_I_V_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN_F_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOLENAT_IV_4MG_5_ML_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN_FLA_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOLTONAR_5_MG_100_ML_V_INF_ZYON_ZELTISI_I_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOMEBON_4MG_5ML_INF_ZYON_I_IN_KONSANTRE_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__BONDREX_4MG_5_ML_IV_NF_ZYON_N_KONSANTRE_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__LAN_CZOL_5_MG_100_ML_IV_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__OSS_4_MG_5_ML_I_V_KONSANTRE_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__PLAZOL_4_MG_5_ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__RON_X_4_MG_5_ML_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLESTO_5_MG_100_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLKA_5MG_100ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLOPOROZ_5MG_100ML_V_NF_ZYON_N_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLTASTA_4MG_5ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ACLABON_5MG_100ML_NF_ZYON_ZELT_S_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__MULTIFLEX_ACLAVER_5_MG_100_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__XENDRO_5_MG_100_ML_IV_NF_ZYON_N_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ZOD_NAS_L_5_MG_100_ML_V_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ZOLTASTA_4MG_5ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__Zoledronik_Asit_Monohidrat__Metarzu_4_mg_5_ml_V_nf_zyon_in_Konsantre_zelti_eren_Flakon_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__Zoledronik_asit_monohidrat__Xolarex_5_mg_100_ml_IV_nf_zyonluk_zelti_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__ek4__EK-4-D.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__ek4__EK-4-E.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__ek4__EK-4-F.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__ek4__EK-4-G.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__sut__SUT.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:35:58 | dogrulama | Arsiv genel dogrulama tamamlandi | 159 PDF markdown'a cevrildi (metin yogunlugu esigine gore pymupdf4llm/docling). Ilk turda 51 belge sessizce kayipli cikmisti (EMA Revlimid oran 0.05, FDA Revlimid 0.12) - tespit edilip yeniden cevrildi, kayip 0. Validator'a kalici hacim kontrolu eklendi (oran<0.5 -> ERROR). Kritik dipnot triyaji: 23 eksikten 12'si klinik kosul tasiyor (MYEL-E 7, MYEL-G 2of5 2, MYEL-I 3). |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer1_clinical__asco__banerjee-et-al-2026-treatment-of-multiple-myeloma-asco-living-guideline-version-2026-1-1.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer1_clinical__esmo__esmo.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer1_clinical__nccn__jnccn-article-e260001.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer1_clinical__nccn__myeloma.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer1_clinical__nci_pdq__NCI_PDQ_myeloma_HP_2026.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_dara_backbone_regimens.md: ERROR 0, WARN 1, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_dara_quad_vs_triplet_2025.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_dara_transplant_ineligible_2025.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_daratumumab_efficacy_safety.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer1_clinical__pubmed_meta__PUBMED_META_quadruplet_TE_NDMM_2025.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_abecma_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_blenrep_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_carvykti_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_darzalex_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_elrexfio_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_empliciti_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_imnovid_PI.md: ERROR 0, WARN 0, REVIEW 3 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_kyprolis_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_lynozyfic_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_nexpovio_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_ninlaro_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_pepaxti_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_revlimid_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_sarclisa_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_talvey_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_tecvayli_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__ema__EMA_velcade_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_ABECMA_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_CARVYKTI_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_DARZALEX_FASPRO_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_DARZALEX_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_ELREXFIO_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_EMPLICITI_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_KYPROLIS_PI.md: ERROR 0, WARN 0, REVIEW 2 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_LYNOZYFIC_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_NINLARO_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_POMALYST_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_REVLIMID_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_SARCLISA_ESCENA_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_SARCLISA_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_TALVEY_PI.md: ERROR 0, WARN 0, REVIEW 5 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_TECVAYLI_PI.md: ERROR 0, WARN 0, REVIEW 5 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_THALOMID_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_VELCADE_PI.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__labels__FDA_XPOVIO_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__fda__orange_book__appendix_fda.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOMIB__BORCADE_3_5_MG_IV_SC_ENJEKSIYONLUK_ZELTI_HAZ_RLAMAK_IN_LIYOF_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOMIB__BORT_REL_1_MG_I_V_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOMIB__BORT_REL_3_5_MG_IV_SC_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOM_B__BORACTIB_3_5_MG_IV_SC_ENJEKSIYONLUK_ZELTI_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOM_B__B_EM_B_3_5_MG_IV_SC_ENJEKS_YONLUK_ZELT_N_TOZ_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOM_B__VELCADE_3_5_MG_IV_SC_ENJEKS_YONLUK_ZELT_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__BORTEZOM_B__VELTEZO_3_5_MG_IV_SC_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_100_MG_5_ML_NF_ZYONLUK_ZELTI_HAZ_RLAMAK_IN_KONSANTR_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_1800_MG_SC_ENJEKSIYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_400_MG_20_ML_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DENOSUMAB__PROL_A_60_MG_ML_SC_ENJEKSIYONLUK_ZELTI_EREN_KULLAN_MA_HAZ_R__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__DENOSUMAB__XGEVA_120_MG_SC_ENJEKS_YONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ELRANATAMAB__ELREXFIO_44_MG_1_1_ML_ENJEKSIYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ELRANATAMAB__ELREXFIO_76_MG_1_9_ML_ENJEKSIYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__IKSAZOMIB_SITRAT__NINLARO_3_MG_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__IKSAZOMIB_SITRAT__NINLARO_4_MG_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__IKSAZOMIB__NINLARO_2_3_MG_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ISATUXIMAB__SARCLISA_100_MG_5_ML_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ISATUXIMAB__SARCLISA_500_MG_25_ML_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARFILZOMIB__KARFILIB_60_MG_I_V_ENJEKSIYONLUK_ZELTI_HAZ_RLAMAK_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARFILZOMIB__KARZOM_60_MG_IV_NF_ZYONLUK_ZELTI_HAZ_RLAMAK_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARFILZOMIB__KYPROL_S_10_MG_IV_INF_ZYONLUK_ZELTI_HAZ_RLAMAK_I_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARFILZOMIB__KYPROL_S_30_MG_IV_INF_ZYONLUK_ZELTI_HAZ_RLAMAK_I_IN_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARF_LZOM_B__CAF_ZO_60_MG_I_V_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARF_LZOM_B__KYPROLIS_60_MG_IV_ENJEKS_YONLUK_ZELT_N_TOZ_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__KARF_LZOM_B__KYPROL_S_60_MG_IV_ENJEKS_YONLUK_ZELT_N_TOZ_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__KOMPL_A_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__KOMPL_A_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__KOMPL_A_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__KOMPL_A_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENATU_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENATU_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENATU_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENATU_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENOM_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENOM_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__LENOM_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__RELIV_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__RELIV_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__RELIV_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__RELIV_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__REVL_M_D_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__R_VEL_ME_20_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__R_VEL_ME_2_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENALIDOMID__R_VEL_ME_7_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENAL_DOM_D__R_VEL_ME_10_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENAL_DOM_D__R_VEL_ME_15_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENAL_DOM_D__R_VEL_ME_25_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__LENAL_DOM_D__R_VEL_ME_5_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__MELFALAN_H_DROKLOR_R__ERIOLAN_50_MG_ENJEKSIYONLUK_NF_ZYONLUK_ZELTI_IN_LIYOFILIZE_T_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__MELFALAN__ALKERAN_2_MG_FILM_TABLET_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMALIDOMID__POMAVID_1_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMALIDOMID__POMAVID_2_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMALIDOMID__POMAVID_3_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMALIDOMID__POMAVID_4_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_1_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_2_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_3_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_4_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D___MNOV_D_1_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D___MNOV_D_2_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D___MNOV_D_3_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__POMAL_DOM_D___MNOV_D_4_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__SELINEKSOR__NEXPOVIO_20_MG_FILM_KAPLI_TABLET_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__TALIDOMIDE__THALIDOMIDE_BMS_50_MG_SERT_KAPS_L_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ACLASTA_5_MG_100_ML_IV_NF_ZYON_ZELTISI_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__BONZOLEN_4_MG_5_ML_I_V_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__KALIKSIR_4MG_5ML_I_V_NF_ZYONLUK_KONSANTRE_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__LUSIMA_5MG_100ML_IV_NF_ZYON_ZELTISI_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__OSTEOZOLEN_4_MG_5_ML_I_V_NFUZYON_IN_KONSANTRE_ZELTI_EREN_FLA_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZOLCURE_5_MG_100_ML_V_INF_ZYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZOLDR_A_4MG_5ML_IV_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZOLON_K_4_MG_5_ML_I_V_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZORONIC_4MG_5ML_IV_NF_ZYON_IN_KONSANTRE_ZELTI_EREN_FLAKON__KUB.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOH_DRAT__OSTEZOLEN_4MG_5ML_IV_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_SUSUZ_ZOLEDRON__ATAZOL_4_MG_5_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ACLASTA_5MG_100_ML_NF_ZYON_ZELTISI_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__BONEDRO_4MG_5ML_V_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN_FLAKO_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__CEM_X_5G_100ML_IV_NF_ZYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__RON_DRO_5_MG_100_ML_I_V_INF_ZYON_ZELTISI_I_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__VERTEBZOL_5_MG_100_ML_I_V_NF_ZYONLUK_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOLEGEN_4_MG_5_ML_I_V_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN_F_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOLENAT_IV_4MG_5_ML_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN_FLA_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOLTONAR_5_MG_100_ML_V_INF_ZYON_ZELTISI_I_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOMEBON_4MG_5ML_INF_ZYON_I_IN_KONSANTRE_ZELTI_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__BONDREX_4MG_5_ML_IV_NF_ZYON_N_KONSANTRE_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__LAN_CZOL_5_MG_100_ML_IV_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__OSS_4_MG_5_ML_I_V_KONSANTRE_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__PLAZOL_4_MG_5_ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__RON_X_4_MG_5_ML_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLESTO_5_MG_100_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLKA_5MG_100ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLOPOROZ_5MG_100ML_V_NF_ZYON_N_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLTASTA_4MG_5ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ACLABON_5MG_100ML_NF_ZYON_ZELT_S_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__MULTIFLEX_ACLAVER_5_MG_100_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__XENDRO_5_MG_100_ML_IV_NF_ZYON_N_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ZOD_NAS_L_5_MG_100_ML_V_NF_ZYONLUK_ZELT__KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ZOLTASTA_4MG_5ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__Zoledronik_Asit_Monohidrat__Metarzu_4_mg_5_ml_V_nf_zyon_in_Konsantre_zelti_eren_Flakon_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer2_regulatory__titck__kub__Zoledronik_asit_monohidrat__Xolarex_5_mg_100_ml_IV_nf_zyonluk_zelti_KUB.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__ek4__EK-4-D.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__ek4__EK-4-E.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__ek4__EK-4-F.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__ek4__EK-4-G.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 09:37:17 | dogrulama | structural validation | _work\parsed\layer3_reimbursement__sut__SUT.md: ERROR 0, WARN 0, REVIEW 0 |
| 2026-08-05 11:49:08 | enrich | bolum zenginlestirme | 144 dosya, eu_smpc_en:407, eu_smpc_tr:2823, fda_pi:812 |
| 2026-08-05 11:50:07 | enrich | bolum zenginlestirme | 143 dosya, eu_smpc_en:407, eu_smpc_tr:2823, fda_pi:812 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer1_clinical__nccn__myeloma.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer1_clinical__pubmed_meta__PUBMED_META_dara_backbone_regimens.md: ERROR 0, WARN 1, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__ema__EMA_imnovid_PI.md: ERROR 0, WARN 0, REVIEW 3 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__ema__EMA_nexpovio_PI.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_ELREXFIO_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_KYPROLIS_PI.md: ERROR 0, WARN 0, REVIEW 2 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_REVLIMID_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_SARCLISA_ESCENA_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_TALVEY_PI.md: ERROR 0, WARN 0, REVIEW 5 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_TECVAYLI_PI.md: ERROR 0, WARN 0, REVIEW 5 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_XPOVIO_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__BORTEZOM_B__BORACTIB_3_5_MG_IV_SC_ENJEKSIYONLUK_ZELTI_IN_TOZ_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_100_MG_5_ML_NF_ZYONLUK_ZELTI_HAZ_RLAMAK_IN_KONSANTR_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_400_MG_20_ML_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__IKSAZOMIB__NINLARO_2_3_MG_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__KARFILZOMIB__KYPROL_S_10_MG_IV_INF_ZYONLUK_ZELTI_HAZ_RLAMAK_I_IN_TOZ_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__KARFILZOMIB__KYPROL_S_30_MG_IV_INF_ZYONLUK_ZELTI_HAZ_RLAMAK_I_IN_TOZ_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__KARF_LZOM_B__CAF_ZO_60_MG_I_V_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__LENALIDOMID__KOMPL_A_15_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_10_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_15_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_25_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__LENALIDOMID__PAUSED_5_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_10_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_25_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_5_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__LENALIDOMID__REVL_M_D_15_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__MELFALAN_H_DROKLOR_R__ERIOLAN_50_MG_ENJEKSIYONLUK_NF_ZYONLUK_ZELTI_IN_LIYOFILIZE_T_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__MELFALAN__ALKERAN_2_MG_FILM_TABLET_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_1_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__POMAL_DOM_D__POMALEM_2_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__TALIDOMIDE__THALIDOMIDE_BMS_50_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__BONZOLEN_4_MG_5_ML_I_V_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__OSTEOZOLEN_4_MG_5_ML_I_V_NFUZYON_IN_KONSANTRE_ZELTI_EREN_FLA_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZOLON_K_4_MG_5_ML_I_V_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZORONIC_4MG_5ML_IV_NF_ZYON_IN_KONSANTRE_ZELTI_EREN_FLAKON__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_SUSUZ_ZOLEDRON__ATAZOL_4_MG_5_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__BONEDRO_4MG_5ML_V_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN_FLAKO_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__VERTEBZOL_5_MG_100_ML_I_V_NF_ZYONLUK_ZELTI_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOLEGEN_4_MG_5_ML_I_V_INF_ZYON_I_IN_KONSANTRE_ZELTI_I_EREN_F_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__ZOMEBON_4MG_5ML_INF_ZYON_I_IN_KONSANTRE_ZELTI_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__OSS_4_MG_5_ML_I_V_KONSANTRE_NF_ZYONLUK_ZELT__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__PLAZOL_4_MG_5_ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLESTO_5_MG_100_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLTASTA_4MG_5ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ACLABON_5MG_100ML_NF_ZYON_ZELT_S_EREN_FLAKON_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__MULTIFLEX_ACLAVER_5_MG_100_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ZOD_NAS_L_5_MG_100_ML_V_NF_ZYONLUK_ZELT__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:51:56 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ZOLTASTA_4MG_5ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:39 | enrich | bolum zenginlestirme | 143 dosya, eu_smpc_en:407, eu_smpc_tr:2868, fda_pi:471 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer1_clinical__nccn__myeloma.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer1_clinical__pubmed_meta__PUBMED_META_dara_backbone_regimens.md: ERROR 0, WARN 1, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__ema__EMA_imnovid_PI.md: ERROR 0, WARN 0, REVIEW 3 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__ema__EMA_nexpovio_PI.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_ELREXFIO_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_KYPROLIS_PI.md: ERROR 0, WARN 0, REVIEW 2 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_REVLIMID_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_SARCLISA_ESCENA_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_TALVEY_PI.md: ERROR 0, WARN 0, REVIEW 5 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_TECVAYLI_PI.md: ERROR 0, WARN 0, REVIEW 5 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_XPOVIO_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_100_MG_5_ML_NF_ZYONLUK_ZELTI_HAZ_RLAMAK_IN_KONSANTR_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_400_MG_20_ML_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__KARF_LZOM_B__CAF_ZO_60_MG_I_V_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_25_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_5_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__MELFALAN_H_DROKLOR_R__ERIOLAN_50_MG_ENJEKSIYONLUK_NF_ZYONLUK_ZELTI_IN_LIYOFILIZE_T_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__MELFALAN__ALKERAN_2_MG_FILM_TABLET_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__OSTEOZOLEN_4_MG_5_ML_I_V_NFUZYON_IN_KONSANTRE_ZELTI_EREN_FLA_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZOLON_K_4_MG_5_ML_I_V_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZORONIC_4MG_5ML_IV_NF_ZYON_IN_KONSANTRE_ZELTI_EREN_FLAKON__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__VERTEBZOL_5_MG_100_ML_I_V_NF_ZYONLUK_ZELTI_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__PLAZOL_4_MG_5_ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLESTO_5_MG_100_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLTASTA_4MG_5ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ACLABON_5MG_100ML_NF_ZYON_ZELT_S_EREN_FLAKON_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__MULTIFLEX_ACLAVER_5_MG_100_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:55:42 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ZOD_NAS_L_5_MG_100_ML_V_NF_ZYONLUK_ZELT__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer1_clinical__nccn__myeloma.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer1_clinical__pubmed_meta__PUBMED_META_dara_backbone_regimens.md: ERROR 0, WARN 1, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__ema__EMA_imnovid_PI.md: ERROR 0, WARN 0, REVIEW 3 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__ema__EMA_nexpovio_PI.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_ELREXFIO_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_KYPROLIS_PI.md: ERROR 0, WARN 0, REVIEW 2 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_REVLIMID_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_SARCLISA_ESCENA_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_TALVEY_PI.md: ERROR 0, WARN 0, REVIEW 5 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_TECVAYLI_PI.md: ERROR 0, WARN 0, REVIEW 5 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_XPOVIO_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_100_MG_5_ML_NF_ZYONLUK_ZELTI_HAZ_RLAMAK_IN_KONSANTR_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_400_MG_20_ML_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__KARF_LZOM_B__CAF_ZO_60_MG_I_V_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_25_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_5_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__MELFALAN_H_DROKLOR_R__ERIOLAN_50_MG_ENJEKSIYONLUK_NF_ZYONLUK_ZELTI_IN_LIYOFILIZE_T_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__MELFALAN__ALKERAN_2_MG_FILM_TABLET_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__OSTEOZOLEN_4_MG_5_ML_I_V_NFUZYON_IN_KONSANTRE_ZELTI_EREN_FLA_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZOLON_K_4_MG_5_ML_I_V_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZORONIC_4MG_5ML_IV_NF_ZYON_IN_KONSANTRE_ZELTI_EREN_FLAKON__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__VERTEBZOL_5_MG_100_ML_I_V_NF_ZYONLUK_ZELTI_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__PLAZOL_4_MG_5_ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLESTO_5_MG_100_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLTASTA_4MG_5ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ACLABON_5MG_100ML_NF_ZYON_ZELT_S_EREN_FLAKON_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__MULTIFLEX_ACLAVER_5_MG_100_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 11:56:05 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ZOD_NAS_L_5_MG_100_ML_V_NF_ZYONLUK_ZELT__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:04:07 | dogrulama | structural validation | layer1_clinical\nccn\nccn_myeloma_manual.md: ERROR 21, WARN 59, REVIEW 28 |
| 2026-08-05 12:05:07 | dogrulama | structural validation | layer1_clinical\nccn\nccn_myeloma_manual.md: ERROR 12, WARN 43, REVIEW 32 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer1_clinical__nccn__myeloma.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer1_clinical__pubmed_meta__PUBMED_META_dara_backbone_regimens.md: ERROR 0, WARN 1, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__ema__EMA_imnovid_PI.md: ERROR 0, WARN 0, REVIEW 3 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__ema__EMA_nexpovio_PI.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_ELREXFIO_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_KYPROLIS_PI.md: ERROR 0, WARN 0, REVIEW 2 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_REVLIMID_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_SARCLISA_ESCENA_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_TALVEY_PI.md: ERROR 0, WARN 0, REVIEW 5 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_TECVAYLI_PI.md: ERROR 0, WARN 0, REVIEW 5 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__fda__labels__FDA_XPOVIO_PI.md: ERROR 0, WARN 0, REVIEW 1 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_100_MG_5_ML_NF_ZYONLUK_ZELTI_HAZ_RLAMAK_IN_KONSANTR_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__DARATUMUMAB__DARZALEX_400_MG_20_ML_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__KARF_LZOM_B__CAF_ZO_60_MG_I_V_ENJEKS_YONLUK_ZELT_HAZIRLAMAK_N_TOZ_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_25_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__LENALIDOMID__REVLIMID_5_MG_SERT_KAPS_L_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__MELFALAN_H_DROKLOR_R__ERIOLAN_50_MG_ENJEKSIYONLUK_NF_ZYONLUK_ZELTI_IN_LIYOFILIZE_T_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__MELFALAN__ALKERAN_2_MG_FILM_TABLET_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__OSTEOZOLEN_4_MG_5_ML_I_V_NFUZYON_IN_KONSANTRE_ZELTI_EREN_FLA_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZOLON_K_4_MG_5_ML_I_V_NF_ZYONLUK_ZELT_HAZIRLAMAK_N_KONSANTRE_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT_MONOHIDRAT__ZORONIC_4MG_5ML_IV_NF_ZYON_IN_KONSANTRE_ZELTI_EREN_FLAKON__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRONIK_ASIT__VERTEBZOL_5_MG_100_ML_I_V_NF_ZYONLUK_ZELTI_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__PLAZOL_4_MG_5_ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLESTO_5_MG_100_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T_MONOH_DRAT__ZOLTASTA_4MG_5ML_I_V_NF_ZYON_N_KONSANTRE_ZELT_EREN_FLAKON_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ACLABON_5MG_100ML_NF_ZYON_ZELT_S_EREN_FLAKON_KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__MULTIFLEX_ACLAVER_5_MG_100_ML_IV_NF_ZYONLUK_ZELT__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | _work\enriched\layer2_regulatory__titck__kub__ZOLEDRON_K_AS_T__ZOD_NAS_L_5_MG_100_ML_V_NF_ZYONLUK_ZELT__KUB.md: ERROR 1, WARN 0, REVIEW 0 |
| 2026-08-05 12:05:23 | dogrulama | structural validation | layer1_clinical\nccn\nccn_myeloma_manual.md: ERROR 12, WARN 43, REVIEW 32 |
| 2026-08-05 13:51:50 | repair | bozuk donusum onarimi | 7 belge duz metin cikaricisiyla yeniden uretildi |
| 2026-08-05 13:51:56 | enrich | bolum zenginlestirme | 143 dosya, eu_smpc_en:407, eu_smpc_tr:2874, fda_pi:471 |
| 2026-08-05 13:53:15 | enrich | bolum zenginlestirme | 143 dosya, eu_smpc_en:407, eu_smpc_tr:2929, fda_pi:471 |
| 2026-08-05 13:57:09 | chunk | chunking | 16411 chunk, 160 belge |
| 2026-08-05 13:58:06 | chunk | chunking | 14351 chunk, 160 belge |
| 2026-08-05 15:09:21 | chunk | chunking | 14531 chunk, 160 belge |
| 2026-08-05 15:36:30 | chunk | chunking | 14531 chunk, 160 belge |
| 2026-08-05 16:01:16 | chunk | chunking | 14532 chunk, 160 belge |
| 2026-08-05 16:47:55 | embed | gomme | BAAI/bge-m3: 32 chunk, 84sn |
| 2026-08-06 11:06:36 | embed | gomme | BAAI/bge-m3: 1200 chunk, 2038sn |
