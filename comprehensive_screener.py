"""
Comprehensive Stock Screener
Screens a large, diverse universe of quality stocks across all sectors
"""

import sys
sys.path.insert(0, '/Users/benjaminkoh/.claude/skills/stock-screener')

from stock_screener import StockScreener
import pandas as pd
import time

def get_comprehensive_universe():
    """
    Returns comprehensive, sector-diverse universe of ~200 stocks
    Includes S&P 500 leaders + high-growth mid-caps across all sectors
    """

    universe = {
        # TECHNOLOGY (40 stocks)
        'Mega Cap Tech': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'AMD', 'AVGO', 'ORCL', 'CSCO', 'INTC'],
        'Software': ['CRM', 'NOW', 'WDAY', 'PANW', 'FTNT', 'SNOW', 'DDOG', 'CRWD', 'ZS', 'OKTA'],
        'Semiconductors': ['TSM', 'ASML', 'QCOM', 'TXN', 'MU', 'LRCX', 'AMAT', 'KLAC', 'MRVL', 'NXPI'],
        'Cloud/SaaS': ['TEAM', 'NET', 'HUBS', 'TWLO', 'MDB', 'DOMO', 'ZM', 'VEEV', 'TTD', 'ESTC'],

        # HEALTHCARE & BIOTECH (35 stocks)
        'Large Cap Healthcare': ['UNH', 'JNJ', 'LLY', 'ABBV', 'TMO', 'ABT', 'DHR', 'PFE', 'MRK', 'BMY'],
        'Biotech Leaders': ['VRTX', 'REGN', 'GILD', 'AMGN', 'BIIB', 'MRNA', 'BNTX', 'IONS', 'ALNY', 'SRPT'],
        'Med Tech': ['ISRG', 'DXCM', 'ALGN', 'PODD', 'EW', 'SYK', 'BSX', 'MDT', 'ILMN', 'IDXX'],
        'Healthcare Services': ['HCA', 'TDOC', 'EXAS', 'HOLX', 'TECH'],

        # CONSUMER DISCRETIONARY (30 stocks)
        'E-Commerce & Tech': ['AMZN', 'TSLA', 'UBER', 'LYFT', 'ABNB', 'DASH', 'ETSY', 'W', 'CHWY', 'CVNA'],
        'Retail': ['HD', 'LOW', 'TGT', 'COST', 'WMT', 'LULU', 'NKE', 'SBUX', 'MCD', 'CMG'],
        'Auto/EV': ['RIVN', 'LCID', 'GM', 'F', 'TM', 'HMC'],
        'Entertainment': ['DIS', 'NFLX', 'SPOT', 'RBLX'],

        # FINANCIALS (25 stocks)
        'Banks': ['JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'SCHW', 'USB', 'PNC', 'BLK'],
        'FinTech': ['V', 'MA', 'PYPL', 'SQ', 'COIN', 'HOOD', 'SOFI', 'AFRM', 'UPST', 'LC'],
        'Insurance': ['BRK-B', 'PGR', 'AIG', 'AFL', 'MET'],

        # INDUSTRIALS (20 stocks)
        'Industrial Leaders': ['CAT', 'DE', 'HON', 'UNP', 'UPS', 'GE', 'MMM', 'BA', 'RTX', 'LMT'],
        'Emerging Industrials': ['CARR', 'OTIS', 'IR', 'XYL', 'GNRC', 'ETN', 'ROK', 'PH', 'FAST', 'WWD'],

        # ENERGY & CLEAN ENERGY (20 stocks)
        'Oil & Gas': ['XOM', 'CVX', 'COP', 'SLB', 'EOG', 'PSX', 'VLO', 'MPC', 'OXY', 'DVN'],
        'Clean Energy': ['ENPH', 'SEDG', 'RUN', 'FSLR', 'BE', 'PLUG', 'NEE', 'DUK', 'SO', 'AEP'],

        # MATERIALS & CHEMICALS (15 stocks)
        'Materials': ['LIN', 'APD', 'ECL', 'SHW', 'NEM', 'FCX', 'VMC', 'MLM', 'NUE', 'STLD'],
        'Chemicals': ['DOW', 'DD', 'PPG', 'ALB', 'FMC'],

        # COMMUNICATION SERVICES (12 stocks)
        'Telecom/Media': ['GOOG', 'META', 'CMCSA', 'T', 'VZ', 'TMUS', 'NFLX', 'DIS', 'PARA', 'WBD', 'FOXA', 'OMC'],

        # REAL ESTATE & REITS (10 stocks)
        'REITs': ['AMT', 'PLD', 'CCI', 'EQIX', 'PSA', 'DLR', 'SBAC', 'EXR', 'AVB', 'EQR'],

        # UTILITIES (8 stocks)
        'Utilities': ['NEE', 'DUK', 'SO', 'D', 'AEP', 'EXC', 'SRE', 'XEL'],
    }

    # Flatten into single list
    all_tickers = []
    for category, tickers in universe.items():
        all_tickers.extend(tickers)

    # Remove duplicates
    unique_tickers = list(set(all_tickers))

    return unique_tickers

def screen_universe():
    """Screen the comprehensive universe"""

    print("\n" + "="*80)
    print("COMPREHENSIVE MARKET SCREENING")
    print("="*80)

    # Get universe
    tickers = get_comprehensive_universe()
    print(f"\n📊 Universe Size: {len(tickers)} stocks across all major sectors")
    print(f"🎯 Goal: Find top 10 with highest appreciation potential")
    print(f"⏱️  Estimated time: ~{len(tickers) * 2 // 60} minutes\n")

    # Initialize screener
    screener = StockScreener()

    # Screen all stocks
    print("Starting comprehensive screening...")
    print("-" * 80)

    results = []
    errors = []

    for i, ticker in enumerate(tickers, 1):
        try:
            if i % 10 == 0:
                print(f"Progress: {i}/{len(tickers)} stocks analyzed ({len(results)} qualified)")

            result = screener.calculate_final_score(ticker)

            if result and result['final_score'] >= 60:  # Only keep scores >= 60
                results.append(result)
                print(f"✓ {ticker}: {result['final_score']:.1f} - {result['rating']}")

        except Exception as e:
            errors.append(ticker)
            print(f"✗ {ticker}: Error - {str(e)[:50]}")

        # Rate limiting
        time.sleep(0.5)

    print("\n" + "="*80)
    print(f"Screening Complete!")
    print(f"  - Analyzed: {len(tickers)}")
    print(f"  - Qualified (score >=60): {len(results)}")
    print(f"  - Errors: {len(errors)}")
    print("="*80)

    # Convert to DataFrame and sort
    if results:
        df = pd.DataFrame(results)
        df = df.sort_values('final_score', ascending=False)

        # Save results
        df.to_csv('screening_results.csv', index=False)
        print(f"\n💾 Full results saved to: screening_results.csv")

        return df
    else:
        print("\n❌ No stocks met the minimum criteria")
        return pd.DataFrame()

def generate_top10_report(df):
    """Generate detailed report for top 10 stocks"""

    if len(df) == 0:
        print("No results to report")
        return

    print("\n" + "="*80)
    print("TOP 10 STOCKS WITH HIGHEST APPRECIATION POTENTIAL")
    print("="*80)

    # Ensure sector diversity (max 3 per sector)
    top10 = []
    sector_count = {}

    for _, row in df.iterrows():
        sector = row['sector']
        if len(top10) >= 10:
            break
        if sector_count.get(sector, 0) < 3:
            top10.append(row)
            sector_count[sector] = sector_count.get(sector, 0) + 1

    # Create summary table
    summary_data = []

    for i, stock in enumerate(top10, 1):
        # Estimate appreciation based on score
        score = stock['final_score']
        if score >= 85:
            appreciation = "60-80%"
        elif score >= 75:
            appreciation = "50-70%"
        elif score >= 65:
            appreciation = "40-60%"
        else:
            appreciation = "30-50%"

        # Get key catalyst
        catalysts = stock['details']['catalyst'].get('catalysts', [])
        key_catalyst = catalysts[0] if catalysts else "Strong fundamentals + technical setup"

        # Create rationale
        fund_score = stock['fundamental_score']
        tech_score = stock['technical_score']
        cat_score = stock['catalyst_score']

        rationale_parts = []
        if fund_score >= 75:
            rationale_parts.append("Strong fundamentals")
        if tech_score >= 75:
            rationale_parts.append("bullish technicals")
        if cat_score >= 75:
            rationale_parts.append("major catalysts")

        rationale = f"{stock['sector']} leader with {', '.join(rationale_parts)}. Score: {score:.1f}/100"

        summary_data.append({
            'Rank': i,
            'Ticker': stock['ticker'],
            'Company': stock['company_name'][:30],
            'Score': f"{score:.1f}",
            'Expected Appreciation': appreciation,
            'Key Catalyst': key_catalyst[:40],
            'Rationale': rationale[:80]
        })

    summary_df = pd.DataFrame(summary_data)

    print("\n" + summary_df.to_string(index=False))
    print("\n" + "="*80)

    # Detailed analysis for each
    print("\nDETAILED ANALYSIS\n")
    print("="*80)

    screener = StockScreener()

    for i, stock in enumerate(top10, 1):
        print(f"\n{'='*80}")
        print(f"#{i} - {stock['ticker']} - {stock['company_name']}")
        print(f"{'='*80}")

        # Re-generate full report
        full_result = screener.calculate_final_score(stock['ticker'])
        if full_result:
            report = screener.generate_report(full_result)
            print(report)

        if i < len(top10):
            print("\n" + "-"*80)

    # Portfolio summary
    print("\n" + "="*80)
    print("PORTFOLIO CONSTRUCTION RECOMMENDATION")
    print("="*80)

    print("\nSuggested Allocation (for speculative growth portfolio):")
    for i, stock in enumerate(top10, 1):
        if i <= 3:
            size = "15-20%"
        elif i <= 7:
            size = "10-15%"
        else:
            size = "5-10%"

        print(f"  {i}. {stock['ticker']:<6} ({stock['sector'][:20]:<20}): {size}")

    print("\nDiversification:")
    sector_breakdown = pd.DataFrame(top10)['sector'].value_counts()
    for sector, count in sector_breakdown.items():
        print(f"  - {sector}: {count} stocks")

    print("\n⚠️  CRITICAL RISK DISCLAIMER:")
    print("-" * 80)
    print("""
This is a HIGH-RISK, SPECULATIVE strategy. Key warnings:

• 50% appreciation in 3 months = ~267% annualized (EXTREMELY RARE)
• Significant downside risk exists
• Use ONLY risk capital you can afford to lose completely
• This is NOT financial advice - educational purposes only
• Always conduct independent research
• Consult a licensed financial advisor before investing

Market conditions, catalysts, and company fundamentals can change rapidly.
Past performance does not guarantee future results.
""")
    print("="*80)

if __name__ == "__main__":
    # Run comprehensive screening
    results_df = screen_universe()

    # Generate top 10 report
    if len(results_df) > 0:
        generate_top10_report(results_df)
    else:
        print("\n❌ Screening produced no qualifying stocks")
