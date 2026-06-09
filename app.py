"""
Namma Market - WhatsApp Chatbot for Mandya District Farmers
Main Flask Application Entry Point
"""

import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

from routes.webhook import webhook_bp

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "namma-market-secret")

# Register blueprints
app.register_blueprint(webhook_bp)


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "bot": "Namma Market", "district": "Mandya"}, 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=os.getenv("FLASK_ENV") != "production", host="0.0.0.0", port=port)
