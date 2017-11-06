from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import src.manipulate_tweets as mt


if __name__ == '__main__':
    tweets_data_path = "data/tweets_data.txt"
    tweets_data = mt.load_tweets_data(tweets_data_path)
    documents = ["Praise the fucking sun!",
                 "Daenerys is the mother of dragons.",
                 "Icarus flew too close to the sun.",
                 "Damn, Icarus got it tough, man.",
                 "Jon Fucking Snow fucked his aunt, Daenerys!",
                 "You're a wizard, Harry.",
                 "Hold the door, Hodor.",
                 "A quick brown fox jumps over the lazy dog."]

    documents_2 = ("The sky is blue.",
                   "The sun is bright.",
                   "The sun in the sky is bright.",
                   "We can see the shining sun, the bright sun.")

    documents_3 = mt.preprocess_tweet(tweets_data)

    tfidf = TfidfVectorizer(tokenizer=mt.tokenize_tweet)
    tfidf_matrix = tfidf.fit_transform(documents_2)

    print("Vocabulary:", tfidf.vocabulary_)
    print("Matrix shape:", tfidf_matrix.shape)
    print("TF-IDF:", tfidf_matrix.todense())
    print("SS:", tfidf_matrix[0:1])
    print("Cosine Similarity of 1st and 3rd documents =", cosine_similarity(tfidf_matrix[0:1],
        tfidf_matrix[2:3]))
