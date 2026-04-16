"""
API routes for alert management
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AlertResponse
from app.models import Alert
from app.services.stock_service import AlertService
from app.services.notifications import TelegramNotificationService
from app.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/", response_model=list[AlertResponse])
def get_alerts(
    active_only: bool = True,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get alerts
    
    - **active_only**: Show only active alerts (default: True)
    - **limit**: Maximum number of alerts to return
    """
    query = db.query(Alert)
    
    if active_only:
        query = query.filter(Alert.is_active == 1)
    
    alerts = query.order_by(Alert.created_at.desc()).limit(limit).all()
    return alerts


@router.get("/by-stock/{symbol}", response_model=list[AlertResponse])
def get_alerts_for_stock(
    symbol: str,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get alerts for a specific stock"""
    query = db.query(Alert).filter(Alert.stock_symbol == symbol.upper())
    
    if active_only:
        query = query.filter(Alert.is_active == 1)
    
    alerts = query.order_by(Alert.created_at.desc()).all()
    return alerts


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """Get specific alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return alert


@router.put("/{alert_id}/mark-as-read")
def mark_alert_as_read(alert_id: int, db: Session = Depends(get_db)):
    """Mark alert as notified"""
    from datetime import datetime
    
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_notified = 1
    alert.notified_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Alert marked as read"}


@router.put("/{alert_id}/deactivate")
def deactivate_alert(alert_id: int, db: Session = Depends(get_db)):
    """Deactivate an alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_active = 0
    db.commit()
    
    return {"message": "Alert deactivated"}


@router.post("/generate")
def trigger_alert_generation(db: Session = Depends(get_db)):
    """
    Manually trigger alert generation
    (In production, this is called by scheduled task)
    """
    AlertService.generate_alerts(db)
    AlertService.deactivate_expired_alerts(db)
    
    return {"message": "Alerts generated successfully"}


@router.post("/test-telegram")
def test_telegram_notification():
    """
    Test Telegram notification - sends a test message to verify bot is working
    """
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        raise HTTPException(
            status_code=400,
            detail="Telegram credentials not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env"
        )
    
    telegram_service = TelegramNotificationService(
        settings.TELEGRAM_BOT_TOKEN,
        settings.TELEGRAM_CHAT_ID
    )
    
    test_message = """
<b>✅ Test Notification - DETAILED FORMAT</b>

Your NEPSE Alert Bot is working!

<b>🎯 SELL TARGET REACHED!</b>

<b>Stock:</b> ADBL
<b>Quantity:</b> 10 shares
<b>Buy Price:</b> NPR 378.91
<b>Current Price:</b> NPR 435.75
<b>Target Price:</b> NPR 435.76

<b>💰 PROFIT DETAILS:</b>
💵 Total Invested: NPR 3,789.10
📊 Current Value: NPR 4,357.50
✅ Profit: NPR 568.40
📈 Gain: <b>15.00%</b>
📅 Days Held: 45 days

<b>🎯 Target Profit:</b> 15%

📲 Consider selling to lock in profits!
"""
    
    success = telegram_service.send_alert(test_message)
    
    if success:
        return {"message": "Detailed test notification sent successfully! Check your Telegram.", "status": "success"}
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to send test notification. Check your bot token and chat ID."
        )
