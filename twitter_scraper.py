import re
import requests
from lxml.etree import ParserError
from pyquery import PyQuery as pq


def get_tweets(user, pages=25):
    url = f'https://twitter.com/i/profiles/show/{user}/timeline/tweets?include_available_features=1&include_entities=1&include_new_items_bar=true'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': f'https://twitter.com/{user}',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
        'X-Twitter-Active-User': 'yes',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def gen_tweets(pages):
        r = requests.get(url, headers=headers)

        while pages > 0:
            try:
                d = pq(r.json()['items_html'])
            except (ParserError, KeyError):
                raise ValueError(
                    f'Oops! Either "{user}" does not exist or private.')

            tweets = [tweet.text_content() for tweet in d('.tweet-text')]
            last_tweet = d('.stream-item')[-1].attrib['data-item-id']

            for tweet in tweets:
                if tweet:
                    yield re.sub('http', ' http', tweet, 1)

            r = requests.get(
                url, params={'max_position': last_tweet}, headers=headers)
            pages += -1

    yield from gen_tweets(pages)
