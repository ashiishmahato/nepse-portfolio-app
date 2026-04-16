"""
Mock data provider for NEPSE stock prices
"""
import random
from datetime import datetime, timedelta
from typing import List, Dict


class MockNEPSEDataProvider:
    """
    Mock data provider for NEPSE stocks
    In production, this would connect to actual NEPSE API
    """
    
    # Comprehensive list of NEPSE stocks
    STOCKS = {
        # Banks
        "NABIL": {"name": "Nabil Bank Limited", "sector": "Banking"},
        "NNPL": {"name": "Nepal Noodle Private Limited", "sector": "Trading"},
        "AKBPL": {"name": "Akbari Cement Limited", "sector": "Cement"},
        "CCBL": {"name": "Century Commercial Bank Limited", "sector": "Banking"},
        "EBL": {"name": "Everest Bank Limited", "sector": "Banking"},
        "GFCL": {"name": "Global Finance Limited", "sector": "Finance"},
        "HBL": {"name": "Himalayan Bank Limited", "sector": "Banking"},
        "ICFC": {"name": "ICFC Finance Limited", "sector": "Finance"},
        "JBBL": {"name": "Janakpur Bank Limited", "sector": "Banking"},
        "KBBL": {"name": "Kist Bank Limited", "sector": "Banking"},
        "NBL": {"name": "Nepal Bank Limited", "sector": "Banking"},
        "NIC": {"name": "NIC Asia Bank Limited", "sector": "Banking"},
        "NIBL": {"name": "Nepal Investment Bank Limited", "sector": "Banking"},
        "SBL": {"name": "Standard Chartered Bank Nepal", "sector": "Banking"},
        "MBL": {"name": "Machhapuchhare Bank Limited", "sector": "Banking"},
        "PRVU": {"name": "Prabhu Bank Limited", "sector": "Banking"},
        "NICA": {"name": "Naya Insurance Company Limited", "sector": "Insurance"},
        "NICSF": {"name": "NIC Credit and Savings", "sector": "Finance"},
        "UPPER": {"name": "Upper Tamakosi Hydropower Limited", "sector": "Hydropower"},
        "BPCL": {"name": "Bhrikuti Hydropower Company Limited", "sector": "Hydropower"},
        # Finance Companies
        "CFCL": {"name": "Central Finance Company", "sector": "Finance"},
        "FCFL": {"name": "First Citizens Finance Limited", "sector": "Finance"},
        "LHPL": {"name": "Laxmi Hydro Power Limited", "sector": "Hydropower"},
        "MFIL": {"name": "Mithila Financial Investments", "sector": "Finance"},
        "NFCL": {"name": "National Finance Company", "sector": "Finance"},
        "SFCL": {"name": "Siddhartha Finance Company", "sector": "Finance"},
        # Insurance
        "AIC": {"name": "Alliance Insurance Company", "sector": "Insurance"},
        "EIC": {"name": "Everest Insurance Company", "sector": "Insurance"},
        "HIC": {"name": "Himalayan Insurance Company", "sector": "Insurance"},
        "NLIC": {"name": "National Life Insurance", "sector": "Insurance"},
        "PIC": {"name": "Premier Insurance Company", "sector": "Insurance"},
        # Trading/Retail
        "ATPL": {"name": "Alternative Telecom Private Limited", "sector": "Trading"},
        "BNPL": {"name": "Bottlers Nepal Private Limited", "sector": "Trading"},
        "CBPO": {"name": "CB Poudel Office", "sector": "Trading"},
        "CHCL": {"name": "Chaudhary Chowk Limited", "sector": "Trading"},
        "DHAN": {"name": "Dhawan Limited", "sector": "Trading"},
        # Cement
        "AKPL": {"name": "Akbarpurantol Cement", "sector": "Cement"},
        "JPWL": {"name": "JP Wallpaper Limited", "sector": "Cement"},
        "MLBBL": {"name": "Mohan Lal Bitumen", "sector": "Cement"},
        # Manufacturing
        "MHNL": {"name": "Mahakali Noodles Limited", "sector": "Manufacturing"},
        "NHPC": {"name": "Nepalese Hydropower Company", "sector": "Hydropower"},
        "PPCL": {"name": "PPC Limited", "sector": "Manufacturing"},
        # Real Estate
        "RSDC": {"name": "Real Estate Developers Consortium", "sector": "Real Estate"},
        "SHPL": {"name": "Samrat Housing Private Limited", "sector": "Real Estate"},
        # Others
        "APCL": {"name": "APL Capital Limited", "sector": "Finance"},
        "MEGA": {"name": "Mega Bank Limited", "sector": "Banking"},
        "SANIMA": {"name": "Sanima Mai FMCG Limited", "sector": "Consumer"},
        "SEBON": {"name": "Securities Board of Nepal", "sector": "Finance"},
        "GEUS": {"name": "Gurkha Engineering Utilities", "sector": "Industrial"},
    }
    
    @staticmethod
    def get_all_stocks() -> List[Dict]:
        """Get list of all available stocks"""
        stocks = []
        for symbol, info in MockNEPSEDataProvider.STOCKS.items():
            stocks.append({
                "symbol": symbol,
                "name": info["name"],
                "sector": info["sector"],
                "current_price": MockNEPSEDataProvider.get_stock_price(symbol),
            })
        return stocks
    
    @staticmethod
    def get_stock_price(symbol: str) -> float:
        """Get current price for a symbol"""
        # Generate consistent but slightly variable prices
        random.seed(hash(symbol) + int(datetime.now().strftime("%Y%m%d")))
        
        base_prices = {
            # Banks
            "NABIL": 1450, "CCBL": 320, "EBL": 640, "HBL": 520, "JBBL": 210,
            "KBBL": 380, "NBL": 280, "NIC": 960, "NIBL": 1200, "SBL": 380,
            "MBL": 420, "PRVU": 310,
            # Finance
            "GFCL": 180, "ICFC": 280, "CFCL": 150, "FCFL": 190, "MFIL": 280,
            "NFCL": 160, "SFCL": 210, "APCL": 140,
            # Insurance
            "NICA": 780, "NICSF": 220, "AIC": 350, "EIC": 420, "HIC": 480,
            "NLIC": 560, "PIC": 390,
            # Trading
            "NNPL": 850, "ATPL": 410, "BNPL": 520, "CBPO": 280, "CHCL": 340,
            "DHAN": 280,
            # Cement
            "AKBPL": 120, "AKPL": 140, "JPWL": 180, "MLBBL": 220,
            # Hydropower
            "UPPER": 680, "BPCL": 590, "LHPL": 420, "NHPC": 350,
            # Manufacturing
            "MHNL": 280, "PPCL": 320,
            # Real Estate
            "RSDC": 180, "SHPL": 260,
            # Others
            "MEGA": 580, "SANIMA": 410, "SEBON": 320, "GEUS": 290,
        }
        
        base_price = base_prices.get(symbol, random.randint(200, 1500))
        # Add some random variation (±5%)
        variation = base_price * random.uniform(-0.05, 0.05)
        return round(base_price + variation, 2)
    
    @staticmethod
    def get_historical_data(symbol: str, days: int = 200) -> List[Dict]:
        """Get historical price data for technical analysis"""
        historical = []
        random.seed(hash(symbol))
        
        base_prices = {
            # Banks
            "NABIL": 1450, "CCBL": 320, "EBL": 640, "HBL": 520, "JBBL": 210,
            "KBBL": 380, "NBL": 280, "NIC": 960, "NIBL": 1200, "SBL": 380,
            "MBL": 420, "PRVU": 310,
            # Finance
            "GFCL": 180, "ICFC": 280, "CFCL": 150, "FCFL": 190, "MFIL": 280,
            "NFCL": 160, "SFCL": 210, "APCL": 140,
            # Insurance
            "NICA": 780, "NICSF": 220, "AIC": 350, "EIC": 420, "HIC": 480,
            "NLIC": 560, "PIC": 390,
            # Trading
            "NNPL": 850, "ATPL": 410, "BNPL": 520, "CBPO": 280, "CHCL": 340,
            "DHAN": 280,
            # Cement
            "AKBPL": 120, "AKPL": 140, "JPWL": 180, "MLBBL": 220,
            # Hydropower
            "UPPER": 680, "BPCL": 590, "LHPL": 420, "NHPC": 350,
            # Manufacturing
            "MHNL": 280, "PPCL": 320,
            # Real Estate
            "RSDC": 180, "SHPL": 260,
            # Others
            "MEGA": 580, "SANIMA": 410, "SEBON": 320, "GEUS": 290,
        }
        
        base_price = base_prices.get(symbol, random.randint(200, 1500))
        current_price = base_price
        
        for i in range(days, 0, -1):
            date = datetime.now() - timedelta(days=i)
            
            # Random walk price movement
            daily_change = random.uniform(-0.02, 0.025)
            current_price = current_price * (1 + daily_change)
            
            open_price = current_price * random.uniform(0.99, 1.01)
            high_price = max(current_price, open_price) * random.uniform(1.0, 1.015)
            low_price = min(current_price, open_price) * random.uniform(0.985, 1.0)
            close_price = current_price
            volume = random.randint(10000, 500000)
            
            historical.append({
                "date": date,
                "open": round(open_price, 2),
                "high": round(high_price, 2),
                "low": round(low_price, 2),
                "close": round(close_price, 2),
                "volume": volume,
            })
        
        return historical
    
    @staticmethod
    def search_stocks(query: str) -> List[Dict]:
        """Search stocks by symbol or name"""
        query_lower = query.lower()
        results = []
        
        for symbol, info in MockNEPSEDataProvider.STOCKS.items():
            if (query_lower in symbol.lower() or 
                query_lower in info["name"].lower() or
                query_lower in info["sector"].lower()):
                results.append({
                    "symbol": symbol,
                    "name": info["name"],
                    "sector": info["sector"],
                    "current_price": MockNEPSEDataProvider.get_stock_price(symbol),
                })
        
        return results
