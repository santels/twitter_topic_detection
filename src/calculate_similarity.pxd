cimport numpy as np

cdef object conn
cdef object cur

ctypedef np.double_t DOUBLE_t

cdef DOUBLE_t THRESHOLD


cdef class Similarity:
    cdef:
        object tfidf
        np.ndarray matrix
        list _features

        np.ndarray[DOUBLE_t, ndim=2] _similarity(self, np.ndarray[DOUBLE_t, ndim=2] M1, np.ndarray[DOUBLE_t, ndim=2] M2, int is_scoring)
        DOUBLE_t _multiply_elements(self, np.ndarray[DOUBLE_t, ndim=1] v1, np.ndarray[DOUBLE_t, ndim=1] v2)
        DOUBLE_t _soft_cosine_similarity(self, np.ndarray[DOUBLE_t, ndim=1] v1, np.ndarray[DOUBLE_t, ndim=1] v2)
        DOUBLE_t _get_score(self, str feature1, str feature2)
        tuple _get_synsets(self, str term1, str term2)
        DOUBLE_t _get_feature_score(self, str term1, str term2)
