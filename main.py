import pygame
import random
import math

pygame.init()

WIDTH = 800
HEIGHT = 600

AGENT_COUNT = 20
FOOD_COUNT = 40

AGENT_RADIUS = 5
FOOD_RADIUS = 3
EAT_DISTANCE = 8

BACKGROUND_COLOR = (20, 20, 20)
AGENT_COLOR = (0, 255, 100)
FOOD_COLOR = (255, 80, 80)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autonomous Agent Sandbox")

clock = pygame.time.Clock()


def random_velocity():
    return random.choice([-2, -1, 1, 2])


def create_food():
    return {
        "x": random.randint(FOOD_RADIUS, WIDTH - FOOD_RADIUS),
        "y": random.randint(FOOD_RADIUS, HEIGHT - FOOD_RADIUS)
    }


agents = []

for _ in range(AGENT_COUNT):
    agents.append({
        "x": random.randint(AGENT_RADIUS, WIDTH - AGENT_RADIUS),
        "y": random.randint(AGENT_RADIUS, HEIGHT - AGENT_RADIUS),
        "dx": random_velocity(),
        "dy": random_velocity(),
        "food_eaten": 0
    })


foods = []

for _ in range(FOOD_COUNT):
    foods.append(create_food())


running = True

while running:

    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for food in foods:
        pygame.draw.circle(
            screen,
            FOOD_COLOR,
            (food["x"], food["y"]),
            FOOD_RADIUS
        )

    for agent in agents:

        agent["x"] += agent["dx"]
        agent["y"] += agent["dy"]

        if agent["x"] <= AGENT_RADIUS or agent["x"] >= WIDTH - AGENT_RADIUS:
            agent["dx"] *= -1

        if agent["y"] <= AGENT_RADIUS or agent["y"] >= HEIGHT - AGENT_RADIUS:
            agent["dy"] *= -1

        for food in foods[:]:
            distance = math.hypot(agent["x"] - food["x"], agent["y"] - food["y"])

            if distance < EAT_DISTANCE:
                foods.remove(food)
                foods.append(create_food())
                agent["food_eaten"] += 1

        pygame.draw.circle(
            screen,
            AGENT_COLOR,
            (int(agent["x"]), int(agent["y"])),
            AGENT_RADIUS
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()