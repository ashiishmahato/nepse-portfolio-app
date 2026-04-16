"""
Service for fetching REAL live NEPSE stock prices
Primary source: NepseClient (official NEPSE API wrapper)
Fallback: nepseapi.surajrimal.dev
"""
import logging
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# Try to import NepseClient service
try:
    from app.services.nepse_client_service import NepseClientService
    NEPSE_CLIENT_AVAILABLE = True
except ImportError:
    NEPSE_CLIENT_AVAILABLE = False
    logger.warning("NepseClient service not available")

class NepseDataService:
    """Service to fetch REAL live NEPSE data - prioritizing NepseClient"""
    
    TIMEOUT = 30
    
    @classmethod
    def get_all_stocks(cls) -> List[Dict[str, Any]]:
        """
        Fetch ALL real NEPSE stocks with LIVE prices
        Uses NepseClient as primary source
        """
        try:
            logger.info("Fetching REAL stocks from NEPSE...")
            
            # Try NepseClient first (most reliable)
            if NEPSE_CLIENT_AVAILABLE:
                stocks = NepseClientService.get_all_stocks()
                if stocks:
                    logger.info(f"✅ Fetched {len(stocks)} REAL stocks using NepseClient")
                    return stocks
                else:
                    logger.warning("NepseClient returned no stocks, trying fallback...")
            
            # Fallback to old API
            logger.warning("Using fallback API for stock data...")
            return cls._get_stocks_fallback()
                
        except Exception as e:
            logger.error(f"Error in get_all_stocks: {str(e)}")
            return cls._get_stocks_fallback()
    
    @classmethod
    def _get_stocks_fallback(cls) -> List[Dict[str, Any]]:
        """Fallback method if NepseClient is unavailable"""
        try:
            logger.info("Using fallback API: nepseapi.surajrimal.dev...")
            url = "https://nepseapi.surajrimal.dev/CompanyList"
            response = requests.get(url, timeout=cls.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            companies = []
            
            if isinstance(data, list):
                companies = data
            elif isinstance(data, dict) and 'data' in data:
                companies = data['data'] if isinstance(data['data'], list) else [data['data']]
            
            logger.info(f"Fetched {len(companies)} stocks from fallback API")
            return companies
            
        except Exception as e:
            logger.error(f"Error with fallback API: {str(e)}")
            return []
    
    @classmethod
    def get_price_volume(cls) -> Dict[str, Any]:
        """
        Fetch price and volume data for all stocks
        """
        try:
            if NEPSE_CLIENT_AVAILABLE:
                price_vol = NepseClientService.get_price_volume()
                if price_vol:
                    logger.info(f"Fetched price/volume for {len(price_vol)} stocks from NepseClient")
                    return price_vol
            
            # Fallback
            url = "https://nepseapi.surajrimal.dev/PriceVolume"
            response = requests.get(url, timeout=cls.TIMEOUT)
            response.raise_for_status()
            return response.json()
                
        except Exception as e:
            logger.error(f"Error fetching price volume data: {str(e)}")
            return {}
    
    @classmethod
    def get_live_market(cls) -> Dict[str, Any]:
        """
        Fetch live market data
        """
        try:
            url = "https://nepseapi.surajrimal.dev/LiveMarket"
            response = requests.get(url, timeout=cls.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            return data
        except Exception as e:
            logger.error(f"Error fetching live market data: {str(e)}")
            return {}
    
    @classmethod
    def get_market_summary(cls) -> Optional[Dict[str, Any]]:
        """
        Fetch market summary
        """
        try:
            if NEPSE_CLIENT_AVAILABLE:
                summary = NepseClientService.get_market_summary()
                if summary:
                    logger.info("Got market summary from NepseClient")
                    return summary
            
            # Fallback
            url = "https://nepseapi.surajrimal.dev/Summary"
            response = requests.get(url, timeout=cls.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            return data
        except Exception as e:
            logger.error(f"Error fetching market summary: {str(e)}")
            return None
    
    @classmethod
    def get_top_gainers(cls, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch top gaining stocks
        """
        try:
            if NEPSE_CLIENT_AVAILABLE:
                gainers = NepseClientService.get_top_gainers(limit)
                if gainers:
                    logger.info(f"Got top {len(gainers)} gainers from NepseClient")
                    return gainers
            
            # Fallback
            url = "https://nepseapi.surajrimal.dev/TopGainers"
            response = requests.get(url, timeout=cls.TIMEOUT)
            response.raise_for_status()
            
            gainers = response.json()
            return gainers[:limit]
        except Exception as e:
            logger.error(f"Error fetching top gainers: {str(e)}")
            return []
    
    @classmethod
    def get_top_losers(cls, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch top losing stocks
        """
        try:
            if NEPSE_CLIENT_AVAILABLE:
                losers = NepseClientService.get_top_losers(limit)
                if losers:
                    logger.info(f"Got top {len(losers)} losers from NepseClient")
                    return losers
            
            # Fallback
            url = "https://nepseapi.surajrimal.dev/TopLosers"
            response = requests.get(url, timeout=cls.TIMEOUT)
            response.raise_for_status()
            
            losers = response.json()
            return losers[:limit]
        except Exception as e:
            logger.error(f"Error fetching top losers: {str(e)}")
            return []
                
        except Exception as e:
            logger.error(f"Error fetching price volume data: {str(e)}")
            return {}
    
    @classmethod
    def get_live_market(cls) -> Dict[str, Any]:
        """
        Fetch live market data
        """
        try:
            url = "https://nepseapi.surajrimal.dev/LiveMarket"
            response = requests.get(url, timeout=cls.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            return data
        except Exception as e:
            logger.error(f"Error fetching live market data: {str(e)}")
            return {}
    
    @classmethod
    def get_market_summary(cls) -> Optional[Dict[str, Any]]:
        """
        Fetch market summary
        """
        try:
            url = "https://nepseapi.surajrimal.dev/Summary"
            response = requests.get(url, timeout=cls.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            return data
        except Exception as e:
            logger.error(f"Error fetching market summary: {str(e)}")
            return None
    
    @classmethod
    def get_top_gainers(cls, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch top gaining stocks
        """
        try:
            url = "https://nepseapi.surajrimal.dev/TopGainers"
            response = requests.get(url, timeout=cls.TIMEOUT)
            response.raise_for_status()
            
            gainers = response.json()
            return gainers[:limit]
        except Exception as e:
            logger.error(f"Error fetching top gainers: {str(e)}")
            return []
    
    @classmethod
    def get_top_losers(cls, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch top losing stocks
        """
        try:
            url = "https://nepseapi.surajrimal.dev/TopLosers"
            response = requests.get(url, timeout=cls.TIMEOUT)
            response.raise_for_status()
            
            losers = response.json()
            return losers[:limit]
        except Exception as e:
            logger.error(f"Error fetching top losers: {str(e)}")
            return []
    
    @classmethod
    def get_live_market(cls) -> Dict[str, Any]:
        """
        Fetch live market data
        """
        try:
            url = f"{cls.BASE_URL}/LiveMarket"
            response = requests.get(url, headers=cls.get_headers(), timeout=cls.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            return data
        except Exception as e:
            logger.error(f"Error fetching live market data: {str(e)}")
            return {}
    
    @classmethod
    def get_market_summary(cls) -> Optional[Dict[str, Any]]:
        """
        Fetch market summary
        """
        try:
            url = f"{cls.BASE_URL}/Summary"
            response = requests.get(url, headers=cls.get_headers(), timeout=cls.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            return data
        except Exception as e:
            logger.error(f"Error fetching market summary: {str(e)}")
            return None
    
    @classmethod
    def get_top_gainers(cls, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch top gaining stocks
        """
        try:
            url = f"{cls.BASE_URL}/TopGainers"
            response = requests.get(url, headers=cls.get_headers(), timeout=cls.TIMEOUT)
            response.raise_for_status()
            
            gainers = response.json()
            return gainers[:limit]
        except Exception as e:
            logger.error(f"Error fetching top gainers: {str(e)}")
            return []
    
    @classmethod
    def get_top_losers(cls, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch top losing stocks
        """
        try:
            url = f"{cls.BASE_URL}/TopLosers"
            response = requests.get(url, headers=cls.get_headers(), timeout=cls.TIMEOUT)
            response.raise_for_status()
            
            losers = response.json()
            return losers[:limit]
        except Exception as e:
            logger.error(f"Error fetching top losers: {str(e)}")
            return []
    
    @classmethod
    def sync_stocks_from_api(cls, session) -> int:
        """
        Sync stocks from NEPSE API into database
        
        Returns the number of stocks inserted/updated
        """
        from ..models.stock import Stock
        
        try:
            # Import here to avoid circular imports
            companies = cls.get_all_stocks()
            
            if not companies:
                logger.warning("No companies fetched from API")
                return 0
            
            price_volume = cls.get_price_volume()
            
            count = 0
            for company in companies:
                try:
                    symbol = company.get('symbol', '')
                    if not symbol:
                        continue
                    
                    # Get price and volume data
                    pv_data = price_volume.get(symbol, {})
                    
                    # Check if stock exists
                    existing_stock = session.query(Stock).filter_by(symbol=symbol).first()
                    
                    stock_data = {
                        'symbol': symbol,
                        'name': company.get('name', ''),
                        'sector': company.get('sector', 'Not Available'),
                        'current_price': float(pv_data.get('ltp', company.get('ltp', 0)) or 0),
                        'open_price': float(pv_data.get('open', 0) or 0),
                        'high_price': float(pv_data.get('high', 0) or 0),
                        'low_price': float(pv_data.get('low', 0) or 0),
                        'volume': int(pv_data.get('volume', 0) or 0),
                        'market_cap': float(company.get('market_cap', 0) or 0),
                        'pe_ratio': float(company.get('pe_ratio', 0) or 0),
                        'dividend_yield': float(company.get('dividend_yield', 0) or 0),
                    }
                    
                    if existing_stock:
                        # Update existing stock
                        for key, value in stock_data.items():
                            setattr(existing_stock, key, value)
                    else:
                        # Create new stock
                        new_stock = Stock(**stock_data)
                        session.add(new_stock)
                    
                    count += 1
                    
                except Exception as e:
                    logger.error(f"Error processing stock {symbol}: {str(e)}")
                    continue
            
            session.commit()
            logger.info(f"Successfully synced {count} stocks from NEPSE API")
            return count
            
        except Exception as e:
            logger.error(f"Error syncing stocks from API: {str(e)}")
            session.rollback()
            return 0
