# docs/

Claude oturumlarında üretilen bütüncül analizler, audit'ler, raporlar burada arşivleniyor. Her dosyanın tepesinde bir Claude Code artifact linki varsa mobilden render'lı halini görürsün; git'ten indirip herhangi bir tarayıcıda da açılır.

Bu klasör **Netlify deploy'a dahil değil** — sadece git'te durur, `cakiroglu.netlify.app/docs/...` gitmez (404 dönar). Sen istediğin cihazdan GitHub üzerinden erişirsin.

## exports/

Her rapor `YYYY-MM-DD-<konu>.<ext>` formatında.

| Tarih       | Konu                       | Tip  | Notlar |
|-------------|----------------------------|------|--------|
| 2026-07-14  | Site audit (v1)            | HTML | 6 güçlü yön, 13 bulgu, 22-madde checklist, 3 blok aksiyon planı, motion planı. Claude Code artifact: https://claude.ai/code/artifact/d2a80f93-07c1-4b7c-9741-e1835209c2af |

## Nasıl aç

- **GitHub'da doğrudan görmek için**: [htmlpreview.github.io](https://htmlpreview.github.io/) servisi ham HTML'i render eder — dosya URL'sini oraya yapıştır. Örn:
  `https://htmlpreview.github.io/?https://github.com/bedirhanckr/websiterepo/blob/main/docs/exports/2026-07-14-site-audit.html`
- **Klonlanmış repo'da**: dosyayı çift tıkla, tarayıcıda açılır.
- **Artifact linki hâlâ canlıysa** (Claude Code hesabında oturum açıksa) o daha hoş görünür — tabloda link olan yerlerde onu kullan.
