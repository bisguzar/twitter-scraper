# Twitter Scraper

![GitHub](https://img.shields.io/github/license/bisguzar/twitter-scraper) ![GitHub contributors](https://img.shields.io/github/contributors/bisguzar/twitter-scraper) ![code size](https://img.shields.io/github/languages/code-size/bisguzar/twitter-scraper) ![maintain status](https://img.shields.io/maintenance/yes/2020)

Twitter's API is annoying to work with, and has lots of limitations — luckily their frontend (JavaScript) has it's own API, which I reverse–engineered. No API rate limits. No restrictions. Extremely fast.

You can use this library to get the text of any user's Tweets trivially.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Internet Connection
* Python 3.6+

## Installing twitter-scraper

If you want to use latest version, install from source. To install twitter-scraper from source, follow these steps:

Linux and macOS:
```bash
git clone https://github.com/bisguzar/twitter-scraper.git
cd twitter-scraper
sudo python3 setup.py install 
```

Also, you can install with PyPI.

```bash
pip3 install twitter_scraper
```

## Using twitter_scraper

Just import **twitter-scraper** and call functions!

### **get_tweets()**
You can get tweets of profile or parse tweets from hashtag, **get_tweets** takes username or hashtag on first parameter as string and how much pages you want to scan on second parameter as integer. 

#### Keep in mind:
* First parameter need to start with #, number sign, if you want to get tweets from hashtag.
* **pages** parameter is optional.

```python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from twitter_scraper import get_tweets
>>> 
>>> for tweet in get_tweets('twitter', pages=1):
...     print(tweet['text'])
... 
spooky vibe check
…
```

It returns a dictionary for each tweet. Keys of the dictionary;

| Key       | Type       | Description                                                      |
|-----------|------------|------------------------------------------------------------------|
| tweetId   | string     | Tweet's identifier, visit twitter.com/USERNAME/ID to view tweet. |
| isRetweet | boolean    | True if it is a retweet, False othercase                         |
| time      | datetime   | Published date of tweet                                          |
| text      | string     | Content of tweet                                                 |
| replies   | integer    | Replies count of tweet                                           |
| retweets  | integer    | Retweet count of tweet                                           |
| likes     | integer    | Like count of tweet                                              |
| entries   | dictionary | Has hashtags, videos, photos, urls keys. Each one's value is list|

## Contributing to twitter-scraper
To contribute to twitter-scraper, follow these steps:

1. Fork this repository.
2. Create a branch with clear name: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contributors

Thanks to the following people who have contributed to this project:

* @kennethreitz (author)
* @bisguzar (maintainer)
* @lionking6792


## Contact
If you want to contact me you can reach me at [@bugraisguzar](https://twitter.com/bugraisguzar).


## License
This project uses the following license: [MIT](https://github.com/bisguzar/twitter-scraper/blob/master/LICENSE).
