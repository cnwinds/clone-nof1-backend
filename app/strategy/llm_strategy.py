"""
LLM 驱动的交易策略
"""
from app.strategy.base import BaseStrategy
from app.strategy.llm_providers.openai import OpenAIProvider
from app.strategy.llm_providers.anthropic import AnthropicProvider
from app.strategy.llm_providers.qwen import QwenProvider
from app.strategy.llm_providers.deepseek import DeepSeekProvider
from app.strategy.prompts import TRADING_PROMPT_TEMPLATE
from app.exchange.factory import ExchangeFactory
from app.models import SeasonModel, Trade, Position, AutomatedChat
from app.core.config import settings
from sqlalchemy.orm import Session, joinedload
from typing import Dict, List
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)


class LLMStrategy(BaseStrategy):
    """基于 LLM 的交易策略"""
    
    def __init__(self, db: Session):
        super().__init__(db)
    
    def _get_llm_provider(self, provider: str, model: str):
        """获取 LLM 提供商实例"""
        if provider == "openai":
            return OpenAIProvider(settings.OPENAI_API_KEY), model
        elif provider == "anthropic":
            return AnthropicProvider(settings.ANTHROPIC_API_KEY), model
        elif provider == "qwen":
            return QwenProvider(settings.MODELSCOPE_API_KEY), model
        elif provider == "deepseek":
            return DeepSeekProvider(settings.DEEPSEEK_API_KEY), model
        else:
            raise ValueError(f"不支持的 LLM 提供商: {provider}")
    
    async def execute(self, season_model_id: str) -> Dict:
        """执行策略"""
        try:
            # 获取赛季模型实例
            season_model = self.db.query(SeasonModel).options(
                joinedload(SeasonModel.model),
                joinedload(SeasonModel.season)
            ).filter(SeasonModel.id == season_model_id).first()
            
            if not season_model:
                return {"success": False, "message": "赛季模型不存在"}
            
            # 检查赛季状态
            if season_model.season.status != "active":
                return {"success": False, "message": "赛季未激活"}
            
            # 检查模型状态
            if season_model.status != "active":
                return {"success": False, "message": "模型已淘汰或已完成"}
            
            # 检查资金
            if season_model.current_value <= 0:
                season_model.status = "eliminated"
                season_model.eliminated_at = datetime.utcnow()
                self.db.commit()
                return {"success": False, "message": "资金已耗尽"}
            
            # 获取当前持仓
            positions = self.db.query(Position).filter(
                Position.season_model_id == season_model_id
            ).all()
            
            # 获取市场数据
            market_data = await self.analyze_market(["BTC", "ETH", "XRP", "SOL", "BNB", "ADA"])
            
            # 构建提示词
            prompt = self._build_prompt(season_model, positions, market_data)
            
            # 调用 LLM 生成决策
            llm_provider, llm_model = self._get_llm_provider(
                season_model.model.llm_provider,
                season_model.model.llm_model
            )
            decision = await llm_provider.generate_decision(prompt, llm_model)
            
            # 记录聊天
            await self._save_chat(season_model_id, prompt, decision)
            
            # 执行交易决策
            trades = await self._execute_decisions(season_model, decision, market_data)
            
            # 更新账户价值
            await self._update_account_value(season_model)
            
            return {
                "success": True,
                "message": f"成功执行 {len(trades)} 笔交易",
                "trades": trades
            }
            
        except Exception as e:
            logger.error(f"执行策略失败 {season_model_id}: {e}")
            return {"success": False, "message": str(e)}
    
    async def analyze_market(self, symbols: List[str]) -> Dict:
        """分析市场"""
        try:
            # 使用模拟交易交易所获取市场数据（不需要 API 密钥）
            exchange = ExchangeFactory.create_exchange("binance", "paper")
            tickers = await exchange.get_multiple_tickers(symbols)
            await exchange.close()
            return tickers
        except Exception as e:
            logger.error(f"获取市场数据失败: {e}")
            return {}
    
    def _build_prompt(
        self,
        season_model: SeasonModel,
        positions: List[Position],
        market_data: Dict
    ) -> str:
        """构建提示词"""
        # 格式化持仓信息
        positions_str = ""
        if positions:
            for pos in positions:
                positions_str += f"- {pos.symbol}: {pos.side} {pos.amount} @ ${pos.entry_price:.2f}, "
                positions_str += f"当前价格: ${pos.current_price:.2f}, "
                positions_str += f"盈亏: ${pos.unrealized_pnl:.2f} ({pos.profit_percent:.2f}%)\n"
        else:
            positions_str = "无持仓\n"
        
        # 格式化市场数据
        market_str = ""
        for symbol, ticker in market_data.items():
            base_symbol = symbol.split('/')[0]
            market_str += f"- {base_symbol}: ${ticker['last']:.2f}\n"
        
        # 使用模型的自定义提示词或默认提示词
        custom_prompt = season_model.model.strategy_prompt or ""
        
        return TRADING_PROMPT_TEMPLATE.format(
            available_cash=season_model.available_cash,
            total_value=season_model.current_value,
            performance=season_model.performance,
            positions=positions_str,
            market_data=market_str
        ) + f"\n\n## 你的交易风格\n{custom_prompt}"
    
    async def _execute_decisions(
        self,
        season_model: SeasonModel,
        decision: Dict,
        market_data: Dict
    ) -> List[Dict]:
        """执行交易决策"""
        trades = []
        
        for dec in decision.get("decisions", []):
            action = dec.get("action", "HOLD")
            
            if action == "BUY":
                trade = await self._open_position(season_model, dec, market_data)
                if trade:
                    trades.append(trade)
            
            elif action == "SELL":
                trade = await self._close_position(season_model, dec, market_data)
                if trade:
                    trades.append(trade)
        
        return trades
    
    async def _open_position(
        self,
        season_model: SeasonModel,
        decision: Dict,
        market_data: Dict
    ) -> Dict:
        """开仓"""
        try:
            symbol = decision["symbol"]
            quantity = decision["quantity"]
            side = decision.get("side", "LONG")
            leverage = decision.get("leverage", 1)
            
            # 获取当前价格
            ticker_symbol = f"{symbol}/USDT"
            if ticker_symbol not in market_data:
                logger.warning(f"市场数据中没有 {ticker_symbol}")
                return None
            
            price = market_data[ticker_symbol]["last"]
            notional = price * quantity * leverage
            
            # 检查资金是否充足
            if notional > season_model.available_cash:
                logger.warning(f"资金不足: 需要 {notional}, 可用 {season_model.available_cash}")
                return None
            
            # 创建交易记录
            trade = Trade(
                id=str(uuid.uuid4()),
                season_model_id=season_model.id,
                symbol=symbol,
                type="long" if side == "LONG" else "short",
                entry_price=price,
                quantity=quantity,
                entry_notional=notional,
                status="open",
                entry_timestamp=datetime.utcnow()
            )
            self.db.add(trade)
            
            # 创建持仓
            position = Position(
                id=str(uuid.uuid4()),
                season_model_id=season_model.id,
                symbol=symbol,
                side=side,
                leverage=leverage,
                amount=quantity,
                entry_price=price,
                current_price=price,
                notional=notional,
                unrealized_pnl=0,
                profit_percent=0
            )
            self.db.add(position)
            
            # 更新可用资金
            season_model.available_cash -= notional / leverage
            season_model.total_trades += 1
            
            self.db.commit()
            
            logger.info(f"开仓: {symbol} {side} {quantity} @ {price}")
            
            return {
                "trade_id": trade.id,
                "symbol": symbol,
                "action": "BUY",
                "price": price,
                "quantity": quantity
            }
            
        except Exception as e:
            logger.error(f"开仓失败: {e}")
            self.db.rollback()
            return None
    
    async def _close_position(
        self,
        season_model: SeasonModel,
        decision: Dict,
        market_data: Dict
    ) -> Dict:
        """平仓"""
        try:
            symbol = decision["symbol"]
            
            # 查找持仓
            position = self.db.query(Position).filter(
                Position.season_model_id == season_model.id,
                Position.symbol == symbol
            ).first()
            
            if not position:
                logger.warning(f"没有找到 {symbol} 的持仓")
                return None
            
            # 获取当前价格
            ticker_symbol = f"{symbol}/USDT"
            if ticker_symbol not in market_data:
                logger.warning(f"市场数据中没有 {ticker_symbol}")
                return None
            
            exit_price = market_data[ticker_symbol]["last"]
            exit_notional = exit_price * position.amount * position.leverage
            
            # 计算盈亏
            if position.side == "LONG":
                pnl = (exit_price - position.entry_price) * position.amount
            else:  # SHORT
                pnl = (position.entry_price - exit_price) * position.amount
            
            pnl_percent = (pnl / position.notional) * 100
            
            # 查找对应的开仓交易
            trade = self.db.query(Trade).filter(
                Trade.season_model_id == season_model.id,
                Trade.symbol == symbol,
                Trade.status == "open"
            ).first()
            
            if trade:
                # 更新交易记录
                trade.exit_price = exit_price
                trade.exit_notional = exit_notional
                trade.pnl = pnl
                trade.pnl_percent = pnl_percent
                trade.status = "closed"
                trade.exit_timestamp = datetime.utcnow()
                
                # 计算持仓时间
                holding_duration = trade.exit_timestamp - trade.entry_timestamp
                hours = holding_duration.total_seconds() / 3600
                if hours < 1:
                    trade.holding_time = f"{int(hours * 60)}M"
                else:
                    trade.holding_time = f"{int(hours)}H"
            
            # 删除持仓
            self.db.delete(position)
            
            # 更新可用资金
            season_model.available_cash += exit_notional / position.leverage
            
            # 更新胜率
            closed_trades = self.db.query(Trade).filter(
                Trade.season_model_id == season_model.id,
                Trade.status == "closed"
            ).all()
            
            winning_trades = len([t for t in closed_trades if t.pnl > 0])
            if len(closed_trades) > 0:
                season_model.win_rate = (winning_trades / len(closed_trades)) * 100
            
            self.db.commit()
            
            logger.info(f"平仓: {symbol} @ {exit_price}, 盈亏: {pnl:.2f}")
            
            return {
                "trade_id": trade.id if trade else None,
                "symbol": symbol,
                "action": "SELL",
                "price": exit_price,
                "pnl": pnl
            }
            
        except Exception as e:
            logger.error(f"平仓失败: {e}")
            self.db.rollback()
            return None
    
    async def _update_account_value(self, season_model: SeasonModel):
        """更新账户价值"""
        try:
            # 获取所有持仓
            positions = self.db.query(Position).filter(
                Position.season_model_id == season_model.id
            ).all()
            
            # 计算持仓市值
            positions_value = sum([pos.notional + pos.unrealized_pnl for pos in positions])
            
            # 总价值 = 可用资金 + 持仓市值
            total_value = season_model.available_cash + positions_value
            season_model.current_value = total_value
            
            # 计算收益率
            if season_model.initial_value > 0:
                season_model.performance = (
                    (total_value - season_model.initial_value) / season_model.initial_value * 100
                )
            
            self.db.commit()
            
        except Exception as e:
            logger.error(f"更新账户价值失败: {e}")
            self.db.rollback()
    
    async def _save_chat(self, season_model_id: str, prompt: str, decision: Dict):
        """保存聊天记录"""
        try:
            content = decision.get("reasoning", "")[:200]  # 摘要
            
            chat = AutomatedChat(
                id=str(uuid.uuid4()),
                season_model_id=season_model_id,
                content=content,
                user_prompt=prompt,
                chain_of_thought=decision.get("reasoning", ""),
                trading_decisions=decision.get("decisions", []),
                timestamp=datetime.utcnow()
            )
            
            self.db.add(chat)
            self.db.commit()
            
        except Exception as e:
            logger.error(f"保存聊天记录失败: {e}")
            self.db.rollback()

