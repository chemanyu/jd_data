@echo off
chcp 65001 >nul
title 数据归因分析系统 - 生产环境启动脚本

echo ===============================================
echo   数据归因分析系统 - 生产环境启动脚本
echo ===============================================
echo.

:: 设置项目根目录
set PROJECT_DIR=%~dp0
cd /d %PROJECT_DIR%

echo [信息] 项目目录: %PROJECT_DIR%
echo.

:: 激活虚拟环境
echo [激活] 激活虚拟环境...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [错误] 激活虚拟环境失败，请先运行 start.bat 初始化环境
    pause
    exit /b 1
)

:: 安装生产服务器
echo [检查] 检查生产服务器依赖...
pip show waitress >nul 2>&1
if errorlevel 1 (
    echo [安装] 安装 Waitress 生产服务器...
    pip install waitress
    if errorlevel 1 (
        echo [错误] 安装 Waitress 失败
        pause
        exit /b 1
    )
)

:: 创建生产环境启动文件
if not exist "wsgi.py" (
    echo [创建] 创建 WSGI 启动文件...
    (
        echo from app import create_app
        echo from app.database import init_db
        echo.
        echo # 创建应用实例
        echo application = create_app^(^)
        echo.
        echo # 初始化数据库
        echo with application.app_context^(^):
        echo     init_db^(^)
        echo     print^("数据库初始化完成"^)
        echo.
        echo if __name__ == '__main__':
        echo     # 开发环境
        echo     application.run^(debug=False, host='0.0.0.0', port=5002^)
    ) > wsgi.py
)

echo.
echo [启动] 正在启动生产环境服务器...
echo [信息] 服务器地址: http://0.0.0.0:5002
echo [信息] 可通过以下地址访问:
echo         - http://localhost:5002
echo         - http://127.0.0.1:5002
echo         - http://[本机IP]:5002
echo [提示] 生产环境模式，性能更好，适合部署使用
echo [提示] 按 Ctrl+C 停止服务
echo.
echo ===============================================
echo           生产服务器启动中...
echo ===============================================
echo.

:: 使用 Waitress 启动
waitress-serve --host=0.0.0.0 --port=5002 --call wsgi:application

:: 如果 Waitress 启动失败，回退到 Flask 内置服务器
if errorlevel 1 (
    echo.
    echo [警告] Waitress 启动失败，回退到 Flask 内置服务器...
    python wsgi.py
)

if errorlevel 1 (
    echo.
    echo [错误] 服务器启动失败，请检查上方错误信息
    pause
)
