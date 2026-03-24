@echo off

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.6+
    echo 访问 https://www.python.org/downloads/ 下载并安装
    pause
    exit /b 1
)

REM 检查pip是否安装
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到pip，请确保Python安装时选择了pip
    pause
    exit /b 1
)

REM 安装PyInstaller
echo 正在安装PyInstaller...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo 错误: 安装PyInstaller失败
    pause
    exit /b 1
)

REM 打包程序
echo 正在打包程序...
pyinstaller --onefile --windowed --name "电脑优化大师" main.py

if %errorlevel% neq 0 (
    echo 错误: 打包失败
    pause
    exit /b 1
)

echo 打包成功！
echo 可执行文件位于 dist\电脑优化大师.exe
echo 请以管理员身份运行该文件
pause
