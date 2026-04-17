"""
Services for stock data and price management
"""
from sqlalchemy.orm import Session
from app.models import Stock, Portfolio, PriceHistory, Alert
from app.services.technical_analysis import TechnicalAnalysisService
from datetime import datetime, timedelta
import random


class StockService:
    """Service for managing stock data"""
    
    @staticmethod
    def get_or_create_stock(db: Session, symbol: str, name: str, sector: str = None) -> Stock:
        """Get existing stock or create new one"""
        stock = db.query(Stock).filter(Stock.symbol == symbol).first()
        if not stock:
            stock = Stock(symbol=symbol, name=name, sector=sector)
            db.add(stock)
            db.commit()
            db.refresh(stock)
        return stock
    
    @staticmethod
    def update_stock_price(db: Session, symbol: str, price: float) -> Stock:
        """Update stock current price"""
        stock = db.query(Stock).filter(Stock.symbol == symbol).first()
        if stock:
            stock.current_price = price
            stock.last_update = datetime.utcnow()
            
            # Update recent high
            if not stock.recent_high or price > stock.recent_high:
                stock.recent_high = price
            
            db.commit()
            db.refresh(stock)
        return stock
    
    @staticmethod
    def calculate_and_update_analysis(db: Session, symbol: str) -> Stock:
        """Calculate technical analysis and update stock"""
        stock = db.query(Stock).filter(Stock.symbol == symbol).first()
        if not stock:
            return None
        
        # Get price history for the last 200 days
        price_history = db.query(PriceHistory).filter(
            PriceHistory.stock_symbol == symbol
        ).order_by(PriceHistory.date).all()
        
        if not price_history or len(price_history) < 50:
            # Not enough data
            return stock
        
        close_prices = [ph.close_price for ph in price_history]
        volumes = [ph.volume for ph in price_history]
        
        # Calculate indicators
        ma_50 = TechnicalAnalysisService.calculate_moving_average(close_prices, 50)
        ma_200 = TechnicalAnalysisService.calculate_moving_average(close_prices, 200)
        rsi = TechnicalAnalysisService.calculate_rsi(close_prices, 14)
        volume_trend = TechnicalAnalysisService.calculate_volume_trend(volumes)
        
        # Update stock
        stock.ma_50 = ma_50
        stock.ma_200 = ma_200
        stock.rsi = rsi
        stock.volume_trend = volume_trend
        
        # Calculate score and recommendation
        score, recommendation = TechnicalAnalysisService.calculate_analysis_score(
            stock.current_price, ma_50, ma_200, rsi, volume_trend
        )
        
        stock.analysis_score = score
        stock.analysis_recommendation = recommendation
        stock.high_52w = max(close_prices)
        stock.low_52w = min(close_prices)
        
        db.commit()
        db.refresh(stock)
        return stock


class PortfolioService:
    """Service for managing user portfolio"""
    
    @staticmethod
    def get_dashboard_summary(db: Session) -> dict:
        """Get dashboard summary for all holdings"""
        portfolio_items = db.query(Portfolio).filter(Portfolio.is_sold == 0).all()
        
        total_invested = 0
        total_current_value = 0
        profit_loss_list = []
        
        for item in portfolio_items:
            total_invested += item.total_invested
            total_current_value += item.current_value
            profit_loss_list.append(item.profit_loss)
        
        total_profit_loss = sum(profit_loss_list)
        total_profit_loss_pct = (
            (total_profit_loss / total_invested * 100) if total_invested > 0 else 0
        )
        
        # Get active alerts
        active_alerts = db.query(Alert).filter(Alert.is_active == 1).all()
        
        summary = {
            "total_invested": round(total_invested, 2),
            "total_current_value": round(total_current_value, 2),
            "total_profit_loss": round(total_profit_loss, 2),
            "total_profit_loss_percentage": round(total_profit_loss_pct, 2),
            "portfolio_count": len(portfolio_items),
            "active_alerts_count": len(active_alerts),
        }
        
        return summary
    
    @staticmethod
    def update_portfolio_values(db: Session):
        """Update all portfolio item values based on current stock prices"""
        portfolio_items = db.query(Portfolio).filter(Portfolio.is_sold == 0).all()
        
        for item in portfolio_items:
            stock = db.query(Stock).filter(Stock.symbol == item.stock_symbol).first()
            if stock:
                item.current_value = stock.current_price * item.quantity
                item.profit_loss = item.current_value - item.total_invested
                item.profit_loss_percentage = (
                    (item.profit_loss / item.total_invested * 100) if item.total_invested > 0 else 0
                )
                item.updated_at = datetime.utcnow()
        
        db.commit()


class AlertService:
    """Service for managing and generating alerts"""
    
    @staticmethod
    def generate_alerts(db: Session):
        """Generate alerts based on portfolio and technical conditions"""
        portfolio_items = db.query(Portfolio).filter(Portfolio.is_sold == 0).all()
        
        for item in portfolio_items:
            stock = db.query(Stock).filter(Stock.symbol == item.stock_symbol).first()
            if not stock:
                continue
            
            current_price = stock.current_price
            
            # Profit target alert
            target_price = item.buy_price * (1 + item.target_profit_percentage / 100)
            if current_price >= target_price:
                # Check if alert already exists
                existing_alert = db.query(Alert).filter(
                    Alert.stock_symbol == item.stock_symbol,
                    Alert.alert_type == "sell_target",
                    Alert.is_active == 1
                ).first()
                
                if not existing_alert:
                    alert = Alert(
                        stock_symbol=item.stock_symbol,
                        alert_type="sell_target",
                        title=f"🎯 Sell Target Reached: {item.stock_symbol}",
                        description=f"Your target profit of {item.target_profit_percentage}% has been reached!",
                        current_price=current_price,
                        trigger_price=target_price,
                        is_active=1
                    )
                    db.add(alert)
            
            # Buy dip alert
            if stock.recent_high:
                dip_threshold = stock.recent_high * 0.85  # 15% below recent high
                if current_price <= dip_threshold:
                    existing_alert = db.query(Alert).filter(
                        Alert.stock_symbol == item.stock_symbol,
                        Alert.alert_type == "buy_dip",
                        Alert.is_active == 1
                    ).first()
                    
                    if not existing_alert:
                        alert = Alert(
                            stock_symbol=item.stock_symbol,
                            alert_type="buy_dip",
                            title=f"💰 Buy Dip Opportunity: {item.stock_symbol}",
                            description=f"Stock is down 15% from recent high. Good buying opportunity!",
                            current_price=current_price,
                            trigger_price=dip_threshold,
                            is_active=1
                        )
                        db.add(alert)
            
            # Stop loss alert
            if item.stop_loss_percentage:
                stop_loss_price = item.buy_price * (1 - item.stop_loss_percentage / 100)
                if current_price <= stop_loss_price:
                    existing_alert = db.query(Alert).filter(
                        Alert.stock_symbol == item.stock_symbol,
                        Alert.alert_type == "stop_loss",
                        Alert.is_active == 1
                    ).first()
                    
                    if not existing_alert:
                        alert = Alert(
                            stock_symbol=item.stock_symbol,
                            alert_type="stop_loss",
                            title=f"⛔ Stop Loss Triggered: {item.stock_symbol}",
                            description=f"Your stop loss of {item.stop_loss_percentage}% has been triggered!",
                            current_price=current_price,
                            trigger_price=stop_loss_price,
                            is_active=1
                        )
                        db.add(alert)
            
            # RSI signals
            if stock.rsi:
                if stock.rsi > 70:
                    existing_alert = db.query(Alert).filter(
                        Alert.stock_symbol == item.stock_symbol,
                        Alert.alert_type == "rsi_signal",
                        Alert.is_active == 1
                    ).first()
                    
                    if not existing_alert:
                        alert = Alert(
                            stock_symbol=item.stock_symbol,
                            alert_type="rsi_signal",
                            title=f"📊 RSI Overbought: {item.stock_symbol}",
                            description=f"RSI is above 70 (overbought). Consider taking profits.",
                            current_price=current_price,
                            trigger_price=current_price,
                            is_active=1
                        )
                        db.add(alert)
        
        db.commit()
    
    @staticmethod
    def deactivate_expired_alerts(db: Session):
        """Deactivate old alerts that are no longer relevant"""
        old_alerts = db.query(Alert).filter(
            Alert.is_active == 1,
            Alert.created_at < datetime.utcnow() - timedelta(days=7)
        ).all()
        
        for alert in old_alerts:
            alert.is_active = 0
        
        db.commit()
