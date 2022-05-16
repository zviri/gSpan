import random
import sys
import networkx as nx

if __name__ == '__main__':
    num_nodes = int(sys.argv[1])
    num_edge_attachments = int(sys.argv[2])

    g = nx.random_graphs.barabasi_albert_graph(num_nodes, num_edge_attachments)
    for node in g.nodes:
        g.nodes[node]["label"] = 1
    num_edges = len(g.edges)
    for edge in g.edges:
        g.edges[edge]["label"] = random.randint(1, num_edges / 2)
    print(f"Num edges: {num_edges}")
    from gspan_mining.is_isomorphic import print_graph
    print_graph(g, "", 1)