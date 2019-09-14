

# Twitter Scraper
Twitter's API is annoying to work with, and has lots of limitations — luckily their frontend (JavaScript) has it's own API, which I reverse–engineered.

 
  - [Why use it instead of the existing Twitter frontend api?](#1-why-use-it-instead-of-the-existing-twitter-frontend-api)
  - [How to use?](#2how-to-use)  
  - [Installating](#installating)      
  - [Important functions and their uses](#important-functions-and-their-uses)
  - [Woohoo now let's have some fun](#3woohoo-now-lets-have-some-fun)  
  - [quick Examples and Usage](#quick-examples-and-usage)
  - [Using the scrapper with Markovify](#4-using-the-scrapper-with-markovify)


##  Why use it instead of the existing Twitter frontend api? 
No API rate limits.

No restrictions.

Extremely fast.

You can use this library to get the text of any user's Tweets trivially. No extensive knowledge of apis or other technical jargon required. For example: you can use it to generate **Markov Chains** really fast.

##  How to use?

**Note: You need python 3.6+ to use this scraper**

### Installating 
1. check that you have python installed, go to your command prompt(if in Windows) or terminal (mac/Linux), then type ``python --version``. If you see something above 3.6 then you are good to go. 
2. If step 1 failed head over to [python website](https://www.python.org/) then follow their steps to download and install python for your python.
3. Next we need `pipenv`. I found [this article](https://medium.com/@mahmudahsan/how-to-use-python-pipenv-in-mac-and-windows-1c6dc87b403e) quite useful to get up and running with `pipenv`.
4. Finally run ``pipenv install twitter-scraper`` in your terminal/ command prompt. That's it!

### Important functions and their uses
You will mainly use the 

```get_tweets(query, pages=25)```

 function to parse and display the tweets. It takes two arguments:

query- the twitter handle of the page you want tweets from
pages-the max amount of pages data can be scraped from

In simple terms the function returns a list called tweets[] and to print the contents in a tweet you would write something like 

```print(tweets['text'])```



##  Woohoo now let's have some fun
### quick Examples and Usage
Let's scrape some tweets from the twitter page of [freecodecamp](https://www.freecodecamp.org/).

1. Create a python file in your favourite editor, say

 ```twits.py```

2. Next we need to import the twiter scraper to start using the module and parse tweets. So in your twits.py write

```from twitter_scraper import get_tweets```

3. Next we want to iterate over the tweets using a for loop instead for manually getting one tweet, so

    
       for tweet in get_tweet('freeCodeCamp', pages=1):

         print(tweet['text'])


4. Run the file from terminal using 

```pipenv run twits.py``` 

you will see a number of tweets from the twitter homepage of freecodecamp.

## Using the scrapper with Markovify
You can also use this to generate Markov chains. first install markovify

```pipenv install markovify```

then like above example create a python file like this

    import markovify
    from twitter_scraper import get_tweets
    tweets = '\n'.join([t['text'] for t in get_tweets('freeCodeCamp', pages=25)])
    text_model = markovify.Text(tweets)
    print(text_model.make_short_sentence(140))

Then run the file like above to get results.

to tinker more with Markov models head over to [markovify's github page](https://github.com/jsvine/markovify).

## License

MIT









 









