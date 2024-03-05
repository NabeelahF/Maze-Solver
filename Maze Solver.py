import random

class Maze:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.maze = [[' ' for _ in range(columns)] for _ in range(rows)]
        self.barrier_nodes = set()

    def set_starting_node(self, x, y):
        self.start_node = (x, y)
        self.maze[y][x] = 'S'

    def set_goal_node(self, x, y):
        self.goal_node = (x, y)
        self.maze[y][x] = 'G'

    def set_barrier_node(self, x, y):
        self.maze[y][x] = 'X'
        self.barrier_nodes.add((x, y))  # Add the barrier node to the set

    def set_path_node(self, x, y):
        self.maze[y][x] = 'P'

    def convert_to_node_number(self, x, y):
        return y + x * self.rows

    def convert_to_coordinates(self, node_number):
        x, y = divmod(node_number, self.rows)
        return x, y

    def print_maze(self, final_path=None):
        for y in range(self.rows):
            for x in range(self.columns):
                node_number = self.convert_to_node_number(x, y)
                if final_path and (x, y) in final_path:
                    print('\033[91m', end='')
                if (x, y) == self.start_node:
                    print('S', end=' ')
                elif (x, y) == self.goal_node:
                    print('G', end=' ')
                elif (x, y) in self.barrier_nodes:
                    print('X', end=' ')
                else:
                    print(f'{node_number:<3}', end=' ')
                if final_path and (x, y) in final_path:
                    print('\033[0m', end='')  # End color
            print()

    def manhattan_distance(self, node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

class DFS:
    def __init__(self, maze):
        self.maze = maze
        self.visited_nodes = set()
        self.final_path = []
        self.time_to_goal = 0

    def is_valid_move(self, x, y):
        return 0 <= x < self.maze.columns and 0 <= y < self.maze.rows

    def is_valid_neighbor(self, x, y):
        return self.is_valid_move(x, y) and self.maze.maze[y][x] != 'X' and (x, y) not in self.visited_nodes

    def get_neighbors_increasing_order(self, x, y):
        neighbors = [
            (x, y - 1),  # Up
            (x - 1, y),  # Left
            (x + 1, y),  # Right
            (x, y + 1),  # Down
            (x - 1, y - 1),  # Diagonal Up-Left
            (x + 1, y - 1),  # Diagonal Up-Right
            (x - 1, y + 1),  # Diagonal Down-Left
            (x + 1, y + 1)   # Diagonal Down-Right
        ]

        # Filter out neighbors outside the maze boundaries
        valid_neighbors = [
            neighbor for neighbor in neighbors if
            self.is_valid_neighbor(*neighbor)
        ]

        # Sort neighbors based on their assigned numbers (row * num_columns + column)
        valid_neighbors.sort(key=lambda n: n[1] * self.maze.columns + n[0])

        return valid_neighbors

    def dfs(self, x, y):
        self.visited_nodes.add((x, y))
        self.time_to_goal += 1

        if (x, y) == self.maze.goal_node:
            self.final_path = [(x, y)]
            return True

        for neighbor in self.get_neighbors_increasing_order(x, y):
            if neighbor not in self.visited_nodes:
                if self.dfs(*neighbor):
                    self.final_path.insert(0, neighbor)
                    return True

        return False

    def solve(self, start_x, start_y):
        self.dfs(start_x, start_y)
        return bool(self.final_path)  # Return True if the final path is found

class AStarSearch:
    def __init__(self, maze):
        self.maze = maze
        self.visited_nodes = set()
        self.final_path = []
        self.time_to_goal = 0

    def is_valid_move(self, x, y):
        return 0 <= x < self.maze.columns and 0 <= y < self.maze.rows

    def is_valid_neighbor(self, x, y):
        return self.is_valid_move(x, y) and self.maze.maze[y][x] != 'X' and (x, y) not in self.visited_nodes

    def get_neighbors_increasing_order(self, x, y):
        neighbors = [
            (x, y - 1),  # Up
            (x - 1, y),  # Left
            (x + 1, y),  # Right
            (x, y + 1),  # Down
            (x - 1, y - 1),  # Diagonal Up-Left
            (x + 1, y - 1),  # Diagonal Up-Right
            (x - 1, y + 1),  # Diagonal Down-Left
            (x + 1, y + 1)   # Diagonal Down-Right
        ]

        # Filter out neighbors outside the maze boundaries
        valid_neighbors = [
            neighbor for neighbor in neighbors if
            self.is_valid_neighbor(*neighbor)
        ]

        # Sort neighbors based on their assigned numbers (row * num_columns + column)
        valid_neighbors.sort(key=lambda n: n[1] * self.maze.columns + n[0])

        return valid_neighbors

    def a_star_search(self):
        start_node_number = self.maze.convert_to_node_number(*self.maze.start_node)
        goal_node_number = self.maze.convert_to_node_number(*self.maze.goal_node)

        open_set = [(start_node_number, 0, 0)]  # (node_number, g_cost, f_cost)
        came_from = {}
        g_cost = {start_node_number: 0}

        while open_set:
            current_node_number, g_current, f_current = min(open_set, key=lambda x: x[2])
            open_set.remove((current_node_number, g_current, f_current))

            if current_node_number == goal_node_number:
                self.final_path = self.reconstruct_path(came_from, current_node_number)
                return True

            current_node = self.maze.convert_to_coordinates(current_node_number)

            for neighbor in self.get_neighbors_increasing_order(*current_node):
                neighbor_node_number = self.maze.convert_to_node_number(*neighbor)
                tentative_g_cost = g_current + 1

                if neighbor_node_number not in g_cost or tentative_g_cost < g_cost[neighbor_node_number]:
                    g_cost[neighbor_node_number] = tentative_g_cost
                    f_cost = tentative_g_cost + self.maze.manhattan_distance(neighbor, self.maze.goal_node)
                    open_set.append((neighbor_node_number, tentative_g_cost, f_cost))
                    came_from[neighbor_node_number] = current_node_number

        return False

    def reconstruct_path(self, came_from, current_node):
        path = [current_node]
        while current_node in came_from:
            current_node = came_from[current_node]
            path.append(current_node)
        return path[::-1]

    def solve(self):
        start_node_number = self.maze.convert_to_node_number(*self.maze.start_node)
        goal_node_number = self.maze.convert_to_node_number(*self.maze.goal_node)

        if self.a_star_search():
            self.time_to_goal = len(self.final_path) - 1
            self.visited_nodes = set(self.final_path)
            return True
        else:
            return False

# Initialize a 6x6 maze
maze = Maze(6, 6)

# Randomly select starting node within the node numbers 0-11 (first two columns)
start_node_number = random.randint(0, 11)
start_x, start_y = maze.convert_to_coordinates(start_node_number)

# Ensure that the starting node is not a barrier node and is in the first two columns
while (start_x, start_y) in maze.barrier_nodes or start_x >= 2:
    start_node_number = random.randint(0, 11)
    start_x, start_y = maze.convert_to_coordinates(start_node_number)

maze.set_starting_node(start_x, start_y)

# Randomly select goal node within the 24-35 nodes
goal_x, goal_y = divmod(random.randint(24, 35), 6)
maze.set_goal_node(goal_x, goal_y)

# Randomly select four barrier nodes from the remaining 34 nodes
barrier_nodes = set()
while len(barrier_nodes) < 4:
    barrier_node = divmod(random.randint(0, 35), 6)
    if barrier_node != maze.start_node and barrier_node != maze.goal_node and barrier_node not in barrier_nodes:
        barrier_nodes.add(barrier_node)

# Set barrier nodes in the maze
for node in barrier_nodes:
    maze.set_barrier_node(*node)

# Print the initial maze
maze.print_maze()

dfs_solver = DFS(maze)

# Perform DFS starting from the initial node
if dfs_solver.solve(start_x, start_y):
    print("DFS Goal reached!")
else:
    print("DFS Goal not reachable.")

# Print results
print("DFS Visited Nodes:", [maze.convert_to_node_number(x, y) for x, y in dfs_solver.visited_nodes])
print("DFS Visited Nodes:", dfs_solver.visited_nodes)
print("DFS Time to Goal:", dfs_solver.time_to_goal, "minutes")
print("DFS Final Path:", [maze.convert_to_node_number(x, y) for x, y in dfs_solver.final_path])
print("DFS Final Path:", dfs_solver.final_path)
print("Final Path Length",len(dfs_solver.final_path))

astar_solver = AStarSearch(maze)

# Perform A* search starting from the initial node
if astar_solver.solve():
    print("A* Goal reached!")
else:
    print("Goal not reachable.")

# Print results
print("A* Visited Nodes:", [maze.convert_to_coordinates(node) for node in astar_solver.visited_nodes])
print("A* Time to Goal:", astar_solver.time_to_goal+1, "minutes")
print("A* Final Path:", [maze.convert_to_coordinates(node) for node in astar_solver.final_path])
