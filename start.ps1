# 数据归因分析系统 - PowerShell 启动脚本
# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "数据归因分析系统 - PowerShell 启动脚本"

# 颜色定义
$InfoColor = "Cyan"
$SuccessColor = "Green"
$WarningColor = "Yellow"
$ErrorColor = "Red"

Write-Host "===============================================" -ForegroundColor $InfoColor
Write-Host "    数据归因分析系统 - PowerShell 启动脚本" -ForegroundColor $InfoColor
Write-Host "===============================================" -ForegroundColor $InfoColor
Write-Host ""

# 获取脚本所在目录
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectDir

Write-Host "[信息] 项目目录: $ProjectDir" -ForegroundColor $InfoColor
Write-Host ""

# 检查 Python 是否安装
Write-Host "[检查] 检查 Python 环境..." -ForegroundColor $InfoColor
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python 未安装或未添加到系统 PATH"
    }
    Write-Host "[信息] Python 版本: $pythonVersion" -ForegroundColor $SuccessColor
} catch {
    Write-Host "[错误] Python 未安装或未添加到系统 PATH" -ForegroundColor $ErrorColor
    Write-Host "[提示] 请先安装 Python 3.8+ 并确保添加到系统 PATH" -ForegroundColor $WarningColor
    Read-Host "按回车键退出"
    exit 1
}
Write-Host ""

# 检查虚拟环境
Write-Host "[检查] 检查虚拟环境..." -ForegroundColor $InfoColor
if (-not (Test-Path "venv")) {
    Write-Host "[信息] 虚拟环境不存在，正在创建..." -ForegroundColor $WarningColor
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] 创建虚拟环境失败" -ForegroundColor $ErrorColor
        Read-Host "按回车键退出"
        exit 1
    }
    Write-Host "[成功] 虚拟环境创建完成" -ForegroundColor $SuccessColor
} else {
    Write-Host "[信息] 虚拟环境已存在" -ForegroundColor $SuccessColor
}
Write-Host ""

# 激活虚拟环境
Write-Host "[激活] 激活虚拟环境..." -ForegroundColor $InfoColor
try {
    & "venv\Scripts\Activate.ps1"
    Write-Host "[成功] 虚拟环境已激活" -ForegroundColor $SuccessColor
} catch {
    Write-Host "[错误] 激活虚拟环境失败" -ForegroundColor $ErrorColor
    Write-Host "[提示] 可能需要设置 PowerShell 执行策略: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor $WarningColor
    Read-Host "按回车键退出"
    exit 1
}
Write-Host ""

# 安装依赖
Write-Host "[安装] 检查并安装项目依赖..." -ForegroundColor $InfoColor
if (Test-Path "requirements.txt") {
    Write-Host "[信息] 发现 requirements.txt，正在安装依赖..." -ForegroundColor $InfoColor
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] 安装依赖失败" -ForegroundColor $ErrorColor
        Read-Host "按回车键退出"
        exit 1
    }
    Write-Host "[成功] 依赖安装完成" -ForegroundColor $SuccessColor
} else {
    Write-Host "[警告] 未找到 requirements.txt 文件" -ForegroundColor $WarningColor
    Write-Host "[信息] 尝试安装基础依赖..." -ForegroundColor $InfoColor
    pip install flask flask-login pymysql requests
}
Write-Host ""

# 检查配置文件
Write-Host "[检查] 检查配置文件..." -ForegroundColor $InfoColor
if (-not (Test-Path "app")) {
    Write-Host "[错误] 应用目录不存在" -ForegroundColor $ErrorColor
    Read-Host "按回车键退出"
    exit 1
}

if (-not (Test-Path "run.py")) {
    Write-Host "[错误] 启动文件 run.py 不存在" -ForegroundColor $ErrorColor
    Read-Host "按回车键退出"
    exit 1
}
Write-Host "[成功] 配置文件检查通过" -ForegroundColor $SuccessColor
Write-Host ""

# 数据库提示
Write-Host "[提示] 请确保 MySQL 数据库服务已启动" -ForegroundColor $WarningColor
Write-Host "[提示] 数据库配置信息在 app/database.py 中" -ForegroundColor $WarningColor
Write-Host "[提示] 默认配置: host=127.0.0.1, user=root, database=release_atd" -ForegroundColor $WarningColor
Write-Host ""

# 启动应用
Write-Host "[启动] 正在启动数据归因分析系统..." -ForegroundColor $InfoColor
Write-Host "[信息] 应用将在 http://127.0.0.1:5002 上运行" -ForegroundColor $InfoColor
Write-Host "[提示] 默认登录信息 - 用户名: admin, 密码: admin123" -ForegroundColor $WarningColor
Write-Host "[提示] 按 Ctrl+C 停止服务" -ForegroundColor $WarningColor
Write-Host ""
Write-Host "===============================================" -ForegroundColor $InfoColor
Write-Host "              应用启动中..." -ForegroundColor $InfoColor
Write-Host "===============================================" -ForegroundColor $InfoColor
Write-Host ""

try {
    python run.py
} catch {
    Write-Host ""
    Write-Host "[错误] 应用启动失败，请检查上方错误信息" -ForegroundColor $ErrorColor
    Read-Host "按回车键退出"
}
