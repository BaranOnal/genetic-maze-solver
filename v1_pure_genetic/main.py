# --- PYGAME VISUALIZATION ---

import pygame

from environment import Maze, maze_static
from population import Population

CELL_SIZE   = 42
PANEL_WIDTH = 340
ROWS, COLS  = maze_static.shape
WIDTH       = COLS * CELL_SIZE + PANEL_WIDTH
HEIGHT      = ROWS * CELL_SIZE
FPS         = 15

# Colors
WHITE      = (245, 245, 245)
BLACK      = (25, 25, 25)
GREEN      = (60, 200, 80)
RED        = (230, 70, 70)
BLUE       = (70, 130, 255, 80)
YELLOW     = (255, 215, 0)
GRAY       = (210, 210, 210)
DARK_BG    = (18, 18, 28)
PANEL_BG   = (28, 28, 42)
TEXT_COLOR = (235, 235, 235)
DIM_TEXT   = (140, 140, 170)
ACCENT     = (100, 100, 200)
DIVIDER    = (60, 60, 90)


def draw_maze(screen, maze_obj):
    for row in range(maze_obj.map.shape[0]):
        for col in range(maze_obj.map.shape[1]):
            rect  = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            value = maze_obj.map[row, col]

            if value == 1:
                pygame.draw.rect(screen, BLACK, rect, border_radius=6)
            elif value == 2:
                pygame.draw.rect(screen, GREEN, rect, border_radius=6)
            elif value == 3:
                pygame.draw.rect(screen, RED, rect, border_radius=6)
            else:
                pygame.draw.rect(screen, WHITE, rect, border_radius=6)

            pygame.draw.rect(screen, GRAY, rect, 1, border_radius=6)


def draw_agents(screen, agents, best_agent):
    surface = pygame.Surface((COLS * CELL_SIZE, HEIGHT), pygame.SRCALPHA)

    # Draw regular agents first (blue), best agent on top (yellow)
    for agent in agents:
        if agent is not best_agent:
            x = agent.pos[1] * CELL_SIZE + CELL_SIZE // 2
            y = agent.pos[0] * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(surface, BLUE, (int(x), int(y)), CELL_SIZE // 6)

    if best_agent:
        x = best_agent.pos[1] * CELL_SIZE + CELL_SIZE // 2
        y = best_agent.pos[0] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(surface, YELLOW, (int(x), int(y)), CELL_SIZE // 4)
        pygame.draw.circle(surface, BLACK,  (int(x), int(y)), CELL_SIZE // 4, 2)

    screen.blit(surface, (0, 0))


def draw_panel(screen, font, small_font, tiny_font, pop, best_agent, alive_count, step_counter, all_time_best_score, speed_multiplier):
    px = COLS * CELL_SIZE

    pygame.draw.rect(screen, PANEL_BG, (px, 0, PANEL_WIDTH, HEIGHT))
    pygame.draw.rect(screen, ACCENT,   (px, 0, 3, HEIGHT))

    y = 16

    # Title
    title = font.render("GENETIC  MAZE", True, YELLOW)
    screen.blit(title, (px + 20, y))
    y += 36

    sub = tiny_font.render("Genetic Algorithm Visualizer", True, DIM_TEXT)
    screen.blit(sub, (px + 22, y))
    y += 24

    pygame.draw.rect(screen, DIVIDER, (px + 16, y, PANEL_WIDTH - 32, 1))
    y += 12

    # --- Simulation ---
    screen.blit(tiny_font.render("SIMULATION", True, ACCENT), (px + 20, y))
    y += 20

    sim_stats = [
        ("Generation",  str(pop.generation)),
        ("Population",  str(pop.pop_size)),
        ("DNA Length",  str(pop.dna_length)),
        ("Alive",       str(alive_count)),
        ("Step",        f"{step_counter} / {pop.dna_length}"),
    ]

    for key, val in sim_stats:
        screen.blit(small_font.render(key, True, DIM_TEXT), (px + 20, y))
        v = small_font.render(val, True, TEXT_COLOR)
        screen.blit(v, (px + PANEL_WIDTH - v.get_width() - 20, y))
        y += 24

    pygame.draw.rect(screen, DIVIDER, (px + 16, y, PANEL_WIDTH - 32, 1))
    y += 12

    # --- Best Agent ---
    screen.blit(tiny_font.render("BEST AGENT", True, ACCENT), (px + 20, y))
    y += 20

    reached = best_agent.reached

    agent_stats = [
        ("Score",       f"{best_agent.fitness_score:.2f}"),
        ("All-Time Best", f"{all_time_best_score:.2f}"),
        ("Collisions",  str(best_agent.collision_count)),
        ("Goal",        str(tuple(best_agent.environment.goal_point))),
        ("Reached",     "YES" if reached else "NO"),
    ]

    for key, val in agent_stats:
        screen.blit(small_font.render(key, True, DIM_TEXT), (px + 20, y))
        color = GREEN if (key == "Reached" and reached) else \
                YELLOW if key == "All-Time Best" else TEXT_COLOR
        v = small_font.render(val, True, color)
        screen.blit(v, (px + PANEL_WIDTH - v.get_width() - 20, y))
        y += 24

    pygame.draw.rect(screen, DIVIDER, (px + 16, y, PANEL_WIDTH - 32, 1))
    y += 12

    # --- Legend ---
    screen.blit(tiny_font.render("LEGEND", True, ACCENT), (px + 20, y))
    y += 20

    legend = [
        "Yellow  =  Best agent",
        "Blue    =  Other agents",
        "Green   =  Start",
        "Red     =  Goal",
    ]
    for text in legend:
        screen.blit(small_font.render(text, True, DIM_TEXT), (px + 20, y))
        y += 22

    pygame.draw.rect(screen, DIVIDER, (px + 16, y, PANEL_WIDTH - 32, 1))
    y += 12

    # --- Controls ---
    screen.blit(tiny_font.render("CONTROLS", True, ACCENT), (px + 20, y))
    y += 20

    speed_color = GREEN if speed_multiplier > 1 else TEXT_COLOR
    controls = [
        ("ESC",     "Quit"),
        ("1 / 2 / 3", f"Speed  {speed_multiplier}x"),
    ]
    for key, val in controls:
        screen.blit(small_font.render(key, True, YELLOW), (px + 20, y))
        v = small_font.render(val, True, speed_color if "Speed" in val else DIM_TEXT)
        screen.blit(v, (px + PANEL_WIDTH - v.get_width() - 20, y))
        y += 24


# --- MAIN LOOP ---

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Genetic Algorithm Maze Solver")
    clock = pygame.time.Clock()

    font       = pygame.font.SysFont("consolas", 22, bold=True)
    small_font = pygame.font.SysFont("consolas", 17)
    tiny_font  = pygame.font.SysFont("consolas", 13, bold=True)

    environment = Maze(maze_static)
    pop = Population(environment, pop_size=200, dna_length=75)

    mutation_rate      = 0.05
    running            = True
    speed_multiplier   = 1       # 1x, 2x or 3x
    all_time_best_score = 0.0

    while running:
        step_counter = 0

        while step_counter < pop.dna_length and running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_1:
                        speed_multiplier = 1
                    elif event.key == pygame.K_2:
                        speed_multiplier = 2
                    elif event.key == pygame.K_3:
                        speed_multiplier = 3

            # Run multiple steps per frame based on speed multiplier
            all_dead = False
            for _ in range(speed_multiplier):
                if step_counter >= pop.dna_length:
                    break
                all_dead = True
                for agent in pop.agents:
                    if not agent.dead:
                        agent.move()
                        all_dead = False
                step_counter += 1
                if all_dead:
                    break

            # Single source of truth for best agent
            best_agent  = max(pop.agents, key=lambda x: x.fitness_score)
            alive_count = sum(not a.dead for a in pop.agents)

            # Track all-time best score across all generations
            if best_agent.fitness_score > all_time_best_score:
                all_time_best_score = best_agent.fitness_score

            screen.fill(DARK_BG)
            draw_maze(screen, environment)
            draw_agents(screen, pop.agents, best_agent)
            draw_panel(screen, font, small_font, tiny_font, pop, best_agent, alive_count, step_counter, all_time_best_score, speed_multiplier)
            pygame.display.flip()
            clock.tick(FPS)

            if all_dead:
                break

        if running:
            pop.evaluate()
            pop.crossover_and_mutate(mutation_rate)

    pygame.quit()


if __name__ == "__main__":
    main()
