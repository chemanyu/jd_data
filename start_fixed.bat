@echo off
chcp 65001 >nul
title 数据归因分析系统 - 启动脚本

echo ===============================================
echo    数据归因分析系统 - Windows 启动脚本
echo ===============================================
echo.

:: 设置项目根目录（当前脚本所在目录）
set PROJECT_DIR=%~dp0
cd /d %PROJECT_DIR%

echo [信息] 项目目录: %PROJECT_DIR%
echo.

:: 检查 Python 是否安装
echo [检查] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python 未安装或未添加到系统 PATH
    echo [提示] 请先安装 Python 3.8+ 并确保添加到系统 PATH
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [信息] Python 版本: %PYTHON_VERSION%
echo.

:: 检查虚拟环境是否存在
echo [检查] 检查虚拟环境...
if not exist "venv\" (
    echo [信息] 虚拟环境不存在，正在创建...
    python -m venv venv
    if errorlevel 1 (
        echo [错误] 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo [成功] 虚拟环境创建完成
) else (
    echo [信息] 虚拟环境已存在
)
echo.

:: 激活虚拟环境
echo [激活] 激活虚拟环境...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [错误] 激活虚拟环境失败
    pause
    exit /b 1
)
echo [成功] 虚拟环境已激活
echo.

:: 安装依赖
echo [安装] 检查并安装项目依赖...
if exist "requirements.txt" (
    echo [信息] 发现 requirements.txt，正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [警告] 使用requirements.txt安装失败，尝试备用方案...
        echo [信息] 使用国内镜像源重试...
        pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
        if errorlevel 1 (
            echo [信息] 尝试安装基础依赖包...
            pip install flask flask-login pymysql requests python-dotenv
            if errorlevel 1 (
                echo [错误] 所有安装方案都失败了
                echo [建议] 请检查网络连接或手动安装依赖
                pause
                exit /b 1
            )
        )
    )
    echo [成功] 依赖安装完成
) else (
    echo [警告] 未找到 requirements.txt 文件
    echo [信息] 尝试安装基础依赖...
    pip install flask flask-login pymysql requests python-dotenv
    if errorlevel 1 (
        echo [信息] 使用国内镜像源重试...
        pip install flask flask-login pymysql requests python-dotenv -i https://pypi.tuna.tsinghua.edu.cn/simple/
        if errorlevel 1 (
            echo [错误] 安装基础依赖失败
            pause
            exit /b 1
        )
    )
)
echo.

:: 检查配置文件
echo [检查] 检查配置文件...
if not exist "app\" (
    echo [错误] 应用目录不存在
    pause
    exit /b 1
)

if not exist "run.py" (
    echo [错误] 启动文件 run.py 不存在
    pause
    exit /b 1
)
echo [成功] 配置文件检查通过
echo.

:: 检查数据库配置
echo [提示] 请确保 MySQL 数据库服务已启动
echo [提示] 数据库配置信息在 app/database.py 中
echo [提示] 默认配置: host=127.0.0.1, user=root, database=release_atd
echo.

:: 启动应用
echo [启动] 正在启动数据归因分析系统...
echo [信息] 应用将在 http://127.0.0.1:5002 上运行
echo [提示] 默认登录信息 - 用户名: admin, 密码: admin123
echo [提示] 按 Ctrl+C 停止服务
echo.
echo ===============================================
echo              应用启动中...
echo ===============================================
echo.

python run.py

:: 如果程序异常退出，暂停以查看错误信息
if errorlevel 1 (
    echo.
    echo [错误] 应用启动失败，请检查上方错误信息
    pause
)
