import math
import random

from config import (
    AGENT_RADIUS,
    COLOR_MUTATION_RATE,
    HAZARD_INFLUENCE_RADIUS,
    HAZARD_ZONE,
    HEIGHT,
    MAX_ENERGY_LOSS_RATE,
    MAX_POSITION_NOISE_PIXELS,
    MAX_RISK_TOLERANCE,
    MAX_SENSOR_NOISE,
    MAX_SPEED,
    MAX_UNCERTAINTY_TOLERANCE,
    MAX_VISION_RADIUS,
    MIN_ENERGY_LOSS_RATE,
    MIN_RISK_TOLERANCE,
    MIN_SENSOR_NOISE,
    MIN_SPEED,
    MIN_UNCERTAINTY_TOLERANCE,
    MIN_VISION_RADIUS,
    MUTATION_RATE,
    STARTING_ENERGY,
    LOW_CONFIDENCE_THRESHOLD,
    WIDTH,
)


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


def hazard_risk_at_point(environment, x, y):
    if not environment.hazard_enabled:
        return 0

    if HAZARD_ZONE.collidepoint(int(x), int(y)):
        return 1

    distance = distance_to_hazard(x, y)

    if distance >= HAZARD_INFLUENCE_RADIUS:
        return 0

    return 1 - (distance / HAZARD_INFLUENCE_RADIUS)


def perceive_food_position(agent, food):
    noise_strength = agent["sensor_noise"] * MAX_POSITION_NOISE_PIXELS

    perceived_x = food["x"] + random.gauss(0, noise_strength)
    perceived_y = food["y"] + random.gauss(0, noise_strength)

    perceived_x = clamp(perceived_x, 0, WIDTH)
    perceived_y = clamp(perceived_y, 0, HEIGHT)

    return perceived_x, perceived_y


def compute_food_confidence(environment, agent, perceived_x, perceived_y, perceived_distance):
    distance_factor = 1 - clamp(perceived_distance / agent["vision_radius"], 0, 1)
    noise_factor = 1 - clamp(agent["sensor_noise"] / MAX_SENSOR_NOISE, 0, 1)
    hazard_factor = 1 - hazard_risk_at_point(environment, perceived_x, perceived_y)

    confidence = (
        distance_factor * 0.45
        + noise_factor * 0.35
        + hazard_factor * 0.20
    )

    return clamp(confidence, 0, 1)


def record_food_perception(agent, confidence_values, selected_confidence):
    if confidence_values:
        agent["perception_confidence_total"] += sum(confidence_values)
        agent["perception_count"] += len(confidence_values)

    if selected_confidence is None:
        agent["last_selected_confidence"] = None
        return

    agent["selected_confidence_total"] += selected_confidence
    agent["selected_target_count"] += 1
    agent["last_selected_confidence"] = selected_confidence

    if selected_confidence < LOW_CONFIDENCE_THRESHOLD:
        agent["low_confidence_decisions"] += 1
    else:
        agent["high_confidence_decisions"] += 1


def create_agent(environment, x=None, y=None, parent=None):
    if parent:
        speed = mutate(parent["speed"], MUTATION_RATE, MIN_SPEED, MAX_SPEED)
        vision_radius = mutate(parent["vision_radius"], 12, MIN_VISION_RADIUS, MAX_VISION_RADIUS)
        energy_loss_rate = mutate(parent["energy_loss_rate"], 0.015, MIN_ENERGY_LOSS_RATE, MAX_ENERGY_LOSS_RATE)
        risk_tolerance = mutate(parent["risk_tolerance"], 0.08, MIN_RISK_TOLERANCE, MAX_RISK_TOLERANCE)
        sensor_noise = mutate(parent["sensor_noise"], 0.08, MIN_SENSOR_NOISE, MAX_SENSOR_NOISE)
        uncertainty_tolerance = mutate(
            parent["uncertainty_tolerance"],
            0.08,
            MIN_UNCERTAINTY_TOLERANCE,
            MAX_UNCERTAINTY_TOLERANCE
        )

        color = mutate_color(parent["color"])
        lineage_id = parent["lineage_id"]
        parent_id = parent["agent_id"]

    else:
        speed = random.uniform(1.5, 2.5)
        vision_radius = random.uniform(90, 150)
        energy_loss_rate = random.uniform(0.11, 0.17)
        risk_tolerance = random.uniform(0.25, 0.75)
        sensor_noise = random.uniform(0.05, 0.45)
        uncertainty_tolerance = random.uniform(0.20, 0.80)

        color = random_agent_color()
        lineage_id = environment.next_lineage_id
        environment.next_lineage_id += 1
        parent_id = None

    dx, dy = random_velocity(speed)

    agent = {
        "agent_id": environment.next_agent_id,
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
        "uncertainty_tolerance": uncertainty_tolerance,
        "perception_confidence_total": 0,
        "perception_count": 0,
        "selected_confidence_total": 0,
        "selected_target_count": 0,
        "last_selected_confidence": None,
        "low_confidence_decisions": 0,
        "high_confidence_decisions": 0,
        "hazard_exposure_steps": 0,
        "total_hazard_energy_penalty": 0,
        "times_entered_hazard": 0,
        "currently_inside_hazard": False,
        "color": color,
        "birth_frame": environment.frame_count
    }

    environment.next_agent_id += 1
    return agent


def choose_best_food(environment, agent):
    best_food = None
    best_score = float("-inf")
    perceived_confidences = []
    selected_confidence = None

    for food in environment.foods:
        actual_distance = math.hypot(food["x"] - agent["x"], food["y"] - agent["y"])

        if actual_distance > agent["vision_radius"]:
            continue

        perceived_x, perceived_y = perceive_food_position(agent, food)
        perceived_distance = math.hypot(perceived_x - agent["x"], perceived_y - agent["y"])

        distance_score = 1 - clamp(perceived_distance / agent["vision_radius"], 0, 1)
        risk_score = hazard_risk_at_point(environment, perceived_x, perceived_y)
        risk_penalty = risk_score * (1 - agent["risk_tolerance"])
        confidence = compute_food_confidence(
            environment,
            agent,
            perceived_x,
            perceived_y,
            perceived_distance
        )
        uncertainty_penalty = (1 - confidence) * (1 - agent["uncertainty_tolerance"]) * 0.8
        confidence_reward = confidence * 0.6
        perceived_confidences.append(confidence)

        energy_urgency = 1 - clamp(agent["energy"] / STARTING_ENERGY, 0, 1)
        hunger_bonus = energy_urgency * 0.4

        score = distance_score + confidence_reward + hunger_bonus - risk_penalty - uncertainty_penalty

        if score > best_score:
            best_score = score
            selected_confidence = confidence
            best_food = {
                "actual": food,
                "perceived_x": perceived_x,
                "perceived_y": perceived_y,
                "confidence": confidence
            }

    record_food_perception(agent, perceived_confidences, selected_confidence)

    if selected_confidence is not None:
        if selected_confidence < LOW_CONFIDENCE_THRESHOLD:
            environment.low_confidence_decisions += 1
        else:
            environment.high_confidence_decisions += 1

    return best_food


def apply_hazard_avoidance(environment, agent, move_x, move_y):
    if not environment.hazard_enabled:
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
