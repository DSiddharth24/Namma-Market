@echo off
title Namma Market Bot
echo.
echo  ==========================================
echo   NAMMA MARKET WhatsApp Bot - Starting...
echo  ==========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check .env exists
if not exist .env (
    echo  [ERROR] .env file not found!
    echo  Run: copy .env.example .env
    echo  Then fill in your API keys.
    pause
    exit /b 1
)

echo  [1/2] Starting Flask server on port 5000...
echo  [2/2] Open a NEW terminal and run: ngrok http 5000
echo.
echo  Then set Twilio webhook to your ngrok URL:
echo  https://YOUR-NGROK-ID.ngrok.io/webhook/whatsapp
echo.
echo  Health check: http://localhost:5000/health
echo.

venv\Scripts\python app.py
pause
