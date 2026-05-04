from neural_network import NeuralNetwork
from environment import *

DIRECTIONS = [np.array([-1, 0]), np.array([1, 0]), np.array([0, 1]), np.array([0, -1])]


class Agent:
    def __init__(self, maze, move_limit):#In the first version, dna_length defines the movement limit. In this version, move_limit
        self.environment = maze
        self.move_limit = move_limit
        self.pos = np.array(maze.start_point)
        self.target = np.array(maze.goal_point)
        self.dead = False
        self.reached = False
        self.fitness_score = 0.0
        self.move_count = 0
        self.collision_count = 0
        self.best_distance = float('inf')

        self.visited = {}
        self.visited[tuple(self.pos)] = 1

        self.nn = NeuralNetwork(input_size=8, hidden_size=16, output_size=4)
        self.dna = self.nn.get_parameters()

        self.dna_length = len(self.dna)
        r, c = self.environment.map.shape
        self._max_dist = float(r + c)
    def get_input(self):
        input_vector = []
        wall_max = np.max(self.environment.map.shape)

        for d in DIRECTIONS:
            dy, dx = d[0], d[1]  # d[0] = row_delta = y_delta, d[1] = col_delta = x_delta
            current_y, current_x = self.pos[0], self.pos[1]
            distance = 0
            while self.environment.is_valid_move(current_y + dy, current_x + dx):
                distance += 1
                current_y += dy
                current_x += dx
            input_vector.append(distance / wall_max)

        real_distance = self.environment.bfs_distance(self.pos, self.target)
        if real_distance == float('inf'):
            input_vector.append(1.0)
        else:
           input_vector.append(real_distance / self._max_dist)

        rel_row = (self.target[0] - self.pos[0]) / self._max_dist
        rel_col = (self.target[1] - self.pos[1]) / self._max_dist
        input_vector.append(np.clip(rel_row, -1, 1))
        input_vector.append(np.clip(rel_col, -1, 1))

        visit_count = self.visited.get(tuple(self.pos), 0)
        input_vector.append(min(visit_count / 10.0, 1.0))

        return np.array(input_vector)


    def move(self):
        if self.dead or self.move_count >= self.move_limit:
            return

        input = self.get_input()

        output = self.nn.forward(input)

        action_index = np.argmax(output)

        direction_vector = DIRECTIONS[action_index]
        new_point = direction_vector + self.pos

        #key = tuple(self.pos)
        #if self.visited[key] >= 3:
        #    self.dead = True


        if self.environment.is_valid_move(new_point[0], new_point[1]):
            self.pos = new_point
        else:
            self.collision_count += 1

        key = tuple(self.pos)
        self.visited[key] = self.visited.get(key, 0) + 1

        if np.array_equal(self.pos, self.target):
            self.reached = True
            self.dead = True

        self.move_count += 1
        self.fitness()

    def fitness(self):
        real_distance = self.environment.bfs_distance(self.pos, self.target)

        # Only update if agent is getting closer — score won't drop if it goes back
        if real_distance < self.best_distance:
            self.best_distance = real_distance

        if self.best_distance == float('inf'):
            self.fitness_score = 0.01
        else:
            self.fitness_score = (10.0 / (self.best_distance + 1.0))

        if self.reached:
            # Large bonus for reaching goal; faster agents rewarded more
            self.fitness_score += 1000.0 + (self.dna_length - self.move_count) * 20.0
        # Collision penalty
        self.fitness_score -= self.collision_count * 0.005
        # Revisit penalty
        revisit_penalty = sum(max(0, v - 1) for v in self.visited.values())
        self.fitness_score -= revisit_penalty * 0.005

        self.fitness_score = max(0.01, self.fitness_score)
