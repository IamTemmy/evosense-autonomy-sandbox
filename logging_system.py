import csv
import os

from config import AGENT_LOG_FILE, FPS, HAZARD_ZONE, SIMULATION_LOG_FILE


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


def log_agent(environment, agent, status):
    agent_position = (int(agent["x"]), int(agent["y"]))
    died_in_hazard = environment.hazard_enabled and HAZARD_ZONE.collidepoint(agent_position)

    with open(AGENT_LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            agent["agent_id"],
            agent["parent_id"],
            agent["lineage_id"],
            environment.preset_name,
            status,
            agent["birth_frame"],
            environment.frame_count,
            round((environment.frame_count - agent["birth_frame"]) / FPS, 2),
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


def log_surviving_agents(environment):
    for agent in environment.agents:
        log_agent(environment, agent, "survived")


def log_simulation_data(environment):
    stats = environment.get_average_stats()

    with open(SIMULATION_LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            environment.frame_count,
            round(environment.frame_count / FPS, 2),
            environment.preset_name,
            len(environment.agents),
            len(environment.foods),
            environment.births,
            environment.deaths,
            round(stats["average_energy"], 3),
            round(stats["average_speed"], 3),
            round(stats["average_vision"], 3),
            round(stats["average_energy_loss"], 5),
            round(stats["average_risk_tolerance"], 3),
            round(stats["average_sensor_noise"], 3),
            stats["living_lineages"],
            environment.hazard_enabled
        ])
