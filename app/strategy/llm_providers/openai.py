"""
OpenAI GPT 提供商
"""
from openai import AsyncOpenAI
from typing import Dict, Optional
import json
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
    ) -> Dict:
        """
        生成交易决策
        
        Args:
            prompt: 提示词
            model: 模型名称 (gpt-4, gpt-3.5-turbo, gpt-4-turbo)
            temperature: 温度参数
            
        Returns:
            {
                "reasoning": "...",
                "decisions": [...]
            }
        """
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是一个专业的加密货币交易 AI。请严格按照 JSON 格式返回结果。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # 尝试解析 JSON
            # 有时 LLM 会返回 ```json ... ``` 格式
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
            logger.error(f"OpenAI 返回内容无法解析为 JSON: {content}")
            # 返回默认的 HOLD 决策
            return {
                "reasoning": "解析错误，保持现有仓位",
                "decisions": [{"symbol": "BTC", "action": "HOLD", "quantity": 0, "confidence": 0}]
            }
        except Exception as e:
            logger.error(f"OpenAI API 调用失败: {e}")
            raise

