import networkx as nx
import matplotlib.pyplot as plt


def create_graph(d):
    G = nx.MultiDiGraph()
    for link, links in d.items():
        for link__ in links:
            for link1, links1 in link__.items():
                G.add_edge(link, link1)
                for link2__ in links1:
                    for link3, links3 in link2__.items():
                        G.add_edge(link1, link3)
                        for link___ in links3:
                            G.add_edge(link3, link___)

    plt.figure(figsize=(30, 30))
    options = {
        'node_color': 'blue',
        'node_size': 10,
        'edge_color': 'red',
        'width': 0.09
    }

    nx.write_gml(G, 'graph.gml')

    nx.draw_random(G, with_labels=False, **options)
    plt.savefig('graph.png')
