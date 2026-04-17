"""
Notification service for sending alerts via email and Telegram
"""
import requests
import logging
from datetime import datetime, time

logger = logging.getLogger(__name__)

# NEPSE Market Hours (Nepal Standard Time - NST)
NEPSE_MARKET_HOURS = {
    "open_time": time(10, 0),  # 10:00 AM NST
    "close_time": time(15, 0),  # 3:00 PM NST
    "timezone": "NST (UTC+5:45)"
}


def get_market_status():
    """Get current NEPSE market status"""
    now = datetime.now().time()
    if NEPSE_MARKET_HOURS["open_time"] <= now < NEPSE_MARKET_HOURS["close_time"]:
        return "🟢 LIVE"
    else:
        return "🔴 CLOSED"


def format_price_change(current_price, previous_price):
    """Format price change with percentage"""
    if previous_price <= 0:
        return ""
    
    change = current_price - previous_price
    change_pct = (change / previous_price) * 100
    
    if change >= 0:
        emoji = "📈"
        return f"{emoji} +Rs. {change:.2f} (+{change_pct:.2f}%)"
    else:
        emoji = "📉"
        return f"{emoji} -Rs. {abs(change):.2f} ({change_pct:.2f}%)"


class EmailNotificationService:
    """Service for sending email alerts"""
    
    def __init__(self, smtp_server, smtp_port, email, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
    
    def send_alert(self, recipient, subject, message):
        """Send email alert"""
        # TODO: Implement email sending
        # import smtplib
        # from email.mime.text import MIMEText
        pass


class TelegramNotificationService:
    """Service for sending Telegram alerts"""
    
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
    
    def send_alert(self, message):
        """Send Telegram alert"""
        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram credentials not configured, skipping notification")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"Telegram alert sent successfully: {message[:50]}...")
                return True
            else:
                logger.error(f"Failed to send Telegram alert: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error sending Telegram alert: {str(e)}")
            return False
    
    def send_alert_with_chart(self, message, chart_file_path=None):
        """Send Telegram alert with optional chart image"""
        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram credentials not configured, skipping notification")
            return False
        
        try:
            # First, send the text message
            self.send_alert(message)
            
            # If chart file exists, send it as a photo
            if chart_file_path:
                try:
                    url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
                    with open(chart_file_path, 'rb') as photo:
                        files = {'photo': photo}
                        data = {'chat_id': self.chat_id}
                        response = requests.post(url, files=files, data=data, timeout=10)
                    
                    if response.status_code == 200:
                        logger.info("Chart sent to Telegram successfully")
                        return True
                except Exception as e:
                    logger.warning(f"Could not send chart: {str(e)}")
            
            return True
        except Exception as e:
            logger.error(f"Error sending Telegram alert with chart: {str(e)}")
            return False


class NotificationManager:
    """Manager for sending notifications through multiple channels"""
    
    def __init__(self, email_service=None, telegram_service=None):
        self.email_service = email_service
        self.telegram_service = telegram_service
    
    @staticmethod
    def format_alert_message(alert_data):
        """Format alert with detailed information"""
        
        message = f"""
<b>{alert_data.get('title', 'Alert')}</b>

📊 <b>Market Status:</b> {get_market_status()}
🕐 <b>Market Hours:</b> {NEPSE_MARKET_HOURS['open_time'].strftime('%H:%M')} - {NEPSE_MARKET_HOURS['close_time'].strftime('%H:%M')} {NEPSE_MARKET_HOURS['timezone']}

━━━━━━━━━━━━━━━━━━
<b>STOCK DETAILS</b>
━━━━━━━━━━━━━━━━━━

📈 <b>Symbol:</b> {alert_data.get('stock_symbol', 'N/A')}
💵 <b>Current Price:</b> Rs. {alert_data.get('current_price', 'N/A'):.2f}
🎯 <b>Trigger Price:</b> Rs. {alert_data.get('trigger_price', 'N/A'):.2f}

<b>Price Change Today:</b>
{alert_data.get('price_change', 'N/A')}

━━━━━━━━━━━━━━━━━━
<b>TECHNICAL ANALYSIS</b>
━━━━━━━━━━━━━━━━━━

📊 <b>RSI:</b> {alert_data.get('rsi', 'N/A')}
📈 <b>MA50:</b> Rs. {alert_data.get('ma_50', 'N/A')}
📈 <b>MA200:</b> Rs. {alert_data.get('ma_200', 'N/A')}
📊 <b>Volume Trend:</b> {alert_data.get('volume_trend', 'N/A')}
💡 <b>Recommendation:</b> {alert_data.get('recommendation', 'N/A')}
🎯 <b>Analysis Score:</b> {alert_data.get('analysis_score', 'N/A')}/100

━━━━━━━━━━━━━━━━━━
<b>ALERT DETAILS</b>
━━━━━━━━━━━━━━━━━━

🏷️ <b>Type:</b> {alert_data.get('alert_type', 'N/A')}
📝 <b>Description:</b> {alert_data.get('description', '')}

<i>52-Week High:</i> Rs. {alert_data.get('high_52w', 'N/A')}
<i>52-Week Low:</i> Rs. {alert_data.get('low_52w', 'N/A')}

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} NST
        """
        return message
    
    def notify_alert(self, alert, send_email=False, send_telegram=False):
        """Send alert through configured channels"""
        message = self.format_alert_message(alert)
        
        if send_email and self.email_service:
            self.email_service.send_alert("user@example.com", alert['title'], message)
        
        if send_telegram and self.telegram_service:
            return self.telegram_service.send_alert(message)
        
        return True
