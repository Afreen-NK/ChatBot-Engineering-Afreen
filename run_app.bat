@echo off
title CareerCompass FAQ Chatbot
echo ===================================================
echo     Launching CareerCompass Assistant...
echo ===================================================
echo.
echo Opening web browser at http://127.0.0.1:5000 ...
start http://127.0.0.1:5000
echo.
echo Starting Flask application server...
py app.py
pause
