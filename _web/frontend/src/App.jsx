import React, { useEffect, useRef, useState } from 'react'

// Atif isaretleri: [K1], [K2, K3] gibi. Metni parcalayip tiklanabilir
// yapiyoruz - hekim kaynagi gormeden bir dozu uygulamamali.
const ATIF = /\[\s*K\s*\d+(?:\s*,\s*K?\s*\d+)*\s*\]/g

// Kaynak metinler Markdown'a cevrilmis PDF'lerden geliyor ve icinde HTML
// kaliyor: "20 mg/m<sup>2</sup>". Model bunu oldugu gibi aktariyor - ki dogru
// davranis, dozu yeniden yazmasini istemiyoruz. Temizlik GORUNTULEME
// katmaninda yapiliyor; cevap metnine dokunmuyoruz ki olculen sey ile
// gosterilen sey ayni kalsin.
function sadelestir(metin) {
  return metin
    .replace(/<sup>\s*([^<]*)<\/sup>/g, '$1')
    .replace(/<\/?(u|b|i|em|strong|mark|br|p)\s*\/?>/g, '')
}

function Cevap({ metin: ham, onKaynak }) {
  const metin = sadelestir(ham)
  const parcalar = []
  let son = 0
  for (const e of metin.matchAll(ATIF)) {
    if (e.index > son) parcalar.push({ tip: 'metin', deger: metin.slice(son, e.index) })
    const nolar = [...e[0].matchAll(/\d+/g)].map((x) => Number(x[0]))
    parcalar.push({ tip: 'atif', nolar })
    son = e.index + e[0].length
  }
  if (son < metin.length) parcalar.push({ tip: 'metin', deger: metin.slice(son) })

  return (
    <p className="cevap">
      {parcalar.map((p, i) =>
        p.tip === 'metin' ? (
          <span key={i}>{p.deger}</span>
        ) : (
          p.nolar.map((n) => (
            <button key={`${i}-${n}`} className="atif" onClick={() => onKaynak(n)}>
              K{n}
            </button>
          ))
        )
      )}
    </p>
  )
}

function Guven({ guven, onbellekten, sure }) {
  const seviye = guven?.seviye || 'dusuk'
  const etiket = { yuksek: 'Yüksek', orta: 'Orta', dusuk: 'Düşük' }[seviye]
  return (
    <div className="guven">
      <span className={`rozet ${seviye}`}>Güven: {etiket}</span>
      <span className="kucuk">
        arama {guven?.arama_skoru} · dayanak {guven?.dayanaklilik?.toFixed?.(2)}
      </span>
      <span className="kucuk">{sure} sn</span>
      {onbellekten && <span className="rozet onbellek">önbellekten</span>}
      {guven?.atif_onarimi && (
        <span className="rozet onarim">
          atıf onarıldı ({guven.atif_onarimi.eklenen} eklendi)
        </span>
      )}
    </div>
  )
}

export default function App() {
  const [soru, setSoru] = useState('')
  const [yanit, setYanit] = useState(null)
  const [bekliyor, setBekliyor] = useState(false)
  const [gecen, setGecen] = useState(0)
  const [hata, setHata] = useState(null)
  const [ornekler, setOrnekler] = useState([])
  const [kaynak, setKaynak] = useState(null)
  const [saglik, setSaglik] = useState(null)
  const sayac = useRef(null)

  useEffect(() => {
    fetch('/api/ornekler').then((r) => r.json()).then(setOrnekler).catch(() => {})
    fetch('/api/saglik').then((r) => r.json()).then(setSaglik).catch(() => {})
  }, [])

  // Gecen sure sayaci: GPU'suz makinede cevap bir dakikayi bulabiliyor.
  // Kullanici sistemin donup donmadigini bilmeli.
  useEffect(() => {
    if (bekliyor) {
      setGecen(0)
      sayac.current = setInterval(() => setGecen((x) => x + 1), 1000)
    } else clearInterval(sayac.current)
    return () => clearInterval(sayac.current)
  }, [bekliyor])

  async function gonder(metin) {
    const s = (metin ?? soru).trim()
    if (s.length < 3 || bekliyor) return
    setSoru(s)
    setBekliyor(true)
    setHata(null)
    setYanit(null)
    setKaynak(null)
    try {
      const y = await fetch('/api/soru', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ soru: s }),
      })
      if (!y.ok) throw new Error((await y.json()).detail || y.statusText)
      setYanit(await y.json())
    } catch (e) {
      setHata(String(e.message || e))
    } finally {
      setBekliyor(false)
    }
  }

  async function kaynakAc(no) {
    const k = (yanit?.guven?.tum_kaynaklar || yanit?.kaynaklar || []).find(
      (x) => x.no === no
    )
    if (!k) return
    setKaynak({ ...k, icerik: null })
    const y = await fetch(`/api/kaynak/${encodeURIComponent(k.chunk_id)}`)
    if (y.ok) {
      const d = await y.json()
      setKaynak({ ...k, icerik: d.icerik, metadata: d.metadata })
    }
  }

  const kaynakListesi = yanit?.guven?.tum_kaynaklar || yanit?.kaynaklar || []

  return (
    <div className="sayfa">
      <header>
        <h1>Multipl Miyelom Karar Destek</h1>
        <p className="alt">
          NCCN · ESMO · TİTCK KÜB · SGK SUT — yalnızca arşivdeki kaynaklara
          dayanır
        </p>
        {saglik && (
          <p className="kucuk">
            {saglik.chunk.toLocaleString('tr')} parça · {saglik.llm} · eşikler:
            arama {saglik.esikler.arama}, dayanak {saglik.esikler.dayanak}
          </p>
        )}
      </header>

      <div className="sorgu">
        <textarea
          value={soru}
          onChange={(e) => setSoru(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) gonder()
          }}
          placeholder="Klinik sorunuzu yazın… (Ctrl+Enter ile gönderin)"
          rows={3}
        />
        <button className="birincil" onClick={() => gonder()} disabled={bekliyor}>
          {bekliyor ? `Aranıyor… ${gecen} sn` : 'Sor'}
        </button>
      </div>

      {ornekler.length > 0 && !yanit && !bekliyor && (
        <div className="ornekler">
          {ornekler.map((o) => (
            <button key={o.soru} onClick={() => gonder(o.soru)} title={o.gosterdigi}>
              <b>{o.baslik}</b>
              <span>{o.gosterdigi}</span>
            </button>
          ))}
        </div>
      )}

      {bekliyor && (
        <div className="kutu bilgi">
          Arşiv taranıyor ve cevap üretiliyor. GPU'suz makinede bu adım
          dakikayı bulabilir.
        </div>
      )}

      {hata && <div className="kutu hata">Hata: {hata}</div>}

      {yanit && yanit.reddedildi && (
        <div className="kutu red">
          <h2>Cevap üretilmedi</h2>
          <p>{yanit.cevap}</p>
          <p className="kucuk">
            {yanit.red_nedeni === 'alan' &&
              'Alan kapısı: soru bu arşivin kapsamı dışında görünüyor.'}
            {yanit.red_nedeni === 'arama' &&
              'Arama kapısı: hiçbir parça benzerlik eşiğini geçmedi.'}
            {yanit.red_nedeni === 'dayanak' &&
              'Dayanak kapısı: üretilen cevap kaynaklara yeterince dayanmıyordu, gösterilmedi.'}
          </p>
          <Guven guven={yanit.guven} onbellekten={yanit.onbellekten} sure={yanit.sure} />
        </div>
      )}

      {yanit && !yanit.reddedildi && (
        <div className="sonuc">
          <Guven guven={yanit.guven} onbellekten={yanit.onbellekten} sure={yanit.sure} />

          {(yanit.guven?.uyarilar || []).map((u, i) => (
            <div key={i} className="kutu uyari">{u}</div>
          ))}

          <Cevap metin={yanit.cevap} onKaynak={kaynakAc} />

          <h3>Kaynaklar</h3>
          <ol className="kaynaklar">
            {kaynakListesi.map((k) => (
              <li key={k.no} className={yanit.kullanilan.includes(k.no) ? 'atifli' : ''}>
                <button onClick={() => kaynakAc(k.no)}>
                  K{k.no} · {k.belge || k.document_name}
                  {k.bolum ? ` — ${k.bolum}` : ''}
                </button>
              </li>
            ))}
          </ol>
          <p className="kucuk">
            Koyu olanlar cevapta atıf verilenler. Diğerleri bağlama girdi ama
            kullanılmadı.
          </p>
        </div>
      )}

      {kaynak && (
        <div className="ortu" onClick={() => setKaynak(null)}>
          <div className="panel" onClick={(e) => e.stopPropagation()}>
            <button className="kapat" onClick={() => setKaynak(null)}>×</button>
            <h3>K{kaynak.no} · {kaynak.belge || kaynak.document_name}</h3>
            {kaynak.bolum && <p className="kucuk">{kaynak.bolum}</p>}
            <pre>{kaynak.icerik ?? 'yükleniyor…'}</pre>
          </div>
        </div>
      )}

      <footer>
        Bu sistem klinik karar desteğidir, klinik kararın yerine geçmez.
        Cevaplar hematolog tarafından doğrulanmamıştır.
      </footer>
    </div>
  )
}
