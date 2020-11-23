from urllib.parse import quote_plus
from datetime import datetime

import requests
import re


def get_quote(symbol, api_key):
    """Get quote for symbol."""

    url = f'https://cloud-sse.iexapis.com/stable/stock/{quote_plus(symbol)}/quote?token={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    return parser_response(response.json())


def parser_response(obj):
    """Parse response."""

    try:
        quote = {'name': obj['companyName'],
                 'price': '${}'.format(float(obj['latestPrice'])),
                 'upd_time': format_date(obj['latestUpdate']),
                 'symbol': obj['symbol']}
    except (KeyError, TypeError, ValueError):
        return None

    return quote


def parse_text(text):
    """Search for symbol in the text."""

    pattern = r'/\w+'
    symbol = re.search(pattern, text)

    if not symbol:
        return None

    return symbol.group()[1:]


def format_date(timestamp):
    return datetime.fromtimestamp(timestamp / 1000) \
            .strftime("%d %b %Y, %H:%M")
