@echo off
title DermaVision Clinical AI Server
echo =====================================================================
echo Launching DermaVision 7-Region Dermatology AI Server
echo =====================================================================
cd /d "%~dp0\.."
python -m streamlit run app.py --server.port 8501 --server.headless false
pause
