"""
Service for fetching REAL live NEPSE stock prices using NepseClient library
This is the official, most reliable source for NEPSE data
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    from nepse_client import NepseClient
    NEPSE_CLIENT_AVAILABLE = True
except ImportError as e:
    NEPSE_CLIENT_AVAILABLE = False
    logger.warning(f"NepseClient not available - install with: pip install nepse-client (Error: {e})")

class NepseClientService:
    """Service to fetch REAL live NEPSE data using the official NepseClient library"""
    
    _client = None
    
    @classmethod
    def _get_client(cls):
        """Initialize NepseClient (singleton pattern)"""
        if cls._client is None and NEPSE_CLIENT_AVAILABLE:
            try:
                cls._client = NepseClient()
                # Disable SSL verification (for development/testing)
                try:
                    cls._client.setTLSVerification(False)
                    logger.warning("SSL verification disabled (for development only)")
                except:
                    pass
                logger.info("✅ NepseClient initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize NepseClient: {e}")
                return None
        return cls._client
    
    @classmethod
    def get_all_stocks(cls) -> List[Dict[str, Any]]:
        """
        Fetch ALL real NEPSE stocks with LIVE prices
        Uses getPriceVolume() which has real market data (269 stocks with active trading)
        """
        try:
            if not NEPSE_CLIENT_AVAILABLE:
                logger.warning("NepseClient not available")
                return []
            
            logger.info("Fetching REAL stocks from NEPSE using NepseClient...")
            
            client = cls._get_client()
            if not client:
                logger.error("Could not initialize NepseClient")
                return []
            
            # Get price/volume data - this has REAL live market prices
            price_volumes = client.getPriceVolume()
            
            if not price_volumes:
                logger.warning("No price/volume data returned from NepseClient")
                return []
            
            # Ensure it's a list
            if not isinstance(price_volumes, list):
                logger.warning(f"Unexpected type from getPriceVolume: {type(price_volumes)}")
                return []
            
            stocks = []
            for price_data in price_volumes:
                try:
                    symbol = price_data.get('symbol', '').upper()
                    if not symbol:
                        continue
                    
                    # Get the last traded price (current market price)
                    ltp = float(price_data.get('lastTradedPrice', 0))
                    
                    stock_data = {
                        'symbol': symbol,
                        'name': price_data.get('securityName', ''),
                        'ltp': ltp,
                        'current_price': ltp,
                        'last_traded_price': ltp,
                        'previous_close': float(price_data.get('previousClose', 0)),
                        'close_price': float(price_data.get('closePrice', 0)),
                        'volume': int(price_data.get('totalTradeQuantity', 0)),
                        'market_cap': price_data.get('marketCapitalization', 0),
                        'pe_ratio': price_data.get('pe', None),
                        'sector': price_data.get('sector', 'Unknown'),
                        'change': float(price_data.get('netChange', ltp - float(price_data.get('previousClose', 0)))),
                        'change_percent': float(price_data.get('percentageChange', 0)),
                        'security_id': price_data.get('securityId'),
                    }
                    stocks.append(stock_data)
                except (ValueError, KeyError, TypeError) as e:
                    logger.debug(f"Error processing stock data: {e}")
                    continue
            
            if stocks:
                logger.info(f"✅ Successfully fetched {len(stocks)} REAL stocks with LIVE prices from NEPSE")
                # Show a few examples
                for stock in stocks[:3]:
                    logger.debug(f"  {stock['symbol']:8} @ Rs. {stock['ltp']:.2f} ({stock['change_percent']:+.2f}%)")
            
            return stocks
            
        except Exception as e:
            logger.error(f"Error fetching stocks from NepseClient: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return []
    
    @classmethod
    def get_stock_price(cls, symbol: str) -> Optional[float]:
        """Fetch real price for a specific stock"""
        try:
            if not NEPSE_CLIENT_AVAILABLE:
                return None
            
            client = cls._get_client()
            if not client:
                return None
            
            logger.info(f"Fetching REAL price for {symbol}...")
            
            # Get details for the company
            company_details = client.getCompanyDetails(symbol.upper())
            
            if company_details:
                price = float(company_details.get('ltp', 0))
                if price > 0:
                    logger.info(f"✅ Got REAL price for {symbol}: Rs. {price}")
                    return price
            
            logger.warning(f"Could not fetch price for {symbol}")
            return None
            
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            return None
    
    @classmethod
    def get_price_volume(cls) -> Dict[str, Dict[str, Any]]:
        """Fetch price and volume data for all stocks"""
        try:
            if not NEPSE_CLIENT_AVAILABLE:
                return {}
            
            client = cls._get_client()
            if not client:
                return {}
            
            price_vol = client.getPriceVolume()
            
            if isinstance(price_vol, dict):
                return price_vol
            elif isinstance(price_vol, list):
                # Convert list to dict keyed by symbol
                result = {}
                for item in price_vol:
                    if isinstance(item, dict) and 'symbol' in item:
                        result[item['symbol']] = item
                return result
            
            return {}
            
        except Exception as e:
            logger.error(f"Error fetching price/volume data: {e}")
            return {}
    
    @classmethod
    def get_market_summary(cls) -> Optional[Dict[str, Any]]:
        """Fetch market summary data"""
        try:
            if not NEPSE_CLIENT_AVAILABLE:
                return None
            
            client = cls._get_client()
            if not client:
                return None
            
            logger.info("Fetching market summary...")
            summary = client.getSummary()
            
            return summary
            
        except Exception as e:
            logger.error(f"Error fetching market summary: {e}")
            return None
    
    @classmethod
    def get_top_gainers(cls, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch top gaining stocks"""
        try:
            if not NEPSE_CLIENT_AVAILABLE:
                return []
            
            client = cls._get_client()
            if not client:
                return []
            
            gainers = client.getTopGainers()
            return gainers[:limit] if gainers else []
        except Exception as e:
            logger.error(f"Error fetching top gainers: {e}")
            return []
    
    @classmethod
    def get_top_losers(cls, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch top losing stocks"""
        try:
            if not NEPSE_CLIENT_AVAILABLE:
                return []
            
            client = cls._get_client()
            if not client:
                return []
            
            losers = client.getTopLosers()
            return losers[:limit] if losers else []
        except Exception as e:
            logger.error(f"Error fetching top losers: {e}")
            return []
    
    @classmethod
    def search_stocks(cls, query: str) -> List[Dict[str, Any]]:
        """Search for stocks by symbol or name"""
        try:
            stocks = cls.get_all_stocks()
            query_upper = query.upper()
            
            results = [
                stock for stock in stocks
                if query_upper in stock.get('symbol', '').upper() or 
                   query_upper in stock.get('name', '').upper()
            ]
            
            logger.info(f"Search for '{query}' found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error searching stocks: {e}")
            return []
