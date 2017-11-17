from calculate_similarity import Similarity
from collections import defaultdict

from manipulate_tweets import ManipulateTweet


class Graph:
    """
    Graph class implementation.
    """
    def __init__(self, matrix=None):
        if matrix is not None:
            self.graph = self.create_graph(matrix)

    def create_graph(self, matrix):
        """
        Creates an undirected weighted graph. Uses the similarity scores of
        each document as weights of the edges and the documents as vertices.
        """
        graph = defaultdict(list)
        for row_i in range(len(matrix)):
            for col_i in range(len(matrix[0])):
                if matrix[row_i, col_i] != 0:
                    graph[row_i].append( (col_i+1, matrix[row_i, col_i]) )
                    graph[col_i+1].append( (row_i, matrix[row_i, col_i]) )

        return graph














if __name__ == '__main__':
    documents = ["Praise the fucking sun!",
                 "Daenerys is the mother of dragons.",
                 "Icarus flew too close to the sun.",
                 "Damn, Icarus got it tough, man.",
                 "Jon Fucking Snow fucked his aunt, Daenerys!",
                 "You're a wizard, Harry.",
                 "Hold the door, Hodor.",
                 "A quick brown fox jumps over the lazy dog."]

    documents2 = ("The sky is blue. #Outdoors",
                  "The dog is barking.",#"The sun is bright.",
                  "The sun in the sky is bright.",
                  "We can see the shining sun, the bright sun. #Outdoors")

    manip_tweet = ManipulateTweet()
    sim = Similarity(documents2, manip_tweet)
    score_matrix = sim.similarity()
    graph = Graph(score_matrix)
    print(graph.graph)
