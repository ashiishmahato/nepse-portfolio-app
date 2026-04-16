"""
Notification service for sending alerts via email and Telegram
"""
import requests
import logging

logger = logging.getLogger(__name__)


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
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info(f"Telegram notification sent successfully")
                return True
            else:
                logger.error(f"Failed to send Telegram notification: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error sending Telegram notification: {str(e)}")
            return False


class NotificationManager:
    """Manager for sending notifications through multiple channels"""
    
    def __init__(self, email_service=None, telegram_service=None):
        self.email_service = email_service
        self.telegram_service = telegram_service
    
    def notify_alert(self, alert, send_email=False, send_telegram=False):
        """Send alert through configured channels"""
        
        message = f"""
        {alert['title']}
        
        Stock: {alert['stock_symbol']}
        Type: {alert['alert_type']}
        Current Price: {alert['current_price']}
        Trigger Price: {alert['trigger_price']}
        
        {alert['description']}
        """
        
        if send_email and self.email_service:
            self.email_service.send_alert("user@example.com", alert['title'], message)
        
        if send_telegram and self.telegram_service:
            self.telegram_service.send_alert(message)
