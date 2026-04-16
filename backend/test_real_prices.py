"""
Debug script to test if real prices are being fetched
"""
import sys
sys.path.insert(0, '/d/NEPSE Project/backend')

from app.services.merolagani_scraper import MerolaganiScraper
from app.services.nepse_data_service import NepseDataService
import json

print("\n" + "="*60)
print("TESTING REAL PRICE FETCHING")
print("="*60)

# Test 1: Try Merolagani scraper directly
print("\n1. Testing Merolagani Scraper...")
try:
    prices = MerolaganiScraper.get_all_stock_prices()
    if prices:
        print(f"✅ Got {len(prices)} stocks from Merolagani")
        print("\nSample prices:")
        for i, (symbol, data) in enumerate(list(prices.items())[:5]):
            print(f"  {symbol}: Rs. {data.get('ltp', 'N/A')}")
    else:
        print("❌ Merolagani returned no prices")
except Exception as e:
    print(f"❌ Error: {str(e)}")

# Test 2: Try NepseDataService
print("\n2. Testing NepseDataService...")
try:
    stocks = NepseDataService.get_all_stocks()
    if stocks:
        print(f"✅ Got {len(stocks)} stocks")
        print("\nSample stocks:")
        for stock in stocks[:5]:
            print(f"  {stock.get('symbol')}: {stock.get('name')} @ Rs. {stock.get('ltp', 'N/A')}")
    else:
        print("❌ NepseDataService returned no stocks")
except Exception as e:
    print(f"❌ Error: {str(e)}")

# Test 3: Try price volume endpoint
print("\n3. Testing Price/Volume Data...")
try:
    price_volume = NepseDataService.get_price_volume()
    if price_volume:
        print(f"✅ Got price/volume data for {len(price_volume)} items")
        for i, (symbol, data) in enumerate(list(price_volume.items())[:3]):
            print(f"  {symbol}: {data}")
    else:
        print("❌ No price/volume data")
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n" + "="*60)
print("Check if prices match Merolagani.com/StockQuote")
print("="*60 + "\n")
