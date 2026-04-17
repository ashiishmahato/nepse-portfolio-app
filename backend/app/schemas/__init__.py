"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Stock Schemas
class StockBase(BaseModel):
    """Base stock schema"""
    symbol: str
    name: str
    sector: Optional[str] = None


class StockCreate(StockBase):
    """Schema for creating a stock"""
    pass


class StockUpdate(BaseModel):
    """Schema for updating stock technical data"""
    current_price: Optional[float] = None
    ma_50: Optional[float] = None
    ma_200: Optional[float] = None
    rsi: Optional[float] = None
    volume_trend: Optional[str] = None
    analysis_score: Optional[float] = None
    analysis_recommendation: Optional[str] = None


class StockResponse(StockBase):
    """Response schema for stock"""
    current_price: float
    ma_50: Optional[float]
    ma_200: Optional[float]
    rsi: Optional[float]
    analysis_score: float
    analysis_recommendation: str
    volume_trend: str
    recent_high: Optional[float]
    high_52w: Optional[float]
    low_52w: Optional[float]
    last_update: datetime
    
    class Config:
        from_attributes = True


# Portfolio Schemas
class PortfolioCreate(BaseModel):
    """Schema for creating portfolio entry"""
    stock_symbol: str
    buy_price: float = Field(gt=0, description="Buy price must be positive")
    quantity: int = Field(gt=0, description="Quantity must be positive")
    target_profit_percentage: float = Field(gt=0, description="Target profit % must be positive")
    stop_loss_percentage: Optional[float] = Field(default=None, gt=0, lt=100)
    notes: Optional[str] = None


class PortfolioUpdate(BaseModel):
    """Schema for updating portfolio entry"""
    target_profit_percentage: Optional[float] = None
    stop_loss_percentage: Optional[float] = None
    notes: Optional[str] = None


class PortfolioResponse(BaseModel):
    """Response schema for portfolio"""
    id: int
    stock_symbol: str
    buy_price: float
    quantity: int
    target_profit_percentage: float
    stop_loss_percentage: Optional[float]
    total_invested: float
    current_value: float
    profit_loss: float
    profit_loss_percentage: float
    is_sold: int
    sell_price: Optional[float]
    sell_date: Optional[datetime]
    purchase_date: datetime
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Alert Schemas
class AlertResponse(BaseModel):
    """Response schema for alert"""
    id: int
    stock_symbol: str
    alert_type: str
    title: str
    description: str
    current_price: float
    trigger_price: float
    is_active: int
    is_notified: int
    created_at: datetime
    notified_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Price History Schemas
class PriceHistoryResponse(BaseModel):
    """Response schema for price history"""
    id: int
    stock_symbol: str
    date: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    
    class Config:
        from_attributes = True


# Dashboard Summary Schema
class DashboardSummary(BaseModel):
    """Dashboard summary response"""
    total_invested: float
    total_current_value: float
    total_profit_loss: float
    total_profit_loss_percentage: float
    portfolio_count: int
    active_alerts_count: int
    top_stocks: list = []
    recent_alerts: list = []
    portfolio_items: list = []
