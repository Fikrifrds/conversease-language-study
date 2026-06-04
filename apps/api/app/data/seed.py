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
            "Discounted Pro access",
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
            "Evaluation and skill report access",
        ],
    },
]

TOPUP_PACKAGES = [
    {"key": "topup_60", "name": "Paket 60 menit tambahan", "price_idr": 15000, "minutes": 60},
    {"key": "topup_200", "name": "Paket 200 menit tambahan", "price_idr": 39000, "minutes": 200},
    {"key": "topup_500", "name": "Paket 500 menit tambahan", "price_idr": 79000, "minutes": 500},
]

A1_COURSE = {
    "language_code": "en",
    "level_code": "A1",
    "level_name": "A1 - Start Simple Conversations",
    "course_slug": "english-a1-start-simple-conversations",
    "course_title": "Start Simple Conversations",
    "units": [
        {
            "slug": "unit-01-greeting-introducing-yourself",
            "title": "Greeting & Introducing Yourself",
            "outcome": "User can greet, introduce themselves, ask someone's name, say where they are from, and complete a first short conversation.",
            "lessons": [
                {
                    "slug": "saying-hello-and-goodbye",
                    "title": "Saying Hello and Goodbye",
                    "conversation_goal": "Start and close a very simple English conversation.",
                    "status": "published",
                    "estimated_minutes": 8,
                    "sections": [
                        "Conversation Goal",
                        "Situation Setup",
                        "Listen to a Dialogue",
                        "Understand the Conversation",
                        "Useful Phrases",
                        "Grammar for Conversation",
                        "Speak Clearly",
                        "Respond Practice",
                        "Conversation Coach Roleplay",
                        "Conversation Feedback",
                        "Conversation Check",
                    ],
                },
                {
                    "slug": "saying-your-name",
                    "title": "Saying Your Name",
                    "conversation_goal": "Say your name naturally and ask for someone's name.",
                    "status": "published",
                    "estimated_minutes": 8,
                    "sections": [
                        "Conversation Goal",
                        "Situation Setup",
                        "Listen to a Dialogue",
                        "Understand the Conversation",
                        "Useful Phrases",
                        "Grammar for Conversation",
                        "Speak Clearly",
                        "Respond Practice",
                        "Conversation Coach Roleplay",
                        "Conversation Feedback",
                        "Conversation Check",
                    ],
                },
                {
                    "slug": "asking-someones-name",
                    "title": "Asking Someone's Name",
                    "conversation_goal": "Ask and answer name questions politely.",
                    "status": "published",
                    "estimated_minutes": 8,
                    "sections": [
                        "Conversation Goal",
                        "Situation Setup",
                        "Listen to a Dialogue",
                        "Understand the Conversation",
                        "Useful Phrases",
                        "Grammar for Conversation",
                        "Speak Clearly",
                        "Respond Practice",
                        "Conversation Coach Roleplay",
                        "Conversation Feedback",
                        "Conversation Check",
                    ],
                },
                {
                    "slug": "saying-where-you-are-from",
                    "title": "Saying Where You Are From",
                    "conversation_goal": "Say where you are from and ask the same question back.",
                    "status": "published",
                    "estimated_minutes": 8,
                    "sections": [
                        "Conversation Goal",
                        "Situation Setup",
                        "Listen to a Dialogue",
                        "Understand the Conversation",
                        "Useful Phrases",
                        "Grammar for Conversation",
                        "Speak Clearly",
                        "Respond Practice",
                        "Conversation Coach Roleplay",
                        "Conversation Feedback",
                        "Conversation Check",
                    ],
                },
                {
                    "slug": "first-conversation-mission",
                    "title": "First Conversation Mission",
                    "conversation_goal": "Combine greeting, name, origin, and a polite closing in one short conversation.",
                    "status": "published",
                    "estimated_minutes": 10,
                    "sections": [
                        "Conversation Goal",
                        "Situation Setup",
                        "Listen to a Dialogue",
                        "Understand the Conversation",
                        "Useful Phrases",
                        "Grammar for Conversation",
                        "Speak Clearly",
                        "Respond Practice",
                        "Conversation Coach Roleplay",
                        "Conversation Feedback",
                        "Conversation Check",
                    ],
                },
            ],
        }
    ],
}

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
]
