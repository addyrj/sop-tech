@echo off
REM =========================================
REM Django + XAMPP MySQL + Waitress Auto Start
REM =========================================

echo.
echo Starting XAMPP MySQL...
cd /d "C:\xampp\mysql\bin"
start "" mysqld.exe

REM Wait for MySQL to initialize
timeout /t 5 >nul

echo.
echo Activating virtual environment...
cd /d "C:\Users\Administrator\Desktop\sop_jazzmin_django"
call "C:\Users\Administrator\Desktop\sop_jazzmin_django\env\Scripts\activate.bat"

echo.
echo Starting Django with Waitress...
echo.

REM Open browser automatically (LAN IP)
start "" http://192.168.1.100:8000

REM Run Django using Waitress (Windows-safe)
waitress-serve --listen=192.168.1.100:8000 core.wsgi:application

REM Keep terminal open if server stops
pause

