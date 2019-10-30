import unittest
from twitter_scraper import get_tweets


class TestFamilyUnderscore(unittest.TestCase):

    def test_father(self):
        user = '_'
        tweets = list(get_tweets(query=user, pages=1))

        self.assertTrue(tweets[0]['text'].__contains__('Want to feel old?'))

    def test_mother(self):
        user = '__'
        tweets = list(get_tweets(query=user, pages=1))
        text = 'It is a gift to be alive in the time of Beyoncé'

        self.assertTrue(tweets[0]['text'].__contains__(text))

    def test_child(self):
        user = '___'
        tweets = list(get_tweets(query=user, pages=1))

        self.assertEqual(tweets[1]['text'], '“Review mirror”')


class TestPages(unittest.TestCase):

    def test_25pages(self):
        """I don't know why but in some cases it only crawls 2~5 pages"""
        user = 'kennethreitz'
        tweets = list(get_tweets(query=user, pages=25))
        self.assertGreater(len(tweets), 486)

    def test_languages(self):
        user = 'fcbarcelona_jp'
        tweets = list(get_tweets(query=user, pages=1))
        self.assertIn('likes', tweets[0])
        self.assertIsInstance(tweets[0]['replies'], int)
        self.assertGreaterEqual(tweets[1]['retweets'], 0)


if __name__ == '__main__':
    unittest.main()
