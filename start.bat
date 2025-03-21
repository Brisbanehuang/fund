@echo off
chcp 65001 >nul
echo ===================================
echo    基金管理分析工具 - 启动程序
echo ===================================
echo.

echo 正在检查Python环境...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python环境，请安装Python 3.8或更高版本。
    echo 您可以从 https://www.python.org/downloads/ 下载安装。
    pause
    exit /b 1
)

echo 正在检查并安装依赖...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [警告] 依赖安装可能不完整，程序可能无法正常运行。
    echo 请尝试手动执行: pip install -r requirements.txt
    pause
) else (
    echo 依赖安装完成！
)

echo.
echo 正在启动基金分析工具...
echo 请稍候，应用程序窗口即将打开...
echo.

streamlit run main.py

if %errorlevel% neq 0 (
    echo [错误] 程序启动失败，请检查错误信息。
    pause
)