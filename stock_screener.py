"""
Stock Screener Implementation
Based on the comprehensive screening methodology guide
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


class StockScreener:
    """
    Comprehensive stock screening system for identifying high-growth potential stocks
    """

    def __init__(self):
        self.weights = {
            'fundamental': 0.30,
            'technical': 0.25,
            'catalyst': 0.30,
            'sentiment': 0.15
        }

    # ==================== DATA RETRIEVAL ====================

    def get_stock_data(self, ticker: str, period: str = '1y') -> Dict:
        """
        Fetch comprehensive stock data

        Args:
            ticker: Stock ticker symbol
            period: Time period ('1y', '2y', etc.)

        Returns:
            Dictionary with price data, fundamentals, and info
        """
        try:
            stock = yf.Ticker(ticker)

            data = {
                'ticker': ticker,
                'history': stock.history(period=period),
                'info': stock.info,
                'financials': stock.financials,
                'balance_sheet': stock.balance_sheet,
                'cashflow': stock.cashflow,
                'quarterly_financials': stock.quarterly_financials,
                'recommendations': stock.recommendations,
                'calendar': stock.calendar
            }

            return data

        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None

    # ==================== TECHNICAL ANALYSIS ====================

    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi.iloc[-1] if len(rsi) > 0 else 50

    def calculate_macd(self, prices: pd.Series) -> Tuple[float, float, float]:
        """Calculate MACD, Signal, and Histogram"""
        exp1 = prices.ewm(span=12, adjust=False).mean()
        exp2 = prices.ewm(span=26, adjust=False).mean()

        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal

        return macd.iloc[-1], signal.iloc[-1], histogram.iloc[-1]

    def calculate_moving_averages(self, prices: pd.Series) -> Dict[str, float]:
        """Calculate key moving averages"""
        return {
            'sma_20': prices.rolling(window=20).mean().iloc[-1],
            'sma_50': prices.rolling(window=50).mean().iloc[-1],
            'sma_200': prices.rolling(window=200).mean().iloc[-1],
            'current_price': prices.iloc[-1]
        }

    def analyze_volume(self, df: pd.DataFrame) -> Dict[str, float]:
        """Analyze volume patterns"""
        avg_volume = df['Volume'].tail(50).mean()
        recent_volume = df['Volume'].tail(10).mean()

        # Up day vs down day volume
        df['price_change'] = df['Close'].diff()
        up_volume = df[df['price_change'] > 0]['Volume'].tail(20).mean()
        down_volume = df[df['price_change'] < 0]['Volume'].tail(20).mean()

        return {
            'avg_volume': avg_volume,
            'recent_volume': recent_volume,
            'relative_volume': recent_volume / avg_volume if avg_volume > 0 else 1,
            'up_down_ratio': up_volume / down_volume if down_volume > 0 else 1
        }

    def score_technical_setup(self, data: Dict) -> Dict:
        """
        Score technical setup (0-100)

        Components:
        - Trend strength: 30 points
        - Momentum indicators: 30 points
        - Volume profile: 20 points
        - Pattern recognition: 20 points
        """
        df = data['history']
        prices = df['Close']

        # Calculate indicators
        rsi = self.calculate_rsi(prices)
        macd, signal, histogram = self.calculate_macd(prices)
        mas = self.calculate_moving_averages(prices)
        volume_metrics = self.analyze_volume(df)

        score = 0
        details = {}

        # 1. Trend Strength (30 points)
        trend_score = 0
        current_price = mas['current_price']

        if current_price > mas['sma_20']:
            trend_score += 10
        if current_price > mas['sma_50']:
            trend_score += 10
        if current_price > mas['sma_200']:
            trend_score += 5
        if mas['sma_50'] > mas['sma_200']:  # Golden cross territory
            trend_score += 5

        details['trend_score'] = trend_score
        score += trend_score

        # 2. Momentum Indicators (30 points)
        momentum_score = 0

        # RSI: Sweet spot 40-70
        if 40 <= rsi <= 70:
            momentum_score += 15
        elif 30 <= rsi <= 80:
            momentum_score += 10
        elif rsi < 30:  # Oversold
            momentum_score += 5

        # MACD
        if histogram > 0:  # Bullish
            momentum_score += 10
            if macd > signal:
                momentum_score += 5

        details['momentum_score'] = momentum_score
        details['rsi'] = rsi
        details['macd_histogram'] = histogram
        score += momentum_score

        # 3. Volume Profile (20 points)
        volume_score = 0

        if volume_metrics['relative_volume'] > 1.5:
            volume_score += 10
        elif volume_metrics['relative_volume'] > 1.2:
            volume_score += 5

        if volume_metrics['up_down_ratio'] > 1.2:
            volume_score += 10
        elif volume_metrics['up_down_ratio'] > 1.0:
            volume_score += 5

        details['volume_score'] = volume_score
        details['relative_volume'] = volume_metrics['relative_volume']
        score += volume_score

        # 4. Pattern Recognition (20 points)
        pattern_score = 0

        # Check for higher highs and higher lows
        recent_highs = df['High'].tail(20)
        recent_lows = df['Low'].tail(20)

        if recent_highs.iloc[-1] >= recent_highs.iloc[-10]:
            pattern_score += 10

        if recent_lows.iloc[-1] >= recent_lows.iloc[-10]:
            pattern_score += 10

        details['pattern_score'] = pattern_score
        score += pattern_score

        details['total_score'] = score

        return details

    # ==================== FUNDAMENTAL ANALYSIS ====================

    def calculate_growth_metrics(self, data: Dict) -> Dict:
        """Calculate key growth metrics from financials"""
        info = data['info']
        metrics = {}

        try:
            # Revenue growth
            metrics['revenue_growth'] = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0

            # Earnings growth
            metrics['earnings_growth'] = info.get('earningsGrowth', 0) * 100 if info.get('earningsGrowth') else 0

            # Margins
            metrics['profit_margin'] = info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0
            metrics['operating_margin'] = info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else 0

            # ROE
            metrics['roe'] = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0

            # Debt metrics
            metrics['debt_to_equity'] = info.get('debtToEquity', 0) / 100 if info.get('debtToEquity') else 0
            metrics['current_ratio'] = info.get('currentRatio', 0)

            # Valuation
            metrics['pe_ratio'] = info.get('trailingPE', 0)
            metrics['forward_pe'] = info.get('forwardPE', 0)
            metrics['peg_ratio'] = info.get('pegRatio', 0)

            # Market cap
            metrics['market_cap'] = info.get('marketCap', 0)

        except Exception as e:
            print(f"Error calculating metrics: {e}")

        return metrics

    def score_fundamentals(self, data: Dict) -> Dict:
        """
        Score fundamental strength (0-100)

        Components:
        - Growth metrics: 40 points
        - Financial health: 30 points
        - Profitability: 20 points
        - Valuation: 10 points
        """
        metrics = self.calculate_growth_metrics(data)

        score = 0
        details = {}

        # 1. Growth Metrics (40 points)
        growth_score = 0

        revenue_growth = metrics.get('revenue_growth', 0)
        if revenue_growth > 30:
            growth_score += 20
        elif revenue_growth > 20:
            growth_score += 15
        elif revenue_growth > 10:
            growth_score += 10

        earnings_growth = metrics.get('earnings_growth', 0)
        if earnings_growth > 30:
            growth_score += 20
        elif earnings_growth > 20:
            growth_score += 15
        elif earnings_growth > 10:
            growth_score += 10

        details['growth_score'] = growth_score
        score += growth_score

        # 2. Financial Health (30 points)
        health_score = 0

        debt_to_equity = metrics.get('debt_to_equity', 999)
        if debt_to_equity < 0.5:
            health_score += 15
        elif debt_to_equity < 1.0:
            health_score += 10
        elif debt_to_equity < 1.5:
            health_score += 5

        current_ratio = metrics.get('current_ratio', 0)
        if current_ratio > 2.0:
            health_score += 15
        elif current_ratio > 1.5:
            health_score += 10
        elif current_ratio > 1.0:
            health_score += 5

        details['health_score'] = health_score
        score += health_score

        # 3. Profitability (20 points)
        profit_score = 0

        profit_margin = metrics.get('profit_margin', 0)
        if profit_margin > 20:
            profit_score += 10
        elif profit_margin > 10:
            profit_score += 7
        elif profit_margin > 5:
            profit_score += 4

        roe = metrics.get('roe', 0)
        if roe > 20:
            profit_score += 10
        elif roe > 15:
            profit_score += 7
        elif roe > 10:
            profit_score += 4

        details['profit_score'] = profit_score
        score += profit_score

        # 4. Valuation (10 points)
        valuation_score = 0

        peg_ratio = metrics.get('peg_ratio', 999)
        if 0 < peg_ratio < 1:
            valuation_score += 10
        elif 1 <= peg_ratio < 1.5:
            valuation_score += 7
        elif 1.5 <= peg_ratio < 2:
            valuation_score += 4

        details['valuation_score'] = valuation_score
        score += valuation_score

        details['total_score'] = score
        details['metrics'] = metrics

        return details

    # ==================== CATALYST ANALYSIS ====================

    def score_catalysts(self, data: Dict) -> Dict:
        """
        Score catalyst potential (0-100)

        Components:
        - Timing certainty: 40 points
        - Impact magnitude: 40 points
        - Multiple catalysts: 20 points
        """
        info = data['info']
        calendar = data.get('calendar', None)

        score = 0
        details = {'catalysts': []}

        # 1. Earnings Catalyst (up to 40 points timing + 20 impact)
        earnings_score = 0

        try:
            # Check if earnings date is upcoming
            if calendar is not None and 'Earnings Date' in calendar:
                earnings_date = calendar['Earnings Date']
                if not pd.isna(earnings_date):
                    # Earnings within next 60 days
                    earnings_score += 30
                    details['catalysts'].append('Upcoming earnings')
        except:
            pass

        # Analyst recommendations
        try:
            if data.get('recommendations') is not None:
                recent_recs = data['recommendations'].tail(5)
                if len(recent_recs) > 0 and 'To Grade' in recent_recs.columns:
                    upgrades = len(recent_recs[recent_recs['To Grade'].str.contains('Buy|Outperform', na=False)])
                    if upgrades >= 2:
                        earnings_score += 20
                        details['catalysts'].append('Recent analyst upgrades')
        except:
            pass  # Skip if recommendations data unavailable

        details['earnings_catalyst_score'] = earnings_score
        score += earnings_score

        # 2. Growth/Business Catalysts (estimated - would need additional data sources)
        business_score = 20  # Placeholder - in real implementation, check news, filings
        details['business_catalyst_score'] = business_score
        score += business_score

        # 3. Market Position (20 points)
        market_score = 0

        # Sector strength indicator
        industry = info.get('industry', '')
        if industry:
            market_score += 10
            details['catalysts'].append(f'Industry: {industry}')

        # Market cap appropriate
        market_cap = info.get('marketCap', 0)
        if 2e9 <= market_cap <= 10e9:  # Mid cap
            market_score += 5
            details['catalysts'].append('Mid cap (optimal size)')
        elif market_cap > 10e9:  # Large cap
            market_score += 5
            details['catalysts'].append('Large cap')

        details['market_score'] = market_score
        score += market_score

        details['total_score'] = score

        return details

    # ==================== SENTIMENT ANALYSIS ====================

    def score_sentiment(self, data: Dict) -> Dict:
        """
        Score sentiment (0-100)

        Components:
        - Insider confidence: 40 points (would need SEC data)
        - Institutional backing: 40 points
        - Positive momentum: 20 points
        """
        info = data['info']

        score = 0
        details = {}

        # 1. Institutional Holdings (40 points)
        institutional_score = 0

        inst_ownership = info.get('heldPercentInstitutions', 0) * 100
        if inst_ownership > 70:
            institutional_score += 40
        elif inst_ownership > 50:
            institutional_score += 30
        elif inst_ownership > 30:
            institutional_score += 20

        details['institutional_score'] = institutional_score
        details['institutional_ownership'] = inst_ownership
        score += institutional_score

        # 2. Insider Holdings (40 points - placeholder)
        # In real implementation, would pull from SEC Form 4 filings
        insider_score = 20  # Neutral score
        details['insider_score'] = insider_score
        score += insider_score

        # 3. Analyst Sentiment (20 points)
        analyst_score = 0

        recommendation = info.get('recommendationKey', '')
        if recommendation in ['strong_buy', 'buy']:
            analyst_score += 20
        elif recommendation == 'hold':
            analyst_score += 10

        details['analyst_score'] = analyst_score
        details['recommendation'] = recommendation
        score += analyst_score

        details['total_score'] = score

        return details

    # ==================== COMPOSITE SCORING ====================

    def calculate_final_score(self, ticker: str) -> Dict:
        """
        Calculate composite final score for a stock

        Returns:
            Dictionary with all scores and final rating
        """
        print(f"\nAnalyzing {ticker}...")

        # Get data
        data = self.get_stock_data(ticker)
        if data is None:
            return None

        # Calculate component scores
        fundamental = self.score_fundamentals(data)
        technical = self.score_technical_setup(data)
        catalyst = self.score_catalysts(data)
        sentiment = self.score_sentiment(data)

        # Calculate weighted final score
        final_score = (
            fundamental['total_score'] * self.weights['fundamental'] +
            technical['total_score'] * self.weights['technical'] +
            catalyst['total_score'] * self.weights['catalyst'] +
            sentiment['total_score'] * self.weights['sentiment']
        )

        # Get basic info
        info = data['info']

        result = {
            'ticker': ticker,
            'company_name': info.get('longName', ticker),
            'sector': info.get('sector', 'Unknown'),
            'industry': info.get('industry', 'Unknown'),
            'market_cap': info.get('marketCap', 0),
            'current_price': info.get('currentPrice', 0),

            'final_score': round(final_score, 2),

            'fundamental_score': fundamental['total_score'],
            'technical_score': technical['total_score'],
            'catalyst_score': catalyst['total_score'],
            'sentiment_score': sentiment['total_score'],

            'details': {
                'fundamental': fundamental,
                'technical': technical,
                'catalyst': catalyst,
                'sentiment': sentiment
            },

            'rating': self._get_rating(final_score)
        }

        return result

    def _get_rating(self, score: float) -> str:
        """Convert score to rating"""
        if score >= 80:
            return "STRONG BUY"
        elif score >= 65:
            return "BUY"
        elif score >= 50:
            return "HOLD"
        else:
            return "PASS"

    # ==================== SCREENING PIPELINE ====================

    def screen_stocks(self, tickers: List[str], min_score: float = 65) -> pd.DataFrame:
        """
        Screen multiple stocks and return ranked results

        Args:
            tickers: List of ticker symbols
            min_score: Minimum score threshold

        Returns:
            DataFrame with results sorted by score
        """
        results = []

        for ticker in tickers:
            try:
                result = self.calculate_final_score(ticker)
                if result and result['final_score'] >= min_score:
                    results.append(result)
            except Exception as e:
                print(f"Error processing {ticker}: {e}")

        if not results:
            return pd.DataFrame()

        df = pd.DataFrame(results)
        df = df.sort_values('final_score', ascending=False)

        return df

    def generate_report(self, result: Dict) -> str:
        """Generate detailed analysis report for a stock"""

        report = f"""
{'='*80}
STOCK ANALYSIS REPORT: {result['ticker']}
{'='*80}

Company: {result['company_name']}
Sector: {result['sector']} | Industry: {result['industry']}
Market Cap: ${result['market_cap']:,.0f}
Current Price: ${result['current_price']:.2f}

{'='*80}
FINAL SCORE: {result['final_score']:.1f}/100 - {result['rating']}
{'='*80}

Component Scores:
  Fundamental Analysis: {result['fundamental_score']:.1f}/100 (Weight: 30%)
  Technical Analysis:   {result['technical_score']:.1f}/100 (Weight: 25%)
  Catalyst Potential:   {result['catalyst_score']:.1f}/100 (Weight: 30%)
  Sentiment Analysis:   {result['sentiment_score']:.1f}/100 (Weight: 15%)

{'-'*80}
FUNDAMENTAL ANALYSIS ({result['fundamental_score']:.1f}/100)
{'-'*80}
"""

        fund = result['details']['fundamental']
        metrics = fund.get('metrics', {})

        report += f"""
Growth Metrics:
  Revenue Growth:    {metrics.get('revenue_growth', 0):.1f}%
  Earnings Growth:   {metrics.get('earnings_growth', 0):.1f}%

Profitability:
  Profit Margin:     {metrics.get('profit_margin', 0):.1f}%
  Operating Margin:  {metrics.get('operating_margin', 0):.1f}%
  ROE:               {metrics.get('roe', 0):.1f}%

Financial Health:
  Debt/Equity:       {metrics.get('debt_to_equity', 0):.2f}
  Current Ratio:     {metrics.get('current_ratio', 0):.2f}

Valuation:
  P/E Ratio:         {metrics.get('pe_ratio', 0):.1f}
  Forward P/E:       {metrics.get('forward_pe', 0):.1f}
  PEG Ratio:         {metrics.get('peg_ratio', 0):.2f}

{'-'*80}
TECHNICAL ANALYSIS ({result['technical_score']:.1f}/100)
{'-'*80}
"""

        tech = result['details']['technical']

        report += f"""
Trend Strength:     {tech.get('trend_score', 0):.0f}/30
Momentum:           {tech.get('momentum_score', 0):.0f}/30
Volume Profile:     {tech.get('volume_score', 0):.0f}/20
Pattern:            {tech.get('pattern_score', 0):.0f}/20

Key Indicators:
  RSI (14):          {tech.get('rsi', 0):.1f}
  MACD Histogram:    {tech.get('macd_histogram', 0):.4f}
  Relative Volume:   {tech.get('relative_volume', 0):.2f}x

{'-'*80}
CATALYST ANALYSIS ({result['catalyst_score']:.1f}/100)
{'-'*80}
"""

        cat = result['details']['catalyst']
        catalysts = cat.get('catalysts', [])

        report += f"""
Identified Catalysts:
"""
        for catalyst in catalysts:
            report += f"  • {catalyst}\n"

        report += f"""
{'-'*80}
SENTIMENT ANALYSIS ({result['sentiment_score']:.1f}/100)
{'-'*80}
"""

        sent = result['details']['sentiment']

        report += f"""
Institutional Ownership: {sent.get('institutional_ownership', 0):.1f}%
Analyst Recommendation:  {sent.get('recommendation', 'N/A').upper()}

{'='*80}
RECOMMENDATION: {result['rating']}
{'='*80}

"""

        if result['final_score'] >= 80:
            report += "Strong buy candidate. High conviction setup with multiple positive factors.\n"
        elif result['final_score'] >= 65:
            report += "Buy candidate. Favorable setup with good risk/reward.\n"
        elif result['final_score'] >= 50:
            report += "Hold or monitor. Some positive factors but not compelling enough.\n"
        else:
            report += "Pass. Does not meet minimum criteria for high-growth potential.\n"

        report += f"\n{'='*80}\n"

        return report


# ==================== USAGE EXAMPLES ====================

def example_single_stock():
    """Example: Analyze a single stock"""
    screener = StockScreener()

    result = screener.calculate_final_score('AAPL')

    if result:
        report = screener.generate_report(result)
        print(report)


def example_screen_multiple():
    """Example: Screen multiple stocks"""
    screener = StockScreener()

    # Example tech stocks
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'AMD', 'TSLA', 'META', 'NFLX']

    results_df = screener.screen_stocks(tickers, min_score=60)

    print("\n" + "="*80)
    print("SCREENING RESULTS")
    print("="*80)
    print(results_df[['ticker', 'company_name', 'final_score', 'rating']].to_string(index=False))
    print("="*80)

    # Generate detailed report for top candidate
    if len(results_df) > 0:
        top_ticker = results_df.iloc[0]['ticker']
        top_result = screener.calculate_final_score(top_ticker)
        print(screener.generate_report(top_result))


if __name__ == "__main__":
    # Run example
    example_single_stock()
    # example_screen_multiple()
