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
        matrix = expand(matrix, exp_power)
        matrix = inflate(matrix, inf_power)
        matrix = normalize(matrix)
    return matrix
