# Almanya'ya taşınma — devir teslim (2026-07-11)

Bedirhan 2026-07-11'de Almanya'ya döndü; iş oradaki PC'de devam edecek. Bu dosya yeni makinede ilk oturumda okunmalı, sonra silinebilir (içeriği PROJECT_STATUS.md'ye işlendiğinde).

## Yanında götürülecekler (öncelik sırasıyla)

1. **`Desktop\portfolio-hosted\` klasörünün tamamı** — 15,5 GB, harici disk/USB gerekir. Tam arşiv (`assets/img/` içindeki 2545 dosyalık döküm) burada; kalan 7 placeholder'ı doldurmak ve render/thumbnail işleri için şart.
   - Acil minimum (arşivsiz devam): `Desktop\portfolio-stage\` (147 MB, üretim kaynağının güncel kopyası) + bu klasördeki tüm `.md` dosyaları. Bulut ile taşınabilir. Ama arşiv olmadan placeholder doldurma ve render işleri yapılamaz.
2. **`Desktop\files\` klasörü** — Claude Code proje kökü: `CLAUDE.md`, `.claude\launch.json` (dev sunucu, port 8021), `.claude\serve.ps1`. Bunlar olmadan yeni PC'de oturum sıfırdan kurulur.
3. **`Desktop\netlify-linux.zip`** (~57 MB) — 2026-07-11'de yeniden üretildi, canlıya atılmayı bekliyor (aşağıya bak). Almanya'dan da atılabilir, zip'i taşımak yeterli. Not: `portfolio-stage\` ve zip artık `portfolio-hosted\rebuild-stage.ps1` ile tek komutla yeniden üretilebiliyor (staging bir kez kayboldu, o yüzden script'e bağladık) — elle kopyalama yapma, script'i çalıştır.

## Yeni PC'de ilk kurulum

1. `portfolio-hosted\` ve `files\` klasörlerini Desktop'a (veya herhangi bir yere) kopyala; yol değişirse `files\CLAUDE.md` içindeki mutlak yolları ve `launch.json`'daki `serve.ps1` yolunu güncelle.
2. Claude Code'u `files\` klasöründe aç — `CLAUDE.md` durumu yükler. Not: Claude'un otomatik hafızası makineye bağlıdır, yeni PC'de boş başlar; tüm proje durumu zaten `PROJECT_STATUS.md` / `PRIORITY.md` / `MEMORY.md` içinde.
3. **Yeni PC'de Python veya Node var mı kontrol et.** Varsa şu bloke işler açılır: standalone CV PDF'lerindeki eski Alias/CATIA listesinin düzeltilmesi (pypdf), `build.py` onarımı. Yoksa aynı elle-senkron düzeni devam eder.
4. Port 8021 yeni makinede muhtemelen boştur; sorun çıkarsa `launch.json`'da değiştir.

## Bekleyen tek manuel iş: Netlify deploy

`netlify-linux.zip` (2026-07-11 sürümü) canlı siteyi güncelleyecek: proje açıklaması düzeltmeleri (Spiegelau/Retroscent/Delta/Rockhounder/Pioneer MKII), `pdf/` destesi, vaka bölümü boşluk artışı, ve **iç dokümanların kaldırılması** (önceki deploy'da MEMORY.md, KARAR-GUNLUGU.md vb. herkese açıktı; bu zip'te yoklar).

Yapılacak: app.netlify.com → cakiroglu site → Deploys → zip'i sürükle-bırak.

## Almanya'da ilk iş kuyruğu

1. Netlify deploy (üstte).
2. 7 boş slot için tarama/re-render: Pioneer sketch, Rockhounder sketch + extra, REX sketch, Delta sketch, Razor extra, Retroscent sketch → `assets/img/<proje>/` içine at, oturuma yolları söyle.
3. Sonrası `PRIORITY.md` sırasıyla devam.
