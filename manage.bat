@echo off
setlocal enabledelayedexpansion

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in your PATH.
    echo Please install Python 3 to run this tool.
    pause
    exit /b 1
)

:: Check if virtual environment exists and activate it
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

:: Run the python tool script
python dev_tool.py

:: If deactivated, deactivate virtualenv
if "%VIRTUAL_ENV%" neq "" (
    deactivate
)
