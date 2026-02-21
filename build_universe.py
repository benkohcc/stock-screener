"""
Build comprehensive stock universe for screening
Filters by market cap, volume, and basic criteria
"""

import yfinance as yf
import pandas as pd
import time
from datetime import datetime

def get_sp500_tickers():
    """Get S&P 500 tickers as starting point"""
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        tables = pd.read_html(url)
        sp500 = tables[0]
        return list(sp500['Symbol'].str.replace('.', '-'))
    except:
        return []

def get_nasdaq100_tickers():
    """Get NASDAQ 100 tickers"""
    try:
        url = 'https://en.wikipedia.org/wiki/Nasdaq-100'
        tables = pd.read_html(url)
        nasdaq = tables[4]  # Usually the 5th table
        return list(nasdaq['Ticker'])
    except:
        return []

def get_russell_midcap_sample():
    """Get sample of Russell Mid Cap stocks"""
    # Common mid-cap tickers across sectors
    midcaps = [
        # Technology
        'PLTR', 'SNOW', 'CRWD', 'NET', 'DDOG', 'ZS', 'OKTA', 'HUBS', 'TWLO', 'DOCU',
        'MDB', 'TEAM', 'ZM', 'U', 'PATH', 'BILL', 'S', 'PCTY', 'ESTC', 'SUMO',

        # Healthcare/Biotech
        'EXAS', 'VRTX', 'REGN', 'MRNA', 'BNTX', 'ILMN', 'DXCM', 'ALGN', 'PODD', 'TDOC',
        'IONS', 'TECH', 'BMRN', 'RARE', 'INCY', 'NBIX', 'ALNY', 'SRPT', 'FOLD', 'ARWR',

        # Consumer
        'RIVN', 'LCID', 'ABNB', 'DASH', 'LYFT', 'UBER', 'ETSY', 'W', 'CVNA', 'CHWY',
        'PTON', 'LULU', 'ULTA', 'DKS', 'FIVE', 'OLLI', 'BURL', 'TJX', 'ROST', 'AEO',

        # Industrials
        'CARR', 'OTIS', 'XYL', 'IR', 'GNRC', 'BLDR', 'FND', 'MLM', 'VMC', 'SUM',

        # Clean Energy
        'ENPH', 'SEDG', 'RUN', 'NOVA', 'FSLR', 'ARRY', 'MAXN', 'CSIQ', 'SHLS', 'BE',

        # Semiconductors
        'ARM', 'MRVL', 'MPWR', 'MU', 'LRCX', 'AMAT', 'KLAC', 'NXPI', 'MCHP', 'ON',
        'SWKS', 'QRVO', 'WOLF', 'CRUS', 'SLAB', 'SITM', 'AOSL', 'FORM', 'POWI', 'MTSI',

        # Software/Cloud
        'WDAY', 'NOW', 'PANW', 'FTNT', 'VEEV', 'TTD', 'DKNG', 'RBLX', 'APP', 'GTLB',

        # Financials
        'COIN', 'HOOD', 'SOFI', 'AFRM', 'UPST', 'LC', 'MARA', 'RIOT', 'HUT', 'BTBT',

        # Real Estate/REITs
        'EQIX', 'DLR', 'AMT', 'CCI', 'SBAC', 'PSA', 'EXR', 'CUBE', 'REXR', 'NSA'
    ]
    return midcaps

def filter_stock(ticker):
    """
    Check if a stock meets our basic criteria
    Returns: (meets_criteria, info_dict)
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Get market cap
        market_cap = info.get('marketCap', 0)
        if market_cap == 0 or market_cap is None:
            return False, None

        # Filter: $2B to $200B market cap
        if market_cap < 2e9 or market_cap > 200e9:
            return False, None

        # Get current price
        current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        if current_price < 10:  # Avoid penny stocks
            return False, None

        # Check volume
        avg_volume = info.get('averageVolume', 0) or info.get('averageDailyVolume10Day', 0)
        if avg_volume < 500000:  # Minimum 500k shares/day
            return False, None

        # Compile key info
        stock_info = {
            'ticker': ticker,
            'name': info.get('longName', ticker),
            'sector': info.get('sector', 'Unknown'),
            'industry': info.get('industry', 'Unknown'),
            'market_cap': market_cap,
            'price': current_price,
            'volume': avg_volume,
            'revenue_growth': info.get('revenueGrowth', 0),
            'profit_margin': info.get('profitMargins', 0),
            'debt_to_equity': info.get('debtToEquity', 0),
        }

        return True, stock_info

    except Exception as e:
        print(f"Error checking {ticker}: {str(e)[:50]}")
        return False, None

def build_universe():
    """Build comprehensive stock universe"""
    print("Building comprehensive stock universe...")
    print("="*80)

    # Combine ticker sources
    print("\n1. Gathering tickers from major indices...")
    sp500 = get_sp500_tickers()
    print(f"   - S&P 500: {len(sp500)} tickers")

    nasdaq100 = get_nasdaq100_tickers()
    print(f"   - NASDAQ 100: {len(nasdaq100)} tickers")

    midcaps = get_russell_midcap_sample()
    print(f"   - Mid Cap sample: {len(midcaps)} tickers")

    # Combine and deduplicate
    all_tickers = list(set(sp500 + nasdaq100 + midcaps))
    print(f"\n2. Total unique tickers to screen: {len(all_tickers)}")

    # Filter stocks
    print("\n3. Filtering by criteria (market cap $2B-$200B, volume >500k, price >$10)...")
    print("   This may take several minutes...\n")

    qualified_stocks = []
    failed_count = 0

    for i, ticker in enumerate(all_tickers, 1):
        if i % 50 == 0:
            print(f"   Processed {i}/{len(all_tickers)} tickers... ({len(qualified_stocks)} qualified so far)")

        meets_criteria, info = filter_stock(ticker)

        if meets_criteria:
            qualified_stocks.append(info)
            print(f"   ✓ {ticker}: {info['name'][:40]} - ${info['market_cap']/1e9:.1f}B")
        else:
            failed_count += 1

        # Rate limiting
        time.sleep(0.1)

    print(f"\n4. Filtering complete!")
    print(f"   - Qualified: {len(qualified_stocks)}")
    print(f"   - Filtered out: {failed_count}")

    # Convert to DataFrame and save
    df = pd.DataFrame(qualified_stocks)

    # Save to CSV
    output_file = 'stock_universe.csv'
    df.to_csv(output_file, index=False)
    print(f"\n5. Universe saved to: {output_file}")

    # Show summary by sector
    print("\n6. Universe breakdown by sector:")
    print(df.groupby('sector').size().sort_values(ascending=False))

    print("\n" + "="*80)
    print(f"Universe building complete: {len(df)} stocks ready for screening")

    return df

if __name__ == "__main__":
    df = build_universe()
    print("\nTop 10 by market cap:")
    print(df.nlargest(10, 'market_cap')[['ticker', 'name', 'market_cap', 'sector']])
