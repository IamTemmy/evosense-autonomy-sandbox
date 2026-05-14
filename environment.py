import math
import random
from collections import Counter

from agents import (
    apply_hazard_avoidance,
    choose_best_food,
    create_agent,
    normalize_vector,
    random_velocity,
)
from config import (
    AGENT_RADIUS,
    EAT_DISTANCE,
    FOOD_RADIUS,
    HEIGHT,
    HAZARD_ZONE,
    LOG_INTERVAL_FRAMES,
    MAX_AGENTS,
    STARTING_ENERGY,
    TEXT_COLOR,
    WIDTH,
)
from logging_system import (
    initialize_agent_log_file,
    initialize_simulation_log_file,
    log_agent,
    log_simulation_data,
)


class SimulationEnvironment:
    def __init__(self, preset_name, preset):
        self.preset_name = preset_name
        self.agent_count = preset["agent_count"]
        self.food_count = preset["food_count"]
        self.hazard_energy_loss_rate = preset["hazard_energy_loss_rate"]
        self.food_energy_gain = preset["food_energy_gain"]
        self.reproduction_energy = preset["reproduction_energy"]
        self.reproduction_cost = preset["reproduction_cost"]

        self.births = 0
        self.deaths = 0
        self.hazard_enabled = True
        self.sensor_display_enabled = False
        self.next_lineage_id = 1
        self.next_agent_id = 1
        self.frame_count = 0
        self.agents = []
        self.foods = []

    def reset(self):
        self.next_lineage_id = 1
        self.next_agent_id = 1
        self.births = 0
        self.deaths = 0
        self.frame_count = 0

        initialize_simulation_log_file()
        initialize_agent_log_file()

        self.agents = [create_agent(self) for _ in range(self.agent_count)]
        self.foods = [self.create_food() for _ in range(self.food_count)]

    def create_food(self):
        while True:
            x = random.randint(FOOD_RADIUS, WIDTH - FOOD_RADIUS)
            y = random.randint(FOOD_RADIUS, HEIGHT - FOOD_RADIUS)

            if not self.hazard_enabled or not HAZARD_ZONE.collidepoint(x, y):
                return {"x": x, "y": y}

    def toggle_hazard(self):
        self.hazard_enabled = not self.hazard_enabled

    def toggle_sensor_display(self):
        self.sensor_display_enabled = not self.sensor_display_enabled

    def add_food(self, amount=5):
        for _ in range(amount):
            self.foods.append(self.create_food())

    def remove_food(self, amount=5):
        for _ in range(min(amount, len(self.foods))):
            self.foods.pop()

    def get_average_stats(self):
        if not self.agents:
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
            "average_energy": sum(agent["energy"] for agent in self.agents) / len(self.agents),
            "average_speed": sum(agent["speed"] for agent in self.agents) / len(self.agents),
            "average_vision": sum(agent["vision_radius"] for agent in self.agents) / len(self.agents),
            "average_energy_loss": sum(agent["energy_loss_rate"] for agent in self.agents) / len(self.agents),
            "average_risk_tolerance": sum(agent["risk_tolerance"] for agent in self.agents) / len(self.agents),
            "average_sensor_noise": sum(agent["sensor_noise"] for agent in self.agents) / len(self.agents),
            "living_lineages": len(set(agent["lineage_id"] for agent in self.agents))
        }

    def get_lineage_stats(self):
        if not self.agents:
            return []

        lineage_counts = Counter(agent["lineage_id"] for agent in self.agents)
        return lineage_counts.most_common(3)

    def get_lineage_color(self, lineage_id):
        lineage_agents = [agent for agent in self.agents if agent["lineage_id"] == lineage_id]

        if not lineage_agents:
            return TEXT_COLOR

        red = int(sum(agent["color"][0] for agent in lineage_agents) / len(lineage_agents))
        green = int(sum(agent["color"][1] for agent in lineage_agents) / len(lineage_agents))
        blue = int(sum(agent["color"][2] for agent in lineage_agents) / len(lineage_agents))

        return (red, green, blue)

    def begin_frame(self):
        self.frame_count += 1

    def update_agents(self):
        newborn_agents = []
        drawable_agents = []

        for agent in self.agents[:]:
            if self.update_agent(agent, newborn_agents):
                drawable_agents.append(agent)

        self.agents.extend(newborn_agents)
        return drawable_agents

    def update_agent(self, agent, newborn_agents):
        agent_position = (int(agent["x"]), int(agent["y"]))

        if self.hazard_enabled and HAZARD_ZONE.collidepoint(agent_position):
            agent["energy"] -= self.hazard_energy_loss_rate
        else:
            agent["energy"] -= agent["energy_loss_rate"]

        if agent["energy"] <= 0:
            log_agent(self, agent, "died")
            self.agents.remove(agent)
            self.deaths += 1
            return False

        target_food = choose_best_food(self, agent)

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

        move_x, move_y = apply_hazard_avoidance(self, agent, move_x, move_y)

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

        self.resolve_food_collisions(agent)
        self.reproduce_if_ready(agent, newborn_agents)
        return True

    def resolve_food_collisions(self, agent):
        for food in self.foods[:]:
            distance = math.hypot(
                agent["x"] - food["x"],
                agent["y"] - food["y"]
            )

            if distance < EAT_DISTANCE:
                self.foods.remove(food)
                self.foods.append(self.create_food())

                agent["food_eaten"] += 1
                agent["energy"] += self.food_energy_gain

    def reproduce_if_ready(self, agent, newborn_agents):
        if agent["energy"] >= self.reproduction_energy and len(self.agents) + len(newborn_agents) < MAX_AGENTS:
            agent["energy"] -= self.reproduction_cost
            agent["birth_count"] += 1

            child_x = max(
                AGENT_RADIUS,
                min(WIDTH - AGENT_RADIUS, agent["x"] + random.randint(-15, 15))
            )

            child_y = max(
                AGENT_RADIUS,
                min(HEIGHT - AGENT_RADIUS, agent["y"] + random.randint(-15, 15))
            )

            child = create_agent(self, child_x, child_y, parent=agent)
            child["energy"] = STARTING_ENERGY / 2

            newborn_agents.append(child)
            self.births += 1

    def log_frame_if_due(self):
        if self.frame_count % LOG_INTERVAL_FRAMES == 0:
            log_simulation_data(self)
