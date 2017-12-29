import numpy as np

import mcl
import cluster_scoring as cs

from calculate_similarity import Similarity
from manipulate_tweets import ManipulateTweet


def run():
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

    documents3 = ["The sky is blue. #Outdoors",
                  "The dog is barking.",  # "The sun is bright.",
                  "The sun in the sky is bright.",
                  "Was that an earthquake???? Motherfucker!!!",
                  "We can see the shining sun, the bright sun. #Outdoors"]

    tweets_data_path = "data/tweets_data_3.txt"

    manip_tweet = ManipulateTweet()

    tweets_data = manip_tweet.load_tweets_data(tweets_data_path)
    documents_3 = manip_tweet.preprocess_tweet(tweets_data)

    #tokens = manip_tweet.tokenize_tweets(documents_3[:20])
    tokens = manip_tweet.tokenize_tweets(documents2)
    print("Tokenization completed!")
    print("No. of tokenized tweets:", len(tokens))

    #for k, v in tokens.items():
    #    print("{} [{}]\n========".format(k, v))

    # Similarity function
    sim = Similarity(tokens)
    print("No. of Features:", len(sim.get_features()))
    #score_matrix = sim.cos_similarity() # Cosine similarity
    score_matrix = sim.similarity()    # Soft cosine similarity
    print("Similarity function operation completed!")

    # Clustering
    matrix = mcl.cluster(score_matrix, iter_count=100)
    clusters, matrix = mcl.get_clusters(matrix)
    #mcl.draw(matrix, clusters)
    print("Clustering finished!")

    # Cluster scoring
    scores = [s for s in cs.score(sim.similarity, matrix, clusters)]
    print("Scoring finished!")
    max_score = np.max(scores)
    tweet_list = list(tokens.values())
    for tweet_index in clusters[np.argmax(scores)]:
        print("{}. {}".format(tweet_index, tweet_list[tweet_index]))
    print("Max score: {} = {}".format(max_score, clusters[np.argmax(scores)]))

    #print("Features:\n", sim._features)
    #print("Matrix:\n", score_matrix)
    #print("MCL Result:\n", matrix)
    print("Clusters :", clusters)
    print("No. of Clusters: \n", len(clusters))













if __name__ == '__main__':
    run()
