from calculate_similarity import Similarity
from manipulate_tweets import ManipulateTweet
from graph import Graph


def run():
   # documents = ["Praise the fucking sun!",
   #              "Daenerys is the mother of dragons.",
   #              "Icarus flew too close to the sun.",
   #              "Damn, Icarus got it tough, man.",
   #              "Jon Fucking Snow fucked his aunt, Daenerys!",
   #              "You're a wizard, Harry.",
   #              "Hold the door, Hodor.",
   #              "A quick brown fox jumps over the lazy dog."]

    documents2 = ("The sky is blue. #Outdoors",
                  "The dog is barking.",#"The sun is bright.",
                  "The sun in the sky is bright.",
                  "We can see the shining sun, the bright sun. #Outdoors")

    #tweets_data_path = "data/tweets_data.txt"

    manip_tweet = ManipulateTweet()

    #tweets_data = manip_tweet.load_tweets_data(tweets_data_path)
    #documents_3 = manip_tweet.preprocess_tweet(tweets_data)

    sim = Similarity(documents2, manip_tweet)
    score_matrix = sim.similarity()
    graph = Graph(score_matrix, gtype='dict')

    print("Graph:", graph.graph)
    print("Matrix:", graph.create_graph(score_matrix, gtype='matrix'))














if __name__ == '__main__':
    run()
