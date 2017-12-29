import re
import json
import spacy

from collections import OrderedDict

from stop_words import STOP_WORDS


class ManipulateTweet:
    """
    Manipulate Tweet class.
    """

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

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
        tweets = [self._clean_tweet(t["text"]) for t in tweet_data]
        return tweets

    def _merge_hashtags(self, tweet, tokens):
        """
        Utility function to find and merge hashtag and words next to it as
        tokens.
        """
        indices = [match.span() for match in re.finditer(
            '#\w+', tweet, flags=re.IGNORECASE)]
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
        tokens = [i for i in tokens if not i.is_punct and
                  re.search(r'[\[\];\'\":<>,.\/?=\+\-\_\)\(*&\^%\$@!~`\\|\{\}]',
                            i.norm_) is None and
                  not i.is_stop              and
                  i.norm_ not in STOP_WORDS  and
                  "'" != i.norm_[0]          and
                  i.is_ascii                 and
                  i.pos_ in ('NOUN', 'PROPN', 'VERB', 'NUM', 'SYM') and
                  not i.is_space]

        modified_tokens = []
        for tok in tokens:
            if '#' in tok.norm_:
                modified_tokens.append(tok.norm_)
            else:
                modified_tokens.append(tok.lemma_.lower())

        return modified_tokens if len(modified_tokens) > 0 else None

    def tokenize_tweets(self, tweet_data):
        """
        Tokenizes tweet data and converts it to dict (to be accessed properly
        in other modules). With document as keys and tokens as values.
        """
        tokens = OrderedDict()
        for tweet in tweet_data:
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
