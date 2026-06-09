"""
Twilio WhatsApp Webhook Handler
Receives incoming WhatsApp messages, routes to AI agent, sends response.
"""

import os
from flask import Blueprint, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator

from services.ai_agent import handle_message

webhook_bp = Blueprint("webhook", __name__)

TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")


def _validate_twilio_request(f):
    """Optional Twilio signature validation decorator."""
    def wrapper(*args, **kwargs):
        if os.getenv("FLASK_ENV") == "production" and TWILIO_AUTH_TOKEN:
            validator = RequestValidator(TWILIO_AUTH_TOKEN)
            url = request.url
            post_data = request.form
            signature = request.headers.get("X-Twilio-Signature", "")
            if not validator.validate(url, post_data, signature):
                return Response("Forbidden", status=403)
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


@webhook_bp.route("/webhook/whatsapp", methods=["POST"])
@_validate_twilio_request
def whatsapp_webhook():
    """
    Twilio sends incoming WhatsApp messages to this endpoint.
    We process the message and reply via TwiML.
    """
    incoming_msg = request.form.get("Body", "").strip()
    sender = request.form.get("From", "")  # e.g., whatsapp:+919876543210

    # Extract phone number (without 'whatsapp:' prefix)
    phone = sender.replace("whatsapp:", "").strip()

    print(f"[Webhook] From: {phone} | Message: {incoming_msg[:100]}")

    if not incoming_msg and not sender:
        return Response("OK", status=200)

    # Get response from AI agent
    try:
        reply = handle_message(phone, incoming_msg)
    except Exception as e:
        print(f"[Webhook] Error processing message: {e}")
        reply = (
            "🙏 ಕ್ಷಮಿಸಿ, ಸಮಸ್ಯೆ ಎದುರಾಗಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೊಮ್ಮೆ ಪ್ರಯತ್ನಿಸಿ.\n"
            "Sorry, an error occurred. Please try again.\n"
            "📞 Help: 08232-222-666"
        )

    # Split long messages (WhatsApp limit is ~4096 chars, but we keep it readable)
    messages = _split_message(reply, max_len=1500)

    resp = MessagingResponse()
    for msg_part in messages:
        resp.message(msg_part)

    print(f"[Webhook] Reply to {phone}: {reply[:100]}...")
    return Response(str(resp), mimetype="application/xml")


def _split_message(text: str, max_len: int = 1500) -> list:
    """Split a long message into chunks at natural break points."""
    if len(text) <= max_len:
        return [text]

    parts = []
    current = ""
    for line in text.split("\n"):
        if len(current) + len(line) + 1 > max_len:
            if current:
                parts.append(current.strip())
            current = line
        else:
            current += ("\n" if current else "") + line

    if current:
        parts.append(current.strip())

    return parts if parts else [text[:max_len]]
