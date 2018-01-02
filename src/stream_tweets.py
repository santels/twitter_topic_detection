import json
import time
import schedule

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from datetime import datetime
from http.client import IncompleteRead
from urllib3.exceptions import ProtocolError


with open('.access_tokens.json') as data_file:
    data = json.load(data_file)

access_token = data["access_token"]
access_token_secret = data["access_token_secret"]
consumer_key = data["consumer_key"]
consumer_secret = data["consumer_secret"]


def get_stream_instance():
    """
    Returns a dict containig instances of TweetStreamListener and OAuthHandler.
    """
    tsl = TweetStreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return {
             "tsl":tsl,
             "auth":auth
           }


class TweetStreamListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
        Writes retrieved tweets to file.
    """
    pathname = ''

    def on_status(self, status):
        """
        Retrieves tweet data and writes it to file.
        """
        try:
            # Save streamed tweets to "data" folder
            with open(self.pathname, 'a') as td:
                # If tweet language is English, save
                if (status.lang is not None and status.lang == 'en'):
                    td.write(json.dumps(status._json))
                    td.write('\n')
                return True

        except BaseException as e:
            print("[ERROR] on_status: {}".format(e))

        return True

    def on_error(self, status):
        print("[ERROR] {}".format(status))

    def on_limit(self, track):
        """
        Called when limitation notice arrives on stream.
        """
        print("[WARNING] Limitation notice received: {}".format(track))
