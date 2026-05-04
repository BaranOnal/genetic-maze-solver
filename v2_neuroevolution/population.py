import numpy as np

from agent import Agent


class Population:
    def __init__(self, maze, pop_size=100,max_steps=20):
        self.maze = maze
        self.pop_size = pop_size
        self.max_steps = max_steps
        self.agents = [Agent(maze, max_steps)for _ in range(pop_size)]
        self.generation = 1

    def evaluate(self):
        for agent in self.agents:
            agent.fitness()

    def selection(self):
        fitness_scores = np.array([a.fitness_score for a in self.agents])
        total = fitness_scores.sum()

        if total == 0:
            probs = np.ones(len(self.agents)) / len(self.agents)
        else:
            probs = fitness_scores / total

        indices = np.random.choice(len(self.agents),size=2, replace=False, p=probs)
        return [self.agents[i] for i in indices]

    def crossover_and_mutate(self, mutation_rate):
        best_agent = max(self.agents, key=lambda x: x.fitness_score)
        elite = Agent(self.maze, self.max_steps)
        elite.nn.set_parameters(np.copy(best_agent.dna))
        elite.dna = elite.nn.get_parameters()
        new_agents = [elite]

        for _ in range(self.pop_size - 1):
            p1, p2 = self.selection()

            mask = np.random.rand(p1.dna_length) < 0.5
            child_dna = np.where(mask, p1.dna, p2.dna)

            mutation_mask = np.random.rand(p1.dna_length) < mutation_rate
            noise = np.random.randn(p1.dna_length) * 0.5
            child_dna = child_dna + (mutation_mask * noise)

            child = Agent(self.maze, self.max_steps)
            child.nn.set_parameters(child_dna)
            child.dna = child.nn.get_parameters()
            new_agents.append(child)
        self.agents = new_agents
        self.generation += 1
