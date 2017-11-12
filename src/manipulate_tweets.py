import re
import json
import string
import pandas as pd

from nltk.corpus import stopwords


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


def preprocess_tweet(tweet_data):
    """
    Preprocesses tweets by cleaning the text:
        1. Removes URLs
        2. Removes emojis and special characters
        3. Removes "RT"'s and @ symbols indicating mentions
    """
    tweets = [clean_tweet(t["text"]) for t in tweet_data]
    return tweets


def get_stopwords():
    """
    Returns list of stopwords and punctuations to be removed.
    """
    return stopwords.words('english') + list(string.punctuation)


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
