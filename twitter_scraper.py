import re
from requests_html import HTMLSession, HTML

session = HTMLSession()


def get_tweets(user, pages=25):
    """Gets tweets for a given user, via the Twitter frontend API."""

    url = 'https://twitter.com/i/profiles/show/{user}/timeline/tweets?' \
          'include_available_features=1&' \
          'include_entities=1&' \
          'include_new_items_bar=true'.format(user=user)
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': f'https://twitter.com/{user}',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
        'X-Twitter-Active-User': 'yes',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def gen_tweets(pages):
        r = session.get(url, headers=headers)

        while pages > 0:
            try:
                html = HTML(html=r.json()['items_html'], url='bunk', default_encoding='utf-8')
            except KeyError:
                raise ValueError(
                    'Oops! Either "{user}" does not exist or is private.'.
                    format(user=user))

            tweets = []
            for tweet in html.find('.stream-item'):
                text = tweet.find('.tweet-text')[0].full_text
                interactions = [x.text for x in tweet.find('.ProfileTweet-actionCountForPresentation')]
                replies = int(interactions[0]) if interactions[0] else 0
                retweets = int(interactions[2]) if interactions[2] else 0
                likes = int(interactions[4]) if interactions[4] else 0
                tweets.append({'text': text, 'replies': replies, 'retweets': retweets, 'likes': likes})
                
            last_tweet = html.find('.stream-item')[-1].attrs['data-item-id']

            for tweet in tweets:
                if tweet:
                    tweet['text'] = re.sub('http', ' http', tweet['text'], 1)
                    yield tweet

            r = session.get(
                url, params={'max_position': last_tweet}, headers=headers)
            pages += -1

    yield from gen_tweets(pages)
