import time
import schedule
import numpy as np

import mcl
import cluster_scoring as cs
import stream_tweets as st
from calculate_similarity import Similarity
from manipulate_tweets import ManipulateTweet


STREAM_INTERVAL = 20
PROCESS_INTERVAL = 30

file_list = []


def run(trigger='both'):
    """
    Entry point of the program.
    """
    schedule.clear()
    # Run streamer only
    if trigger == 'stream':
        streamer = st.get_stream_instance()

        schedule.every(STREAM_INTERVAL).minutes.do(run_streaming,
                streamer["tsl"], streamer["auth"])
        while True:
            schedule.run_pending()

    # Run tweet processor only
    elif trigger == 'process':
        schedule.every(PROCESS_INTERVAL).minutes.do(run_tweet_processing)
        while True:
            schedule.run_pending()

    # Run both streamer and tweet processor
    else:
        streamer = st.get_stream_instance()
        schedule.every(STREAM_INTERVAL).minutes.do(run_streaming,
                streamer["tsl"], streamer["auth"])
        schedule.every(PROCESS_INTERVAL).minutes.do(run_tweet_processing)
        while True:
            schedule.run_pending()


def run_streaming(tsl, auth):
    """
    Runs streaming process.
    """
    timestr = time.strftime("%Y%m%d-%H%M")
    tsl.pathname = 'data/td-' + timestr + '.txt'
    # Tries to reconnect to stream after IncompleteRead/ProtocolError
    # exceptions are caught.
    print("Stream running...")
    start = time.time()
    while True:
        try:
            # Connect/reconnect the stream
            stream = Stream(auth, tsl)
            print("Getting samples...")
            stream.sample()
            if _get_time(start, STREAM_INTERVAL) == STREAM_INTERVAL:
                file_list.append(tsl.pathname)
                break
        except (IncompleteRead, ProtocolError):
            # Ignores exception and continues
            continue
        except KeyboardInterrupt:
            # Exits loop
            print("Stream ended.")
            stream.disconnect()
            break


def run_tweet_processing():
    """
    Runs modules in processing collected tweets.
    """
    print("Starting operation...")
    documents = [
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
                  "The dog is barking.",  # "The sun is bright.",
                  "The sun in the sky is bright.",
                  "Was that an earthquake???? Motherfucker!!!",
                  "We can see the shining sun, the bright sun. #Outdoors",
                  "The cat is meowing back at the dog.",
                  "The dog and cat fought each other.",
                  "I think that was magnitude 5.4?!?! I thought I died! Damn, nigga, wtf. Where was the epicenter??",
                  "That trembles the ground so much, man!!!! Aftershock would kill mah guts.",
                  "Martin played with his new PS4.",
                  "Lucas really liked gaming with his PS4.",
                  "Quit playing games with mah heart, mofo!",
                  ]

    documents3 = ["The sky is blue.",
                  "The sun is bright.",
                  "I saw Jim's wife yesterday with their dog, Barn.",
                  "The sun in the sky is bright.",
                  "We can see the scorching sun, the bright sun.",
                  "Marissa--Jim's wife--was walking with Barn earlier.",
                  "Have you seen the the moon and Earth?"]

    tweets_data_path = file_list[-1]

    start = time.time()
    manip_tweet = ManipulateTweet()

    tweets_data = manip_tweet.load_tweets_data(tweets_data_path)
    tweets = manip_tweet.preprocess_tweet(tweets_data)

    print("Tokenizing...")
    tokens = manip_tweet.tokenize_tweets(tweets[:100])
    #tokens = manip_tweet.tokenize_tweets(documents2)
    print("Tokenization completed!")
    print("No. of tokenized tweets:", len(tokens))
    print("> Elapsed:", time.strftime("%H:%M:%S", time.gmtime(time.time() - start)))

    # Similarity function
    print("Getting similarity between tweets...")
    sim = Similarity(tokens)
    print("No. of Features:", len(sim.get_features()))
    #score_matrix = sim.cos_similarity() # Cosine similarity
    score_matrix = sim.similarity()    # Soft cosine similarity
    print("Similarity function operation completed!")
    print("> Elapsed:", time.strftime("%H:%M:%S", time.gmtime(time.time() - start)))

    # Clustering
    print("Clustering...")
    matrix = mcl.cluster(score_matrix, iter_count=1000)
    clusters, matrix = mcl.get_clusters(matrix)
    #mcl.draw(matrix, clusters)
    print("Clustering finished!")
    print("> Elapsed:", time.strftime("%H:%M:%S", time.gmtime(time.time() - start)))

    # Cluster scoring
    print("Scoring...")
    scores = [s for s in cs.score(sim.similarity, matrix, clusters)]
    print("Scoring finished!")
    print("> Elapsed:", time.strftime("%H:%M:%S", time.gmtime(time.time() - start)))

    max_score = np.max(scores)
    tweet_list = list(tokens.keys())
    for tweet_index in clusters[np.argmax(scores)]:
        print("{}. {}".format(tweet_index, tweet_list[tweet_index]))
    print("Max score: {} = {}".format(max_score, clusters[np.argmax(scores)]))

    #print("Features:\n", sim._features)
    #print("Matrix:\n", score_matrix)
    #print("MCL Result:\n", matrix)
    #print("Clusters:", clusters)
    print("No. of Clusters:", len(clusters))


def _get_time(start, interval):
    return round(interval - ((time.time() - start) % interval))










if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] in ('--stream-only', '-so'):
            run('stream')
        elif sys.argv[1] in ('--process-only', '-po'):
            run('process')
        else:
            run()
    else:
        run()
