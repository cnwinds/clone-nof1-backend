# 解决 Binance 地理限制问题 - 使用 CoinGecko

## 问题描述

如果你遇到以下错误：
```
"msg": "Service unavailable from a restricted location according to 'b. Eligibility'"
```

这是因为 Binance 对某些地区有访问限制（如美国、中国等）。

## ✅ 已解决！

**好消息**：代码已经更新为使用 **CoinGecko API**，无地理限制！

### 更改内容

1. ✅ 新增 `app/exchange/coingecko.py` - CoinGecko 数据源
2. ✅ 更新 `app/exchange/paper_trading.py` - 默认使用 CoinGecko
3. ✅ 无需任何配置，开箱即用

## 🚀 立即测试

### 1. 运行测试脚本

```bash
python scripts/test_real_market_data.py
```

**预期输出**：
```
============================================================
测试获取真实市场数据（CoinGecko）
============================================================

1. 获取 BTC 实时价格...
   ✓ BTC/USDT
     当前价格: $95,234.50
     24h 最高: $96,100.00
     24h 最低: $94,200.00
     买价: $95,233.00
     卖价: $95,236.00

2. 批量获取多个币种价格...
   ✓ BTC   $ 95,234.50
   ✓ ETH   $  3,456.78
   ✓ XRP   $     2.15
   ✓ SOL   $   145.67
   ✓ BNB   $   612.34
   ✓ ADA   $     0.65

3. 模拟交易（使用真实市场价格）...
   ✓ 模拟买入订单
   ...

✓ 所有测试通过！

说明:
- ✓ 使用真实的 CoinGecko 市场数据
- ✓ 无需 API 密钥
- ✓ 无地理位置限制
- ✓ 交易是模拟的
```

### 2. 启动完整系统

```bash
# 终端 1: 数据库
docker-compose up -d mysql redis

# 终端 2: 初始化
alembic upgrade head
python scripts/seed_data.py

# 终端 3: API 服务
uvicorn app.main:app --reload --port 3001

# 终端 4: Celery Worker
celery -A app.tasks.celery_app worker --loglevel=info

# 终端 5: Celery Beat
celery -A app.tasks.celery_app beat --loglevel=info
```

### 3. 查看日志

**Celery Worker 输出**：
```
[2024-01-01 10:00:00] 更新了 6 个币种的价格
[2024-01-01 10:05:00] 执行策略: 赛季=2025 Q1..., 模型=QWEN3 MAX
[2024-01-01 10:05:02] 模拟交易: buy 0.01 BTC/USDT @ 95234.50
```

✅ 不再有地理限制错误！

## 📊 CoinGecko vs Binance

| 特性 | CoinGecko | Binance |
|------|-----------|---------|
| **地理限制** | ❌ 无限制 | ⚠️ 有限制 |
| **需要 API 密钥** | ❌ 不需要 | ✅ 读取公开数据不需要 |
| **支持币种** | ✅ 10,000+ | ✅ 600+ |
| **更新频率** | 1-2 分钟 | 实时 |
| **适用场景** | 测试、开发 | 生产环境 |

## 🔧 高级配置

### 如果想切换回 Binance（需要无限制地区）

编辑 `app/exchange/paper_trading.py`：

```python
# 方式 1: 使用 Binance（有地理限制）
import ccxt.async_support as ccxt
self.exchange = ccxt.binance({'enableRateLimit': True})

# 方式 2: 使用 CoinGecko（无地理限制，默认）
from app.exchange.coingecko import CoinGeckoExchange
self.exchange = CoinGeckoExchange()
```

### 添加更多币种

编辑 `app/exchange/coingecko.py`：

```python
SYMBOL_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "XRP": "ripple",
    "SOL": "solana",
    "BNB": "binancecoin",
    "ADA": "cardano",
    # 添加新币种
    "DOGE": "dogecoin",
    "DOT": "polkadot",
    "MATIC": "matic-network",
}
```

查找币种 ID：https://www.coingecko.com/en/coins

## ⚡ CoinGecko API 限制

### 免费版
- **请求限制**: 50 次/分钟
- **速率**: 每个请求 1-2 秒延迟

### 当前配置
- 每 30 秒更新一次价格 ✅
- 批量获取（一次请求获取多个币种）✅
- 完全够用于测试和开发 ✅

### 如果需要更高频率

可以申请 CoinGecko Pro（付费）：
- 500 次/分钟
- 更低延迟

## 🌐 其他备选方案

### 方案 2: Binance.US（仅美国用户）

```python
# app/exchange/paper_trading.py
self.exchange = ccxt.binanceus({
    'enableRateLimit': True,
})
```

### 方案 3: Coinbase（全球可用）

```python
# app/exchange/paper_trading.py
self.exchange = ccxt.coinbase({
    'enableRateLimit': True,
})
```

### 方案 4: 多数据源备份

```python
# 自动切换（如果 CoinGecko 失败，尝试其他源）
try:
    ticker = await coingecko.get_ticker(symbol)
except:
    ticker = await coinbase.get_ticker(symbol)
```

## ❓ 常见问题

### Q: CoinGecko 数据准确吗？

**A**: 非常准确！CoinGecko 聚合多个交易所的数据，提供平均市场价格。

### Q: 为什么不直接使用 Binance？

**A**: Binance 有地理限制。CoinGecko 全球可用，更适合测试和开发。

### Q: CoinGecko 支持实时交易吗？

**A**: CoinGecko 只提供价格数据，不支持交易。但我们的系统是**模拟交易**，只需要价格数据。

### Q: 如何切换到真实交易？

**A**: 真实交易需要：
1. 在交易所（Binance/Coinbase）注册账户
2. 获取 API 密钥
3. 配置 `.env` 文件
4. 将模型的 `trading_mode` 改为 `"real"`

但**强烈建议**先用模拟交易测试！

## 📝 总结

✅ **问题已解决**：使用 CoinGecko 替代 Binance  
✅ **无需配置**：开箱即用  
✅ **无地理限制**：全球可用  
✅ **真实数据**：来自真实市场  
✅ **模拟交易**：安全测试  

现在可以正常使用所有功能了！🎉

---

**需要帮助？** 查看 [README.md](README.md) 或创建 Issue。

