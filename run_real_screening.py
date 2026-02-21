"""
Real Stock Screening with Live Data - PHASE 1 ONLY
Uses yfinance in Python 3.11 environment

This script performs PHASE 1: Quantitative Screening
- Screens 500 stocks using Yahoo Finance data
- Calculates 4-component scores (Fundamental, Technical, Catalyst, Sentiment)
- Identifies top 15 candidates
- Saves results to JSON for Phase 2 research validation

PHASE 2 (Research Validation) is performed by Claude using WebSearch
"""

import sys
import os
import json
import time
sys.path.insert(0, '/Users/benjaminkoh/.claude/skills/stock-screener')

from stock_screener import StockScreener
import pandas as pd
from datetime import datetime
from universe_fetcher import get_universe

# Output directory: User's Desktop
DESKTOP_DIR = os.path.expanduser('~/Desktop')

def get_screening_universe(mode='auto', max_stocks=500, exclude_tickers=None):
    """
    Get stock universe - prioritizes LIVE sources

    Default: Fetches S&P 500 from Wikipedia (up to 500 stocks)
    Fallback: Hardcoded list if live fetch fails

    Args:
        mode: Selection mode ('auto', 'sp500', 'nasdaq100', 'combined', etc.)
        max_stocks: Maximum number of stocks to include
        exclude_tickers: List of ticker symbols to exclude

    Returns:
        List of ticker symbols
    """
    tickers = get_universe(mode=mode, max_stocks=max_stocks, min_mcap=2e9)

    # Filter out excluded tickers
    if exclude_tickers:
        exclude_set = set(exclude_tickers)
        tickers = [t for t in tickers if t not in exclude_set]
        print(f"   Excluded {len(exclude_set)} tickers from screening")

    return tickers

def run_comprehensive_screening(mode='auto', max_stocks=500, exclude_tickers=None):
    """
    Run PHASE 1 screening on full universe with real data

    Args:
        mode: Universe selection mode ('auto', 'sp500', 'nasdaq100', etc.)
        max_stocks: Maximum number of stocks to screen
        exclude_tickers: List of ticker symbols to exclude

    Returns:
        tuple: (DataFrame of results, timestamp string, JSON output path)
    """
    # Generate timestamp for output files
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')

    print("\n" + "="*80)
    print("PHASE 1: QUANTITATIVE STOCK SCREENING - LIVE DATA")
    print("="*80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Data Source: Yahoo Finance (yfinance)")
    print(f"Python: 3.11.14 with OpenSSL 3.6.0")
    print(f"Universe Mode: {mode}")
    print("="*80 + "\n")

    # Get universe
    tickers = get_screening_universe(mode=mode, max_stocks=max_stocks, exclude_tickers=exclude_tickers)
    print(f"\n📊 Screening Universe: {len(tickers)} stocks")
    print(f"🎯 Minimum Score: 60 (QUALIFIED rating or higher)")
    print(f"⏱️  Estimated time: ~{len(tickers) * 2 // 60} minutes\n")

    # Initialize screener
    screener = StockScreener()

    # Screen all stocks
    print("Starting analysis with REAL market data...")
    print("-" * 80)

    results = []
    errors = []
    start_time = time.time()

    for i, ticker in enumerate(tickers, 1):
        try:
            # Calculate progress metrics
            elapsed = time.time() - start_time
            pct = (i / len(tickers)) * 100

            # Calculate ETA (only after first stock to avoid division by zero)
            if i > 1:
                avg_time_per_stock = elapsed / (i - 1)
                remaining_stocks = len(tickers) - i
                eta_seconds = remaining_stocks * avg_time_per_stock
                eta_minutes = eta_seconds / 60
                print(f"[{i}/{len(tickers)} - {pct:.1f}%] {ticker} | Elapsed: {elapsed/60:.1f}m | ETA: {eta_minutes:.1f}m", end=' ', flush=True)
            else:
                print(f"[{i}/{len(tickers)} - {pct:.1f}%] Analyzing {ticker}...", end=' ', flush=True)

            result = screener.calculate_final_score(ticker)

            if result and result['final_score'] >= 60:  # Keep scores >= 60
                results.append(result)
                print(f"✓ Score: {result['final_score']:.1f} - {result['rating']}")
            elif result:
                print(f"○ Score: {result['final_score']:.1f} (below threshold)")
            else:
                print(f"✗ Failed")
                errors.append(ticker)

        except Exception as e:
            print(f"✗ Error: {str(e)[:40]}")
            errors.append(ticker)

    print("\n" + "="*80)
    print(f"PHASE 1 SCREENING COMPLETE")
    print(f"  Total analyzed: {len(tickers)}")
    print(f"  Qualified (≥60): {len(results)}")
    print(f"  Errors: {len(errors)}")
    print("="*80)

    if not results:
        print("\n❌ No stocks met minimum criteria")
        return None, None, None

    # Convert to DataFrame and sort
    df = pd.DataFrame(results)
    df = df.sort_values('final_score', ascending=False)

    # Save full results to CSV for reference
    output_csv = os.path.join(DESKTOP_DIR, f'screening_results_{timestamp}.csv')
    df.to_csv(output_csv, index=False)
    print(f"\n💾 Full results saved: {output_csv}")

    # Extract top 15 candidates for Phase 2
    top15 = df.head(15).to_dict('records')

    # Save top 15 to JSON for Phase 2 research validation
    phase1_output = {
        'timestamp': timestamp,
        'phase1_complete': True,
        'screening_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_analyzed': len(tickers),
        'qualified_count': len(results),
        'top15': top15
    }

    json_output_path = os.path.join(DESKTOP_DIR, f'phase1_top15_{timestamp}.json')
    with open(json_output_path, 'w') as f:
        json.dump(phase1_output, f, indent=2, default=str)

    print(f"💾 Top 15 candidates saved: {json_output_path}")

    # Print Phase 2 handoff message
    print("\n" + "="*80)
    print("⚠️  PHASE 1 COMPLETE - Top 15 Candidates Identified")
    print("="*80)
    print(f"\nTop 15 Stocks for Research Validation:")
    for i, stock in enumerate(top15, 1):
        print(f"  {i:2}. {stock['ticker']:<6} - Score: {stock['final_score']:.1f} ({stock['sector']})")

    print("\n" + "="*80)
    print("⚠️  PHASE 2 REQUIRED: Research Validation")
    print("="*80)
    print(f"\n📄 Candidates saved to: {json_output_path}")
    print(f"\nNext: Claude will now execute Phase 2 research validation...")
    print("  - WebSearch for analyst reports, earnings, price targets")
    print("  - Validate quantitative signals with qualitative research")
    print("  - Generate researched investment rationales")
    print("  - Disqualify stocks where research conflicts with signals")
    print("  - Produce final Top 10 with specific analyst data")
    print("\n" + "="*80 + "\n")

    return df, timestamp, json_output_path

if __name__ == "__main__":
    import argparse

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Stock Screener - Phase 1 Quantitative Analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python run_real_screening.py                     # Default: S&P 500 (up to 500 stocks)
  python run_real_screening.py --mode nasdaq100    # NASDAQ 100 only
  python run_real_screening.py --mode tech         # Technology stocks
  python run_real_screening.py --max-stocks 200    # Limit to 200 stocks

Output:
  - screening_results_{timestamp}.csv: All qualified stocks (score ≥60)
  - phase1_top15_{timestamp}.json: Top 15 candidates for Phase 2 validation
        '''
    )
    parser.add_argument(
        '--mode',
        default='auto',
        choices=['auto', 'sp500', 'nasdaq100', 'combined', 'tech', 'healthcare', 'growth', 'file'],
        help='Universe selection mode (default: auto - fetches S&P 500 from Wikipedia)'
    )
    parser.add_argument(
        '--max-stocks',
        type=int,
        default=500,
        help='Maximum number of stocks to screen (default: 500)'
    )
    parser.add_argument(
        '--exclude',
        type=str,
        default=None,
        help='Comma-separated list of ticker symbols to exclude (e.g., AAPL,MSFT,GOOGL)'
    )

    args = parser.parse_args()

    # Parse exclude list
    exclude_tickers = None
    if args.exclude:
        exclude_tickers = [t.strip().upper() for t in args.exclude.split(',')]
        print(f"\n🚫 Excluding {len(exclude_tickers)} tickers: {', '.join(exclude_tickers[:10])}{'...' if len(exclude_tickers) > 10 else ''}\n")

    # Run Phase 1 screening
    results_df, timestamp, json_path = run_comprehensive_screening(
        mode=args.mode,
        max_stocks=args.max_stocks,
        exclude_tickers=exclude_tickers
    )

    if results_df is None:
        print("\n❌ Phase 1 screening failed to produce results")
        sys.exit(1)

    print("✅ Phase 1 complete. Ready for Phase 2 research validation by Claude.")
