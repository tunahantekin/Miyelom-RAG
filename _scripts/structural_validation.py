#!/usr/bin/env python
"""Structural Validation - ground truth GEREKTIRMEYEN, deterministik tutarlilik kontrolu.

Ayni dosya -> ayni sonuc. Referans belgeyi okumaya gerek yok; belgenin kendi
icinde tutarli olup olmadigina bakilir. Bu yuzden tum arsive olceklenir ve
kaynak guncellendiginde regresyon testi olarak tekrar kosar.

Uc siddet seviyesi:
  ERROR  - kesin hata (kirik atif, cift dipnot tanimi, eksik dipnot)
  WARN   - buyuk ihtimalle hata (tablo sutun uyumsuzlugu, oksuz dipnot)
  REVIEW - deterministik tespit, olasiliksal yorum: insana git
           (ebeveynsiz dal dugumu = duzlesmis hiyerarsi suphesi)

Semantic dogrulama (karar dali eksik mi, rejim kaybolmus mu) BU DOSYANIN
KAPSAMI DISINDA - o ground truth ve insan hakemi ister.

Calistirma:
    python _scripts/structural_validation.py layer1_clinical/nccn/nccn_myeloma_manual.md
    python _scripts/structural_validation.py _work/parse_full
"""
import argparse, json, os, re, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))
from plog import log

CIKTI = os.path.join(ROOT, "_logs", "structural_validation.json")

# Dal dugumu kalibi: "For X, see Y" / "See Y". Bunlar bir ust kategoriye ait
# olmali; en ust seviyede ebeveynsiz duruyorlarsa hiyerarsi duzlesmis olabilir.
DAL_KALIP = re.compile(r"^\s*[-*•]\s*(?:for\s+.+?,\s*)?see\s+\[?[a-z]", re.I)


def bulgu(seviye, tur, detay, satir=None):
    return dict(seviye=seviye, tur=tur, detay=detay, satir=satir)


def satir_no(t, konum):
    return t.count("\n", 0, konum) + 1


def dipnot_kontrol(t, kardes_tanim=frozenset(), kardes_kullanim=frozenset()):
    """kardes_* : ayni sayfa kodunu paylasan diger parcalarda gecen isaretler.

    NCCN'de harfler her SAYFADA yeniden basliyor, bu yuzden cift tanim kontrolu
    sayfa bazinda kalmali. Ama MYEL-E gibi cok sayfali kodlarda isaret ilk
    sayfada kullanilip tanim son sayfada veriliyor; eksik/oksuz kontrolu bu
    yuzden kardes sayfalari da gormek zorunda.
    """
    b, tanim = [], {}
    for m in re.finditer(r"(?m)^\s*[-*]?\s*\[\^([^\]]+)\]\s*:", t):
        tanim.setdefault(m.group(1), []).append(satir_no(t, m.start()))

    kullanim, ilk = Counter(), {}
    for m in re.finditer(r"\[\^([^\]]+)\]", t):
        bas = t.rfind("\n", 0, m.start()) + 1
        if re.match(r"\s*[-*]?\s*\[\^[^\]]+\]\s*:", t[bas:bas + 60]):
            continue                       # tanim satirinin kendisi
        kullanim[m.group(1)] += 1
        ilk.setdefault(m.group(1), satir_no(t, m.start()))

    for h, n in sorted(kullanim.items()):
        if h not in tanim and h not in kardes_tanim:
            b.append(bulgu("ERROR", "missing_footnote",
                           f"[^{h}] metinde {n} kez kullanilmis, tanimi yok", ilk[h]))
    for h, sat in sorted(tanim.items()):
        if len(sat) > 1:
            b.append(bulgu("ERROR", "duplicate_footnote",
                           f"[^{h}] {len(sat)} kez tanimlanmis (satir {sat})", sat[0]))
        if h not in kullanim and h not in kardes_kullanim:
            b.append(bulgu("WARN", "orphan_footnote",
                           f"[^{h}] tanimlanmis ama hicbir yerden atif yok", sat[0]))

    tek = sorted(x for x in tanim if re.fullmatch(r"[a-z]", x))
    for i in range(len(tek) - 1):
        a, c = ord(tek[i]), ord(tek[i + 1])
        if c - a > 1:
            # NCCN sayfalari harflerin bir ALT KUMESINI kullanabiliyor (a,b,c,d,i,q gibi);
            # bosluk tek basina hata degil, sadece bakilmaya deger.
            b.append(bulgu("REVIEW", "footnote_gap",
                           f"dipnot harf dizisinde bosluk: {tek[i]} -> {tek[i+1]} "
                           f"(eksik: {''.join(chr(x) for x in range(a+1, c))})",
                           tanim[tek[i]][0]))
    return b


def atif_kontrol(t):
    b, capa = [], set()
    for m in re.finditer(r"(?m)^#{1,6}\s+(.+)$", t):
        s = m.group(1).strip().lower()
        capa.add(re.sub(r"[^a-z0-9]+", "-", s).strip("-"))
        k = re.match(r"([a-z]+-[0-9a-z]+)", s)          # "myel-g (4 of 5)" -> myel-g
        if k:
            capa.add(k.group(1))

    hedefler = set()
    for m in re.finditer(r"\[([^\]]{1,80})\]\(#([^)]+)\)", t):
        h = m.group(2).strip().lower()
        hedefler.add(h)
        if h not in capa:
            b.append(bulgu("ERROR", "broken_link",
                           f"'{m.group(1)}' -> #{h} : boyle bir bolum yok",
                           satir_no(t, m.start())))
    # Erisilebilirlik kontrolu yalnizca capa-bagi KULLANAN belgeler icin anlamli;
    # duz metne cevrilmis belgelerde her baslik "erisilemez" gorunur, bu gurultu.
    if hedefler:
        for c in sorted(capa):
            if re.fullmatch(r"[a-z]+-[0-9a-z]+", c) and c not in hedefler:
                b.append(bulgu("WARN", "unreachable_section",
                               f"'{c}' bolumune hicbir yerden bag yok"))
    return b


def tablo_kontrol(t):
    b, satirlar, i = [], t.split("\n"), 0
    while i < len(satirlar):
        if not satirlar[i].lstrip().startswith("|"):
            i += 1
            continue
        bas, blok = i, []
        while i < len(satirlar) and satirlar[i].lstrip().startswith("|"):
            blok.append(satirlar[i]); i += 1
        if len(blok) < 2:
            b.append(bulgu("WARN", "table_orphan_row",
                           "tek satirlik tablo parcasi", bas + 1))
            continue
        if not re.fullmatch(r"\s*\|[\s:|-]+\|\s*", blok[1]):
            b.append(bulgu("ERROR", "table_no_separator",
                           "tablo basligindan sonra ayrac satiri yok", bas + 2))
            continue
        n = blok[0].count("|")
        for k, s in enumerate(blok[2:], start=2):
            if s.count("|") != n:
                b.append(bulgu("WARN", "table_column_mismatch",
                               f"satirda {s.count('|')-1} hucre, baslikta {n-1}",
                               bas + k + 1))
    return b


def hiyerarsi_kontrol(t):
    b = []
    for ln, s in enumerate(t.split("\n"), start=1):
        if DAL_KALIP.match(s) and len(s) - len(s.lstrip()) == 0:
            b.append(bulgu("REVIEW", "orphan_branch_node",
                           f"dal dugumu en ust seviyede, ebeveyn kategori yok: "
                           f"{s.strip()[:70]}", ln))
    return b


SAYFA_KODU = re.compile(r"(?m)^###\s+\**\s*([A-Za-z]+-[0-9A-Za-z]+)")


def bolumler(t):
    """Dipnot isim uzayi SAYFA KODU bazlidir.

    NCCN her sayfada a,b,c'den yeniden basliyor, bu yuzden tum dosyayi tek uzay
    saymak sahte 'duplicate_footnote' uretiyordu. Ama tersi de dogru degil: bir
    sayfa kodu birden fazla ### bolume bolunmus olabiliyor ("MYEL-E (1 of 3)",
    "(2 of 3)", "(3 of 3)") ve tanimlarin tamami son parcada duruyor. Her parcayi
    ayri uzay saymak bu kez sahte 'missing_footnote' uretiyordu.
    Cozum: parca birimi sayfa olarak kalir, ama her parca hangi SAYFA KODUNA ait
    oldugunu da soyler; eksik/oksuz kontrolu kardes parcalari gorebilsin diye.

    Doner: [(ilk_satir, metin, sayfa_kodu)]
    """
    bas = []
    for m in re.finditer(r"(?m)^###\s+\S", t):
        k = SAYFA_KODU.match(t, m.start())
        bas.append((m.start(), k.group(1).lower() if k else None))
    if not bas:
        return [(1, t, None)]
    if bas[0][0]:
        bas = [(0, None)] + bas
    return [(satir_no(t, bas[i][0]),
             t[bas[i][0]: bas[i + 1][0] if i + 1 < len(bas) else len(t)],
             bas[i][1])
            for i in range(len(bas))]


ORAN_ESIGI = 0.5
_INDEKS = {}


def KAYNAK_INDEKS():
    """md dosya adi -> kaynak PDF yolu.

    Ad uzerinden yol tahmin etmek ise yaramiyor: KUB dosya adlarinin ICINDE
    zaten '__' var (ETKENMADDE__URUNADI), bu yuzden '__'yi klasor ayracina
    cevirmek 108 belgede yanlis yol uretip kontrolu sessizce atliyordu.
    Onun yerine gercek PDF agaci bir kez taranip tersten eslesme kurulur.
    """
    if _INDEKS:
        return _INDEKS
    for k in ("layer1_clinical", "layer2_regulatory", "layer3_reimbursement"):
        for kok, _, fs in os.walk(os.path.join(ROOT, k)):
            for f in fs:
                if not f.lower().endswith(".pdf"):
                    continue
                p = os.path.join(kok, f)
                ad = os.path.relpath(p, ROOT).replace(os.sep, "__")[:-4] + ".md"
                _INDEKS[ad] = p
    return _INDEKS


def hacim_kontrol(md_yolu, metin):
    """Donusum kaybi kontrolu.

    Docling, metin katmanli etiketlerde cokmeden 'OK' donup icerigin %90'ini
    sessizce dusurebiliyordu (EMA Revlimid: 247k karakter -> 13k). Dosya var,
    aciliyor, makul gorunuyor; sadece uyarilar ve doz ayarlamalari yok.
    Bu yuzden yapisal kontrollerden ONCE hacim karsilastirilir.

    _work/parsed/<katman>__<klasor>__<ad>.md -> <katman>/<klasor>/<ad>.pdf
    """
    pdf = KAYNAK_INDEKS().get(os.path.basename(md_yolu))
    if not pdf:
        return []
    try:
        import fitz
    except ImportError:
        return []
    d = fitz.open(pdf)
    kaynak = sum(len(p.get_text()) for p in d)
    if kaynak < 500:                      # taranmis belge: oran anlamsiz
        return [bulgu("REVIEW", "kaynak_metin_katmani_yok",
                      f"PDF'te metin katmani yok ({d.page_count} sayfa), cikti OCR'a "
                      f"dayaniyor - dogruluk dusuk olabilir")]
    oran = len(metin) / kaynak
    if oran < ORAN_ESIGI:
        return [bulgu("ERROR", "donusum_kaybi",
                      f"kaynak {kaynak} karakter -> cikti {len(metin)} "
                      f"(oran {oran:.2f}); belgenin buyuk kismi kayip")]
    return []


_ENRICH = None


def ENRICH():
    global _ENRICH
    if _ENRICH is None:
        p = os.path.join(ROOT, "_logs", "enrich_report.json")
        _ENRICH = {r["dosya"]: r for r in json.load(open(p, encoding="utf-8"))} \
            if os.path.exists(p) else {}
    return _ENRICH


def bolum_kontrol(yol):
    """Kanonik bolum kumesine gore eksik bolum.

    Zenginlestirme adimi (_scripts/enrich_sections.py) her etiket icin hangi
    numarali bolumlerin bulundugunu kaydediyor. SmPC/PI semasi sabit oldugu icin
    "4.2 Pozoloji yok" ground truth gerektirmeyen, deterministik bir bulgudur -
    ve hacim oranindan cok daha keskindir: belge acilir, uzunlugu makul gorunur,
    ama doz bolumu kayiptir.
    """
    r = ENRICH().get(os.path.basename(yol))
    if not r or not r["eksik"]:
        return []
    return [bulgu("ERROR", "eksik_bolum",
                  f"{r['sinif']} semasinda zorunlu bolum yok: "
                  f"{', '.join(r['eksik'])} ({len(r['eksik'])} bolum)")]


def kapsam(t, yol):
    """Hangi kontrolun MALZEMESI vardi?

    Bir kontrolun bulgu uretmemesi iki farkli sey olabilir: baktim ve temiz,
    ya da bakacak bir sey yoktu. Ikisini sessizlikle ifade etmek raporu
    yaniltici kiliyordu; burada acikca ayriliyor.
    """
    ad = os.path.basename(yol)
    return dict(
        dipnot="[^" in t,
        atif="](#" in t,
        tablo=bool(re.search(r"(?m)^\s*\|", t)),
        # DAL_KALIP satir basina bagli; kapsam taramasi satir satir yapilmali.
        hiyerarsi=any(DAL_KALIP.match(s) for s in t.split("\n")),
        bolum=ad in ENRICH(),
        hacim=ad in KAYNAK_INDEKS(),
    )


def dogrula(yol):
    t = open(yol, encoding="utf-8", errors="replace").read()
    b = hacim_kontrol(yol, t) + bolum_kontrol(yol)
    parcalar = bolumler(t)
    kod_tanim, kod_kullanim = defaultdict(set), defaultdict(set)
    for _, blok, kod in parcalar:
        if kod:
            kod_tanim[kod] |= set(re.findall(r"(?m)^\s*[-*]?\s*\[\^([^\]]+)\]\s*:", blok))
            kod_kullanim[kod] |= set(re.findall(r"\[\^([^\]]+)\]", blok))

    for ilk_satir, blok, kod in parcalar:
        for x in dipnot_kontrol(blok, kod_tanim[kod], kod_kullanim[kod]):
            if x["satir"]:
                x["satir"] += ilk_satir - 1
            b.append(x)
    b += atif_kontrol(t) + tablo_kontrol(t) + hiyerarsi_kontrol(t)
    o = Counter(x["seviye"] for x in b)
    return dict(dosya=os.path.relpath(yol, ROOT),
                ozet={k: o.get(k, 0) for k in ("ERROR", "WARN", "REVIEW")},
                kapsam=kapsam(t, yol),
                bulgular=b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("hedef", nargs="+")
    ap.add_argument("--limit", type=int, default=12)
    a = ap.parse_args()

    dosyalar = []
    for h in a.hedef:
        if os.path.isdir(h):
            for kok, _, fs in os.walk(h):
                dosyalar += [os.path.join(kok, f) for f in fs if f.endswith(".md")]
        elif h.endswith(".md"):
            dosyalar.append(h)

    raporlar = [dogrula(d) for d in sorted(dosyalar)]
    json.dump(raporlar, open(CIKTI, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    if len(raporlar) > 1:
        n = len(raporlar)
        print(f"--- ARSIV SAGLIK RAPORU ({n} belge)")
        for k in ("hacim", "bolum", "tablo", "dipnot", "atif", "hiyerarsi"):
            var = sum(1 for r in raporlar if r["kapsam"][k])
            print(f"  {k:10s} malzeme bulunan {var:4d}/{n}"
                  f"   kapsam disi {n-var:4d}")
        t = Counter(x["tur"] for r in raporlar for x in r["bulgular"])
        print("  bulgu turleri: " +
              (", ".join(f"{k}={v}" for k, v in t.most_common()) or "yok"))
        temiz = sum(1 for r in raporlar if not any(r["ozet"].values()))
        print(f"  bulgusuz belge: {temiz}/{n}")

    for r in raporlar:
        o = r["ozet"]
        if len(raporlar) > 1 and not any(o.values()):
            continue                       # temiz belgeyi tek tek listeleme
        print(f"\n=== {r['dosya']}  ERROR {o['ERROR']} | WARN {o['WARN']} | REVIEW {o['REVIEW']}")
        for x in r["bulgular"][:a.limit]:
            yer = f"satir {x['satir']}" if x["satir"] else "-"
            print(f"  [{x['seviye']:6s}] {x['tur']:22s} {yer:>10s}  {x['detay'][:88]}")
        if len(r["bulgular"]) > a.limit:
            print(f"  ... +{len(r['bulgular'])-a.limit} bulgu daha -> {CIKTI}")
        log("structural validation", "dogrulama",
            f"{r['dosya']}: ERROR {o['ERROR']}, WARN {o['WARN']}, REVIEW {o['REVIEW']}")


if __name__ == "__main__":
    main()
