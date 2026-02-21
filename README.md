# Stock Screener - Research-Validated Approach

A Claude Code skill for identifying high-growth potential stocks using a **two-phase research-validated methodology**.

## Quick Start

**Recommended: Full Research-Validated Screening**

```bash
cd ~/.claude/skills/stock-screener
source venv/bin/activate
python run_real_screening.py
```

**IMPORTANT**: This runs Phase 1 only (Python quantitative screening). Claude must execute Phase 2 (research validation) after Phase 1 completes.

- **Phase 1 Time**: ~15-17 minutes (Python)
- **Phase 2 Time**: ~35-45 minutes (Claude - includes Tier 1 + Tier 2 validation)
- **Total Time**: ~50-62 minutes
- **Phase 1 Output**: `~/Desktop/phase1_top15_YYYY-MM-DD_HHMMSS.json` (top 15 candidates)
- **Phase 2 Output**: `~/Desktop/TOP_10_STOCKS_YYYY-MM-DD_HHMMSS.md` (researched top 10)
- **What you get**: Top 10 stocks with researched investment rationales (not generic templates)

---

## Two-Phase Methodology

### Phase 1: Quantitative Screening (~15-17 min) - Python

**Executed by**: `run_real_screening.py` Python script

- Analyzes **500 stocks** (full S&P 500) using Yahoo Finance real-time data
- Scores 0-100 based on 4 components:
  - **Fundamental** (30%): Revenue growth, margins, ROE, P/E
  - **Technical** (25%): RSI, MACD, trend strength, volume
  - **Catalyst** (30%): Upcoming earnings, industry trends
  - **Sentiment** (15%): Institutional ownership, analyst ratings
- Identifies top 15 candidates (score ≥60)
- Saves to: `~/Desktop/phase1_top15_{timestamp}.json`

### Phase 2: Research Validation (~35-45 min) - Claude

**Executed by**: Claude using WebSearch tool (after Phase 1 completes)

**Tier 1 Validation (All 15 stocks):**
- Web search for analyst reports, earnings news, catalysts
- Initial validation: Stock must pass 2 of 3 categories (Analyst/Earnings/Catalysts)

**Tier 2 Deep Dive (Top 10 after Tier 1):**
- Balance sheet & liquidity (credit ratings, debt concerns, cash position)
- Competitive positioning (market share, customer wins/losses)
- Management quality (insider trading, executive changes, capital allocation)
- Red flag screening (SEC investigations, accounting issues, guidance cuts)

**Critical Red Flags (Immediate Disqualification):**
- Credit rating downgrade
- SEC investigation or accounting inquiry
- CFO/CEO sudden departure
- Major customer loss (>10% revenue)
- Accounting restatement
- Debt covenant breach

**Final Output** - Generates researched investment rationale for Top 10:
- Recent analyst upgrades with price targets and dates
- Actual earnings numbers and guidance
- Specific catalysts with timelines
- Fundamental health check results
- Industry/sector trends
- Risk factors (including deep dive findings)
- Saves to: `~/Desktop/TOP_10_STOCKS_{timestamp}.md`

---

## What Makes This Different

**Traditional stock screeners:**
- Generic rationales: "Strong fundamentals, good setup"
- No validation against current news/analyst sentiment
- Risk of outdated information

**This research-validated screener:**
- Searches latest analyst reports (current month)
- Finds specific price targets (e.g., "Bernstein $330, Rosenblatt $500")
- Actual earnings guidance (e.g., "Q2 EPS $8.42, +440% YoY")
- **Deep fundamental validation** (balance sheet health, competitive position, management quality)
- **Red flag screening** (SEC investigations, credit downgrades, executive departures)
- **Removes stocks** where research contradicts buy signal OR critical red flags exist

Example: DXCM scored 70.6 but was disqualified after research found Barclays downgrade and -16.7% YoY performance.

---

## Output Files

All saved to **`~/Desktop/`** with timestamps to prevent overwrites:

### Phase 1 Output (Python)

1. **phase1_top15_YYYY-MM-DD_HHMMSS.json** (~10KB)
   - Top 15 candidates with quantitative scores
   - Input for Phase 2 research validation
   - **IMPORTANT**: Claude reads this file to execute Phase 2

2. **screening_results_YYYY-MM-DD_HHMMSS.csv** (~50KB)
   - All stocks scoring ≥60 (typically 37+)
   - Includes quantitative scores only
   - Reference file for full screening results

### Phase 2 Output (Claude)

3. **TOP_10_STOCKS_YYYY-MM-DD_HHMMSS.md** (~50KB)
   - Detailed analysis for validated Top 10
   - Researched investment rationales (analyst data, earnings, catalysts)
   - Portfolio construction guidance
   - **PRIMARY OUTPUT**: This is what users should read

**Example filenames:**
- Phase 1: `phase1_top15_2026-01-18_143522.json`
- Phase 1: `screening_results_2026-01-18_143522.csv`
- Phase 2: `TOP_10_STOCKS_2026-01-18_143522.md`

---

## How to Use

### Automatic Activation

The skill automatically activates when you ask:
- "Find stocks likely to appreciate 50% in 3 months"
- "Screen for high-growth stocks"
- "Identify investment opportunities"
- "What stocks should I buy?"

### Manual Invocation

Run the screener directly:
```bash
bash ~/.claude/skills/stock-screener/run_screening.sh
```

Or in Python:
```bash
cd ~/.claude/skills/stock-screener
source venv/bin/activate
python run_real_screening.py
```

---

## Files

- **SKILL.md**: Claude Code skill definition
- **README.md**: This file
- **METHODOLOGY.md**: Detailed scoring methodology
- **stock_screener.py**: 4-component scoring engine
- **run_real_screening.py**: Phase 1 screening script (saves top 15 to JSON)
- **universe_fetcher.py**: Dynamic universe fetching (Wikipedia, Yahoo API, config files)
- **yahoo_api_fetcher.py**: Alternative data fetcher (currently unused)
- **requirements.txt**: Python dependencies
- **venv/**: Python 3.11 virtual environment

---

## Requirements

**Python Environment:**
- Python 3.11+ (for OpenSSL 3.x compatibility with Yahoo Finance)
- Virtual environment already set up at `~/.claude/skills/stock-screener/venv/`

**Dependencies** (already installed):
- yfinance
- pandas
- numpy

**To reinstall dependencies:**
```bash
cd ~/.claude/skills/stock-screener
source venv/bin/activate
pip install -r requirements.txt
```

---

## Customization

### Universe Selection

By default, the screener **automatically fetches S&P 500 constituents from Wikipedia** (~500 stocks, live data).

**Available Modes:**

```bash
# Default: S&P 500 from Wikipedia (recommended)
python run_real_screening.py

# NASDAQ 100 only
python run_real_screening.py --mode nasdaq100

# Combined S&P 500 + NASDAQ 100
python run_real_screening.py --mode combined

# Sector-specific screening
python run_real_screening.py --mode tech        # Technology stocks only
python run_real_screening.py --mode healthcare  # Healthcare stocks only
python run_real_screening.py --mode growth      # Tech + Healthcare + Consumer

# Limit the number of stocks
python run_real_screening.py --max-stocks 200   # Screen only 200 stocks

# Use custom config file
python run_real_screening.py --mode file        # Reads from universe_config.yaml
```

**How It Works:**

1. **Live Data Priority**: Fetches current index constituents from Wikipedia
2. **Graceful Fallback**: Uses curated hardcoded list if live fetch fails
3. **Config File**: Only used when explicitly requested with `--mode file`

**Performance by Universe Size:**

| Stocks | Phase 1 (Screening) | Phase 2 (Research) | Total |
|--------|---------------------|-------------------|-------|
| 500    | ~15-17 min         | ~35-45 min        | ~50-62 min |
| 200    | ~6-7 min           | ~35-45 min        | ~41-52 min |
| 100    | ~3-4 min           | ~35-45 min        | ~38-49 min |

**Creating Custom Universe:**

Edit `universe_config.yaml`:
```yaml
filters:
  indices: [sp500, nasdaq100]
  sectors: [Technology]
  min_market_cap: 5000000000  # $5B
  max_stocks: 150
```

Then run:
```bash
python run_real_screening.py --mode file
```

### Adjust Minimum Score

Default: 60 (qualified stocks)

Change in `run_real_screening.py` line 88:
```python
if result and result['final_score'] >= 60:  # Change threshold here
```

---

## Rating Scale

- **80-100**: STRONG BUY - Exceptional characteristics
- **70-79**: SOLID BUY - Strong fundamentals and setup
- **65-69**: BUY - Good potential
- **60-64**: QUALIFIED - Meets minimum criteria
- **<60**: Excluded from results

---

## Monitoring Progress

Since the full screening takes 50-62 minutes, you can monitor progress in real-time:

### **Phase 1 Progress (Python Screening)**

**What you'll see:**
```
[127/500 - 25.4%] AAPL | Elapsed: 5.2m | ETA: 15.8m ✓ Score: 69.5 - BUY
[128/500 - 25.6%] MSFT | Elapsed: 5.3m | ETA: 15.7m ○ Score: 53.2 (below threshold)
```

**Progress indicators:**
- `[127/500 - 25.4%]`: Current stock, total stocks, completion percentage
- `Elapsed: 5.2m`: Time since screening started
- `ETA: 15.8m`: Estimated time remaining
- `✓`: Passed (score ≥60), `○`: Below threshold, `✗`: Error

**How to monitor:**
- **If running in foreground:** Progress appears automatically in terminal
- **If running in background:** Ask Claude to check progress using bash process ID

### **Phase 2 Progress (Claude Research)**

**What you'll see:**
```
================================================================================
PHASE 2: RESEARCH VALIDATION - TIER 1 (Core Validation)
================================================================================
Researching 15 candidates: Analyst actions, Earnings, Catalysts
Estimated time: ~25-30 minutes

[1/15] TIER 1: AAPL (Apple Inc.)
  → Searching analyst upgrades/downgrades...
  → Searching earnings reports...
  → Searching catalysts and upcoming events...
  ✓ Tier 1 validation complete for AAPL

[2/15] TIER 1: MSFT (Microsoft Corporation)
  ...
```

**Progress indicators:**
- Tier headers show which phase (Tier 1 or Tier 2) and estimated time
- `[3/15]`: Current stock number out of total
- `→`: Currently researching this category
- `✓`: Category or stock completed

**How to monitor:**
- Phase 2 progress appears in Claude's chat responses as it executes
- Each stock's research categories are shown in real-time

### **Checking Background Processes**

If Phase 1 is running in the background, ask Claude:
```
"Check progress of my screening"
```

Claude will use the BashOutput tool to show the latest progress.

---

## Troubleshooting

**SSL/HTTPS errors:**
- Need Python 3.11+ (current venv has 3.11.14)
- OpenSSL 3.x required (current venv has 3.6.0)

**Module not found:**
```bash
cd ~/.claude/skills/stock-screener
source venv/bin/activate
pip install -r requirements.txt
```

**Screening too slow:**
- Phase 1 (quantitative): ~15-17 min is normal for 500 stocks
- Phase 2 (research): ~35-45 min is normal (Tier 1 + Tier 2 validation with web search rate limits)
- Total ~50-62 min cannot be reduced
- This is a comprehensive screening with deep fundamental validation - time reflects thoroughness

---

## Example Output

From `TOP_10_STOCKS_RESEARCHED.md`:

```markdown
### #1 - MICRON TECHNOLOGY (MU)
**Score: 78.5/100 | Price: $362.75**

#### RESEARCHED INVESTMENT RATIONALE

**Recent Analyst Actions:**
- Bernstein upgraded to $330 (Jan 2, triggered 7.5% pop)
- Rosenblatt street-high $500 target (+80% upside)
- JPMorgan $350: "Blowout quarter validates AI memory cycle"

**Q1 FY2026 Earnings (Dec 2025):**
- Revenue: $13.6B (+56% YoY)
- EPS: $4.60 (+175% YoY)

**Q2 Guidance (The Catalyst):**
- Revenue: $18.7B (+38% YoY)
- EPS: $8.42 (+440% YoY) ← Key number
- Gross margins: 67%

**The HBM Story:**
Micron has sold out entire 2026 HBM supply, including next-gen
HBM4 before it ships. Only 3 global suppliers creates pricing power.

**The Trade:**
- Entry: $360-375
- Target: $500-550
- Stop: $315 (-13%)
- Position: 15-20% (highest conviction)
```

---

## Data Sources

**Quantitative (Phase 1):**
- Yahoo Finance API (yfinance library)
- Real-time price data
- Historical technicals (180 days)

**Qualitative (Phase 2):**
- Web search for analyst reports
- Recent news and earnings announcements
- Current market sentiment

All sources are **free** (no paid subscriptions required).

---

## Disclaimer

⚠️ **HIGH-RISK STRATEGY - Educational purposes only. NOT financial advice.**

- 50% in 3 months = 267% annualized (extremely rare)
- Stocks can decline 30-50%+ in corrections
- Use ONLY risk capital you can afford to lose completely
- Verify all data independently
- Consult a licensed financial advisor before investing
- Past performance does NOT guarantee future results

---

## Version History

- **v2.0** (Jan 18, 2026): Added research validation phase
- **v1.0** (Jan 2026): Initial quantitative screener

---

**Created**: January 2026
**Last Updated**: January 18, 2026
**Python**: 3.11.14
**Status**: Production-ready
