@echo off
title 数据归因分析系统 - 快速启动

:: 切换到脚本所在目录
cd /d %~dp0

:: 激活虚拟环境并启动应用
call venv\Scripts\activate.bat && python run.py

:: 如果出错，暂停以查看错误
if errorlevel 1 pause
