import re
import math
import time
import numpy as np

from nltk.corpus import wordnet as wn
from scipy.sparse import csc_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


THRESHOLD = 0.5


class Similarity:
    """
    Document Similarity Measure class implementing Soft Cosine Measure and
    using WordNet's wup_similarity function for getting feature similarity
    score.
    """
    def __init__(self, tokens):
        """
        Similarity class constructor.
        """
        self.tfidf = TfidfVectorizer(tokenizer=lambda keys: tokens[keys])
        self.matrix = self.tfidf.fit_transform(tokens.keys())
        self._features = self.tfidf.get_feature_names()
        self._synset_pairs = {}
        self._synsets = {}
        self.start = time.time()

    def similarity(self, M1=None, M2=None, is_scoring=False):
        """
        Calculates similarity measure of each document matrix. Uses soft cosine
        similarity measure to calculate document similarities.
        """
        print("Start:", time.strftime("%H:%M:%S", time.gmtime(self.start)))
        if M1 is None:
            M1 = self.matrix
            if M2 is None:
                M2 = self.matrix

        if is_scoring:
            M1 = csc_matrix(M1)
            M2 = csc_matrix(M2)
            M1_len = M1.shape[1]
            M2_len = M2.shape[1]
            M1_get_vect = M1.getcol
            M2_get_vect = M2.getcol
        else:
            M1_len = M1.shape[0]
            M2_len = M2.shape[0]
            M1_get_vect = M1.getrow
            M2_get_vect = M2.getrow

        # Get the sum of consecutive integers for the size of the array
        doc_pairs = {}
        doc_sim = np.zeros([M1_len, M2_len])
        soft_cosine_similarity = self._soft_cosine_similarity
        print("Shape:", M1_len, M2_len)
        for i in range(M1_len):
            for j in range(M2_len):
                print(i, j)
                sorted_indices = tuple(sorted((i, j)))
                if sorted_indices in doc_pairs:
                    doc_sim[i, j] = doc_pairs[sorted_indices]
                else:
                    if i == j:
                        doc_sim[i, j] = 1
                    else:
                        doc_sim[i, j] = soft_cosine_similarity(M1_get_vect(i),
                                                               M2_get_vect(j))
                        doc_pairs[sorted_indices] = doc_sim[i, j]
                print("Elapsed:", time.strftime("%H:%M:%S", time.gmtime(time.time() - self.start)))
        return doc_sim

    def cos_similarity(self, M1=None, M2=None):
        '''
        Cosine similarity measure of documents. For testing purposes.
        '''

        if M1 is None:
            M1 = self.matrix
            if M2 is None:
                M2 = self.matrix
        return cosine_similarity(M1, M2)

    def _multiply_elements(self, v1, v2):
        """
        Multiplies values between vector elements and similarity function
        scores.
        """
        total_score = 0
        features = self._features
        get_score = self._get_score
        total_score = np.sum((v1[i] * v2[j] * get_score(features[i],
                             features[j]) for i in range(v1.shape[0])
                             for j in range(v1.shape[0])))
        return total_score

    def _soft_cosine_similarity(self, v1, v2):
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

    def _get_score(self, feature1, feature2):
        """
        Filters feature score and ignores score less than the specified
        threshold.
        """
        feature_score = 0
        # Same terms have 1.0 similarity.
        if feature1 == feature2:
            feature_score = 1
        else:
            feature_score = self._get_feature_score(feature1, feature2)
            if feature_score <= THRESHOLD:
                feature_score = 0
        return feature_score

    def _get_synsets(self, term1, term2):
        """
        Gets best synsets of each term based on the highest path similarity
        among all pairs compared; if the synset's pos() is not a noun or verb,
        it gets its related nouns/forms.
        """
        synset_list1 = wn.synsets(term1)
        synset_list2 = wn.synsets(term2)
        max_score = -1.0

        if (len(synset_list1) == 0) or (len(synset_list2) == 0):
            return None, None
        else:
            best_pair = [None, None]
            for i in iter(synset_list1):
                i_shortest_path_distance = i.shortest_path_distance
                for j in iter(synset_list2):
                    score = 1.0 / (i_shortest_path_distance(j, True) + 1)
                    if score is not None and score > max_score:
                        max_score = score
                        best_pair = [i, j]

            if (best_pair[0] is not None) and \
                    (best_pair[0].pos() not in ('n', 'v')):
                best_pair[0] = self._get_related_nouns(best_pair[0])

            if (best_pair[1] is not None) and \
                    (best_pair[1].pos() not in ('n', 'v')):
                best_pair[1] = self._get_related_nouns(best_pair[1])

            return tuple(best_pair)

    def _get_related_nouns(self, synset):
        """
        Gets derivationally related word forms as noun synsets of a given
        synset to measure its similarity to other terms.
        """
        related = None
        lemmas = synset.lemmas()
        if len(lemmas) > 0:
            derived = lemmas[0].derivationally_related_forms()
            if len(derived) > 0:
                related = derived[0].synset()
        return related

    def _get_feature_score(self, term1, term2):
        """
        If syn1 and syn2 are synsets, returns their similarity score. If they
        are lists, gets all similarity scores of each element and returns the
        best score.
        """
        sorted_terms = tuple(sorted((term1, term2)))

        # Checks if synset pair had already been calculated.
        if sorted_terms in self._synset_pairs:
            return self._synset_pairs[tuple(sorted((term1, term2)))]

        # If a term contains a hashtag, it automatically does not contain
        # synsets, thus, returning 0.
        if any("#" in term for term in (term1, term2)):
            return 0

        # If a term has does not fully contains alpha characters, it has no
        # synsets.
        if any(re.search(r'^([a-zA-Z]+[-]?[a-zA-Z]+)$', term) is None
               for term in (term1, term2)):
            return 0

        # If the synset has already been captured. Checks the cache to get the
        # synset of a term faster.
        syn1 = self._synsets.get(term1)
        syn2 = self._synsets.get(term2)

        if all(syn is None for syn in (syn1, syn2)):
            syn1, syn2 = self._get_synsets(term1, term2)

        # If one/both synset/s is/are not found in WordNet. If it's not found,
        # its value is None, otherwise, a Synset object.
        if syn1 is None or syn2 is None:
            if syn1 is not None:
                self._synsets[term1] = syn1

            if syn2 is not None:
                self._synsets[term2] = syn2
            return 0

        score = wn.wup_similarity(syn1, syn2)

        if score is None:
            score = 0

        self._synset_pairs[sorted_terms] = score
        return score


if __name__ == '__main__':
    tweets_data_path = "data/tweets_data.txt"
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
