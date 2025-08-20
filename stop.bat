@echo off
chcp 65001 >nul
title 数据归因分析系统 - 停止脚本

echo ===============================================
echo    数据归因分析系统 - 停止服务脚本
echo ===============================================
echo.

echo [信息] 正在查找运行中的应用进程...

:: 查找并终止Python进程（包含run.py）
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" /fo table /nh 2^>nul ^| findstr python') do (
    echo [发现] Python 进程 PID: %%i
    taskkill /pid %%i /f >nul 2>&1
    if not errorlevel 1 (
        echo [成功] 已停止进程 %%i
    )
)

:: 查找并终止可能的Flask进程
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" /fo table /nh 2^>nul') do (
    for /f %%j in ('wmic process where "ProcessId=%%i" get CommandLine /value 2^>nul ^| findstr "run.py"') do (
        echo [发现] Flask 应用进程 PID: %%i
        taskkill /pid %%i /f >nul 2>&1
        if not errorlevel 1 (
            echo [成功] 已停止 Flask 应用 %%i
        )
    )
)

:: 释放端口（如果被占用）
echo [检查] 检查端口 5002 使用情况...
for /f "tokens=5" %%i in ('netstat -ano ^| findstr ":5002"') do (
    echo [发现] 端口 5002 被进程 %%i 占用
    taskkill /pid %%i /f >nul 2>&1
    if not errorlevel 1 (
        echo [成功] 已释放端口 5002
    )
)

echo.
echo [完成] 服务停止操作完成
echo [提示] 如果仍有残留进程，请手动检查任务管理器
echo.
pause
