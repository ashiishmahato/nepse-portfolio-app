"""
Alert model for storing generated alerts
"""
from sqlalchemy import Column, String, Float, Integer, DateTime, func
from datetime import datetime
from app.database import Base


class Alert(Base):
    """Alert model for tracking generated alerts"""
    __tablename__ = "alerts"
    
    # Columns
    id = Column(Integer, primary_key=True, index=True)
    stock_symbol = Column(String, index=True)
    alert_type = Column(String)  # sell_target, buy_dip, stop_loss, rsi_signal, ma_crossover
    title = Column(String)
    description = Column(String)
    current_price = Column(Float)
    trigger_price = Column(Float)
    
    # Status
    is_active = Column(Integer, default=1)
    is_notified = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    notified_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Alert(symbol={self.stock_symbol}, type={self.alert_type}, id={self.id})>"
