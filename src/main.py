import mcl

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
                  "The dog is barking.",#"The sun is bright.",
                  "The sun in the sky is bright.",
                  "We can see the shining sun, the bright sun. #Outdoors",
                  "The cat is meowing back at the dog.",
                  "The dog and cat fought each other."
                  ]

    tweets_data_path = "data/tweets_data_3.txt"

    manip_tweet = ManipulateTweet()

    tweets_data = manip_tweet.load_tweets_data(tweets_data_path)
    documents_3 = manip_tweet.preprocess_tweet(tweets_data)

    tokens = manip_tweet.tokenize_tweets(documents_3)
    sim = Similarity(tokens)
    #score_matrix = sim.similarity()
    #matrix = mcl.cluster(score_matrix, iter_count=100)
    #clusters = mcl.get_clusters(matrix)

    print("Features:\n", sim._features)
    #print("Matrix:\n", score_matrix)
    #print("MCL Result:\n", matrix)
    print("Clusters: \n", clusters)
    print("No. of Clusters: \n", len(clusters))
    print("No. of Features: \n", len(sim._features))













if __name__ == '__main__':
    run()
