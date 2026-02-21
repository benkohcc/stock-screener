"""
Yahoo Finance Web Scraper
Fetches real stock data by scraping Yahoo Finance pages
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from datetime import datetime, timedelta

class YahooFinanceScraper:
    """Scrapes stock data from Yahoo Finance"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        self.session = requests.Session()

    def _get_page(self, url, retries=3):
        """Fetch page with retries"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    return response
                time.sleep(2)
            except Exception as e:
                if attempt == retries - 1:
                    raise
                time.sleep(2)
        return None

    def _parse_number(self, text):
        """Parse number from text (handles K, M, B, T suffixes)"""
        if not text or text == 'N/A' or text == '--':
            return None

        text = text.strip().replace(',', '').replace('$', '').replace('%', '')

        # Handle multipliers
        multipliers = {'K': 1e3, 'M': 1e6, 'B': 1e9, 'T': 1e12}
        for suffix, mult in multipliers.items():
            if suffix in text.upper():
                try:
                    return float(text.upper().replace(suffix, '')) * mult
                except:
                    return None

        try:
            return float(text)
        except:
            return None

    def get_quote_data(self, ticker):
        """
        Scrape main quote page for price and basic info
        """
        url = f"https://finance.yahoo.com/quote/{ticker}"

        try:
            response = self._get_page(url)
            if not response:
                return None

            soup = BeautifulSoup(response.content, 'html.parser')

            data = {'ticker': ticker}

            # Try to find price using multiple selectors
            price_selectors = [
                ('fin-streamer', {'data-symbol': ticker, 'data-field': 'regularMarketPrice'}),
                ('span', {'class': re.compile(r'Fw\(b\).*Fz\(36px\)')}),
            ]

            for tag, attrs in price_selectors:
                price_elem = soup.find(tag, attrs)
                if price_elem:
                    data['price'] = self._parse_number(price_elem.text)
                    break

            # Extract header info
            header = soup.find('div', {'id': 'quote-header-info'})
            if header:
                # Company name
                h1 = header.find('h1')
                if h1:
                    data['name'] = h1.text.strip().split('(')[0].strip()

            # Try to extract key stats from summary
            summary_table = soup.find('div', {'data-test': 'quote-statistics'})
            if summary_table:
                rows = summary_table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        label = cells[0].text.strip()
                        value = cells[1].text.strip()

                        if 'Market Cap' in label:
                            data['market_cap'] = self._parse_number(value)
                        elif 'P/E Ratio' in label or 'PE Ratio' in label:
                            data['pe_ratio'] = self._parse_number(value)
                        elif 'Volume' in label and 'Avg' not in label:
                            data['volume'] = self._parse_number(value)
                        elif 'Avg. Volume' in label:
                            data['avg_volume'] = self._parse_number(value)

            return data if 'price' in data else None

        except Exception as e:
            print(f"Error scraping {ticker}: {e}")
            return None

    def get_statistics(self, ticker):
        """
        Scrape key statistics page for fundamentals
        """
        url = f"https://finance.yahoo.com/quote/{ticker}/key-statistics"

        try:
            response = self._get_page(url)
            if not response:
                return {}

            soup = BeautifulSoup(response.content, 'html.parser')
            stats = {}

            # Find all table rows
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        label = cells[0].text.strip()
                        value = cells[1].text.strip()

                        # Map labels to our metrics
                        if 'Market Cap' in label:
                            stats['market_cap'] = self._parse_number(value)
                        elif 'Trailing P/E' in label:
                            stats['pe_ratio'] = self._parse_number(value)
                        elif 'Forward P/E' in label:
                            stats['forward_pe'] = self._parse_number(value)
                        elif 'PEG Ratio' in label:
                            stats['peg_ratio'] = self._parse_number(value)
                        elif 'Profit Margin' in label:
                            stats['profit_margin'] = self._parse_number(value)
                        elif 'Operating Margin' in label:
                            stats['operating_margin'] = self._parse_number(value)
                        elif 'Return on Equity' in label:
                            stats['roe'] = self._parse_number(value)
                        elif 'Revenue Per Share' in label:
                            stats['revenue_per_share'] = self._parse_number(value)
                        elif 'Quarterly Revenue Growth' in label:
                            stats['revenue_growth'] = self._parse_number(value)
                        elif 'Quarterly Earnings Growth' in label:
                            stats['earnings_growth'] = self._parse_number(value)
                        elif 'Total Debt/Equity' in label:
                            stats['debt_to_equity'] = self._parse_number(value)
                        elif 'Current Ratio' in label:
                            stats['current_ratio'] = self._parse_number(value)
                        elif 'Beta' in label:
                            stats['beta'] = self._parse_number(value)

            return stats

        except Exception as e:
            print(f"Error scraping statistics for {ticker}: {e}")
            return {}

    def get_profile(self, ticker):
        """Get company profile including sector"""
        url = f"https://finance.yahoo.com/quote/{ticker}/profile"

        try:
            response = self._get_page(url)
            if not response:
                return {}

            soup = BeautifulSoup(response.content, 'html.parser')
            profile = {}

            # Look for sector and industry in profile page
            text = soup.get_text()

            # Try to find sector/industry using common patterns
            if 'Sector' in text:
                # Basic extraction - can be improved
                pass

            return profile

        except Exception as e:
            return {}

    def get_historical_prices(self, ticker, days=180):
        """
        Get historical price data for technical analysis
        Uses Yahoo Finance download endpoint
        """
        try:
            # Calculate timestamps
            end_date = int(time.time())
            start_date = end_date - (days * 24 * 60 * 60)

            # Yahoo Finance historical data endpoint
            url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}"
            params = {
                'period1': start_date,
                'period2': end_date,
                'interval': '1d',
                'events': 'history'
            }

            response = self.session.get(url, params=params, headers=self.headers)

            if response.status_code == 200:
                # Parse CSV response
                from io import StringIO
                df = pd.read_csv(StringIO(response.text))
                df['Date'] = pd.to_datetime(df['Date'])
                return df
            else:
                return None

        except Exception as e:
            print(f"Error getting historical data for {ticker}: {e}")
            return None

    def get_comprehensive_data(self, ticker):
        """
        Get all available data for a ticker
        """
        print(f"Scraping {ticker}...", end=' ')

        # Get quote data
        quote = self.get_quote_data(ticker)
        if not quote:
            print("FAILED (quote)")
            return None

        # Small delay between requests
        time.sleep(0.5)

        # Get statistics
        stats = self.get_statistics(ticker)

        time.sleep(0.5)

        # Get historical prices
        hist = self.get_historical_prices(ticker)

        # Combine all data
        data = {
            'ticker': ticker,
            'name': quote.get('name', ticker),
            'price': quote.get('price'),
            'market_cap': quote.get('market_cap') or stats.get('market_cap'),
            'volume': quote.get('volume'),
            'avg_volume': quote.get('avg_volume'),

            # From statistics
            'pe_ratio': stats.get('pe_ratio'),
            'forward_pe': stats.get('forward_pe'),
            'peg_ratio': stats.get('peg_ratio'),
            'profit_margin': stats.get('profit_margin'),
            'operating_margin': stats.get('operating_margin'),
            'roe': stats.get('roe'),
            'revenue_growth': stats.get('revenue_growth'),
            'earnings_growth': stats.get('earnings_growth'),
            'debt_to_equity': stats.get('debt_to_equity'),
            'current_ratio': stats.get('current_ratio'),
            'beta': stats.get('beta'),

            # Historical prices
            'historical_prices': hist,

            # Metadata
            'scraped_at': datetime.now().isoformat()
        }

        print(f"✓ (${data['price']:.2f})" if data['price'] else "✓")

        return data


# Test function
if __name__ == "__main__":
    scraper = YahooFinanceScraper()

    print("Testing Yahoo Finance Scraper\n")
    print("="*80)

    test_tickers = ['AAPL', 'NVDA', 'TSLA']

    for ticker in test_tickers:
        print(f"\nTesting {ticker}:")
        print("-"*80)

        data = scraper.get_comprehensive_data(ticker)

        if data:
            print(f"\nResults for {ticker}:")
            print(f"  Name: {data.get('name', 'N/A')}")
            print(f"  Price: ${data.get('price', 0):.2f}")
            mcap = data.get('market_cap')
            if mcap:
                print(f"  Market Cap: ${mcap/1e9:.2f}B")
            else:
                print(f"  Market Cap: N/A")
            print(f"  P/E Ratio: {data.get('pe_ratio', 'N/A')}")
            print(f"  Revenue Growth: {data.get('revenue_growth', 'N/A')}")
            print(f"  Profit Margin: {data.get('profit_margin', 'N/A')}")
            if data.get('historical_prices') is not None:
                print(f"  Historical data points: {len(data['historical_prices'])}")
        else:
            print(f"  ✗ Failed to scrape data")

        print()
        time.sleep(2)  # Be nice to Yahoo

    print("="*80)
    print("Test complete!")
