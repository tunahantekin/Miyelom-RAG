# 13) ATIF ONARIMI OLCUMU (Level 4). GPU'suz, dil modeli KOSMUYOR.
#     Onarim deterministik - ayni cevap + ayni parcalar ayni atifi verir - bu
#     yuzden 40 dakikalik yeniden uretim yerine KAYITLI 78 cevap uzerinde
#     olculuyor. Sadece BGE-M3 gerekiyor, o da CPU'da kosuyor.
#
#     ONCE yerelde: python _scripts/colab_paketle.py
#     Sonra asagidaki yuklemede "1" klasorunden su UC dosyayi sec:
#       pipeline.py   answer_eval.py   level3_yeniden.json
#     (hepsi ayni klasorde, tek seferde secilebiliyor)
from google.colab import files
import shutil, importlib, os, glob

YER = {'pipeline.py': '_scripts', 'answer_eval.py': '_scripts',
       'level3_yeniden.json': '_logs'}

for ad in files.upload():
    temiz = ad
    for ek in (' (1)', ' (2)', ' (3)'):
        temiz = temiz.replace(ek, '')
    if temiz not in YER:
        print('ATLANDI (listede yok):', ad)
        continue
    hedef_dizin = f'{KOK}/{YER[temiz]}'
    os.makedirs(hedef_dizin, exist_ok=True)
    shutil.move(ad, f'{hedef_dizin}/{temiz}')
    print('yuklendi ->', f'{YER[temiz]}/{temiz}')

# Dosya gercekten yerine oturdu mu? Onceki denemede hata tam burada cikti,
# bu yuzden artik once ariyoruz ve bulamazsak nedenini yaziyoruz.
KAYIT = f'{KOK}/_logs/level3_yeniden.json'
if not os.path.exists(KAYIT):
    aday = glob.glob('/content/**/level3_yeniden.json', recursive=True)
    if aday:
        os.makedirs(f'{KOK}/_logs', exist_ok=True)
        shutil.copy(aday[0], KAYIT)
        print('baska yerde bulundu, tasindi:', aday[0])
    else:
        print('BULUNAMADI. /content altindaki json dosyalari:')
        for y in glob.glob('/content/**/*.json', recursive=True)[:30]:
            print('   ', y)
        raise SystemExit('level3_yeniden.json yuklenmemis - hucreyi tekrar '
                         'calistirip UC dosyayi da sec')

import pipeline as P
import answer_eval as AE
importlib.reload(P)
importlib.reload(AE)
print('esikler:', P.REDDET_ESIGI, P.DAYANAK_ESIGI, P.SEM_ESIGI, P.ALAN_KURAL)
print('atif_onar var mi:', hasattr(P, 'atif_onar'))

# Qdrant yerel modda depoyu kilitliyor: defterde acik istemci varken ikinci
# istemci acilamiyor. Acik olani devrediyoruz, yoksa yenisini aciyoruz.
try:
    istemci
except NameError:
    import qdrant_index as QI
    istemci = QI.ac()

AE.yeniden_rapor(KAYIT, k=4, istemci=istemci)

files.download(KAYIT)
