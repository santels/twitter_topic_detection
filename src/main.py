import mcl

from calculate_similarity import Similarity
from manipulate_tweets import ManipulateTweet


def run():
    documents = set(["Praise the fucking sun!",
                 "Daenerys is the mother of dragons.",
                 "Icarus flew too close to the sun.",
                 "Damn, Icarus got it tough, man.",
                 "Jon Fucking Snow fucked his aunt, Daenerys!",
                 "You're a wizard, Harry.",
                 "Hold the door, Hodor.",
                 "A quick brown fox jumps over the lazy dog."])

    documents2 = set(["The sky is blue. #Outdoors",
                  "The dog is barking.",#"The sun is bright.",
                  "The sun in the sky is bright.",
                  "We can see the shining sun, the bright sun. #Outdoors",
                  "The cat is meowing back at the dog.",
                  "The dog and cat fought each other."])

    #tweets_data_path = "data/tweets_data.txt"

    manip_tweet = ManipulateTweet()

    #tweets_data = manip_tweet.load_tweets_data(tweets_data_path)
    #documents_3 = manip_tweet.preprocess_tweet(tweets_data)

    sim = Similarity(documents, manip_tweet)
    score_matrix = sim.similarity()
    matrix = mcl.cluster(score_matrix, iter_count=5)

    print("Matrix:\n", score_matrix)
    print("Result:\n", matrix)













if __name__ == '__main__':
    run()
