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

BASE_SPEED = 2.0
BASE_VISION_RADIUS = 120
BASE_ENERGY_LOSS_RATE = 0.14

STARTING_ENERGY = 100
HAZARD_ENERGY_LOSS_RATE = 0.35
FOOD_ENERGY_GAIN = 24
REPRODUCTION_ENERGY = 160
REPRODUCTION_COST = 70

MUTATION_RATE = 0.12
COLOR_MUTATION_RATE = 18

MIN_SPEED = 1.0
MAX_SPEED = 3.5

MIN_VISION_RADIUS = 60
MAX_VISION_RADIUS = 200

MIN_ENERGY_LOSS_RATE = 0.08
MAX_ENERGY_LOSS_RATE = 0.25

BACKGROUND_COLOR = (20, 20, 20)
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
hazard_enabled = True
next_lineage_id = 1


def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


def mutate(value, mutation_strength, min_value, max_value):
    mutation = random.uniform(-mutation_strength, mutation_strength)
    return clamp(value + mutation, min_value, max_value)


def mutate_color(color):
    r, g, b = color

    r = int(clamp(r + random.randint(-COLOR_MUTATION_RATE, COLOR_MUTATION_RATE), 40, 255))
    g = int(clamp(g + random.randint(-COLOR_MUTATION_RATE, COLOR_MUTATION_RATE), 40, 255))
    b = int(clamp(b + random.randint(-COLOR_MUTATION_RATE, COLOR_MUTATION_RATE), 40, 255))

    return (r, g, b)


def random_agent_color():
    return (
        random.randint(80, 255),
        random.randint(80, 255),
        random.randint(80, 255)
    )


def random_velocity(speed):
    angle = random.uniform(0, math.tau)
    return math.cos(angle) * speed, math.sin(angle) * speed


def normalize_vector(x, y, speed):
    magnitude = math.hypot(x, y)

    if magnitude == 0:
        return random_velocity(speed)

    return x / magnitude * speed, y / magnitude * speed


def create_food():
    while True:
        x = random.randint(FOOD_RADIUS, WIDTH - FOOD_RADIUS)
        y = random.randint(FOOD_RADIUS, HEIGHT - FOOD_RADIUS)

        if not hazard_enabled or not HAZARD_ZONE.collidepoint(x, y):
            return {"x": x, "y": y}


def create_agent(x=None, y=None, parent=None):
    global next_lineage_id

    if parent:
        speed = mutate(parent["speed"], MUTATION_RATE, MIN_SPEED, MAX_SPEED)
        vision_radius = mutate(parent["vision_radius"], 12, MIN_VISION_RADIUS, MAX_VISION_RADIUS)
        energy_loss_rate = mutate(
            parent["energy_loss_rate"],
            0.015,
            MIN_ENERGY_LOSS_RATE,
            MAX_ENERGY_LOSS_RATE
        )

        color = mutate_color(parent["color"])
        lineage_id = parent["lineage_id"]

    else:
        speed = random.uniform(1.5, 2.5)
        vision_radius = random.uniform(90, 150)
        energy_loss_rate = random.uniform(0.11, 0.17)

        color = random_agent_color()
        lineage_id = next_lineage_id
        next_lineage_id += 1

    dx, dy = random_velocity(speed)

    return {
        "x": x if x is not None else random.randint(AGENT_RADIUS, WIDTH - AGENT_RADIUS),
        "y": y if y is not None else random.randint(AGENT_RADIUS, HEIGHT - AGENT_RADIUS),
        "dx": dx,
        "dy": dy,
        "energy": STARTING_ENERGY,
        "food_eaten": 0,
        "speed": speed,
        "vision_radius": vision_radius,
        "energy_loss_rate": energy_loss_rate,
        "color": color,
        "lineage_id": lineage_id
    }


def reset_simulation():
    global agents, foods, births, deaths, next_lineage_id

    next_lineage_id = 1
    agents = [create_agent() for _ in range(AGENT_COUNT)]
    foods = [create_food() for _ in range(FOOD_COUNT)]
    births = 0
    deaths = 0


def draw_stats():
    if agents:
        average_energy = sum(agent["energy"] for agent in agents) / len(agents)
        average_speed = sum(agent["speed"] for agent in agents) / len(agents)
        average_vision = sum(agent["vision_radius"] for agent in agents) / len(agents)
        average_energy_loss = sum(agent["energy_loss_rate"] for agent in agents) / len(agents)

        living_lineages = len(set(agent["lineage_id"] for agent in agents))
    else:
        average_energy = 0
        average_speed = 0
        average_vision = 0
        average_energy_loss = 0
        living_lineages = 0

    stats = [
        f"Population: {len(agents)}",
        f"Food: {len(foods)}",
        f"Average Energy: {average_energy:.1f}",
        f"Births: {births}",
        f"Deaths: {deaths}",
        f"Living Lineages: {living_lineages}",
        f"Hazard: {'ON' if hazard_enabled else 'OFF'}",
        "",
        "Traits:",
        f"Avg Speed: {average_speed:.2f}",
        f"Avg Vision: {average_vision:.1f}",
        f"Avg Energy Loss: {average_energy_loss:.3f}",
        "",
        "Controls:",
        "R = Reset",
        "H = Toggle hazard",
        "F = Add food",
        "G = Remove food"
    ]

    y = 10

    for stat in stats:
        text_surface = font.render(stat, True, TEXT_COLOR)
        screen.blit(text_surface, (10, y))
        y += 22


agents = []
foods = []
reset_simulation()

running = True

while running:

    screen.fill(BACKGROUND_COLOR)

    if hazard_enabled:
        pygame.draw.rect(screen, HAZARD_COLOR, HAZARD_ZONE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_simulation()

            if event.key == pygame.K_h:
                hazard_enabled = not hazard_enabled

            if event.key == pygame.K_f:
                for _ in range(5):
                    foods.append(create_food())

            if event.key == pygame.K_g:
                for _ in range(min(5, len(foods))):
                    foods.pop()

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

        if hazard_enabled and HAZARD_ZONE.collidepoint(agent_position):
            agent["energy"] -= HAZARD_ENERGY_LOSS_RATE
        else:
            agent["energy"] -= agent["energy_loss_rate"]

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

            if distance < closest_distance and distance < agent["vision_radius"]:
                closest_distance = distance
                closest_food = food

        if closest_food:
            direction_x = closest_food["x"] - agent["x"]
            direction_y = closest_food["y"] - agent["y"]
            agent["dx"], agent["dy"] = normalize_vector(
                direction_x,
                direction_y,
                agent["speed"]
            )
        else:
            if random.random() < 0.03:
                agent["dx"], agent["dy"] = random_velocity(agent["speed"])

        if hazard_enabled and HAZARD_ZONE.collidepoint(agent_position):
            agent["dx"] *= 0.95
            agent["dy"] *= 0.95

            if random.random() < 0.08:
                agent["dx"], agent["dy"] = random_velocity(agent["speed"])

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

            child = create_agent(child_x, child_y, parent=agent)
            child["energy"] = STARTING_ENERGY / 2

            newborn_agents.append(child)
            births += 1

        dynamic_radius = max(3, min(12, int(agent["energy"] / 15)))

        pygame.draw.circle(
            screen,
            agent["color"],
            (int(agent["x"]), int(agent["y"])),
            dynamic_radius
        )

    agents.extend(newborn_agents)

    draw_stats()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()