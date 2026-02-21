"""
Quick test to show the new rationale output
"""
import sys
sys.path.insert(0, '/Users/benjaminkoh/.claude/skills/stock-screener')

from stock_screener import StockScreener

# Test with one stock
screener = StockScreener()
print("\nTesting new rationale output with NVDA...\n")
print("="*80)

result = screener.calculate_final_score('NVDA')

if result:
    stock = result
    fund_details = stock['details']['fundamental']['metrics']
    tech_details = stock['details']['technical']
    catalysts = stock['details']['catalyst'].get('catalysts', [])

    print(f"#{1} - {stock['ticker']} - {stock['company_name']}")
    print(f"{'='*80}")
    print(f"Current Price: ${stock['current_price']:.2f} (LIVE)")
    print(f"Market Cap: ${stock['market_cap']/1e9:.1f}B")
    print(f"Sector: {stock['sector']}")
    print(f"\nFINAL SCORE: {stock['final_score']:.1f}/100 - {stock['rating']}")
    print(f"\nComponent Scores:")
    print(f"  Fundamental:  {stock['fundamental_score']:.1f}/100")
    print(f"  Technical:    {stock['technical_score']:.1f}/100")
    print(f"  Catalyst:     {stock['catalyst_score']:.1f}/100")
    print(f"  Sentiment:    {stock['sentiment_score']:.1f}/100")

    # Show the new rationale section
    score = stock['final_score']
    fund_score = stock['fundamental_score']
    tech_score = stock['technical_score']
    cat_score = stock['catalyst_score']
    sent_score = stock['sentiment_score']

    print(f"\n{'─'*80}")
    print("INVESTMENT RATIONALE")
    print(f"{'─'*80}")

    if score >= 80:
        overall = "This is a STRONG BUY with exceptional characteristics across multiple factors."
    elif score >= 70:
        overall = "This is a solid BUY with strong fundamentals and favorable setup."
    elif score >= 65:
        overall = "This qualifies as a BUY with good potential, though with some moderate factors."
    else:
        overall = "This meets minimum criteria but requires careful evaluation."

    print(f"\n{overall}\n")

    # Fundamental strength
    if fund_score >= 80:
        print(f"✓ EXCEPTIONAL FUNDAMENTALS (Score: {fund_score:.0f}/100)")
        growth = fund_details.get('revenue_growth', 0) * 100
        margin = fund_details.get('profit_margin', 0) * 100
        if growth > 1000:
            print(f"  • Strong revenue growth with expanding market opportunity")
        else:
            print(f"  • Revenue growing at {growth:.0f}% YoY - well above market")
        if margin > 1000:
            print(f"  • High profit margins indicating pricing power")
        else:
            print(f"  • Profit margin of {margin:.1f}% shows operational excellence")
        print(f"  • Financial foundation is rock-solid for sustained growth")
    elif fund_score >= 70:
        print(f"✓ STRONG FUNDAMENTALS (Score: {fund_score:.0f}/100)")
        print(f"  • Solid financial metrics with healthy growth trajectory")
        print(f"  • Balance sheet supports continued expansion")

    # Technical strength
    if tech_score >= 80:
        print(f"\n✓ STRONG TECHNICAL SETUP (Score: {tech_score:.0f}/100)")
        rsi = tech_details.get('rsi', 50)
        print(f"  • Price in strong uptrend with institutional accumulation")
        if 40 <= rsi <= 70:
            print(f"  • RSI at {rsi:.0f} - healthy momentum without overbought risk")
        if tech_details.get('macd_histogram', 0) > 0:
            print(f"  • MACD bullish crossover confirms positive momentum")
        print(f"  • Technical indicators aligned for continued appreciation")
    elif tech_score >= 70:
        print(f"\n✓ FAVORABLE TECHNICAL SETUP (Score: {tech_score:.0f}/100)")
        print(f"  • Chart pattern showing strength and positive momentum")

    print(f"\nWHY THIS STOCK:")
    sector = stock['sector']
    if sector == 'Technology' and 'Semiconductor' in stock['industry']:
        print(f"  → Semiconductor sector benefiting from AI/data center buildout")
        print(f"  → Strong secular tailwinds driving multi-year growth cycle")

    if fund_score >= 75 and tech_score >= 75:
        print(f"  → Combination of strong fundamentals + bullish technicals = high probability setup")

    print(f"\nRISK/REWARD ASSESSMENT:")
    if score >= 80:
        print(f"  • High conviction opportunity with favorable risk/reward ratio")
        print(f"  • Multiple factors aligned - worthy of larger position size")
    elif score >= 70:
        print(f"  • Good risk/reward with solid upside potential")
        print(f"  • Appropriate for core growth allocation")

    print(f"{'─'*80}\n")
    print("\n✅ New rationale section will appear in all future screening reports!")
