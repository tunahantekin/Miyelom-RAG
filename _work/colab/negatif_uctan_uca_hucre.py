# 12) TAZE NEGATIFLER, UCTAN UCA. Kapilar artik cevapla() icine bagli, yani
#     bu kosu gercek sistemin davranisini gosteriyor. 11 soru modele hic
#     gitmeyecek (alan kapisi), 4 soru gidecek; dorduncu kapi (dayanaklilik)
#     onlarin bir kismini daha eleyebilir. Ekranda kalan cevaplar UYDURMA
#     adayidir - klinik gozle bakilacak olan onlar.
#
#     ONCE: guncel pipeline.py'yi yukle (yerelde _scripts/pipeline.py).
from google.colab import files
import shutil, importlib, os

for ad in files.upload():
    shutil.move(ad, f'{KOK}/_scripts/pipeline.py')
    print('yuklendi ->', ad)

import pipeline as P
importlib.reload(P)
print('esikler:', P.REDDET_ESIGI, P.DAYANAK_ESIGI, P.SEM_ESIGI, P.ALAN_KURAL)

SORULAR = [
    ('N16', 'Akut miyeloid lösemide 7+3 indüksiyon rejimi nasıl uygulanır?'),
    ('N17', 'İmmün trombositopenide birinci basamak tedavi nedir?'),
    ('N18', 'Kronik miyeloid lösemide imatinib başlangıç dozu kaç mg?'),
    ('N19', 'Erken evre Hodgkin lenfomada kaç kür ABVD verilir?'),
    ('N20', 'Derin ven trombozunda warfarin ile hedef INR aralığı nedir?'),
    ('N21', 'Demir eksikliği anemisinde oral demir tedavisi kaç ay sürdürülmeli?'),
    ('N22', 'Orak hücreli anemide hidroksiüre hangi hastalara başlanır?'),
    ('N23', "Hemofili A'da faktör VIII replasman dozu nasıl hesaplanır?"),
    ('N24', 'Ağır aplastik anemide antitimosit globulin tedavisi nasıl verilir?'),
    ('N25', 'Del(5q) miyelodisplastik sendromda lenalidomid dozu nedir?'),
    ('N26', 'Mantle hücreli lenfomada bortezomib hangi rejimle kombine edilir?'),
    ('N27', 'Kronik lenfositik lösemide ibrutinib ne zaman kesilmeli?'),
    ('N28', 'Otoimmün hemolitik anemide rituksimab hangi basamakta kullanılır?'),
    ('N29', 'Polisitemia verada flebotomi için hedef hematokrit değeri kaçtır?'),
    ('N30', 'Talasemi majorda demir şelasyonuna hangi ferritin düzeyinde başlanır?'),
]

try:
    istemci
except NameError:
    import qdrant_index as QI
    istemci = QI.ac()

import json
sonuc = []
for kimlik, soru in SORULAR:
    r = P.cevapla(soru, llm=llm, istemci=istemci, k=4)
    g = r['guven']
    neden = ('alan kapisi' if 'alan_kapisi' in g else
             'dayanak kapisi' if 'dayanak_kapisi' in g else
             'arama kapisi' if r['reddedildi'] else 'CEVAP URETILDI')
    print('=' * 72)
    print(f"{kimlik}  {soru}")
    print(f"  skor {g['arama_skoru']}  dayanak {g.get('dayanaklilik', 0):.2f}"
          f"  -> {neden}")
    if not r['reddedildi']:
        print(r['cevap'])
        for x in r['kaynaklar'][:4]:
            print('   ', P.kunye(x))
    sonuc.append({'id': kimlik, 'soru': soru, 'reddedildi': r['reddedildi'],
                  'neden': neden, 'arama_skoru': g['arama_skoru'],
                  'dayanaklilik': g.get('dayanaklilik', 0.0),
                  'cevap': r['cevap'],
                  'gizlenen_cevap': g.get('gizlenen_cevap', '')})

reddedilen = [x for x in sonuc if x['reddedildi']]
print()
print("TOPLAM 15 taze negatif")
print(f"  reddedildi     : {len(reddedilen)}")
for ad in ('arama kapisi', 'alan kapisi', 'dayanak kapisi'):
    print(f"    {ad:15s}: {sum(1 for x in sonuc if x['neden'] == ad)}")
print(f"  CEVAP URETILDI : {15 - len(reddedilen)}  <- uydurma adayi")

json.dump(sonuc, open('/content/negatif_uctan_uca.json', 'w', encoding='utf-8'),
          indent=1, ensure_ascii=False)
files.download('/content/negatif_uctan_uca.json')
