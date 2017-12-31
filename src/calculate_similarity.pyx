from __future__ import print_function

import re
import math
import sqlite3
import numpy as np
cimport numpy as np

from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer


conn = sqlite3.connect('.word_scores.db')
cur = conn.cursor()
THRESHOLD = 0.6

ctypedef np.double_t DOUBLE_t
ctypedef np.int_t INT_t


cdef class Similarity:
    """
    Document Similarity Measure class implementing Soft Cosine Measure and
    using WordNet's wup_similarity function for getting feature similarity
    score.
    """
    cdef np.ndarray matrix
    cdef list _features
    cdef dict _synsets

    def __cinit__(self, tokens):
        """
        Similarity class constructor.
        """
        self.initialize(tokens)
        self._synsets = {}

    def initialize(self, tokens):
        """
        Utility function to initialize and setup database connection and
        get TF-IDF values of documents and its features.
        """
        tfidf = TfidfVectorizer(tokenizer=lambda keys: tokens[keys])
        matrix_csr = tfidf.fit_transform(tokens.keys())

        self.matrix = matrix_csr.A
        self._features = tfidf.get_feature_names()
        conn.execute("DROP TABLE IF EXISTS tblWord")
        conn.execute("CREATE TABLE tblWord(wordPair UNIQUE, score DOUBLE)")

    def get_features(self):
        """
        Gets list of features generated by the tf-idf vectorizer.
        (This is created because of the cdef declaration which does not allow
        other Python modules to access C-type variables).
        """
        return self._features

    def similarity(self, M1=None, M2=None, is_scoring=False):
        """
        Calculates similarity measure of each document matrix. Uses soft cosine
        similarity measure to calculate document similarities.
        """
        if M1 is None:
            M1 = self.matrix
            if M2 is None:
                M2 = self.matrix

        cdef int M1_len = M1.shape[0]
        cdef int M2_len = M2.shape[0]

        # Get the sum of consecutive integers for the size of the array
        cdef np.ndarray[DOUBLE_t, ndim=2] doc_sim = np.zeros([M1_len, M2_len])

        for i in range(M1_len):
            for j in range(M2_len):
                if i == j:
                    doc_sim[i, j] = 1.0
                else:
                    doc_sim[i, j] = self._soft_cosine_similarity(M1[i],
                                                                 M2[j])
        return doc_sim

    def cos_similarity(self, M1=None, M2=None):
        '''
        Cosine similarity measure of documents. For testing purposes.
        '''
        from sklearn.metrics.pairwise import cosine_similarity
        if M1 is None:
            M1 = self.matrix
            if M2 is None:
                M2 = self.matrix
        return cosine_similarity(M1, M2)

    cdef double _multiply_elements(self ,np.ndarray[DOUBLE_t, ndim=1] v1,
            np.ndarray[DOUBLE_t, ndim=1] v2):
        """
        Multiplies values between vector elements and similarity function
        scores.
        """
        cdef double total_score = 0.0
        cdef np.ndarray[INT_t, ndim=1] v1nz = v1.nonzero()[0]
        cdef np.ndarray[INT_t, ndim=1] v2nz = v2.nonzero()[0]

        for i in v1nz:
            for j in v2nz:
                total_score += v1[i] * v2[j] * self._get_score(
                    self._features[i], self._features[j])
        return total_score

    cdef DOUBLE_t _soft_cosine_similarity(self, np.ndarray[DOUBLE_t, ndim=1] v1,
            np.ndarray[DOUBLE_t, ndim=1] v2):
        """
        Soft Cosine Similarity Measure
        ------------------------------
        Traditional Cosine Similarity Measure that takes into account the
        semantic similarities of each features in each documents.
        """
        cdef double product = self._multiply_elements(v1, v2)
        cdef double denom1 = math.sqrt(self._multiply_elements(v1, v1))
        cdef double denom2 = math.sqrt(self._multiply_elements(v2, v2))

        if denom1 == 0 or denom2 == 0:
            return 0

        return product / (denom1 * denom2)

    cdef double _get_score(self, str feature1, str feature2):
        """
        Gets and filters feature score and ignores score less than the
        specified threshold.
        """
        cdef double feature_score = 0
        # Same terms have 1.0 similarity.
        if feature1 == feature2:
            feature_score = 1
        else:
            feature_score = self._get_feature_score(feature1,
                    feature2)
            if feature_score <= THRESHOLD:
                feature_score = 0

            word_pair = ' '.join(sorted([feature1, feature2]))
            try:
                conn.execute('''
                    INSERT INTO tblWord(wordPair, score) VALUES (?, ?)
                    ''',
                    (word_pair, feature_score))
            except:
                pass

        return feature_score

    cdef tuple _get_synsets(self, str term1, str term2):
        """
        Gets best synsets of each term based on the highest path similarity
        among all pairs compared; if the synset's pos() is not a noun or verb,
        it gets its related nouns/forms.
        """
        synset_list1 = wn.synsets(term1)
        synset_list2 = wn.synsets(term2)
        cdef float max_score = -1.0

        if (len(synset_list1) == 0) or (len(synset_list2) == 0):
            return None, None

        cdef tuple best_pair = (synset_list1[0], synset_list2[0])
        return best_pair

    cdef double _get_feature_score(self, str term1, str term2):
        """
        If term1 and term2 are synsets, returns their similarity score. If they
        are lists, gets all similarity scores of each element and returns the
        best score.
        """
        cdef tuple sorted_terms
        cdef double score

        term1, term2 = tuple(sorted((term1, term2)))
        sorted_terms = (term1, term2)

        # Checks if synset pair has already been calculated.
        cur.execute("SELECT score FROM tblWord WHERE wordPair=?",
                (' '.join(sorted_terms),))
        _score = cur.fetchone()
        if _score:
            return _score[0]

        # If a term contains a hashtag, it automatically does not contain
        # synsets, thus, returning 0.
        if any("#" in term for term in sorted_terms):
            return 0.0

        # If a term has does not fully contains alpha characters, it has no
        # synsets.
        if any(re.search(r'^([a-zA-Z]+[-]?[a-zA-Z]+)$', term) is None
               for term in sorted_terms):
            return 0.0

        # If the synset of a term  has already been captured. Checks the cache
        # to get the synset of a term faster.
        syn1 = self._synsets.get(term1)
        syn2 = self._synsets.get(term2)

        if all(syn is None for syn in (syn1, syn2)):
            syn1, syn2 = self._get_synsets(term1, term2)

        # Checks if one/both synset/s is/are not found in WordNet. If it's not
        # found, its value is None, otherwise, caches the Synset object.
        if syn1 is None or syn2 is None:
            if syn1 is not None:
                self._synsets[term1] = syn1

            if syn2 is not None:
                self._synsets[term2] = syn2
            return 0.0

        _score = wn.wup_similarity(syn1, syn2)

        if _score is None:
            score = 0.0
        else:
            score = _score
        return score
