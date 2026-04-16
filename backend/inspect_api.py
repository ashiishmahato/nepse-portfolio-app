#!/usr/bin/env python3
import sys, json
sys.path.insert(0, '.')

from nepse_client import NepseClient

client = NepseClient()
client.setTLSVerification(False)

print("Testing getPriceVolume()...\n")

price_vol = client.getPriceVolume()

print(f"Type: {type(price_vol)}")
print(f"Length: {len(price_vol) if hasattr(price_vol, '__len__') else 'N/A'}")

if isinstance(price_vol, dict):
    print(f"Keys: {list(price_vol.keys())[:10]}")
    # Show first item
    first_key = list(price_vol.keys())[0]
    print(f"\nFirst entry ({first_key}):")
    print(json.dumps(price_vol[first_key], indent=2)[:500])
elif isinstance(price_vol, list):
    print(f"First item type: {type(price_vol[0])}")
    if len(price_vol) > 0:
        print("\nFirst item:")
        if isinstance(price_vol[0], dict):
            print(json.dumps(price_vol[0], indent=2)[:500])
        else:
            print(price_vol[0])

print("\n" + "="*60)
print("Testing getLiveMarket()...\n")

live = client.getLiveMarket()

print(f"Type: {type(live)}")
print(f"Length: {len(live) if hasattr(live, '__len__') else 'N/A'}")

if isinstance(live, dict):
    print(f"Keys (first 5): {list(live.keys())[:5]}")
    first_key = list(live.keys())[0]
    print(f"\nFirst entry ({first_key}):")
    print(json.dumps(live[first_key], indent=2)[:500])
elif isinstance(live, list) and len(live) > 0:
    print(f"First item type: {type(live[0])}")
    print("\nFirst item:")
    if isinstance(live[0], dict):
        print(json.dumps(live[0], indent=2)[:500])
    else:
        print(live[0])
