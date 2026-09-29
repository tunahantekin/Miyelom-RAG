#!/usr/bin/env python
"""Sorgu isleme - boru hattinin 7. adimi.

NEDEN VAR

Level 2 olcumunde Q18 dort modun dordunde de kacti. Soru teklistamab'in
basamakli doz semasini soruyordu; dort mod da elranatamab (ELREXFIO) getirdi.
Teklistamab arsivde eksik degil - FDA ve EMA belgelerinde 56 chunk var. Sorun
su: iki ilac da BCMA hedefli bispesifik antikor, ikisinin de basamakli dozu ve
sitokin salinim sendromu uyarisi var. Anlamsal olarak metinler nerdeyse ayni;
ayirt eden tek sey ozel isim. Gomme modeli konuyu agirliklandiriyor, ismi degil.

Reranker bunu duzeltemedi cunku dogru chunk havuza hic girmemisti. Duzeltme
sorgu tarafinda olmali: sorudaki etken maddeyi tani, aramayi ona gore duzenle.

TASARIM KARARI: FILTRE DEGIL, SIRALAMA

Sert metadata filtresi (drug == teclistamab olmayani ele) cazip ama tehlikeli.
drug_names 14.532 chunk'in 8.819'unda dolu; %39'u etiketsiz. Etiketsizler
cogunlukla kilavuzlarin genel bolumleri, tani algoritmalari ve SUT maddeleri.
Sert filtre bunlarin tamamini eler ve etiketleme bir chunk'i kacirmissa dogru
cevap da elenir. Sonuc bos liste olur - kullanici "bilgi yok" saniyor, oysa
bilgi arsivde duruyor. Sessiz kayip, yanlis cevaptan daha sinsi.

Bu yuzden uc kumeye ayirip sirayi degistiriyoruz, hicbir sey atilmiyor:
    A) sorudaki ilacla etiketli chunk'lar       -> yukari
    B) hic ilac etiketi olmayan chunk'lar       -> ortada (genel kilavuz metni)
    C) YALNIZCA baska ilacla etiketli chunk'lar -> asagi
Q18'de ELREXFIO'yu asagi iten C kurali.

KAYNAK FIKRI: sozluk chunk.py'den geliyor

Chunk'lari etiketlerken kullanilan ILAC sozlugunun aynisi sorgu tarafinda da
kullaniliyor. Iki ayri sozluk tutulsaydi zamanla birbirinden sapar, etiketle
sorgu birbirini bulamaz hale gelirdi.

Calistirma (20 golden query uzerinde ne tespit edildigini gorur):
    _env/parse/Scripts/python.exe _scripts/query_processing.py
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chunk import ILAC, HASTALIK, ilac_bul


# --- Rejim kisaltmalari -------------------------------------------------
# Klinik soru "VRd rejimi" der, KUB'de "bortezomib + lenalidomid + deksametazon"
# yazar. Kisaltma bilesenlerine acilmazsa hicbir arama bunlari birlestiremez.
REJIM = {
    "VRd":    ["Bortezomib", "Lenalidomide", "Dexamethasone"],
    "RVd":    ["Bortezomib", "Lenalidomide", "Dexamethasone"],
    "RVD":    ["Bortezomib", "Lenalidomide", "Dexamethasone"],
    "KRd":    ["Carfilzomib", "Lenalidomide", "Dexamethasone"],
    "DRd":    ["Daratumumab", "Lenalidomide", "Dexamethasone"],
    "DVd":    ["Daratumumab", "Bortezomib", "Dexamethasone"],
    "DPd":    ["Daratumumab", "Pomalidomide", "Dexamethasone"],
    "VTd":    ["Bortezomib", "Thalidomide", "Dexamethasone"],
    "DVTd":   ["Daratumumab", "Bortezomib", "Thalidomide", "Dexamethasone"],
    "DVRd":   ["Daratumumab", "Bortezomib", "Lenalidomide", "Dexamethasone"],
    "VMP":    ["Bortezomib", "Melphalan", "Prednisone"],
    "MPT":    ["Melphalan", "Prednisone", "Thalidomide"],
    "CyBorD": ["Cyclophosphamide", "Bortezomib", "Dexamethasone"],
    "VCd":    ["Cyclophosphamide", "Bortezomib", "Dexamethasone"],
    "KCd":    ["Carfilzomib", "Cyclophosphamide", "Dexamethasone"],
    "IsaKd":  ["Isatuximab", "Carfilzomib", "Dexamethasone"],
    "IsaPd":  ["Isatuximab", "Pomalidomide", "Dexamethasone"],
    "PVd":    ["Pomalidomide", "Bortezomib", "Dexamethasone"],
    "EloPd":  ["Elotuzumab", "Pomalidomide", "Dexamethasone"],
    "SVd":    ["Selinexor", "Bortezomib", "Dexamethasone"],
    "IRd":    ["Ixazomib", "Lenalidomide", "Dexamethasone"],
    "Rd":     ["Lenalidomide", "Dexamethasone"],
}

# --- Ilac siniflari -----------------------------------------------------
# Klinik soru cogu zaman molekul degil SINIF adi kullaniyor: "bisfosfonat mi
# denosumab mi", "proteozom inhibitoru ile idame". Sinif taninmazsa boost
# tehlikeli hale geliyor: Q05'te yalnizca Denosumab tespit edilseydi zoledronik
# asit chunk'lari "baska ilac" sayilip asagi itilirdi ve karsilastirma sorusunun
# yarisi kaybolurdu. Yani sinif sozlugu bir iyilestirme degil, boost'un dogru
# calismasi icin zorunlu parca.
SINIF = {
    "bisfosfonat|bisphosphonate": ["Zoledronic acid", "Pamidronate"],
    "proteozom inhibit|proteasome inhibitor": ["Bortezomib", "Carfilzomib",
                                               "Ixazomib"],
    "immunomodulat|immünomodülat|imid\\b": ["Lenalidomide", "Thalidomide",
                                            "Pomalidomide"],
    "anti-?cd38|cd38": ["Daratumumab", "Isatuximab"],
    "bispesifik|bispecific|bcma hedefli": ["Teclistamab", "Talquetamab",
                                           "Elranatamab"],
    "car-?t|kimerik antijen": ["Idecabtagene vicleucel",
                               "Ciltacabtagene autoleucel"],
    # Ciplak "steroid" tetikleyici DEGIL: her bransta kullanilan genel bir
    # sozcuk. Negatif kumede "KOAH alevlenmesinde sistemik steroid" sorusu bu
    # yuzden miyelom alaninda saniliyordu. Sinif adi acikca yazilmali.
    "kortikosteroid|glukokortikoid": ["Dexamethasone", "Prednisone"],
    "alkilleyici|alkylating": ["Melphalan", "Cyclophosphamide", "Bendamustine"],
}

# --- Klinik kisaltmalar -------------------------------------------------
# Acilimlar hem Turkce hem Ingilizce veriliyor: sorular Turkce, NCCN Ingilizce.
# BM25'in Turkce soruyla Ingilizce basligi birlestirememesinin caresi bu.
KISALTMA = {
    "MRD":   "minimal residual disease minimal rezidüel hastalık",
    "ASCT":  "autologous stem cell transplant otolog kök hücre nakli",
    "OKHN":  "otolog kök hücre nakli autologous stem cell transplant",
    "CRS":   "cytokine release syndrome sitokin salınım sendromu",
    "ICANS": "immune effector cell-associated neurotoxicity nörotoksisite",
    "MGUS":  "monoclonal gammopathy of undetermined significance monoklonal gammopati",
    "SMM":   "smoldering multiple myeloma sessiz miyelom",
    "ISS":   "international staging system evreleme",
    "VTE":   "venous thromboembolism venöz tromboembolizm",
    "PN":    "peripheral neuropathy periferik nöropati",
    "CRAB":  "hypercalcemia renal failure anemia bone lesions",
    "FISH":  "fluorescence in situ hybridization sitogenetik",
    "sCR":   "stringent complete response",
    "VGPR":  "very good partial response",
    "IMiD":  "immunomodulatory drug immünomodülatör",
    "BCMA":  "B-cell maturation antigen bispecific",
    "IVIG":  "intravenous immunoglobulin intravenöz immünoglobulin",
    "GVHD":  "graft versus host disease",
    "SUT":   "sağlık uygulama tebliği geri ödeme",
}

# --- Sitogenetik -------------------------------------------------------
# Yazim cok degisken: del(17p) / del 17p / 17p delesyonu / t(4;14) / t(4:14).
SITOGENETIK = [
    ("del(17p)", r"del\s*\(?\s*17\s*p|17\s*p\s*(delesyon|deletion)"),
    ("t(4;14)",  r"t\s*\(?\s*4\s*[;:,]\s*14"),
    ("t(14;16)", r"t\s*\(?\s*14\s*[;:,]\s*16"),
    ("t(11;14)", r"t\s*\(?\s*11\s*[;:,]\s*14"),
    ("1q21",     r"1\s*q\s*21|gain\s*\(?\s*1q|amp\s*\(?\s*1q"),
    ("TP53",     r"\bTP53\b|\bp53\b"),
]


def _kelime(kalip, metin, buyuk_kucuk_onemli=False):
    """Kisaltmalar sozcuk sinirinda aranmali.

    'Rd' iki harf; sinirsiz aranirsa Turkce metinde her yerde tutar. Rejim
    kisaltmalari ayrica buyuk/kucuk harfe duyarli araniyor - 'rd' rastgele bir
    hece, 'Rd' bir rejim.
    """
    bayrak = 0 if buyuk_kucuk_onemli else re.I
    return re.search(r"(?<![A-Za-z0-9])" + kalip + r"(?![A-Za-z0-9])",
                     metin, bayrak) is not None


def analiz(soru):
    """Sorudan varlik cikar.

    Adim 1 (tespit) ve 2 (normalizasyon) burada birlikte oluyor: ilac_bul
    zaten marka adini INN'e ceviriyor (Tecvayli -> Teclistamab, Kyprolis ->
    Carfilzomib), cunku ILAC sozlugunun anahtari INN, degeri varyant listesi.
    """
    ilac, atc = ilac_bul(soru)
    ilac, atc = list(ilac), list(atc)

    rejim = {}
    for kis, bilesen in REJIM.items():
        if _kelime(re.escape(kis), soru, buyuk_kucuk_onemli=True):
            rejim[kis] = bilesen
            for inn in bilesen:
                if inn not in ilac:
                    ilac.append(inn)
                    atc.append(ILAC[inn][1])

    sinif = {}
    for kalip, uyeler in SINIF.items():
        if re.search(kalip, soru, re.I):
            sinif[kalip.split("|")[0]] = uyeler
            for inn in uyeler:
                if inn not in ilac:
                    ilac.append(inn)
                    atc.append(ILAC[inn][1])

    kisaltma = [(k, v) for k, v in KISALTMA.items() if _kelime(re.escape(k), soru)]
    sitogenetik = [ad for ad, k in SITOGENETIK if re.search(k, soru, re.I)]
    hastalik = [ad for ad, anahtar in HASTALIK
                if any(x in soru.lower() for x in anahtar)]

    return dict(ilac=ilac, atc=atc, rejim=rejim, sinif=sinif, kisaltma=kisaltma,
                sitogenetik=sitogenetik, hastalik=hastalik)


def genislet(soru, sonuc=None):
    """Sorguyu leksik arama icin zenginlestir.

    Yalnizca BM25 icin. Dense tarafta ham soru kullaniliyor: gomme modelleri
    dogal cumleyle egitildi, sorguyu anahtar kelime yiginina cevirmek vektoru
    bozar. Eklenenler: INN'in Ingilizce adi, ATC kodu, kisaltmanin acilimi.
    """
    s = sonuc or analiz(soru)
    ek = list(s["ilac"]) + list(s["atc"])
    ek += [v for _, v in s["kisaltma"]]
    ek += [b for bilesenler in s["rejim"].values() for b in bilesenler]
    return (soru + " " + " ".join(ek)).strip()


def boost_uygula(sirali, chunks, ilaclar):
    """Sirayi ilac uyumuna gore yeniden dizer. Hicbir aday atilmaz.

    A: sorudaki ilacla etiketli / B: etiketsiz / C: yalnizca baska ilacla
    etiketli. Kume icinde ozgun sira korunur, yani retriever'in karari
    ilac uyumu esitken hala gecerli.
    """
    if not ilaclar:
        return sirali
    hedef = set(ilaclar)
    a, b, c = [], [], []
    for i in sirali:
        etiket = set(chunks[i]["metadata"].get("drug_names") or [])
        (a if etiket & hedef else b if not etiket else c).append(i)
    return a + b + c


if __name__ == "__main__":
    import json
    yol = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "_work", "eval", "golden_queries.json")
    for s in json.load(open(yol, encoding="utf-8")):
        r = analiz(s["soru"])
        bulunan = {k: v for k, v in r.items() if v}
        print(f"{s['id']}: {s['soru'][:58]}")
        print(f"     {bulunan if bulunan else '- hicbir varlik bulunamadi'}")
