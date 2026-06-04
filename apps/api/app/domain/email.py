from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from html import escape
import re
from typing import Dict, Optional


class EmailStatus(str, Enum):
    QUEUED = "queued"
    SENDING = "sending"
    SENT = "sent"
    DELIVERED = "delivered"
    BOUNCED = "bounced"
    FAILED = "failed"
    SUPPRESSED = "suppressed"


class EmailCategory(str, Enum):
    AUTH = "auth"
    PAYMENT = "payment"
    SUBSCRIPTION = "subscription"
    LEARNING = "learning"
    EVALUATION = "evaluation"
    MINUTES = "minutes"
    ADMIN = "admin"


@dataclass(frozen=True)
class EmailTemplate:
    template_key: str
    category: EmailCategory
    subject: str
    preheader: str
    html_body: str
    text_body: str
    cta_label: str
    cta_url: str
    language_code: str = "id"
    version: int = 1
    is_active: bool = True


@dataclass(frozen=True)
class EmailEvent:
    template_key: str
    recipient_email: str
    payload: Dict[str, str]
    idempotency_key: str
    status: EmailStatus = EmailStatus.QUEUED
    scheduled_at: Optional[datetime] = None


def build_idempotency_key(user_id: str, template_key: str, event_id: str) -> str:
    return f"{user_id}:{template_key}:{event_id}"


def render_template(template: str, payload: Dict[str, str]) -> str:
    rendered = template
    for key, value in payload.items():
        rendered = rendered.replace("{{ " + key + " }}", value)
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def unresolved_template_variables(rendered_template: str) -> list[str]:
    return sorted(set(re.findall(r"{{\s*([a-zA-Z0-9_]+)\s*}}", rendered_template)))


def public_asset_url(public_app_url: str, path: str) -> str:
    clean_path = path if path.startswith("/") else f"/{path}"
    return f"{public_app_url.rstrip('/')}{clean_path}"


def branded_email_html(
    *,
    public_app_url: str,
    preheader: str,
    title: str,
    body_html: str,
    cta_label: Optional[str] = None,
    cta_url: Optional[str] = None,
    footer_note: Optional[str] = None,
) -> str:
    logo_url = public_asset_url(public_app_url, "/logo.png")
    home_url = public_app_url.rstrip("/")
    safe_preheader = escape(preheader)
    safe_title = escape(title)
    safe_cta_label = escape(cta_label or "")
    safe_cta_url = escape(cta_url or "", quote=True)
    safe_footer_note = escape(
        footer_note or "Email ini dikirim otomatis oleh Conversease. Abaikan jika kamu tidak merasa melakukan tindakan ini."
    )
    cta_html = ""
    if cta_label and cta_url:
        cta_html = f"""
          <tr>
            <td style="padding: 8px 0 22px;">
              <a href="{safe_cta_url}" style="display: inline-block; background: #f97316; color: #ffffff; font-size: 15px; font-weight: 700; line-height: 20px; text-decoration: none; padding: 14px 22px; border-radius: 8px;">
                {safe_cta_label}
              </a>
            </td>
          </tr>
        """

    return f"""<!doctype html>
<html lang="id">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="color-scheme" content="light">
    <meta name="supported-color-schemes" content="light">
    <title>{safe_title}</title>
  </head>
  <body style="margin: 0; padding: 0; background: #fffaf5; color: #1c1917; font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;">
    <div style="display: none; max-height: 0; overflow: hidden; opacity: 0; color: transparent;">
      {safe_preheader}
    </div>
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background: #fffaf5; border-collapse: collapse;">
      <tr>
        <td align="center" style="padding: 34px 16px;">
          <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width: 600px; background: #ffffff; border: 1px solid #fed7aa; border-radius: 14px; overflow: hidden; box-shadow: 0 16px 50px rgba(124, 45, 18, 0.10); border-collapse: separate;">
            <tr>
              <td style="background: #1c1917; padding: 22px 28px;">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse;">
                  <tr>
                    <td style="vertical-align: middle;">
                      <a href="{home_url}" style="text-decoration: none;">
                        <img src="{logo_url}" width="40" height="40" alt="Conversease" style="display: inline-block; vertical-align: middle; border: 0; margin-right: 10px; background: #ffffff; border-radius: 8px;">
                        <span style="display: inline-block; vertical-align: middle; color: #ffffff; font-size: 18px; font-weight: 800;">Conversease</span>
                      </a>
                    </td>
                    <td align="right" style="color: #facc15; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em;">
                      Converse with ease
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding: 30px 28px 26px;">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse;">
                  <tr>
                    <td>
                      <h1 style="margin: 0 0 14px; color: #1c1917; font-size: 26px; line-height: 34px; font-weight: 800;">
                        {safe_title}
                      </h1>
                    </td>
                  </tr>
                  <tr>
                    <td style="color: #57534e; font-size: 15px; line-height: 24px;">
                      {body_html}
                    </td>
                  </tr>
                  {cta_html}
                  <tr>
                    <td style="padding: 16px 18px; background: #ffedd5; border-radius: 10px; color: #7c2d12; font-size: 13px; line-height: 20px;">
                      {safe_footer_note}
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
          <p style="margin: 18px 0 0; color: #78716c; font-size: 12px; line-height: 18px;">
            Conversease - Dari paham menjadi berani bicara.
          </p>
        </td>
      </tr>
    </table>
  </body>
</html>"""
