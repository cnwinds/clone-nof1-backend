"""
通义千问提供商 (通过 ModelScope API)
文档: https://www.modelscope.cn/docs/model-service/API-Inference/intro
"""
from openai import AsyncOpenAI
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class QwenProvider:
    """通义千问提供商 (ModelScope API)"""
    
    def __init__(self, api_key: str):
        # ModelScope API 兼容 OpenAI 格式
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api-inference.modelscope.cn/v1"
        )
    
    async def generate_decision(
        self,
        prompt: str,
        model: str = "Qwen/Qwen3-235B-A22B-Instruct-2507",
        temperature: float = 0.7
    ) -> str:
        """
        生成交易决策
        
        Args:
            prompt: 提示词
            model: 模型名称 (qwen-max, qwen-plus, qwen-turbo, qwen2.5-72b-instruct 等)
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
            logger.error(f"Qwen API 调用失败: {e}")
            # 返回默认的 HOLD 决策
            return """
### chain_of_thought

解析错误，保持现有仓位

### trading_decisions

BTC HOLD 0%
QUANTITY: 0
"""

