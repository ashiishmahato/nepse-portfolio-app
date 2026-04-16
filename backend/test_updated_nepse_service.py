#!/usr/bin/env python3
"""Quick test of updated NepseClientService"""
import sys
import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

sys.path.insert(0, r"d:\NEPSE Project\backend")

from app.services.nepse_client_service import NepseClientService

print("="*60)
print("TESTING UPDATED NEPSECLIENT SERVICE")
print("="*60)

# Test 1: Get all stocks
print("\n1. Fetching all real stocks from NEPSE...")
stocks = NepseClientService.get_all_stocks()

if stocks:
    print(f"✅ SUCCESS! Got {len(stocks)} stocks")
    print("\nSample stocks with REAL prices:")
    print("-"*70)
    print(f"{'Symbol':<10} {'Name':<25} {'Price':<12} {'Change %':<10}")
    print("-"*70)
    
    # Show specific stocks we know about
    for stock in stocks[:10]:
        symbol = stock.get('symbol', '')
        name = stock.get('name', '')[:23]
        price = stock.get('ltp', 0)
        change = stock.get('change_percent', 0)
        print(f"{symbol:<10} {name:<25} Rs. {price:>9.2f}  {change:>8.2f}%")
    
    print(f"\n... and {len(stocks) - 10} more stocks\n")
    
    # Check UPPER specifically
    upper = next((s for s in stocks if s['symbol'] == 'UPPER'), None)
    if upper:
        print(f"UPPER stock price: Rs. {upper['ltp']:.2f}")
        print(f"(Expected: ~Rs. 224-230 from real market)")
        print(f"(Old API was showing: Rs. 699.01)")
else:
    print("❌ FAILED! No stocks returned")

# Test 2: Get price for specific stock
print("\n2. Testing specific stock price fetch...")
price = NepseClientService.get_stock_price("NABIL")
if price:
    print(f"✅ NABIL price: Rs. {price:.2f}")
else:
    print("❌ Could not fetch NABIL price")

# Test 3: Get top gainers
print("\n3. Fetching top gainers...")
gainers = NepseClientService.get_top_gainers(5)
if gainers:
    print(f"✅ Got {len(gainers)} top gainers:")
    for gainer in gainers:
        print(f"  {gainer.get('symbol', 'N/A')}: {gainer.get('percentageChange', 0):.2f}%")
else:
    print("❌ No gainers returned")

# Test 4: Search
print("\n4. Testing stock search...")
results = NepseClientService.search_stocks("BANK")
if results:
    print(f"✅ Found {len(results)} stocks matching 'BANK'")
    for r in results[:3]:
        print(f"  {r['symbol']}: {r['name']}")
else:
    print("❌ No results for 'BANK'")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
