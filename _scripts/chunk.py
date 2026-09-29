#!/usr/bin/env python
"""Yapi farkindali chunk uretici - RAG icin JSON chunk nesneleri.

Girdi: _work/enriched/*.md (bolum omurgasi kurulmus) + elle hazirlanmis NCCN dosyasi.
Cikti: _work/chunks/chunks.json

TASARIM KARARLARI

1. Sinir = baslik. Etiketlerde her numarali SmPC/PI bolumu (4.1, 4.2, ...) yeni
   chunk baslatir; NCCN'de her sayfa kodu (MYEL-4, MYEL-G (2 of 5)) yeni chunk
   baslatir. Bolum ~800 token'i asarsa paragraf sinirindan alt bolunur ve
   parent_id ile ana bolume baglanir. Cumle ortasindan asla bolunmez.

2. Tablolar atomik. Tablo hicbir kosulda bolunmez, ustune baglam satiri eklenir.
   Cok uzun tablo tek chunk olarak kalir ve COK_BUYUK_TABLO isaretlenir - cunku
   bolmek satirla baslik arasindaki bagi koparir, ki dozaj tablosunda bu hasta
   guvenligi sorunudur.

3. Dipnot asla tek basina chunk olmaz. Ait oldugu bolumun sonuna
   "### ASSOCIATED FOOTNOTES:" basligi altinda eklenir. NCCN'de kosul bilgisi
   (kime uygulanir, hangi bobrek fonksiyonunda) dipnotta duruyor; koparsa
   rejim kosulsuz gorunur.

4. Ortusme yalnizca ayni bolum icindeki ardisik metin parcalari arasinda ve
   ~40 token. Tablo ve karar dugumunde ortusme YASAK.

5. Akis semasi. Gorsel karar agacini IF/THEN kuraline cevirmek anlam cikarimi
   ister; bu script uretmez, yalnizca dal kalibi tasiyan chunk'i
   REQUIRES_FLOWCHART_REVIEW ile isaretler. Uydurma karar kurali uretmek,
   eksik kural birakmaktan daha tehlikelidir.

Calistirma:
    python _scripts/chunk.py
    python _scripts/chunk.py --limit 5 --ornek
"""
import argparse, hashlib, json, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))
from plog import log

GIRDI = os.path.join(ROOT, "_work", "enriched")
NCCN_ELLE = os.path.join(ROOT, "layer1_clinical", "nccn", "nccn_myeloma_manual.md")
CIKTI_DIZIN = os.path.join(ROOT, "_work", "chunks")
CIKTI = os.path.join(CIKTI_DIZIN, "chunks.json")

AZAMI_TOKEN = 800          # bunu asan bolum alt bolunur
ORTUSME_TOKEN = 40         # yalnizca ardisik metin parcalari arasinda
TABLO_UYARI_TOKEN = 1500   # bolunemeyecek kadar buyuk tablo: isaretle, bolme


# --- Ilac sozlugu -------------------------------------------------------------
# Gecici konum: bu sozluk buyudukce ayri module tasinacak (INN -> Turkce varyant
# -> ATC -> ruhsat durumu). Turkce metinlerde etken madde ve urun adi farkli
# yaziliyor, bu yuzden her INN icin varyant listesi tutulur.
ILAC = {
    "Bortezomib":      (["bortezomib", "velcade", "borcade", "boractib", "bortrel"], "L01XG01"),
    "Carfilzomib":     (["carfilzomib", "karfilzomib", "kyprolis", "cafizo"], "L01XG02"),
    "Ixazomib":        (["ixazomib", "iksazomib", "ninlaro"], "L01XG03"),
    "Lenalidomide":    (["lenalidomide", "lenalidomid", "revlimid"], "L04AX04"),
    "Thalidomide":     (["thalidomide", "talidomid"], "L04AX02"),
    "Pomalidomide":    (["pomalidomide", "pomalidomid", "imnovid", "pomalyst"], "L04AX06"),
    "Daratumumab":     (["daratumumab", "darzalex"], "L01FC01"),
    "Isatuximab":      (["isatuximab", "isatuksimab", "sarclisa"], "L01FC02"),
    "Elotuzumab":      (["elotuzumab", "empliciti"], "L01FX08"),
    "Selinexor":       (["selinexor", "selineksor", "xpovio", "nexpovio"], "L01XX66"),
    "Melphalan":       (["melphalan", "melfalan", "alkeran", "eriolan"], "L01AA03"),
    "Cyclophosphamide": (["cyclophosphamide", "siklofosfamid", "endoxan"], "L01AA01"),
    "Dexamethasone":   (["dexamethasone", "deksametazon"], "H02AB02"),
    "Prednisone":      (["prednisone", "prednizon"], "H02AB07"),
    "Doxorubicin":     (["doxorubicin", "doksorubisin"], "L01DB01"),
    "Bendamustine":    (["bendamustine", "bendamustin"], "L01AA09"),
    "Venetoclax":      (["venetoclax", "venetoklaks"], "L01XX52"),
    "Teclistamab":     (["teclistamab", "teklistamab", "tecvayli"], "L01FX28"),
    "Talquetamab":     (["talquetamab", "talkuetamab", "talvey"], "L01FX31"),
    "Elranatamab":     (["elranatamab", "elrexfio"], "L01FX32"),
    "Belantamab mafodotin": (["belantamab", "blenrep"], "L01FX15"),
    "Idecabtagene vicleucel": (["idecabtagene", "idekabtajen", "abecma"], "L01XL07"),
    "Ciltacabtagene autoleucel": (["ciltacabtagene", "siltakabtajen", "carvykti"], "L01XL08"),
    "Zoledronic acid": (["zoledronic", "zoledronik"], "M05BA08"),
    "Pamidronate":     (["pamidronate", "pamidronat"], "M05BA03"),
    "Denosumab":       (["denosumab", "xgeva", "prolia"], "M05BX04"),
    "Plerixafor":      (["plerixafor", "pleriksafor", "mozobil"], "L03AX16"),
    "Filgrastim":      (["filgrastim", "g-csf"], "L03AA02"),
}


def token_say(s):
    """Kaba token tahmini. Tam tokenizer bagimliligi eklemeye degmez;
    sinir kararlari icin +-%15 yeterli."""
    return max(1, int(len(s) / 3.6))


def kimlik(*parca):
    return hashlib.sha1("|".join(str(p) for p in parca).encode("utf-8")).hexdigest()[:16]


# --- Belge sinifi -------------------------------------------------------------

def sinifla(ad):
    if "__titck__kub__" in ad:
        return "TITCK_KUB"
    if "__fda__labels__" in ad:
        return "FDA_SMPC"
    if "__ema__" in ad:
        return "EMA_SMPC"
    if "__sut__" in ad or "__ek4__" in ad:
        return "SUT"
    if "nccn" in ad:
        return "NCCN"
    return "OTHER"


def belge_adi(ad):
    """BENZERSIZ belge kimligi.

    Onceden yalnizca dosya adinin son parcasi kullaniliyordu; farkli belgeler
    ayni ada dusuyordu (birkac KUB dogrudan "KUB" oluyordu) ve 160 belge 150
    kimlige siserek gruplamayi bozuyordu. Katman oneki atilir ama gerisi korunur.
    """
    p = ad[:-3].split("__") if ad.endswith(".md") else ad.split("__")
    return "__".join(p[1:]) if len(p) > 1 else p[0]


def belge_etiket(ad):
    """Insan icin kisa ad; benzersiz olmak zorunda degil (baglam satiri, alinti)."""
    p = ad[:-3].split("__") if ad.endswith(".md") else ad.split("__")
    return p[-1] if len(p) > 1 else p[0]


# Belge surumu. Klinik bilgi surumsuz kullanilmamali: hangi NCCN surumunun,
# hangi tarihli KUB'un, hangi SUT degisikliginin cevap verdigi gorunmeli.
SURUM_KALIP = [
    ("nccn", re.compile(r"Version\s+(\d+\.\d{4})")),
    ("fda", re.compile(r"Revised:?\s*\**\s*(\d{1,2}/\d{4})", re.I)),
    ("kub_yenileme", re.compile(r"Ruhsat\s+yenileme\s+tarihi:?\s*<?/?u?>?\s*"
                                r"(\d{2}[./]\d{2}[./]\d{4})", re.I)),
    ("kub_ilk", re.compile(r"İlk\s+ruhsat\s+tarihi:?\s*<?/?u?>?\s*"
                           r"(\d{2}[./]\d{2}[./]\d{4})", re.I)),
]
SUT_RG = re.compile(r"RG[-:\s]*(\d{2}[./]\d{2}[./]\d{4})")


def surum_bul(metin):
    """(surum, kaynak) - bulunamazsa (None, None).

    SUT'ta en GUNCEL Resmi Gazete tarihi alinir; belge boyunca birikmis
    degisiklik notlari var ve ilkini almak belgeyi eski gosterir.
    """
    rg = SUT_RG.findall(metin)
    if rg:
        return max(rg, key=lambda d: d.replace(".", "/").split("/")[::-1]), "sut_rg"
    for ad, k in SURUM_KALIP:
        m = k.search(metin)
        if m and m.group(1).strip():
            return m.group(1), ad
    return None, None


# --- Metin cozumleme ----------------------------------------------------------

SAYFA = re.compile(r"<!--\s*sayfa\s+(\d+)\s*-->")
BASLIK = re.compile(r"(?m)^(#{2,3})\s+(\S+)\s*(.*)$")
DIPNOT_TANIM = re.compile(r"(?m)^\s*[-*]?\s*\[\^([^\]]+)\]\s*:\s*(.+)$")
DIPNOT_ISARET = re.compile(r"\[\^([^\]]+)\]")
DAL = re.compile(r"(?mi)^\s*[-*•]\s*(?:for\s+.+?,\s*)?see\s+")


def sayfa_haritasi(metin):
    """[(karakter konumu, kaynak PDF sayfasi)] - isaret yoksa bos."""
    return [(m.start(), int(m.group(1))) for m in SAYFA.finditer(metin)]


def sayfa_bul(harita, konum):
    s = None
    for k, n in harita:
        if k <= konum:
            s = n
        else:
            break
    return s


def bolumlere_ayir(metin):
    """[(numara, baslik, govde, konum)] - baslik yoksa tek parca doner."""
    b = list(BASLIK.finditer(metin))
    if not b:
        return [(None, None, metin, 0)]
    parcalar = []
    if b[0].start() > 0:
        on = metin[:b[0].start()].strip()
        if token_say(on) > 20:
            parcalar.append((None, "Giriş", on, 0))
    for i, m in enumerate(b):
        son = b[i + 1].start() if i + 1 < len(b) else len(metin)
        parcalar.append((m.group(2), m.group(3).strip() or m.group(2),
                         metin[m.end():son].strip(), m.start()))
    return parcalar


def tablo_ayikla(govde):
    """Govdeyi sirayla [(tur, metin)] parcalarina boler; tur: 'metin' | 'tablo'."""
    sat, out, tampon, i = govde.split("\n"), [], [], 0
    while i < len(sat):
        if sat[i].lstrip().startswith("|"):
            if tampon:
                out.append(("metin", "\n".join(tampon).strip()))
                tampon = []
            blok = []
            while i < len(sat) and sat[i].lstrip().startswith("|"):
                blok.append(sat[i])
                i += 1
            out.append(("tablo", "\n".join(blok)))
        else:
            tampon.append(sat[i])
            i += 1
    if tampon:
        out.append(("metin", "\n".join(tampon).strip()))
    return [(t, m) for t, m in out if m.strip()]


def paragraf_bol(metin, azami=AZAMI_TOKEN):
    """Paragraf sinirindan boler; tek paragraf sinirdan buyukse cumleye iner.
    Cumle ortasindan asla bolunmez."""
    if token_say(metin) <= azami:
        return [metin]
    parcalar, cur = [], []
    for p in re.split(r"\n\s*\n", metin):
        if not p.strip():
            continue
        if token_say(p) > azami:
            if cur:
                parcalar.append("\n\n".join(cur))
                cur = []
            c = []
            for s in re.split(r"(?<=[.!?])\s+", p):
                if token_say(" ".join(c + [s])) > azami and c:
                    parcalar.append(" ".join(c))
                    c = [s]
                else:
                    c.append(s)
            if c:
                parcalar.append(" ".join(c))
        elif token_say("\n\n".join(cur + [p])) > azami and cur:
            parcalar.append("\n\n".join(cur))
            cur = [p]
        else:
            cur.append(p)
    if cur:
        parcalar.append("\n\n".join(cur))
    return parcalar


def ortusme_ekle(parcalar):
    """Ardisik metin parcalari arasina ~ORTUSME_TOKEN kadar kuyruk tasir.
    Tasinan sey son CUMLELERDIR, kesik metin degil."""
    out = []
    for i, p in enumerate(parcalar):
        if i == 0:
            out.append(p)
            continue
        onceki = re.split(r"(?<=[.!?])\s+", parcalar[i - 1].strip())
        kuyruk, t = [], 0
        for s in reversed(onceki):
            if t + token_say(s) > ORTUSME_TOKEN:
                break
            kuyruk.insert(0, s)
            t += token_say(s)
        out.append((" ".join(kuyruk) + "\n\n" + p) if kuyruk else p)
    return out


# --- Metadata -----------------------------------------------------------------

def ilac_bul(metin):
    dusuk = metin.lower()
    adlar, atc = [], []
    for inn, (varyant, kod) in ILAC.items():
        if any(v in dusuk for v in varyant):
            adlar.append(inn)
            atc.append(kod)
    return adlar, atc


HASTALIK = [
    ("Multiple Myeloma", ["multipl miyelom", "multiple myeloma", "myeloma", "miyelom"]),
    ("Smoldering Myeloma", ["smoldering", "sessiz miyelom"]),
    ("MGUS", ["mgus", "monoclonal gammopathy", "monoklonal gammopati"]),
    ("Amyloidosis", ["amyloidosis", "amiloidoz"]),
    ("Solitary Plasmacytoma", ["solitary plasmacytoma", "soliter plazmasitom"]),
]


def hastalik_bul(metin):
    d = metin.lower()
    return [ad for ad, k in HASTALIK if any(x in d for x in k)]


def kardes_tanimlar(parcalar):
    """Sayfa kodu -> o kodun TUM parcalarindaki dipnot tanimlari.

    NCCN'de cok sayfali kodlarda (MYEL-E 1/2/3 of 3) isaret ilk sayfada
    kullanilip tanim son sayfada veriliyor. Tanimi yalnizca kendi bolumunde
    aramak, kosul bilgisini chunk'tan koparıyordu.
    """
    d = {}
    for numara, _, govde, _ in parcalar:
        if not numara:
            continue
        d.setdefault(numara, {}).update(
            {m.group(1): m.group(2).strip() for m in DIPNOT_TANIM.finditer(govde)})
    return d


def dipnot_toplama(govde, tam_bolum, kardes=None):
    """Bu parcada ATIF EDILEN dipnotlarin tanimlarini dondurur.

    Tanimlar bolumun sonunda toplu duruyor; parca bazinda yalnizca gercekten
    kullanilan isaretler eklenir ki her chunk tum dipnot listesini tasimasin.
    """
    tanim = dict(kardes or {})
    tanim.update({m.group(1): m.group(2).strip()
                  for m in DIPNOT_TANIM.finditer(tam_bolum)})
    if not tanim:
        return []
    kullanilan, gorulen = [], set()
    for m in DIPNOT_ISARET.finditer(govde):
        h = m.group(1)
        if h in tanim and h not in gorulen:
            gorulen.add(h)
            kullanilan.append((h, tanim[h]))
    return kullanilan


def govdeden_tanimlari_at(govde):
    """Dipnot TANIM satirlari govdeden cikarilir; ASSOCIATED FOOTNOTES altinda
    yeniden eklenecekler. Boylece tanim iki kez gecmez."""
    return re.sub(r"(?m)^\s*[-*]?\s*\[\^[^\]]+\]\s*:.*$", "", govde).strip()


def dipnot_ekle(icerik, dipnotlar):
    if not dipnotlar:
        return icerik
    return icerik + "\n\n### ASSOCIATED FOOTNOTES:\n" + \
        "\n".join(f"[^{h}]: {t}" for h, t in dipnotlar)


# --- Chunk uretimi ------------------------------------------------------------

def chunk_yap(kaynak_tur, dosya_adi, numara, baslik, icerik, sayfa,
              parent=None, tur="metin", ek_isaret=(), surum=None):
    isaret = list(ek_isaret)
    if tur == "tablo":
        isaret.append("CONTAINS_TABLE")
    if DAL.search(icerik):
        isaret.append("REQUIRES_FLOWCHART_REVIEW")
    if DIPNOT_ISARET.search(icerik) and "ASSOCIATED FOOTNOTES" not in icerik:
        isaret.append("REQUIRES_MANUAL_FOOTNOTE_AUDIT")
    ilaclar, atc = ilac_bul(icerik)
    return {
        "chunk_id": kimlik(dosya_adi, numara, baslik, icerik[:200], parent or ""),
        "parent_id": parent,
        "metadata": {
            "source_type": kaynak_tur,
            "document_name": belge_adi(dosya_adi),
            "document_label": belge_etiket(dosya_adi),
            "version": surum,
            "section_number": numara,
            "section_title": baslik,
            "page_number": sayfa,
            "disease": hastalik_bul(icerik),
            "drug_names": ilaclar,
            "atc_codes": atc,
            "parsing_flags": sorted(set(isaret)),
        },
        "content": icerik,
    }


def baglam_satiri(dosya_adi, numara, baslik):
    p = [belge_etiket(dosya_adi)]
    if numara:
        p.append(str(numara))
    if baslik and baslik != numara:
        p.append(baslik)
    return f"[CONTEXT: {' - '.join(p)}]"


def dosya_chunkla(yol):
    ad = os.path.basename(yol)
    kaynak_tur = sinifla(ad)
    metin = open(yol, encoding="utf-8", errors="replace").read()
    harita = sayfa_haritasi(metin)
    surum, _ = surum_bul(metin)
    chunks = []

    parcalar_tum = bolumlere_ayir(metin)
    kardes_map = kardes_tanimlar(parcalar_tum)

    for numara, baslik, govde, konum in parcalar_tum:
        # Bos govdeli bolum atlanamaz: parser yer yer baslik ile govdeyi ayni
        # satira dusuruyor ("### **~~CONTRAINDICATIONS~~** Patients with severe
        # hypersensitivity..."), o zaman icerik baslik alanina giriyor. Bos
        # govdede atlamak bu metni sessizce siliyordu.
        if not govde.strip():
            if baslik and len(baslik.strip(" *~#")) > 25:
                govde = baslik.strip()
            else:
                continue
        sayfa = sayfa_bul(harita, konum)
        tam_bolum = govde
        govde = govdeden_tanimlari_at(govde)
        if not govde:
            continue
        baslik_satiri = f"### {numara or ''} {baslik or ''}".strip()
        parcalar = tablo_ayikla(govde)

        # Bolum tek metin parcasi ve sinirin altindaysa: tek chunk, alt bolme yok.
        if len(parcalar) == 1 and parcalar[0][0] == "metin" \
                and token_say(parcalar[0][1]) <= AZAMI_TOKEN:
            icerik = baslik_satiri + "\n\n" + parcalar[0][1]
            chunks.append(chunk_yap(
                kaynak_tur, ad, numara, baslik,
                dipnot_ekle(icerik, dipnot_toplama(parcalar[0][1], tam_bolum, kardes_map.get(numara))), sayfa,
                surum=surum))
            continue

        # Cok parcali bolum: parent_id, bolumun ILK chunk'ini gosterir.
        # Once sentetik bir kimlik uretiliyordu, ama o kimlikte chunk yoktu;
        # 1370 chunk sahipsiz bir ebeveyne isaret ediyordu. parent_id ancak
        # gercekten var olan bir chunk'i gosterirse ise yarar.
        bolum_bas = len(chunks)
        for tur, m in parcalar:
            if tur == "tablo":
                isaret = ["CONTAINS_TABLE"]
                if token_say(m) > TABLO_UYARI_TOKEN:
                    isaret.append("COK_BUYUK_TABLO")
                icerik = baglam_satiri(ad, numara, baslik) + "\n\n" + m
                chunks.append(chunk_yap(
                    kaynak_tur, ad, numara, baslik,
                    dipnot_ekle(icerik, dipnot_toplama(m, tam_bolum, kardes_map.get(numara))), sayfa,
                    parent=None, tur="tablo", ek_isaret=isaret, surum=surum))
                continue
            for a in ortusme_ekle(paragraf_bol(m)):
                icerik = baslik_satiri + "\n\n" + a
                chunks.append(chunk_yap(
                    kaynak_tur, ad, numara, baslik,
                    dipnot_ekle(icerik, dipnot_toplama(a, tam_bolum, kardes_map.get(numara))), sayfa, surum=surum))
    return chunks


ASGARI_TOKEN = 120         # bundan kucuk metin chunk'i komsusuyla birlesir


def kucukleri_birlestir(chunks):
    """Ardisik kucuk METIN chunk'larini birlestirir.

    Kisa bolumler (bir cumlelik "EDITOR'S NOTE" gibi) tek baslarina chunk olunca
    aramada gurultu yapiyor. Birlesme yalnizca ayni belgede, ardisik ve ikisi de
    metin olan chunk'lar arasinda olur; TABLO asla birlesmez (atomikligi bozar),
    belge siniri asilmaz.
    """
    out = []
    for c in chunks:
        tablo = "CONTAINS_TABLE" in c["metadata"]["parsing_flags"]
        if out and not tablo:
            o = out[-1]
            ayni = (o["metadata"]["document_name"] == c["metadata"]["document_name"]
                    and "CONTAINS_TABLE" not in o["metadata"]["parsing_flags"])
            if ayni and token_say(o["content"]) < ASGARI_TOKEN \
                    and token_say(o["content"] + c["content"]) <= AZAMI_TOKEN:
                o["content"] += "\n\n" + c["content"]
                m, n = o["metadata"], c["metadata"]
                m["disease"] = sorted(set(m["disease"]) | set(n["disease"]))
                m["drug_names"] = sorted(set(m["drug_names"]) | set(n["drug_names"]))
                m["atc_codes"] = sorted(set(m["atc_codes"]) | set(n["atc_codes"]))
                m["parsing_flags"] = sorted(set(m["parsing_flags"]) |
                                            set(n["parsing_flags"]) | {"BIRLESTIRILDI"})
                if m["section_number"] != n["section_number"]:
                    m["section_title"] = f"{m['section_title']} + {n['section_title']}"
                continue
        out.append(c)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--ornek", action="store_true", help="ilk chunk'lari yazdir")
    a = ap.parse_args()

    dosyalar = [os.path.join(GIRDI, f) for f in sorted(os.listdir(GIRDI))
                if f.endswith(".md")]
    dosyalar.append(NCCN_ELLE)
    if a.limit:
        dosyalar = dosyalar[:a.limit]

    hepsi = []
    for y in dosyalar:
        hepsi += dosya_chunkla(y)
    hepsi = kucukleri_birlestir(hepsi)

    os.makedirs(CIKTI_DIZIN, exist_ok=True)
    json.dump(hepsi, open(CIKTI, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    tur = Counter(c["metadata"]["source_type"] for c in hepsi)
    bayrak = Counter(f for c in hepsi for f in c["metadata"]["parsing_flags"])
    tok = sorted(token_say(c["content"]) for c in hepsi)
    print(f"{len(hepsi)} chunk / {len(dosyalar)} belge")
    print("  kaynak turu:", dict(tur))
    print("  isaretler  :", dict(bayrak))
    print(f"  token: ortanca {tok[len(tok)//2]}, %90 {tok[int(len(tok)*0.9)]}, "
          f"azami {tok[-1]}")
    print(f"  ilac etiketli chunk: {sum(1 for c in hepsi if c['metadata']['drug_names'])}")
    print(f"  sayfa no'lu chunk  : {sum(1 for c in hepsi if c['metadata']['page_number'])}")
    print(f"  -> {CIKTI}")
    if a.ornek:
        for c in hepsi[:2]:
            print(json.dumps(c, ensure_ascii=False, indent=1)[:1100])
    log("chunking", "chunk", f"{len(hepsi)} chunk, {len(dosyalar)} belge")


if __name__ == "__main__":
    main()
