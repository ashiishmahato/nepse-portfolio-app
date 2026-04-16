#!/usr/bin/env python3
"""
Test the NepseClient service for real NEPSE stock prices
"""
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_nepse_client():
    """Test NepseClient service"""
    try:
        print("\n" + "="*60)
        print("TESTING NEPSECLIENT SERVICE")
        print("="*60 + "\n")
        
        from app.services.nepse_client_service import NepseClientService
        
        print("Fetching all REAL stocks from NEPSE...\n")
        stocks = NepseClientService.get_all_stocks()
        
        if stocks:
            print(f"SUCCESS! Fetched {len(stocks)} REAL stocks\n")
            print("Sample prices:")
            print("-" * 60)
            print(f"{'Symbol':<10} {'LTP':<12} {'Change %':<12} {'Sector':<20}")
            print("-" * 60)
            
            # Show first 10 stocks
            for stock in stocks[:10]:
                symbol = stock.get('symbol', 'N/A')
                ltp = stock.get('ltp', 'N/A')
                change = stock.get('change_percent', 'N/A')
                sector = stock.get('sector', 'Unknown')
                print(f"{symbol:<10} Rs. {ltp:<10} {change:>10}% {sector:<20}")
            
            print(f"\n... and {len(stocks) - 10} more stocks\n")
            
            # Check for UPPER specifically
            upper = next((s for s in stocks if s.get('symbol') == 'UPPER'), None)
            if upper:
                upper_price = upper.get('ltp', 'N/A')
                print(f"UPPER stock price: Rs. {upper_price}")
                print(f"(Expected: ~Rs. 224-230 from real market)")
                print(f"(Old API was showing: Rs. 699.01)\n")
            
            # Check for market summary
            print("Fetching market summary...\n")
            summary = NepseClientService.get_market_summary()
            if summary:
                print(f"Market Summary:")
                for key, value in list(summary.items())[:5]:
                    print(f"  {key}: {value}")
            
            return True
        else:
            print("FAILED! No stocks returned\n")
            print("Possible causes:")
            print("   - NepseClient network issue")
            print("   - API returned error")
            print("   - No internet connection\n")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return False
    finally:
        print("="*60 + "\n")

if __name__ == '__main__':
    success = test_nepse_client()
    sys.exit(0 if success else 1)
