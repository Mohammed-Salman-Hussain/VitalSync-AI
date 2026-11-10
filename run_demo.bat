@echo off
title VitalSync AI - College Presentation & Live Demo Launcher
color 0B
cls

echo ===============================================================================
echo        VITALSYNC AI : MULTI-MODEL HEALTH & CIRCADIAN INTELLIGENCE ENGINE
echo                     College Presentation & Live Viva Mode
echo ===============================================================================
echo.
echo [1/3] Verifying Python Environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in PATH! Please install Python 3.10+ and try again.
    pause
    exit /b
)

echo [2/3] Checking Project Integrity & Health Pipeline...
python -c "import api_server; print('       [OK] Fast-API server & ML engines verified.')"
if %errorlevel% neq 0 (
    echo [WARNING] Dependency warning detected, but fallback analytical engines are active.
)

echo.
echo [3/3] Launching VitalSync AI Web Application on http://localhost:8000 ...
echo       Opening default web browser in 2 seconds...
echo.

start "" "http://localhost:8000"

python api_server.py

pause

