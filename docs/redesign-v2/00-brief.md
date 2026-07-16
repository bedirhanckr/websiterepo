# Redesign V2 — Brief

_Bedirhan'ın 2026-07-16 tarihinde ilettiği v2 çalışma çerçevesi. Sonraki oturumlar başka bir bilgisayardan açıldığında bu dosya okunarak bağlam kurulur._

## Project goal

Bu bir developer portfolyosu değil — bir **industrial designer / design engineer**'ın uzun vadeli portfolyosu.

Site şunları anlatmalı: **industrial design · product development · engineering · manufacturing · prototyping · precision**.

**Görsel dil ilhamı** (layout / typography / renk / brand kopyalanmayacak, yalnızca prensipler):
- Layer Design
- Marc Newson
- Karim Rashid

Prensipler ORİJİNAL bir tasarım diline dönüştürülecek. Mevcut portfolyoda güçlü bir kimlik var — **replace etmiyoruz, evolve ediyoruz**.

## Workflow

- Mevcut sürüm = **V1** (main branch, canlı, korunuyor).
- V2 çalışması **`redesign-v2` yerel branch**'te (push yok, deploy yok, main'e dokunmaz).
- Preview'lar HTML artifact olarak sunulacak (dev.claude'a paralel URL yok).

## Kurallar

- Kod yazma — talep gelene kadar.
- Redesign her şeyi — bir kerede değil.
- Varsayım yapma — belirsizse sor.

## Görsel yön (V2 hedefi)

Site şu hissiyatı vermeli:

**Calm · Premium · Engineered · Editorial · Minimal · Industrial**

Kaçınılacak: trendy, flashy, SaaS, developer portfolio.

## Ben (Claude) rolüm

Lead frontend engineer ve design system architect.

## İlk görev

Kod dokunuşu YOK. Kapsamlı audit + design review + roadmap. Rapor only.

**Audit başlıkları** (20):
1. Framework · 2. Folder structure · 3. Component hierarchy · 4. Routing · 5. Styling system · 6. Animation libraries · 7. Typography system · 8. Color tokens · 9. Spacing system · 10. Hero implementation · 11. Project grid implementation · 12. Project detail pages · 13. About section · 14. Experience section · 15. Contact section · 16. Responsive implementation · 17. Build system · 18. Deployment · 19. Performance risks · 20. Accessibility issues

**Design review** — Creative Director gözüyle her bölüm için:
- Current quality · Problems · Improvement ideas · Priority
- Rating 1–10

**Roadmap** — V2.1, V2.2, V2.3, … her sürüm SADECE bir bölümü modifiye eder.

## Çıktı formatı

1. Audit  ·  2. Problems  ·  3. Opportunities  ·  4. Roadmap  ·  5. Risks

Onay bekle → sonrasında kod başlar.

## Ek dosyalar

Bedirhan `skills.md` ve diğer md dosyalarını ayrıca gönderecek. Onlar geldikçe bu klasöre eklenecek (`docs/redesign-v2/<NN>-<name>.md`), sonraki oturumlar sıraya bakarak yüklesin.
