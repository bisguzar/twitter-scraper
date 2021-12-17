import re
from requests_html import HTMLSession, HTML
from datetime import datetime
from urllib.parse import quote
from lxml.etree import ParserError

session = HTMLSession()

def get_tweets(query=None, search=None, pages=25):
    """Gets tweets for a given user, via the Twitter frontend API."""

    if not query and not search:
        raise RuntimeError("Please specify a 'query' or a 'search' to check the tweets on.")
    elif query and search:
        raise RuntimeError("Please specify only one of either a 'search' or 'query'.")	

    after_part = (
        f"include_available_features=1&include_entities=1&include_new_items_bar=true"
    )
    if not query: # if query not exists, it's a search method
        search_term=quote(search)
        url = f"https://twitter.com/i/search/timeline?f=tweets&vertical=default&q={search_term}&src=tyah&reset_error_state=false&"

    elif query.startswith("#"):
        query = quote(query)
        url = f"https://twitter.com/i/search/timeline?f=tweets&vertical=default&q={query}&src=tyah&reset_error_state=false&"
    else:
        url = f"https://twitter.com/i/profiles/show/{query}/timeline/tweets?"
    url += after_part

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": f"https://twitter.com/{query}",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
        "X-Twitter-Active-User": "yes",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "en-US",
    }

    def gen_tweets(pages):
        request = session.get(url + '&max_position', headers=headers)

        while pages > 0:
            try:
                json_response = request.json()
                html = HTML(
                    html=json_response["items_html"], url="bunk", default_encoding="utf-8"
                )
            except KeyError:
                raise ValueError(
                    f'Oops! Either "{query}" does not exist or is private.'
                )
            except ParserError:
                break

            comma = ","
            dot = "."
            tweets = []
            for tweet, profile in zip(
                html.find(".stream-item"), html.find(".js-profile-popup-actionable")
            ):
                # 10~11 html elements have `.stream-item` class and also their `data-item-type` is `tweet`
                # but their content doesn't look like a tweet's content
                try:
                    text = tweet.find(".tweet-text")[0].full_text
                except IndexError:  # issue #50
                    continue


                tweet_id = tweet.attrs["data-item-id"]
                tweet_url = profile.attrs["data-permalink-path"]
                username = profile.attrs["data-screen-name"]
                user_id = profile.attrs["data-user-id"]
                is_pinned = bool(tweet.find("div.pinned"))

                time = datetime.fromtimestamp(
                    int(tweet.find("._timestamp")[0].attrs["data-time-ms"]) / 1000.0
                )

                interactions = [x.text for x in tweet.find(".ProfileTweet-actionCount")]

                replies = int(
                    interactions[0].split(" ")[0].replace(comma, "").replace(dot, "")
                    or interactions[3]
                )

                retweets = int(
                    interactions[1].split(" ")[0].replace(comma, "").replace(dot, "")
                    or interactions[4]
                    or interactions[5]
                )

                likes = int(
                    interactions[2].split(" ")[0].replace(comma, "").replace(dot, "")
                    or interactions[6]
                    or interactions[7]
                )

                hashtags = [
                    hashtag_node.full_text
                    for hashtag_node in tweet.find(".twitter-hashtag")
                ]

                urls = [
                    url_node.attrs["data-expanded-url"]
                    for url_node in (
                        tweet.find("a.twitter-timeline-link:not(.u-hidden)") +
                        tweet.find("[class='js-tweet-text-container'] a[data-expanded-url]")
                    )
                ]
                urls = list(set(urls)) # delete duplicated elements

                photos = [
                    photo_node.attrs["data-image-url"]
                    for photo_node in tweet.find(".AdaptiveMedia-photoContainer")
                ]

                is_retweet = (
                    True
                    if tweet.find(".js-stream-tweet")[0].attrs.get(
                        "data-retweet-id", None
                    )
                    else False
                )

                videos = []
                video_nodes = tweet.find(".PlayableMedia-player")
                for node in video_nodes:
                    styles = node.attrs["style"].split()
                    for style in styles:
                        if style.startswith("background"):
                            tmp = style.split("/")[-1]
                            video_id = (
                                tmp[: tmp.index(".jpg")]
                                if ".jpg" in tmp
                                else tmp[: tmp.index(".png")]
                                if ".png" in tmp
                                else None
                            )
                            videos.append({"id": video_id})

                tweets.append(
                    {
                        "tweetId": tweet_id,
                        "tweetUrl": tweet_url,
                        "username": username,
                        "userId": user_id,
                        "isRetweet": is_retweet,
                        "isPinned": is_pinned,
                        "time": time,
                        "text": text,
                        "replies": replies,
                        "retweets": retweets,
                        "likes": likes,
                        "entries": {
                            "hashtags": hashtags,
                            "urls": urls,
                            "photos": photos,
                            "videos": videos,
                        },
                    }
                )

            last_tweet = html.find(".stream-item")[-1].attrs["data-item-id"]

            for tweet in tweets:
                tweet["text"] = re.sub(r"(\S)http", "\g<1> http", tweet["text"], 1)
                tweet["text"] = re.sub(
                    r"(\S)pic\.twitter", "\g<1> pic.twitter", tweet["text"], 1
                )
                yield tweet

            request = session.get(url, params={"max_position": json_response['min_position']}, headers=headers)
            pages += -1

    yield from gen_tweets(pages)


# for searching:
#
# https://twitter.com/i/search/timeline?vertical=default&q=foof&src=typd&composed_count=0&include_available_features=1&include_entities=1&include_new_items_bar=true&interval=30000&latent_count=0
# replace 'foof' with your query string.  Not sure how to decode yet but it seems to work.
