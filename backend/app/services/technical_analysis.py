"""
Services for technical analysis and calculations
"""
import numpy as np
from typing import List, Tuple


class TechnicalAnalysisService:
    """Service for calculating technical indicators"""
    
    @staticmethod
    def calculate_moving_average(prices: List[float], period: int) -> float:
        """
        Calculate simple moving average
        
        Args:
            prices: List of prices in chronological order
            period: Period for MA (e.g., 50, 200)
            
        Returns:
            Moving average value
        """
        if not prices or len(prices) < period:
            return None
        
        prices_array = np.array(prices[-period:])
        return float(np.mean(prices_array))
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> float:
        """
        Calculate Relative Strength Index (RSI)
        
        RSI ranges from 0-100:
        - Below 30: Oversold (potential buy)
        - Above 70: Overbought (potential sell)
        - 30-70: Normal range
        
        Args:
            prices: List of prices in chronological order
            period: Period for RSI calculation (default 14)
            
        Returns:
            RSI value (0-100)
        """
        if not prices or len(prices) < period + 1:
            return None
        
        prices_array = np.array(prices)
        
        # Calculate changes
        deltas = np.diff(prices_array)
        seed = deltas[:period+1]
        
        # Separate gains and losses
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        
        rs = up / down if down != 0 else 0
        rsi = 100 - 100 / (1 + rs)
        
        # Calculate RSI for remaining prices
        for i in range(period, len(deltas)):
            delta = deltas[i]
            if delta > 0:
                up_change = delta
                down_change = 0
            else:
                up_change = 0
                down_change = -delta
            
            up = (up * (period - 1) + up_change) / period
            down = (down * (period - 1) + down_change) / period
            
            rs = up / down if down != 0 else 0
            rsi = 100 - 100 / (1 + rs)
        
        return float(rsi)
    
    @staticmethod
    def calculate_volume_trend(volumes: List[int]) -> str:
        """
        Determine volume trend
        
        Args:
            volumes: List of volumes in chronological order
            
        Returns:
            'high', 'normal', or 'low'
        """
        if not volumes or len(volumes) < 10:
            return "neutral"
        
        recent_volume = np.mean(volumes[-5:])
        average_volume = np.mean(volumes[-10:])
        
        ratio = recent_volume / average_volume if average_volume > 0 else 1
        
        if ratio > 1.2:
            return "high"
        elif ratio < 0.8:
            return "low"
        else:
            return "normal"
    
    @staticmethod
    def calculate_analysis_score(
        current_price: float,
        ma_50: float,
        ma_200: float,
        rsi: float,
        volume_trend: str
    ) -> Tuple[float, str]:
        """
        Calculate investment score and recommendation
        
        Score: 0-4 (4 = Strong Buy, 2-3 = Watch, 0-1 = Avoid)
        
        Args:
            current_price: Current stock price
            ma_50: 50-day moving average
            ma_200: 200-day moving average
            rsi: RSI value (0-100)
            volume_trend: Volume trend ('high', 'normal', 'low')
            
        Returns:
            Tuple of (score, recommendation)
        """
        score = 0.0
        
        # Price vs MA indicators
        if current_price and ma_50 and ma_200:
            if current_price > ma_50 > ma_200:
                score += 1.5  # Strong uptrend
            elif current_price > ma_50:
                score += 0.75
            elif current_price > ma_200:
                score += 0.5
            
            # Golden cross or death cross
            if ma_50 > ma_200:
                score += 0.5
        
        # RSI signals
        if rsi:
            if rsi < 30:
                score += 1.0  # Oversold - potential buy
            elif rsi < 40:
                score += 0.5
            elif rsi > 70:
                score -= 0.5  # Overbought
            elif rsi > 60:
                score -= 0.25
        
        # Volume trend
        if volume_trend == "high":
            score += 0.5
        elif volume_trend == "low":
            score -= 0.25
        
        # Cap score at 4
        score = min(max(score, 0), 4)
        
        # Determine recommendation
        if score >= 3.5:
            recommendation = "strong_buy"
        elif score >= 2.5:
            recommendation = "buy"
        elif score >= 1.5:
            recommendation = "watch"
        elif score >= 0.5:
            recommendation = "sell"
        else:
            recommendation = "strong_sell"
        
        return score, recommendation
