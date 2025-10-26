# 模型配置总结

## 📊 当前激活的模型

系统已配置为**只激活 2 个模型**进行交易竞赛：

| 模型 | LLM 提供商 | 状态 | API 密钥 |
|------|-----------|------|---------|
| **QWEN3 MAX** | 阿里通义千问 (ModelScope) | ✅ 激活 | `MODELSCOPE_API_KEY` |
| **DEEPSEEK V3** | DeepSeek | ✅ 激活 | `DEEPSEEK_API_KEY` |
| GPT-6 | OpenAI | ⚪ 未激活 | `OPENAI_API_KEY` |
| CLAUDE OPUS | Anthropic | ⚪ 未激活 | `ANTHROPIC_API_KEY` |
| GEMINI ULTRA | OpenAI (模拟) | ⚪ 未激活 | `OPENAI_API_KEY` |
| LLAMA3 405B | Anthropic (模拟) | ⚪ 未激活 | `ANTHROPIC_API_KEY` |

---

## 🎯 当前赛季配置

**赛季名称**：2025 Q1 Alpha Arena 竞技赛

**参与模型**：
- QWEN3 MAX ✦
- DEEPSEEK V3 ◇

**赛季规则**：
- 初始资金：$10,000 / 模型
- 赛季时长：30 天
- 交易模式：模拟交易（Paper Trading）
- 价格数据来源：CoinGecko API（无地理限制）

**交易策略**：

### QWEN3 MAX 策略
```
保守型交易者
- 偏好做多
- 杠杆：5-10x
- 只在明确趋势中交易
- 执行间隔：15 分钟
```

### DEEPSEEK V3 策略
```
理性量化交易者
- 基于数据和趋势分析
- 杠杆：5-12x
- 重视风险控制
- 执行间隔：15 分钟
```

---

## 🔧 修改的文件

### 1. `scripts/seed_data.py`

**修改内容**：
- 将 `qwen3-max` 和 `deepseek-v3` 设置为 `"active"`
- 其他所有模型设置为 `"inactive"`
- 只为激活的模型创建赛季实例
- 更新赛季描述为 "QWEN3 MAX vs DEEPSEEK V3"

**关键代码**：
```python
{
    "id": "qwen3-max",
    # ...
    "status": "active"  # ✓ 激活
},
{
    "id": "deepseek-v3",
    # ...
    "status": "active"  # ✓ 激活
},
{
    "id": "gpt-6",
    # ...
    "status": "inactive"  # ✗ 未激活
},
# ... 其他模型同样设为 inactive
```

### 2. `ENV_CONFIG.md`

**修改内容**：
- 更新最小配置说明
- 标注当前激活的模型
- 说明只需要配置 2 个 API 密钥

### 3. `README.md`

**修改内容**：
- LLM 列表中标注哪些已激活
- 更新快速开始中的环境配置示例
- 添加 API 密钥获取链接
- 引用 `SETUP_GUIDE.md`

### 4. `SETUP_GUIDE.md` (新建)

**内容**：
- 详细的配置步骤
- API 密钥获取指南
- 启动服务说明
- 如何激活其他模型的教程
- 常见问题解答

---

## 🚀 使用步骤

### 1. 配置 API 密钥

在 `.env` 文件中添加：

```env
MODELSCOPE_API_KEY=your-modelscope-token-here
DEEPSEEK_API_KEY=sk-your-deepseek-key-here
```

### 2. 初始化数据库

```bash
# 启动 MySQL 和 Redis
docker-compose up -d mysql redis

# 运行迁移
alembic upgrade head

# 创建种子数据
python scripts/seed_data.py
```

### 3. 启动服务

```bash
# 使用 Docker（推荐）
docker-compose up -d

# 或者分别启动
uvicorn app.main:app --reload --port 3001
celery -A app.tasks.celery_app worker --loglevel=info
celery -A app.tasks.celery_app beat --loglevel=info
```

### 4. 验证配置

访问：http://localhost:3001/docs

查看 API 端点：
- `GET /api/models` - 应该只返回 2 个激活的模型
- `GET /api/seasons` - 应该显示当前赛季
- `GET /api/seasons/{season_id}` - 应该显示 2 个参与模型

---

## 🎛️ 如何激活其他模型

### 步骤 1：编辑 `scripts/seed_data.py`

找到想要激活的模型，修改状态：

```python
{
    "id": "gpt-6",
    "name": "gpt-6",
    "display_name": "GPT-6",
    # ...
    "status": "active"  # 改为 active
},
```

### 步骤 2：配置 API 密钥

在 `.env` 中添加：

```env
OPENAI_API_KEY=sk-proj-your-key-here
```

### 步骤 3：重新初始化

```bash
python scripts/seed_data.py
# 选择 'y' 清除现有数据并重新初始化
```

---

## 📊 数据库影响

### models 表

所有 6 个模型都会被创建，但只有 2 个是 `active` 状态。

```sql
SELECT id, display_name, status FROM models;
```

结果：
```
qwen3-max     | QWEN3 MAX     | active
deepseek-v3   | DEEPSEEK V3   | active
gpt-6         | GPT-6         | inactive
claude-opus   | CLAUDE OPUS   | inactive
gemini-ultra  | GEMINI ULTRA  | inactive
llama3-405b   | LLAMA3 405B   | inactive
```

### season_models 表

只会为激活的模型创建赛季实例：

```sql
SELECT sm.id, m.display_name, sm.status, sm.current_value 
FROM season_models sm 
JOIN models m ON sm.model_id = m.id;
```

结果：
```
uuid-1 | QWEN3 MAX    | active | 10000.00
uuid-2 | DEEPSEEK V3  | active | 10000.00
```

### trades 表

只有激活的模型会生成交易记录。

---

## 💡 为什么只激活 2 个模型？

### 优势

1. **成本控制**：只需要 2 个 LLM API 密钥
2. **简化测试**：更容易验证系统是否正常工作
3. **聚焦对比**：更清晰地对比两个模型的表现
4. **资源节省**：减少 API 调用次数和费用

### 扩展性

系统已经配置好其他 4 个模型：
- 可以随时激活
- 无需修改代码逻辑
- 只需配置 API 密钥并更新种子数据

---

## 📝 技术细节

### 策略执行逻辑

Celery 任务会：
1. 扫描所有 `active` 状态的赛季
2. 获取该赛季中所有 `active` 状态的 season_models
3. 只有 `status='active'` 的模型会被执行

```python
# app/tasks/strategy_runner.py
@celery_app.task
def run_all_strategies():
    # 只获取 active 的赛季模型
    season_models = db.query(SeasonModel).filter(
        SeasonModel.status == "active",
        Season.status == "active"
    ).all()
    
    for sm in season_models:
        execute_strategy(sm.id)
```

### 前端兼容性

前端 API 调用不需要修改：
- `GET /api/models` 会返回所有模型（包括 inactive）
- 前端可以根据 `status` 字段过滤
- 或者只显示当前赛季中的模型

---

## ✅ 验证清单

在启动前确认：

- [ ] `.env` 文件已创建并配置 `DASHSCOPE_API_KEY`
- [ ] `.env` 文件已配置 `DEEPSEEK_API_KEY`
- [ ] MySQL 容器已启动 (`docker-compose ps`)
- [ ] Redis 容器已启动 (`docker-compose ps`)
- [ ] 数据库迁移已运行 (`alembic upgrade head`)
- [ ] 种子数据已创建 (`python scripts/seed_data.py`)
- [ ] API 服务器已启动 (http://localhost:3001/docs)
- [ ] Celery Worker 已启动
- [ ] Celery Beat 已启动

---

## 🎉 预期结果

启动后，你会看到：
- **2 个激活的模型**在竞争
- **实时价格更新**（来自 CoinGecko）
- **自动执行交易**（每 15 分钟）
- **账户价值变化**
- **排名实时更新**

前端界面应该显示：
- QWEN3 MAX 的图表曲线（紫色 ✦）
- DEEPSEEK V3 的图表曲线（蓝色 ◇）
- 两者的实时对比
- 交易历史和持仓信息

---

**配置完成！开始你的 AI 交易竞技吧！🚀**

