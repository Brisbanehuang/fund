@echo off
chcp 65001
setlocal enabledelayedexpansion

title Fund Analysis Tool

echo Checking Python environment...
where python >nul 2>nul
if %errorlevel% neq 0 (
    color 4F
    echo Error: Python not found. Please make sure Python is installed and added to PATH.
    echo You can download Python from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set pyver=%%i
echo Python version detected: %pyver%

echo.
echo ==========================================
echo             Fund Analysis Tool v2.0
echo ==========================================
echo.
echo  * Query: http://localhost:8501/基金查询
echo  * Favorites: http://localhost:8501/自选基金
echo  * Portfolio: http://localhost:8501/基金持仓
echo  * Compare: http://localhost:8501/基金比较
echo  * Investment Plan: http://localhost:8501/基金投资计划
echo  * More Features: http://localhost:8501/待开发
echo ==========================================
echo.

if not exist requirements.txt (
    echo Error: requirements.txt file not found.
    pause
    exit /b 1
)

echo.
echo Starting Fund Analysis Tool...
echo After startup, access the application at http://localhost:8501
echo.
echo Tips:
echo - Closing this window will terminate the application
echo - First-time fund data queries may be slow
echo.

REM 先尝试直接启动应用
python -m streamlit run main.py
set start_result=%errorlevel%

REM 如果启动失败，尝试安装依赖后再运行
if %start_result% neq 0 (
    echo.
    echo Application startup failed. Installing dependencies...
    python -m pip install --upgrade pip --quiet
    python -m pip install -r requirements.txt --quiet
    echo Dependencies installed successfully.
    echo.
    echo Trying to start the application again...
    python -m streamlit run main.py
)

echo.
echo Application closed.
pause