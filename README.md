# Miyelom-RAG

Multipl miyelom tedavisine dair Türkçe soruları klinik kılavuz, ruhsat ve geri ödeme belgelerine dayanarak cevaplayan bir RAG sistemi. Her cevap künyeli kaynaklarıyla birlikte geliyor.

**163 belge · 14.532 parça · 3 katman · 78 test sorusu**

## Ne işe yarıyor

Bir hekimin tedavi kararı üç soruya dayanır. Kanıt rejimi destekliyor mu? İlaç Türkiye'de ruhsatlı mı? SGK bedelini ödüyor mu? Bu soruların cevabı üç ayrı belge kümesinde duruyor ve Miyelom-RAG hepsini tek bir arşivde topluyor.

| Katman | Kaynaklar |
|---|---|
| Klinik kanıt | NCCN, EHA-ESMO, ASCO, NCI PDQ, meta-analizler |
| Ruhsat | FDA, EMA, TİTCK Kısa Ürün Bilgileri |
| Geri ödeme | SGK Sağlık Uygulama Tebliği ve EK-4 listeleri |

## Nasıl çalışıyor

```
soru → sorgu işleme → BGE-M3 gömme → Qdrant arama
     → KAPI 1: arama skoru
     → KAPI 2: alan kapısı
     → Qwen2.5-7B ile cevap → atıf onarımı
     → KAPI 3: dayanaklılık
     → cevap + kaynaklar + güven seviyesi
```

Üç kapı sistemin uydurmasını engelliyor. Soru arşivin konusu dışındaysa dil modeli hiç çağrılmıyor ve cevap yaklaşık bir saniyede reddediliyor.

## Sonuçlar

Eşikler test sorularının yarısında seçilip donduruldu. Aşağıdaki rakamlar, eşiklerin hiç görmediği diğer yarıdan geliyor.

| Ölçü | Sonuç |
|---|---|
| Cevaplanan soru | 33 / 39 |
| Cümlelerin kaynağa dayanma oranı | %94 |
| Arşiv dışı sorularda uydurma | **0 / 15** |

> **En önemli bulgu:** Benzerlik skoru arşiv dışı soruları ayırt edemedi, 15 sorunun 15'i de skor kapısını geçti. Reddetmeyi sağlayan şey belgelerin metadata'sına dayanan alan kapısı oldu.

Tüm ölçümler, karşılaştırılan beş dil modeli ve geçersiz sayılan rakamlar [`_logs/KARAR_KAYDI.md`](_logs/KARAR_KAYDI.md) dosyasında.

## Kurulum

Kaynak PDF'ler telif ve boyut nedeniyle depoda yok. Listeleri [`DATA_CATALOG.csv`](DATA_CATALOG.csv) dosyasında.

```bash
# boru hattı
python _scripts/batch_docling.py
python _scripts/repair_parsed.py
python _scripts/enrich_sections.py
python _scripts/chunk.py
python _scripts/embed_chunks.py
python _scripts/qdrant_index.py

# servis ve arayüz
pip install -r _web/backend/requirements.txt
cp _web/backend/.env.ornek _web/backend/.env
ollama pull qwen2.5:7b
cd _web/backend && uvicorn app:uygulama --port 8000 --workers 1
cd _web/frontend && npm install && npm run dev
```

Ayrıntılar [`_web/KURULUM.md`](_web/KURULUM.md) dosyasında.

## Bilinen eksikler

- Cevapları bir hematolog gözden geçirmedi, klinik doğrulama yapılmadı.
- Geri ödeme tabloları yapılandırılmış veri olarak eklenmedi.
- Kimlik doğrulama katmanı yok.

---

Staj sürecinde geliştirildi. Bir araştırma prototipidir ve klinik kararın yerine geçmez.
