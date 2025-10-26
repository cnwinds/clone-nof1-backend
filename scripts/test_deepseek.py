"""
测试 DeepSeek API 连接
文档: https://platform.deepseek.com/api-docs
"""
import sys
from pathlib import Path
import asyncio

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from app.strategy.llm_providers.deepseek import DeepSeekProvider
from app.core.config import settings


async def test_deepseek():
    """测试 DeepSeek API"""
    print("=" * 60)
    print("测试 DeepSeek API")
    print("=" * 60)
    print()
    
    # 检查 API 密钥
    if not settings.DEEPSEEK_API_KEY:
        print("❌ 错误: 未配置 DEEPSEEK_API_KEY")
        print()
        print("请在 .env 文件中添加:")
        print("DEEPSEEK_API_KEY=sk-your-deepseek-key-here")
        print()
        print("获取 API Key:")
        print("https://platform.deepseek.com/api_keys")
        return
    
    print(f"✓ API 密钥已配置: {settings.DEEPSEEK_API_KEY[:20]}...")
    print()
    
    try:
        # 创建提供商实例
        provider = DeepSeekProvider(settings.DEEPSEEK_API_KEY)
        print("✓ DeepSeekProvider 初始化成功")
        print()
        
        # 测试简单的提示词
        test_prompt = """
你是一个加密货币交易专家。请根据以下市场数据给出交易建议：

BTC 当前价格: $67,000
24h 涨跌: +2.5%
市场情绪: 看涨

请以 JSON 格式返回你的分析和决策:
{
    "reasoning": "你的分析思路",
    "decisions": [
        {
            "symbol": "BTC",
            "action": "BUY/SELL/HOLD",
            "quantity": 数量,
            "confidence": 0-100
        }
    ]
}
"""
        
        print("🤖 正在调用 DeepSeek API...")
        print(f"模型: deepseek-chat")
        print()
        
        # 调用 API
        result = await provider.generate_decision(
            prompt=test_prompt,
            model="deepseek-chat",
            temperature=0.7
        )
        
        print("✅ API 调用成功！")
        print()
        print("=" * 60)
        print("返回结果:")
        print("=" * 60)
        print()
        print(f"推理过程: {result.get('reasoning', 'N/A')}")
        print()
        print("交易决策:")
        for decision in result.get('decisions', []):
            print(f"  - 币种: {decision.get('symbol', 'N/A')}")
            print(f"    动作: {decision.get('action', 'N/A')}")
            print(f"    数量: {decision.get('quantity', 0)}")
            print(f"    信心: {decision.get('confidence', 0)}%")
            print()
        
        print("=" * 60)
        print("🎉 测试通过！DeepSeek API 工作正常")
        print("=" * 60)
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ 测试失败")
        print("=" * 60)
        print()
        print(f"错误信息: {e}")
        print()
        print("常见问题:")
        print("1. 检查 API Key 是否正确")
        print("2. 检查网络连接")
        print("3. 检查 API Key 是否有效（未过期）")
        print()
        print("获取帮助:")
        print("- DeepSeek 文档: https://platform.deepseek.com/api-docs")
        print("- API Key 管理: https://platform.deepseek.com/api_keys")
        raise


if __name__ == "__main__":
    asyncio.run(test_deepseek())
