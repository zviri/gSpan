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
                _, from_id, to_id, label = line.strip().split(" ")
                g.add_edge(from_id, to_id, label=label)
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
    expected, found = sys.argv[1:3]
    expected_graphs = load_graphs(expected)
    found_graphs = load_graphs(found)
    print(f"Num expected graphs: {len(expected_graphs)}")
    print(f"Num found graphs: {len(found_graphs)}")
    retry = True
    while retry:
        retry = False
        for expected_i, (expected_g, expected_support) in enumerate(expected_graphs):
            for found_i, (found_g, found_support) in enumerate(found_graphs):
                if nx.is_isomorphic(
                    expected_g, found_g, node_match=node_match, edge_match=edge_match
                ) and expected_support == found_support:
                    expected_graphs.pop(expected_i)
                    found_graphs.pop(found_i)
                    retry = True
                    break
            if retry:
                break

    print(f"Expected graphs that were not found ({len(expected_graphs)})")
    for i, (expected_g, expected_support) in enumerate(expected_graphs, start=1):
        print_graph(expected_g, expected_support, i)
        print("============")
    print(f"Found graphs that were not expected ({len(found_graphs)})")
    for i, (found_g, found_support) in enumerate(found_graphs, start=1):
        print_graph(found_g, found_support, i)
        print("============")

