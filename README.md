# SmartInvoice – Akıllı Fatura Denetleyici

SmartInvoice, Excel veya CSV formatındaki fatura verilerini analiz ederek; **tutar bazlı anormallikler**, **şüpheli açıklamalar**, **tekrarlayan işlemler** ve **müşteri bazında sıra dışı hareketler** gibi önemli noktaları tespit eden, Türkçe destekli bir veri denetim uygulamasıdır.

Yapay zekâ algoritmaları ve metin işleme teknikleri ile şirketlere, mali müşavirlere ve belediyelere fatura analizinde hız ve öngörü sağlar.

---

## Özellikler

- **Tutar Bazlı Anomali Tespiti** – Isolation Forest algoritması ile aykırı fatura tutarlarını belirler.  
- **NLP ile Şüpheli Açıklamalar** – Açıklama alanlarında geçen belirsiz veya kısa ifadeleri tespit eder.  
- **Tekrarlayan Açıklama ve Tutarlar** – Aynı açıklama ve benzer tutarla yinelenen faturaları bulur.  
- **Gelişmiş Anomali Tespiti** – Tutar, miktar, açıklama uzunluğu ve müşteri kimliği gibi çoklu özellikleri analiz eder.  
- **Müşteri/Firma Bazında Anomali** – Her müşterinin genel ortalamasına göre sıra dışı tutarları bulur.  
- **Otomatik Excel Raporu** – Tüm analizleri sekmeli bir Excel dosyası olarak indirilebilir sunar.  
- **Türkçe Streamlit Arayüzü** – Kullanımı kolay, sade, anlaşılır grafiksel kullanıcı arayüzü.

---

## Örnek Veri Seti Üzerinden Giriş Verisi

Uygulama; aşağıdaki sütunları içeren bir Excel (`.xlsx`) veya CSV (`.csv`) dosyasıyla çalışır:

| Gerekli Sütunlar     | Açıklama                             |
|----------------------|--------------------------------------|
| `Invoice`            | Fatura numarası                      |
| `Description`        | Açıklama metni (örn. hizmet bedeli)  |
| `Price`              | Fatura tutarı                        |
| `Quantity`           | Miktar (ürün adedi, opsiyonel)       |
| `Customer ID`        | Müşteri ya da firma numarası         |

---

## Raporlama Özelliği
- Analiz sonuçları tek tıkla indirilebilir, çok sekmeli bir Excel dosyasına dönüştürülür. Rapor sekmeleri:
- Tutar Bazlı Anomali
- Şüpheli Açıklamalar
- Tekrarlayan Faturalar
- Gelişmiş Anomali
- Müşteri Bazlı Anomali

---

## Kullanılan Teknolojiler

| Teknoloji            | Kullanım Amacı                       |
|----------------------|--------------------------------------|
| `Streamlit`          | Fatura numarası                      |
| `Pandas`             | Açıklama metni (örn. hizmet bedeli)  |
| `NumPy`              | Fatura tutarı                        |
| `LabelEncoder`       | Miktar (ürün adedi, opsiyonel)       |
| `XlsxWriter`         | Müşteri ya da firma numarası         |
| `io.BytesIO`         | Müşteri ya da firma numarası         |

---

## Her türlü geri bildirim veya öneri için:

E-posta: [sahinaliriza888@gmail.com](mailto:sahinaliriza888@gmail.com)  
GitHub: [github.com/aliriza5382](https://github.com/aliriza5382)
