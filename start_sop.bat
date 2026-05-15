@echo off
echo =========================
echo Starting Full IoT Django Stack
echo =========================

REM =========================
REM 1. Start Mosquitto MQTT Broker (Background)
REM =========================
tasklist | findstr /i "mosquitto.exe" >nul
if errorlevel 1 (
echo Starting Mosquitto MQTT Broker...
cd /d "C:\Program Files\mosquitto"
start /B mosquitto -c mosquitto.conf -v
) else (
echo Mosquitto already running.
)

REM =========================
REM 2. Start MySQL if not running
REM =========================
tasklist | findstr /i "mysqld.exe" >nul
if errorlevel 1 (
echo Starting MySQL...
start "" "C:\xampp\mysql\bin\mysqld.exe"
) else (
echo MySQL already running.
)

REM =========================
REM 3. Go to Django project root
REM =========================
cd /d "C:\Users\Administrator\Desktop\project\sop_jazzmin_django"

REM =========================
REM 4. Activate virtual environment
REM =========================
call env\Scripts\activate.bat

REM =========================
REM 5. Start Django Server
REM =========================
echo Starting Django development server...
start "" cmd /k python manage.py runserver 0.0.0.0:8000 --noreload

REM =========================
REM 6. Start MQTT Listener
REM =========================
echo Starting MQTT Listener...
start "" cmd /k python sop\mqtt_listener.py

REM =========================
REM 7. Wait for server startup
REM =========================
timeout /t 2 >nul

REM =========================
REM 8. Open browser
REM =========================
start http://192.168.1.100:8000
