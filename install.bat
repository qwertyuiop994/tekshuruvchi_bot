@echo off
chcp 65001 >nul
echo ======================================================
echo   Telegram Bot uchun kerakli kutubxonalarni o'rnatish
echo ======================================================
"%LOCALAPPDATA%\Python\bin\python.exe" -m pip install google-generativeai pydantic-settings
echo.
echo O'rnatish yakunlandi. Endi run.bat orqali botni ishga tushirishingiz mumkin!
pause
