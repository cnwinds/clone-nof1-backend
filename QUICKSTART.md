# Alpha Arena 快速入门指南

> 5 分钟快速搭建并运行 Alpha Arena 后端

## 前置条件

- Python 3.11+
- MySQL 8.0（或使用 Docker）
- Redis（或使用 Docker）

## 方式一：本地开发（推荐）

### 1. 安装依赖

```bash
# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 启动数据库服务

```bash
# 使用 Docker 快速启动 MySQL 和 Redis
docker-compose up -d mysql redis

# 等待服务就绪（约 10 秒）
```

### 3. 配置环境变量

创建 `.env` 文件：

```bash
# 复制示例配置
cp .env.example .env
```

**最小配置（用于测试）**：

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/alpha_arena
REDIS_URL=redis://localhost:6379/0

# 至少配置一个 LLM API（用于策略执行）
OPENAI_API_KEY=sk-your-key-here
```

### 4. 初始化数据库

```bash
# 创建数据库表
alembic upgrade head

# 初始化演示数据
python scripts/seed_data.py
```

**输出示例**：
```
✓ 创建了 5 个演示模型
✓ 创建了赛季: 2025 Q1 Alpha Arena 竞技赛
✓ 初始化完成！
```

### 5. 启动服务

打开 **3 个终端窗口**：

**终端 1 - API 服务器**：
```bash
uvicorn app.main:app --reload --port 3001
```

**终端 2 - Celery Worker**：
```bash
celery -A app.tasks.celery_app worker --loglevel=info
```

**终端 3 - Celery Beat**（定时任务）：
```bash
celery -A app.tasks.celery_app beat --loglevel=info
```

### 6. 验证安装

```bash
# 运行测试脚本
python scripts/test_system.py
```

或访问：
- API 文档: http://localhost:3001/docs
- 健康检查: http://localhost:3001/health

---

## 方式二：Docker Compose（一键启动）

### 1. 配置环境变量

创建 `.env` 文件并配置 LLM API 密钥：

```env
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
DASHSCOPE_API_KEY=sk-your-key-here
```

### 2. 启动所有服务

```bash
docker-compose up -d
```

这将启动：
- MySQL 数据库
- Redis 缓存
- FastAPI 服务器
- Celery Worker
- Celery Beat

### 3. 初始化数据

```bash
# 等待服务启动（约 15 秒）
sleep 15

# 进入容器并初始化数据
docker-compose exec api python scripts/seed_data.py
```

### 4. 访问服务

- API: http://localhost:3001
- API 文档: http://localhost:3001/docs

---

## 基本使用

### 1. 获取赛季列表

```bash
curl http://localhost:3001/api/seasons
```

### 2. 查看模型

```bash
curl http://localhost:3001/api/models
```

### 3. 查看交易记录

```bash
curl http://localhost:3001/api/trades?limit=10
```

### 4. 手动触发策略执行

在 Python 中：

```python
import asyncio
from app.core.database import SessionLocal
from app.models import SeasonModel
from app.strategy.llm_strategy import LLMStrategy

db = SessionLocal()
season_model = db.query(SeasonModel).first()
strategy = LLMStrategy(db)
result = asyncio.run(strategy.execute(season_model.id))
print(result)
db.close()
```

---

## 常见问题

### Q: 端口 3001 已被占用

修改 `.env` 中的 `API_PORT=3002`，然后重启服务。

### Q: 数据库连接失败

检查 MySQL 是否运行：
```bash
docker-compose ps mysql
# 或本地：
mysql -u root -p
```

### Q: LLM API 调用失败

确保在 `.env` 中配置了正确的 API 密钥。可以先使用一个 LLM 提供商测试。

### Q: Celery 任务不执行

检查 Redis 是否运行：
```bash
docker-compose ps redis
# 或本地：
redis-cli ping
```

确保 Celery Beat 正在运行（负责定时任务调度）。

---

## 下一步

- 📖 阅读完整文档: [README.md](README.md)
- 📖 查看 API 文档: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- 🎯 创建自定义模型和策略
- 🎮 连接前端界面

---

## 停止服务

### 本地开发

在各终端按 `Ctrl+C` 停止服务。

### Docker

```bash
docker-compose down

# 删除数据（可选）
docker-compose down -v
```

---

**🎉 恭喜！你已经成功搭建了 Alpha Arena 后端！**

有问题？查看 [README.md](README.md) 或创建 Issue。

