# payment_manual_rejected

Subject: Konfirmasi transfer Conversease perlu dicek ulang

Preheader: Admin belum bisa menyetujui konfirmasi transfer kamu.

CTA: Buka Billing

```html
<p>Hi {{ name }}, konfirmasi transfer untuk {{ package_name }} belum bisa disetujui.</p>
<p>Nominal order: {{ amount }}.</p>
<p>Catatan admin: {{ admin_notes }}</p>
<p>Buka halaman billing untuk membuat order baru atau hubungi support: <a href="{{ billing_url }}">{{ billing_url }}</a></p>
<p>Order ID: {{ order_id }}</p>
```

```txt
Hi {{ name }}, konfirmasi transfer untuk {{ package_name }} belum bisa disetujui. Nominal order: {{ amount }}. Catatan admin: {{ admin_notes }}. Buka halaman billing: {{ billing_url }}. Order ID: {{ order_id }}
```
