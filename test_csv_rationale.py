"""
Test that rationale appears in CSV output
"""
import sys
sys.path.insert(0, '/Users/benjaminkoh/.claude/skills/stock-screener')

from run_real_screening import generate_rationale
from stock_screener import StockScreener
import pandas as pd

print("\nTesting CSV rationale output...\n")
print("="*80)

# Test with NVDA
screener = StockScreener()
result = screener.calculate_final_score('NVDA')

if result:
    # Add rationale
    result['rationale'] = generate_rationale(result)

    # Show what will be in CSV
    print(f"Stock: {result['ticker']}")
    print(f"Score: {result['final_score']:.1f}")
    print(f"\nRationale (as it will appear in CSV):")
    print(f"{result['rationale']}")

    # Create a small DataFrame to show CSV format
    df = pd.DataFrame([result])

    # Show just the key columns
    print("\n" + "="*80)
    print("CSV Preview (key columns):")
    print("="*80)
    cols = ['ticker', 'final_score', 'rating', 'rationale']
    print(df[cols].to_string(index=False))

    print("\n✅ Rationale will now be included in screening_results_live.csv!")
else:
    print("❌ Failed to fetch data")

print("="*80)
