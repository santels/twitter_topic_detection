import re
import json

from spacy.lang.en import English
from spacy.matcher import Matcher

from stop_words import STOP_WORDS


class ManipulateTweet:
    """
    Manipulate Tweet class.
    """

    def __init__(self):
        self.nlp = English()
        self.matcher = Matcher(self.nlp.vocab)
        self.matcher.add('HASHTAG', self._merge_hashtags,
                [{'ORTH': '#'}, {'IS_ASCII': True}])

    def load_tweets_data(self, path):
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

    def preprocess_tweet(self, tweet_data):
        """
        Preprocesses tweets by cleaning the text:
            1. Removes URLs
            2. Removes emojis and special characters
            3. Removes "RT"'s and @ symbols indicating mentions
        """
        tweets = [self._clean_tweet(t["text"]) for t in tweet_data.__iter__()]
        return tweets

    def _merge_hashtags(self, matcher, doc, i, matches):
        """
        Utility function to merge hashtag and words next to it as tokens.
        Code located in spacy docs:
        https://spacy.io/usage/linguistic-features#example3
        """
        match_id, start, end = matches[i]
        span = doc[start : end]
        span.merge() # merge hashtag

    def tokenize(self, tweet):
        """
        Tokenizes tweet, removes stopwords and punctuations and returns list of
        tokens.
        """
        tokens = self.nlp(tweet)
        self.matcher(tokens)
        tokens = [i.norm_ for i in tokens if not i.is_punct and \
                i.norm_ not in STOP_WORDS and \
                "'" != i.norm_[0] and \
                i.is_ascii and \
                not i.is_space]
        return tokens if tokens != [] else None

    def _clean_tweet(self, text):
        text = self._remove_link(text)
        text = self._remove_emojis(text)
        text = self._remove_mentions(text)

        return text

    def _remove_emojis(self, text):
        emoji_pattern = re.compile("["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\u261E"                 # ☞ additional
            "\u2026"                 # ellipsis
        "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)

    def _remove_link(self, text):
        regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        return re.sub(regex, '', text)

    def _remove_mentions(self, text):
        regex = r'(RT )*@[^\s]*'
        return re.sub(regex, '', text)


if __name__ == '__main__':
    c = ManipulateTweet()
    tweets_data_path = "data/tweets_data.txt"
    tweets_data = c.load_tweets_data(tweets_data_path)
    documents_3 = c.preprocess_tweet(tweets_data)
    documents_3 = documents_3 * 10
    x = []
    for i in documents_3.__iter__():
        g = c.tokenize(i)
        if g is not None:
            x.append(g)

    print(len(x))
