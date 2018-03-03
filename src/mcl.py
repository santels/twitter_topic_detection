import numpy as np
import sklearn.preprocessing


"""
Markov Clustering Algorithm (MCL Algorithm) Implementation.
Visit https://micans.org/mcl/index.html for more details about MCL.
This is an implementation of Stijn van Dongen's algorithm of the same name.
"""


def normalize(M):
    """
    Normailizes matrix to get transition matrix.
    """
    return sklearn.preprocessing.normalize(M, norm="l1", axis=0)


def expand(M, power):
    """
    Applies expansion process to the matrix with the given power.
    """
    return np.linalg.matrix_power(M, power)


def inflate(M, power):
    """
    Applies inflation process to the matrix with the given power.
    """
    return normalize(np.power(M, power))


def check_convergence(M1, M2):
    """
    Checks for convergence in the matrix. If M1 and M2 have
    approximately equal values.
    """
    return np.allclose(M1, M2)


def prune(M, threshold):
    """
    Prunes the matrix removing weak edges (edges lower than the pruning
    threshold specified.
    """
    pruned_mat = M.copy()
    pruned_mat[pruned_mat < threshold] = 0
    return pruned_mat


def draw(M, clusters, tweet_list, node_size=55, with_labels=True):
    """
    Draws and shows clusters created after clustering.
    """
    import networkx as nx
    import mplcursors
    import matplotlib.pyplot as plt
    from matplotlib.pylab import show, axis

    graph = nx.Graph(M)
    pos = nx.spring_layout(graph, k=0.2)
    plt.figure('Output Graphs')
    plt.title('Clustered Graphs')
    #cluster_map = {node: i for i, cluster in enumerate(clusters)
    #               for node in cluster}

    labels = [tweet_list[node] for node in graph.nodes()]

    nx.draw_networkx_nodes(graph, pos, node_color='red', node_size=node_size,
                           with_labels=with_labels)
    nx.draw_networkx_edges(graph, pos, alpha=0.8, edge_color="silver", width='2')

    def show_label(sel, label):
        index = sel.target.index
        if not isinstance(index, tuple):
            return sel.annotation.set_text(label[index])

    mplcursors.cursor(hover=True).connect(
        "add", lambda sel: show_label(sel, labels)
    )
    plt.show()
    axis("off")
    show(block=True)


def get_clusters(M):
    """
    Gets clusters generated by `cluster` function which performs MCL Algorithm.
    """
    # Gets the attractors in the clustered graph.
    attractor_list = iter(M.diagonal().nonzero()[0])

    cluster_set = set()

    # Puts graph vertices in cluster set.
    for attractor in attractor_list:
        cluster = tuple(M[attractor].nonzero()[0].tolist())
        cluster_set.add(cluster)

    return sorted(list(cluster_set)), M


def cluster(M, exp_power=2, inf_power=2, iter_count=10,
            pr_threshold=0.001):
    """
    Performs Markov Clustering Algorithm.
    Clusters matrix with the following steps:
        1. Normalizes matrix.
        2. While iteration count not reached or convergence not met:
            2.1. Expand matrix.
            2.2. Inflate matrix and normalize.
            2.3. Prunes matrix.
    """
    M = normalize(M)
    for i in range(iter_count):

        prev_mat = M.copy()  # Copies last matrix for convergence check.
        M = expand(M, exp_power)
        M = inflate(M, inf_power)

        if pr_threshold > 0:
            M = prune(M, pr_threshold)

        if check_convergence(M, prev_mat):
            break
    return M
