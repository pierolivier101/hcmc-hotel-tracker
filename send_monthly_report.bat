@echo off
color 0b
echo ====================================================
echo   MONTHLY REPORT REMINDER: HCMC Hotel Tracker
echo ====================================================
echo.
echo It is time to send the monthly price report!
echo This script will download the latest data from GitHub
echo and send the Excel report securely from this computer.
echo.
pause

echo.
echo [1/3] Downloading latest daily data from GitHub...
curl -s -o history.json https://raw.githubusercontent.com/pierolivier101/hcmc-hotel-tracker/main/history.json
if %errorlevel% neq 0 (
    color 0c
    echo Error: Failed to download history.json from GitHub. Please check your internet connection.
    pause
    exit /b
)

echo [2/3] Generating Excel Report and Sending Email...
python monthly_reporter.py

echo.
echo [3/3] Finished! The email has been sent.
echo.
pause
