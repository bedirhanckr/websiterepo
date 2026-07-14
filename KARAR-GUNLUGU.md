# Portfolyo — Karar Günlüğü & Proje Bağlamı
_Son güncelleme: bu sohbetin sonunda. Claude Code'a geçerken bu dosyayı klasörde tut ve ilk iş olarak okut._

---

## KİM / KONUMLANDIRMA
- **Bedirhan Çakıroğlu** — Industrial Designer / Design Engineer, Paderborn (Almanya).
- Ana kimlik: **Endüstriyel tasarımcı** — ama mühendislik ekibiyle aynı dili konuşan, üretilebilirlik bilinciyle çalışan. (Almanya CV'sinde "Industrial Designer | Mechanical Design Engineer" ikili unvan kullanılıyor; site "Industrial Designer / Design Engineer" olarak hizalandı.)
- **Hedef:** İşe alım yöneticisi ilk 30-60 saniyede "Bu kişi güçlü bir Design Engineer, ürün geliştirme sürecini biliyor, üretilebilir tasarım yapabiliyor, teknik düşünme becerisi yüksek" desin.
- İletişim: bedirhanckr.id@gmail.com · linkedin.com/in/bedirhanckr · behance.net/bedirhanckr · +49 176 741 20 219
- **Dil:** Site 3 dilli — EN (varsayılan) / DE / TR. Bedirhan'la sohbet Türkçe.

## TASARIM DİLİ (onaylı)
- Braun / Dieter Rams fonksiyonel minimalizmi + İsviçre tipografisi + mühendislik hassasiyeti.
- Gri tonlama iskeleti + TEK sinyal rengi (Braun kırmızısı `#C1401F`), sadece işlevsel kullanım.
- Tipografi: Inter (gövde/arayüz) + JetBrains Mono (teknik etiketler, spec).
- İmza öğesi: teknik çizim ölçü çizgisinden gelen `dim-mark`.
- İSTENMEYEN: parallax, büyük gradient, neon, glassmorphism, gereksiz 3D, aşırı animasyon, "template" hissi, Behance-tarzı uzun galeriler.
- Sakin, sessiz-güçlü, zamansız, premium.

## MİMARİ
- Statik site, build tool yok. `build.py` üretici → hem `site/` (hosted, harici asset) hem `site-standalone/` (CSS/JS/görsel gömülü, her yerde açılır).
- Sayfa gövdeleri `bodies/*.html`, ortak header/footer/dil-seçici `build.py` içinde.
- Çeviriler `assets/js/i18n.js` (data-i18n attribute sistemi).
- Tasarım tokenları `assets/css/tokens.css`, bileşenler `assets/css/style.css` (10 bölümlü, dokümante).

## CASE STUDY ŞABLONU (13 aşama)
Problem → Araştırma → Tasarım Kriterleri → Konsept → Sketch → CAD → Mühendislik Kararları → DFM/DFA → Prototip → Testler → İterasyon → Nihai Tasarım → Kazanım.
Her aşama gerçek içerik gerektirir; olmayan aşama dürüstçe "bu aşama arşivlenmedi/sonraki adım" diye işaretlenir, uydurulmaz.

## PROJELER (7 aktif)
| Proje | Durum | Not |
|---|---|---|
| **Pioneer Mk2** (ROV baş modülü) | FLAGSHIP, tam case study yazıldı, 14 görsel | Açılış projesi. |
| **Spiegelau** (cam kadeh ailesi) | Görseller mevcut, case study yazıldı | Stok fotoğraflı 2 sayfa ÇIKARILDI. |
| **Urn** (sıcak içecek istasyonu) | İskelet + görsel bekleniyor | Scenario of Maintenance öne çıkacak. |
| **Rockhounder** (mezuniyet, 2.'lik) | İskelet + görsel bekleniyor | Çanta üretim süreci (CAD→kağıt kalıp→kumaş) ana hikaye. |
| **Herptile** (pregnancy pilates) | İskelet + görsel bekleniyor | Sac büküm/enjeksiyon + Service Blueprint. Fiziksel prototip yok (dürüst belirt). |
| **Delta** (kinematik mobilya) | İskelet + ödül fotoğrafı eklendi | "Mekanizma tasarımı" olarak çerçevele. 1:5 model, tam ölçek doğrulama YOK (dürüst belirt). |
| **Razor** (tıraş makinesi redesign) | İskelet + görsel bekleniyor | Onarılabilirlik teması, köpük prototip + banyo testi. |

## PORTFOLYODAN ÇIKARILANLAR
- **Visual Identity (Gentle Hype)** — grafik tasarım, odak dışı. ÇIKARILDI.
- **Søborg Chair** — Blender render pratiği, orijinal tasarım DEĞİL (birebir kopya). ASLA girmeyecek.
- Spiegelau'daki **stok/composite kadın fotoğrafları** — telif + "kendi işi gibi gösterme" riski. ÇIKARILDI.

## ROV — KRİTİK DOĞRULUK NOTU
- **Explorer** aracı → MATE ROV Norveç 3.'lük. Bedirhan'ın katkısı: planlama/geliştirme süreçleri (spesifik parça değil).
- **Pioneer Mk2** (torpido formlu) → sadece TEKNOFEST, genel derece YOK ama **Dizayn ve Sunum kategorisinde derece**. Baş modülü (iç braket + dış hidrodinamik kabuk) tamamen Bedirhan'ın bireysel tasarımı.
- İki aracı KARIŞTIRMA. Norveç sonucunu Pioneer'a mal etme.
- Turuncu renk: su altı görünürlüğü için bilinçli karar; üretimde zaman kısıtı yüzünden mevcut filamentle devam edildi → "gerçek üretim baskısı" hikayesi olarak öne çıkarılıyor, gizlenmiyor.
- **Ground Control Box**: Pioneer sayfasında "ek katkı, kavramsal" olarak; Bedirhan eskiz/araştırma/sunum + 3D model yaptı, sonrasını takip etmedi (dürüst belirt). Render'lar sonra gelecek.

## BEKLENEN MALZEMELER
- Urn, Rockhounder, Herptile, Razor render/görselleri.
- Ground Control Box render'ları.
- TUS Metallbau materyalleri — proje değil, CV/deneyim seviyesinde kullanılacak, en sona bırakıldı.

## GENEL KURALLAR
1. Hiçbir proje Behance'taki haliyle kalmaz, hepsi yeniden kurgulanır.
2. Akademik brief/ders kodu/hoca adı/dönem → her zaman çıkarılır.
3. Eksik/zayıf noktalar (tam ölçek doğrulama yokluğu vb.) gizlenmez, dürüstçe belirtilir — güven inşa eder.
4. Her proje "neden bu kararı verdim" cümlesine sahip olur, sadece "ne yaptım" değil.
5. **eBay'den hiçbir bağlamda bahsedilmez.**
6. Claude, net kararlarda inisiyatif alır; sadece stratejik belirsizlikte (proje dahil/çıkar, sıralama) onay ister.

## SONRAKİ ADIMLAR (Code'da)
1. Yerel sunucu başlat (`python3 -m http.server`), siteyi canlı gör.
2. Kalan 5 proje sayfasını gerçek görseller + 13 aşama şablonuyla doldur.
3. Pioneer & Spiegelau uzun metinlerini EN/DE'ye çevir (şu an gövde metinleri TR; yapı/nav çok dilli çalışıyor).
4. Ground Control Box'ı Pioneer sayfasına ekle (render gelince).
5. Hosting (Netlify/Vercel) + gerekirse PDF portfolyo versiyonu.
6. CV'yi site "Hakkımda" içeriğiyle senkronize et.
