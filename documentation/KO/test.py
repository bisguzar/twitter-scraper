import unittest
from twitter_scraper import get_tweets


class TestFamilyUnderscore(unittest.TestCase):

    def test_father(self):
        user = '_'
        tweets = list(get_tweets(query=user, pages=1))

        self.assertTrue(tweets[0]['text'].__contains__('나이가 들었다고 생각하고 싶으세요?'))

    def test_mother(self):
        user = '__'
        tweets = list(get_tweets(query=user, pages=1))

        self.assertTrue(tweets[0]['text'].__contains__('비욘세 시대에 살아 있는 것은 선물이다.'))

    def test_child(self):
        user = '___'
        tweets = list(get_tweets(query=user, pages=1))

        self.assertEqual(tweets[1]['text'], '할 수만 있다면 그럴 테지만, 할 수 없다면 그럴 수 없을 거예요.')


class TestPages(unittest.TestCase):

    def test_25pages(self):
        """저도 왜 인지는 모르겠지만, 어쩔 때에는 2~5 페이지 밖에 크롤링 되지 않습니다."""
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
