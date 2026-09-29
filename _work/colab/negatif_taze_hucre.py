# 11) TAZE NEGATIF OLCUMU - tek parca, dosya yuklemesi gerektirmez.
#     Esikler DONDURULMUS: arama 0.50, alan kurali "varlik|hast75".
#     Alt surec kullanmiyoruz: Qdrant yerel modda depoyu kilitliyor.
import json, pipeline as P, qdrant_index as QI, query_processing as QP

ARAMA_ESIGI, K = 0.50, 4
SORULAR = [
    ('N16', 'yakin', 'Akut miyeloid lösemide 7+3 indüksiyon rejimi nasıl uygulanır?'),
    ('N17', 'yakin', 'İmmün trombositopenide birinci basamak tedavi nedir?'),
    ('N18', 'yakin', 'Kronik miyeloid lösemide imatinib başlangıç dozu kaç mg?'),
    ('N19', 'yakin', 'Erken evre Hodgkin lenfomada kaç kür ABVD verilir?'),
    ('N20', 'yakin', 'Derin ven trombozunda warfarin ile hedef INR aralığı nedir?'),
    ('N21', 'yakin', 'Demir eksikliği anemisinde oral demir tedavisi kaç ay sürdürülmeli?'),
    ('N22', 'yakin', 'Orak hücreli anemide hidroksiüre hangi hastalara başlanır?'),
    ('N23', 'yakin', "Hemofili A'da faktör VIII replasman dozu nasıl hesaplanır?"),
    ('N24', 'yakin', 'Ağır aplastik anemide antitimosit globulin tedavisi nasıl verilir?'),
    ('N25', 'tuzak', 'Del(5q) miyelodisplastik sendromda lenalidomid dozu nedir?'),
    ('N26', 'tuzak', 'Mantle hücreli lenfomada bortezomib hangi rejimle kombine edilir?'),
    ('N27', 'yakin', 'Kronik lenfositik lösemide ibrutinib ne zaman kesilmeli?'),
    ('N28', 'yakin', 'Otoimmün hemolitik anemide rituksimab hangi basamakta kullanılır?'),
    ('N29', 'yakin', 'Polisitemia verada flebotomi için hedef hematokrit değeri kaçtır?'),
    ('N30', 'yakin', 'Talasemi majorda demir şelasyonuna hangi ferritin düzeyinde başlanır?'),
]

try:
    istemci
except NameError:
    istemci = QI.ac()

kayit = []
for i, (kimlik, zorluk, soru) in enumerate(SORULAR, 1):
    analiz = QP.analiz(soru)
    vek = P._sorgu_vektoru(soru)
    noktalar = QI.ara(istemci, vek, k=P.ADAY, ilac=analiz["ilac"])
    if analiz["ilac"]:
        hedefli = QI.ara(istemci, vek, k=K, zorunlu_ilac=analiz["ilac"])
        var = {p.id for p in hedefli}
        noktalar = hedefli + [p for p in noktalar if p.id not in var]
    en_iyi = max((p.score for p in noktalar), default=0.0)
    secili = P.tekrar_ayikla(P.baglam_sec(noktalar, analiz["ilac"]))[:K]
    hast = round(sum(1 for x in secili
                     if (x["nokta"].payload.get("disease") or []))
                 / max(1, len(secili)), 3)
    varlik = P.alan_skoru(soru, analiz)["varlik"]
    arama_ok, alan_ok = en_iyi >= ARAMA_ESIGI, (varlik or hast >= 0.75)
    kayit.append({"id": kimlik, "soru": soru, "zorluk": zorluk,
                  "arama_skoru": round(en_iyi, 3), "alan_varlik": bool(varlik),
                  "alan_hast": hast,
                  "taninan": {t: analiz[t] for t in
                              ("ilac", "hastalik", "rejim", "sinif")
                              if analiz[t]},
                  "arama_kapisi": "gecti" if arama_ok else "durdurdu",
                  "alan_kapisi": "gecti" if alan_ok else "durdurdu",
                  "modele_ulasti": bool(arama_ok and alan_ok)})
    print(f"  {i:2d}/15 {kimlik} skor {en_iyi:.2f} varlik {int(varlik)} "
          f"hast {hast:.2f} "
          f"{'MODELE ULASTI' if arama_ok and alan_ok else 'durduruldu'}",
          flush=True)

ulasan = [x for x in kayit if x["modele_ulasti"]]
arama = [x for x in kayit if x["arama_kapisi"] == "durdurdu"]
alan = [x for x in kayit if x["arama_kapisi"] == "gecti"
        and x["alan_kapisi"] == "durdurdu"]
print()
print(f"TOPLAM {len(kayit)} taze negatif")
print(f"  arama kapisi durdurdu : {len(arama)}")
print(f"  alan kapisi durdurdu  : {len(alan)}")
print(f"  MODELE ULASAN         : {len(ulasan)}  (uydurma ust siniri)")
for x in ulasan:
    print(f"    {x['id']} [{x['zorluk']}] skor {x['arama_skoru']} "
          f"taninan {x['taninan']}")

json.dump({"esikler": {"arama": ARAMA_ESIGI, "alan": "varlik|hast75"},
           "sorular": "negative_queries_v2.json",
           "ozet": {"toplam": len(kayit), "arama_durdurdu": len(arama),
                    "alan_durdurdu": len(alan), "modele_ulasan": len(ulasan)},
           "kayitlar": kayit},
          open("/content/negatif_taze.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
from google.colab import files
files.download("/content/negatif_taze.json")