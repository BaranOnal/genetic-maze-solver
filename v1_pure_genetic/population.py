import numpy as np

from agent import Agent, DIRECTIONS


class Population:
    def __init__(self, maze, pop_size=100, dna_length=50):
        self.maze = maze
        self.dna_length = dna_length
        self.pop_size = pop_size
        self.agents = [Agent(maze, dna_length) for _ in range(pop_size)]
        self.generation = 1

    def evaluate(self):
        for agent in self.agents:
            agent.fitness()

    def selection(self):
        """Roulette wheel selection — parents chosen proportional to fitness."""
        fitness_scores = np.array([a.fitness_score for a in self.agents])
        total = fitness_scores.sum()

        if total == 0:
            probs = np.ones(len(self.agents)) / len(self.agents)
        else:
            probs = fitness_scores / total

        indices = np.random.choice(len(self.agents), size=2, replace=False, p=probs)
        return [self.agents[i] for i in indices]

    def crossover_and_mutate(self, mutation_rate):
        # Elitism: copy best agent's DNA into a fresh agent (reset state)
        best_agent = max(self.agents, key=lambda a: a.fitness_score)
        elite = Agent(self.maze, self.dna_length)
        elite.dna = best_agent.dna[:]
        new_agents = [elite]

        for _ in range(self.pop_size - 1):
            p1, p2 = self.selection()

            # Uniform crossover
            child_dna = []
            for j in range(self.dna_length):
                child_dna.append(p1.dna[j] if np.random.rand() < 0.5 else p2.dna[j])

            # Mutation
            for j in range(self.dna_length):
                if np.random.rand() < mutation_rate:
                    child_dna[j] = DIRECTIONS[np.random.randint(0, 4)]

            child = Agent(self.maze, self.dna_length)
            child.dna = child_dna
            new_agents.append(child)

        self.agents = new_agents
        self.generation += 1
