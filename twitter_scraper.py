import re
from requests_html import HTMLSession, HTML
from datetime import datetime
import json

session = HTMLSession()


def get_tweets(user, pages=25):
    """Gets tweets for a given user, via the Twitter frontend API."""

    url = f'https://twitter.com/i/profiles/show/{user}/timeline/tweets?include_available_features=1&include_entities=1&include_new_items_bar=true'
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
                html = HTML(html=r.json()['items_html'],
                            url='bunk', default_encoding='utf-8')
            except KeyError:
                raise ValueError(
                    f'Oops! Either "{user}" does not exist or is private.')

            comma = ","
            dot = "."
            tweets = []
            for tweet in html.find('.stream-item'):
                text = tweet.find('.tweet-text')[0].full_text
                tweetId = tweet.find(
                    '.js-permalink')[0].attrs['data-conversation-id']
                time = datetime.fromtimestamp(
                    int(tweet.find('._timestamp')[0].attrs['data-time-ms'])/1000.0)
                interactions = [x.text for x in tweet.find(
                    '.ProfileTweet-actionCount')]
                replies = int(interactions[0].split(" ")[0].replace(comma, "").replace(dot,""))
                retweets = int(interactions[1].split(" ")[
                               0].replace(comma, "").replace(dot,""))
                likes = int(interactions[2].split(" ")[0].replace(comma, "").replace(dot,""))
                hashtags = [hashtag_node.full_text for hashtag_node in tweet.find('.twitter-hashtag')]
                urls = [url_node.attrs['data-expanded-url'] for url_node in tweet.find('a.twitter-timeline-link:not(.u-hidden)')]
                photos = [photo_node.attrs['data-image-url'] for photo_node in tweet.find('.AdaptiveMedia-photoContainer')]
                
                videos = []
                video_nodes = tweet.find(".PlayableMedia-player")
                for node in video_nodes:
                    styles = node.attrs['style'].split()
                    for style in styles:
                        if style.startswith('background'):
                            tmp = style.split('/')[-1]
                            video_id = tmp[:tmp.index('.jpg')]
                            videos.append({'id': video_id})
                tweets.append({'tweetId': tweetId, 'time': time, 'text': text,
                               'replies': replies, 'retweets': retweets, 'likes': likes, 
                               'entries': {
                                    'hashtags': hashtags, 'urls': urls,
                                    'photos': photos, 'videos': videos
                                }
                               })

            last_tweet = html.find('.stream-item')[-1].attrs['data-item-id']

            for tweet in tweets:
                if tweet:
                    tweet['text'] = re.sub('http', ' http', tweet['text'], 1)
                    yield tweet

            r = session.get(
                url, params = {'max_position': last_tweet}, headers = headers)
            pages += -1

    yield from gen_tweets(pages)
    
def _get_tweet_text(result, tweet_from):
    """parse a result li element to extract the text"""
    text = ''
    for div in result.find('div'):
        reply_to = div.attrs.get('data-reply-to-users-json')
        if reply_to:
            obj = json.loads(reply_to.encode(errors='ignore'))
            for user in obj:
                if user['screen_name'] != tweet_from:
                    text += f'@{user["screen_name"]} '

    return text + result.find('p')[0].full_text

def search(query):
    """perform Twitter search without auth"""
    url = 'https://twitter.com/i/search/timeline'
    params = {
        'vertical': 'news',
        'src': 'typd',
        'include_entities': 0,
        'composed_count': 0,
        'oldest_unread_id': 0,
        'q': query,
        'f': 'realtime',
    }
    resp = session.get(url, params=params)

    items_html = resp.json()['items_html']
    html = HTML(
        html=items_html,
        url='bunk', default_encoding='utf-8')

    tweets = []
    for result in html.find('li'):
        try:
            timestamp = None
            for link in result.find('span'):
                timestamp = link.attrs.get('data-time')
                if timestamp:
                    break
            div = result.find('div')[0]
            screen_name = div.attrs['data-screen-name']
            tweet = {
                'id': int(result.attrs['data-item-id']),
                'id_str': str(result.attrs['data-item-id']),
                'url': f'https:/twitter.com{div.attrs["data-permalink-path"]}',
                'timestamp': int(timestamp),
                'created_at': datetime.fromtimestamp(int(timestamp)).strftime('%a %b %d %H:%M:%S +0000 %Y'),
                'user':{
                    'screen_name': screen_name,
                    'id_str': str(div.attrs['data-user-id']),
                    'name': div.attrs['data-name'],
                }
            }
            tweet['text'] = _get_tweet_text(result, tweet_from=screen_name)
        except KeyError:
            continue
        except IndexError:
            continue
        
        tweets.append(tweet)
    return tweets
