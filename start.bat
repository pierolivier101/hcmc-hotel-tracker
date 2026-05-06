@echo off
echo ==============================================
echo      HCMC Premium Hotel Price Tracker
echo ==============================================
echo.
echo Running daily scraper to check newest prices...
python scraper.py
echo.
echo Starting local server...
start "" http://localhost:8000
timeout /t 1 >nul
python -m http.server 8000 --bind 0.0.0.0
