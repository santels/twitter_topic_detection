import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from urllib3.exceptions import ProtocolError
from http.client import IncompleteRead
from datetime import datetime
from time import clock

access_token = "124689202-gdkYDTBPdJbmfhi2kDR7E87drsun0sMhiKhdPvlI"
access_token_secret = "sW6LYAW6ZDuC4PtDbKFWN4uFaJYQV2PbZZ5fOJYBzp9uw"
consumer_key = "HqtQlD3YOF1Qk0XApbsEO05mK"
consumer_secret = "9fNvyTG5t51yTePoa4wxpfZB1CzHU7JVXRHVTCWbJK454DN9XB"


class TweetStreamListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
        Writes retrieved tweets to file.
    """

    def on_status(self, status):
        """
        Retrieves tweet data and writes it to file.
        """
        try:

            # Save streamed tweets to "data" folder
            with open('data/tweets_data.txt', 'a') as td:
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


if __name__ == '__main__':

    print("Time started: {}".format(datetime.now()))

    #This handles Twitter authetification and the connection to Twitter Streaming API
    tsl = TweetStreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # stream = Stream(auth, tsl)

    # stream.filter(languages=['en'], track=['python', 'javascript', 'ruby'])
    # stream.sample()

    # Tries to reconnect to stream after IncompleteRead/ProtocolError exceptions are caught
    while True:
        try:
            # Connect/reconnect the stream
            stream = Stream(auth, tsl)
            stream.sample()
        except (IncompleteRead, ProtocolError):
            # Ignores exception and continues
            continue
        except KeyboardInterrupt:
            # Exits loop
            stream.disconnect()
            break

    print("Time ended: {}".format(datetime.now()))
