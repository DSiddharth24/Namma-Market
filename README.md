# 🌾 Namma Market — WhatsApp AI Chatbot for Mandya Farmers

**ಮಂಡ್ಯ ಜಿಲ್ಲೆ ರೈತರಿಗಾಗಿ WhatsApp AI ಸಹಾಯಕ**

A WhatsApp chatbot built for farmers in Mandya district, Karnataka that provides:

- 📊 **Live APMC Market Rates** — Mandya, Maddur, Malavalli, Nagamangala, KR Pete, Pandavapura, Srirangapatna
- 🏛️ **Government Schemes** — PM-KISAN, PMFBY, KCC, Raita Siri, Soil Health Card, Drip Irrigation Subsidy
- ✅ **Eligibility Engine** — Interactive Q&A to check if farmer qualifies for any scheme
- 🏦 **Bank Loans** — KCC, Agriculture Term Loan, Crop Loan with Mandya bank contacts
- 🌿 **Crop & Fertilizer Advice** — Sugarcane, Paddy, Ragi, Tomato, Coconut, Banana
- 🛒 **Local Shop Recommendations** — Mandya fertilizer shops with contact numbers
- 🗣️ **Bilingual** — English + Kannada (ಕನ್ನಡ) in every response

---

## 🏗️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.11 + Flask |
| WhatsApp API | Twilio WhatsApp Business API |
| AI Brain | OpenAI GPT-4o-mini |
| Market Data | data.gov.in Agmarknet API |
| Session Storage | Redis (in-memory fallback) |
| Deployment | Any cloud (Railway, Render, AWS, GCP) |

---

## 🚀 Quick Setup

### 1. Prerequisites

- Python 3.11+
- Twilio account with WhatsApp Sandbox enabled
- OpenAI API key
- data.gov.in API key (free registration at [data.gov.in](https://data.gov.in))
- Redis (optional — falls back to in-memory)
- ngrok (for local testing)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
OPENAI_API_KEY=sk-...
DATA_GOV_API_KEY=your_data_gov_key
REDIS_URL=redis://localhost:6379/0
FLASK_SECRET_KEY=any-random-string
FLASK_ENV=development
PORT=5000
```

### 4. Get API Keys

#### Twilio WhatsApp Sandbox
1. Sign up at [twilio.com](https://twilio.com)
2. Go to **Messaging → Try it out → Send a WhatsApp message**
3. Follow sandbox setup (send join code from your phone)
4. Set webhook URL: `https://your-domain.com/webhook/whatsapp`

#### data.gov.in API Key (Free)
1. Register at [data.gov.in](https://data.gov.in)
2. Go to API section → Get your API key
3. The chatbot automatically falls back to curated Mandya rates if API is unavailable

#### OpenAI API Key
1. Get at [platform.openai.com](https://platform.openai.com)
2. GPT-4o-mini is used (cost-effective)

### 5. Run Locally

```bash
python app.py
```

### 6. Expose via ngrok (for Twilio webhook)

```bash
ngrok http 5000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok.io`) and set as Twilio webhook:
`https://abc123.ngrok.io/webhook/whatsapp`

---

## 📁 Project Structure

```
namma-market/
├── app.py                      # Flask app entry point
├── requirements.txt
├── .env.example
├── routes/
│   └── webhook.py              # Twilio WhatsApp webhook handler
├── services/
│   ├── ai_agent.py             # Main AI agent & conversation routing
│   ├── apmc_service.py         # APMC market rate fetching
│   ├── session_manager.py      # Redis/in-memory session management
│   └── eligibility_engine.py   # Scheme/loan eligibility checker
└── data/
    ├── schemes.py              # Government schemes data
    └── fertilizer_shops.py     # Crop advice + local shop data
```

---

## 💬 How It Works

```
Farmer sends WhatsApp message
         ↓
Twilio webhook → Flask /webhook/whatsapp
         ↓
ai_agent.handle_message()
         ↓
Intent Detection (APMC / Scheme / Loan / Fertilizer / Eligibility)
         ↓
Specialized handler OR GPT-4o-mini fallback
         ↓
Session state updated (Redis)
         ↓
Response sent back via Twilio
         ↓
Farmer receives bilingual reply (English + Kannada)
```

---

## 🌾 Supported Features

### 1. APMC Rates
Farmers can ask:
- "ಇಂದಿನ ಟೊಮೆಟೊ ದರ" (Today's tomato rate)
- "sugarcane price mandya"
- "show all rates"

### 2. Government Schemes
Ask about any scheme — bot explains benefit, eligibility, how to apply, and official contacts.

### 3. Eligibility Engine
Bot asks questions ONE BY ONE:
- Land ownership → income tax → government employee → Aadhaar status
- Gives ELIGIBLE/NOT ELIGIBLE with reasons and next steps

### 4. Bank Loans
- KCC at 4% effective interest
- Agriculture term loans
- Official bank contacts in Mandya

### 5. Crop & Fertilizer Advice
- Variety recommendations
- Fertilizer schedule (basal + top dressing)
- Water management
- Pest/disease management
- Nearest Mandya fertilizer shop with contact number

---

## 🌐 Deployment

### Railway (Recommended — Free tier available)
```bash
railway login
railway init
railway up
```

### Render
1. Connect GitHub repo
2. Set environment variables
3. Deploy (auto-detects Python)

### Procfile (already created for Heroku/Railway)
```
web: gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT
```

---

## 📞 Mandya Official Contacts in Bot

| Office | Number |
|--------|--------|
| Mandya APMC Yard | 08232-222-345 |
| District Agriculture Office | 08232-222-666 |
| Soil Testing Lab | 08232-222-888 |
| Horticulture Department | 08232-222-777 |
| Mandya Sugar Factory | 08232-222-200 |
| SBI Mandya | 08232-222-001 |
| Karnataka Grameena Bank | 08232-225-700 |
| PM-KISAN Helpline | 155261 |
| PMFBY Helpline | 14447 |

---

## 📝 License

MIT License — Free to use for agricultural development purposes.
