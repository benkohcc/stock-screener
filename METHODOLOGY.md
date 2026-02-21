# Stock Screening Methodology Reference

## Quick Overview

This document provides detailed reference information for the stock screening methodology. The main SKILL.md contains the workflow; this file contains the "why" and "how" behind each component.

---

## Scoring System Details

### Final Score Calculation

```
Final Score = (Fundamental × 0.30) + (Technical × 0.25) + (Catalyst × 0.30) + (Sentiment × 0.15)
```

### Component Weights Rationale

| Component | Weight | Why This Weight |
|-----------|--------|-----------------|
| Fundamental | 30% | Foundation of long-term value |
| Technical | 25% | Timing and entry point optimization |
| Catalyst | 30% | Drives short-term appreciation |
| Sentiment | 15% | Validates institutional interest |

**Note:** For 3-month timeframe, catalysts are weighted heavily because short-term moves require events/drivers.

---

## 1. Fundamental Analysis (30%)

### Scoring Breakdown (0-100)

#### Growth Metrics (40 points)
- **Revenue Growth** (20 pts max):
  - >30% YoY: 20 points
  - 20-30%: 15 points
  - 10-20%: 10 points
  - <10%: 5 points or less

- **Earnings Growth** (20 pts max):
  - >30% YoY: 20 points
  - 20-30%: 15 points
  - 10-20%: 10 points
  - <10%: 5 points or less

**Why It Matters:** Accelerating growth suggests market share gains, pricing power, or expanding TAM.

#### Financial Health (30 points)
- **Debt/Equity Ratio** (15 pts max):
  - <0.5: 15 points (strong balance sheet)
  - 0.5-1.0: 10 points (healthy)
  - 1.0-1.5: 5 points (moderate leverage)
  - >1.5: 0-2 points (risky)

- **Current Ratio** (15 pts max):
  - >2.0: 15 points (very liquid)
  - 1.5-2.0: 10 points (adequate)
  - 1.0-1.5: 5 points (tight)
  - <1.0: 0 points (liquidity risk)

**Why It Matters:** Financial flexibility allows companies to invest in growth and weather downturns.

#### Profitability (20 points)
- **Profit Margin** (10 pts max):
  - >20%: 10 points
  - 10-20%: 7 points
  - 5-10%: 4 points
  - <5%: 0-2 points

- **ROE** (10 pts max):
  - >20%: 10 points
  - 15-20%: 7 points
  - 10-15%: 4 points
  - <10%: 0-2 points

**Why It Matters:** High margins + ROE indicate competitive advantages and efficient capital allocation.

#### Valuation (10 points)
- **PEG Ratio** (10 pts max):
  - 0-1.0: 10 points (undervalued growth)
  - 1.0-1.5: 7 points (fair value)
  - 1.5-2.0: 4 points (slightly expensive)
  - >2.0: 0-2 points (overvalued)

**Why It Matters:** Growth-adjusted valuation prevents overpaying. PEG <1 means stock is cheap relative to growth.

---

## 2. Technical Analysis (25%)

### Scoring Breakdown (0-100)

#### Trend Strength (30 points)
- Price above 20-day MA: 10 points
- Price above 50-day MA: 10 points
- Price above 200-day MA: 5 points
- 50-day MA above 200-day MA (Golden Cross): 5 points

**Why It Matters:** Stocks in uptrends tend to continue. Multiple MA support levels provide cushion.

#### Momentum Indicators (30 points)
- **RSI (14-day)** (15 pts max):
  - 40-70 (sweet spot): 15 points
  - 30-40 or 70-80 (acceptable): 10 points
  - <30 (oversold): 5 points
  - >80 (overbought): 3 points

- **MACD** (15 pts max):
  - Histogram positive + MACD > Signal: 15 points
  - Histogram positive only: 10 points
  - Histogram negative but improving: 5 points
  - Histogram negative and weakening: 0 points

**Why It Matters:** RSI 40-70 shows bullish momentum without overbought risk. Positive MACD confirms trend.

#### Volume Profile (20 points)
- **Relative Volume** (10 pts max):
  - >1.5x average: 10 points
  - 1.2-1.5x: 5 points
  - <1.2x: 2 points

- **Up/Down Volume Ratio** (10 pts max):
  - >1.2 (more volume on up days): 10 points
  - 1.0-1.2: 5 points
  - <1.0 (distribution): 0-2 points

**Why It Matters:** High volume confirms moves. Accumulation (up volume > down volume) shows institutional buying.

#### Pattern Recognition (20 points)
- Higher highs in recent 20 days: 10 points
- Higher lows in recent 20 days: 10 points

**Why It Matters:** Higher highs + higher lows = confirmed uptrend. Technical definition of bullish pattern.

---

## 3. Catalyst Analysis (30%)

### Scoring Breakdown (0-100)

#### Earnings Catalysts (40 points)
- Upcoming earnings within 60 days: 30 points
- Recent analyst upgrades (2+ in last month): 20 points
- Positive earnings estimate revisions: 10 points

**Why It Matters:** Earnings beats drive short-term appreciation. Analyst activity signals changing sentiment.

#### Business Catalysts (40 points)
Examples (manual research required):
- Product launches (confirmed date): 15-20 points
- FDA approvals expected (drugs/devices): 20-25 points
- Major contract wins announced: 10-15 points
- M&A activity (target or acquirer): 15-25 points
- Regulatory tailwinds: 10-15 points

**Why It Matters:** Business events create fundamental re-rating opportunities.

#### Market Catalysts (20 points)
- Industry positioned in growing sector: 10 points
- Appropriate market cap for growth stage: 5 points
- Sector rotation favorable: 5 points

**Why It Matters:** Sector tailwinds lift all boats. Right market cap allows appreciation room.

---

## 4. Sentiment Analysis (15%)

### Scoring Breakdown (0-100)

#### Institutional Ownership (40 points)
- >70% institutional ownership: 40 points
- 50-70%: 30 points
- 30-50%: 20 points
- <30%: 10 points

**Why It Matters:** Institutions do deep research. High ownership validates quality.

#### Insider Activity (40 points)
Manual check via SEC Form 4:
- 3+ insiders buying (last 60 days, >$100k each): 40 points
- 2 insiders buying: 30 points
- 1 insider buying: 20 points
- No activity or selling: 5-10 points

**Why It Matters:** Insiders have best information. Cluster buying signals confidence.

#### Analyst Sentiment (20 points)
- Strong Buy / Buy recommendation: 20 points
- Hold: 10 points
- Sell: 0 points

**Why It Matters:** Analyst coverage affects institutional buying and price targets.

---

## Risk Assessment Framework

### Position Sizing Formula

```
Position Size = Base Size × Score Multiplier × Risk Adjustment

Where:
- Base Size: 10% (conservative) to 15% (moderate) of portfolio
- Score Multiplier: (Final Score / 80)
- Risk Adjustment: 0.7 (high volatility) to 1.0 (stable)
```

**Examples:**
- Stock scoring 85 with low volatility: 15% × (85/80) × 1.0 = 15.9% → 15% (capped at 20%)
- Stock scoring 70 with high volatility: 15% × (70/80) × 0.7 = 9.2%

### Stop Loss Calculation

**Initial Stop:** 15-20% below entry
- More volatile stocks: 20%
- More stable stocks: 15%

**Trailing Stop:** Once position up 10%+
- Move stop to breakeven (+0-2%)
- As stock appreciates, trail by 10-15%

**Catalyst-Based Stop:**
- If catalyst fails: Exit immediately (don't wait for price stop)
- If thesis breaks: Exit regardless of price

---

## Data Source Details

### Yahoo Finance (yfinance)
**Access:** `pip install yfinance`

**Available Data:**
- Historical OHLCV (unlimited history)
- Financial statements (annual + quarterly)
- Balance sheet, income statement, cash flow
- Key statistics (PE, PEG, margins, etc.)
- Analyst recommendations
- Earnings calendar
- Corporate actions (splits, dividends)

**Limitations:**
- 15-20 minute delay on prices
- Occasional data gaps for small caps
- Rate limiting on rapid requests

**Best Practice:** Cache data locally; don't re-fetch unnecessarily.

### SEC EDGAR
**Access:** https://www.sec.gov/edgar/searchedgar/companysearch.html

**Key Filings:**
- **Form 4:** Insider transactions (real-time)
- **13F:** Institutional holdings (quarterly, 45-day lag)
- **10-Q/10-K:** Quarterly/annual reports
- **8-K:** Material events

**Best Practice:** Check Form 4 filings weekly for insider buying clusters.

### Finviz Free Screener
**Access:** https://finviz.com/screener.ashx

**Use Case:** Initial filtering to create watchlist

**Key Filters:**
- Market Cap
- Fundamental metrics (growth, margins, ratios)
- Technical patterns
- Sector/Industry

**Limitation:** Max 100 results at once; cannot export directly.

---

## Common Pitfalls & Solutions

### Pitfall 1: Chasing Recent Winners
**Problem:** Screening stocks that already ran up 50%+
**Solution:** Filter out stocks up >30% in last month

### Pitfall 2: Ignoring Sector Context
**Problem:** Stock looks good, but sector is out of favor
**Solution:** Check sector ETF performance; avoid deteriorating sectors

### Pitfall 3: Overweighting Single Sector
**Problem:** All top picks are tech stocks
**Solution:** Cap sector exposure at 40% of portfolio

### Pitfall 4: Missing Negative Catalysts
**Problem:** Focusing only on positive drivers
**Solution:** Check for upcoming lockup expirations, debt maturities, regulatory issues

### Pitfall 5: Ignoring Liquidity
**Problem:** Small-cap stocks with low volume
**Solution:** Require minimum average volume (e.g., 500k shares/day)

---

## Customization Guide

### For More Conservative Approach
```python
screener.weights = {
    'fundamental': 0.50,  # Emphasize quality
    'technical': 0.15,
    'catalyst': 0.20,
    'sentiment': 0.15
}
min_score = 75  # Higher threshold
```

### For More Aggressive Approach
```python
screener.weights = {
    'fundamental': 0.20,
    'technical': 0.25,
    'catalyst': 0.40,  # Emphasize events
    'sentiment': 0.15
}
min_score = 60  # Lower threshold
```

### For Technical Focus
```python
screener.weights = {
    'fundamental': 0.20,
    'technical': 0.40,  # Emphasize charts
    'catalyst': 0.25,
    'sentiment': 0.15
}
```

---

## Validation & Backtesting

### How to Validate Methodology

1. **Paper Trading:** Track picks for 3 months without real money
2. **Historical Test:** Apply methodology to past dates, see how picks performed
3. **Component Analysis:** Which component (F/T/C/S) best predicts performance?
4. **Threshold Tuning:** Test different score thresholds (60 vs 70 vs 80)

### Success Metrics

Track:
- Win rate (% of positions with >0% return)
- Average gain on winners
- Average loss on losers
- Sharpe ratio (return/volatility)
- Maximum drawdown

**Realistic Expectations:**
- Win rate: 50-60% (good for high-risk strategy)
- Avg gain on winners: 30-50%
- Avg loss on losers: -15% (if stops honored)
- Max drawdown: 20-30% (portfolio level)

---

## Additional Resources

### For Further Research
- **SEC Filings:** Deep dive into 10-K/10-Q for business understanding
- **Earnings Call Transcripts:** Seeking Alpha, Yahoo Finance
- **Industry Reports:** IBISWorld, Statista (free summaries)
- **Economic Data:** FRED for macro context

### Technical Analysis Resources
- **TradingView:** Free charting with indicators
- **StockCharts.com:** Educational content
- **Investopedia:** Definitions and tutorials

### Fundamental Analysis
- **Macrotrends:** Free historical financials
- **EDGAR:** Primary source for SEC filings
- **Company investor relations:** Presentations, fact sheets

---

## Glossary

- **RSI:** Relative Strength Index (momentum oscillator, 0-100)
- **MACD:** Moving Average Convergence Divergence (trend-following momentum indicator)
- **PEG Ratio:** Price/Earnings-to-Growth ratio (P/E divided by growth rate)
- **ROE:** Return on Equity (net income / shareholder equity)
- **Current Ratio:** Current assets / current liabilities (liquidity measure)
- **Form 4:** SEC filing for insider transactions
- **13F:** SEC filing for institutional holdings (>$100M AUM)
- **Golden Cross:** 50-day MA crosses above 200-day MA (bullish signal)
- **Accumulation:** More volume on up days vs down days (bullish)

---

**This methodology is a starting point, not a complete system. Always conduct independent research and consult professionals before investing.**
