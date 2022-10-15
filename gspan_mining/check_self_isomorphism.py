import sys
import networkx as nx


def load_graphs(path):
    graphs = []
    with open(path) as ifile:
        g = None
        support = None
        for line in ifile:
            if line == "":
                break
            if line.startswith("t"):
                if g is not None:
                    graphs.append((g, support))
                _, _, _, support = line.strip().split(" ")
                g = nx.Graph()
            elif line.startswith("v"):
                _, node_id, node_label = line.strip().split(" ")
                g.add_node(node_id, label=node_label)
            elif line.startswith("e"):
                _, from_id, to_id, time_label, other_label = line.strip().split(" ")
                g.add_edge(from_id, to_id, label=(time_label, other_label))
        if g is not None:
            graphs.append((g, support))
    return graphs


def print_graph(graph, support, num):
    print(f"t {num} {support}")
    for node in graph.nodes:
        print(f"v {node} {graph.nodes[node]['label']}")        
    for edge in graph.edges:
        print(f"e {edge[0]} {edge[1]} {graph.edges[edge]['label']}")        


def node_match(n1, n2):
    return n1["label"] == n2["label"]


def edge_match(e1, e2):
    return e1["label"] == e2["label"]


if __name__ == "__main__":
    found = sys.argv[1]
    found_graphs = load_graphs(found)
    print(f"Num found graphs: {len(found_graphs)}")
    duplicit_graphs = []
    retry = False
    for i, (found_g_1, found_support_1) in enumerate(found_graphs):
        for found_g_2, found_support_2 in found_graphs[i+1:]:
            if nx.is_isomorphic(
                found_g_1, found_g_1, node_match=node_match, edge_match=edge_match
            ):
                duplicit_graphs.append(found_g_1)
   

    print(f"Found {len(duplicit_graphs)} duplicit graphs!")
    for i, (duplicit_g, g_support) in enumerate(duplicit_graphs, start=1):
        print_graph(duplicit_g, g_support, i)
        print("============")

