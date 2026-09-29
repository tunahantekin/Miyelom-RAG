#!/usr/bin/env python
"""Bolum numaralarini yapisal markdown basligina cevirir (Document Enrichment).

Neden gerekli: parser cikti olarak duz metin veya tek seviye baslik uretiyor.
Structural Validator'in bolum bazli kontrolleri (dipnot isim uzayi, tablo
sahipligi) ve chunking katmani bir BOLUM OMURGASI olmadan calisamiyor.

Neden sozluk tabanli: etiketlerde numarali talimat listeleri var
("1. Flakonu buzdolabindan cikarin", "2. Sulandirin"). Sadece "satir basinda
sayi" arayan bir kural bunlari baslik yapar ve belgeyi bozar. Bu yuzden
numara TEK BASINA yeterli sayilmaz; basligin kanonik bolum adiyla eslesmesi
sartlanir. Boylece yanlis pozitif pratikte sifira iner.

Kaynak dosyalar degistirilmez: _work/parsed -> _work/enriched.

Ek kazanc: kanonik bolum kumesi bilindigi icin EKSIK BOLUM tespit edilebilir.
"4.2 Pozoloji yok" bulgusu, hacim oranindan cok daha keskin bir kalite sinyali:
belge acilir, uzunlugu makul, ama doz bolumu kayiptir.

Calistirma:
    python _scripts/enrich_sections.py
    python _scripts/enrich_sections.py --sinif fda --limit 3 --kuru
"""
import argparse, json, os, re, sys, unicodedata
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))
from plog import log

GIRDI = os.path.join(ROOT, "_work", "parsed")
CIKTI = os.path.join(ROOT, "_work", "enriched")
RAPOR = os.path.join(ROOT, "_logs", "enrich_report.json")

# --- Kanonik bolum sozlukleri -------------------------------------------------
# numara -> o bolum basliginda GECMESI GEREKEN anahtar sozcuklerden en az biri.
# Anahtarlar normalize edilmis halde (kucuk harf, aksansiz, sadece harf/rakam/bosluk).

TR_SMPC = {
    "1":   ["beseri tibbi urunun adi", "urunun adi"],
    "2":   ["kalitatif", "bilesim"],
    "3":   ["farmasotik form"],
    "4":   ["klinik ozellik"],
    "4.1": ["terapotik endikasyon", "endikasyon"],
    "4.2": ["pozoloji"],
    "4.3": ["kontrendikasyon"],
    "4.4": ["uyari", "onlem"],
    "4.5": ["etkilesim"],
    "4.6": ["gebelik", "laktasyon"],
    "4.7": ["arac ve mak", "makine kullan", "makina kullan"],
    "4.8": ["istenmeyen etki"],
    "4.9": ["doz asimi"],
    "5":   ["farmakolojik ozellik"],
    "5.1": ["farmakodinamik"],
    "5.2": ["farmakokinetik"],
    "5.3": ["klinik oncesi"],
    "6":   ["farmasotik ozellik"],
    "6.1": ["yardimci madde"],
    "6.2": ["gecimsizlik"],
    "6.3": ["raf omru"],
    "6.4": ["saklama"],
    "6.5": ["ambalaj"],
    "6.6": ["imha", "arta kalan", "beseri tibbi urunden"],
    "7":   ["ruhsat sahibi"],
    "8":   ["ruhsat numara"],
    "9":   ["ilk ruhsat"],
    "10":  ["yenilenme"],
}

EN_SMPC = {
    "1":   ["name of the medicinal product"],
    "2":   ["qualitative and quantitative composition"],
    "3":   ["pharmaceutical form"],
    "4":   ["clinical particulars"],
    "4.1": ["therapeutic indications"],
    "4.2": ["posology"],
    "4.3": ["contraindications"],
    "4.4": ["special warnings"],
    "4.5": ["interaction with other"],
    "4.6": ["fertility pregnancy", "pregnancy and lactation"],
    "4.7": ["ability to drive"],
    "4.8": ["undesirable effects"],
    "4.9": ["overdose"],
    "5":   ["pharmacological properties"],
    "5.1": ["pharmacodynamic"],
    "5.2": ["pharmacokinetic"],
    "5.3": ["preclinical safety"],
    "6":   ["pharmaceutical particulars"],
    "6.1": ["list of excipients"],
    "6.2": ["incompatibilities"],
    "6.3": ["shelf life"],
    "6.4": ["special precautions for storage"],
    "6.5": ["nature and contents"],
    "6.6": ["special precautions for disposal", "disposal"],
}

# FDA Prescribing Information ust seviye bolumleri sabittir; alt bolum BASLIKLARI
# urune gore degisir ("14.1 Relapsed or Refractory Multiple Myeloma" gibi),
# bu yuzden alt bolumler sozlukle degil EBEVEYN BAGLAMI ile dogrulanir.
FDA_UST = {
    "1":  ["indications and usage"],
    "2":  ["dosage and administration"],
    "3":  ["dosage forms and strengths"],
    "4":  ["contraindications"],
    "5":  ["warnings and precautions"],
    "6":  ["adverse reactions"],
    "7":  ["drug interactions"],
    "8":  ["use in specific populations"],
    "9":  ["drug abuse and dependence"],
    "10": ["overdosage"],
    "11": ["description"],
    "12": ["clinical pharmacology"],
    "13": ["nonclinical toxicology"],
    "14": ["clinical studies"],
    "15": ["references"],
    "16": ["how supplied", "storage and handling"],
    "17": ["patient counseling"],
}

# Bu bolumler urune gore hic yazilmayabilir; yoklugu belge kusuru DEGILDIR.
# (Karfilzomib gibi bir onkoloji urununde "Drug Abuse and Dependence" bulunmaz.)
OPSIYONEL = {
    "fda_pi": {"7", "9", "10", "15"},
    "eu_smpc_tr": set(),
    "eu_smpc_en": set(),
}

# --- Yardimcilar --------------------------------------------------------------

# "# **4.2 Pozoloji ve uygulama sekli**" / "4.2. Pozoloji" / "**5.1 Farmakodinamik**"
# Numara ile baslik ayri kalin bloklarda da olabiliyor: "# **4.2.** **Pozoloji**".
# Bu yuzden ayrac, bosluk YA DA kapanan kalin isareti olarak tanimli.
SATIR = re.compile(
    r"^[ \t]*(?:#{1,6}[ \t]*)?(?:\*\*|__)?[ \t]*"
    r"(\d{1,2})(?:\.(\d{1,2}))?\.?"
    r"(?:[ \t]+|(?:\*\*|__)[ \t]*)"
    r"([^\n]{2,110}?)"
    r"[ \t]*(?:\*\*|__)?[ \t]*:?[ \t]*$"
)

# Parser yer yer vurgu etiketi birakiyor (<mark>, <u>); baslik eslesmesini bozar.
ETIKET = re.compile(r"</?[a-z][a-z0-9]*>")

# Satir icinde bolum numarasi: "4", "4.2", "4.2." - versiyon/tarih/dozdan ayrilsin
# diye once ve sonra baska rakam olmamali.
NUM_ICI = re.compile(r"(?<![\d.,/-])(\d{1,2})(?:\.(\d{1,2}))?\.?(?![\d.,/%-])")

# "bkz. Bolum 4.4", "see Section 2.1" - bunlar capraz atif, baslik degil.
ATIF_ONEK = re.compile(r"(bkz|b[oö]l[uü]m|kisim|k[ıi]s[ıi]m|see|section|tablo|table)"
                       r"[\s.:*]*$", re.I)


def normalize(s):
    """Turkce noktali I ve aksanlar eslesmeyi bozuyor; sade forma indir."""
    s = s.replace("İ", "i").replace("I", "ı").replace("̇", "")
    s = s.lower().replace("ı", "i")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def sinifla(ad):
    # Yalnizca urun etiketleri (PI) numarali bolum semasi tasir; Orange Book gibi
    # diger FDA belgeleri bu semaya uymaz, kanonik kume onlara uygulanamaz.
    if "__fda__labels__" in ad:
        return "fda_pi"
    if "__ema__" in ad:
        return "eu_smpc_en"
    if "__titck__kub__" in ad:
        return "eu_smpc_tr"
    return None


def sozluk(sinif):
    return {"eu_smpc_tr": TR_SMPC, "eu_smpc_en": EN_SMPC, "fda_pi": FDA_UST}[sinif]


# Tek basina bolum numarasi tasiyan satir: "4.1", "**6.**", "## 5."
SADECE_NUM = re.compile(r"^[ \t]*(?:#{1,6}[ \t]*)?(?:\*\*|__)?[ \t]*"
                        r"\d{1,2}(?:\.\d{1,2})?\.?[ \t]*(?:\*\*|__)?[ \t]*$")


def on_isle(metin):
    """Numarasi ve basligi ayri satirlara dusmus bolumleri birlestirir.

    Duz metin cikaricisi PDF'teki satir kirilimini oldugu gibi koruyor:
        4.1
        Terapotik endikasyonlar
    Iki satir ayri kaldiginda numaradan sonrasi bos gorunuyor ve bolum
    bulunamiyordu. Birlestirme baslik terfisini garanti etmez; sozluk
    eslesmesi yine sartlanir.
    """
    sat, out, i = metin.split("\n"), [], 0
    while i < len(sat):
        if SADECE_NUM.match(sat[i]) and i + 1 < len(sat) and sat[i + 1].strip():
            out.append(sat[i].rstrip() + " " + sat[i + 1].strip())
            i += 2
        else:
            out.append(sat[i])
            i += 1
    return "\n".join(out)


def temizle(s):
    return ETIKET.sub("", re.sub(r"\*\*|__|#|>", "", s)).strip(" :*\t")


def aday_bul(metin, sinif):
    """Satir icinde kanonik bolum baslarini tarar.

    Satir BASI kurali yetmiyor, cunku parser iki kusur uretiyor:
      - iki basligi tek satira yapistiriyor:
        "## 4 KLINIK OZELLIKLER 4.1 Terapotik endikasyonlar"
      - basligi sayfa altbilgisinin icine gomuyor:
        "> **Belge Dogrulama Kodu: ... 6. FARMASOTIK OZELLIKLER**"
    Ikisinde de baslik satirin ortasinda kaliyor ve gorunmez oluyordu.

    Yanlis pozitife karsi iki kilit: (1) kanonik bolum adi numaradan sonraki
    ilk ANAHTAR_UZAKLIK karakter icinde gecmeli, (2) numaranin onunde capraz
    atif kalibi ("bkz. Bolum 5.1", "see Section 2.1") olmamali.

    Doner: [(satir_indeksi, [(sutun, numara, baslik), ...])]
    """
    sz = sozluk(sinif)
    adaylar = []
    for i, ln in enumerate(metin.split("\n")):
        vurus = []
        for m in NUM_ICI.finditer(ln):
            ust, alt = m.group(1), m.group(2)
            num = f"{ust}.{alt}" if alt else ust
            if ATIF_ONEK.search(ln[max(0, m.start() - 24):m.start()]):
                continue
            kalan = temizle(ln[m.end():])
            nk = normalize(kalan)
            if not nk:
                continue
            if num in sz:
                # Anahtar sozcuk basligin basinda olmak zorunda degil ("Ozel
                # kullanim UYARILARI ve onlemleri"), ama numaraya yakin olmali;
                # uzakta gecen bir kelime govde metnidir, baslik degil.
                if any(0 <= nk.find(k) <= ANAHTAR_UZAKLIK for k in sz[num]):
                    vurus.append((m.start(), num, kalan))
            elif sinif == "fda_pi" and alt and ust in FDA_UST and m.start() == 0:
                # FDA alt bolum basliklari urune gore degisiyor, sozlukle
                # dogrulanamiyor; bu yuzden yalnizca satir basinda ve
                # cumle gibi durmuyorsa kabul edilir.
                if kalan.rstrip().endswith(".") or len(kalan) > 70:
                    continue
                if len(kalan.split()) > 9:
                    continue
                vurus.append((m.start(), num, kalan))
        if vurus:
            adaylar.append((i, vurus))
    return adaylar


def son_gecisi_sec(adaylar):
    """Ayni numara birden fazla yerde gecebilir.

    FDA PI belgeleri basta tam bir icindekiler listesi tasiyor; oradaki satirlar
    da desene uyuyor. Govdedeki gercek bolum her zaman SONRA geliyor, bu yuzden
    her numaranin son gecisi baslik yapilir, oncekiler duz metin kalir.
    """
    son = {}
    for i, vurus in adaylar:
        for sutun, num, baslik in vurus:
            son[num] = (i, sutun, num, baslik)
    return sorted(son.values())


ANAHTAR_UZAKLIK = 40      # numaradan sonra kanonik sozcuk en gec buraya kadar
BASLIK_AZAMI = 90          # bunu asan kuyruk baslik degil govde metnidir


def uygula(metin, secili):
    """Secilen bolum baslarini gercek markdown basligina cevirir.

    Bir satirda birden fazla bolum bası olabilir; satir parcalanir. Numaradan
    onceki metin (altbilgi, onceki paragrafin kuyrugu) kaybolmasin diye ayri
    satir olarak korunur.
    """
    satirlar = metin.split("\n")
    gruplu = defaultdict(list)
    for i, sutun, num, baslik in secili:
        gruplu[i].append((sutun, num, baslik))

    for i, vurus in gruplu.items():
        vurus.sort()
        ln, yeni = satirlar[i], []
        onek = temizle(ln[:vurus[0][0]])
        if len(onek) > 3:
            yeni.append(onek)
        for k, (sutun, num, baslik) in enumerate(vurus):
            son = vurus[k + 1][0] if k + 1 < len(vurus) else len(ln)
            # Baslik metni bir sonraki bolum basina kadar uzanir; numaranin
            # kendi uzunlugu kadarini atlayarak yeniden kesiyoruz.
            ham = temizle(ln[sutun:son])
            ham = re.sub(r"^\d{1,2}(?:\.\d{1,2})?\.?\s*", "", ham)
            kuyruk = ""
            if len(ham) > BASLIK_AZAMI:
                kes = ham.rfind(" ", 0, BASLIK_AZAMI)
                ham, kuyruk = ham[:kes], ham[kes:].strip()
            seviye = "##" if "." not in num else "###"
            yeni.append(f"{seviye} {num} {ham}".rstrip())
            if kuyruk:
                yeni.append(kuyruk)
        satirlar[i] = "\n".join(yeni)
    return "\n".join(satirlar)


def oku(yol):
    return open(yol, encoding="utf-8", errors="replace").read()


def yaz(ad, metin):
    os.makedirs(CIKTI, exist_ok=True)
    with open(os.path.join(CIKTI, ad), "w", encoding="utf-8") as f:
        f.write(metin)


def islem(yol, kuru=False):
    ad = os.path.basename(yol)
    sinif = sinifla(ad)
    if not sinif:
        # Kanonik semasi olmayan belge (kilavuz, Orange Book, SUT...). Yine de
        # kopyalanir: _work/enriched tum arsivi temsil eden tek asama olsun,
        # dogrulama arsivin bir kismini gormeden gecmesin.
        if not kuru:
            yaz(ad, oku(yol))
        return None
    metin = on_isle(oku(yol))
    secili = son_gecisi_sec(aday_bul(metin, sinif))
    bulunan = {n for _, _, n, _ in secili}
    beklenen = set(sozluk(sinif))
    sirala = lambda s: sorted(s, key=lambda x: [int(p) for p in x.split(".")])
    eksik = sirala(beklenen - bulunan - OPSIYONEL[sinif])
    eksik_ops = sirala((beklenen - bulunan) & OPSIYONEL[sinif])

    if not kuru:
        yaz(ad, uygula(metin, secili))
    return dict(dosya=ad, sinif=sinif, terfi=len(secili),
                bulunan=sirala(bulunan), eksik=eksik, eksik_opsiyonel=eksik_ops)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sinif", help="fda / ema / titck ad filtresi")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--kuru", action="store_true", help="yazma, sadece raporla")
    a = ap.parse_args()

    dosyalar = sorted(f for f in os.listdir(GIRDI) if f.endswith(".md"))
    if a.sinif:
        dosyalar = [f for f in dosyalar if f"__{a.sinif}__" in f]
    if a.limit:
        dosyalar = dosyalar[:a.limit]

    raporlar, atlanan = [], 0
    for f in dosyalar:
        r = islem(os.path.join(GIRDI, f), a.kuru)
        if r is None:
            atlanan += 1
            continue
        raporlar.append(r)

    if not a.kuru:
        json.dump(raporlar, open(RAPOR, "w", encoding="utf-8"),
                  indent=1, ensure_ascii=False)

    say = defaultdict(lambda: [0, 0, 0])          # sinif -> [dosya, terfi, eksik]
    eksik_dagilim = defaultdict(lambda: defaultdict(int))
    for r in raporlar:
        s = say[r["sinif"]]
        s[0] += 1; s[1] += r["terfi"]; s[2] += len(r["eksik"])
        for e in r["eksik"]:
            eksik_dagilim[r["sinif"]][e] += 1

    print(f"islenen {len(raporlar)} dosya, kapsam disi {atlanan}")
    for s, (d, t, e) in sorted(say.items()):
        print(f"  {s:12s} dosya {d:4d}  terfi {t:5d}  eksik bolum {e:4d}"
              f"  (dosya basi {t/d:.1f} baslik)")
    for s, dag in sorted(eksik_dagilim.items()):
        ilk = sorted(dag.items(), key=lambda x: -x[1])[:8]
        print(f"  en cok eksik [{s}]: " +
              ", ".join(f"{n}x{v}" for n, v in ilk))
    if not a.kuru:
        log("bolum zenginlestirme", "enrich",
            f"{len(raporlar)} dosya, " +
            ", ".join(f"{s}:{v[1]}" for s, v in sorted(say.items())))


if __name__ == "__main__":
    main()
