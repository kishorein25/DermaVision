@echo off
title DermaVision - 7-Region Dermatology AI
echo ===================================================
echo Starting DermaVision Web Dashboard...
echo ===================================================
cd /d D:\DermaVision
python -m streamlit run app.py
pause
