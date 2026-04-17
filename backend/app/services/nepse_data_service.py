"""
Service for fetching real NEPSE data from Official NEPSE API
"""
import logging
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class NepseDataService:
    """Service to interact with official NEPSE API for real NEPSE data"""
    
    # Timeout for API calls
    TIMEOUT = 30
    
    @staticmethod
    def get_all_stocks() -> List[Dict[str, Any]]:
        """
        Fetch all NEPSE stocks from the official NEPSE API
        Returns all available companies listed on NEPSE with real data
        """
        try:
            logger.info("Fetching stocks from official NEPSE API...")
            
            # Try to use official nepse-api library
            try:
                from nepse import SecurityClient
                
                async def fetch_stocks():
                    client = SecurityClient()
                    securities = await client.get_all_securities()
                    return securities
                
                # Run async function in sync context
                import nest_asyncio
                nest_asyncio.apply()
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                securities = loop.run_until_complete(fetch_stocks())
                logger.info(f"Successfully fetched {len(securities)} securities from official API")
                
                # Convert to expected format
                companies = []
                for sec in securities:
                    companies.append({
                        'symbol': sec.symbol,
                        'name': sec.name,
                        'sector': getattr(sec, 'industry', 'Unknown'),
                        'ltp': float(getattr(sec, 'ltp', 0) or 0)
                    })
                return companies
                
            except ImportError:
                logger.warning("nepse-api not installed, falling back to requests API")
                return NepseDataService._get_stocks_from_requests()
                
        except Exception as e:
            logger.error(f"Error fetching from official API: {str(e)}")
            logger.info("Falling back to requests-based API")
            return NepseDataService._get_stocks_from_requests()
    
    @staticmethod
    def _get_stocks_from_requests() -> List[Dict[str, Any]]:
        """Fallback method using requests library"""
        import requests
        
        try:
            # Try primary endpoint first
            url = "https://nepseapi.surajrimal.dev/CompanyList"
            response = requests.get(url, timeout=NepseDataService.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            companies = []
            
            # Handle different response formats
            if isinstance(data, list):
                companies = data
            elif isinstance(data, dict) and 'data' in data:
                companies = data['data']
            
            logger.info(f"Fetched {len(companies)} stocks from fallback API")
            return companies
            
        except Exception as e:
            logger.error(f"Error fetching stocks: {str(e)}")
            return []
    
    @classmethod
    def get_price_volume(cls) -> Dict[str, Dict[str, Any]]:
        """
        Fetch price and volume data for all stocks
        """
        try:
            url = f"{cls.BASE_URL}/PriceVolume"
            response = requests.get(url, headers=cls.get_headers(), timeout=cls.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Fetched price/volume data for {len(data)} stocks")
            return data
        except Exception as e:
            logger.error(f"Error fetching price volume data: {str(e)}")
            return {}
    
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
