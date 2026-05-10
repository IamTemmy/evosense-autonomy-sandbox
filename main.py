import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
AGENT_COUNT = 20
AGENT_RADIUS = 5
AGENT_COLOR = (0, 255, 100)
BACKGROUND_COLOR = (20, 20, 20)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autonomous Agent Sandbox")

clock = pygame.time.Clock()


def random_velocity():
    """Return a non-zero velocity so agents always move."""
    return random.choice([-2, -1, 1, 2])


agents = []

for _ in range(AGENT_COUNT):
    agents.append({
        "x": random.randint(AGENT_RADIUS, WIDTH - AGENT_RADIUS),
        "y": random.randint(AGENT_RADIUS, HEIGHT - AGENT_RADIUS),
        "dx": random_velocity(),
        "dy": random_velocity()
    })


running = True

while running:
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for agent in agents:
        agent["x"] += agent["dx"]
        agent["y"] += agent["dy"]

        if agent["x"] <= AGENT_RADIUS or agent["x"] >= WIDTH - AGENT_RADIUS:
            agent["dx"] *= -1

        if agent["y"] <= AGENT_RADIUS or agent["y"] >= HEIGHT - AGENT_RADIUS:
            agent["dy"] *= -1

        pygame.draw.circle(
            screen,
            AGENT_COLOR,
            (int(agent["x"]), int(agent["y"])),
            AGENT_RADIUS
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()