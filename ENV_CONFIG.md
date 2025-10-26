# 环境变量配置指南

## 创建 .env 文件

在项目根目录创建 `.env` 文件，包含以下内容：

```env
# ========================================
# 数据库配置
# ========================================
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/alpha_arena

# ========================================
# Redis 配置
# ========================================
REDIS_URL=redis://localhost:6379/0

# ========================================
# LLM API 密钥（至少配置一个）
# ========================================
# OpenAI GPT
OPENAI_API_KEY=sk-your-openai-key-here

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# 阿里通义千问 (ModelScope API)
MODELSCOPE_API_KEY=your-modelscope-api-key-here

# DeepSeek
DEEPSEEK_API_KEY=sk-your-deepseek-key-here

# ========================================
# 交易所 API 密钥（可选，模拟交易不需要）
# ========================================
BINANCE_API_KEY=
BINANCE_SECRET=
COINBASE_API_KEY=
COINBASE_SECRET=

# ========================================
# 应用配置
# ========================================
ENV=development
API_PORT=3001
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
LOG_LEVEL=INFO

# ========================================
# 赛季配置
# ========================================
DEFAULT_INITIAL_CAPITAL=10000.0
```

## 最小配置（用于测试）

**当前激活的模型**：QWEN3 MAX 和 DEEPSEEK V3

只需要配置这 4 项即可启动：

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/alpha_arena
REDIS_URL=redis://localhost:6379/0
MODELSCOPE_API_KEY=your-modelscope-token-here
DEEPSEEK_API_KEY=sk-your-deepseek-key-here
```

⚠️ **注意**：只有激活的模型需要配置 API 密钥。如需激活其他模型，请修改 `scripts/seed_data.py`。

## 获取 LLM API 密钥

### OpenAI
1. 访问：https://platform.openai.com/api-keys
2. 登录或注册账号
3. 创建新的 API 密钥
4. 复制密钥，格式：`sk-proj-...` 或 `sk-...`

### Anthropic Claude
1. 访问：https://console.anthropic.com/settings/keys
2. 登录或注册账号
3. 创建 API 密钥
4. 复制密钥，格式：`sk-ant-...`

### 阿里通义千问 (ModelScope)
1. 访问：https://www.modelscope.cn/my/myaccesstoken
2. 登录 ModelScope 账号（可使用 GitHub/微信/手机号）
3. 创建或查看 API Token
4. 复制 API Token
5. 文档：https://www.modelscope.cn/docs/model-service/API-Inference/intro

### DeepSeek
1. 访问：https://platform.deepseek.com/api_keys
2. 登录或注册账号
3. 创建 API 密钥
4. 复制密钥，格式：`sk-...`

## 配置说明

### 数据库

**本地开发**（使用本地 MySQL）：
```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/alpha_arena
```

**Docker**（使用 docker-compose 中的 MySQL）：
```env
DATABASE_URL=mysql+pymysql://root:password@mysql:3306/alpha_arena
```

### Redis

**本地开发**：
```env
REDIS_URL=redis://localhost:6379/0
```

**Docker**：
```env
REDIS_URL=redis://redis:6379/0
```

### 交易所 API

⚠️ **注意**：默认使用**模拟交易模式**，不需要配置交易所 API。

只有在切换到**真实交易模式**时才需要：
1. 在 Binance/Coinbase 注册账号
2. 创建 API 密钥（需要交易权限）
3. 配置到 .env 文件

## 创建步骤

### 方式 1：手动创建

```bash
# 1. 在项目根目录创建 .env 文件
notepad .env

# 2. 复制上面的配置内容，填入实际值

# 3. 保存文件
```

### 方式 2：命令行创建

```bash
# Windows PowerShell
@"
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/alpha_arena
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=
DASHSCOPE_API_KEY=
ENV=development
API_PORT=3001
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
DEFAULT_INITIAL_CAPITAL=10000.0
"@ | Out-File -FilePath .env -Encoding utf8
```

```bash
# Linux/Mac
cat > .env << EOF
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/alpha_arena
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=
DASHSCOPE_API_KEY=
ENV=development
API_PORT=3001
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
DEFAULT_INITIAL_CAPITAL=10000.0
EOF
```

## 验证配置

创建好 `.env` 文件后，运行测试：

```bash
python scripts/test_coingecko.py
```

如果看到：
```
🎉 测试通过！CoinGecko API 工作正常
```

说明配置正确！

## 常见问题

### Q: 没有 LLM API 密钥怎么办？

**A**: 需要至少一个 LLM API 密钥才能运行策略。建议：
1. 注册 OpenAI 账号（最常用）
2. 或者注册阿里通义千问（国内访问快）

### Q: 如何修改数据库密码？

**A**: 修改 `docker-compose.yml` 中的 `MYSQL_ROOT_PASSWORD` 和 `.env` 中的 `DATABASE_URL`。

### Q: 可以不配置交易所 API 吗？

**A**: 可以！默认使用**模拟交易模式**，只需要 CoinGecko 的公开数据（无需密钥）。

### Q: .env 文件会被提交到 Git 吗？

**A**: 不会！`.gitignore` 已经配置忽略 `.env` 文件。

## 安全提示

⚠️ **重要**：
- ✅ 不要将 `.env` 文件提交到 Git
- ✅ 不要在公开场合分享 API 密钥
- ✅ 定期更换 API 密钥
- ✅ 使用只读权限的 API 密钥（如果只需要读取数据）
- ✅ 生产环境使用环境变量而非 .env 文件

## 下一步

配置好 `.env` 文件后：

1. 启动数据库：`docker-compose up -d mysql redis`
2. 初始化数据库：`alembic upgrade head`
3. 创建种子数据：`python scripts/seed_data.py`
4. 启动服务：`uvicorn app.main:app --reload --port 3001`

---

**需要帮助？** 查看 [README.md](README.md) 或 [QUICKSTART.md](QUICKSTART.md)

