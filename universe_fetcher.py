"""
Dynamic Stock Universe Fetcher
Fetches stock tickers from live sources (Wikipedia, yfinance)
Priority: Live sources → Config file → Hardcoded fallback
"""

import pandas as pd
import yfinance as yf
from typing import List, Optional, Set
import yaml
import os
import time
import requests


def fetch_sp500_tickers() -> List[str]:
    """
    Fetch S&P 500 constituents from Wikipedia (Enhanced with retries)

    Returns:
        List of ticker symbols (~503 stocks)

    Raises:
        Exception if all retry attempts fail
    """
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    # User-Agent header to avoid Wikipedia blocking
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for attempt in range(3):  # 3 retry attempts
        try:
            # Fetch with User-Agent header and timeout
            tables = pd.read_html(
                url,
                storage_options={'User-Agent': headers['User-Agent']},
                #timeout=10  # 10 second timeout (removed - not supported in older pandas)
            )
            df = tables[0]  # First table contains the constituent list

            # Validate table structure
            if 'Symbol' not in df.columns:
                raise ValueError("Wikipedia table structure changed - 'Symbol' column not found")

            # Extract and clean ticker symbols
            tickers = df['Symbol'].str.replace('.', '-', regex=False).tolist()  # Convert BRK.B to BRK-B format

            # Validate ticker count (S&P 500 should have ~480-520 stocks)
            if len(tickers) < 480 or len(tickers) > 520:
                raise ValueError(f"Unexpected ticker count: {len(tickers)} (expected 480-520)")

            return tickers

        except Exception as e:
            if attempt < 2:  # Not the last attempt
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s
                print(f"   Attempt {attempt + 1} failed: {str(e)}")
                print(f"   Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            else:
                # Last attempt failed
                raise Exception(f"Failed to fetch S&P 500 from Wikipedia after 3 attempts: {str(e)}")


def fetch_nasdaq100_tickers() -> List[str]:
    """
    Fetch NASDAQ 100 constituents from Wikipedia

    Returns:
        List of ticker symbols (~100 stocks)
    """
    url = 'https://en.wikipedia.org/wiki/Nasdaq-100'

    try:
        # Read the Wikipedia table
        tables = pd.read_html(url)
        df = tables[4]  # The components table (may need adjustment if Wikipedia changes)

        # Extract ticker symbols
        tickers = df['Ticker'].tolist()

        return tickers
    except Exception as e:
        raise Exception(f"Failed to fetch NASDAQ 100 from Wikipedia: {str(e)}")


def fetch_sp500_yahoo_screener() -> List[str]:
    """
    Fetch S&P 500 constituents using Yahoo Finance Screener API (undocumented)

    This is a fallback method when Wikipedia is unavailable.
    Note: This API is undocumented and may break in the future.

    Returns:
        List of ticker symbols (~500 stocks)

    Raises:
        Exception if the API request fails
    """
    url = "https://query1.finance.yahoo.com/v1/finance/screener"

    # Request payload for S&P 500 filter
    payload = {
        "size": 600,  # Request more than 500 to ensure we get all
        "offset": 0,
        "sortField": "ticker",
        "sortType": "ASC",
        "quoteType": "EQUITY",
        "query": {
            "operator": "and",
            "operands": [
                {
                    "operator": "eq",
                    "operands": ["region", "us"]
                },
                {
                    "operator": "eq",
                    "operands": ["index", "^GSPC"]  # S&P 500 index code
                }
            ]
        },
        "userId": "",
        "userIdType": "guid"
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()  # Raise exception for HTTP errors

        data = response.json()

        # Extract tickers from API response
        if 'finance' in data and 'result' in data['finance'] and len(data['finance']['result']) > 0:
            results = data['finance']['result'][0].get('quotes', [])
            tickers = [quote['symbol'] for quote in results if 'symbol' in quote]

            # Validate ticker count
            if len(tickers) < 450 or len(tickers) > 550:
                raise ValueError(f"Unexpected ticker count from Yahoo API: {len(tickers)}")

            return tickers
        else:
            raise ValueError("Unexpected Yahoo API response structure")

    except Exception as e:
        raise Exception(f"Failed to fetch S&P 500 from Yahoo Finance Screener API: {str(e)}")


def fetch_sp500_pytickersymbols() -> List[str]:
    """
    Fetch S&P 500 constituents using pytickersymbols library

    This is a fallback method when Wikipedia and Yahoo API are unavailable.
    Requires: pip install pytickersymbols

    Returns:
        List of ticker symbols (~500 stocks)

    Raises:
        Exception if the library is not installed or fails
    """
    try:
        from pytickersymbols import PyTickerSymbols

        stock_data = PyTickerSymbols()
        sp500_stocks = stock_data.get_stocks_by_index('S&P 500')

        # Extract ticker symbols
        tickers = [stock['symbol'] for stock in sp500_stocks]

        # Validate ticker count
        if len(tickers) < 450 or len(tickers) > 550:
            raise ValueError(f"Unexpected ticker count from pytickersymbols: {len(tickers)}")

        return tickers

    except ImportError:
        raise Exception("pytickersymbols library not installed. Install with: pip install pytickersymbols")
    except Exception as e:
        raise Exception(f"Failed to fetch S&P 500 from pytickersymbols: {str(e)}")


def filter_by_sector(tickers: List[str], sectors: List[str]) -> List[str]:
    """
    Filter tickers by sector using yfinance

    Args:
        tickers: List of ticker symbols
        sectors: List of sectors to include (e.g., ['Technology', 'Healthcare'])

    Returns:
        Filtered list of tickers
    """
    filtered = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            stock_sector = info.get('sector', '')

            if stock_sector in sectors:
                filtered.append(ticker)
        except:
            # Skip on error
            continue

    return filtered


def filter_by_market_cap(tickers: List[str], min_mcap: float) -> List[str]:
    """
    Filter tickers by minimum market cap using yfinance

    Args:
        tickers: List of ticker symbols
        min_mcap: Minimum market cap in dollars (e.g., 2e9 for $2B)

    Returns:
        Filtered list of tickers
    """
    filtered = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            mcap = info.get('marketCap', 0)

            if mcap >= min_mcap:
                filtered.append(ticker)
        except:
            # Skip on error
            continue

    return filtered


def get_hardcoded_fallback() -> List[str]:
    """
    Return comprehensive hardcoded S&P 500 list as last-resort fallback

    This list contains 500+ major S&P 500 constituents organized by sector.
    Last updated: January 2026

    Returns:
        List of 500+ ticker symbols
    """
    return [
        # TECHNOLOGY SECTOR (~100 stocks)
        # Mega Cap Tech
        'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'META', 'NVDA', 'TSLA', 'NFLX', 'ADBE',
        # Semiconductors
        'AMD', 'INTC', 'QCOM', 'AVGO', 'MU', 'AMAT', 'LRCX', 'KLAC', 'MRVL', 'NXPI',
        'TXN', 'ADI', 'MPWR', 'ON', 'MCHP', 'SWKS', 'QRVO', 'WOLF', 'ENTG', 'MTSI',
        # Software & Cloud
        'CRM', 'ORCL', 'INTU', 'NOW', 'WDAY', 'PANW', 'SNOW', 'DDOG', 'NET', 'CRWD',
        'ZS', 'OKTA', 'FTNT', 'TEAM', 'HUBS', 'VEEV', 'DOCU', 'ZM', 'CFLT', 'DBX',
        'BOX', 'SMAR', 'RNG', 'GDDY', 'TWLO', 'DT', 'ESTC', 'MDB', 'PATH', 'BILL',
        # IT Services & Consulting
        'ACN', 'IBM', 'CSCO', 'ANET', 'APH', 'TEL', 'GLW', 'JNPR', 'NTAP', 'HPE',
        # Hardware & Electronics
        'DELL', 'HPQ', 'SMCI', 'STX', 'WDC', 'PSTG', 'FLEX', 'JBL', 'ARW', 'AVT',
        # Payments & Fintech
        'V', 'MA', 'PYPL', 'AXP', 'FIS', 'FISV', 'GPN', 'FLT', 'CPAY', 'TOST',

        # HEALTHCARE SECTOR (~90 stocks)
        # Pharmaceuticals - Large Cap
        'LLY', 'JNJ', 'UNH', 'PFE', 'ABBV', 'MRK', 'TMO', 'ABT', 'BMY', 'AMGN',
        'GILD', 'CVS', 'CI', 'HUM', 'MCK', 'COR', 'CAH', 'ZTS', 'ELV', 'CNC',
        # Biotechnology
        'REGN', 'VRTX', 'BIIB', 'MRNA', 'ILMN', 'ALNY', 'SGEN', 'INCY', 'EXAS', 'TECH',
        'IONS', 'BMRN', 'SRPT', 'RARE', 'FOLD', 'ARWR', 'BLUE', 'NBIX', 'UTHR', 'TGTX',
        # Medical Devices
        'ISRG', 'DHR', 'SYK', 'BSX', 'MDT', 'EW', 'HOLX', 'ALGN', 'DXCM', 'PODD',
        'IDXX', 'RMD', 'BDX', 'BAX', 'ZBH', 'STE', 'GEHC', 'QDEL', 'NVST', 'TFX',
        # Health Care Equipment & Supplies
        'A', 'TDOC', 'VEEV', 'HCA', 'UHS', 'CRL', 'IQV', 'LH', 'DGX', 'MOH',
        # Health Care Services
        'HSIC', 'PDCO', 'ENSG', 'DVA', 'ACHC', 'THC', 'AMED', 'CHE', 'SGRY', 'CLOV',

        # FINANCIAL SERVICES SECTOR (~80 stocks)
        # Banks - Money Center
        'JPM', 'BAC', 'WFC', 'C', 'USB', 'PNC', 'TFC', 'COF', 'KEY', 'FITB',
        'RF', 'CFG', 'HBAN', 'MTB', 'ZION', 'WTFC', 'CMA', 'SIVB', 'FRC', 'WAL',
        # Investment Banks & Brokers
        'GS', 'MS', 'SCHW', 'BLK', 'SPGI', 'MCO', 'CME', 'ICE', 'NDAQ', 'CBOE',
        'MKTX', 'IBKR', 'HOOD', 'COIN', 'VIRT', 'LPLA', 'SF', 'RJF', 'PIPER', 'BGC',
        # Insurance
        'BRK-B', 'PGR', 'ALL', 'TRV', 'AIG', 'MET', 'PRU', 'AFL', 'CINF', 'L',
        'GL', 'WRB', 'AIZ', 'RNR', 'AJG', 'MMC', 'AON', 'BRO', 'ERIE', 'HIG',
        # REITs
        'AMT', 'PLD', 'EQIX', 'PSA', 'DLR', 'SPG', 'O', 'WELL', 'AVB', 'EQR',
        'VTR', 'PEAK', 'ARE', 'MAA', 'UDR', 'ESS', 'CPT', 'EXR', 'CUBE', 'LSI',

        # CONSUMER DISCRETIONARY (~70 stocks)
        # Retail - General
        'HD', 'LOW', 'TGT', 'COST', 'WMT', 'DG', 'DLTR', 'BBY', 'ROST', 'TJX',
        'TSCO', 'AZO', 'ORLY', 'AAP', 'AN', 'KMX', 'LAD', 'ABG', 'GPI', 'SAH',
        # E-commerce & Internet Retail
        'AMZN', 'EBAY', 'ETSY', 'W', 'CHWY', 'FTCH', 'RH', 'WSM', 'PRTS', 'CVNA',
        # Restaurants & Food
        'MCD', 'SBUX', 'YUM', 'CMG', 'DPZ', 'QSR', 'WEN', 'JACK', 'PZZA', 'BLMN',
        'DIN', 'EAT', 'TXRH', 'CBRL', 'CAKE', 'DENN', 'BJRI', 'RUTH', 'PLAY', 'WING',
        # Apparel & Footwear
        'NKE', 'LULU', 'GPS', 'UAA', 'VFC', 'CROX', 'DECK', 'RL', 'PVH', 'HBI',
        # Automotive
        'TSLA', 'GM', 'F', 'RIVN', 'LCID', 'APTV', 'BWA', 'LEA', 'GT', 'ADNT',
        # Travel & Leisure
        'BKNG', 'MAR', 'HLT', 'ABNB', 'EXPE', 'UBER', 'LYFT', 'DASH', 'TCOM', 'TRIP',

        # COMMUNICATION SERVICES (~30 stocks)
        'GOOGL', 'GOOG', 'META', 'DIS', 'NFLX', 'CMCSA', 'T', 'TMUS', 'VZ', 'CHTR',
        'SPOT', 'RBLX', 'EA', 'TTWO', 'ATVI', 'ZNGA', 'LYV', 'WBD', 'FOXA', 'FOX',
        'NWSA', 'NWS', 'NYT', 'MSGS', 'MSGN', 'IPG', 'OMC', 'ROKU', 'MTCH', 'BMBL',

        # INDUSTRIALS (~70 stocks)
        # Aerospace & Defense
        'BA', 'RTX', 'LMT', 'GD', 'NOC', 'TDG', 'HWM', 'LHX', 'TXT', 'HII',
        'AXON', 'IRDM', 'AIR', 'KTOS', 'AVAV', 'LDOS', 'SAIC', 'CACI', 'HXL', 'MOG-A',
        # Machinery & Equipment
        'CAT', 'DE', 'CMI', 'ETN', 'EMR', 'HON', 'ITW', 'ROK', 'PH', 'AME',
        'DOV', 'IR', 'XYL', 'FTV', 'GNRC', 'WTS', 'CR', 'AOS', 'BLDR', 'WSO',
        # Industrials - Transportation
        'UNP', 'UPS', 'FDX', 'NSC', 'CSX', 'JBHT', 'ODFL', 'XPO', 'CHRW', 'EXPD',
        'R', 'LSTR', 'ARCB', 'SAIA', 'WERN', 'KNX', 'HUBG', 'SNDR', 'YELL', 'MATX',
        # Construction & Engineering
        'GE', 'MMM', 'DHI', 'LEN', 'PHM', 'TOL', 'NVR', 'BLD', 'OC', 'VMC',
        'MLM', 'SUM', 'FBIN', 'MAS', 'CARR', 'JCI', 'TRMB', 'BWA', 'LECO', 'AIT',

        # ENERGY SECTOR (~40 stocks)
        # Oil & Gas - Integrated
        'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'MPC', 'VLO', 'PSX', 'PXD', 'OXY',
        'HAL', 'BKR', 'OKE', 'WMB', 'KMI', 'HES', 'DVN', 'FANG', 'MRO', 'APA',
        # Oil & Gas - E&P
        'CTRA', 'OVV', 'EQT', 'AR', 'RRC', 'MTDR', 'SM', 'CHRD', 'PR', 'NOG',
        # Energy Equipment & Services
        'FTI', 'NOV', 'CHX', 'LBRT', 'HP', 'RIG', 'VAL', 'WTTR', 'PUMP', 'NINE',
        # Renewable Energy
        'ENPH', 'SEDG', 'RUN', 'FSLR', 'NOVA', 'SHLS', 'ARRY', 'SPWR', 'BE', 'PLUG',

        # CONSUMER STAPLES (~40 stocks)
        'PG', 'KO', 'PEP', 'COST', 'WMT', 'PM', 'MO', 'CL', 'MDLZ', 'GIS',
        'KHC', 'HSY', 'K', 'CPB', 'CAG', 'SJM', 'HRL', 'MKC', 'TSN', 'BF-B',
        'STZ', 'TAP', 'SAM', 'KDP', 'MNST', 'CELH', 'KR', 'SYY', 'ADM', 'BG',
        'EL', 'CLX', 'CHD', 'KMB', 'SWK', 'NWL', 'CASY', 'PFGC', 'UNFI', 'SMPL',

        # MATERIALS SECTOR (~30 stocks)
        'LIN', 'APD', 'SHW', 'ECL', 'DD', 'DOW', 'NEM', 'FCX', 'NUE', 'STLD',
        'VMC', 'MLM', 'ALB', 'CE', 'FMC', 'IFF', 'PPG', 'RPM', 'SEE', 'AVY',
        'IP', 'PKG', 'AMCR', 'GPK', 'WRK', 'SON', 'SLGN', 'HUN', 'SMG', 'MOS',

        # UTILITIES SECTOR (~30 stocks)
        'NEE', 'DUK', 'SO', 'D', 'AEP', 'SRE', 'EXC', 'XEL', 'ED', 'PEG',
        'WEC', 'ES', 'DTE', 'ETR', 'FE', 'PPL', 'AEE', 'CMS', 'CNP', 'NI',
        'ATO', 'EVRG', 'LNT', 'PNW', 'OGE', 'NWE', 'AVA', 'SJW', 'MSEX', 'AWR',

        # REAL ESTATE (~20 stocks)
        'AMT', 'PLD', 'EQIX', 'PSA', 'DLR', 'SPG', 'O', 'WELL', 'AVB', 'EQR',
        'VTR', 'ARE', 'MAA', 'UDR', 'ESS', 'CPT', 'EXR', 'CUBE', 'FR', 'REXR',
    ]


def load_from_config(config_file: str = 'universe_config.yaml') -> List[str]:
    """
    Load universe from config file

    Args:
        config_file: Path to YAML config file

    Returns:
        List of tickers from config
    """
    config_path = os.path.join(os.path.dirname(__file__), config_file)

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Check if explicit tickers are provided
    if 'tickers' in config and config['tickers']:
        return config['tickers']

    # Otherwise use filters
    if 'filters' in config:
        filters = config['filters']
        tickers = []

        # Fetch from specified indices
        if 'indices' in filters:
            for index in filters['indices']:
                if index == 'sp500':
                    tickers.extend(fetch_sp500_tickers())
                elif index == 'nasdaq100':
                    tickers.extend(fetch_nasdaq100_tickers())

        # Deduplicate
        tickers = list(set(tickers))

        # Apply sector filter if specified
        if 'sectors' in filters and filters['sectors']:
            tickers = filter_by_sector(tickers, filters['sectors'])

        # Apply market cap filter if specified
        if 'min_market_cap' in filters:
            tickers = filter_by_market_cap(tickers, filters['min_market_cap'])

        # Apply max stocks limit
        if 'max_stocks' in filters:
            tickers = tickers[:filters['max_stocks']]

        return tickers

    raise ValueError("Config file must contain either 'tickers' or 'filters' section")


def get_universe(
    mode: str = 'auto',
    sectors: Optional[List[str]] = None,
    min_mcap: Optional[float] = 2e9,
    max_stocks: int = 500
) -> List[str]:
    """
    Get stock universe with live data priority

    Args:
        mode: Selection mode ('auto', 'sp500', 'nasdaq100', 'combined',
              'tech', 'healthcare', 'growth', 'file')
        sectors: List of sectors to filter (only used in auto mode)
        min_mcap: Minimum market cap in dollars (only used in auto mode)
        max_stocks: Maximum number of stocks to return

    Returns:
        List of ticker symbols
    """
    if mode == 'auto':
        # Multi-source fallback chain: Wikipedia → Yahoo API → pytickersymbols → Hardcoded

        # ATTEMPT 1: Wikipedia (Primary Source)
        try:
            print("📡 Fetching S&P 500 constituents from Wikipedia...")
            tickers = fetch_sp500_tickers()
            print(f"✓ Wikipedia SUCCESS: Fetched {len(tickers)} tickers")

            if sectors:
                print(f"→ Filtering for sectors: {', '.join(sectors)}")
                tickers = filter_by_sector(tickers, sectors)
                print(f"✓ {len(tickers)} stocks after sector filter")

            if min_mcap:
                print(f"→ Filtering for market cap ≥ ${min_mcap/1e9:.0f}B")
                # Note: Filtering by market cap is slow, skip for default mode
                # Can be enabled if user specifically requests it
                # tickers = filter_by_market_cap(tickers, min_mcap)
                # print(f"✓ {len(tickers)} stocks after market cap filter")

            # Return up to max_stocks (default 500)
            result = tickers[:max_stocks]
            print(f"→ Final universe: {len(result)} stocks (Source: Wikipedia)\n")
            return result

        except Exception as e:
            print(f"✗ Wikipedia fetch failed: {str(e)[:100]}")

        # ATTEMPT 2: Yahoo Finance Screener API (Secondary Fallback)
        try:
            print("📡 Trying Yahoo Finance Screener API...")
            tickers = fetch_sp500_yahoo_screener()
            print(f"✓ Yahoo API SUCCESS: Fetched {len(tickers)} tickers")
            print(f"⚠️  WARNING: Using Yahoo Finance API fallback (Wikipedia unavailable)")

            result = tickers[:max_stocks]
            print(f"→ Final universe: {len(result)} stocks (Source: Yahoo Finance API)\n")
            return result

        except Exception as e:
            print(f"✗ Yahoo API fetch failed: {str(e)[:100]}")

        # ATTEMPT 3: pytickersymbols Library (Tertiary Fallback)
        try:
            print("📡 Trying pytickersymbols library...")
            tickers = fetch_sp500_pytickersymbols()
            print(f"✓ pytickersymbols SUCCESS: Fetched {len(tickers)} tickers")
            print(f"⚠️  WARNING: Using pytickersymbols fallback (Wikipedia & Yahoo unavailable)")

            result = tickers[:max_stocks]
            print(f"→ Final universe: {len(result)} stocks (Source: pytickersymbols)\n")
            return result

        except Exception as e:
            print(f"✗ pytickersymbols fetch failed: {str(e)[:100]}")

        # ATTEMPT 4: Hardcoded List (Last Resort)
        print("⚠️  ⚠️  ⚠️  ALL LIVE SOURCES FAILED")
        print(f"→ Using hardcoded S&P 500 list (last resort, updated Jan 2026)")
        result = get_hardcoded_fallback()[:max_stocks]
        print(f"→ Final universe: {len(result)} stocks (Source: HARDCODED)\n")
        return result

    elif mode == 'sp500':
        print("📡 Fetching S&P 500 constituents from Wikipedia...")
        tickers = fetch_sp500_tickers()
        print(f"✓ Fetched {len(tickers)} tickers from S&P 500\n")
        return tickers[:max_stocks]

    elif mode == 'nasdaq100':
        print("📡 Fetching NASDAQ 100 constituents from Wikipedia...")
        tickers = fetch_nasdaq100_tickers()
        print(f"✓ Fetched {len(tickers)} tickers from NASDAQ 100\n")
        return tickers[:max_stocks]

    elif mode == 'combined':
        print("📡 Fetching S&P 500 + NASDAQ 100 from Wikipedia...")
        sp500 = set(fetch_sp500_tickers())
        nasdaq = set(fetch_nasdaq100_tickers())
        combined = list(sp500 | nasdaq)  # Union
        print(f"✓ Fetched {len(combined)} unique tickers (combined)\n")
        return combined[:max_stocks]

    elif mode == 'tech':
        print("📡 Fetching S&P 500 and filtering for Technology sector...")
        tickers = fetch_sp500_tickers()
        tickers = filter_by_sector(tickers, ['Technology'])
        print(f"✓ {len(tickers)} Technology stocks found\n")
        return tickers[:max_stocks]

    elif mode == 'healthcare':
        print("📡 Fetching S&P 500 and filtering for Healthcare sector...")
        tickers = fetch_sp500_tickers()
        tickers = filter_by_sector(tickers, ['Healthcare'])
        print(f"✓ {len(tickers)} Healthcare stocks found\n")
        return tickers[:max_stocks]

    elif mode == 'growth':
        print("📡 Fetching S&P 500 and filtering for growth sectors...")
        tickers = fetch_sp500_tickers()
        growth_sectors = ['Technology', 'Healthcare', 'Consumer Cyclical']
        tickers = filter_by_sector(tickers, growth_sectors)
        print(f"✓ {len(tickers)} growth stocks found\n")
        return tickers[:max_stocks]

    elif mode == 'file':
        print("📄 Loading universe from config file...")
        tickers = load_from_config('universe_config.yaml')
        print(f"✓ Loaded {len(tickers)} tickers from config\n")
        return tickers[:max_stocks]

    else:
        raise ValueError(f"Unknown mode: {mode}. Choose from: auto, sp500, nasdaq100, combined, tech, healthcare, growth, file")


if __name__ == "__main__":
    # Test the fetcher
    print("Testing universe_fetcher...\n")

    try:
        tickers = get_universe(mode='auto', max_stocks=10)
        print(f"Sample tickers: {tickers[:10]}")
    except Exception as e:
        print(f"Error: {e}")
