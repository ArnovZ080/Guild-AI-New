"""Guild-owned transactional mailer (SendGrid). Users never configure this."""
import logging
import httpx

from services.core.config import settings

logger = logging.getLogger(__name__)


class EmailNotConfigured(Exception):
    pass


async def send_email(to_email: str, to_name: str, subject: str, body: str,
                     reply_to: str | None = None) -> dict:
    """Send one email. Returns {"status": "sent", "message_id": ...} or raises."""
    if not settings.SENDGRID_API_KEY:
        raise EmailNotConfigured("SENDGRID_API_KEY not set")

    payload = {
        "personalizations": [{"to": [{"email": to_email, "name": to_name or ""}]}],
        "from": {"email": settings.EMAIL_FROM, "name": settings.EMAIL_FROM_NAME},
        "subject": subject,
        "content": [{"type": "text/plain", "value": body}],
    }
    if reply_to:
        payload["reply_to"] = {"email": reply_to}

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(
            "https://api.sendgrid.com/v3/mail/send",
            json=payload,
            headers={"Authorization": f"Bearer {settings.SENDGRID_API_KEY}"},
        )
    if r.status_code != 202:
        raise RuntimeError(f"SendGrid {r.status_code}: {r.text[:300]}")
    return {"status": "sent",
            "message_id": r.headers.get("X-Message-Id", "")}
