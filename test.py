import unittest
from twitter_scraper import get_tweets


class TestFamilyUnderscore(unittest.TestCase):

    def test_father(self):
        user = '_'
        tweets = list(get_tweets(user=user, pages=1))

        self.assertTrue(tweets[0]['text'].__contains__('Want to feel old?'))

    def test_mother(self):
        user = '__'
        tweets = list(get_tweets(user=user, pages=1))

        self.assertTrue(tweets[0]['text'].__contains__('It is a gift to be alive in the time of Beyoncé'))

    def test_child(self):
        user = '___'
        tweets = list(get_tweets(user=user, pages=1))

        self.assertEqual(tweets[1]['text'], 'If I could, I would, but if I can’t, I wan’t.')


class TestPages(unittest.TestCase):
    """
    In some cases it only crawls 2~5 pages
    """

    def test_25pages(self):
        user = 'kennethreitz'
        tweets = list(get_tweets(user=user, pages=25))
        self.assertGreater(len(tweets), 486)


if __name__ == '__main__':
    unittest.main()
