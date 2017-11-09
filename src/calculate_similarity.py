from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet as wn
from operator import itemgetter

import math
import numpy as np
import manipulate_tweets as mt


THRESHOLD = 0.5


def multiply_elements(v1, v2, features):
    """
    Multiplies values between vector elements and similarity function scores.
    """
    sum = 0
    for i in range(v1.shape[0]):
        for j in range(v1.shape[0]):

            feature_score = get_feature_score(features[i], features[j])
            if feature_score < THRESHOLD:
                feature_score = 0

            sum += v1[i] * v2[j] * feature_score
    return sum


def soft_cosine_measure(v1, v2, features):
    """
    Soft Cosine Similarity Measure
    ------------------------------
    Traditional Cosine Similarity Measure that takes into account the
    semantic similarities of each features in each documents.
    """
    v1 = v1.toarray()[0]
    v2 = v2.toarray()[0]
    product = multiply_elements(v1, v2, features)
    denom1 = math.sqrt(multiply_elements(v1, v1, features))
    denom2 = math.sqrt(multiply_elements(v2, v2, features))
    return product / (denom1 * denom2)


def get_synsets(term1, term2):
    """
    Gets synsets of each term, if the synset's pos() is not at noun or verb,
    it gets its related nouns/forms.
    """
    synset1 = wn.synsets(term1)
    synset2 = wn.synsets(term2)

    if (len(synset1) > 0):
        synset1 = synset1[0]

        if synset1.pos() not in  ('n', 'v'):
            synset1 = get_related_nouns(synset1)
    else:
        synset1 = None

    if (len(synset2) > 0):
        synset2 = synset2[0]

        if synset2.pos() not in  ('n', 'v'):
            synset2 = get_related_nouns(synset2)
    else:
        synset2 = None

    return synset1, synset2


def get_related_nouns(synset):
    """
    Gets derivationally related word forms as noun synsets of a given synset
    to measure its similarity to other terms.
    """
    return [rel.synset() for lemma in synset.lemmas()
                         for rel in lemma.derivationally_related_forms()
                         if rel.synset().pos() == 'n']


def get_feature_score(term1, term2):
    """
    If syn1 and syn2 are synsets, returns their similarity score. If they are
    lists, gets all similarity scores of each element and returns the best
    score.
    """
    syn1, syn2 = get_synsets(term1, term2)

    # If one/both synset/s is/are not found in WordNet. If it's not found, its
    # value is None, otherwise, a Synset object.
    if all((syn1, syn2)) == False:
        return 0 

    score = 0
    if type(syn1) is list and type(syn2) is not list:
        score = max([wn.wup_similarity(syn2, i) for i in syn1])
    elif type(syn1) is not list and type(syn2) is list:
        score = max([wn.wup_similarity(syn1, i) for i in syn2])
    elif all(type(x) is list for x in (syn1, syn2)):
        score = max([wn.wup_similarity(i, j) for i in syn1 for j in syn2])
    else:
        score = wn.wup_similarity(syn1, syn2)

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

    documents2 = ("The sky is blue. #Outdoors",
                  "The dog is playing.",#"The sun is bright.",
                  "The sun in the sky is bright.",
                  "We can see the shining sun, the bright sun. #Outdoors")

    documents_3 = mt.preprocess_tweet(tweets_data)

    tfidf = TfidfVectorizer(tokenizer=mt.tokenize_tweet)
    tfidf_matrix = tfidf.fit_transform(documents2)

    print("Vocabulary:", tfidf.vocabulary_)
    features = [feat[0] for feat in sorted(
        tfidf.vocabulary_.items(), key=itemgetter(1))]
    print("Features:", features)

    print("Matrix shape:", tfidf_matrix.shape)
    print("TF-IDF:", tfidf_matrix.todense())
    print("Cosine Similarity of 1st and 1-n documents:\n",
            np.dstack(cosine_similarity(tfidf_matrix.getrow(2),
        tfidf_matrix)))

    print("Soft Cosine Similarity of 1st and 1-n documents:")
    for i in range(tfidf_matrix.shape[0]):
        print(soft_cosine_measure(tfidf_matrix.getrow(2), tfidf_matrix.getrow(i), features))
