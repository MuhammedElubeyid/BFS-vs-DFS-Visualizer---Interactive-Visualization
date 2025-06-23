from collections import deque

def bfs(graph, start):
    if start not in graph:
        return []
    visited = set()
    queue = deque([start])
    steps = []
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            steps.append(list(visited))
            for nbr in graph[node]:
                if nbr not in visited:
                    queue.append(nbr)
    return steps


def dfs(graph, start):
    if start not in graph:
        return []
    visited = set()
    stack = [start]
    steps = []
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            steps.append(list(visited))
            for nbr in reversed(graph[node]):
                if nbr not in visited:
                    stack.append(nbr)
    return steps