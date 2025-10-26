"""
DeepSeek 提供商
文档: https://platform.deepseek.com/api-docs
"""
from openai import AsyncOpenAI
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class DeepSeekProvider:
    """DeepSeek LLM 提供商 (兼容 OpenAI API)"""
    
    def __init__(self, api_key: str):
        # DeepSeek API 兼容 OpenAI 格式
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
    
    async def generate_decision(
        self,
        prompt: str,
        model: str = "deepseek-chat",
        temperature: float = 0.7
    ) -> str:
        """
        生成交易决策
        
        Args:
            prompt: 提示词
            model: 模型名称 (deepseek-chat, deepseek-reasoner)
            temperature: 温度参数
            
        Returns:
            决策文本字符串
        """
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            return content
            
        except Exception as e:
            logger.error(f"DeepSeek API 调用失败: {e}")
            # 返回默认的 HOLD 决策
            return """
### chain_of_thought

解析错误，保持现有仓位

### trading_decisions

BTC HOLD 0%
QUANTITY: 0
"""

