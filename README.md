# 832401218 Calculator Backend

前后端分离计算器系统的**后端**部分，基于 Flask + SQLite 实现。
负责表达式解析与计算、计算历史的持久化存储，对外提供 HTTP/JSON API。

## 技术栈

| 组件 | 技术 |
| --- | --- |
| 语言 | Python 3.10+ |
| Web 框架 | Flask 3.x |
| 数据库 | SQLite（标准库 sqlite3，无需额外安装） |
| 表达式解析 | 手写 tokenizer + 递归下降解析器（不使用 eval/exec） |

## 运行环境

- Python 3.10 或更高版本
- 无其他系统依赖（SQLite 为 Python 内置）

## 安装与启动

```bash
# 1. 创建并激活虚拟环境（可选但推荐）
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务（默认 0.0.0.0:5000）
python run.py
```

服务启动后可通过 `GET http://localhost:5000/api/health` 检查运行状态。

## 数据库初始化

无需手动初始化：服务首次启动时会自动在项目根目录创建 `calculator.db`
并建表。表结构如下：

```sql
CREATE TABLE calculation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expression TEXT NOT NULL,   -- 计算表达式，如 (1+2)*3
    result TEXT NOT NULL,       -- 计算结果，如 9
    created_at TEXT NOT NULL    -- 计算时间，如 2026-10-03 19:33:55
);
```

如需重置数据，直接删除 `calculator.db` 文件后重启服务即可。

## API 一览

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/health` | 健康检查 |
| POST | `/api/calculate` | 计算表达式并写入历史 |
| GET | `/api/history` | 查询全部计算历史（按 id 倒序） |
| DELETE | `/api/history/{id}` | 删除指定历史记录 |
| DELETE | `/api/history` | 清空全部历史记录（扩展功能） |

### 计算请求示例

请求：`POST /api/calculate`

```json
{ "expression": "(1+2)*3" }
```

成功响应（HTTP 200）：

```json
{ "success": true, "expression": "(1+2)*3", "result": "9", "id": 1, "created_at": "2026-10-03 19:33:55" }
```

失败响应（HTTP 400，例如除零、非法表达式）：

```json
{ "success": false, "message": "Division by zero" }
```

## 前后端连接方式

- 服务默认监听 `0.0.0.0:5000`，已开启 CORS，允许任意前端跨域调用。
- 前端项目中的 API 地址配置项（`script.js` 中的 `API_BASE`）
  需指向本服务的 `/api` 前缀，例如 `http://localhost:5000/api`。
- 部署后只需将前端的 `API_BASE` 改为后端公网地址即可。

## 项目结构

```
832401218_calculator_backend/
├── run.py                     # 启动入口
├── requirements.txt
├── src/
│   ├── app.py                 # Flask 应用工厂（含 CORS 配置）
│   ├── controller/routes.py   # HTTP 路由层
│   ├── service/
│   │   ├── calculator_service.py  # 表达式 tokenizer + 递归下降解析器
│   │   └── history_service.py     # 计算与历史的业务逻辑
│   └── model/database.py      # SQLite 数据访问层
└── test_api.py                # API 冒烟测试（Flask test client）
```

## 测试

```bash
python test_api.py
```

覆盖：四则运算、复合表达式（优先级、括号、一元正负号、小数）、
非法表达式、除零、历史增删查、清空历史等场景。
