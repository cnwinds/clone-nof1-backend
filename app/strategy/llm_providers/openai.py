"""
OpenAI GPT 提供商
"""
from openai import AsyncOpenAI
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class OpenAIProvider:
    """OpenAI GPT 提供商"""
    
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def generate_decision(
        self,
        prompt: str,
        model: str = "gpt-4",
        temperature: float = 0.7
    ) -> str:
        """
        生成交易决策
        
        Args:
            prompt: 提示词
            model: 模型名称 (gpt-4, gpt-3.5-turbo, gpt-4-turbo)
            temperature: 温度参数
            
        Returns:
            决策文本字符串
        """
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是一个专业的加密货币交易 AI。请严格按照指定的格式返回结果。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            return content
            
        except Exception as e:
            logger.error(f"OpenAI API 调用失败: {e}")
            # 返回默认的 HOLD 决策
            return """
### chain_of_thought

解析错误，保持现有仓位

### trading_decisions

BTC HOLD 0%
QUANTITY: 0
"""

