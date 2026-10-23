@echo off
title Install DermaVision Dependencies
echo =====================================================================
echo Installing DermaVision Python Dependencies
echo =====================================================================
cd /d "%~dp0\.."
pip install -r requirements.txt
echo.
echo Dependencies installed successfully!
pause
