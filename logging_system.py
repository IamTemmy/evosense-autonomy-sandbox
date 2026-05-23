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
            "average_uncertainty_tolerance",
            "average_perception_confidence",
            "average_selected_target_confidence",
            "low_confidence_decisions",
            "high_confidence_decisions",
            "living_lineages",
            "total_hazard_exposure_steps",
            "average_hazard_exposure_steps",
            "total_hazard_energy_penalty",
            "average_hazard_energy_penalty",
            "total_hazard_entries",
            "agents_inside_hazard",
            "average_memory_influenced_decisions",
            "average_memory_reward_score",
            "average_memory_risk_score",
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
            "uncertainty_tolerance",
            "food_eaten",
            "birth_count",
            "final_energy",
            "death_x",
            "death_y",
            "died_in_hazard",
            "hazard_exposure_steps",
            "total_hazard_energy_penalty",
            "times_entered_hazard",
            "average_perception_confidence",
            "average_selected_target_confidence",
            "low_confidence_decisions",
            "high_confidence_decisions",
            "memory_influenced_decisions",
            "average_memory_reward_score",
            "average_memory_risk_score",
            "food_memory_size",
            "hazard_memory_size"
        ])


def log_agent(environment, agent, status):
    agent_position = (int(agent["x"]), int(agent["y"]))
    died_in_hazard = environment.hazard_enabled and HAZARD_ZONE.collidepoint(agent_position)
    average_perception_confidence = (
        agent["perception_confidence_total"] / agent["perception_count"]
        if agent["perception_count"]
        else 0
    )
    average_selected_target_confidence = (
        agent["selected_confidence_total"] / agent["selected_target_count"]
        if agent["selected_target_count"]
        else 0
    )
    average_memory_reward_score = (
        agent["memory_reward_score"] / agent["memory_influenced_decisions"]
        if agent["memory_influenced_decisions"]
        else 0
    )
    average_memory_risk_score = (
        agent["memory_risk_score"] / agent["memory_influenced_decisions"]
        if agent["memory_influenced_decisions"]
        else 0
    )

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
            round(agent["uncertainty_tolerance"], 3),
            agent["food_eaten"],
            agent["birth_count"],
            round(agent["energy"], 3),
            round(agent["x"], 2),
            round(agent["y"], 2),
            died_in_hazard,
            agent["hazard_exposure_steps"],
            round(agent["total_hazard_energy_penalty"], 3),
            agent["times_entered_hazard"],
            round(average_perception_confidence, 3),
            round(average_selected_target_confidence, 3),
            agent["low_confidence_decisions"],
            agent["high_confidence_decisions"],
            agent["memory_influenced_decisions"],
            round(average_memory_reward_score, 3),
            round(average_memory_risk_score, 3),
            len(agent["food_memory"]),
            len(agent["hazard_memory"])
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
            round(stats["average_uncertainty_tolerance"], 3),
            round(stats["average_perception_confidence"], 3),
            round(stats["average_selected_target_confidence"], 3),
            stats["low_confidence_decisions"],
            stats["high_confidence_decisions"],
            stats["living_lineages"],
            stats["total_hazard_exposure_steps"],
            round(stats["average_hazard_exposure_steps"], 3),
            round(stats["total_hazard_energy_penalty"], 3),
            round(stats["average_hazard_energy_penalty"], 3),
            stats["total_hazard_entries"],
            stats["agents_inside_hazard"],
            round(stats["average_memory_influenced_decisions"], 3),
            round(stats["average_memory_reward_score"], 3),
            round(stats["average_memory_risk_score"], 3),
            environment.hazard_enabled
        ])
