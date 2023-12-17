#!/usr/bin/env python

import sys
import heapq

def dijkstra_constraints(grid, min_consecutive = 0, max_consecutive = 3):
    rows, cols = len(grid), len(grid[0])

    def get_cost(x, y):
        return int(grid[x][y])

    directions = [(-1, 0, 'N'), (1, 0, 'S'), (0, -1, 'W'), (0, 1, 'E')]

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols

    pq = [(0, 0, 0, '', 0, [])]  # Added path as part of the state
    visited = set()

    while pq:
        cost, x, y, last_dir, consecutive, path = heapq.heappop(pq)

        if (x, y) == (rows - 1, cols - 1):
            return cost, path + [(x, y)]

        if (x, y, last_dir, consecutive) in visited:
            continue
        visited.add((x, y, last_dir, consecutive))

        for dx, dy, dir in directions:
            if consecutive <= min_consecutive and (last_dir != '' and dir != last_dir):
                continue

            new_x, new_y = x + dx, y + dy

            if is_valid(new_x, new_y) and (not path or (new_x, new_y) != path[-1]):
                if dir == last_dir:
                    new_consecutive = consecutive + 1
                else:
                    new_consecutive = 1

                if new_consecutive <= max_consecutive:
                    new_cost = cost + get_cost(new_x, new_y) if (new_x, new_y) != (0, 0) else cost
                    heapq.heappush(pq, (new_cost, new_x, new_y, dir, new_consecutive, path + [(x, y)]))

    return float('inf'), []

def main():
    FILE_NAME = sys.argv[1]
    grid = []
    with open(FILE_NAME, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            grid.append(line)

    # p1
    shortest_path_cost, path = dijkstra_constraints(grid, max_consecutive = 3)

    # Display the path visually
    visual_grid = [list(row) for row in grid]
    for x, y in path:
        visual_grid[x][y] = '*'

    # Join the rows for display
    visual_grid = [''.join(row) for row in visual_grid]
    visual_path = "\n".join(visual_grid)

    print(visual_path)
    print('Part 1:', shortest_path_cost)

    # p2
    shortest_path_cost, path = dijkstra_constraints(grid, min_consecutive = 3, max_consecutive = 10)

    # Display the path visually
    visual_grid = [list(row) for row in grid]
    for x, y in path:
        visual_grid[x][y] = '*'

    # Join the rows for display
    visual_grid = [''.join(row) for row in visual_grid]
    visual_path = "\n".join(visual_grid)

    print(visual_path)
    print('Part 2:', shortest_path_cost)
if __name__ == "__main__":
    main()
