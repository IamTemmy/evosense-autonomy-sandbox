import pygame
import random
import math
import csv
import os
import argparse
from collections import Counter

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

PRESETS = {
    "balanced": {
        "agent_count": 20,
        "food_count": 18,
        "hazard_energy_loss_rate": 0.35,
        "food_energy_gain": 24,
        "reproduction_energy": 160,
        "reproduction_cost": 70
    },
    "scarce": {
        "agent_count": 20,
        "food_count": 10,
        "hazard_energy_loss_rate": 0.35,
        "food_energy_gain": 18,
        "reproduction_energy": 170,
        "reproduction_cost": 75
    },
    "abundant": {
        "agent_count": 20,
        "food_count": 30,
        "hazard_energy_loss_rate": 0.25,
        "food_energy_gain": 30,
        "reproduction_energy": 145,
        "reproduction_cost": 60
    },
    "harsh": {
        "agent_count": 25,
        "food_count": 8,
        "hazard_energy_loss_rate": 0.55,
        "food_energy_gain": 16,
        "reproduction_energy": 180,
        "reproduction_cost": 85
    }
}

parser = argparse.ArgumentParser(description="Run the Autonomous Agent Sandbox simulation.")
parser.add_argument(
    "--preset",
    choices=PRESETS.keys(),
    default="balanced",
    help="Experiment preset to run: balanced, scarce, abundant, or harsh."
)

args = parser.parse_args()
EXPERIMENT_PRESET = args.preset
preset = PRESETS[EXPERIMENT_PRESET]

AGENT_COUNT = preset["agent_count"]
FOOD_COUNT = preset["food_count"]
MAX_AGENTS = 60

AGENT_RADIUS = 5
FOOD_RADIUS = 3
EAT_DISTANCE = 8

STARTING_ENERGY = 100
HAZARD_ENERGY_LOSS_RATE = preset["hazard_energy_loss_rate"]
FOOD_ENERGY_GAIN = preset["food_energy_gain"]
REPRODUCTION_ENERGY = preset["reproduction_energy"]
REPRODUCTION_COST = preset["reproduction_cost"]

MUTATION_RATE = 0.12
COLOR_MUTATION_RATE = 18

MIN_SPEED = 1.0
MAX_SPEED = 3.5
MIN_VISION_RADIUS = 60
MAX_VISION_RADIUS = 200
MIN_ENERGY_LOSS_RATE = 0.08
MAX_ENERGY_LOSS_RATE = 0.25
MIN_RISK_TOLERANCE = 0.10
MAX_RISK_TOLERANCE = 1.00
MIN_SENSOR_NOISE = 0.00
MAX_SENSOR_NOISE = 1.00

HAZARD_INFLUENCE_RADIUS = 120
MAX_POSITION_NOISE_PIXELS = 45

LOG_INTERVAL_FRAMES = 60
SIMULATION_LOG_FILE = "data/simulation_log.csv"
AGENT_LOG_FILE = "data/agent_log.csv"

BACKGROUND_COLOR = (20, 20, 20)
FOOD_COLOR = (255, 80, 80)
TEXT_COLOR = (230, 230, 230)
HAZARD_COLOR = (90, 20, 80)
SENSOR_COLOR = (120, 120, 120)

HAZARD_ZONE = pygame.Rect(300, 200, 200, 160)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autonomous Agent Sandbox")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

births = 0
deaths = 0
hazard_enabled = True
sensor_display_enabled = False
next_lineage_id = 1
next_agent_id = 1
frame_count = 0


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


def closest_point_on_rect(rect, x, y):
    closest_x = clamp(x, rect.left, rect.right)
    closest_y = clamp(y, rect.top, rect.bottom)
    return closest_x, closest_y


def distance_to_hazard(x, y):
    closest_x, closest_y = closest_point_on_rect(HAZARD_ZONE, x, y)
    return math.hypot(x - closest_x, y - closest_y)


def hazard_risk_at_point(x, y):
    if not hazard_enabled:
        return 0

    if HAZARD_ZONE.collidepoint(int(x), int(y)):
        return 1

    distance = distance_to_hazard(x, y)

    if distance >= HAZARD_INFLUENCE_RADIUS:
        return 0

    return 1 - (distance / HAZARD_INFLUENCE_RADIUS)


def create_food():
    while True:
        x = random.randint(FOOD_RADIUS, WIDTH - FOOD_RADIUS)
        y = random.randint(FOOD_RADIUS, HEIGHT - FOOD_RADIUS)

        if not hazard_enabled or not HAZARD_ZONE.collidepoint(x, y):
            return {"x": x, "y": y}


def perceive_food_position(agent, food):
    noise_strength = agent["sensor_noise"] * MAX_POSITION_NOISE_PIXELS

    perceived_x = food["x"] + random.gauss(0, noise_strength)
    perceived_y = food["y"] + random.gauss(0, noise_strength)

    perceived_x = clamp(perceived_x, 0, WIDTH)
    perceived_y = clamp(perceived_y, 0, HEIGHT)

    return perceived_x, perceived_y


def create_agent(x=None, y=None, parent=None):
    global next_lineage_id, next_agent_id

    if parent:
        speed = mutate(parent["speed"], MUTATION_RATE, MIN_SPEED, MAX_SPEED)
        vision_radius = mutate(parent["vision_radius"], 12, MIN_VISION_RADIUS, MAX_VISION_RADIUS)
        energy_loss_rate = mutate(parent["energy_loss_rate"], 0.015, MIN_ENERGY_LOSS_RATE, MAX_ENERGY_LOSS_RATE)
        risk_tolerance = mutate(parent["risk_tolerance"], 0.08, MIN_RISK_TOLERANCE, MAX_RISK_TOLERANCE)
        sensor_noise = mutate(parent["sensor_noise"], 0.08, MIN_SENSOR_NOISE, MAX_SENSOR_NOISE)

        color = mutate_color(parent["color"])
        lineage_id = parent["lineage_id"]
        parent_id = parent["agent_id"]

    else:
        speed = random.uniform(1.5, 2.5)
        vision_radius = random.uniform(90, 150)
        energy_loss_rate = random.uniform(0.11, 0.17)
        risk_tolerance = random.uniform(0.25, 0.75)
        sensor_noise = random.uniform(0.05, 0.45)

        color = random_agent_color()
        lineage_id = next_lineage_id
        next_lineage_id += 1
        parent_id = None

    dx, dy = random_velocity(speed)

    agent = {
        "agent_id": next_agent_id,
        "parent_id": parent_id,
        "lineage_id": lineage_id,
        "x": x if x is not None else random.randint(AGENT_RADIUS, WIDTH - AGENT_RADIUS),
        "y": y if y is not None else random.randint(AGENT_RADIUS, HEIGHT - AGENT_RADIUS),
        "dx": dx,
        "dy": dy,
        "energy": STARTING_ENERGY,
        "food_eaten": 0,
        "birth_count": 0,
        "speed": speed,
        "vision_radius": vision_radius,
        "energy_loss_rate": energy_loss_rate,
        "risk_tolerance": risk_tolerance,
        "sensor_noise": sensor_noise,
        "color": color,
        "birth_frame": frame_count
    }

    next_agent_id += 1
    return agent


def initialize_simulation_log_file():
    os.makedirs("data", exist_ok=True)

    with open(SIMULATION_LOG_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "frame",
            "time_seconds",
            "preset",
            "population",
            "food_count",
            "births",
            "deaths",
            "average_energy",
            "average_speed",
            "average_vision",
            "average_energy_loss",
            "average_risk_tolerance",
            "average_sensor_noise",
            "living_lineages",
            "hazard_enabled"
        ])


def initialize_agent_log_file():
    os.makedirs("data", exist_ok=True)

    with open(AGENT_LOG_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "agent_id",
            "parent_id",
            "lineage_id",
            "preset",
            "status",
            "birth_frame",
            "end_frame",
            "lifespan_seconds",
            "speed",
            "vision_radius",
            "energy_loss_rate",
            "risk_tolerance",
            "sensor_noise",
            "food_eaten",
            "birth_count",
            "final_energy",
            "death_x",
            "death_y",
            "died_in_hazard"
        ])


def log_agent(agent, status):
    agent_position = (int(agent["x"]), int(agent["y"]))
    died_in_hazard = hazard_enabled and HAZARD_ZONE.collidepoint(agent_position)

    with open(AGENT_LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            agent["agent_id"],
            agent["parent_id"],
            agent["lineage_id"],
            EXPERIMENT_PRESET,
            status,
            agent["birth_frame"],
            frame_count,
            round((frame_count - agent["birth_frame"]) / FPS, 2),
            round(agent["speed"], 3),
            round(agent["vision_radius"], 3),
            round(agent["energy_loss_rate"], 5),
            round(agent["risk_tolerance"], 3),
            round(agent["sensor_noise"], 3),
            agent["food_eaten"],
            agent["birth_count"],
            round(agent["energy"], 3),
            round(agent["x"], 2),
            round(agent["y"], 2),
            died_in_hazard
        ])


def log_surviving_agents():
    for agent in agents:
        log_agent(agent, "survived")


def reset_simulation():
    global agents, foods, births, deaths, next_lineage_id, next_agent_id, frame_count

    next_lineage_id = 1
    next_agent_id = 1
    births = 0
    deaths = 0
    frame_count = 0

    initialize_simulation_log_file()
    initialize_agent_log_file()

    agents = [create_agent() for _ in range(AGENT_COUNT)]
    foods = [create_food() for _ in range(FOOD_COUNT)]


def get_average_stats():
    if not agents:
        return {
            "average_energy": 0,
            "average_speed": 0,
            "average_vision": 0,
            "average_energy_loss": 0,
            "average_risk_tolerance": 0,
            "average_sensor_noise": 0,
            "living_lineages": 0
        }

    return {
        "average_energy": sum(agent["energy"] for agent in agents) / len(agents),
        "average_speed": sum(agent["speed"] for agent in agents) / len(agents),
        "average_vision": sum(agent["vision_radius"] for agent in agents) / len(agents),
        "average_energy_loss": sum(agent["energy_loss_rate"] for agent in agents) / len(agents),
        "average_risk_tolerance": sum(agent["risk_tolerance"] for agent in agents) / len(agents),
        "average_sensor_noise": sum(agent["sensor_noise"] for agent in agents) / len(agents),
        "living_lineages": len(set(agent["lineage_id"] for agent in agents))
    }


def log_simulation_data():
    stats = get_average_stats()

    with open(SIMULATION_LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            frame_count,
            round(frame_count / FPS, 2),
            EXPERIMENT_PRESET,
            len(agents),
            len(foods),
            births,
            deaths,
            round(stats["average_energy"], 3),
            round(stats["average_speed"], 3),
            round(stats["average_vision"], 3),
            round(stats["average_energy_loss"], 5),
            round(stats["average_risk_tolerance"], 3),
            round(stats["average_sensor_noise"], 3),
            stats["living_lineages"],
            hazard_enabled
        ])


def get_lineage_stats():
    if not agents:
        return []

    lineage_counts = Counter(agent["lineage_id"] for agent in agents)
    return lineage_counts.most_common(3)


def get_lineage_color(lineage_id):
    lineage_agents = [agent for agent in agents if agent["lineage_id"] == lineage_id]

    if not lineage_agents:
        return TEXT_COLOR

    red = int(sum(agent["color"][0] for agent in lineage_agents) / len(lineage_agents))
    green = int(sum(agent["color"][1] for agent in lineage_agents) / len(lineage_agents))
    blue = int(sum(agent["color"][2] for agent in lineage_agents) / len(lineage_agents))

    return (red, green, blue)


def choose_best_food(agent):
    best_food = None
    best_score = float("-inf")

    for food in foods:
        actual_distance = math.hypot(food["x"] - agent["x"], food["y"] - agent["y"])

        if actual_distance > agent["vision_radius"]:
            continue

        perceived_x, perceived_y = perceive_food_position(agent, food)
        perceived_distance = math.hypot(perceived_x - agent["x"], perceived_y - agent["y"])

        distance_score = 1 - clamp(perceived_distance / agent["vision_radius"], 0, 1)
        risk_score = hazard_risk_at_point(perceived_x, perceived_y)
        risk_penalty = risk_score * (1 - agent["risk_tolerance"])

        energy_urgency = 1 - clamp(agent["energy"] / STARTING_ENERGY, 0, 1)
        hunger_bonus = energy_urgency * 0.4

        score = distance_score + hunger_bonus - risk_penalty

        if score > best_score:
            best_score = score
            best_food = {
                "actual": food,
                "perceived_x": perceived_x,
                "perceived_y": perceived_y
            }

    return best_food


def apply_hazard_avoidance(agent, move_x, move_y):
    if not hazard_enabled:
        return move_x, move_y

    hazard_distance = distance_to_hazard(agent["x"], agent["y"])
    agent_position = (int(agent["x"]), int(agent["y"]))

    cautious_detection_radius = HAZARD_INFLUENCE_RADIUS * (1.2 - agent["risk_tolerance"])

    if HAZARD_ZONE.collidepoint(agent_position):
        avoid_x = agent["x"] - HAZARD_ZONE.centerx
        avoid_y = agent["y"] - HAZARD_ZONE.centery
        avoid_strength = 3.0 * (1.2 - agent["risk_tolerance"])

        avoid_dx, avoid_dy = normalize_vector(avoid_x, avoid_y, avoid_strength)
        move_x += avoid_dx
        move_y += avoid_dy

    elif hazard_distance < cautious_detection_radius:
        hazard_x, hazard_y = closest_point_on_rect(HAZARD_ZONE, agent["x"], agent["y"])

        avoid_x = agent["x"] - hazard_x
        avoid_y = agent["y"] - hazard_y

        proximity_factor = 1 - (hazard_distance / cautious_detection_radius)
        caution_factor = 1 - agent["risk_tolerance"]

        avoid_strength = 2.5 * proximity_factor * caution_factor

        if avoid_strength > 0:
            avoid_dx, avoid_dy = normalize_vector(avoid_x, avoid_y, avoid_strength)
            move_x += avoid_dx
            move_y += avoid_dy

    return move_x, move_y


def draw_stats():
    stats_data = get_average_stats()

    stats = [
        f"Preset: {EXPERIMENT_PRESET}",
        f"Population: {len(agents)}",
        f"Food: {len(foods)}",
        f"Average Energy: {stats_data['average_energy']:.1f}",
        f"Births: {births}",
        f"Deaths: {deaths}",
        f"Living Lineages: {stats_data['living_lineages']}",
        f"Hazard: {'ON' if hazard_enabled else 'OFF'}",
        f"Sensors: {'ON' if sensor_display_enabled else 'OFF'}",
        f"Time: {frame_count / FPS:.1f}s",
        "",
        "Traits:",
        f"Avg Speed: {stats_data['average_speed']:.2f}",
        f"Avg Vision: {stats_data['average_vision']:.1f}",
        f"Avg Energy Loss: {stats_data['average_energy_loss']:.3f}",
        f"Avg Risk Tolerance: {stats_data['average_risk_tolerance']:.2f}",
        f"Avg Sensor Noise: {stats_data['average_sensor_noise']:.2f}",
        "",
        "Top Lineages:"
    ]

    y = 10

    for stat in stats:
        text_surface = font.render(stat, True, TEXT_COLOR)
        screen.blit(text_surface, (10, y))
        y += 22

    for lineage_id, count in get_lineage_stats():
        lineage_color = get_lineage_color(lineage_id)

        pygame.draw.rect(screen, lineage_color, (10, y + 4, 14, 14))

        text_surface = font.render(
            f"Lineage {lineage_id}: {count} agents",
            True,
            TEXT_COLOR
        )

        screen.blit(text_surface, (32, y))
        y += 22

    control_lines = [
        "",
        "Controls:",
        "R = Reset",
        "H = Toggle hazard",
        "S = Toggle sensors",
        "F = Add food",
        "G = Remove food"
    ]

    for line in control_lines:
        text_surface = font.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (10, y))
        y += 22


agents = []
foods = []
reset_simulation()

running = True

while running:

    frame_count += 1

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

            if event.key == pygame.K_s:
                sensor_display_enabled = not sensor_display_enabled

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
            log_agent(agent, "died")
            agents.remove(agent)
            deaths += 1
            continue

        target_food = choose_best_food(agent)

        move_x = agent["dx"]
        move_y = agent["dy"]

        if target_food:
            direction_x = target_food["perceived_x"] - agent["x"]
            direction_y = target_food["perceived_y"] - agent["y"]

            food_dx, food_dy = normalize_vector(
                direction_x,
                direction_y,
                agent["speed"]
            )

            move_x += food_dx
            move_y += food_dy
        else:
            if random.random() < 0.03:
                move_x, move_y = random_velocity(agent["speed"])

        move_x, move_y = apply_hazard_avoidance(agent, move_x, move_y)

        agent["dx"], agent["dy"] = normalize_vector(
            move_x,
            move_y,
            agent["speed"]
        )

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
            agent["birth_count"] += 1

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

        if sensor_display_enabled:
            pygame.draw.circle(
                screen,
                SENSOR_COLOR,
                (int(agent["x"]), int(agent["y"])),
                int(agent["vision_radius"]),
                1
            )

        dynamic_radius = max(3, min(12, int(agent["energy"] / 15)))

        pygame.draw.circle(
            screen,
            agent["color"],
            (int(agent["x"]), int(agent["y"])),
            dynamic_radius
        )

    agents.extend(newborn_agents)

    if frame_count % LOG_INTERVAL_FRAMES == 0:
        log_simulation_data()

    draw_stats()

    pygame.display.flip()
    clock.tick(FPS)

log_surviving_agents()
pygame.quit()