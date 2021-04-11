import networkx as nx
import numpy as np

np.seterr(divide='ignore', invalid='ignore')


def matrix_from_graph():
    G = nx.read_gml('graph.gml')

    A = nx.adjacency_matrix(G)

    B = (A / A.sum(axis=0))
    B = np.nan_to_num(B)

    G_LIST = G.nodes()

    B.tofile('matrix.out', sep=' ')

    height, width = B.shape

    return B, height, G_LIST