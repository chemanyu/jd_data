# 数据归因分析系统

这是一个用于展示数据归因分析的Web应用系统，提供统一的数据查询、展示和管理功能。

## 🌟 功能特性

- **用户登录鉴权**: 安全的用户认证系统
- **集成数据查询**: 在仪表盘直接进行数据查询，无需页面跳转
- **可折叠展示**: 采用手风琴式面板展示不同数据模块
- **账户搜索**: 支持按账户ID过滤查询结果
- **响应式设计**: 适配桌面和移动设备
- **实时数据**: 调用外部API获取最新归因数据

## 📊 数据展示模块

### 汇总统计
- 总请求数统计
- 错误数量统计  
- 成功率计算

### 详细分析
- **账户请求统计**: 各账户请求量分布和占比
- **错误类型统计**: 不同错误类型的发生频率
- **账户错误详情**: 每个账户的具体错误明细

## 🚀 安装和运行

### 环境要求
- Python 3.8+
- MySQL 5.7+
- 现代浏览器

### 安装步骤

1. **克隆项目并进入目录**:
```bash
cd /Users/chemanyu/workspace/python/jd_data
```

2. **安装依赖包**:
```bash
pip install -r requirements.txt
```

3. **配置数据库**:
- 确保MySQL数据库服务正在运行
- 创建数据库 `release_atd`
- 修改 `app/database.py` 中的数据库配置

4. **运行应用**:
```bash
python run.py
```

5. **访问应用**:
打开浏览器访问 `http://localhost:5001`

## 📁 项目结构

```
jd_data/
├── app/
│   ├── __init__.py              # 应用初始化
│   ├── models.py                # 数据模型
│   ├── routes.py                # 路由处理
│   ├── database.py              # 数据库配置
│   ├── api_client.py            # API客户端
│   ├── templates/               # HTML模板
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html       # 主仪表盘
│   │   ├── query.html
│   │   ├── query_result.html
│   │   ├── history.html
│   │   └── profile.html
│   └── static/                  # 静态资源
│       ├── css/style.css
│       └── js/main.js
├── requirements.txt             # 依赖包列表
├── run.py                      # 应用启动文件
├── test_setup.py               # 环境测试脚本
├── README.md                   # 项目说明
└── FEATURES.md                 # 功能详情说明
```

## 🎯 使用指南

### 登录系统
- **默认账号**: `admin`
- **默认密码**: `admin123`

### 数据查询
1. 在仪表盘选择查询日期（默认为昨天）
2. 可选：输入账户ID进行过滤搜索
3. 点击"查询"按钮获取数据
4. 查看可折叠的统计结果

### 功能操作
- **折叠面板**: 点击面板标题展开/收起详细信息
- **搜索过滤**: 账户ID支持部分匹配搜索
- **历史记录**: 通过快速访问链接查看查询历史
- **用户管理**: 通过导航栏访问个人资料

## 🔧 API接口

### 外部数据源
- **接口地址**: `http://ad-ocpx.zhltech.net/attribution/data`
- **参数**: `date` (格式: YYYYMMDD)
- **返回**: JSON格式的归因数据

### 内部API
- **GET** `/api/data?date=YYYYMMDD` - 获取格式化的归因数据

## 🛠 错误类型说明

| 字段名 | 字段意义 |
|--------|----------|
| `channer_not_found` | 链接异常 |
| `cid_callback_error` | 归因异常 |
| `cid_callback_empty` | 归因字段为空 |
| `parse_callback_raw_error` | 数据解析异常 |
| `p1_missing` | 平台异常 |
| `send_track_flag_false` | 回传字段判断不通过 |
| `advertiser_rate_false` | 扣量过滤 |

## 🔍 测试和调试

### 环境测试
运行测试脚本检查环境配置：
```bash
python test_setup.py
```

### 调试模式
应用默认以调试模式运行，支持：
- 代码热重载
- 详细错误信息
- 调试工具栏

## 📈 性能优化

- 异步数据加载
- 前端数据缓存
- 响应式布局
- 优化的SQL查询

## 🔒 安全考虑

- 用户密码哈希存储
- Session管理
- CSRF保护
- 输入数据验证

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

本项目仅供学习和开发使用。

---

**版本**: 1.0.0  
**最后更新**: 2025年8月20日  
**技术栈**: Flask + MySQL + Bootstrap + JavaScript
# jd_data
