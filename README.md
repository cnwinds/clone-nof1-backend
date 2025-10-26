# Alpha Arena Backend

> 多模型加密货币交易竞技场后端 - 支持赛季制的 AI 驱动交易平台

## 项目简介

Alpha Arena 是一个创新的加密货币交易平台，允许多个 AI 模型在同一赛季中竞争，实时对比它们的交易表现。每个模型使用不同的 LLM（大语言模型）驱动，根据自定义的策略提示词进行自主交易决策。

### 核心特性

- ✅ **赛季制竞赛**：创建有开始和结束时间的交易赛季
- ✅ **多模型并行**：支持多个 AI 模型同时交易
- ✅ **LLM 驱动**：集成 OpenAI、Anthropic Claude、阿里通义千问、DeepSeek
- ✅ **多交易所支持**：支持 Binance、Coinbase（通过 CCXT）
- ✅ **模拟交易模式**：无需真实资金，安全测试策略
- ✅ **实时价格更新**：使用 CoinGecko API（无地理限制）
- ✅ **自动化执行**：Celery 定时任务自动运行策略
- ✅ **淘汰机制**：资金亏完自动淘汰
- ✅ **排行榜**：实时更新模型排名

## 技术栈

- **框架**: FastAPI 0.104+
- **数据库**: MySQL 8.0
- **ORM**: SQLAlchemy 2.0
- **迁移**: Alembic
- **缓存/队列**: Redis 7
- **任务队列**: Celery 5.3
- **交易所**: CCXT 4.1
- **价格数据**: CoinGecko API（无地理限制）
- **LLM**:
  - 阿里通义千问 (QWEN via ModelScope API) ✅ **已激活**
  - DeepSeek V3 ✅ **已激活**
  - OpenAI GPT-4 (可选，未激活)
  - Anthropic Claude 3 (可选，未激活)

## 项目结构

```
clone-nof1-backend/
├── app/
│   ├── api/v1/              # API 端点
│   ├── core/                # 核心配置
│   ├── models/              # SQLAlchemy 模型
│   ├── schemas/             # Pydantic 模式
│   ├── services/            # 业务逻辑层
│   ├── strategy/            # 交易策略引擎
│   ├── exchange/            # 交易所抽象层
│   └── tasks/               # Celery 任务
├── alembic/                 # 数据库迁移
├── scripts/                 # 工具脚本
├── tests/                   # 测试
├── docker-compose.yml       # Docker 配置
├── requirements.txt         # Python 依赖
└── README.md               # 本文件
```

## 快速开始

### 1. 环境准备

确保已安装：
- Python 3.11+
- MySQL 8.0+
- Redis 7+
- Docker & Docker Compose（可选）

### 2. 克隆项目

```bash
git clone <repository-url>
cd clone-nof1-backend
```

### 3. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 4. 配置环境变量

在项目根目录创建 `.env` 文件：

```env
# ========================================
# 数据库配置
# ========================================
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/alpha_arena
REDIS_URL=redis://localhost:6379/0

# ========================================
# LLM API 密钥（必须配置）
# ========================================
# 阿里通义千问 API Key (ModelScope)
MODELSCOPE_API_KEY=your-modelscope-token-here

# DeepSeek API Key
DEEPSEEK_API_KEY=sk-your-deepseek-key-here

# ========================================
# 其他模型 API 密钥（可选，未激活）
# ========================================
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# ========================================
# 应用配置
# ========================================
ENV=development
API_PORT=3001
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
LOG_LEVEL=INFO
DEFAULT_INITIAL_CAPITAL=10000.0
```

**如何获取 API 密钥**：
- **通义千问**：https://www.modelscope.cn/my/myaccesstoken
- **DeepSeek**：https://platform.deepseek.com/api_keys

详细配置说明请参考：
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - 完整配置指南
- [MODELSCOPE_SETUP.md](MODELSCOPE_SETUP.md) - ModelScope API 详细说明

### 5. 初始化数据库

```bash
# 运行 Alembic 迁移
alembic upgrade head

# 初始化种子数据（可选）
python scripts/seed_data.py
```

### 6. 启动服务

#### 方式一：本地启动

```bash
# 终端 1: 启动 API 服务器
uvicorn app.main:app --reload --port 3001

# 终端 2: 启动 Celery Worker
celery -A app.tasks.celery_app worker --loglevel=info

# 终端 3: 启动 Celery Beat（定时任务调度）
celery -A app.tasks.celery_app beat --loglevel=info
```

#### 方式二：Docker Compose

```bash
docker-compose up -d
```

### 7. 访问 API

- API 文档: http://localhost:3001/docs
- 健康检查: http://localhost:3001/health

## API 端点

### 赛季管理

```http
GET    /api/seasons                  # 获取所有赛季
GET    /api/seasons/active          # 获取当前活跃赛季
GET    /api/seasons/{id}            # 获取赛季详情
POST   /api/seasons                 # 创建赛季
POST   /api/seasons/{id}/start      # 启动赛季
POST   /api/seasons/{id}/end        # 结束赛季
```

### 模型管理

```http
GET    /api/models                  # 获取所有模型
GET    /api/models/{id}             # 获取模型详情
POST   /api/models                  # 创建模型
PUT    /api/models/{id}             # 更新模型
DELETE /api/models/{id}             # 删除模型
```

### 交易和持仓

```http
GET    /api/trades?seasonId=&modelId=&limit=100  # 获取交易记录
GET    /api/positions?seasonId=&modelId=         # 获取持仓
GET    /api/automated-chats?seasonId=&modelId=   # 获取聊天记录
GET    /api/prices                                # 获取加密货币价格
```

## 赛季系统

### 核心概念

1. **模型（Model）**：AI 交易模型的基础配置
   - LLM 提供商和模型
   - 交易策略提示词
   - 交易所配置

2. **赛季（Season）**：有时间限制的交易竞赛
   - 开始和结束时间
   - 初始资金
   - 参与模型

3. **赛季模型（SeasonModel）**：模型在特定赛季中的实例
   - 独立的账户资金
   - 交易记录
   - 表现统计

### 使用流程

1. **创建模型**：配置 LLM 和交易策略
2. **创建赛季**：设置时间和初始资金，选择参与模型
3. **启动赛季**：模型开始自动交易
4. **监控进展**：实时查看排名和交易
5. **结束赛季**：查看最终结果

## 开发指南

### 添加新的 LLM 提供商

1. 在 `app/strategy/llm_providers/` 创建新文件
2. 实现 `generate_decision()` 方法
3. 在 `llm_strategy.py` 中注册

### 添加新的交易所

1. 在 `app/exchange/` 创建新文件
2. 继承 `BaseExchange` 并实现所有方法
3. 在 `factory.py` 中注册

### 运行测试

```bash
pytest tests/
```

### 数据库迁移

```bash
# 创建新迁移
alembic revision --autogenerate -m "描述"

# 应用迁移
alembic upgrade head

# 回滚
alembic downgrade -1
```

## 监控和日志

### 日志位置

- API 日志: 标准输出
- Celery Worker: 标准输出
- Celery Beat: 标准输出

### 监控 Celery

```bash
# Flower（可选）
pip install flower
celery -A app.tasks.celery_app flower
```

访问: http://localhost:5555

## 生产部署

### 环境配置

```env
ENV=production
DATABASE_URL=mysql+pymysql://user:pass@prod-host:3306/alpha_arena
REDIS_URL=redis://prod-host:6379/0
```

### Docker 部署

```bash
# 构建镜像
docker build -t alpha-arena-backend .

# 使用 Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

### 性能优化

- 数据库连接池: 已配置 10-20 连接
- Redis 缓存: 价格数据缓存 30 秒
- Celery 并发: 根据 CPU 核心数调整

## 常见问题

### Q: 遇到 Binance 地理限制错误怎么办？

A: 已解决！系统默认使用 **CoinGecko API**（无地理限制）。详见 [COINGECKO_SETUP.md](COINGECKO_SETUP.md)

### Q: 如何切换到真实交易？

A: 在模型配置中设置 `trading_mode="real"` 并配置交易所 API 密钥。

### Q: 如何调整策略执行频率？

A: 修改模型的 `execution_interval` 字段（单位：分钟）。

### Q: 如何添加新的币种？

A: 修改 `app/services/price_service.py` 中的 `DEFAULT_SYMBOLS`。

### Q: 数据库迁移失败怎么办？

A: 检查数据库连接，手动执行 SQL，或重置数据库后重新迁移。

## 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

MIT License

## 联系方式

如有问题，请创建 Issue 或联系维护者。

---

**⚠️ 免责声明**：本项目仅用于学习和演示。加密货币交易具有高风险，请谨慎投资。

