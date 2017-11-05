
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


def _make_request(market: str, symbol: str, page_size=10, start=0):
    """ Make request to Google """
    params = {
        'q': '{market}:{symbol}'.format(market=market, symbol=symbol),
        'num': page_size,
        'start': start,
        'output': 'rss'
    }

    url = 'https://www.google.com/finance/company_news'
    return requests.get(url, params=params)


def _format_links(links):
    return [{'url': link.attrs.get('href'), 'text': link.get_text()} for link in links]


def _parse_item(item):
    result = {}

    description = item.find('description')
    for _text in description.itertext():
        soup = BeautifulSoup(_text, 'html.parser')
        result['content'] = soup.get_text().strip()
        result['content_links'] = _format_links(soup.find_all('a'))

    title = item.find('title')
    for _text in title.itertext():
        result['title'] = _text.strip()

    guid = item.find('guid')
    for _text in guid.itertext():
        result['guid'] = _text.strip()

    link = item.find('link')
    for _text in link.itertext():
        result['link'] = _text.strip()

    published = item.find('pubDate')
    for _text in published.itertext():
        result['published'] = _text.strip()

    return result


def _parse_response(response_string):
    root = ET.fromstring(response_string)
    channel = root.find('channel')

    result = [_parse_item(item) for item in channel.findall('item')]

    return result

