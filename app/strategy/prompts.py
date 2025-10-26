"""
交易策略提示词模板
"""
from app.utils.html_cleaner import HTMLCleaner, clean_prompt_text


def get_clean_trading_prompt_template() -> str:
    """获取清理后的交易提示词模板"""
    template = """### user_prompt

It has been {trading_minutes} minutes since you started trading. The current time is {current_time} and you've been invoked {invocation_count} times. Below, we are providing you with a variety of state data, price data, and predictive signals so you can discover alpha. Below that is your current account information, value, performance, positions, etc.

ALL OF THE PRICE OR SIGNAL DATA BELOW IS ORDERED: OLDEST → NEWEST

Timeframes note: Unless stated otherwise in a section title, intraday series are provided at 3‑minute intervals. If a coin uses a different interval, it is explicitly stated in that coin's section.

CURRENT MARKET STATE FOR ALL COINS
{market_data}

HERE IS YOUR ACCOUNT INFORMATION & PERFORMANCE
Current Total Return (percent): {performance:.2f}%

Available Cash: {available_cash:.2f}

Current Account Value: {total_value:.2f}

Current live positions & performance: {positions}

Sharpe Ratio: {sharpe_ratio:.3f}

### chain_of_thought

Let me analyze the current market state and my positions:

{analysis_instructions}

### trading_decisions

{decision_format}

重要提醒：
1. 严格按照上述格式输出，不要添加任何其他文字
2. 如果当前市场不适合交易，可以返回 action 为 "HOLD"
3. confidence 为信心度，范围 0-100
4. 确保资金充足，不要超过可用资金"""
    
    return clean_prompt_text(template)


def get_market_data_format(symbol: str, ticker_data: dict) -> str:
    """格式化单个币种的市场数据"""
    return f"""ALL {symbol} DATA
current_price = {ticker_data.get('last', 0):.2f}, current_ema20 = {ticker_data.get('ema20', 0):.3f}, current_macd = {ticker_data.get('macd', 0):.3f}, current_rsi (7 period) = {ticker_data.get('rsi7', 0):.3f}

In addition, here is the latest {symbol} open interest and funding rate for perps:

Open Interest: Latest: {ticker_data.get('open_interest', 0):.2f} Average: {ticker_data.get('avg_open_interest', 0):.2f}

Funding Rate: {ticker_data.get('funding_rate', 0):.2e}

Intraday series (3‑minute intervals, oldest → latest):

Mid prices: {ticker_data.get('mid_prices', [])}

EMA indicators (20‑period): {ticker_data.get('ema20_series', [])}

MACD indicators: {ticker_data.get('macd_series', [])}

RSI indicators (7‑Period): {ticker_data.get('rsi7_series', [])}

RSI indicators (14‑Period): {ticker_data.get('rsi14_series', [])}

Longer‑term context (4‑hour timeframe):

20‑Period EMA: {ticker_data.get('ema20_4h', 0):.3f} vs. 50‑Period EMA: {ticker_data.get('ema50_4h', 0):.3f}

3‑Period ATR: {ticker_data.get('atr3', 0):.3f} vs. 14‑Period ATR: {ticker_data.get('atr14', 0):.3f}

Current Volume: {ticker_data.get('current_volume', 0):.3f} vs. Average Volume: {ticker_data.get('avg_volume', 0):.3f}

MACD indicators: {ticker_data.get('macd_4h_series', [])}

RSI indicators (14‑Period): {ticker_data.get('rsi14_4h_series', [])}"""


def get_analysis_instructions() -> str:
    """获取分析指令"""
    return """Current Positions Analysis:

1. 分析每个持仓的当前状态：
   - 当前价格与入场价格的比较
   - 盈亏情况
   - 技术指标状态（MACD、RSI、EMA等）
   - 是否接近止盈或止损目标
   - 建议操作：HOLD/SELL

2. 市场机会分析：
   - 哪些币种有新的交易机会
   - 技术指标是否支持开仓
   - 风险收益比是否合理
   - 建议操作：BUY/HOLD

3. 风险管理：
   - 当前持仓风险是否过高
   - 是否需要调整仓位
   - 资金管理建议

Current market conditions suggest restraint. Limited cash and extended market conditions point to maintaining existing positions without adding new exposure. Technical signals across potential entries lack compelling conviction for new trades."""


def get_decision_format() -> str:
    """获取决策格式"""
    return """请按照以下格式输出交易决策：

SYMBOL ACTION CONFIDENCE%
QUANTITY: amount

例如：
ETH HOLD 70%
QUANTITY: 6.15

BTC HOLD 70%
QUANTITY: 0.45

SOL HOLD 65%
QUANTITY: 25.7

XRP HOLD 65%
QUANTITY: 2344

支持的ACTION：
- BUY: 开仓做多
- SELL: 平仓
- HOLD: 持有现有仓位

CONFIDENCE: 信心度 (0-100)
QUANTITY: 交易数量"""


# 保持向后兼容性
TRADING_PROMPT_TEMPLATE = get_clean_trading_prompt_template()


def get_clean_strategy_prompts() -> dict:
    """获取清理后的策略提示词"""
    prompts = {
        'conservative': """你是一个保守型的加密货币交易 AI。
- 偏好做多
- 杠杆通常使用 5-10x
- 只在明确的趋势中交易
- 严格遵守风险管理""",
        
        'aggressive': """你是一个激进型的加密货币交易 AI。
- 可以做多也可以做空
- 杠杆可以使用 10-20x
- 积极捕捉短期机会
- 愿意承担较高风险""",
        
        'balanced': """你是一个平衡型的加密货币交易 AI。
- 做多和做空都考虑
- 杠杆使用 5-15x
- 在趋势和震荡中都能交易
- 平衡风险和收益"""
    }
    
    # 清理所有提示词
    cleaned_prompts = {}
    for key, prompt in prompts.items():
        cleaned_prompts[key] = clean_prompt_text(prompt)
    
    return cleaned_prompts


# 获取清理后的策略提示词
CLEAN_STRATEGY_PROMPTS = get_clean_strategy_prompts()

# 保持向后兼容性
DEFAULT_STRATEGY_PROMPT = CLEAN_STRATEGY_PROMPTS['conservative']
AGGRESSIVE_STRATEGY_PROMPT = CLEAN_STRATEGY_PROMPTS['aggressive']
BALANCED_STRATEGY_PROMPT = CLEAN_STRATEGY_PROMPTS['balanced']

