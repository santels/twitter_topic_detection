cimport numpy as np

cdef object conn
cdef object cur

ctypedef np.double_t DOUBLE_t
ctypedef np.int_t INT_t


cdef class Similarity:
    cdef readonly DOUBLE_t THRESHOLD
    cdef np.ndarray matrix
    cdef list _features

    cdef np.ndarray[DOUBLE_t, ndim=2] _similarity(self,
            np.ndarray[DOUBLE_t, ndim=2] M1, np.ndarray[DOUBLE_t, ndim=2] M2)

    cdef DOUBLE_t _multiply_elements(self ,np.ndarray[DOUBLE_t, ndim=1] v1,
            np.ndarray[DOUBLE_t, ndim=1] v2)

    cdef DOUBLE_t _soft_cosine_similarity(self, np.ndarray[DOUBLE_t, ndim=1] v1,
            np.ndarray[DOUBLE_t, ndim=1] v2)

    cdef DOUBLE_t _get_score(self, str feature1, str feature2)
    cdef tuple _get_synsets(self, str term1, str term2)
    cdef DOUBLE_t _get_feature_score(self, str term1, str term2)
