import re
import json
import string
import pandas as pd

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer


def load_tweets_data(path):
    """
    Loads tweet data from the specified path.
    """
    tweets_data = []
    tweets_file = open(path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue

    return tweets_data


def preprocess_tweet(text):
    """
    Preprocesses tweets by:
    1. Cleaning the text:
        1.1 Removes URLs
        1.2 Removes emojis and special characters
        1.3 Removes "RT"'s and @ symbols indicating mentions
    2. Removing stopwords and most common unnecessary words.
    3. Tokenizing the text by splitting it into tokens.
    """
    tokenizer = TweetTokenizer()

    text = clean_tweet(text)
    stop_words = stopwords.words('english') + list(string.punctuation)
    tokens = tokenizer.tokenize(text)

    # Removes stopwords in a tweet
    filtered_tokens = [w for w in tokens if w not in stop_words]

    return filtered_tokens


def clean_tweet(text):
    text = remove_link(text)
    text = remove_emojis(text)
    text = remove_mentions(text)

    return text


def remove_emojis(text):
    emoji_pattern = re.compile("["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\u261E"                 # ☞ additional
        "\u2026"                 # ellipsis
    "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def remove_link(text):
    regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    return re.sub(regex, '', text)


def remove_mentions(text):
    regex = r'(RT )*@[^\s]*'
    return re.sub(regex, '', text)


if __name__ == '__main__':
    tweets_data_path = "data/tweets_data_2.txt"
    tweets_data = load_tweets_data(tweets_data_path)
    sample_tweets = map(lambda tweet: preprocess_tweet(tweet['text']), tweets_data)
    sample_tweets = [i for i in sample_tweets]

    for i, t in enumerate(sample_tweets[10:21]):
        print("{}. {}".format(i + 1, t))
    print("Number of tweets:", len(tweets_data))
