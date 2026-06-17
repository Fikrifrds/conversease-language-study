from app.domain.email import EmailCategory, EmailTemplate


SUBSCRIPTION_PLANS = [
    {
        "key": "free",
        "name": "Free",
        "price_idr": 0,
        "duration_months": 0,
        "monthly_minutes": 10,
        "features": [
            "Selected A1 lessons",
            "Basic Conversation Feedback",
            "Trial Conversation Coach session",
        ],
    },
    {
        "key": "pro_1_month",
        "name": "Pro 1 Month",
        "price_idr": 49000,
        "duration_months": 1,
        "monthly_minutes": 300,
        "features": [
            "All active English lessons",
            "Arabic beta included",
            "Detailed Conversation Feedback",
            "Full A1 Level Conversation Test",
            "Monthly Conversation Coach practice quota",
        ],
    },
    {
        "key": "pro_3_months",
        "name": "Pro 3 Months",
        "price_idr": 129000,
        "duration_months": 3,
        "monthly_minutes": 300,
        "features": [
            "Discounted Pro All Access",
            "English active track and Arabic beta",
            "Monthly Conversation Coach quota reset",
            "Pro-only top-up support",
        ],
    },
    {
        "key": "pro_12_months",
        "name": "Pro 12 Months",
        "price_idr": 399000,
        "duration_months": 12,
        "monthly_minutes": 300,
        "features": [
            "Best value",
            "Full active curriculum access",
            "Arabic beta included",
            "Evaluation and skill report access",
        ],
    },
]

TOPUP_PACKAGES = [
    {"key": "topup_60", "name": "Paket 60 menit tambahan", "price_idr": 15000, "minutes": 60},
    {"key": "topup_200", "name": "Paket 200 menit tambahan", "price_idr": 39000, "minutes": 200},
    {"key": "topup_500", "name": "Paket 500 menit tambahan", "price_idr": 79000, "minutes": 500},
]

EMAIL_TEMPLATES = [
    EmailTemplate(
        template_key="auth_verify_email",
        category=EmailCategory.AUTH,
        subject="Verifikasi email Conversease kamu",
        preheader="Satu langkah lagi untuk mulai belajar lewat percakapan.",
        html_body=(
            '<p style="margin: 0 0 14px;">Hi {{ name }},</p>'
            '<p style="margin: 0 0 18px;">Verifikasi email kamu untuk mengaktifkan akun '
            "Conversease dan mulai mission pertama.</p>"
        ),
        text_body="Hi {{ name }}, buka link berikut untuk verifikasi email: {{ verify_url }}",
        cta_label="Verifikasi Email",
        cta_url="{{ verify_url }}",
    ),
    EmailTemplate(
        template_key="payment_success_subscription",
        category=EmailCategory.PAYMENT,
        subject="Pembayaran Pro Conversease berhasil",
        preheader="Akses Pro kamu sudah aktif.",
        html_body=(
            '<p style="margin: 0 0 14px;">Hi {{ name }}, pembayaran Pro kamu berhasil.</p>'
            '<p style="margin: 0 0 18px;">Akses Pro sudah aktif untuk kurikulum lengkap, '
            "feedback detail, evaluasi level, dan latihan Conversation Coach.</p>"
        ),
        text_body="Hi {{ name }}, pembayaran Pro kamu berhasil. Lanjut belajar: {{ dashboard_url }}",
        cta_label="Lanjut Belajar",
        cta_url="{{ dashboard_url }}",
    ),
    EmailTemplate(
        template_key="payment_manual_approved",
        category=EmailCategory.PAYMENT,
        subject="Pembayaran Conversease kamu sudah disetujui",
        preheader="Akses kamu sudah aktif setelah verifikasi transfer manual.",
        html_body=(
            '<p style="margin: 0 0 14px;">Hi {{ name }}, pembayaran {{ package_name }} kamu '
            "sudah disetujui.</p>"
            '<p style="margin: 0 0 14px;">Akses sudah aktif. Nominal yang diverifikasi: '
            "{{ amount }}.</p>"
            '<p style="margin: 0 0 18px; color: #78716c;">Order ID: {{ order_id }}</p>'
        ),
        text_body=(
            "Hi {{ name }}, pembayaran {{ package_name }} kamu sudah disetujui. "
            "Akses sudah aktif. Nominal yang diverifikasi: {{ amount }}. "
            "Lanjut belajar: {{ dashboard_url }}. Order ID: {{ order_id }}"
        ),
        cta_label="Lanjut Belajar",
        cta_url="{{ dashboard_url }}",
    ),
    EmailTemplate(
        template_key="payment_manual_rejected",
        category=EmailCategory.PAYMENT,
        subject="Konfirmasi transfer Conversease perlu dicek ulang",
        preheader="Admin belum bisa menyetujui konfirmasi transfer kamu.",
        html_body=(
            '<p style="margin: 0 0 14px;">Hi {{ name }}, konfirmasi transfer untuk '
            "{{ package_name }} belum bisa disetujui.</p>"
            '<p style="margin: 0 0 14px;">Nominal order: {{ amount }}.</p>'
            '<p style="margin: 0 0 14px;">Catatan admin: {{ admin_notes }}</p>'
            '<p style="margin: 0 0 18px; color: #78716c;">Order ID: {{ order_id }}</p>'
        ),
        text_body=(
            "Hi {{ name }}, konfirmasi transfer untuk {{ package_name }} belum bisa disetujui. "
            "Nominal order: {{ amount }}. Catatan admin: {{ admin_notes }}. "
            "Buka halaman billing: {{ billing_url }}. Order ID: {{ order_id }}"
        ),
        cta_label="Buka Billing",
        cta_url="{{ billing_url }}",
    ),
    EmailTemplate(
        template_key="minutes_low",
        category=EmailCategory.MINUTES,
        subject="Menit Conversation Coach kamu hampir habis",
        preheader="Top up agar latihan speaking tetap lancar.",
        html_body=(
            '<p style="margin: 0 0 14px;">Menit Conversation Coach kamu tersisa '
            "{{ remaining_minutes }} menit.</p>"
            '<p style="margin: 0 0 18px;">Top up jika kamu ingin lanjut latihan speaking '
            "tambahan tanpa menunggu reset kuota berikutnya.</p>"
        ),
        text_body=(
            "Menit Conversation Coach kamu tersisa {{ remaining_minutes }} menit. "
            "Top up: {{ billing_url }}"
        ),
        cta_label="Top Up Kuota Coach",
        cta_url="{{ billing_url }}",
    ),
    EmailTemplate(
        template_key="level_completed",
        category=EmailCategory.LEARNING,
        subject="Selamat! Kamu menyelesaikan level {{ completed_level }} 🎉",
        preheader="Level berikutnya sekarang terbuka.",
        html_body=(
            '<p style="margin: 0 0 14px;">Hi {{ name }},</p>'
            '<p style="margin: 0 0 14px;">Selamat! Kamu sudah menyelesaikan semua lesson di '
            "level {{ completed_level }} - {{ completed_level_title }}.</p>"
            '<p style="margin: 0 0 18px;">{{ next_level_message }}</p>'
        ),
        text_body=(
            "Hi {{ name }}, selamat! Kamu menyelesaikan level {{ completed_level }}. "
            "{{ next_level_message }} Lanjutkan: {{ courses_url }}"
        ),
        cta_label="Lanjut Belajar",
        cta_url="{{ courses_url }}",
    ),
]
