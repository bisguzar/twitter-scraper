Twitter Scraper
===============

Twitter's API is annoying to work with, and has lots of limitations —
luckily their frontend (JavaScript) has it's own API, which I reverse–engineered.
No API rate limits. No restrictions. Extremely fast.

You can use this library to get the text of any user's Tweets trivially.

Very useful for making markov chains.

Usage
=====

.. code-block:: pycon

    >>> from twitter_scraper import get_tweets

    >>> for tweet in get_tweets('kennethreitz', pages=1):
    >>>     print(tweet)
    P.S. your API is a user interface
    s3monkey just hit 100 github stars! Thanks, y’all!
    I’m not sure what this /dev/fd/5 business is, but it’s driving me up the wall.
    …

It appears you can ask for up to 25 pages of tweets reliably (~486 tweets).

Installation
============

.. code-block:: shell

    $ pipenv install twitter_scraper

Only Python 3.6 is supported.