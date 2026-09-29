#!/usr/bin/env python
"""Cevap katmani - tek giris noktasi.

Bir soru girer, yapilandirilmis bir cevap cikar. Demo da bunu cagirir, Level 3
degerlendirmesi de bunu cagirir. Iki ayri yol yazilsaydi olctugumuz sistemle
gosterdigimiz sistem farkli olurdu ve bunu fark etmezdik.

AKIS
    soru
     -> sorgu isleme      (etken madde, rejim, sinif, kisaltma tespiti)
     -> Qdrant aramasi    (ilac uyumuna gore siralanmis adaylar)
     -> tekrar ayiklama   (ayni metnin kopyalari eleniyor)
     -> baglam kurma      (kaynak numaralariyla)
     -> dil modeli
     -> denetim           (atif, dayanaklilik, ruhsat uyarisi)
     -> guven

NEDEN TEKRAR AYIKLAMA, NEDEN OZETLEME DEGIL

Arsivde ayni etken maddenin sekiz markasi var ve hepsinin 4.2 bolumu ayni seyi
yaziyor. Olcumde gorduk: bir soruda ilk uc sonuc ayni urunun uc farkli dozuydu.
Yani on parcalik baglamin yedisi ayni metnin kopyasi olabiliyor. Ayiklama
baglami hem kucultuyor hem zenginlestiriyor - yer acilinca kilavuz ve SUT
parcalari da giriyor.

Ozetleme yapmiyoruz. Ozet, yeniden yazmaktir; yeniden yazilan bir doz
cumlesinde "kreatinin klerensi 30'un altinda" ifadesi "bobrek yetmezliginde"
oluverir. Klinik metinde bu kabul edilemez. Sikistirma seciyor, uretmiyor.

Calistirma:
    _env/parse/Scripts/python.exe _scripts/pipeline.py "sorunuz"
    ... --llm sahte        (varsayilan; model olmadan borulari test eder)
    ... --llm ollama --model qwen2.5:7b
"""
import argparse, json, os, re, sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))

import qdrant_index as QI
import query_processing as QP

ADAY = 30                  # aramadan cekilen ham aday
BAGLAM_PARCA = 4           # ayiklamadan sonra modele giden parca
# 5 degil 4: butun olcumler k=4 ile yapildi (answer_eval, llm_bakeoff,
# negatif_taze). Uretimin olculenden farkli kosmasi, raporladigimiz
# rakamlarin gosterdigimiz sistemi tarif etmemesi demek olurdu. Alan
# kapisinin hastalik-etiketi orani da secilen parca sayisina bagli.
# Neden 8 degil 5: chunk tavani 800 token, sekiz parca ~6.500 token ediyor ve
# dikkat hesabinin bellegi dizi uzunlugunun karesiyle buyuyor. T4'te (14,5 GB)
# dort bitlik model + gomme modeli yanindayken bu tasiyor. Bes parca ~4.000
# token; tekrar ayiklama sayesinde bes parca, ayiklamasiz sekizden daha cok
# FARKLI bilgi tasiyor.
TEKRAR_ESIGI = 0.85        # bu oranin uzerinde ortusen parcalar kopya sayilir
REDDET_ESIGI = 0.50        # en iyi parcanin skoru bunun altindaysa cevap yok
DAYANAK_ESIGI = 0.20       # dayanakli cumle ORANI bunun altindaysa cevap yok
SEM_ESIGI = 0.50           # bir cumle icin "kaynakta var" sayilma esigi
ALAN_KURAL = "varlik|hast75"

# Bu dort deger A yarisindan (39 pozitif + 8 negatif) secildi, B yarisi hic
# gorulmeden. Eski degerler (0,55 ve 0,40) dort demo cevabina bakilarak
# konmustu ve olcum bunlarin yanlis yerde durdugunu gosterdi.
#
# DAYANAK_ESIGI neden bu kadar dustu: eski olcut leksik idi - cumleyle kaynak
# metnin ortak sozcuklerine bakiyordu. Arsiv iki dilli (NCCN ve FDA Ingilizce,
# cevap Turkce), yani dogru cevaplarda bile ortak sozcuk cikmiyordu; olculen
# dayanaklilik medyani hem dogru hem uydurma cevaplarda 0,00 idi. Olcut simdi
# anlamsal: cumle ile kaynak parcanin BGE-M3 kosinusu. Esik degeri bu yuzden
# eski olcutun degeriyle karsilastirilamaz.

# Neden iki kapi: apandisit sorusu (arsivde yok) 0,565 skorla esigi kil payi
# gecti ve model kendi bilgisinden cevap uydurdu - klindamisin, sefalosporin.
# Skor esigini yukseltmek cozum degildi: gecerli bir teklistamab sorusu 0,63
# aliyor, yani pencere cok dar. Ikinci kapi cevaba bakiyor: model kaynaklara
# dayanamadiysa (atif yok ya da atif tutmuyor) cevap gosterilmiyor. Uyduran
# model zaten dayanamaz, cunku dayanacak kaynak yoktur.

# Turkiye'de ruhsati olmayan etken maddeler. Kapsam kararinin geregi: bilgi
# gosterilir ama "bugun yazilabilir" gibi sunulmaz.
# NOT: Bu liste elle tutuluyor. TITCK ruhsat listesi (22.965 satir) sisteme
# eklendiginde buradan degil oradan okunmali - o zamana kadar bilinen eksik.
RUHSATSIZ = {"Teclistamab", "Talquetamab", "Elranatamab", "Belantamab mafodotin",
             "Idecabtagene vicleucel", "Ciltacabtagene autoleucel", "Elotuzumab",
             "Plerixafor"}

# --- Alan kapisi --------------------------------------------------------
# NEDEN: Level 3 olcumunde negatif sorularin 6/7'si kapiyi gecti ve esik
# taramasi HICBIR kombinasyonda sifir uydurma bulamadi. Sebep yapisal:
# dayanaklilik "bu iddia verilen kaynaklarda var mi" diye soruyor, "kaynaklar
# soruyla ilgili mi" diye degil. Apandisit sorusunda model SUT'un genel
# antibiyotik kurallarina dayanmisti - o cumleler gercekten baglamda vardi.
#
# Anlamsal benzerlik de ise yaramiyor: butun klinik metinler birbirine benziyor.
# Isleyen sinyal leksik ve basit - ilac ve hastalik adlari ozel isimdir, arsivde
# ya gecer ya gecmez. "apandisit" sifir kez, "lenalidomid" binlerce kez.
SOZLUK_YOL = os.path.join(ROOT, "_work", "arsiv_sozluk.json")
CHUNKS_YOL = os.path.join(ROOT, "_work", "chunks", "chunks.json")
KOK_UZUNLUK = 5        # Turkce ekleri kirpmak icin: klerensi/klerensinin -> klere
TERIM_UZUNLUK = 6      # bu uzunlugun altindaki sozcukler ayirt edici degil

_SOZLUK = None


def _kokler(metin, asgari=4):
    return {w[:KOK_UZUNLUK]
            for w in re.findall(r"[a-zçğıöşü0-9]{%d,}" % asgari, metin.lower())}


def arsiv_sozluk():
    """Arsivde gecen tum sozcuk koklerinin kumesi. Bir kez uretilip saklaniyor."""
    global _SOZLUK
    if _SOZLUK is not None:
        return _SOZLUK
    if os.path.exists(SOZLUK_YOL):
        _SOZLUK = set(json.load(open(SOZLUK_YOL, encoding="utf-8")))
        return _SOZLUK
    s = set()
    for c in json.load(open(CHUNKS_YOL, encoding="utf-8")):
        s |= _kokler(c.get("content") or "")
    json.dump(sorted(s), open(SOZLUK_YOL, "w", encoding="utf-8"),
              ensure_ascii=False)
    _SOZLUK = s
    return s


def alan_skoru(soru, analiz=None):
    """Soru bu arsivin alanina giriyor mu?

    kapsam  : sorudaki ayirt edici terimlerin arsivde bulunma orani
    eksik   : arsivde hic gecmeyen terimler (asil sinyal bunlar)
    varlik  : sorguda ilac / hastalik / rejim / sinif tanindi mi
    """
    s = arsiv_sozluk()
    terimler = sorted({w for w in re.findall(r"[a-zçğıöşü]{%d,}" % TERIM_UZUNLUK,
                                             soru.lower())})
    eksik = [w for w in terimler if w[:KOK_UZUNLUK] not in s]
    a = analiz or QP.analiz(soru)
    return {
        "kapsam": round(1 - len(eksik) / max(1, len(terimler)), 3),
        "eksik": eksik,
        "varlik": bool(a["ilac"] or a["hastalik"] or a["rejim"] or a["sinif"]),
    }


SISTEM = """Sen multipl miyelom konusunda calisan bir klinik karar destek
asistanisin. Turkiye'deki hekimlere yardimci oluyorsun.

KURALLAR
1. YALNIZCA sana verilen kaynak metinlere dayan. Kendi bilgini kullanma.
2. Her iddianin sonuna dayandigi kaynagin numarasini koy: [K1], [K2] gibi.
3. Kaynaklarda cevap yoksa "Bu bilgi arsivde bulunamadi." de ve baska bir sey
   ekleme. Tahmin yurutme, genel bilgiyle doldurma.
4. Doz, sure ve esik degerlerini kaynakta yazdigi gibi aktar. Yuvarlama,
   sadelestirme, kendi ifadenle yeniden yazma.
5. Kaynaklar birbiriyle celisiyorsa celiskiyi belirt, birini secme.
6. Kisa ve klinik yaz. Giris cumlesi kurma, dogrudan cevaba gec.
7. HER cumlenin ve HER madde isaretinin sonunda atif olmali. Atif koyamadigin
   bir cumleyi hic yazma.
8. Sonuc ya da ozet cumlesi ekleme. Kaynakta olmayan genel degerlendirme yapma
   ("bu sema yan etkileri azaltmak uzere tasarlanmistir" gibi cumleler yasak).

ORNEK - dogru bicim:
Baslangic dozu 1,3 mg/m2'dir. [K2]
Doz, 21 gunluk dongunun 1, 4, 8 ve 11. gunlerinde uygulanir. [K2]
Agir bobrek yetmezliginde doz azaltilir. [K5]

ORNEK - yanlis bicim (bunu YAPMA):
Baslangic dozu 1,3 mg/m2'dir ve 21 gunluk dongude uygulanir.
Bu sema toksisiteyi azaltmak icin tasarlanmistir. [K2]
(Ilk cumlede atif yok; ikinci cumle kaynakta olmayan bir yorum.)"""


# --- Dil modeli arka uclari --------------------------------------------
# Arka uc degistirilebilir olmali: yerelde GPU yok, gercek model Colab'da
# kosacak. Iskeleti GPU beklemeden test edebilmek icin sahte arka uc var.

class SahteLLM:
    """Model yok. Baglamdan cikarimci bir cevap uretir.

    Amaci cevap kalitesi degil: baglam kurma, atif ayiklama, dayanaklilik
    olcumu ve guven hesabi model olmadan test edilebilsin diye var.
    """

    ad = "sahte"

    def uret(self, sistem, kullanici):
        parcalar = re.findall(r"\[K(\d+)\][^\n]*\n(.+?)(?=\n\[K\d+\]|\Z)",
                              kullanici, re.S)
        satir = []
        for no, govde in parcalar[:3]:
            ilk = re.split(r"(?<=[.!?])\s", govde.strip())[0][:220]
            satir.append(f"{ilk} [K{no}]")
        return "\n".join(satir) if satir else "Bu bilgi arsivde bulunamadi."


class OllamaLLM:
    ad = "ollama"

    def __init__(self, model="qwen2.5:7b", url="http://localhost:11434"):
        self.model, self.url = model, url

    def uret(self, sistem, kullanici):
        import urllib.request
        # temperature 0: cozumleme acgozlu olmali. Hem transformers arka
        # ucuyla (do_sample=False) ayni davransin, hem de web katmanindaki
        # cevap onbellegi anlamli olsun - ayni soru ayni cevabi vermezse
        # onbellek "eski bir cevabi" gosteriyor demektir.
        veri = json.dumps({
            "model": self.model, "stream": False,
            "options": {"temperature": 0, "num_predict": 500},
            "messages": [{"role": "system", "content": sistem},
                         {"role": "user", "content": kullanici}],
        }).encode()
        istek = urllib.request.Request(
            self.url + "/api/chat", data=veri,
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(istek, timeout=600) as y:
            ham = json.loads(y.read())["message"]["content"]
        return DUSUNCE.sub("", ham).strip()


# Dusunen modellerin ic konusma blogu. Kapanis etiketi hic gelmeyebilir
# (token butcesi bitince), o yuzden ikinci desen acilisi da temizliyor.
DUSUNCE = re.compile(r"<think>.*?</think>|<think>.*", re.S | re.I)


class TransformersLLM:
    """Colab icin. Ilk cagrida modeli yukler."""

    ad = "transformers"

    def __init__(self, model="Qwen/Qwen2.5-7B-Instruct", dort_bit=True,
                 azami_token=None):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.tok = AutoTokenizer.from_pretrained(model)
        ek = {}
        if dort_bit:
            # T4 16 GB; 7 milyarlik model yarim hassasiyette ~15 GB tutuyor ve
            # aktivasyonlarla birlikte bellege sigmiyor. Dort bit ~5 GB.
            from transformers import BitsAndBytesConfig
            ek["quantization_config"] = BitsAndBytesConfig(
                load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4")
        else:
            ek["torch_dtype"] = torch.float16
        self.m = AutoModelForCausalLM.from_pretrained(
            model, device_map="auto", **ek)
        # Dusunen modeller token butcesinin buyuk kismini <think> blogunda
        # harciyor; 500 tokenle cevaba hic sira gelmez ve model haksiz yere
        # "bos cevap veriyor" gorunurdu. Ayrimi model adindan yapiyoruz.
        dusunen = any(x in model.lower() for x in ("r1", "distill", "think"))
        self.azami_token = azami_token or (1400 if dusunen else 500)

    def uret(self, sistem, kullanici):
        mesaj = [{"role": "system", "content": sistem},
                 {"role": "user", "content": kullanici}]
        # apply_chat_template'e return_tensors VERMIYORUZ: transformers'in yeni
        # surumlerinde tensor degil BatchEncoding donduruyor ve generate()
        # icinde .shape patliyor. Once metne cevirip sonra tokenize etmek her
        # surumde ayni calisiyor.
        # enable_thinking=False: Qwen3 ailesinin sablonu bu bayragi taniyor ve
        # dusunme bolumunu kapatiyor. Qwen3.6-27B ilk kosuda dusunme surecini
        # DUZ METIN olarak cevaba yazdi ("Here's a thinking process: ...
        # Rules: 1. Only use provided source texts") - <think> etiketi
        # olmadigi icin ayiklayici da yakalayamadi. Sonuc: ortalama 1772
        # karakterlik cevap, 614 dayanaksiz cumle, kanit orani 0,36.
        # Bayragi tanimayan sablonlar TypeError veriyor, o yuzden geri adim var.
        try:
            metin = self.tok.apply_chat_template(
                mesaj, add_generation_prompt=True, tokenize=False,
                enable_thinking=False)
        except TypeError:
            metin = self.tok.apply_chat_template(
                mesaj, add_generation_prompt=True, tokenize=False)
        girdi = self.tok(metin, return_tensors="pt").to(self.m.device)
        uzunluk = girdi["input_ids"].shape[1]
        cikti = self.m.generate(**girdi, max_new_tokens=self.azami_token,
                                do_sample=False,
                                pad_token_id=self.tok.eos_token_id)
        ham = self.tok.decode(cikti[0][uzunluk:], skip_special_tokens=True)
        # Dusunen modeller (R1 turevleri) cevaptan once <think> blogu uretiyor.
        # Blok kalirsa hem cumle bolmeye hem atif onarimina karisir; ayrica
        # dayanaklilik olcumu bu ic konusmayi "dayanaksiz cumle" sayardi.
        return DUSUNCE.sub("", ham).strip()


def llm_kur(ad, model=None):
    if ad == "ollama":
        # OLLAMA_URL ile uzak bir sunucuya baglanilabiliyor. Gerekcesi:
        # GTX 1650'de (4 GB) 7B model ancak yari yariya GPU'ya siginiyor
        # ("50%/50% CPU/GPU") ve bir cevap 320-376 saniye suruyor. Ayni model
        # Colab T4'te 10-30 saniyede bitiyor. Arama yerelde kaliyor, yalnizca
        # uretim disari gidiyor.
        # DIKKAT: uzak adres verildiginde soru metni VE getirilen kaynak
        # parcalari o sunucuya gonderilir. Kilavuz metinleri acik kaynak
        # oldugu icin sunum baglaminda sakincasiz, ama hasta verisi iceren
        # bir kurulumda bu tercih ayrica degerlendirilmeli.
        return OllamaLLM(model or "qwen2.5:7b",
                         url=os.environ.get("OLLAMA_URL",
                                            "http://localhost:11434"))
    if ad == "transformers":
        return TransformersLLM(model or "Qwen/Qwen2.5-7B-Instruct")
    return SahteLLM()


# --- Baglam kurma -------------------------------------------------------

def _imza(metin):
    """Tekrar tespiti icin sadelestirilmis sozcuk kumesi."""
    return set(re.findall(r"[a-z0-9çğıöşü]{4,}", metin.lower()))


def tekrar_ayikla(adaylar, esik=TEKRAR_ESIGI):
    """Ayni metnin kopyalarini eler, ilkini tutar.

    Marka farki icerigi degistirmiyor: sekiz lenalidomid KUB'unun 4.2 bolumu
    birbirinin ayni. Jaccard benzerligi esigi asarsa sonrakini atiyoruz.
    Atilan parcanin belgesi kaynak listesinde "ayrica" olarak aniliyor ki
    hekim ayni bilginin baska markada da gectigini gorebilsin.
    """
    tutulan, imzalar = [], []
    for p in adaylar:
        im = _imza(p.payload.get("content") or "")
        if not im:
            continue
        kopya = None
        for j, onceki in enumerate(imzalar):
            oran = len(im & onceki) / max(1, min(len(im), len(onceki)))
            if oran >= esik:
                kopya = j
                break
        if kopya is None:
            imzalar.append(im)
            tutulan.append({"nokta": p, "ayrica": []})
        else:
            tutulan[kopya]["ayrica"].append(p.payload.get("document_label"))
    return tutulan


def baglam_sec(noktalar, ilaclar):
    """Baglama girecek adaylari daraltir.

    Aramada uc kume kullaniyoruz (ilac uyan / etiketsiz / baska ilac) ve
    hicbirini atmiyoruz - orada amac dogru parcanin listeye GIRMESI. Baglam
    kurarken amac farkli: modelin onune konan sekiz parcanin hepsi ise
    yaramali. Ilk denemede sekiz parcanin ikisi, teklistamab sorusuna
    lenalidomid doz tablosu olarak geldi.

    Bu yuzden soruda etken madde tanindiginda baska ilaca ait parcalar
    baglama hic alinmiyor. Etiketsizler kaliyor: kilavuzlarin genel bolumleri,
    tani algoritmalari ve SUT maddeleri etiketsiz ve cogu zaman cevabin
    kendisi orada. Uyan hic yoksa daraltma yapilmiyor - bos baglam, kotu
    baglamdan beterdir.
    """
    if not ilaclar:
        return noktalar
    hedef = set(ilaclar)
    uyan, etiketsiz = [], []
    for p in noktalar:
        etiket = set(p.payload.get("drug_names") or [])
        if not etiket:
            # Parcanin kendi metninde ilac adi gecmiyorsa etiketsiz kaliyor;
            # ama parca bir ilacin KUB'undan geliyorsa aslinda etiketsiz degil.
            # "Doz azaltma basamaklari" tablosu REVLIMID belgesinde lenalidomid
            # icindir, metninde lenalidomid yazmasa da. Belge adindan cozuyoruz.
            etiket = set(QP.ilac_bul(str(p.payload.get("document_name") or ""))[0])
        if etiket & hedef:
            uyan.append(p)
        elif not etiket:
            etiketsiz.append(p)
    return (uyan + etiketsiz) if uyan else noktalar


ETIKET = re.compile(r"</?[a-zA-Z][^>]*>")
ISARET = re.compile(r"[*_~#`]+")
# Gecerli bolum numarasi: KUB'de "4.2", FDA'da "5.1", NCCN'de "MYEL-G".
BOLUM_NO = re.compile(r"^(?:\d{1,2}(?:\.\d{1,2})?|[A-Z]{2,5}-[0-9A-Z]{1,3})$")


def temiz_baslik(s):
    """Bolum basligini gosterime hazirlar.

    Parser basliklarda markdown ve HTML artiklari birakiyor:
    '**<u>Doz</u>**' gibi. Bunlar chunk metninde zararsiz ama kunye satirinda
    kullanicinin gozune carpiyor ve sistemin ozensiz oldugu izlenimi veriyor.
    Metnin kendisine dokunmuyoruz - yalnizca gosterilen basligi sadelestiriyoruz.
    """
    if not s:
        return None
    s = ISARET.sub(" ", ETIKET.sub(" ", str(s)))
    s = re.sub(r"\s+", " ", s).strip(" :-–—")
    return s or None


def kunye(k):
    """Kaynak satiri. Eksik alanlar satiri bozmasin diye atlaniyor.

    Sayfa ve surum arsivin buyuk bolumunde bos; bunu 's.None surum None' diye
    yazmak bilgi vermiyor, sadece eksigi vurguluyor.
    """
    p = [f"[K{k['no']}]", k["belge"] or "?"]
    # section_number bazi belgelerde baslik artigi tasiyor ("**NCCN" gibi).
    # Gercek bir bolum numarasina benzemiyorsa kunyeye yazmiyoruz.
    if k["bolum"] and BOLUM_NO.match(str(k["bolum"])):
        p.append(f"bölüm {k['bolum']}")
    if k["baslik"]:
        p.append(k["baslik"][:60])
    if k["sayfa"]:
        p.append(f"s.{k['sayfa']}")
    if k["surum"]:
        p.append(f"sürüm {k['surum']}")
    if k["ayrica"]:
        p.append(f"(ayrıca {len(k['ayrica'])} belgede)")
    return " · ".join(p)


def baglam_kur(secili):
    """Modele verilecek metin + kaynak listesi.

    Her parcanin basina belge, bolum ve sayfa yaziliyor. Model atif verirken
    numaraya bakiyor; numarayi kaynaga biz cozuyoruz, model degil. Modele
    kaynak adini yazdirsaydik uydurma kaynak uretmesi mumkun olurdu.
    """
    satir, kaynaklar = [], []
    for i, kayit in enumerate(secili, start=1):
        y = kayit["nokta"].payload
        basli = " / ".join(str(x) for x in
                           [y.get("document_label"), y.get("section_number"),
                            y.get("section_title")] if x)
        satir.append(f"[K{i}] {basli}\n{(y.get('content') or '').strip()}")
        kaynaklar.append({
            "no": i, "belge": y.get("document_label"),
            "bolum": y.get("section_number"),
            "baslik": temiz_baslik(y.get("section_title")),
            "baslik_ham": y.get("section_title"),
            "sayfa": y.get("page_number"), "surum": y.get("version"),
            "kaynak_tipi": y.get("source_type"), "chunk_id": y.get("chunk_id"),
            "ilac": y.get("drug_names") or [],
            "ayrica": kayit["ayrica"],
        })
    return "\n\n".join(satir), kaynaklar


# --- Denetim ------------------------------------------------------------

# Rakamdan sonraki noktada BOLMUYORUZ. Turkcede sira sayilari noktayla yaziliyor
# ("1. ve 2. gunlerinde", "28 gunluk dongunun 1, 2, 8, 9, 15 ve 16. gunlerinde")
# ve bunlari cumle sonu saymak dozaj cumlelerini parcaliyordu. Parcalanan
# cumleler atifsiz kaldigi icin dogru dayanakli bir cevap 0,2 olculuyordu.
CUMLE = re.compile(r"(?<![0-9]\.)(?<=[.!?])\s+")
# Model atifi tek tek de yaziyor ([K1][K3]) toplu da ([K1, K2, K3]). Onceki
# desen yalnizca tekil bicimi taniyordu; Q14 ve Q16'da "atif yok" gorunmesinin
# sebebi buydu, oysa cevaplarda uc kaynak birden gosterilmisti.
ATIF = re.compile(r"\[\s*K\s*\d+(?:\s*,\s*K?\s*\d+)*\s*\]")
_SAYI = re.compile(r"\d+")


def atif_nolari(metin):
    return [int(n) for p in ATIF.findall(metin) for n in _SAYI.findall(p)]


_SADECE_ATIF = re.compile(r"\[\s*K\s*\d+(?:\s*,\s*K?\s*\d+)*\s*\]|[\s.,;:]")


def cumlelere_bol(metin):
    """Cevabi atif birimlerine boler.

    Satir sonlari de sinir sayiliyor: model cevaplarinin ucte ikisi madde
    listesi iceriyor ve madde satirlari nokta ile bitmiyor. Yalnizca [.!?]
    ile bolununce butun liste tek bir "cumle" oluyordu; listenin sonundaki
    tek atif butun maddeleri atifli gosteriyor, atifsiz liste ise tek bir
    atifsiz birim sayiliyordu. Iki hata da olcumu bozar.
    """
    parcalar = []
    for satir in metin.strip().splitlines():
        satir = satir.strip()
        if not satir:
            continue
        parcalar += [c.strip() for c in CUMLE.split(satir) if c.strip()]

    # Model atifi cogu zaman NOKTADAN SONRA yaziyor ("... yapilmalidir. [K3]").
    # Bolucu noktada boldugu icin [K3] ayri bir parcaya dusuyor, kisa oldugu
    # icin eleniyor ve geriye kalan cumle ATIFSIZ gorunuyordu. Ilk Level 4
    # teshisindeki "144 cumlede atif yok" rakami bu yapaylikla sisirilmisti.
    # Yalnizca atif isaretinden ibaret parcalar bir oncekine geri yapistiriliyor.
    birlesik = []
    for p in parcalar:
        if birlesik and not _SADECE_ATIF.sub("", p).strip():
            birlesik[-1] = f"{birlesik[-1]} {p}"
        else:
            birlesik.append(p)

    # Esik 15 degil 10: klinik madde satirlari cok kisa olabiliyor
    # ("- 1,3 mg/m2 IV" 14 karakter) ve bunlar atlanirsa hem atifsiz kalirlar
    # hem de olcumden duserler - oysa dozu tasiyan satir tam da bu.
    return [c for c in birlesik if len(c) > 10]


def atif_onar(cevap, secili, sem_esigi=None):
    """Atifsiz cumlelere kaynak numarasi takar, yanlis olani duzeltir.

    NEDEN MODELDEN ISTEMIYORUZ

    Isteme "her cumlenin sonunda atif olmali" kurali ve dogru/yanlis bicim
    ornegi konuldu; iki kosuda da tutmadi. 78 cevabin 30'unda hicbir atif
    yoktu, yalnizca 11'i her cumlede atif verdi. Buna karsilik NUMARA neredeyse
    hic sasmiyordu: 273 cumlenin sadece 4'unde model yanlis numara yazmisti.
    Yani eksik olan bilgi degil, bicim disiplini - ve bu boyuttaki bir modelden
    bicim disiplinini istemek yerine isi kendimiz yapmak daha saglam.

    Atif, cumle ile parca gommelerinin kosinusuyle atanyor. Esigi gecen parca
    yoksa cumle ATIFSIZ birakiliyor - uydurma bir kaynak takmaktansa dayanaksiz
    gorunmesi dogru, zaten dayanaklilik kapisi da onu yakalayacak.

    Donen: (yeni_cevap, {"eklenen": n, "duzeltilen": n, "biraklan": n})
    """
    sem_esigi = SEM_ESIGI if sem_esigi is None else sem_esigi
    sayac = {"eklenen": 0, "duzeltilen": 0, "biraklan": 0}
    cumleler = cumlelere_bol(cevap)
    gv = _parca_vektorleri(secili)
    if not cumleler or gv is None:
        return cevap, sayac

    cv = _sorgu_vektoru([ATIF.sub("", c) for c in cumleler])
    benzerlik = gv @ cv.T                     # (parca, cumle)

    yeni = cevap
    for j, c in enumerate(cumleler):
        skor = benzerlik[:, j]
        en_iyi = int(skor.argmax())
        varolan = atif_nolari(c)
        if varolan:
            # Model numara yazmis. Yalnizca gosterdigi parca esigin altindayken
            # ve baska bir parca esigi gecerken duzeltiyoruz.
            mevcut = max((float(skor[n - 1]) for n in varolan
                          if 1 <= n <= len(secili)), default=0.0)
            if mevcut >= sem_esigi or float(skor[en_iyi]) < sem_esigi:
                continue
            duzeltilmis = ATIF.sub(f"[K{en_iyi + 1}]", c)
            sayac["duzeltilen"] += 1
        elif float(skor[en_iyi]) >= sem_esigi:
            duzeltilmis = f"{c} [K{en_iyi + 1}]"
            sayac["eklenen"] += 1
        else:
            sayac["biraklan"] += 1
            continue
        yeni = yeni.replace(c, duzeltilmis, 1)
    return yeni, sayac


def dayanaklilik(cevap, secili, sem_esigi=None):
    """Cevaptaki cumlelerin kaci gercekten kaynaga dayaniyor?

    OLCUT NEDEN DEGISTI

    Onceki surum leksikti: cumle ile kaynak metnin ortak sozcuklerine bakiyor,
    ustune atif zorunlulugu koyuyordu. Iki dilli bir arsivde bu yapisal olarak
    calismiyor - kaynak "administer 27 mg/m2 on days 1, 2, 8, 9", cevap "27
    mg/m2 dozunda 1, 2, 8 ve 9. gunlerde uygulanir". Ortak sozcuk neredeyse
    yok. Level 3 olcumunde dayanakliligin medyani hem dogru hem uydurma
    cevaplarda 0,00 cikti, yani olcut hicbir sey ayirt etmiyordu.

    Simdiki olcut anlamsal: cumle ile parcanin BGE-M3 kosinusu. Ayrica atif
    zorunlulugu bu kapidan kaldirildi - burada sorulan sey "bu iddia verilen
    kaynaklarda VAR MI" (guvenlik sorusu). Atifin DOGRU parcayi gosterip
    gostermedigi ayri bir olcu (Level 4) ve ayri raporlaniyor; ikisini tek
    sayida birlestirmek, dogru bilgiyi yanlis numarayla veren cevabi uydurma
    saymak olurdu.
    """
    sem_esigi = SEM_ESIGI if sem_esigi is None else sem_esigi
    cumleler = cumlelere_bol(cevap)
    if not cumleler:
        return 0.0, []
    gv = _parca_vektorleri(secili)
    if gv is None:
        return 0.0, [c[:90] for c in cumleler]

    duz = [ATIF.sub("", c) for c in cumleler]
    cv = _sorgu_vektoru(duz)                 # (cumle, 1024), normalize
    benzerlik = gv @ cv.T                    # (parca, cumle)
    dayanan, havada = 0, []
    for j, c in enumerate(cumleler):
        if float(benzerlik[:, j].max()) >= sem_esigi:
            dayanan += 1
        else:
            havada.append(c[:90])
    return dayanan / len(cumleler), havada


def guven_hesapla(arama_skoru, dayanak, kaynaklar, analiz):
    """Uc sinyalden kategorik guven.

    Sayisal bir olasilik uretmiyoruz. Kalibrasyon verisi olmadan "%87 dogru"
    demek uydurma bir kesinlik verir; kategorik ifade daha durust.
    """
    uyarilar = []

    ruhsatsiz = sorted(set(analiz["ilac"]) & RUHSATSIZ)
    if ruhsatsiz:
        uyarilar.append("Turkiye'de ruhsatsiz: " + ", ".join(ruhsatsiz) +
                        " - ithal / endikasyon disi yolu gerekir.")

    tipler = {k.get("kaynak_tipi") for k in kaynaklar}
    if analiz["ilac"] and "SUT" not in tipler:
        uyarilar.append("Geri odeme kaynagi getirilmedi; SUT kosulu ayrica "
                        "dogrulanmali.")

    if arama_skoru >= 0.70 and dayanak >= 0.8:
        seviye = "yuksek"
    elif arama_skoru >= 0.60 and dayanak >= 0.5:
        seviye = "orta"
    else:
        seviye = "dusuk"
    if uyarilar and seviye == "yuksek":
        seviye = "orta"
    return {"seviye": seviye, "arama_skoru": round(float(arama_skoru), 3),
            "dayanaklilik": round(float(dayanak), 3), "uyarilar": uyarilar}


# --- Ana giris ----------------------------------------------------------

_MODEL = None


def _sorgu_vektoru(soru):
    """Sorgu ham haliyle gomuluyor - genisletilmis haliyle degil.

    Genisletme yalnizca leksik arama icin: gomme modeli dogal cumleyle
    egitildi, sorguyu anahtar kelime yiginina cevirmek vektoru bozar.
    """
    global _MODEL
    if _MODEL is None:
        os.environ.setdefault("HF_HOME", "D:/hf_cache")
        from sentence_transformers import SentenceTransformer
        # CPU'da tutuluyor. GPU'da ~2,3 GB yer kapliyor ve o yeri dil modeline
        # birakmak gerekiyor - burada kodlanan tek bir kisa cumle, CPU'da yarim
        # saniye suruyor. Zorunlu hallerde GOMME_CIHAZ=cuda ile degistirilebilir.
        _MODEL = SentenceTransformer(
            "BAAI/bge-m3", cache_folder=os.environ["HF_HOME"],
            device=os.environ.get("GOMME_CIHAZ", "cpu"))
        _MODEL.max_seq_length = 512
    return _MODEL.encode(soru, normalize_embeddings=True, convert_to_numpy=True)


VEKTOR_YOL = os.path.join(ROOT, "_work", "embeddings", "BAAI_bge-m3.npy")
_VEKTOR = None


def _parca_vektorleri(secili):
    """Secili parcalarin gomme vektorleri, (parca, 1024) dizisi.

    Parcalar yeniden kodlanmiyor: ayni vektorler indeksleme sirasinda uretilip
    diske yazildi ve Qdrant nokta id'si chunks.json satir numarasina esit, yani
    dogrudan satir olarak okunabiliyorlar. Yeniden kodlamak hem yavas olurdu
    hem de ARAMADA kullanilandan farkli bir vektor uretme riski tasirdi.
    """
    global _VEKTOR
    if _VEKTOR is None:
        if not os.path.exists(VEKTOR_YOL):
            return None
        _VEKTOR = np.load(VEKTOR_YOL, mmap_mode="r")
    satir = [x["nokta"].id for x in secili]
    if not satir:
        return None
    return np.asarray(_VEKTOR[satir], dtype=np.float32)


def alan_gecti(soru, secili, analiz=None, kural=None):
    """Soru bu arsivin alanina giriyor mu? (uretim oncesi ucuncu kapi)

    'varlik|hast75': sorguda miyelom alanina ait bir varlik taniniyorsa VEYA
    getirilen parcalarin en az %75'i hastalik etiketi tasiyorsa gecer.

    Kural A yarisindan secildi. Alternatifleri de olculdu: yalniz 'varlik' bir
    dogru cevabi daha eliyordu, yalniz 'hast75' 39 sorunun 16'sina dusuyordu.
    "kapali" degeri kapiyi devre disi birakir - karsilastirmali olcum icin.
    """
    kural = ALAN_KURAL if kural is None else kural
    if kural == "kapali":
        return True
    varlik = alan_skoru(soru, analiz)["varlik"]
    if kural == "varlik":
        return varlik
    hast = (sum(1 for x in secili
                if (x["nokta"].payload.get("disease") or []))
            / max(1, len(secili)))
    if kural == "hast75":
        return hast >= 0.75
    if kural == "varlik|hast100":
        return varlik or hast >= 1.0
    return varlik or hast >= 0.75


def cevapla(soru, llm=None, istemci=None, k=None, aday=None,
            reddet_esigi=None, dayanak_esigi=None, alan_kural=None,
            atif_onarim=True):
    # Varsayilanlar gövdede okunuyor, imzada degil: Python varsayilan degeri
    # fonksiyon TANIMLANIRKEN bir kez hesapliyor, bu yuzden calisma aninda
    # BAGLAM_PARCA'yi degistirmek imzadaki degere hic yansimazdi. Bellek
    # ayarini Colab'dan degistirebilmek icin bu gerekli.
    k = k or BAGLAM_PARCA
    aday = aday or ADAY
    reddet_esigi = REDDET_ESIGI if reddet_esigi is None else reddet_esigi
    # Degerlendirmede ikisi de 0 verilip kapilar kapatiliyor: dil modeli BIR KEZ
    # kosuyor, esikler sonradan ham kayitlara uygulaniyor. Aksi halde her esik
    # denemesi icin butun kumeyi yeniden uretmek gerekirdi.
    dayanak_esigi = DAYANAK_ESIGI if dayanak_esigi is None else dayanak_esigi
    llm = llm or SahteLLM()
    kapat = istemci is None
    c = istemci or QI.ac()
    try:
        analiz = QP.analiz(soru)
        vek = _sorgu_vektoru(soru)
        noktalar = QI.ara(c, vek, k=aday, ilac=analiz["ilac"])
        if analiz["ilac"]:
            # Ikinci arama, yalnizca o etken maddenin chunk'lari icinde.
            # Genel aramada TECVAYLI urun bilgisi ilk 30'a giremiyordu: soru
            # Turkce ("basamakli doz semasi"), belge Ingilizce ("step-up
            # dosing"), ve ayni konuda Turkce yazilmis baska belgeler one
            # geciyordu. Filtreli arama bu mesafeyi asiyor.
            hedefli = QI.ara(c, vek, k=k, zorunlu_ilac=analiz["ilac"])
            varolan = {p.id for p in hedefli}
            noktalar = hedefli + [p for p in noktalar if p.id not in varolan]

        en_iyi = max((p.score for p in noktalar), default=0.0)
        if not noktalar or en_iyi < reddet_esigi:
            # Arsivde karsiligi yokken cevap uretmek, klinik bir sistemde
            # yanlis cevaptan daha tehlikeli. Burada model hic cagrilmiyor.
            return {"soru": soru, "cevap": "Bu bilgi arsivde bulunamadi.",
                    "kaynaklar": [], "kullanilan": [], "reddedildi": True,
                    "guven": {"seviye": "dusuk", "arama_skoru": round(en_iyi, 3),
                              "dayanaklilik": 0.0,
                              "uyarilar": ["En iyi eslesme esigin altinda."]},
                    "analiz": analiz}

        secili = tekrar_ayikla(baglam_sec(noktalar, analiz["ilac"]))[:k]

        # ALAN KAPISI. Arama skoru kapisi alan disi sorulari AYIRT ETMIYOR:
        # taze negatif kumede 15 sorunun 15'i de esigi gecti (0,53 - 0,72).
        # Gomme modeli "tibbi soru - tibbi metin" benzerligini olcuyor, "bu
        # arsivin konusu mu" sorusunu degil. Ayirt eden iki sinyal: sorguda
        # miyelom alanina ait bir varlik taninmasi, ve getirilen parcalarin
        # hastalik etiketi tasimasi.
        if not alan_gecti(soru, secili, analiz, alan_kural):
            return {"soru": soru, "cevap": "Bu bilgi arsivde bulunamadi.",
                    "kaynaklar": [], "kullanilan": [], "reddedildi": True,
                    "guven": {"seviye": "dusuk", "arama_skoru": round(en_iyi, 3),
                              "dayanaklilik": 0.0,
                              "alan_kapisi": "Soru bu arsivin kapsami disinda "
                                             "gorunuyor (multipl miyelom).",
                              "uyarilar": ["Kapsam disi soru."]},
                    "analiz": analiz}

        baglam, kaynaklar = baglam_kur(secili)
        istem = f"KAYNAKLAR\n\n{baglam}\n\nSORU\n{soru}"
        cevap = llm.uret(SISTEM, istem).strip()

        # Atif onarimi uretimden SONRA, dayanaklilik olcumunden ONCE. Sirasi
        # onemli: dayanaklilik atiftan bagimsiz olcusuyor, ama kullaniciya
        # gosterilen ve degerlendirilen metin onarilmis olan olmali.
        ham_cevap = cevap
        cevap, onarim = atif_onar(cevap, secili) if atif_onarim else (cevap, None)

        dayanak, havada = dayanaklilik(cevap, secili)
        guven = guven_hesapla(en_iyi, dayanak, kaynaklar, analiz)
        if onarim and (onarim["eklenen"] or onarim["duzeltilen"]):
            guven["atif_onarimi"] = onarim
            guven["model_atifi"] = sorted(set(atif_nolari(ham_cevap)))
        if havada:
            guven["dayanaksiz_cumleler"] = havada

        # Ikinci kapi. Skor esigini gecmis ama kaynaga dayanmayan cevap,
        # klinik bir sistemde gosterilmemeli: dogru gorunur, dogrulanamaz.
        if dayanak < dayanak_esigi:
            guven["dayanak_kapisi"] = (
                f"Uretilen cevabin dayanaklilik orani {dayanak:.2f}, esik "
                f"{dayanak_esigi}. Cevap gosterilmedi.")
            guven["seviye"] = "dusuk"
            guven["gizlenen_cevap"] = cevap
            return {"soru": soru, "cevap": "Bu bilgi arsivde bulunamadi.",
                    "kaynaklar": [], "kullanilan": [], "reddedildi": True,
                    "guven": guven, "analiz": analiz}

        kullanilan = sorted(set(atif_nolari(cevap)))
        # Tum kaynaklar da donuyor: degerlendirici, modelin atif vermedigi ama
        # baglama giren parcalari da gormek zorunda - yanlis reddetme ile gercek
        # bilgi yoklugunu ayirt etmenin tek yolu bu.
        guven["tum_kaynaklar"] = kaynaklar
        return {"soru": soru, "cevap": cevap,
                "kaynaklar": [x for x in kaynaklar if x["no"] in kullanilan]
                             or kaynaklar,
                "kullanilan": kullanilan, "reddedildi": False,
                "guven": guven, "analiz": analiz}
    finally:
        if kapat:
            c.close()


def yazdir(s):
    print(f"\nSORU  {s['soru']}")
    g = s["guven"]
    print(f"GUVEN {g['seviye']}  (arama {g['arama_skoru']}, "
          f"dayanaklilik {g['dayanaklilik']})")
    for u in g["uyarilar"]:
        print(f"  ! {u}")
    print(f"\n{s['cevap']}\n")
    if s["kaynaklar"]:
        print("KAYNAKLAR")
        for x in s["kaynaklar"]:
            print("  " + kunye(x))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("soru")
    ap.add_argument("--llm", default="sahte",
                    choices=["sahte", "ollama", "transformers"])
    ap.add_argument("--model", default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    s = cevapla(a.soru, llm=llm_kur(a.llm, a.model))
    if a.json:
        s.pop("analiz", None)
        print(json.dumps(s, ensure_ascii=False, indent=1))
    else:
        yazdir(s)
