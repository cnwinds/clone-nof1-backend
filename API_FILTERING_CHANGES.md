# API 过滤功能说明

## 📋 变更概述

**目标**：不参与交易的模型（`status != "active"`）不通过 API 返回给前端。

**影响**：前端只会看到当前激活的模型，简化界面显示。

---

## 🔄 API 变更详情

### 1. `/api/models` - 获取模型列表

**变更前**：返回所有模型（包括未激活的）

**变更后**：只返回激活的模型（`status = "active"`）

```json
// 变更前：返回 6 个模型
{
  "success": true,
  "data": [
    {"id": "qwen3-max", "display_name": "QWEN3 MAX", "status": "active"},
    {"id": "deepseek-v3", "display_name": "DEEPSEEK V3", "status": "active"},
    {"id": "gpt-6", "display_name": "GPT-6", "status": "inactive"},
    {"id": "claude-opus", "display_name": "CLAUDE OPUS", "status": "inactive"},
    {"id": "gemini-ultra", "display_name": "GEMINI ULTRA", "status": "inactive"},
    {"id": "llama3-405b", "display_name": "LLAMA3 405B", "status": "inactive"}
  ]
}

// 变更后：只返回 2 个激活的模型
{
  "success": true,
  "data": [
    {"id": "qwen3-max", "display_name": "QWEN3 MAX", "status": "active"},
    {"id": "deepseek-v3", "display_name": "DEEPSEEK V3", "status": "active"}
  ]
}
```

### 2. `/api/models/all` - 获取所有模型（新增）

**用途**：管理员接口，查看所有模型（包括未激活的）

```json
{
  "success": true,
  "data": [
    {"id": "qwen3-max", "display_name": "QWEN3 MAX", "status": "active"},
    {"id": "deepseek-v3", "display_name": "DEEPSEEK V3", "status": "active"},
    {"id": "gpt-6", "display_name": "GPT-6", "status": "inactive"},
    {"id": "claude-opus", "display_name": "CLAUDE OPUS", "status": "inactive"},
    {"id": "gemini-ultra", "display_name": "GEMINI ULTRA", "status": "inactive"},
    {"id": "llama3-405b", "display_name": "LLAMA3 405B", "status": "inactive"}
  ]
}
```

### 3. `/api/seasons/{season_id}` - 赛季详情

**变更**：赛季排名中只显示激活的模型

```json
{
  "success": true,
  "data": {
    "id": "season-uuid",
    "name": "2025 Q1 Alpha Arena 竞技赛",
    "models": [
      {
        "id": "sm-uuid-1",
        "model_id": "qwen3-max",
        "display_name": "QWEN3 MAX",
        "current_value": 10000.0,
        "performance": 0.0,
        "rank": 1
      },
      {
        "id": "sm-uuid-2", 
        "model_id": "deepseek-v3",
        "display_name": "DEEPSEEK V3",
        "current_value": 10000.0,
        "performance": 0.0,
        "rank": 2
      }
    ]
  }
}
```

---

## 📂 修改的文件

### 1. `app/services/model_service.py`

**新增方法**：
```python
@staticmethod
def get_active_models(db: Session) -> List[AIModel]:
    """获取激活的模型（参与交易的模型）"""
    return db.query(AIModel).filter(AIModel.status == "active").all()
```

### 2. `app/api/v1/models.py`

**修改**：
- `GET /api/models` - 使用 `get_active_models()` 替代 `get_all_models()`
- `GET /api/models/all` - 新增管理员接口，使用 `get_all_models()`

### 3. `app/api/v1/seasons.py`

**修改**：
- `GET /api/seasons/{season_id}` - 赛季详情中只显示激活的模型

---

## 🧪 测试验证

### 运行测试脚本

```bash
python scripts/test_api_filtering.py
```

### 手动测试

```bash
# 1. 测试激活模型列表
curl http://localhost:3001/api/models

# 2. 测试所有模型列表（管理员）
curl http://localhost:3001/api/models/all

# 3. 测试赛季详情
curl http://localhost:3001/api/seasons
# 获取赛季 ID，然后：
curl http://localhost:3001/api/seasons/{season_id}
```

### 预期结果

- ✅ `/api/models` 只返回 2 个激活的模型
- ✅ `/api/models/all` 返回 6 个模型（包括未激活的）
- ✅ 赛季详情只显示激活模型的排名

---

## 🎯 前端影响

### 前端需要调整的地方

1. **模型选择器**：现在只会显示激活的模型
2. **排行榜**：只显示参与交易的模型
3. **图表显示**：只显示激活模型的曲线

### 前端代码示例

```javascript
// 获取激活的模型（用于交易界面）
const activeModels = await fetch('/api/models').then(r => r.json());

// 获取所有模型（用于管理界面）
const allModels = await fetch('/api/models/all').then(r => r.json());

// 渲染模型选择器（只显示激活的）
activeModels.data.forEach(model => {
  console.log(`${model.display_name} (${model.llm_provider})`);
});
```

---

## 🔧 管理功能

### 激活/停用模型

如果需要激活其他模型，可以通过以下方式：

#### 方式 1：直接修改数据库

```sql
-- 激活 GPT-6
UPDATE models SET status = 'active' WHERE id = 'gpt-6';

-- 停用某个模型
UPDATE models SET status = 'inactive' WHERE id = 'qwen3-max';
```

#### 方式 2：修改种子数据脚本

编辑 `scripts/seed_data.py`，修改模型状态：

```python
{
    "id": "gpt-6",
    # ...
    "status": "active"  # 改为 active
},
```

然后重新初始化：

```bash
python scripts/seed_data.py
```

#### 方式 3：添加管理 API（未来）

可以添加管理接口：

```python
@router.post("/models/{model_id}/activate")
async def activate_model(model_id: str, db: Session = Depends(get_db)):
    """激活模型"""
    # 实现激活逻辑

@router.post("/models/{model_id}/deactivate") 
async def deactivate_model(model_id: str, db: Session = Depends(get_db)):
    """停用模型"""
    # 实现停用逻辑
```

---

## 📊 当前配置

### 激活的模型

| 模型 | LLM 提供商 | 状态 | API 返回 |
|------|-----------|------|---------|
| QWEN3 MAX | ModelScope | ✅ active | ✅ 是 |
| DEEPSEEK V3 | DeepSeek | ✅ active | ✅ 是 |
| GPT-6 | OpenAI | ⚪ inactive | ❌ 否 |
| CLAUDE OPUS | Anthropic | ⚪ inactive | ❌ 否 |
| GEMINI ULTRA | OpenAI | ⚪ inactive | ❌ 否 |
| LLAMA3 405B | Anthropic | ⚪ inactive | ❌ 否 |

### API 端点对比

| 端点 | 返回内容 | 用途 |
|-----|---------|------|
| `GET /api/models` | 只返回激活模型 | 前端交易界面 |
| `GET /api/models/all` | 返回所有模型 | 管理界面 |
| `GET /api/seasons/{id}` | 只显示激活模型排名 | 赛季排行榜 |

---

## ✅ 验证清单

- [ ] `/api/models` 只返回 2 个激活的模型
- [ ] `/api/models/all` 返回 6 个模型
- [ ] 赛季详情只显示激活模型的排名
- [ ] 前端界面只显示激活的模型
- [ ] 管理界面可以查看所有模型
- [ ] 测试脚本通过

---

## 🎉 总结

**变更效果**：
- ✅ 前端界面更简洁（只显示参与交易的模型）
- ✅ 减少不必要的数据传输
- ✅ 保持管理功能的完整性
- ✅ 向后兼容（新增 `/all` 端点）

**使用建议**：
- 前端交易界面使用 `/api/models`
- 管理界面使用 `/api/models/all`
- 赛季排行榜自动过滤未激活模型

---

**变更完成！现在 API 只会返回参与交易的激活模型！** 🚀

