from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import wordnet as wn
from collections import defaultdict

import math
import numpy as np


THRESHOLD = 0.4


class Similarity:
    """
    Document Similarity Measure class implementing Soft Cosine Measure and
    using WordNet's wup_similarity function for getting feature similarity
    score.
    """
    def __init__(self, document, manip_tweet):
        """
        Similarity class constructor.
        `document` - list of documents to be analyzed.
        `manip_tweet` - class object instance of manipulate tweet module.
        """
        self.tfidf = TfidfVectorizer(tokenizer=manip_tweet.tokenize)
        self.matrix = self.tfidf.fit_transform(document)
        self._features = self.tfidf.get_feature_names()
        self._synset_pairs = defaultdict(float)

    def similarity(self):
        """
        Calculates similarity measure of each document matrix. Uses soft cosine
        similarity measure to calculate document similarities.
        """
        # Get the sum of consecutive integers for the size of the array
        doc_sim = np.zeros([self.matrix.shape[0] - 1, self.matrix.shape[0] - 1])
        for i in range(self.matrix.shape[0] - 1):
            for j in range(i + 1, self.matrix.shape[0]):
                doc_sim[i, j - 1] = self._soft_cosine_measure(
                        self.matrix.getrow(i), self.matrix.getrow(j))
        return doc_sim

    def _multiply_elements(self, v1, v2):
        """
        Multiplies values between vector elements and similarity function scores.
        """
        sum = 0
        for i in range(v1.shape[0]):
            for j in range(v1.shape[0]):

                feature_score = self._get_feature_score(self._features[i],
                    self._features[j])

                if feature_score <= THRESHOLD:
                    feature_score = 0

                sum += v1[i] * v2[j] * feature_score
        return sum

    def _soft_cosine_measure(self, v1, v2):
        """
        Soft Cosine Similarity Measure
        ------------------------------
        Traditional Cosine Similarity Measure that takes into account the
        semantic similarities of each features in each documents.
        """
        v1 = v1.toarray()[0]
        v2 = v2.toarray()[0]
        product = self._multiply_elements(v1, v2)
        denom1 = math.sqrt(self._multiply_elements(v1, v1))
        denom2 = math.sqrt(self._multiply_elements(v2, v2))
        return product / (denom1 * denom2)

    def _get_synsets(self, term1, term2):
        """
        Gets best synsets of each term based on the highest path similarity
        among all pairs compared; if the synset's pos() is not at noun or verb,
        it gets its related nouns/forms.
        <reference github repo>
        """
        # Checks whether the term pairs have already been calculated.
        if self._synset_pairs:
            for syn_pair in self._synset_pairs.keys().__iter__():
                if tuple( sorted((term1, term2)) ) == syn_pair:
                    return syn_pair

        synset_list1 = wn.synsets(term1)
        synset_list2 = wn.synsets(term2)
        max_score = -1.0

        if (len(synset_list1) == 0) or (len(synset_list2) == 0):
            return None, None
        else:
           # best_pair = [synset_list1[0], synset_list2[0]]
            best_pair = [None, None]
            for i in synset_list1.__iter__():
                for j in synset_list2.__iter__():
                    score = 1.0 / (i.shortest_path_distance(j, True) + 1)
                    if score is not None and score > max_score:
                        score = max_score
                        best_pair = [i, j]


            if (best_pair[0] is not None) and \
                    (best_pair[0].pos() not in ('n', 'v')):
                best_pair[0] = self._get_related_nouns(best_pair[0])

                if best_pair[0] is not None:
                    best_pair[0] = best_pair[0][0]

            if (best_pair[1] is not None) and \
                    (best_pair[1].pos() not in ('n', 'v')):
                best_pair[1] = self._get_related_nouns(best_pair[1])

                if best_pair[1] is not None:
                    best_pair[1] = best_pair[1][0]

            return tuple(best_pair)


    def _get_related_nouns(self, synset):
        """
        Gets derivationally related word forms as noun synsets of a given synset
        to measure its similarity to other terms.
        """
        related = [rel.synset() for lemma in synset.lemmas().__iter__()
                                for rel in lemma.derivationally_related_forms().__iter__()
                                if rel.synset().pos() == 'n']
        return None if related == [] else related


    def _get_feature_score(self, term1, term2):
        """
        If syn1 and syn2 are synsets, returns their similarity score. If they are
        lists, gets all similarity scores of each element and returns the best
        score.
        """

        # Same terms has 1.0 similarity.
        if term1 == term2:
            return 1

        syn1, syn2 = self._get_synsets(term1, term2)

        # If one/both synset/s is/are not found in WordNet. If it's not found, its
        # value is None, otherwise, a Synset object.
        if all((syn1, syn2)) == False:
            return 0

        # Checks if synset pair had already been calculated.
        if tuple( sorted((term1, term2)) ) in self._synset_pairs:
            return self._synset_pairs[tuple( sorted((term1, term2)) )]

        score = wn.wup_similarity(syn1, syn2)

        if score is None:
            score = 0
        else:
            print(term1, term2, score)
            self._synset_pairs[tuple( sorted((term1, term2)) )] = score
        return score


if __name__ == '__main__':
    tweets_data_path = "data/tweets_data.txt"
    #tweets_data = mt.load_tweets_data(tweets_data_path)
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

    #documents_3 = mt.preprocess_tweet(tweets_data[:5])

    sim = Similarity(documents_3)

    print("Vocabulary:", sim.tfidf.vocabulary_)
    print("Features:", sim._features)

    print("Matrix shape:", sim.tfidf_matrix.shape)
    print("TF-IDF:", sim.tfidf_matrix.todense())

    #print("Soft Cosine Similarity of 1-n and 1-n documents:")
    #print(similarity(tfidf_matrix, features))
