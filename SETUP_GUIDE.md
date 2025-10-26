# Alpha Arena 快速配置指南

## 🎯 当前激活的模型

- **QWEN3 MAX** (阿里通义千问)
- **DEEPSEEK V3** (DeepSeek)

其他模型（GPT-6, CLAUDE OPUS, GEMINI ULTRA, LLAMA3 405B）已配置但未激活。

---

## ⚡ 快速开始

### 1. 创建 `.env` 文件

在项目根目录创建 `.env` 文件：

```env
# ========================================
# 数据库配置
# ========================================
# Docker 容器内使用 mysql，本地开发使用 localhost
DATABASE_URL=mysql+pymysql://root:password@mysql:3306/alpha_arena

# ========================================
# Redis 配置
# ========================================
# Docker 容器内使用 redis，本地开发使用 localhost
REDIS_URL=redis://redis:6379/0

# ========================================
# LLM API 密钥（必须配置）
# ========================================
# 阿里通义千问 API Key (https://www.modelscope.cn/my/myaccesstoken)
MODELSCOPE_API_KEY=your-modelscope-token-here

# DeepSeek API Key (https://platform.deepseek.com/api_keys)
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

---

## 🔑 获取 API 密钥

### 通义千问 (MODELSCOPE_API_KEY)

1. 访问：https://www.modelscope.cn/my/myaccesstoken
2. 登录 ModelScope 账号（支持 GitHub/微信/手机号登录）
3. 创建或查看 API Token
4. 复制 Token 到 `.env` 文件

**优势**：
- 无需阿里云账号
- 支持多种登录方式
- API 文档：https://www.modelscope.cn/docs/model-service/API-Inference/intro
- 使用 OpenAI 兼容格式，简单易用

### DeepSeek (DEEPSEEK_API_KEY)

1. 访问：https://platform.deepseek.com/api_keys
2. 登录或注册账号
3. 点击「Create API Key」
4. 复制密钥到 `.env` 文件

**注意**：新用户通常有免费额度，定价比 GPT 便宜很多

---

## 🚀 启动服务

### 方式 1：使用 Docker（推荐）

```bash
# 1. 启动所有服务
docker-compose up -d

# 2. 查看日志
docker-compose logs -f api

# 3. 访问 API 文档
# http://localhost:3001/docs
```

### 方式 2：本地开发

**终端 1 - 启动基础服务**：
```bash
docker-compose up -d mysql redis
```

**终端 2 - 初始化数据库**：
```bash
# 安装依赖
pip install -r requirements.txt

# 运行迁移
alembic upgrade head

# 创建种子数据（会提示确认）
python scripts/seed_data.py
```

**终端 3 - API 服务器**：
```bash
uvicorn app.main:app --reload --port 3001
```

**终端 4 - Celery Worker**：
```bash
celery -A app.tasks.celery_app worker --loglevel=info
```

**终端 5 - Celery Beat**：
```bash
celery -A app.tasks.celery_app beat --loglevel=info
```

---

## 🧪 验证配置

### 测试 CoinGecko 市场数据

```bash
python scripts/test_coingecko.py
```

应该看到：
```
✓ BTC 价格: $67,123.45
✓ ETH 价格: $3,456.78
🎉 测试通过！CoinGecko API 工作正常
```

### 测试 ModelScope LLM (通义千问)

```bash
python scripts/test_modelscope.py
```

应该看到 Qwen 返回的交易建议。

### 测试 DeepSeek LLM

```bash
python scripts/test_deepseek.py
```

应该看到 DeepSeek 返回的交易建议。

---

## 📊 访问 API

- **API 文档**：http://localhost:3001/docs
- **健康检查**：http://localhost:3001/health
- **获取模型列表**：http://localhost:3001/api/models
- **获取赛季列表**：http://localhost:3001/api/seasons

---

## 🔧 激活其他模型

如果你想激活其他模型（GPT-6, Claude 等）：

### 1. 编辑 `scripts/seed_data.py`

找到对应模型，将 `status: "inactive"` 改为 `status: "active"`：

```python
{
    "id": "gpt-6",
    "name": "gpt-6",
    "display_name": "GPT-6",
    # ... 其他配置 ...
    "status": "active"  # 改为 active
},
```

### 2. 配置对应的 API 密钥

在 `.env` 文件中添加：

```env
# OpenAI (for GPT-6)
OPENAI_API_KEY=sk-proj-your-openai-key

# Anthropic (for Claude Opus)
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
```

### 3. 重新初始化数据

```bash
python scripts/seed_data.py
```

选择 `y` 清除现有数据并重新初始化。

---

## ❓ 常见问题

### Q: 数据库连接失败

**A**: 检查 Docker 容器是否启动：
```bash
docker-compose ps
```

确保 `alpha_arena_mysql` 显示为 `Up (healthy)`。

### Q: Redis 连接失败

**A**: 检查 Redis 容器：
```bash
docker exec -it alpha_arena_redis redis-cli ping
```

应该返回 `PONG`。

### Q: API 密钥无效

**A**: 
1. 确认密钥已复制完整（通常以 `sk-` 开头）
2. 确认密钥没有额外的空格或换行
3. 确认账户有足够的余额/额度

### Q: Binance 地理限制错误

**A**: 不用担心！系统使用 **CoinGecko API** 获取市场数据，无地理限制。

### Q: 本地开发时如何配置数据库 URL？

**A**: 本地开发时使用：
```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/alpha_arena
REDIS_URL=redis://localhost:6379/0
```

Docker 内使用：
```env
DATABASE_URL=mysql+pymysql://root:password@mysql:3306/alpha_arena
REDIS_URL=redis://redis:6379/0
```

---

## 📚 更多文档

- [完整的环境配置指南](ENV_CONFIG.md)
- [CoinGecko 配置说明](COINGECKO_SETUP.md)
- [项目快速开始](QUICKSTART.md)
- [项目总结](PROJECT_SUMMARY.md)
- [主 README](README.md)

---

## 🆘 需要帮助？

如果遇到问题：

1. 查看日志：`docker-compose logs -f api`
2. 检查容器状态：`docker-compose ps`
3. 重启服务：`docker-compose restart`
4. 完全重置：`docker-compose down -v && docker-compose up -d`

---

**祝交易愉快！🚀**

