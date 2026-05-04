import numpy as np
from collections import deque


maze_static = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
])



def bfs_distance(maze_map, start, goal):
    """Calculates the real path distance in the maze using BFS."""
    queue = deque()
    queue.append((tuple(start), 0))
    visited = set()
    visited.add(tuple(start))

    while queue:
        (y, x), dist = queue.popleft()

        if (y, x) == tuple(goal):
            return dist

        for dy, dx in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            ny, nx = y + dy, x + dx
            if (ny, nx) not in visited:
                if 0 <= ny < maze_map.shape[0] and 0 <= nx < maze_map.shape[1]:
                    if maze_map[ny, nx] != 1:
                        visited.add((ny, nx))
                        queue.append(((ny, nx), dist + 1))

    return float('inf')


class Maze:
    def __init__(self, maze):
        self.map = maze
        self._bfs_cache = {}  # Shared cache for all agents

        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                if self.map[i, j] == 2:
                    self.start_point = (i, j)
                if self.map[i, j] == 3:
                    self.goal_point = (i, j)

    def is_valid_move(self, target_y, target_x):
        rows, cols = self.map.shape
        if target_y < 0 or target_y >= rows or target_x < 0 or target_x >= cols:
            return False
        if self.map[target_y, target_x] == 1:
            return False
        return True

    def bfs_distance(self, start, goal):
        """Cached BFS: avoids recomputing the same position."""
        key = (tuple(start), tuple(goal))
        if key not in self._bfs_cache:
            self._bfs_cache[key] = bfs_distance(self.map, start, goal)
        return self._bfs_cache[key]

