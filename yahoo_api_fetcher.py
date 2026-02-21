"""
Yahoo Finance API Data Fetcher
Uses Yahoo's JSON API endpoints (more reliable than HTML scraping)
"""

import requests
import pandas as pd
import time
from datetime import datetime
import json

class YahooAPIFetcher:
    """Fetches stock data using Yahoo Finance JSON APIs"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        self.session = requests.Session()

    def get_quote_data(self, ticker):
        """
        Get real-time quote data using Yahoo's quote API
        """
        url = f"https://query1.finance.yahoo.com/v7/finance/quote"
        params = {
            'symbols': ticker,
            'fields': 'symbol,longName,regularMarketPrice,regularMarketVolume,averageDailyVolume10Day,marketCap,trailingPE,forwardPE,priceToBook,profitMargins,operatingMargins,returnOnEquity,revenueGrowth,earningsGrowth,debtToEquity,currentRatio,sector,industry,beta'
        }

        try:
            response = self.session.get(url, params=params, headers=self.headers, timeout=10)
            data = response.json()

            if 'quoteResponse' in data and 'result' in data['quoteResponse']:
                results = data['quoteResponse']['result']
                if results:
                    return results[0]

            return None

        except Exception as e:
            print(f"Error fetching quote for {ticker}: {e}")
            return None

    def get_historical_data(self, ticker, days=180):
        """
        Get historical price data
        """
        try:
            end_time = int(time.time())
            start_time = end_time - (days * 24 * 60 * 60)

            url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}"
            params = {
                'period1': start_time,
                'period2': end_time,
                'interval': '1d',
                'events': 'history'
            }

            response = self.session.get(url, params=params, headers=self.headers)

            if response.status_code == 200:
                from io import StringIO
                df = pd.read_csv(StringIO(response.text))
                df['Date'] = pd.to_datetime(df['Date'])
                return df
            return None

        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {e}")
            return None

    def get_comprehensive_data(self, ticker):
        """
        Get all available data for a ticker
        """
        print(f"  Fetching {ticker}...", end=' ', flush=True)

        # Get quote data
        quote = self.get_quote_data(ticker)
        if not quote:
            print("FAILED")
            return None

        # Small delay
        time.sleep(0.3)

        # Get historical data
        hist = self.get_historical_data(ticker)

        # Build comprehensive data dict
        data = {
            'ticker': ticker,
            'name': quote.get('longName', ticker),
            'sector': quote.get('sector', 'Unknown'),
            'industry': quote.get('industry', 'Unknown'),

            # Price data
            'price': quote.get('regularMarketPrice'),
            'market_cap': quote.get('marketCap'),
            'volume': quote.get('regularMarketVolume'),
            'avg_volume': quote.get('averageDailyVolume10Day'),

            # Valuation
            'pe_ratio': quote.get('trailingPE'),
            'forward_pe': quote.get('forwardPE'),
            'price_to_book': quote.get('priceToBook'),

            # Profitability
            'profit_margin': quote.get('profitMargins'),
            'operating_margin': quote.get('operatingMargins'),
            'roe': quote.get('returnOnEquity'),

            # Growth
            'revenue_growth': quote.get('revenueGrowth'),
            'earnings_growth': quote.get('earningsGrowth'),

            # Financial health
            'debt_to_equity': quote.get('debtToEquity'),
            'current_ratio': quote.get('currentRatio'),

            # Risk
            'beta': quote.get('beta'),

            # Historical
            'historical_prices': hist,

            # Metadata
            'scraped_at': datetime.now().isoformat()
        }

        # Convert percentages (Yahoo returns as decimals)
        if data.get('profit_margin'):
            data['profit_margin'] *= 100
        if data.get('operating_margin'):
            data['operating_margin'] *= 100
        if data.get('roe'):
            data['roe'] *= 100
        if data.get('revenue_growth'):
            data['revenue_growth'] *= 100
        if data.get('earnings_growth'):
            data['earnings_growth'] *= 100

        price_str = f"${data['price']:.2f}" if data.get('price') else "N/A"
        print(f"✓ ({price_str})")

        return data

    def batch_fetch(self, tickers, delay=0.5):
        """
        Fetch data for multiple tickers
        """
        results = []
        failed = []

        print(f"\nFetching data for {len(tickers)} stocks...")
        print("="*80)

        for i, ticker in enumerate(tickers, 1):
            try:
                data = self.get_comprehensive_data(ticker)
                if data:
                    results.append(data)
                else:
                    failed.append(ticker)

                # Progress indicator
                if i % 10 == 0:
                    print(f"  Progress: {i}/{len(tickers)} ({len(results)} successful, {len(failed)} failed)")

                # Rate limiting
                time.sleep(delay)

            except Exception as e:
                print(f"  ✗ {ticker}: {str(e)[:50]}")
                failed.append(ticker)

        print("="*80)
        print(f"Batch fetch complete: {len(results)}/{len(tickers)} successful\n")

        return results, failed


# Test function
if __name__ == "__main__":
    fetcher = YahooAPIFetcher()

    print("\n" + "="*80)
    print("Testing Yahoo Finance API Fetcher")
    print("="*80)

    test_tickers = ['AAPL', 'NVDA', 'TSLA', 'GOOGL', 'MSFT']

    print(f"\nTesting with {len(test_tickers)} stocks:\n")

    results, failed = fetcher.batch_fetch(test_tickers, delay=1)

    print("\n" + "="*80)
    print("RESULTS SUMMARY")
    print("="*80)

    for data in results:
        print(f"\n{data['ticker']} - {data['name']}")
        print(f"  Sector: {data.get('sector', 'N/A')}")
        print(f"  Price: ${data.get('price', 0):.2f}")

        mcap = data.get('market_cap')
        if mcap:
            print(f"  Market Cap: ${mcap/1e9:.1f}B")

        print(f"  P/E: {data.get('pe_ratio', 'N/A')}")
        print(f"  Revenue Growth: {data.get('revenue_growth', 'N/A'):.1f}%" if data.get('revenue_growth') else "  Revenue Growth: N/A")
        print(f"  Profit Margin: {data.get('profit_margin', 'N/A'):.1f}%" if data.get('profit_margin') else "  Profit Margin: N/A")
        print(f"  ROE: {data.get('roe', 'N/A'):.1f}%" if data.get('roe') else "  ROE: N/A")

        if data.get('historical_prices') is not None:
            print(f"  Historical data: {len(data['historical_prices'])} days")

    if failed:
        print(f"\n\nFailed tickers: {', '.join(failed)}")

    print("\n" + "="*80)
