import math
import numpy as np

"""
Markov Clustering Algorithm (MCL Algorithm) Implementation.
Visit https://micans.org/mcl/index.html for more details about MCL.
This is an implementation of Stijn van Dongen's algorithm of the same name.
"""

def normalize(matrix):
    """
    Normailizes matrix to get transition matrix.
    """
    return matrix/np.sum(matrix, axis=0)

def expand(matrix, power):
    """
    Applies expansion process to the matrix with the given power.
    """
    return np.linalg.matrix_power(matrix, power)

def inflate(matrix, power):
    """
    Applies inflation process to the matrix with the given power.
    """
    for elem in np.nditer(matrix, op_flags=['readwrite']):
        elem[...] = math.pow(elem, power)
    return matrix

def check_state(matrix):
    """
    Checks if the matrix is at steady state.
    """
    def check_column(column):
        val = 0
        for i in nditer(column):
            if i != 0:
                val = i
                break

        for i in nditer(column):
            if i != 0 and i != val:
                return False
        return True

    return all(check_column(matrix[:, i]) for i in matrix)


def cluster(matrix, exp_power=2, inf_power=2, iter_count=10):
    """
    Clusters matrix with the following steps:
        1. Normalizes matrix.
        2. While iteration count not reached:
            2.1. Expand matrix.
            2.2. Inflate matrix.
            2.3. Normalize matrix.
    """
    matrix = normalize(matrix)
    for _ in range(iter_count):

        if check_state(matrix):
            break

        matrix = expand(matrix, exp_power)
        matrix = inflate(matrix, inf_power)
        matrix = normalize(matrix)
    return matrix
