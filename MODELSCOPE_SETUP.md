# ModelScope API 配置指南

## 📖 关于 ModelScope

[ModelScope](https://www.modelscope.cn/) 是阿里巴巴达摩院推出的开源模型社区，提供了通义千问系列模型的 API 服务。

**官方文档**：https://www.modelscope.cn/docs/model-service/API-Inference/intro

---

## ✨ 为什么使用 ModelScope API？

与阿里云 DashScope API 相比，ModelScope API 具有以下优势：

### 1. **更简单的认证**
- ✅ 无需阿里云账号
- ✅ 支持 GitHub/微信/手机号登录
- ✅ 一键获取 API Token

### 2. **OpenAI 兼容格式**
- ✅ 使用标准的 OpenAI SDK
- ✅ 无需额外安装 `dashscope` 包
- ✅ 代码更简洁，易于维护

### 3. **灵活的模型选择**
- ✅ 支持 `qwen-max`
- ✅ 支持 `qwen-plus`
- ✅ 支持 `qwen-turbo`
- ✅ 支持 `qwen2.5-72b-instruct`
- ✅ 更多开源模型

### 4. **更好的开发体验**
- ✅ 与 OpenAI/DeepSeek API 使用相同的代码模式
- ✅ 统一的错误处理
- ✅ 更好的文档和社区支持

---

## 🔑 获取 API Token

### 步骤 1：访问 ModelScope

打开浏览器，访问：https://www.modelscope.cn/my/myaccesstoken

### 步骤 2：登录账号

支持以下登录方式：
- **GitHub** 账号（推荐）
- **微信** 扫码登录
- **手机号** + 验证码

### 步骤 3：创建或查看 Token

1. 如果还没有 Token，点击「创建新的 API Token」
2. 输入 Token 名称（如：`alpha-arena-backend`）
3. 点击「创建」
4. **立即复制 Token**（只显示一次！）

### 步骤 4：保存到 `.env`

将 Token 保存到项目根目录的 `.env` 文件：

```env
MODELSCOPE_API_KEY=your-modelscope-token-here
```

⚠️ **重要**：Token 只在创建时显示一次，请妥善保管！

---

## 🚀 API 使用说明

### Base URL

```
https://api-inference.modelscope.cn/v1
```

### 支持的模型

| 模型名称 | 说明 | 适用场景 |
|---------|------|---------|
| `qwen-max` | 最强大的模型 | 复杂推理、专业分析 |
| `qwen-plus` | 平衡性能和速度 | 一般对话、常规任务 |
| `qwen-turbo` | 最快速度 | 简单任务、高并发 |
| `qwen2.5-72b-instruct` | 开源版本 | 自定义部署 |

**推荐**：Alpha Arena 使用 `qwen-max` 以获得最佳交易决策质量。

### 请求格式

ModelScope API 完全兼容 OpenAI 格式：

```python
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key="your-token",
    base_url="https://api-inference.modelscope.cn/v1"
)

response = await client.chat.completions.create(
    model="qwen-max",
    messages=[
        {"role": "user", "content": "你好"}
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)
```

### 参数说明

| 参数 | 类型 | 说明 | 默认值 |
|-----|------|------|--------|
| `model` | string | 模型名称 | 必填 |
| `messages` | array | 对话消息列表 | 必填 |
| `temperature` | float | 随机性 (0-2) | 0.7 |
| `max_tokens` | int | 最大生成 token 数 | 1500 |
| `top_p` | float | 核采样概率 | 1.0 |
| `stream` | bool | 是否流式返回 | false |

---

## 🧪 测试 API 连接

### 运行测试脚本

```bash
python scripts/test_modelscope.py
```

### 预期输出

```
============================================================
测试 ModelScope API (通义千问)
============================================================

✓ API 密钥已配置: your-token...

✓ QwenProvider 初始化成功

🤖 正在调用 ModelScope API...
模型: qwen-max

✅ API 调用成功！

============================================================
返回结果:
============================================================

推理过程: 基于当前 BTC 价格走势和市场情绪...

交易决策:
  - 币种: BTC
    动作: BUY
    数量: 0.1
    信心: 75%

============================================================
🎉 测试通过！ModelScope API 工作正常
============================================================
```

---

## 🔧 代码实现

### 在 Alpha Arena 中的使用

项目中已经集成了 ModelScope API，相关代码：

#### `app/strategy/llm_providers/qwen.py`

```python
from openai import AsyncOpenAI

class QwenProvider:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api-inference.modelscope.cn/v1"
        )
    
    async def generate_decision(
        self,
        prompt: str,
        model: str = "qwen-max",
        temperature: float = 0.7
    ) -> Dict:
        response = await self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=1000
        )
        
        content = response.choices[0].message.content.strip()
        return json.loads(content)
```

#### `app/core/config.py`

```python
class Settings(BaseSettings):
    # ...
    MODELSCOPE_API_KEY: str = ""  # 通义千问 (ModelScope API)
```

#### `app/strategy/llm_strategy.py`

```python
def _get_llm_provider(self, provider: str, model: str):
    if provider == "qwen":
        return QwenProvider(settings.MODELSCOPE_API_KEY), model
    # ...
```

---

## 💰 费用说明

### 免费额度

新用户通常会获得一定的免费额度。

### 计费方式

按 Token 数量计费，具体价格请查看：
https://www.modelscope.cn/docs/model-service/API-Inference/intro

### 成本优化建议

1. **选择合适的模型**
   - 简单任务使用 `qwen-turbo`（更便宜）
   - 复杂分析使用 `qwen-max`

2. **控制 Token 数量**
   - 设置合理的 `max_tokens`
   - 精简提示词

3. **监控使用量**
   - 定期检查 Token 消耗
   - 设置预算告警

---

## 🐛 常见问题

### Q1: API Token 在哪里获取？

**A**: 访问 https://www.modelscope.cn/my/myaccesstoken

### Q2: Token 创建后忘记保存怎么办？

**A**: 删除旧 Token，创建新的 Token。Token 只在创建时显示一次。

### Q3: 提示 "Invalid API Key" 错误？

**A**: 检查：
1. Token 是否复制完整
2. `.env` 文件中是否有多余的空格或引号
3. Token 是否已过期或被删除

### Q4: 与 DashScope API 有什么区别？

**A**: 
- **DashScope**: 阿里云官方 API，需要阿里云账号
- **ModelScope**: 社区版 API，使用 OpenAI 格式，更简单

两者都调用同样的通义千问模型，质量相同。

### Q5: 可以使用其他模型吗？

**A**: 可以！ModelScope 支持多种开源模型。修改 `model` 参数即可：
```python
model="qwen2.5-72b-instruct"  # 或其他支持的模型
```

查看完整模型列表：https://www.modelscope.cn/models

### Q6: 支持流式输出吗？

**A**: 支持！设置 `stream=True`：
```python
response = await client.chat.completions.create(
    model="qwen-max",
    messages=[...],
    stream=True
)

async for chunk in response:
    print(chunk.choices[0].delta.content)
```

---

## 📊 性能对比

### 响应速度

| 模型 | 平均延迟 | 适用场景 |
|-----|---------|---------|
| `qwen-turbo` | ~1-2s | 高频交易信号 |
| `qwen-plus` | ~2-4s | 常规分析 |
| `qwen-max` | ~3-6s | 深度分析 |

### 质量评估

对于加密货币交易分析：
- **准确性**: qwen-max > qwen-plus > qwen-turbo
- **推理能力**: qwen-max > qwen-plus > qwen-turbo
- **成本**: qwen-max > qwen-plus > qwen-turbo

**建议**: Alpha Arena 使用 `qwen-max` 以获得最佳决策质量。

---

## 🔒 安全建议

1. **不要泄露 Token**
   - ✅ 添加到 `.gitignore`
   - ✅ 不要提交到代码仓库
   - ✅ 不要在公开场合分享

2. **定期轮换 Token**
   - 定期（如每月）更新 Token
   - 怀疑泄露时立即更换

3. **设置使用限制**
   - 在 ModelScope 控制台设置配额
   - 监控异常使用

---

## 📚 相关链接

- **ModelScope 首页**: https://www.modelscope.cn/
- **API 文档**: https://www.modelscope.cn/docs/model-service/API-Inference/intro
- **API Token 管理**: https://www.modelscope.cn/my/myaccesstoken
- **模型列表**: https://www.modelscope.cn/models
- **社区论坛**: https://www.modelscope.cn/forum

---

## 🆘 获取帮助

如果遇到问题：

1. 查看本文档的「常见问题」部分
2. 检查官方文档：https://www.modelscope.cn/docs/model-service/API-Inference/intro
3. 运行测试脚本：`python scripts/test_modelscope.py`
4. 查看日志文件了解详细错误信息

---

**祝你使用愉快！🎉**

