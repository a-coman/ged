# GED (Graph Edit Distance)

This is a Graph Edit Distance calculation script for [llm-instancer](https://github.com/a-coman/llm-instancer/) and [llm-evaluator](https://github.com/a-coman/llm-evaluator/) projects using [NetworkX](https://networkx.org/) in order to evaluate the structural similarity between different object diagrams represented as graphs.

## What is Graph Edit Distance (GED)?
The [Graph Edit Distance (GED)](https://en.wikipedia.org/wiki/Graph_edit_distance) is a measure of similarity between two graphs. It is defined as the minimum number of edit operations required to transform one graph into another. The edit operations can include:
- Node insertion / deletion.
- Edge insertion / deletion.

View [NetworkX's implementation](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.similarity.graph_edit_distance.html).

In our case:
- The nodes represent classes in an object diagram.
- The edges represent relationships between these classes - note that if a relationship is double between two nodes, it's also taken into account, as we are using a weighted adjacency matrix.

Additionally we also consider as edit operations:
- Node labels (The class names, e.g., Bank, Account, Person...) which count as node substitutions if they differ.
- [ ] **TO BE IMPLEMENTED** - Edge labels (The relationship names, e.g., user-owner, manager-employee...) which count as edge substitutions if they differ - note that edge labels are bidirectional, so a relationship "manager-employee" from A to B is considered the same as "employee-manager" from B to A.

**Normalization:**
To provide a more interpretable similarity score, we normalize the GED to a [0,1] range using the formula: `similarity = 1 - (ged / (0.5 * (ged_to_empty_A + ged_to_empty_B)))`
Where `ged_to_empty_A` and `ged_to_empty_B` are the GED values of each graph to an empty graph. This normalization ensures that:
- A similarity of 1 indicates identical graphs (GED = 0).
- A similarity of 0 indicates completely dissimilar graphs (maximum GED).

## How to run
This project uses [Astral UV](https://docs.astral.sh/uv/) to manage dependencies and run the script. After [installing UV](https://docs.astral.sh/uv/getting-started/installation/), you can run the script with the following command:
```bash
uv run main.py
```
**Note:** 
UV automatically downloads the necessary python version, creates the corresponding virtual environment, and installs the dependencies specified in `pyproject.toml`.
