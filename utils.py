import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def get_sample_graph(name):
    if name == "Linear Graph":
        return {"A":["B"],"B":["C"],"C":["D"],"D":["E"],"E":["F"],"F":["G"],"G":[]}
    if name == "Binary Tree":
        return {"A":["B","C"],"B":["D","E"],"C":["F","G"],"D":[],"E":[],"F":[],"G":[]}
    if name == "Tree with Uneven Depths":
        return {"A":["B","C","D"],"B":[],"C":[],"D":["E"],"E":["F"],"F":["G"],"G":[]}
    if name == "Directed Graph":
        return {"A":["B","C"],"B":["D"],"C":["E"],"D":["F"],"E":["G"],"F":[],"G":[]}
    if name == "Cyclic Graph":
        return {
            "A":["B","F"],
            "B":["C"],
            "C":["D","G"],
            "D":["E"],
            "E":["F"],
            "F":[],
            "G":[]
        }
    return {}


def visualize_graph_steps(graph, visited_nodes):
    G = nx.DiGraph()
    for n, nbrs in graph.items():
        G.add_node(n)
        for m in nbrs:
            G.add_edge(n, m)
    def compute_positions(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
        pos = {}
        def dfs_pos(node, left, right, y, visited):
            visited.add(node)
            pos[node] = ((left+right)/2, y)
            children = [c for c in G.successors(node) if c not in visited]
            if not children:
                return
            dx = (right-left)/len(children)
            x = left
            for c in children:
                dfs_pos(c, x, x+dx, y-vert_gap, visited)
                x += dx
        dfs_pos(root, 0, width, vert_loc, set())
        return pos
    try:
        root = next(nx.topological_sort(G))
    except nx.NetworkXUnfeasible:
        root = next(iter(G.nodes()), None)
    if root is None:
        st.error("Graph empty or invalid.")
        return
    pos = compute_positions(G, root)
    color_map = ["#4CAF50" if n in visited_nodes else "#E0E0E0" for n in G.nodes()]
    fig, ax = plt.subplots(figsize=(6,4))
    nx.draw(G, pos, with_labels=True, node_color=color_map,
            node_size=800, font_weight='bold', arrowsize=12)
    st.pyplot(fig)