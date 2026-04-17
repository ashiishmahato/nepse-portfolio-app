"""
Chart generation service for price visualization
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import PriceHistory
import logging
import os

logger = logging.getLogger(__name__)

CHART_OUTPUT_DIR = "charts"
if not os.path.exists(CHART_OUTPUT_DIR):
    os.makedirs(CHART_OUTPUT_DIR)


class ChartService:
    """Service for generating price charts"""
    
    @staticmethod
    def generate_price_chart(db: Session, symbol: str, days: int = 60) -> str:
        """
        Generate a price chart for a stock
        Returns the file path of the generated chart
        """
        try:
            # Get price history
            price_history = db.query(PriceHistory).filter(
                PriceHistory.stock_symbol == symbol,
                PriceHistory.date >= datetime.utcnow() - timedelta(days=days)
            ).order_by(PriceHistory.date).all()
            
            if not price_history:
                logger.warning(f"No price history found for {symbol}")
                return None
            
            # Prepare data
            dates = [ph.date for ph in price_history]
            close_prices = [ph.close_price for ph in price_history]
            high_prices = [ph.high_price for ph in price_history]
            low_prices = [ph.low_price for ph in price_history]
            
            # Create figure with subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})
            fig.patch.set_facecolor('#1e1e1e')
            
            # Price chart
            ax1.plot(dates, close_prices, label='Close Price', color='#00FF00', linewidth=2)
            ax1.fill_between(dates, low_prices, high_prices, alpha=0.2, color='#00FF00')
            ax1.set_title(f'{symbol} - Price Chart (Last {days} Days)', color='white', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Price (Rs.)', color='white')
            ax1.legend(loc='upper left', facecolor='#1e1e1e', edgecolor='white')
            ax1.grid(True, alpha=0.3, color='gray')
            ax1.set_facecolor('#2d2d2d')
            ax1.tick_params(colors='white')
            
            # Volume chart (approximate based on price range)
            price_range = max(close_prices) - min(close_prices)
            volumes = [price_range * (p - min(close_prices)) / price_range for p in close_prices]
            ax2.bar(dates, volumes, color='#3498db', alpha=0.7)
            ax2.set_xlabel('Date', color='white')
            ax2.set_ylabel('Volume (approx)', color='white')
            ax2.set_facecolor('#2d2d2d')
            ax2.tick_params(colors='white')
            ax2.grid(True, alpha=0.3, color='gray', axis='y')
            
            # Format x-axis
            for ax in [ax1, ax2]:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
                ax.xaxis.set_major_locator(mdates.AutoDateLocator())
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            
            # Save figure
            filename = f"{CHART_OUTPUT_DIR}/{symbol}_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.tight_layout()
            plt.savefig(filename, facecolor='#1e1e1e', edgecolor='none', dpi=100)
            plt.close()
            
            logger.info(f"Chart generated for {symbol}: {filename}")
            return filename
        
        except Exception as e:
            logger.error(f"Error generating chart for {symbol}: {str(e)}")
            return None
    
    @staticmethod
    def generate_summary_text(price_history):
        """Generate text summary of price trends"""
        if not price_history or len(price_history) < 2:
            return ""
        
        first_price = price_history[0].close_price
        last_price = price_history[-1].close_price
        min_price = min([ph.close_price for ph in price_history])
        max_price = max([ph.close_price for ph in price_history])
        
        change = last_price - first_price
        change_pct = (change / first_price * 100) if first_price > 0 else 0
        
        summary = f"""
<b>📊 PRICE SUMMARY:</b>
• Period: {len(price_history)} days
• Opening: Rs. {first_price:.2f}
• Closing: Rs. {last_price:.2f}
• Change: {change:+.2f} ({change_pct:+.2f}%)
• High: Rs. {max_price:.2f}
• Low: Rs. {min_price:.2f}
• Range: Rs. {max_price - min_price:.2f}
        """
        return summary
