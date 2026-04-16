#!/usr/bin/env python3
"""
Quick test of the Selenium-based Merolagani scraper
"""
import sys
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_scraper():
    """Test the Merolagani scraper"""
    try:
        print("\n" + "="*60)
        print("TESTING MEROLAGANI SELENIUM SCRAPER")
        print("="*60 + "\n")
        
        from app.services.merolagani_scraper import MerolaganiScraper
        
        print("Fetching all stock prices from Merolagani...\n")
        prices = MerolaganiScraper.get_all_stock_prices()
        
        if prices:
            print(f"SUCCESS! Fetched {len(prices)} stocks\n")
            print("Sample prices:")
            print("-" * 50)
            
            # Show first 10 stocks
            for i, (symbol, data) in enumerate(list(prices.items())[:10]):
                price = data.get('current_price', data.get('ltp', 'N/A'))
                print(f"   {symbol:8} = Rs. {price}")
            
            print(f"\n... and {len(prices) - 10} more stocks\n")
            
            # Check for UPPER specifically
            if 'UPPER' in prices:
                upper_price = prices['UPPER'].get('current_price', prices['UPPER'].get('ltp'))
                print(f"UPPER stock price: Rs. {upper_price}")
                print(f"(Expected: ~Rs. 224.50 from Merolagani)")
                print(f"(Was showing: Rs. 699.01 from old API)\n")
            
            return True
        else:
            print("FAILED! No prices returned\n")
            print("Possible causes:")
            print("   - Merolagani website structure changed")
            print("   - Page elements not loading properly")
            print("   - Network issue\n")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return False
    finally:
        print("="*60 + "\n")

if __name__ == '__main__':
    success = test_scraper()
    sys.exit(0 if success else 1)
