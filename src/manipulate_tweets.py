import re
import json

from collections import OrderedDict
from spacy.lang.en import English

from stop_words import STOP_WORDS


class ManipulateTweet:
    """
    Manipulate Tweet class.
    """

    def __init__(self):
        self.nlp = English()

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

    def _merge_hashtags(self, tweet, tokens):
        """
        Utility function to find and merge hashtag and words next to it as
        tokens.
        """
        indices = [match.span() for match in re.finditer('#\w+', tweet, flags=re.IGNORECASE)]
        for start, end in indices:
            tokens.merge(start_idx=start, end_idx=end)
        return tokens

    def _tokenize(self, tweet):
        """
        Tokenizes tweet, removes stopwords and punctuations and returns list of
        tokens.
        """
        tokens = self.nlp(tweet)
        tokens = self._merge_hashtags(tweet, tokens)
        tokens = [i.norm_ for i in tokens if not i.is_punct and \
                re.search(r'[\[\];\'\":<>,./?=+-_\)\(*&^%$@!~`\\|\{\}]', i.norm_) is None           and \
                i.norm_ not in STOP_WORDS                   and \
                "'" != i.norm_[0]                           and \
                i.is_ascii                                  and \
                not i.is_space]
        return tokens if tokens != [] else None

    def tokenize_tweets(self, tweet_data):
        """
        Tokenizes tweet data and converts it to dict (to be accessed properly
        in other modules). With document as keys and tokens as values.
        """
        tokens = OrderedDict()
        for tweet in tweet_data.__iter__():
            tokenized = self._tokenize(tweet)
            if tokenized is not None:
                tokens[tweet.lower()] = tokenized
        return tokens

    def _clean_tweet(self, text):
        text = self._remove_link(text)
        text = self._remove_emojis(text)
        text = self._remove_mentions(text)
        text = self._remove_html_characters(text)

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

    def _remove_html_characters(self, text):
        regex = r'&(.*);'
        return re.sub(regex, '', text)


if __name__ == '__main__':
    c = ManipulateTweet()
    tweets_data_path = "data/tweets_data_3.txt"
    tweets_data = c.load_tweets_data(tweets_data_path)
    documents = c.preprocess_tweet(tweets_data)
    documents3 = [
        "Apple is looking at buying U.K. startup for $1 billion",
        "Autonomous cars shift insurance liability toward manufacturers",
        "San Francisco considers banning sidewalk delivery robots",
        "London is a big city in the United Kingdom.",
        "Where are you?",
        "Who is the president of France?",
        "What is the capital of the United States?",
        "When was Barack Obama born?"
    ]
    documents2 = ["The sky is blue. #Outdoors",
                  "The dog is barking.",#"The sun is bright.",
                  "The sun in the sky is bright.",
                  "We can see the shining sun, the bright sun. #Outdoors",
                  "The cat is meowing back at the dog.",
                  "The dog and cat fought each other."
                  ]
    x = []
    for i in documents.__iter__():
        g = c._tokenize(i)
        if g is not None:
            x.append(g)

    for i in x[:15].__iter__():
        print(i)

    print("Length: {}".format(len(x)))
