"""
Stock model for storing stock information
"""
from sqlalchemy import Column, String, Float, Integer, DateTime, func
from datetime import datetime
from app.database import Base


class Stock(Base):
    """Stock information model"""
    __tablename__ = "stocks"
    
    # Columns
    symbol = Column(String, primary_key=True, index=True)  # NABIL, NNPL, etc.
    name = Column(String, nullable=False)  # Full stock name
    sector = Column(String)  # Banking, Insurance, etc.
    current_price = Column(Float, default=0.0)  # Current market price
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Technical Analysis
    ma_50 = Column(Float, nullable=True)  # 50-day moving average
    ma_200 = Column(Float, nullable=True)  # 200-day moving average
    rsi = Column(Float, nullable=True)  # Relative Strength Index (0-100)
    volume_trend = Column(String, default="neutral")  # high, normal, low
    
    # Analysis Score (0-4)
    analysis_score = Column(Float, default=0.0)
    analysis_recommendation = Column(String, default="watch")  # strong_buy, buy, watch, sell, strong_sell
    
    # Historical data
    high_52w = Column(Float, nullable=True)  # 52-week high
    low_52w = Column(Float, nullable=True)  # 52-week low
    recent_high = Column(Float, nullable=True)  # Recent high price
    
    def __repr__(self):
        return f"<Stock(symbol={self.symbol}, name={self.name}, price={self.current_price})>"
