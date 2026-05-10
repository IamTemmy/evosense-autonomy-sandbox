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
VISION_RADIUS = 120

STARTING_ENERGY = 100
ENERGY_LOSS_RATE = 0.08
FOOD_ENERGY_GAIN = 30

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


def create_agent():
    return {
        "x": random.randint(AGENT_RADIUS, WIDTH - AGENT_RADIUS),
        "y": random.randint(AGENT_RADIUS, HEIGHT - AGENT_RADIUS),
        "dx": random_velocity(),
        "dy": random_velocity(),
        "energy": STARTING_ENERGY,
        "food_eaten": 0
    }


agents = [create_agent() for _ in range(AGENT_COUNT)]
foods = [create_food() for _ in range(FOOD_COUNT)]

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

    for agent in agents[:]:

        agent["energy"] -= ENERGY_LOSS_RATE

        if agent["energy"] <= 0:
            agents.remove(agent)
            continue

        # FIND CLOSEST FOOD
        closest_food = None
        closest_distance = float("inf")

        for food in foods:
            distance = math.hypot(
                food["x"] - agent["x"],
                food["y"] - agent["y"]
            )

            if distance < closest_distance and distance < VISION_RADIUS:
                closest_distance = distance
                closest_food = food

        # MOVE TOWARD FOOD
        if closest_food:

            direction_x = closest_food["x"] - agent["x"]
            direction_y = closest_food["y"] - agent["y"]

            magnitude = math.hypot(direction_x, direction_y)

            if magnitude != 0:
                agent["dx"] = direction_x / magnitude * 2
                agent["dy"] = direction_y / magnitude * 2

        agent["x"] += agent["dx"]
        agent["y"] += agent["dy"]

        # WALL BOUNCE
        if agent["x"] <= AGENT_RADIUS or agent["x"] >= WIDTH - AGENT_RADIUS:
            agent["dx"] *= -1

        if agent["y"] <= AGENT_RADIUS or agent["y"] >= HEIGHT - AGENT_RADIUS:
            agent["dy"] *= -1

        # FOOD COLLISION
        for food in foods[:]:

            distance = math.hypot(
                agent["x"] - food["x"],
                agent["y"] - food["y"]
            )

            if distance < EAT_DISTANCE:
                foods.remove(food)
                foods.append(create_food())

                agent["food_eaten"] += 1
                agent["energy"] += FOOD_ENERGY_GAIN

        pygame.draw.circle(
            screen,
            AGENT_COLOR,
            (int(agent["x"]), int(agent["y"])),
            AGENT_RADIUS
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()