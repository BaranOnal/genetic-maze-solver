import numpy as np


DIRECTIONS = [np.array([-1, 0]), np.array([1, 0]), np.array([0, 1]), np.array([0, -1])]


class Agent:
    def __init__(self, maze, dna_length):
        self.environment = maze
        self.dna_length = dna_length
        self.pos = np.array(maze.start_point)
        self.target = np.array(maze.goal_point)
        self.dead = False
        self.reached = False
        self.fitness_score = 0.0
        self.move_count = 0
        self.collision_count = 0
        self.best_distance = float('inf')  # Tracks the closest the agent has been to the goal

        random_index = np.random.randint(low=0, high=4, size=dna_length)
        self.dna = [DIRECTIONS[i] for i in random_index]

    def move(self):
        if self.dead or self.move_count >= self.dna_length:
            return

        direction_vector = self.dna[self.move_count]
        new_point = direction_vector + self.pos

        if self.environment.is_valid_move(  new_point[0], new_point[1]):
            self.pos = new_point
        else:
            self.collision_count += 1

        if np.array_equal(self.pos, self.target):
            self.reached = True
            self.dead = True

        self.move_count += 1
        self.fitness()  # Update fitness every step

    def fitness(self):
        real_distance = self.environment.bfs_distance(self.pos, self.target)

        # Only update if agent is getting closer — score won't drop if it goes back
        if real_distance < self.best_distance:
            self.best_distance = real_distance

        if self.best_distance == float('inf'):
            self.fitness_score = 0.01
        else:
            # Exponential reward: agents closer to goal are rewarded much more
            self.fitness_score = (10.0 / (self.best_distance + 1.0)) ** 2

        if self.reached:
            # Large bonus for reaching goal; faster agents rewarded more
            self.fitness_score += 1000.0 + (self.dna_length - self.move_count) * 20.0

        # Collision penalty
        self.fitness_score -= self.collision_count * 0.01
        self.fitness_score = max(0.01, self.fitness_score)
