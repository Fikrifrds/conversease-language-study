# payment_manual_rejected

Subject: Konfirmasi transfer Conversease perlu dicek ulang

Preheader: Admin belum bisa menyetujui konfirmasi transfer kamu.

CTA: Buka Billing

```html
<p style="margin: 0 0 14px;">Hi {{ name }}, konfirmasi transfer untuk {{ package_name }} belum bisa disetujui.</p>
<p style="margin: 0 0 14px;">Nominal order: {{ amount }}.</p>
<p style="margin: 0 0 14px;">Catatan admin: {{ admin_notes }}</p>
<p style="margin: 0 0 18px; color: #78716c;">Order ID: {{ order_id }}</p>
```

```txt
Hi {{ name }}, konfirmasi transfer untuk {{ package_name }} belum bisa disetujui. Nominal order: {{ amount }}. Catatan admin: {{ admin_notes }}. Buka halaman billing: {{ billing_url }}. Order ID: {{ order_id }}
```
