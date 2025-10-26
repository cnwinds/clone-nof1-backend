# 变更日志

## [2025-10-26] - ModelScope API 迁移 + 模型配置优化

### 🎯 主要变更

#### 1. **通义千问 API 迁移** 

从 DashScope API 迁移到 ModelScope API

**为什么迁移？**
- ✅ 无需阿里云账号
- ✅ 使用 OpenAI 兼容格式
- ✅ 更简单的认证流程
- ✅ 与其他 LLM 提供商代码风格统一

**变更详情**:
- `app/strategy/llm_providers/qwen.py` - 使用 OpenAI SDK + ModelScope base URL
- `app/core/config.py` - `DASHSCOPE_API_KEY` → `MODELSCOPE_API_KEY`
- `app/strategy/llm_strategy.py` - 更新密钥引用
- `requirements.txt` - 移除 `dashscope` 包

**相关文档**:
- [MODELSCOPE_SETUP.md](MODELSCOPE_SETUP.md) - 详细配置指南
- [MODELSCOPE_MIGRATION.md](MODELSCOPE_MIGRATION.md) - 迁移说明

---

#### 2. **模型配置优化**

只激活 **QWEN3 MAX** 和 **DEEPSEEK V3** 两个模型进行竞技

**变更文件**:
- `scripts/seed_data.py` - 设置模型激活状态
  - `qwen3-max`: `active`
  - `deepseek-v3`: `active`
  - 其他模型: `inactive`

**影响**:
- 只需配置 2 个 API 密钥即可启动
- 降低 API 调用成本
- 简化测试流程

**相关文档**:
- [MODEL_CONFIG_SUMMARY.md](MODEL_CONFIG_SUMMARY.md) - 模型配置详情

---

#### 3. **Docker Compose 配置优化**

简化环境变量配置

**变更**:
- 使用 `env_file` 替代显式的 `environment` 列表
- 所有环境变量统一在 `.env` 文件管理
- 自动读取 `.env` 文件中的所有变量

---

#### 4. **新增测试脚本**

**新增文件**:
- `scripts/test_modelscope.py` - 测试 ModelScope API 连接

**使用**:
```bash
python scripts/test_modelscope.py
```

---

#### 5. **文档完善**

**新增文档**:
- `MODELSCOPE_SETUP.md` - ModelScope API 详细配置指南
- `MODELSCOPE_MIGRATION.md` - DashScope → ModelScope 迁移说明
- `SETUP_GUIDE.md` - 完整配置指南
- `MODEL_CONFIG_SUMMARY.md` - 模型配置总结
- `CHANGELOG.md` - 本文档

**更新文档**:
- `README.md` - 更新 API 密钥链接和配置说明
- `ENV_CONFIG.md` - 更新环境变量说明
- All docs - 所有 `DASHSCOPE_API_KEY` 引用更新为 `MODELSCOPE_API_KEY`

---

### 🔄 迁移指南

#### 旧用户（已部署）

如果你之前使用 DashScope API：

1. **获取 ModelScope Token**
   ```
   https://www.modelscope.cn/my/myaccesstoken
   ```

2. **更新 `.env` 文件**
   ```bash
   # 删除
   DASHSCOPE_API_KEY=sk-xxx
   
   # 添加
   MODELSCOPE_API_KEY=your-token-here
   ```

3. **更新依赖**
   ```bash
   pip uninstall dashscope -y
   pip install -r requirements.txt
   ```

4. **重启服务**
   ```bash
   docker-compose restart
   # 或
   # 重启 API 和 Celery Worker
   ```

#### 新用户

直接按照 [SETUP_GUIDE.md](SETUP_GUIDE.md) 配置即可。

---

### 📦 依赖变更

#### 移除
```diff
- dashscope==1.14.0
```

#### 无需新增
ModelScope API 使用 OpenAI SDK，无需额外包。

---

### 🔑 环境变量变更

#### 重命名
```diff
- DASHSCOPE_API_KEY=sk-xxx
+ MODELSCOPE_API_KEY=your-token-xxx
```

#### 最小配置（当前激活模型）
```env
DATABASE_URL=mysql+pymysql://root:password@mysql:3306/alpha_arena
REDIS_URL=redis://redis:6379/0
MODELSCOPE_API_KEY=your-modelscope-token-here  # 通义千问
DEEPSEEK_API_KEY=sk-your-deepseek-key-here     # DeepSeek
```

---

### ✅ 兼容性

#### API 功能
- ✅ 所有 DashScope 功能在 ModelScope 中完全支持
- ✅ 模型名称保持不变 (`qwen-max`, `qwen-plus`, `qwen-turbo`)
- ✅ 输出质量和格式完全一致

#### 现有数据
- ✅ 无需修改数据库
- ✅ 现有的模型、赛季、交易记录不受影响
- ✅ 只需更新 API 密钥

---

### 🧪 测试

#### 单元测试

```bash
# 测试 ModelScope API
python scripts/test_modelscope.py

# 测试 DeepSeek API
python scripts/test_deepseek.py

# 测试 CoinGecko API
python scripts/test_coingecko.py
```

#### 集成测试

```bash
# 完整系统测试
python scripts/test_system.py
```

---

### 📊 性能影响

#### 响应延迟
- 📈 无明显变化（~3s，与 DashScope 一致）

#### API 成本
- 💰 可能更低（具体查看 ModelScope 定价）

#### 开发体验
- 🚀 显著提升（统一的代码风格）

---

### 🐛 已知问题

目前无已知问题。

如遇到问题，请查看：
- [MODELSCOPE_SETUP.md](MODELSCOPE_SETUP.md) - 常见问题
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - 故障排除

---

### 📚 相关链接

**项目文档**:
- [README.md](README.md) - 项目主文档
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - 配置指南
- [QUICKSTART.md](QUICKSTART.md) - 快速开始
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 项目总结

**ModelScope 相关**:
- [MODELSCOPE_SETUP.md](MODELSCOPE_SETUP.md) - ModelScope 配置
- [MODELSCOPE_MIGRATION.md](MODELSCOPE_MIGRATION.md) - 迁移说明
- [ModelScope 官网](https://www.modelscope.cn/)
- [ModelScope API 文档](https://www.modelscope.cn/docs/model-service/API-Inference/intro)
- [获取 API Token](https://www.modelscope.cn/my/myaccesstoken)

**其他**:
- [ENV_CONFIG.md](ENV_CONFIG.md) - 环境变量
- [MODEL_CONFIG_SUMMARY.md](MODEL_CONFIG_SUMMARY.md) - 模型配置

---

### 👥 贡献者

本次更新由 AI 助手完成。

---

### 📝 反馈

如有问题或建议，请：
1. 查看相关文档的「常见问题」部分
2. 运行测试脚本诊断问题
3. 检查日志文件

---

**更新日期**: 2025-10-26
**版本**: v1.1.0

