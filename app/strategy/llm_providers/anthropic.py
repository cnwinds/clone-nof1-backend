"""
Anthropic Claude 提供商
"""
from anthropic import AsyncAnthropic
from typing import Dict, Optional
import json
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
    ) -> Dict:
        """
        生成交易决策
        
        Args:
            prompt: 提示词
            model: 模型名称 (claude-3-opus, claude-3-sonnet, claude-3-haiku)
            temperature: 温度参数
            
        Returns:
            {
                "reasoning": "...",
                "decisions": [...]
            }
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
            
            # 尝试解析 JSON
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            
            content = content.strip()
            
            result = json.loads(content)
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Claude 返回内容无法解析为 JSON: {content}")
            # 返回默认的 HOLD 决策
            return {
                "reasoning": "解析错误，保持现有仓位",
                "decisions": [{"symbol": "BTC", "action": "HOLD", "quantity": 0, "confidence": 0}]
            }
        except Exception as e:
            logger.error(f"Claude API 调用失败: {e}")
            raise

