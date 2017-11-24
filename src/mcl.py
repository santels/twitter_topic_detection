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
    return normalize(np.power(matrix, power))

def check_convergence(matrix1, matrix2):
    """
    Checks for convergence in the matrix. If matrix1 and matrix2 have
    approximately equal values.
    """
    return np.allclose(matrix1, matrix2)

def prune(matrix, threshold):
    """
    Prunes the matrix removing weak edges (edges lower than the pruning 
    threshold specified.
    """
    pruned_mat = matrix.copy()
    pruned_mat[pruned_mat < threshold] = 0
    return pruned_mat

def get_clusters(matrix):
    """
    Gets clusters generated by `cluster` function which performs MCL Algorithm.
    """
    # Gets the attractors in the clustered graph.
    attractor_list = matrix.diagonal().nonzero()[0]

    cluster_set = set()

    # Puts graph vertices in cluster set.
    for attractor in attractor_list:
        cluster = tuple(matrix[attractor].nonzero()[0].tolist())
        cluster_set.add(cluster)

    return sorted(list(cluster_set))

def cluster(matrix, exp_power=2, inf_power=2, iter_count=10,
            pr_threshold=0.0001):
    """
    Performs Markov Clustering Algorithm.
    Clusters matrix with the following steps:
        1. Normalizes matrix.
        2. While iteration count not reached or convergence not met:
            2.1. Expand matrix.
            2.2. Inflate matrix and normalize.
            2.3. Prunes matrix.
    """
    matrix = normalize(matrix)
    for i in range(iter_count):
        print("Iteration {}".format(i))

        prev_mat = matrix.copy() # Copies last matrix for convergence check.
        matrix = expand(matrix, exp_power)
        matrix = inflate(matrix, inf_power)

        if pr_threshold > 0:
            matrix = prune(matrix, pr_threshold)

        if check_convergence(matrix, prev_mat):
            print("Convergence found. Stopping loop...")
            break

    return matrix
