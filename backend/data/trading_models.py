from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, Float
from sqlalchemy.dialects.postgresql import UUID
from backend.data.trading_base import TradingBase  # Importing the correct base
import uuid


class Trade(TradingBase):
    __tablename__ = "trades"

    trade_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    stock_symbol = Column(String(10), nullable=False)
    trade_type = Column(String(10), nullable=False)  # Buy/Sell
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    executed_at = Column(TIMESTAMP, server_default="NOW()")
