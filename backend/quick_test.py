#!/usr/bin/env python3
import sys
import logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

sys.path.insert(0, '.')
from app.services.nepse_client_service import NepseClientService

print("\n" + "="*60)
print("FETCHING REAL PRICES FROM NEPSE")
print("="*60 + "\n")

stocks = NepseClientService.get_all_stocks()
print(f"\nTotal stocks fetched: {len(stocks)}\n")

if stocks:
    print("Sample stocks with REAL prices:")
    print("-"*50)
    for s in stocks[:5]:
        print(f"{s['symbol']:8} = Rs. {s['ltp']:>10.2f}")
    
    print("\n\nKey stocks we care about:")
    print("-"*50)
    for s in stocks:
        if s['symbol'] in ['NABIL', 'UPPER', 'HBL', 'EBL', 'NIMB']:
            print(f"{s['symbol']:8} = Rs. {s['ltp']:>10.2f}")
else:
    print("ERROR: No stocks returned!")

print("\n" + "="*60)
