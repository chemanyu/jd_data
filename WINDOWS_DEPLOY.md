# Windows 部署指南

## 系统要求

- Windows 10/11 或 Windows Server 2019+
- Python 3.8 或更高版本
- MySQL 8.0 或更高版本（或兼容的数据库）
- 至少 2GB 可用内存
- 至少 1GB 可用磁盘空间

## 安装步骤

### 1. 安装 Python

1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载 Python 3.8+ 版本
3. 安装时**务必勾选** "Add Python to PATH"
4. 验证安装：打开命令行，输入 `python --version`

### 2. 安装 MySQL

1. 访问 [MySQL 官网](https://dev.mysql.com/downloads/mysql/)
2. 下载并安装 MySQL Server
3. 记住设置的 root 密码
4. 确保 MySQL 服务已启动

### 3. 配置数据库

1. 打开 MySQL 命令行或 MySQL Workbench
2. 创建数据库：
   ```sql
   CREATE DATABASE release_atd CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. 创建用户（可选）：
   ```sql
   CREATE USER 'jd_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON release_atd.* TO 'jd_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### 4. 部署应用

1. 将项目文件复制到目标服务器
2. 编辑 `app/database.py` 配置数据库连接信息
3. 双击运行 `start.bat` 进行初始化

## 启动脚本说明

### start.bat - 开发环境启动
- 自动检查并创建虚拟环境
- 安装项目依赖
- 启动开发服务器
- 适合开发和测试使用

### start_production.bat - 生产环境启动
- 使用 Waitress 高性能服务器
- 适合生产部署
- 支持更多并发连接

### start.ps1 - PowerShell 启动脚本
- 功能与 start.bat 相同
- 更好的错误处理和彩色输出
- 需要设置 PowerShell 执行策略

### stop.bat - 停止服务
- 自动查找并终止应用进程
- 释放占用的端口

## 配置说明

### 数据库配置 (app/database.py)
```python
DB_CONFIG = {
    'host': '127.0.0.1',      # 数据库主机
    'user': 'root',           # 数据库用户名
    'password': '',           # 数据库密码
    'database': 'release_atd', # 数据库名
    'charset': 'utf8mb4'
}
```

### 应用配置 (run.py)
```python
app.run(debug=False, host='0.0.0.0', port=5002)
```
- `debug=False`: 生产环境请设为 False
- `host='0.0.0.0'`: 允许外部访问
- `port=5002`: 应用端口

## 使用方法

### 1. 首次启动
1. 双击 `start.bat`
2. 等待依赖安装完成
3. 打开浏览器访问 `http://localhost:5002`
4. 使用默认账号登录：
   - 用户名：admin
   - 密码：admin123

### 2. 日常使用
- 启动：双击 `start.bat` 或 `start_production.bat`
- 停止：按 Ctrl+C 或运行 `stop.bat`
- 访问：浏览器打开 `http://localhost:5002`

### 3. 生产部署
1. 使用 `start_production.bat` 启动
2. 配置防火墙允许端口 5002
3. 考虑使用 IIS 或 Nginx 作为反向代理

## 故障排除

### 常见问题

1. **Python 未找到**
   - 确保 Python 已安装并添加到 PATH
   - 重新安装 Python 并勾选 "Add to PATH"

2. **数据库连接失败**
   - 检查 MySQL 服务是否启动
   - 验证数据库配置信息
   - 确保数据库已创建

3. **端口被占用**
   - 运行 `stop.bat` 释放端口
   - 或在 `run.py` 中修改端口号

4. **依赖安装失败**
   - 检查网络连接
   - 尝试使用国内镜像：
     ```
     pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
     ```

5. **PowerShell 执行策略错误**
   - 以管理员身份打开 PowerShell
   - 执行：`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 日志查看
- 应用日志会显示在命令行窗口中
- MySQL 日志通常在 MySQL 安装目录的 `data` 文件夹中

### 性能优化
1. 使用 SSD 硬盘
2. 分配足够的内存给 MySQL
3. 使用生产环境启动脚本
4. 考虑使用缓存（Redis）

## 安全建议

1. 修改默认登录密码
2. 使用强密码策略
3. 配置防火墙规则
4. 定期备份数据库
5. 保持系统和依赖更新

## 支持

如有问题，请检查：
1. Python 版本是否正确
2. MySQL 服务是否运行
3. 防火墙设置
4. 日志错误信息

更多技术支持，请查看项目文档或联系开发团队。
