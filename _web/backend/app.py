#!/usr/bin/env python
"""Klinik karar destek arsivi - HTTP servisi.

TASARIM KARARLARI

1. TEK ISCI. Qdrant gomulu modda depo klasorunu isletim sistemi kilidiyle
   tutuyor; ikinci bir islem acmaya calisirsa "already accessed by another
   instance" hatasi verir. Bu yuzden uvicorn --workers 1 ile kosulmali.
   Sunucuya tasinirken es zamanlilik gerekirse Qdrant SUNUCU moduna gecilir
   (docker); kod degismez, yalnizca qdrant_index.ac() baglanti kurar.

2. MODEL BIR KEZ YUKLENIR. Gomme modeli (BGE-M3, ~2,3 GB) ve Qdrant istemcisi
   uygulama omru boyunca acik kalir. Her istekte yuklemek 30 saniye ekler.

3. ONBELLEK. Cozumleme acgozlu (do_sample=False), yani ayni soru ayni cevabi
   veriyor. Sunum sirasinda dakikalarca beklememek icin cevaplar diske
   yaziliyor. Onbellekten gelen cevap arayuzde ISARETLENIYOR - klinik bir
   sistemde "bu cevap simdi mi uretildi" sorusunun cevabi gizlenmemeli.
   Anahtara model ve esikler de giriyor: yapilandirma degisince eski cevabi
   dondurmek, degisikligi gormemek olurdu.

4. GUVEN NESNESI OLDUGU GIBI DONUYOR. Hangi kapinin kapattigi, hangi cumlenin
   dayanaksiz oldugu, atifin onarilip onarilmadigi - hepsi arayuze gidiyor.
   Bunlari saklamak sistemi oldugundan emin gostermek olurdu.

Calistirma:
    uvicorn app:uygulama --host 127.0.0.1 --port 8000 --workers 1
"""
import hashlib, json, os, sys, time
from contextlib import asynccontextmanager

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "_scripts"))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import pipeline as P
import qdrant_index as QI

ONBELLEK_YOL = os.path.join(ROOT, "_work", "onbellek.json")
CHUNKS_YOL = os.path.join(ROOT, "_work", "chunks", "chunks.json")

# Ayarlar .env'den. Yerelde CPU + Ollama, sunucuda GPU + transformers.
LLM_ARKA = os.environ.get("LLM_ARKA", "ollama")
LLM_MODEL = os.environ.get("LLM_MODEL", "qwen2.5:7b")
ONBELLEK_ACIK = os.environ.get("ONBELLEK", "1") == "1"
KOKEN = [x.strip() for x in
         os.environ.get("KOKEN", "http://localhost:5173").split(",") if x.strip()]

D = {}          # uygulama omru boyunca yasayan nesneler


def onbellek_yukle():
    if os.path.exists(ONBELLEK_YOL):
        try:
            return json.load(open(ONBELLEK_YOL, encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def onbellek_anahtar(soru):
    imza = (f"{soru.strip().lower()}|{LLM_ARKA}|{LLM_MODEL}|{P.REDDET_ESIGI}|"
            f"{P.DAYANAK_ESIGI}|{P.SEM_ESIGI}|{P.ALAN_KURAL}|{P.BAGLAM_PARCA}")
    return hashlib.sha256(imza.encode("utf-8")).hexdigest()[:16]


@asynccontextmanager
async def omur(uygulama):
    t0 = time.time()
    D["istemci"] = QI.ac()
    P._sorgu_vektoru("isitma")              # gomme modelini simdi yukle
    D["llm"] = P.llm_kur(LLM_ARKA, LLM_MODEL)
    D["onbellek"] = onbellek_yukle()
    D["chunk"] = {c["chunk_id"]: c
                  for c in json.load(open(CHUNKS_YOL, encoding="utf-8"))}
    print(f"hazir: {LLM_ARKA}/{LLM_MODEL}, {len(D['chunk'])} chunk, "
          f"{len(D['onbellek'])} onbellek kaydi, {time.time() - t0:.0f} sn")
    yield
    D["istemci"].close()


uygulama = FastAPI(title="Multipl Miyelom Karar Destek", lifespan=omur)
uygulama.add_middleware(CORSMiddleware, allow_origins=KOKEN,
                        allow_methods=["*"], allow_headers=["*"])


class Soru(BaseModel):
    soru: str = Field(min_length=3, max_length=500)


def yanit_paketle(r, sure, onbellekten=False):
    g = r.get("guven") or {}
    return {
        "soru": r["soru"],
        "cevap": r["cevap"],
        "reddedildi": r["reddedildi"],
        "red_nedeni": ("alan" if "alan_kapisi" in g else
                       "dayanak" if "dayanak_kapisi" in g else
                       "arama" if r["reddedildi"] else None),
        "kaynaklar": r.get("kaynaklar") or [],
        "kullanilan": r.get("kullanilan") or [],
        "guven": g,
        "ilaclar": (r.get("analiz") or {}).get("ilac") or [],
        "sure": round(sure, 1),
        "onbellekten": onbellekten,
    }


@uygulama.get("/api/saglik")
def saglik():
    return {"durum": "calisiyor", "llm": f"{LLM_ARKA}/{LLM_MODEL}",
            "chunk": len(D.get("chunk") or {}),
            "esikler": {"arama": P.REDDET_ESIGI, "dayanak": P.DAYANAK_ESIGI,
                        "anlamsal": P.SEM_ESIGI, "alan": P.ALAN_KURAL},
            "onbellek": len(D.get("onbellek") or {})}


@uygulama.post("/api/soru")
def sor(istek: Soru):
    anahtar = onbellek_anahtar(istek.soru)
    if ONBELLEK_ACIK and anahtar in D["onbellek"]:
        kayit = dict(D["onbellek"][anahtar])
        kayit["onbellekten"] = True
        return kayit

    t0 = time.time()
    try:
        r = P.cevapla(istek.soru, llm=D["llm"], istemci=D["istemci"])
    except Exception as e:
        raise HTTPException(500, f"{type(e).__name__}: {e}")

    yanit = yanit_paketle(r, time.time() - t0)
    if ONBELLEK_ACIK:
        D["onbellek"][anahtar] = yanit
        json.dump(D["onbellek"], open(ONBELLEK_YOL, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
    return yanit


@uygulama.get("/api/kaynak/{chunk_id}")
def kaynak(chunk_id: str):
    """Bir parcanin TAM metni. Hekim atifi tiklayip kaynagi gormeli;
    ozetlenmis kaynak, dogrulanamayan kaynaktir."""
    c = (D.get("chunk") or {}).get(chunk_id)
    if not c:
        raise HTTPException(404, "parca bulunamadi")
    return {"chunk_id": chunk_id, "icerik": c["content"],
            "metadata": c.get("metadata") or {}}


@uygulama.get("/api/ornekler")
def ornekler():
    """Sunum senaryolari. Her biri sistemin BASKA bir yonunu gosteriyor."""
    return [
        {"baslik": "Doz sorusu",
         "soru": "Karfilzomib hangi dozda ve hangi günlerde uygulanır?",
         "gosterdigi": "Sayısal değerler kaynaktaki gibi aktarılıyor"},
        {"baslik": "İlaç karışması",
         "soru": "Teklistamab tedavisinde sitokin salınım sendromu için "
                 "basamaklı doz şeması nedir?",
         "gosterdigi": "Sorgu işleme olmadan elranatamab geliyordu"},
        {"baslik": "Geri ödeme",
         "soru": "SUT'a göre lenalidomid hangi koşullarda ödeniyor?",
         "gosterdigi": "Türkiye katmanı — SGK koşulları"},
        {"baslik": "Arşiv dışı soru",
         "soru": "Akut miyeloid lösemide 7+3 indüksiyon rejimi nasıl "
                 "uygulanır?",
         "gosterdigi": "Alan kapısı: sistem cevap üretmeyi reddediyor"},
        {"baslik": "Ruhsatsız ilaç",
         "soru": "Talkuetamab hangi hastalarda kullanılıyor?",
         "gosterdigi": "Türkiye'de ruhsatsız uyarısı"},
    ]
