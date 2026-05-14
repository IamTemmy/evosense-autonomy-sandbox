import pygame

from config import (
    AGENT_RADIUS,
    BACKGROUND_COLOR,
    FOOD_COLOR,
    FOOD_RADIUS,
    FPS,
    HAZARD_COLOR,
    HAZARD_ZONE,
    HEIGHT,
    SENSOR_COLOR,
    TEXT_COLOR,
    WIDTH,
)


def initialize_display():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Autonomous Agent Sandbox")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)
    return screen, clock, font


def draw_background(environment, screen):
    screen.fill(BACKGROUND_COLOR)

    if environment.hazard_enabled:
        pygame.draw.rect(screen, HAZARD_COLOR, HAZARD_ZONE)


def draw_foods(environment, screen):
    for food in environment.foods:
        pygame.draw.circle(
            screen,
            FOOD_COLOR,
            (food["x"], food["y"]),
            FOOD_RADIUS
        )


def draw_agent(environment, screen, agent):
    if environment.sensor_display_enabled:
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


def draw_stats(environment, screen, font):
    stats_data = environment.get_average_stats()

    stats = [
        f"Preset: {environment.preset_name}",
        f"Population: {len(environment.agents)}",
        f"Food: {len(environment.foods)}",
        f"Average Energy: {stats_data['average_energy']:.1f}",
        f"Births: {environment.births}",
        f"Deaths: {environment.deaths}",
        f"Living Lineages: {stats_data['living_lineages']}",
        f"Hazard: {'ON' if environment.hazard_enabled else 'OFF'}",
        f"Sensors: {'ON' if environment.sensor_display_enabled else 'OFF'}",
        f"Time: {environment.frame_count / FPS:.1f}s",
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

    for lineage_id, count in environment.get_lineage_stats():
        lineage_color = environment.get_lineage_color(lineage_id)

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
