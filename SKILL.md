---
name: stock-screener
description: Identifies US Mid Cap and Large Cap stocks with high appreciation potential using a TWO-PHASE approach - (1) quantitative screening of 500 stocks using fundamental, technical, catalyst, and sentiment analysis, then (2) tiered web research validation (Tier 1: analyst/earnings/catalysts for all 15 candidates; Tier 2: deep fundamental dive including balance sheet, competitive position, management quality, and red flag screening for top 10 finalists) to produce thoroughly researched Top 10 recommendations. Use when asked to find growth stocks, screen stocks, analyze stock potential, or identify investment opportunities. Requires web search for validation phase.
allowed-tools: Read, Bash, Grep, Glob, WebSearch, WebFetch
---

# Stock Screener Skill

## Purpose

This skill identifies US stocks with strong appreciation potential using a **two-phase research-validated approach**:

**Phase 1: Quantitative Screening**
- Analyze ~100 stocks using 4-component scoring system
- Generate objective scores (0-100) based on fundamentals, technicals, catalysts, and sentiment
- Identify top 15 candidates for deeper research

**Phase 2: Research Validation (Tiered Approach)**
- **Tier 1** (All 15): Web search for analyst reports, earnings news, catalysts
- **Tier 2** (Top 10): Deep dive into balance sheet health, competitive position, management quality, red flags
- Validate that quantitative signals align with qualitative research
- Disqualify stocks where research conflicts OR critical red flags exist
- Generate detailed researched investment rationales for final Top 10

**Target Profile:**
- Market Cap: Mid Cap ($2B-$10B) and Large Cap ($10B+)
- Time Horizon: 3-month window (customizable)
- Strategy: High-risk, speculative growth plays
- Data Sources: Yahoo Finance (quantitative) + Web search (validation)

## When to Use This Skill

Activate this skill when the user asks to:
- Find stocks with high growth potential
- Screen stocks for appreciation opportunities
- Analyze specific stocks for investment potential
- Compare stocks for selection
- Identify stocks that could double or appreciate significantly
- Build a growth stock portfolio
- Evaluate stocks using fundamental and technical analysis

## Workflow

### Step 1: Understand User Requirements

First, gather the following information from the user (ask if not provided):

1. **Tickers**: Do they have specific stocks to analyze, or do they want help creating a watchlist?
2. **Market Cap**: Mid cap ($2B-$10B), Large cap ($10B+), or both?
3. **Sectors**: Any sector preferences or exclusions?
4. **Risk Tolerance**: Conservative, Moderate, or Aggressive?
5. **Time Horizon**: Default 3 months, or different timeframe?

**If user provides tickers**: Proceed directly to analysis.

**If screening from scratch**: Guide them to create initial watchlist:
- Suggest using Finviz free screener (https://finviz.com/screener.ashx)
- Provide specific filter criteria based on their preferences:
  - Market Cap: $2B+ (Mid/Large)
  - Revenue Growth (YoY): >20%
  - EPS Growth (YoY): >25%
  - Profit Margin: >10%
  - Debt/Equity: <1.0
- Once they provide 10-50 tickers, proceed to analysis

### Step 2: Set Up Python Environment

Before running analysis, check if dependencies are installed:

```bash
cd ~/.claude/skills/stock-screener
pip list | grep yfinance || pip install -r requirements.txt
```

### Step 3: Execute Two-Phase Research-Validated Screening

**IMPORTANT**: The screening process has TWO distinct phases:
- **Phase 1**: Python script performs quantitative analysis
- **Phase 2**: Claude performs web research validation

**You MUST execute BOTH phases** to complete the screening process.

---

#### Phase 1: Quantitative Screening (Python)

Run the Python screening script:

```bash
cd ~/.claude/skills/stock-screener
source venv/bin/activate
python run_real_screening.py
```

**What Phase 1 Does:**
- Screens 500 stocks (full S&P 500) using Yahoo Finance data
- Calculates 4-component scores (Fundamental, Technical, Catalyst, Sentiment)
- Identifies top 15 candidates (score ≥60)
- Saves results to: `~/Desktop/phase1_top15_{timestamp}.json`
- **Duration**: ~15-17 minutes

**IMPORTANT**: By default, this screens the **full S&P 500 universe (~500 stocks)** for comprehensive coverage. Do NOT use `--max-stocks` parameter unless the user explicitly requests a limited universe.

**Phase 1 Completion Signal:**
When Phase 1 completes, you will see:
```
⚠️  PHASE 1 COMPLETE - Top 15 Candidates Identified
================================================================================
📄 Candidates saved to: ~/Desktop/phase1_top15_YYYY-MM-DD_HHMMSS.json

Next: Claude will now execute Phase 2 research validation...
```

---

#### Phase 2: Research Validation (Claude - REQUIRED)

**CRITICAL**: Phase 2 MUST execute automatically after Phase 1 completes. Do NOT skip this step.

**Execution Workflow:**

1. **Read Phase 1 Output:**
   ```bash
   # Read the JSON file created by Phase 1
   Read ~/Desktop/phase1_top15_{timestamp}.json
   ```

2. **Establish Date Context for Searches:**

   Before executing searches, determine current date context to ensure searches are always current:

   - **Current Date**: [Today's date - e.g., "January 19, 2026"]
   - **Current Month**: [Month Year - e.g., "January 2026"]
   - **Current Year**: [Year - e.g., "2026"]
   - **Current Quarter**: [Q# Year - e.g., "Q1 2026"]
   - **Previous Quarter**: [Q# Year - e.g., "Q4 2025"]
   - **Last 90 Days Period**: [Calculate from today - e.g., "October 19, 2025 to January 19, 2026"]

   **Use these dynamic dates in all search queries below** (never use hardcoded dates like "January 2026").

3. **Source Quality Hierarchy:**

   When evaluating search results, prioritize sources in this order:

   **Tier 1 Sources (Highest Credibility - Use First):**
   - SEC filings (8-K, 10-K, 10-Q, earnings releases)
   - Company investor relations (press releases, earnings call transcripts)
   - Bloomberg, Reuters, Wall Street Journal, Financial Times

   **Tier 2 Sources (Credible - Use If Tier 1 Unavailable):**
   - Seeking Alpha (analyst articles, not comment sections)
   - CNBC, MarketWatch, Barron's
   - Named sell-side analyst reports (JPMorgan, Goldman Sachs, etc.)

   **Tier 3 Sources (Use With Caution):**
   - Seeking Alpha comments, Twitter/X posts (even from verified accounts)
   - Unnamed "sources familiar with the matter"
   - Promotional stock websites, investor forums

   **Rule**: If Tier 1 and Tier 3 sources conflict, always use Tier 1. If you must use Tier 3, explicitly note: "Per [source], treated as unconfirmed"

4. **Print Tier 1 Research Header:**

   Before beginning Tier 1 research, print this header to show progress:

   ```
   ================================================================================
   PHASE 2: RESEARCH VALIDATION - TIER 1 (Core Validation)
   ================================================================================
   Researching 15 candidates: Analyst actions, Earnings, Catalysts
   Estimated time: ~25-30 minutes
   ```

5. **For Each of the Top 15 Stocks, Execute WebSearch:**

   For each stock in the JSON, perform these searches:

   **IMPORTANT: Print progress before each stock:**
   ```
   [{current_index}/15] TIER 1: {TICKER} ({Company Name})
   ```

   **TIER 1: Core Validation (Mandatory - All 15 Stocks)**

   a. **Analyst Actions Search:**

   **Print progress:**
   ```
     → Searching analyst upgrades/downgrades...
   ```

   ```
   WebSearch: "{TICKER} analyst upgrade downgrade {CURRENT_MONTH} {CURRENT_YEAR}"
   WebSearch: "{TICKER} price target {CURRENT_YEAR}"
   ```

   **Extraction Process:**
   1. Scan results for articles from last 90 days (calculate: {LAST_90_DAYS_PERIOD})
   2. Extract ONLY from Tier 1/2 sources (Bloomberg, Reuters, WSJ, Seeking Alpha articles, company releases)
   3. For each analyst action found, record:
      - Firm name (e.g., "JPMorgan", "Bernstein")
      - Action (upgrade/downgrade/initiate/reiterate)
      - Price target (specific number + date)
      - Date of action (must be within 90 days from today)
      - Brief quote if available (analyst's rationale in 1 sentence)

   **Scoring This Category:**
   - ✅ **POSITIVE**: 2+ recent upgrades (within 90 days) OR street-high price target >20% above current price
   - ⚠️ **NEUTRAL**: Mixed (1 upgrade, 1 downgrade) OR only reiterations OR price targets <10% above current
   - ❌ **NEGATIVE**: 2+ recent downgrades (within 90 days) OR price target cuts

   **Search Strategy:**
   - First attempt: Use the exact query above
   - If no relevant results: Try "{TICKER} stock rating {CURRENT_YEAR}"
   - Maximum 2 search attempts
   - If both fail: Mark as NEUTRAL (not NEGATIVE) and note "Limited analyst coverage"

   b. **Earnings Search:**

   **Print progress:**
   ```
     → Searching earnings reports...
   ```

   ```
   WebSearch: "{TICKER} earnings report {PREVIOUS_QUARTER} OR {CURRENT_QUARTER}"
   WebSearch: "{TICKER} quarterly results latest"
   ```

   **Extraction Process:**
   1. Look for most recent quarterly earnings (typically reported within last 90 days)
   2. Extract from Tier 1 sources first (SEC filings, company IR), then Tier 2 (Bloomberg, WSJ, Reuters)
   3. For earnings found, record:
      - Quarter reported (e.g., "Q4 2025", "Q1 2026")
      - Report date (actual date earnings were released)
      - Revenue: Actual vs. estimate, YoY growth %
      - EPS: Actual vs. estimate, YoY growth %
      - Key metrics: Any standout numbers (margin expansion, user growth, etc.)
      - Forward guidance: Next quarter revenue/EPS guidance if provided

   **Scoring This Category:**
   - ✅ **POSITIVE**: Beat on revenue AND EPS, strong forward guidance (>10% growth), positive management commentary
   - ⚠️ **NEUTRAL**: Mixed (beat on one, miss on other) OR inline results OR guidance in-line with expectations
   - ❌ **NEGATIVE**: Miss on revenue OR EPS, weak/lowered guidance, negative management commentary

   **Search Strategy:**
   - First attempt: Use the exact query above
   - If no relevant results: Try "{COMPANY_NAME} earnings {CURRENT_YEAR}"
   - Maximum 2 search attempts
   - If both fail: Mark as NEUTRAL and note "Earnings pending for {EXPECTED_QUARTER}" (company may not have reported yet)

   c. **Catalyst Search:**

   **Print progress:**
   ```
     → Searching catalysts and upcoming events...
   ```

   ```
   WebSearch: "{TICKER} catalyst news {CURRENT_MONTH} {CURRENT_YEAR}"
   WebSearch: "{TICKER} upcoming events {CURRENT_YEAR}"
   ```

   **Extraction Process:**
   1. Look for concrete upcoming events (product launches, FDA approvals, contract wins, regulatory decisions)
   2. Focus on time-bound catalysts happening within next 90 days from today
   3. For each catalyst found, record:
      - Event type (product launch, FDA decision, earnings date, investor day, etc.)
      - Expected date or timeframe (e.g., "Q2 2026", "March 2026", "within 60 days")
      - Significance: Why this matters (market size, competitive advantage, revenue impact)
      - Source credibility (company announcement vs. rumor)

   **Scoring This Category:**
   - ✅ **POSITIVE**: Confirmed near-term catalyst (within 90 days) with material impact, multiple upcoming events
   - ⚠️ **NEUTRAL**: Catalyst exists but far-future (>90 days) OR low materiality OR unconfirmed rumors
   - ❌ **NEGATIVE**: Catalyst delays, failed FDA approval, lost contract, postponed events

   **Search Strategy:**
   - First attempt: Use the exact query above
   - If no relevant results: Try "{TICKER} product launch contract win {CURRENT_YEAR}"
   - Maximum 2 search attempts
   - If both fail: Mark as NEUTRAL and note "No near-term catalysts identified"

   **Print completion after each stock:**
   ```
     ✓ Tier 1 validation complete for {TICKER}
   ```

   **TIER 2: Fundamental Deep Dive (Top 10 Finalists After Tier 1)**

   **Print Tier 2 Research Header:**

   After Tier 1 validation completes, before beginning Tier 2, print this header:

   ```
   ================================================================================
   PHASE 2: RESEARCH VALIDATION - TIER 2 (Deep Dive)
   ================================================================================
   Deep diving {count} finalists: Balance sheet, Competitive position, Management, Red flags
   Estimated time: ~10-15 minutes
   ```

   After Tier 1 validation, for the top 10 survivors, perform additional fundamental validation:

   **IMPORTANT: Print progress before each stock:**
   ```
   [{current_index}/{total}] TIER 2: {TICKER} ({Company Name})
   ```

   d. **Balance Sheet & Liquidity Search:**

   **Print progress:**
   ```
     → Analyzing balance sheet & credit health...
   ```

   ```
   WebSearch: "{TICKER} debt refinancing {CURRENT_YEAR} credit rating"
   WebSearch: "{TICKER} cash position working capital {PREVIOUS_QUARTER}"
   ```

   **Extraction Process:**
   1. Look for credit rating actions (upgrades/downgrades) from last 180 days
   2. Search for debt refinancing news, covenant issues, liquidity concerns
   3. Extract latest balance sheet strength indicators from recent quarter
   4. For findings, record:
      - Credit rating: Current rating, any changes in last 180 days (Moody's, S&P, Fitch)
      - Debt concerns: Refinancing needs, covenant proximity, interest coverage
      - Cash position: Cash + equivalents, free cash flow trend
      - Liquidity issues: Any warnings about working capital, cash burn

   **Red Flag Detection:**
   - 🚨 **CRITICAL**: Credit downgrade within 180 days, covenant breach warning, liquidity crisis
   - ⚠️ **WARNING**: Credit on negative watch, rising debt/EBITDA, declining cash position
   - ✅ **POSITIVE**: Credit upgrade, strong cash position, debt paydown

   **Search Strategy:**
   - First attempt: Use the exact query above
   - If no relevant results: Try "{TICKER} balance sheet financial health {CURRENT_YEAR}"
   - Maximum 2 search attempts
   - If both fail: Note "No recent balance sheet concerns found"

   e. **Competitive Positioning Search:**

   **Print progress:**
   ```
     → Checking competitive position & market share...
   ```

   ```
   WebSearch: "{TICKER} market share gains {CURRENT_YEAR}"
   WebSearch: "{TICKER} losing customers competitors {CURRENT_YEAR}"
   ```

   **Extraction Process:**
   1. Look for market share data, competitive wins/losses from last 180 days
   2. Search for customer wins, contract awards, or customer losses
   3. Monitor pricing power indicators (price increases, margin expansion)
   4. For findings, record:
      - Market share: Gaining, flat, or losing (cite specific % if available)
      - Customer wins/losses: Named customers or contracts (quantify revenue impact if possible)
      - Competitive dynamics: New entrants, pricing pressure, consolidation
      - Pricing power: Recent price increases or margin trends

   **Red Flag Detection:**
   - 🚨 **CRITICAL**: Major customer loss (>10% revenue), collapsing market share, pricing collapse
   - ⚠️ **WARNING**: Gradual share erosion, increasing competitive intensity, pricing pressure
   - ✅ **POSITIVE**: Market share gains, customer wins, pricing power expansion

   **Search Strategy:**
   - First attempt: Use the exact query above
   - If no relevant results: Try "{TICKER} competitive position market share {CURRENT_YEAR}"
   - Maximum 2 search attempts
   - If both fail: Note "Limited competitive data available"

   f. **Management & Capital Allocation Search:**

   **Print progress:**
   ```
     → Reviewing management quality & insider activity...
   ```

   ```
   WebSearch: "{TICKER} insider buying selling {CURRENT_MONTH} {CURRENT_YEAR}"
   WebSearch: "{TICKER} CEO CFO management changes executive {CURRENT_YEAR}"
   ```

   **Extraction Process:**
   1. Search for insider transactions from last 90 days (Form 4 filings)
   2. Look for executive departures, appointments from last 180 days
   3. Review capital allocation decisions (buybacks, dividends, M&A)
   4. For findings, record:
      - Insider transactions: Who (role), what (buy/sell), when (date), size ($ amount)
      - Management changes: Role, who departed/joined, reason if disclosed, timing
      - Capital allocation: Buyback announcements, dividend changes, M&A activity

   **Red Flag Detection:**
   - 🚨 **CRITICAL**: CFO/CEO sudden departure without explanation, cluster of C-suite selling (3+ executives in 90 days)
   - ⚠️ **WARNING**: Moderate insider selling, unexplained executive turnover
   - ✅ **POSITIVE**: Insider buying clusters, stable management, shareholder-friendly capital allocation

   **Decision Logic for Insider Selling:**
   - Cluster (3+ executives within 90 days, unexplained) = 🚨 CRITICAL RED FLAG
   - Single executive with clear reason (10b5-1 plan, estate planning, diversification) = IGNORE
   - CFO/CEO selling with no explanation = 🚨 CRITICAL RED FLAG

   **Search Strategy:**
   - First attempt: Use the exact query above
   - If no relevant results: Try "{TICKER} management executive team {CURRENT_YEAR}"
   - Maximum 2 search attempts
   - If both fail: Note "No management red flags found"

   **TIER 3: Risk Screening (Critical Red Flags)**

   g. **Earnings Quality & Red Flags Search:**

   **Print progress:**
   ```
     → Screening for critical red flags (SEC, accounting, guidance)...
   ```

   ```
   WebSearch: "{TICKER} accounting investigation SEC inquiry restatement"
   WebSearch: "{TICKER} guidance raise lower {CURRENT_YEAR}"
   ```

   **Note:** First search looks at ALL TIME for accounting issues (not date-filtered - these are rare but critical). Second search should focus on recent guidance changes.

   **Extraction Process:**
   1. Search for SEC investigations, accounting inquiries (all time - these are critical regardless of age)
   2. Look for restatements, auditor warnings, unusual accounting practices
   3. Check guidance revisions from last 180 days
   4. For findings, record:
      - SEC/Accounting: Investigation status, inquiry topic, restatement details, timing
      - Guidance changes: Original vs. revised guidance, frequency of changes, direction (raise/lower)
      - Audit concerns: Auditor changes, going concern warnings, material weaknesses

   **Red Flag Detection:**
   - 🚨 **CRITICAL**: Active SEC investigation, accounting restatement, going concern warning, material weakness
   - ⚠️ **WARNING**: SEC inquiry (not formal investigation), repeated guidance cuts, auditor change
   - ✅ **POSITIVE**: Clean accounting, guidance raises, no audit concerns

   **Search Strategy:**
   - Maximum 2 search attempts for each query
   - If no red flags found: This is POSITIVE (absence of red flags = good news)
   - If guidance changes found: Assess if raised (positive), lowered (warning), or mixed

   **Print completion after each stock:**
   ```
     ✓ Tier 2 deep dive complete for {TICKER}
   ```

6. **Validate Research vs. Quantitative Signals:**

   **TIER 1 Validation (Initial Filter - All 15 Stocks):**

   Stock must meet **2 of 3 categories** to proceed to Tier 2:

   - ✅ **POSITIVE**: Analyst upgrades, earnings beats, strong guidance, concrete catalysts
   - ⚠️ **NEUTRAL**: Mixed signals or limited data
   - ❌ **NEGATIVE**: Downgrades, earnings misses, weak guidance, catalyst failures

   **TIER 2 Validation (Deep Dive - Top 10 After Tier 1):**

   Check for critical red flags that override quantitative scores:

   - 🚨 **CRITICAL RED FLAGS (Immediate Disqualification):**
     - Credit rating downgrade
     - SEC investigation or accounting inquiry
     - Major customer loss (>10% revenue)
     - CFO/CEO sudden departure without explanation
     - Accounting restatement
     - Debt covenant breach warnings

   - ⚠️ **WARNING SIGNS (Reduce Conviction):**
     - Insider selling clusters
     - Market share erosion
     - Guidance cuts
     - Rising customer churn
     - Competitive pricing pressure

   **Final Decision Logic:**

   - ✅ **KEEP**: Pass Tier 1 (2 of 3 positive) AND no critical red flags in Tier 2
   - ❌ **DISQUALIFY**: Fail Tier 1 OR any critical red flag in Tier 2

   **Edge Case Decision Tree:**

   **Scenario 1**: All three Tier 1 categories are NEUTRAL
   → Decision: PASS to Tier 2 (absence of negative = qualified, but lower confidence)

   **Scenario 2**: One NEGATIVE, two NEUTRAL in Tier 1
   → Decision: DISQUALIFY (fails 2-of-3 requirement)

   **Scenario 3**: One POSITIVE, one NEGATIVE, one NEUTRAL
   → Decision: DISQUALIFY (does not meet 2-of-3 POSITIVE requirement)

   **Scenario 4**: Warning signs in Tier 2 but no critical red flags
   → Decision: KEEP but reduce conviction tier, note in rationale: "Monitor: [warning sign]"

   **Scenario 5**: Insider selling detected
   → Before marking as warning, check if it's:
     - Cluster (3+ executives within 90 days) = WARNING SIGN
     - Single executive with clear reason (estate planning, diversification) = IGNORE
     - CFO/CEO with no explanation = CRITICAL RED FLAG

   **Scenario 6**: Credit rating under review (not yet downgraded)
   → Decision: WARNING SIGN (not critical red flag), but note in rationale

   **Scenario 7**: Earnings beat but weak guidance
   → Score as NEUTRAL (mixed signal), explain in rationale

   **Scenario 8**: Screening runs in different month (future-proofing)
   → All search queries dynamically use current month/quarter (e.g., if run in March 2026, searches use "March 2026", "Q1 2026")
   → "Last 90 days" is calculated from current date (not hardcoded)
   → Earnings expectations adjust: If run in Feb 2026, expect Q4 2025 or Q1 2026 results (not Q4 2024)

   **Scenario 9**: Stock hasn't reported recent quarter yet
   → If search finds no recent earnings because company hasn't reported yet = NEUTRAL (not NEGATIVE)
   → Note in rationale: "Earnings pending for {EXPECTED_QUARTER}"

6. **Verification Before Proceeding:**

   After completing research for each stock, verify:

   - [ ] All extracted data includes dates (no undated claims)
   - [ ] Analyst actions are within last 90 days from TODAY (calculate current date - 90 days dynamically)
   - [ ] Earnings data is from most recent reported quarter (check if Q4 2025, Q1 2026, etc. based on current date)
   - [ ] Quarter labels are correct (e.g., if today is Feb 2026, most recent should be Q4 2025 or Q1 2026)
   - [ ] Sources are credible (prioritize: SEC filings, company IR, Bloomberg, Reuters, WSJ, FT over blogs/rumors)
   - [ ] Contradictory information is flagged (e.g., "Source A says X, Source B says Y - using A because...")
   - [ ] "No information found" is distinguished from "negative information found"
   - [ ] Date ranges used in searches match current date context (not hardcoded to January 2026)

7. **Generate Researched Investment Rationale:**

   For each KEPT stock, create detailed rationale with:

   ```markdown
   ### #{RANK} - {COMPANY NAME} ({TICKER})
   **Score: {SCORE}/100 | Price: ${PRICE}**

   #### RESEARCHED INVESTMENT RATIONALE

   **Recent Analyst Actions:**
   - {FIRM} {upgraded/initiated} to ${TARGET} on {DATE}
   - {FIRM} street-high ${TARGET} target (+X% upside)
   - {FIRM} ${TARGET}: "{QUOTE from analyst}"

   **{QUARTER} Earnings ({DATE}):**
   - Revenue: ${X}B (+X% YoY)
   - EPS: ${X} (+X% YoY)
   - {Key metric}: {Actual number}

   **{NEXT_QUARTER} Guidance (The Catalyst):**
   - Revenue: ${X}B (+X% YoY)
   - EPS: ${X} (+X% YoY)
   - {Key guidance metric}

   **Fundamental Health Check:**
   - Balance Sheet: {Credit rating status, debt position, cash position}
   - Competitive Position: {Market share trend, competitive dynamics}
   - Management: {Insider activity, recent changes, capital allocation}

   **The Story:**
   Write 2-3 sentences that synthesize the research into a coherent investment thesis:
   - Sentence 1: The core driver (what's causing appreciation potential)
   - Sentence 2: The catalyst/timing (why now, what specific event)
   - Sentence 3: The confluence (how quantitative + qualitative align)

   **Example:**
   "Micron has sold out its entire 2026 HBM supply before product launch, creating unprecedented pricing power in a supply-constrained market with only 3 global competitors. The Q2 guidance (+440% YoY EPS) validates the AI memory cycle thesis that drove our quantitative score. With Rosenblatt's $500 price target implying 80% upside and no execution red flags in our deep dive, this is a rare alignment of fundamental strength, technical setup, and Wall Street conviction."

   **Avoid:** Generic statements like "Strong fundamentals and good technical setup create upside potential"

   **The Trade:**
   - Entry: ${LOW}-${HIGH}
   - Target: ${TARGET_PRICE}
   - Stop: ${STOP} (-X%)
   - Position: X-X% (conviction level based on Tier 2 findings)

   **Risk Factors:**
   - {Specific risk identified in research}
   - {Specific risk identified in research}
   - {Fundamental concerns from deep dive, if any}
   - {Warning signs from Tier 2, if applicable}
   ```

8. **Create Final Top 10 Report:**

   - Rank validated stocks by final score
   - Select top 10 (disqualify stocks where research conflicts or critical red flags exist)
   - If fewer than 10 survive validation, report actual count (quality over quantity)
   - Save to: `~/Desktop/TOP_10_STOCKS_{timestamp}.md`

**Phase 2 Duration**: ~35-45 minutes (includes Tier 1 validation for all 15 stocks + Tier 2 deep dive for top 10 finalists)

**Output File Format:**
```markdown
# TOP 10 STOCKS - Research-Validated Analysis
Generated: {DATE} {TIME}

## Summary
- Screened: {N} stocks
- Qualified (≥60): {N} stocks
- Top 15 Researched: 15 stocks
- **Final Top 10**: {N} stocks (after research validation)

## Top 10 Stocks

### #1 - {TICKER}
{Researched rationale as shown above}

### #2 - {TICKER}
...

## Portfolio Construction
{Allocation guidance, diversification, position sizing}

## Risk Disclaimer
{Standard disclaimer}
```

---

**Alternative: Quick Quantitative Analysis Only**

For quick analysis without research validation (use ONLY when time-constrained or user explicitly requests):

```bash
cd ~/.claude/skills/stock-screener
source venv/bin/activate
python -c "
from stock_screener import StockScreener
screener = StockScreener()
result = screener.calculate_final_score('TICKER')
if result:
    print(f\"{result['ticker']}: {result['final_score']:.1f}/100 - {result['rating']}\")
"
```

Note: This provides quantitative scores only, without research validation. Generic rationales, not researched.

### Step 4: Analyze Results

The screener outputs scores based on four components:

**1. Fundamental Analysis (30% weight)**
- Growth: Revenue/earnings growth rates
- Health: Debt ratios, liquidity
- Profitability: Margins, ROE
- Valuation: P/E, PEG ratios

**2. Technical Analysis (25% weight)**
- Trend: Moving average alignment
- Momentum: RSI, MACD signals
- Volume: Accumulation patterns
- Patterns: Breakouts, support/resistance

**3. Catalyst Analysis (30% weight)**
- Timing: Upcoming events (earnings, FDA approvals, etc.)
- Impact: Expected magnitude
- Multiple catalysts: Number of positive drivers

**4. Sentiment Analysis (15% weight)**
- Insider: Form 4 filings (buying activity)
- Institutional: Ownership percentage
- Analyst: Recommendations, upgrades

**Scoring Thresholds:**
- **80-100**: STRONG BUY - High conviction setup
- **65-79**: BUY - Favorable risk/reward
- **50-64**: HOLD - Monitor only
- **<50**: PASS - Does not meet criteria

### Step 5: Review Research-Validated Results

After the screening completes, review the output files on the user's Desktop:

**Primary Output: `~/Desktop/TOP_10_STOCKS_YYYY-MM-DD_HHMMSS.md`**

This timestamped file contains the final Top 10 validated stocks with detailed researched investment rationales. Each stock includes:

- **Researched Investment Rationale**: Real analyst upgrades with specific price targets, dates, and firm names (e.g., "Bernstein upgraded to $330 on Jan 2")
- **Actual Earnings Data**: Real quarterly results and guidance numbers (e.g., "Q2 EPS $8.42, +440% YoY")
- **Specific Catalysts**: Concrete events with timelines (not generic templates)
- **Component Scores**: Fundamental, Technical, Catalyst, Sentiment breakdown
- **The Trade**: Entry price, target, stop loss, position size recommendations
- **Risk Factors**: Specific risks identified during research

**Key Difference from Traditional Screeners:**

The research validation phase ensures that:
- Quantitative buy signals are validated by current market sentiment
- Stocks where research conflicts with buy signals are disqualified (not forced into the Top 10)
- Investment rationales are based on recent analyst reports and earnings data (not generic templates)

**Secondary Output: `~/Desktop/screening_results_YYYY-MM-DD_HHMMSS.csv`**

Contains all stocks scoring ≥60 with quantitative metrics and basic rationale (37+ stocks typically).

**Process Log: `~/Desktop/screening_output_YYYY-MM-DD_HHMMSS.log`**

Full console output showing the screening process (only when using `run_screening.sh`).

**Note**: All files include timestamps (format: YYYY-MM-DD_HHMMSS) to prevent overwrites from multiple screening runs.

### Step 6: Portfolio Construction Guidance

Provide portfolio-level recommendations:

```
## Recommended Portfolio

**Allocation:**
1. TICKER1: X% (Sector: XX)
2. TICKER2: X% (Sector: XX)
3. TICKER3: X% (Sector: XX)
...

**Diversification Check:**
- Total positions: X
- Sectors represented: [List]
- Max single position: X%
- Geographic diversity: [US-based, International revenue %]

**Position Sizing Logic:**
- Higher scores → Larger positions (up to 20% max)
- Diversify across sectors (max 2 per sector)
- Leave 20-30% cash for opportunities

**Risk Management:**
- Portfolio stop loss: -15% overall
- Individual stops: 15-20% per position
- Rebalance trigger: Any position >25% of portfolio
```

### Step 7: Monitoring Plan

Provide actionable monitoring guidance:

```
## Monitoring & Management Plan

**Daily Tasks:**
- Check prices and volume
- Scan news for catalyst updates
- Monitor stop loss levels

**Weekly Review:**
- Re-run screening on positions
- Check for score changes
- Adjust trailing stops
- Review thesis validity

**Key Dates to Watch:**
- [TICKER1]: Earnings on [DATE]
- [TICKER2]: [Catalyst event] on [DATE]
- [TICKER3]: [Event] expected [TIMEFRAME]

**Exit Triggers:**
- Stop loss hit (-15-20%)
- Catalyst fails to materialize
- Thesis breaks (score drops below 50)
- Better opportunities emerge

**Profit Taking Strategy:**
- Take 25% off at +25% gain
- Take 25% off at +50% gain (target reached)
- Trail remainder with 10-15% stop
```

### Step 8: Risk Disclaimer

**ALWAYS include this critical disclaimer:**

```
⚠️ RISK DISCLAIMER

This analysis is for EDUCATIONAL PURPOSES ONLY. It is NOT financial advice.

**Critical Warnings:**
- 50% appreciation in 3 months = ~267% annualized return (EXTREMELY RARE)
- This is a HIGH-RISK, SPECULATIVE strategy
- Significant downside risk exists
- Use ONLY risk capital you can afford to lose completely
- Past performance does NOT guarantee future results
- Consult a licensed financial advisor before investing

**Methodology Limitations:**
- Based on historical data (backward-looking)
- Cannot predict black swan events
- Free data sources have delays
- Catalyst timing is uncertain
- Market conditions change rapidly

**Your Responsibility:**
- Verify all data independently
- Conduct your own due diligence
- Understand each investment thoroughly
- Never invest more than you can afford to lose
```

## Advanced Features

### Universe Selection (Dynamic Stock List)

**Default behavior:** Automatically fetches S&P 500 constituents from Wikipedia (~500 stocks, live data)

The screener now supports dynamic universe fetching with multiple modes:

```bash
# Default: S&P 500 from Wikipedia (recommended)
python run_real_screening.py

# NASDAQ 100 only (~100 stocks)
python run_real_screening.py --mode nasdaq100

# Sector-specific screening
python run_real_screening.py --mode tech        # Technology stocks only
python run_real_screening.py --mode healthcare  # Healthcare stocks only
python run_real_screening.py --mode growth      # Tech + Healthcare + Consumer

# Limit to specific number (ONLY use when user explicitly requests it)
python run_real_screening.py --max-stocks 200

# Use custom config file
python run_real_screening.py --mode file
```

**IMPORTANT - When to use --max-stocks:**
- **Default behavior (RECOMMENDED)**: Do NOT include `--max-stocks` → screens full 500 stocks
- **Only use --max-stocks when**: User explicitly requests a limited universe (e.g., "screen only 200 stocks", "just check 100 stocks")
- **Do NOT use --max-stocks when**: User asks general questions like "find stocks that could double" or "screen for growth stocks" - use the full 500-stock default

**How it works:**
1. **Live sources first**: Fetches current index constituents from Wikipedia
2. **Graceful fallback**: Uses curated hardcoded list if live fetch fails
3. **Config file**: Only used when explicitly requested with `--mode file`

**Performance:**
- 500 stocks: ~15-17 min (Phase 1) + 35-45 min (Phase 2) = ~50-62 min total
- 100 stocks: ~3-4 min (Phase 1) + 35-45 min (Phase 2) = ~38-49 min total

### Custom Weighting

If user wants different emphasis (e.g., more fundamental-focused):

```python
screener = StockScreener()
screener.weights = {
    'fundamental': 0.50,  # Increased
    'technical': 0.15,
    'catalyst': 0.20,
    'sentiment': 0.15
}
```

### Comparing Stocks Head-to-Head

For 2-stock comparisons, create comparison table showing all metrics side-by-side.

## Supporting Files

- **README.md**: User-facing documentation with Quick Start guide and two-phase methodology
- **METHODOLOGY.md**: Detailed explanation of the screening methodology, scoring system, and research approach
- **run_real_screening.py**: Phase 1 quantitative screening script (saves top 15 to JSON for Claude's Phase 2)
- **stock_screener.py**: Core scoring engine with StockScreener class (Phase 1 quantitative analysis)
- **universe_fetcher.py**: Dynamic universe fetching from Wikipedia, yfinance, and config files
- **universe_config.yaml**: Optional config file for custom universe definitions (used with `--mode file`)
- **yahoo_api_fetcher.py**: Alternative data fetcher (currently unused, yfinance preferred)
- **requirements.txt**: Python dependencies (yfinance, pandas, numpy, beautifulsoup4, lxml, pyyaml)
- **venv/**: Python 3.11 virtual environment with all dependencies

Refer to README.md for:
- Quick start instructions
- Two-phase methodology explanation
- Output files description
- Troubleshooting guide

Refer to METHODOLOGY.md for:
- Detailed scoring algorithms
- Technical indicator calculations
- Fundamental metric definitions
- Catalyst identification strategies
- Risk management frameworks

## Output Best Practices

1. **Use Research-Validated Rationales**: Always prefer researched rationales with specific analyst data over generic templates
2. **Show Scores**: Always display component scores and final score for transparency
3. **Validate with Research**: If quantitative score conflicts with web research, acknowledge the conflict and adjust recommendation
4. **Be Specific**: Include actual analyst names, price targets, dates, and earnings numbers (not generic phrases)
5. **Be Realistic**: Emphasize the high-risk nature, don't oversell
6. **Provide Actions**: Clear next steps (entry points, stops, monitoring)
7. **Include Dates**: Specific catalyst timelines (e.g., "Q2 earnings on Feb 15" not "upcoming earnings")
8. **Highlight Risks**: Be upfront about what could go wrong, including research-identified concerns
9. **Disqualify Conflicts**: Remove stocks from recommendations where research contradicts buy signals

## Common Scenarios

### Scenario 1: "Find me stocks that could double"
**Use the research-validated screening approach:**

1. **Execute Phase 1**: Run `python run_real_screening.py` (screens **full S&P 500 universe, ~500 stocks**)
   - Wait for completion (~15-17 min)
   - Python identifies top 15 candidates and saves to JSON

2. **Execute Phase 2** (YOUR responsibility as Claude):
   - Read `~/Desktop/phase1_top15_{timestamp}.json`
   - **Tier 1 (All 15 stocks)**: Execute WebSearch for analyst reports, earnings, catalysts
   - **Tier 2 (Top 10 after Tier 1)**: Execute WebSearch for balance sheet, competitive position, management, red flags
   - Validate quantitative signals with research
   - Disqualify stocks with critical red flags (SEC investigations, credit downgrades, CFO departures, etc.)
   - Generate researched investment rationales (specific data, not templates)
   - Create final report: `~/Desktop/TOP_10_STOCKS_{timestamp}.md`
   - Duration: ~35-45 min

3. **Present Results**:
   - Direct user to `~/Desktop/TOP_10_STOCKS_{timestamp}.md` (timestamped file)
   - Highlight stocks scoring ≥80 (highest conviction)
   - Provide portfolio construction guidance based on validated Top 10

**CRITICAL**: Do NOT skip Phase 2. The two-phase process is mandatory for research-validated results.

**NOTE**: Use the default command WITHOUT `--max-stocks` parameter for comprehensive screening.

### Scenario 2: "Analyze AAPL, MSFT, GOOGL"
1. Run screening on all three
2. Generate scores and rankings
3. Provide detailed analysis for each
4. Recommend best 1-2 based on scores
5. Compare and contrast

### Scenario 3: "Update my watchlist from last week"
1. Ask for previous tickers
2. Re-run analysis
3. Show score changes (▲▼)
4. Flag new catalysts or concerns
5. Update buy/hold/sell recommendations

### Scenario 4: "What tech stocks look good?"
1. Suggest a tech stock watchlist (AAPL, MSFT, NVDA, AMD, etc.)
2. Run screening
3. Present results ranked by score
4. Deep dive on top 3

## Troubleshooting

### If data retrieval fails:
- Check internet connection
- Verify ticker symbols are correct (use Yahoo Finance format)
- Try again (rate limits may apply)
- Use alternative tickers

### If all scores are low:
- Explain market conditions may not be favorable
- Suggest trying different sectors
- Consider lowering threshold to 55-60
- Provide educational value on what makes a good setup

### If Python errors occur:
- Verify dependencies installed: `pip install -r requirements.txt`
- Check Python version (3.11+ required for OpenSSL 3.x compatibility)
- SSL/HTTPS errors indicate older Python - upgrade to 3.11+
- Virtual environment at `~/.claude/skills/stock-screener/venv/` uses Python 3.11.14
- Read error message and debug

## Success Criteria

A successful research-validated screening includes:
- ✅ Phase 1 quantitative screening completed (500 stocks → top 15 saved to JSON)
- ✅ Phase 2 web research validation completed (top 15 researched → final 10)
- ✅ Researched investment rationales with specific analyst data (not generic templates)
- ✅ Actual earnings numbers and guidance (not estimates)
- ✅ Specific catalysts with dates and timelines
- ✅ Component score breakdown for each stock
- ✅ Entry/exit levels and position sizing
- ✅ Risk factors identified during research
- ✅ Portfolio construction guidance
- ✅ Comprehensive risk disclaimer
- ✅ Output files saved to `~/Desktop/` with timestamps to prevent overwrites

## Notes

- This skill uses ONLY free data sources:
  - **Phase 1**: Yahoo Finance API (yfinance library) for quantitative data
  - **Phase 2**: Web search for analyst reports, earnings news, and validation
- **Timing**:
  - Phase 1: ~15-17 minutes (500 stocks quantitative screening by Python)
  - Phase 2: ~35-45 minutes (Tier 1 validation of 15 stocks + Tier 2 deep dive of top 10 by Claude)
  - Total: ~50-62 minutes for complete research-validated screening
- **Python Environment**: Requires Python 3.11+ with OpenSSL 3.x (for Yahoo Finance SSL compatibility)
- **Output Location**: All results saved to `~/Desktop/` with timestamps (YYYY-MM-DD_HHMMSS) to prevent overwrites
- **File Naming**: Each screening run creates uniquely timestamped files for historical tracking
- User should verify all information independently
- This is a starting point for research, not a complete investment decision

---

**Remember**: Always validate quantitative signals with qualitative research. Use researched rationales with specific data (analyst targets, earnings numbers, dates), not generic templates. If research conflicts with buy signals, disqualify the stock. Be objective, show your work, emphasize risk, and provide actionable guidance. The goal is to help users make informed decisions, not to guarantee returns.
