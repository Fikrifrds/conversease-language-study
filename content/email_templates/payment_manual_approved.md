# payment_manual_approved

Subject: Pembayaran Conversease kamu sudah disetujui

Preheader: Akses kamu sudah aktif setelah verifikasi transfer manual.

CTA: Lanjut Belajar

```html
<p>Hi {{ name }}, pembayaran {{ package_name }} kamu sudah disetujui.</p>
<p>Akses sudah aktif. Nominal yang diverifikasi: {{ amount }}.</p>
<p><a href="{{ dashboard_url }}">Lanjut belajar</a></p>
<p>Order ID: {{ order_id }}</p>
```

```txt
Hi {{ name }}, pembayaran {{ package_name }} kamu sudah disetujui. Akses sudah aktif. Nominal yang diverifikasi: {{ amount }}. Lanjut belajar: {{ dashboard_url }}. Order ID: {{ order_id }}
```
