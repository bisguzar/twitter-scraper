import unittest
from twitter_scraper import get_tweets, get_trends


class TestFamilyUnderscore(unittest.TestCase):
    def test_father(self):
        user = "_"
        tweets = list(get_tweets(query=user, pages=1))

        self.assertTrue(tweets[0]["text"].__contains__("Want to feel old?"))

    def test_mother(self):
        user = "__"
        tweets = list(get_tweets(query=user, pages=1))

        self.assertTrue(
            tweets[3]["text"].__contains__(
                "It is a gift to be alive in the time of Beyoncé"
            )
        )

    def test_child(self):
        user = "___"
        tweets = list(get_tweets(query=user, pages=1))

        self.assertEqual(tweets[1]["text"], "“Review mirror”")


class TestPages(unittest.TestCase):
    def test_25pages(self):
        """I don't know why but in some cases it only crawls 2~5 pages"""
        user = "gvanrossum"
        tweets = list(get_tweets(query=user, pages=25))
        self.assertGreater(len(tweets), 498)

    def test_languages(self):
        user = "fcbarcelona_jp"
        tweets = list(get_tweets(query=user, pages=1))
        self.assertIn("likes", tweets[0])
        self.assertIsInstance(tweets[0]["replies"], int)
        self.assertGreaterEqual(tweets[1]["retweets"], 0)

class TestSearch(unittest.TestCase):
    def search_25pages(self):
        tweets = list(get_tweets(search="hello, world!", pages=2))
        self.assertGreater(len(tweets), 1)
    def search_user(self):
        user = "gvanrossum"
        tweets = list(get_tweets(user, pages=2))
        self.assertGreater(len(tweets), 1)




class TestTrends(unittest.TestCase):
    def test_returned(self):
        self.assertIsInstance(get_trends(), list)

    def test_returned_string(self):
        for trend in get_trends():
            self.assertIsInstance(trend, str)


if __name__ == "__main__":
    unittest.main()
