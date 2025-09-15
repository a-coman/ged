import os
from utils import read_file, save_file, array_to_markdown_table
from soil_to_graph import soil_to_graph
import networkx as nx

def adj_labels_to_nx(adj : list[list[float]], labels: list[str]):
    G: nx.Graph = nx.Graph()
    n = len(adj)
    for i in range(n):
        G.add_node(i, label=labels[i])
    for i in range(n):
        for j in range(i+1, n):
            if adj[i][j]:
                G.add_edge(i, j)
    return G

def main():
    llm = "GPT_4O"
    type = "Simple"
    system = "bank"
    time = "21-03-2025--15-41-00"
    filepath = "/home/aac/Repos/llm-instancer/src/main/resources/instances/" + type + "/" + system + "/" + llm + "/" + time + "/"
    #filepath = "./instances/"
    numberOfGen = len([item for item in os.listdir(filepath) if os.path.isdir(os.path.join(filepath, item)) and item.startswith("gen")])
    nx_graphs = []

    result = []
    result.append("# Adj, edge, label \n```\n")
    processedItems = []

    for i in range(1, numberOfGen + 1):
        items = os.listdir(filepath + "gen" + str(i))
        for item in items:
            if not item.endswith(".soil"):
                continue
            if type == "CoT" and (item.startswith("output") or item.startswith("temp")):
                continue
            processedItems.append(item)
            print("Processing file " + item + " of gen" + str(i))
            file = read_file(filepath + "gen" + str(i) + "/" + item)
            adj, labels, edges = soil_to_graph(file)
            
            result.append("Adj" + str(i) + "-" + item + ": ")
            result.append(str(adj))
            result.append("\n\n")
            result.append("Labels" + str(i) + "-" + item + ": ")
            result.append(str(labels))
            result.append("\n\n")
            result.append("Edges" + str(i) + "-" + item + ": ")
            result.append(str(edges))
            result.append("\n\n")

            nx_graphs.append(adj_labels_to_nx(adj, labels))

    # After collecting all nx_graphs:
    ged_matrix = [[0.0 for _ in range(len(nx_graphs))] for _ in range(len(nx_graphs))]
    for i in range(len(nx_graphs)):
        for j in range(i, len(nx_graphs)):
            if i == j:
                ged = 0.0
            else:
                print(f"Calculating GED between graph {i} and graph {j}, computed so far: {ged_matrix[i][j]}, total graphs: {len(nx_graphs)}")
                ged = nx.graph_edit_distance(nx_graphs[i], nx_graphs[j], node_match=lambda n1, n2: n1['label'] == n2['label'])
            ged_matrix[i][j] = ged
            ged_matrix[j][i] = ged  # symmetric

    # Add to markdown output:
    result.append("```\n")
    result.append("# GED Matrix: \n```\n")
    result.append(str(ged_matrix))
    result.append("\n```\n")
    result.append("# GED 2D table: \n")
    markdown_ged = array_to_markdown_table(ged_matrix, processedItems)
    result.append(markdown_ged)

    result = "".join(result)
    save_file(result, filepath + "ged.md")
    print(result)
    print("\n")
    print(filepath)

if __name__ == "__main__":
    main()
