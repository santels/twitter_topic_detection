from collections import defaultdict
import numpy as np


class Graph:
    """
    Custom graph class implementation.
    """
    def __init__(self, matrix=None, gtype='matrix'):
        if matrix is not None:
            self.graph = self.create_graph(matrix, gtype)

    def create_graph(self, matrix, gtype='matrix'):
        """
        Creates an undirected weighted graph. Uses the similarity scores of
        each document as weights of the edges and the documents as vertices.
        gtype can be:
            'matrix' - returns a numpy matrix containing graph information.
            'dict'   - returns a dictionary containing graph information.
        """
        if gtype == 'matrix':
            return self._create_matrix_graph(matrix)
        elif gtype == 'dict':
            return self._create_dict_graph(matrix)
        else:
            print("[ERROR] Type '{}' not found.".format(gtype))

        return None

    def _create_matrix_graph(self, matrix):
        """
        Creates an NxN matrix of undirected weighted graph. Values of each
        element are the weights.
        """
        return matrix


    def _create_dict_graph(self, matrix):
        """
        Creates an dictionary of undirected weighted graph. The keys contain
        the vertices and the values contain 2-tuple with the vertices they're
        connecting to and its weights.
        """
        graph = defaultdict(list)
        for row_i in range(len(matrix)):
            for col_i in range(len(matrix[0])):
                if matrix[row_i, col_i] not in (0, 1):
                    graph[row_i].append( (col_i, matrix[row_i, col_i]) )
                    graph[col_i].append( (row_i, matrix[row_i, col_i]) )

        return graph
