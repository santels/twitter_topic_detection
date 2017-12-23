import numpy as np

"""
Scores clusters implementing (Manaskasemsak, 2016)'s paper:
    'Graph Clustering-Based Emerging Event Detection From Twitter
    Data Stream'
"""


def score(sim, cluster_mat, cluster_indices):
    """ Gets scores of clusters. """
    for cluster in iter(cluster_indices):
        r_deg = get_tweet_related_degree(sim, cluster_mat, cluster)
        e_size = get_event_size(cluster, cluster_indices)

        yield get_final_score(e_size, r_deg)


def get_tweet_related_degree(sim, cluster_mat, cluster):
    """ Gets tweet related degree of a cluster. """
    centroid = get_centroid_vector(cluster, cluster_mat)
    total = sum(sim(centroid, cluster_mat[i].reshape(1, centroid.shape[1]))
                for i in iter(cluster))
    return total[0, 0]


def get_centroid_vector(cluster, cluster_mat):
    """ Gets centroid vector of a cluster. """
    total_mat = np.zeros((1, cluster_mat.shape[1]))
    for i in iter(cluster):
        total_mat += cluster_mat[i]
    return total_mat / len(cluster)


def get_event_size(cluster, cluster_indices):
    """ Gets event size of a graph. """
    cl_graph_size = 0
    for cl in iter(cluster_indices):
        cl_graph_size += len(cl)

    return len(cluster) / cl_graph_size


def get_final_score(event_size, related_degree):
    """ Gets final score of a cluster using an F-measure-inspired formula."""
    return (2 * related_degree * event_size) / (related_degree + event_size)
