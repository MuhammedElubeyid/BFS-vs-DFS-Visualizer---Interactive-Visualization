from collections import deque

def bfs(graph, start):
    """
    Perform breadth-first search on the given graph from the start node,
    logging the order of visits at each step.
    Returns a list of lists, where each inner list is the visited order so far.
    """
    if start not in graph:
        return []
    visited = set()
    visited_order = []
    queue = deque([start])
    steps = []

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            visited_order.append(node)
            steps.append(list(visited_order))
            for nbr in graph[node]:
                if nbr not in visited:
                    queue.append(nbr)
    return steps


def dfs(graph, start):
    """
    Perform depth-first search on the given graph from the start node,
    logging the order of visits at each step.
    Returns a list of lists, where each inner list is the visited order so far.
    """
    if start not in graph:
        return []
    visited = set()
    visited_order = []
    stack = [start]
    steps = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            visited_order.append(node)
            steps.append(list(visited_order))
            # Add neighbors in reverse order so normal order is preserved
            for nbr in reversed(graph[node]):
                if nbr not in visited:
                    stack.append(nbr)
    return steps