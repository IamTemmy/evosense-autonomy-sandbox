import pygame
import random
import math

pygame.init()

WIDTH = 800
HEIGHT = 600

AGENT_COUNT = 20
FOOD_COUNT = 18
MAX_AGENTS = 60

AGENT_RADIUS = 5
FOOD_RADIUS = 3

EAT_DISTANCE = 8
VISION_RADIUS = 100
HAZARD_AVOID_RADIUS = 80

STARTING_ENERGY = 100
ENERGY_LOSS_RATE = 0.14
HAZARD_ENERGY_LOSS_RATE = 0.45
FOOD_ENERGY_GAIN = 22
REPRODUCTION_ENERGY = 160
REPRODUCTION_COST = 70

BACKGROUND_COLOR = (20, 20, 20)
AGENT_COLOR = (0, 255, 100)
FOOD_COLOR = (255, 80, 80)
TEXT_COLOR = (230, 230, 230)
HAZARD_COLOR = (90, 20, 80)

HAZARD_ZONE = pygame.Rect(300, 200, 200, 160)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autonomous Agent Sandbox")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

births = 0
deaths = 0


def random_velocity():
    return random.choice([-2, -1, 1, 2])


def create_food():
    return {
        "x": random.randint(FOOD_RADIUS, WIDTH - FOOD_RADIUS),
        "y": random.randint(FOOD_RADIUS, HEIGHT - FOOD_RADIUS)
    }


def create_agent(x=None, y=None):
    return {
        "x": x if x is not None else random.randint(AGENT_RADIUS, WIDTH - AGENT_RADIUS),
        "y": y if y is not None else random.randint(AGENT_RADIUS, HEIGHT - AGENT_RADIUS),
        "dx": random_velocity(),
        "dy": random_velocity(),
        "energy": STARTING_ENERGY,
        "food_eaten": 0
    }


def draw_stats():
    if agents:
        average_energy = sum(agent["energy"] for agent in agents) / len(agents)
    else:
        average_energy = 0

    stats = [
        f"Population: {len(agents)}",
        f"Food: {len(foods)}",
        f"Average Energy: {average_energy:.1f}",
        f"Births: {births}",
        f"Deaths: {deaths}",
        "Purple Zone: Hazard",
        "Behavior: Seek food + avoid hazard"
    ]

    y = 10

    for stat in stats:
        text_surface = font.render(stat, True, TEXT_COLOR)
        screen.blit(text_surface, (10, y))
        y += 22


def closest_point_on_rect(rect, x, y):
    closest_x = max(rect.left, min(x, rect.right))
    closest_y = max(rect.top, min(y, rect.bottom))
    return closest_x, closest_y


agents = [create_agent() for _ in range(AGENT_COUNT)]
foods = [create_food() for _ in range(FOOD_COUNT)]

running = True

while running:

    screen.fill(BACKGROUND_COLOR)

    pygame.draw.rect(screen, HAZARD_COLOR, HAZARD_ZONE)

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

    newborn_agents = []

    for agent in agents[:]:

        agent_position = (int(agent["x"]), int(agent["y"]))

        if HAZARD_ZONE.collidepoint(agent_position):
            agent["energy"] -= HAZARD_ENERGY_LOSS_RATE
        else:
            agent["energy"] -= ENERGY_LOSS_RATE

        if agent["energy"] <= 0:
            agents.remove(agent)
            deaths += 1
            continue

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

        move_x = agent["dx"]
        move_y = agent["dy"]

        if closest_food:
            direction_x = closest_food["x"] - agent["x"]
            direction_y = closest_food["y"] - agent["y"]

            magnitude = math.hypot(direction_x, direction_y)

            if magnitude != 0:
                move_x = direction_x / magnitude * 2
                move_y = direction_y / magnitude * 2

        hazard_x, hazard_y = closest_point_on_rect(
            HAZARD_ZONE,
            agent["x"],
            agent["y"]
        )

        hazard_distance = math.hypot(
            agent["x"] - hazard_x,
            agent["y"] - hazard_y
        )

        if hazard_distance < HAZARD_AVOID_RADIUS:
            avoid_x = agent["x"] - hazard_x
            avoid_y = agent["y"] - hazard_y

            avoid_magnitude = math.hypot(avoid_x, avoid_y)

            if avoid_magnitude != 0:
                avoid_x = avoid_x / avoid_magnitude * 2.5
                avoid_y = avoid_y / avoid_magnitude * 2.5

                move_x += avoid_x
                move_y += avoid_y

        move_magnitude = math.hypot(move_x, move_y)

        if move_magnitude != 0:
            agent["dx"] = move_x / move_magnitude * 2
            agent["dy"] = move_y / move_magnitude * 2

        agent["x"] += agent["dx"]
        agent["y"] += agent["dy"]

        if agent["x"] <= AGENT_RADIUS or agent["x"] >= WIDTH - AGENT_RADIUS:
            agent["dx"] *= -1

        if agent["y"] <= AGENT_RADIUS or agent["y"] >= HEIGHT - AGENT_RADIUS:
            agent["dy"] *= -1

        agent["x"] = max(AGENT_RADIUS, min(WIDTH - AGENT_RADIUS, agent["x"]))
        agent["y"] = max(AGENT_RADIUS, min(HEIGHT - AGENT_RADIUS, agent["y"]))

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

        if agent["energy"] >= REPRODUCTION_ENERGY and len(agents) + len(newborn_agents) < MAX_AGENTS:
            agent["energy"] -= REPRODUCTION_COST

            child_x = max(
                AGENT_RADIUS,
                min(WIDTH - AGENT_RADIUS, agent["x"] + random.randint(-15, 15))
            )

            child_y = max(
                AGENT_RADIUS,
                min(HEIGHT - AGENT_RADIUS, agent["y"] + random.randint(-15, 15))
            )

            child = create_agent(child_x, child_y)
            child["energy"] = STARTING_ENERGY / 2

            newborn_agents.append(child)
            births += 1

        dynamic_radius = max(3, min(12, int(agent["energy"] / 15)))

        pygame.draw.circle(
            screen,
            AGENT_COLOR,
            (int(agent["x"]), int(agent["y"])),
            dynamic_radius
        )

    agents.extend(newborn_agents)

    draw_stats()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()