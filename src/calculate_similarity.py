from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet as wn
from operator import itemgetter

import math
import manipulate_tweets as mt
import numpy as np


def soft_cosine_measure(v1, v2):
    """
    Soft Cosine Similarity Measure
    ------------------------------
    Traditional Cosine Similarity Measure that takes into account the
    semantic similarities of each features in each documents.
    """
    product = v1.dot(v2.transpose()).data

    if len(product) == 0:
        return 0

    product = product[0]
    denom1 = math.sqrt(v1.dot(v1.transpose()).data[0])
    denom2 = math.sqrt(v2.dot(v2.transpose()).data[0])
    return product / (denom1 * denom2)


def get_related_nouns(synset):
    """
    Gets derivationally related word forms as noun synsets of a given synset
    to measure its similarity to other terms.
    """
    return [rel.synset() for lemma in synset.lemmas()
                         for rel in lemma.derivationally_related_forms()
                         if rel.synset().pos() == 'n']


def get_feature_score(syn_a, syn_b):
    """
    If syn_a and syn_b are synsets, returns their similarity score. If they are
    lists, gets all similarity scores of each element and returns the best
    score.
    """
    score = 0
    if type(syn_a) is list and type(syn_b) is not list:
        score = max([wn.wup_similarity(syn_b, i) for i in syn_a])
    elif type(syn_a) is not list and type(syn_b) is list:
        score = max([wn.wup_similarity(syn_a, i) for i in syn_b])
    elif all(type(x) is list for x in (syn_a, syn_b)):
        score = max([wn.wup_similarity(i, j) for i in syn_a for j in syn_b])
    else:
        score = wn.wup_similarity(syn_a, syn_b)

    score = 0 if score is None else score
    return score


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
    features = [feat[0] for feat in sorted(
        tfidf.vocabulary_.items(), key=itemgetter(1))]
    print("Features:", features)

    for term_1 in features:
        for term_2 in features:
            print("{} && {} = ".format(term_1, term_2), end='')

            synset_1 = wn.synsets(term_1)[0]
            synset_2 = wn.synsets(term_2)[0]

            if synset_1.pos() != 'n':
                synset_1 = get_related_nouns(synset_1)

            if synset_2.pos() != 'n':
                synset_2 = get_related_nouns(synset_2)

            print(get_feature_score(synset_1, synset_2))

    print("Matrix shape:", tfidf_matrix.shape)
    print("TF-IDF:", tfidf_matrix.todense())
    print("Cosine Similarity of 1st and 3rd documents =", cosine_similarity(tfidf_matrix[0:1],
        tfidf_matrix))

    for i in range(tfidf_matrix.shape[0]):
        print(soft_cosine_measure(tfidf_matrix.getrow(0), tfidf_matrix.getrow(i)))
