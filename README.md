# 🧬 Genetic Maze Solver

 A project exploring different AI approaches for solving a grid-based maze — evolving agents to reach the goal efficiently.

---

##  Project Structure

```
genetic-maze-solver/
├── v1_pure_genetic/
│   ├── agent.py          # Agent class with DNA and fitness logic
│   ├── environment.py    # Maze definition and BFS distance utility
│   ├── population.py     # Selection, crossover, mutation
│   └── main.py           # Pygame visualization and main loop
└── README.md
```

---

## ️ Project Roadmap

| Version | Approach | Status |
|---------|----------|--------|
| v1 | Pure Genetic Algorithm | ✅ Complete |
| v2 | Neuroevolution (GA-evolved neural networks) | 🔜 Coming Soon |

---

## v1 — Pure Genetic Algorithm

Agents carry a fixed-length DNA sequence of movement directions. Over generations, the population evolves through selection, crossover, and mutation to find a path from start to goal.

### Algorithm Details

| Parameter | Value |
|-----------|-------|
| Population size | 200 agents |
| DNA length | 75 steps |
| Selection | Roulette wheel (fitness-proportional) |
| Crossover | Uniform (50% per gene) |
| Mutation rate | 5% |
| Elitism | Best agent preserved each generation |
| Fitness | BFS-based true path distance + goal bonus |

### Fitness Function

- Reward is based on the **closest BFS distance** the agent ever reached to the goal (best distance is monotonically tracked — score never drops for backtracking)
- Exponential reward: `(10 / (best_distance + 1))²`
- **Goal bonus:** `1000 + (dna_length - move_count) × 20` — faster agents are rewarded more
- **Collision penalty:** `-0.01` per wall collision
- Minimum fitness score is clamped to `0.01`

### Setup & Run

```bash
    pip install numpy pygame
    cd v1_pure_genetic
    python main.py
```

### Controls

| Key | Action |
|-----|--------|
| `1` / `2` / `3` | Speed multiplier |
| `ESC` | Quit |

### Visualization

| Color | Meaning |
|-------|---------|
| Yellow | Best agent (current generation) |
| Blue | All other agents |
| Green | Start point |
| Red | Goal point |

The side panel shows real-time stats: generation number, alive agents, current step, best fitness score, and whether the goal has been reached.

---


## v2 — Neuroevolution (Coming Soon)

Instead of a fixed DNA sequence, agents will use a small neural network to decide their next move based on local environment observations. The genetic algorithm will evolve the network weights across generations.

---

## Maze

The maze is a 15×15 grid hardcoded in `environment.py`. Cells:
- `0` → Open path
- `1` → Wall
- `2` → Start (green)
- `3` → Goal (red)

BFS distances are computed lazily and cached per `(start, goal)` pair to avoid redundant computation across the population.

---