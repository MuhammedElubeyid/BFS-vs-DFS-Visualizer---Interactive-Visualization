# app.py

import streamlit as st
import pandas as pd
from algorithm import bfs, dfs
from utils import get_sample_graph, visualize_graph_steps
import time

# ----------------------------------------
# Page configuration
# ----------------------------------------
st.set_page_config(page_title="BFS vs DFS Visualizer", layout="centered")

# ----------------------------------------
# Main title
# ----------------------------------------
st.title("🔁 BFS vs DFS Visualization")

# ----------------------------------------
# Sidebar: user settings
# ----------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    graph_type = st.selectbox(
        "Select Graph Type",
        [
            "Linear Graph",
            "Binary Tree",
            "Tree with Uneven Depths",
            "Directed Graph",
            "Cyclic Graph"
        ]
    )
    graph = get_sample_graph(graph_type)

    start_node = st.selectbox("Start Node", sorted(graph.keys()))

    algo = st.radio(
        "Traversal Algorithm",
        ["Breadth-First Search (BFS)", "Depth-First Search (DFS)"]
    )

    delay = st.slider(
        "Step Delay (seconds):", 
        min_value=0.0, max_value=1.0, value=0.2, step=0.1
    )

    run = st.button("🚀 Run Traversal")

# ----------------------------------------
# Helper function to build textual explanations per step
# ----------------------------------------
def build_textual_steps(steps_list):
    """
    Given a list of 'visited' lists after each visit,
    return a list of strings like:
    'Step 1: Visited node X. Visited so far: [...]'
    """
    explanations = []
    previous_set = set()
    for i, visited in enumerate(steps_list, start=1):
        current_set = set(visited)
        # The newly visited node is the one in current_set but not in previous_set
        new_nodes = list(current_set - previous_set)
        if new_nodes:
            new_node = new_nodes[0]
        else:
            new_node = "?"
        explanations.append(
            f"Step {i}: Visited node **{new_node}**. Visited so far: {visited}"
        )
        previous_set = current_set
    return explanations

# ----------------------------------------
# When the user clicks “Run Traversal”
# ----------------------------------------
if run:
    st.info(f"Running **{algo}** from node **{start_node}**.")

    # 1. Run the chosen algorithm and measure only the algorithm time
    algo_start = time.perf_counter()
    steps = bfs(graph, start_node) if "BFS" in algo else dfs(graph, start_node)
    algo_end = time.perf_counter()

    # 2. Show step-by-step **visualization**
    placeholder = st.empty()
    for step in steps:
        with placeholder:
            visualize_graph_steps(graph, step)
        time.sleep(delay)

    # 3. Display completion message and number of steps
    st.success("Traversal complete.")
    st.write(f"Number of steps: **{len(steps)}**")

    # 4. Compute and display algorithm runtime in milliseconds
    algo_time_ms = (algo_end - algo_start) * 1000
    st.write("---")
    st.write(f"⏱️ **Algorithm run time ({algo}):** {algo_time_ms:.3f} ms")

    # ===================================================
    # “Step-By-Step Explanation” section
    # ===================================================
    st.markdown("---")
    st.header("📝 Step-By-Step Explanation")

    # Build a list of markdown strings describing each step
    textual_steps = build_textual_steps(steps)
    with st.expander("Show textual explanation of each step"):
        for line in textual_steps:
            st.markdown(line)

    # ===================================================
    # “Test Cases Demonstration” section
    # ===================================================
    st.markdown("---")
    st.header("🧪 Test Cases Demonstration")

    # 1) Define a variety of test graphs and expected outputs
    #    Each entry has: description, graph dict, start node, algorithm, expected visited order.
    test_cases = [
        {
            "description": "Empty graph",
            "graph": {},
            "start": "A",
            "algorithm": "BFS",
            "expected": []
        },
        {
            "description": "Single-node graph",
            "graph": {"A": []},
            "start": "A",
            "algorithm": "BFS",
            "expected": ["A"]
        },
        {
            "description": "Simple linear graph",
            "graph": {"A": ["B"], "B": ["C"], "C": []},
            "start": "A",
            "algorithm": "BFS",
            "expected": ["A", "B", "C"]
        },
        {
            "description": "Simple linear graph",
            "graph": {"A": ["B"], "B": ["C"], "C": []},
            "start": "A",
            "algorithm": "DFS",
            "expected": ["A", "B", "C"]
        },
        {
            "description": "Binary tree structure",
            "graph": {
                "A": ["B", "C"], 
                "B": ["D", "E"], 
                "C": ["F", "G"], 
                "D": [], "E": [], "F": [], "G": []
            },
            "start": "A",
            "algorithm": "BFS",
            "expected": ["A", "B", "C", "D", "E", "F", "G"]
        },
        {
            "description": "Binary tree structure",
            "graph": {
                "A": ["B", "C"], 
                "B": ["D", "E"], 
                "C": ["F", "G"], 
                "D": [], "E": [], "F": [], "G": []
            },
            "start": "A",
            "algorithm": "DFS",
            "expected": ["A", "B", "D", "E", "C", "F", "G"]
        },
        {
            "description": "Cyclic graph – BFS should not loop infinitely",
            "graph": {"A": ["B"], "B": ["A"]},
            "start": "A",
            "algorithm": "BFS",
            "expected": ["A", "B"]
        },
        {
            "description": "Cyclic graph – DFS should not loop infinitely",
            "graph": {"A": ["B"], "B": ["A"]},
            "start": "A",
            "algorithm": "DFS",
            "expected": ["A", "B"]
        },
        {
            "description": "Invalid start node",
            "graph": {"A": ["B"], "B": []},
            "start": "Z",
            "algorithm": "BFS",
            "expected": []
        },
        {
            "description": "Invalid start node",
            "graph": {"A": ["B"], "B": []},
            "start": "Z",
            "algorithm": "DFS",
            "expected": []
        }
    ]

    # 2) Execute each test case and record actual vs. expected
    results = []
    for tc in test_cases:
        description = tc["description"]
        g = tc["graph"]
        start = tc["start"]
        alg = tc["algorithm"]

        if alg == "BFS":
            actual_steps = bfs(g, start)
        else:
            actual_steps = dfs(g, start)

        # The final visited order is the last element in steps (or [] if no steps)
        actual_visited = actual_steps[-1] if actual_steps else []

        expected = tc["expected"]
        passed = (actual_visited == expected)

        results.append({
            "Description": description,
            "Algorithm": alg,
            "Start Node": start,
            "Input Graph": g,
            "Expected Order": expected,
            "Actual Order": actual_visited,
            "Result": "Pass" if passed else "Fail"
        })

    # 3) Build a DataFrame and display it
    df_tests = pd.DataFrame(results)
    st.dataframe(df_tests, use_container_width=True)

    # ===================================================
    # “Complexity Analysis” section
    # ===================================================
    st.markdown("---")
    st.header("📈 Complexity Analysis")

    st.markdown(
        """
**Breadth-First Search (BFS):**

- **Time Complexity – O(V + E)**  
  1. We visit every vertex (node) at most once, marking it as visited.  
  2. For each visited vertex, we inspect all its outgoing edges exactly once.  
  3. Summing over all vertices and edges yields O(V + E), where V = number of vertices and E = number of edges.

- **Space Complexity – O(V)**  
  1. We maintain a `visited` set of size up to V.  
  2. We maintain a queue that can hold up to O(V) vertices in the worst-case.  
  3. Storing the graph itself (adjacency lists) is also O(V + E), but usually we consider just the additional data structures: visited set + queue = **O(V)**.

---

**Depth-First Search (DFS):**

- **Time Complexity – O(V + E)**  
  1. Similar to BFS, each vertex is visited once and each edge is explored once in the recursion/stack process.  
  2. Therefore, total time is O(V + E).

- **Space Complexity – O(V)**  
  1. We maintain a `visited` set of up to V elements.  
  2. We use an explicit or implicit stack (in our implementation, a list is used as a stack).  
  3. In the worst case (a path of length V), the stack can hold up to V frames if the graph is a linear chain.  
  4. Hence additional space = visited set + stack = **O(V)**.

---

### How These Measures Were Determined:

- **BFS (O(V + E) time):**  
  1. We begin from a start node, enqueue it, and mark as visited.  
  2. While the queue is not empty, we dequeue a node, then enqueue all of its unvisited neighbors.  
  3. Each edge is enqueued (i.e., considered) at most once, and each vertex is dequeued/visited exactly once.  
  4. Thus, scanning adjacency lists over the entire run costs O(V + E).

- **DFS (O(V + E) time):**  
  1. We use a stack (or recursive calls) to explore as deeply as possible before backtracking.  
  2. Each vertex is pushed onto the stack and popped once; each edge is examined once when exploring neighbors.  
  3. Hence O(V + E) in total.

- **Space (O(V) for both):**  
  - The `visited` set holds up to V vertices.  
  - The queue (BFS) or stack (DFS) can hold up to O(V) in the worst-case (for example, a wide level in BFS or a long path in DFS).  
  - We ignore the O(V + E) for storing the original graph (adjacency list) because that is input size, not additional auxiliary space.

> **Note:**  
> - If the graph is extremely sparse or extremely dense, the O(V + E) bound still applies.  
> - In a directed graph, E counts directed edges. In an undirected graph, each undirected edge is counted twice in adjacency lists, but the time complexity remains O(V + E).

"""
    )
