"""
Anthropic Claude 提供商
"""
from anthropic import AsyncAnthropic
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class AnthropicProvider:
    """Anthropic Claude 提供商"""
    
    def __init__(self, api_key: str):
        self.client = AsyncAnthropic(api_key=api_key)
    
    async def generate_decision(
        self,
        prompt: str,
        model: str = "claude-3-opus-20240229",
        temperature: float = 0.7
    ) -> str:
        """
        生成交易决策
        
        Args:
            prompt: 提示词
            model: 模型名称 (claude-3-opus, claude-3-sonnet, claude-3-haiku)
            temperature: 温度参数
            
        Returns:
            决策文本字符串
        """
        try:
            response = await self.client.messages.create(
                model=model,
                max_tokens=1000,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.content[0].text.strip()
            return content
            
        except Exception as e:
            logger.error(f"Claude API 调用失败: {e}")
            # 返回默认的 HOLD 决策
            return """
### chain_of_thought

解析错误，保持现有仓位

### trading_decisions

BTC HOLD 0%
QUANTITY: 0
"""

