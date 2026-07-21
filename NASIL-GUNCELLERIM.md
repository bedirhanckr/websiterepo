# Siteyi nasıl güncellerim? — Bedirhan'ın el kitabı

_Claude olmadan siteyi güncellemek için pratik rehber. Panik yok: her şey geri alınabilir._

## Altın kurallar

1. **`main` branch'e push edilen her şey 1 dakika içinde canlıya gider.** Vercel otomatik yayınlar.
2. **Her değişiklik geri alınabilir.** Bir şey bozulursa Vercel panelinden tek tıkla önceki sürüme dönersin (aşağıda "Acil durum").
3. **Emin olmadığın CSS'e dokunma.** Metin ve görsel değişikliği güvenli, tasarım dosyaları (`assets/css/`) hassas.

---

## Yöntem A: GitHub web editörü (küçük değişiklikler, 2 dakika)

Yazım hatası düzeltme, bir cümleyi değiştirme, telefon/mail güncelleme için.

1. `github.com/bedirhanckr/websiterepo` aç, giriş yap
2. Değiştireceğin dosyaya tıkla (örn. `index.html`)
3. Sağ üstteki **kalem ikonuna** bas
4. Düzenle
5. Sağ üstte **"Commit changes"** → kısa bir açıklama yaz ("fix typo in hero") → onayla
6. 1 dakika bekle → siteyi yenile, canlıda

**Görsel yüklemek için:** klasöre gir (örn. `assets/img/pioneer-mk2/`) → **"Add file" → "Upload files"** → sürükle-bırak → Commit.

## Yöntem B: github.dev (birden çok dosya, kurulum yok)

Repo sayfasında klavyeden **`.` (nokta)** tuşuna bas. Tarayıcıda VS Code açılır.
Sol panelden dosyaları gez, düzenle, soldaki dal ikonundan (Source Control) commit + push et.

## Yöntem C: VS Code + GitHub Desktop (ciddi çalışma)

Tek seferlik kurulum:

1. [code.visualstudio.com](https://code.visualstudio.com) → VS Code indir
2. [desktop.github.com](https://desktop.github.com) → GitHub Desktop indir, GitHub hesabınla gir
3. GitHub Desktop → "Clone a repository" → `bedirhanckr/websiterepo` → klasör seç

Günlük akış:

1. GitHub Desktop'ı aç → **"Fetch origin"** (son hali çek — Claude da değişiklik yapmış olabilir!)
2. VS Code ile klasörü aç, düzenle
3. Önizleme: `index.html`'e sağ tık → "Open with Live Server" (eklenti) veya dosyayı tarayıcıya sürükle
4. GitHub Desktop → değişiklikleri gör → özet yaz → **"Commit to main"** → **"Push origin"**
5. 1 dakika sonra canlıda

> **Önemli:** Çalışmaya başlamadan önce hep "Fetch origin" + "Pull" yap. Yoksa Claude'un yaptığı değişikliklerle çakışırsın.

---

## Hangi dosya ne işe yarıyor?

| Dosya / klasör | İçerik | Risk |
|---|---|---|
| `index.html` | Ana sayfa iskeleti (İngilizce metinler) | Orta — tag'leri bozma |
| `assets/js/i18n.js` | **TR/DE/EN tüm çeviriler.** Bir metni değiştireceksen asıl yer burası: 3 dilde de değiştir | Düşük — sadece tırnak içindeki metni değiştir |
| `work/*.html` | 9 proje sayfası | Orta |
| `contact/index.html` | İletişim sayfası | Orta |
| `assets/img/` | Tüm görseller (proje klasörlerine ayrılmış) | Düşük — yeni dosya eklemek güvenli |
| `assets/css/tokens.css` | Renkler, fontlar, ölçüler | **Yüksek — dokunma** |
| `assets/css/style.css` | Tüm tasarım | **Yüksek — dokunma** |
| `cv/` | CV sayfaları (EN/DE/TR) | Düşük |
| `pdf/` | Portfolyo teslim sayfası (şu an "coming soon") | Düşük |
| `sitemap.xml`, `robots.txt` | Google SEO dosyaları | Orta — yapıyı koru |
| `vercel.json` | Yönlendirmeler, güvenlik başlıkları | **Yüksek — dokunma** |

## Sık işler tarifi

### Bir metni değiştirmek (3 dilde)

1. `assets/js/i18n.js` aç
2. Ctrl+F ile mevcut metni ara (örn. "Benim tutkum")
3. Aynı anahtarı (örn. `"home.h1"`) dosyada 3 kez bulacaksın: EN (~satır 45), DE (~satır 520), TR (~satır 990)
4. Üçünü de değiştir, tırnakları ve virgülleri koru
5. `index.html`'de de aynı metin varsa (fallback), orada da güncelle

### Yeni görsel eklemek

1. Görseli hazırla: JPG (quality 90) veya PNG, uzun kenar 1600-3200 px
2. `assets/img/<proje>/` klasörüne yükle, anlamlı isim ver (`hero-render.jpg`)
3. İlgili `work/<proje>.html` dosyasında eski görselin `src`'ini yeni dosya adına çevir
4. Mümkünse `.webp` versiyonu da koy (Claude'a bırakabilirsin, şart değil)

### Görseli değiştirmek (aynı isimle)

En kolayı: yeni görsele **eski dosyanın adını ver** ve üzerine yükle. HTML'e dokunmana gerek kalmaz.
Cache yüzünden hemen görünmezse `?v=20260801` gibi bir sürüm eki güncelle.

### CV'yi güncellemek

`cv/index.html` (EN), `cv/de/index.html`, `cv/tr/index.html` — üçünü de düzenle.
PDF CV'yi değiştirmek için: yeni PDF'i aynı adla (`CV-en-Bedirhan-Cakiroglu-0726.pdf`) yükle veya adını değiştirip `cv/` sayfalarındaki linki güncelle.

### Portfolyo hazır olunca /pdf/'i açmak

1. `pdf/index.html` sil (şu anki "coming soon" sayfası)
2. Hazır portfolyo dosyanı `pdf/index.html` olarak koy
3. `sitemap.xml`'e `/pdf/` URL bloğunu geri ekle
4. İçindeki `<meta name="robots" content="noindex, nofollow">` satırını kaldır

---

## Acil durum: site bozuldu

**Panik yok. İki yol:**

**Vercel rollback (30 saniye):**
1. [vercel.com](https://vercel.com) → giriş → websiterepo projesi
2. "Deployments" sekmesi
3. Bozulmadan önceki deployment'ı bul (yeşil, çalışan)
4. Sağındaki `⋯` menü → **"Promote to Production"**
5. Site anında eski haline döner

**GitHub revert:**
1. Repo → "Commits" listesi
2. Bozan commit'i bul → tıkla
3. Sağ üst `⋯` → "Revert commit" → onayla

## Güvenlik hatırlatması

- GitHub ve Vercel hesaplarında **2FA açık tut**
- Repo'ya asla şifre, API key, kişisel veri koyma — her şey herkese açık
- Tanımadığın "pull request" veya "collaborator" davetlerini kabul etme

## Claude ile çalışma notu

Claude da bu repo'da çalışıyor. Çakışmayı önlemek için:
- Kendi başına çalışmadan önce **Fetch/Pull** yap (son hali al)
- Büyük değişiklikleri ya hep Claude'a, ya hep kendine ayır — aynı dosyada aynı anda çalışmayın
