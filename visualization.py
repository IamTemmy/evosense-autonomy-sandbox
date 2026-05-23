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
    pygame.display.set_caption("EvoSense")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)
    return screen, clock, font


def draw_background(environment, screen):
    screen.fill(BACKGROUND_COLOR)

    if environment.hazard_enabled:
        pygame.draw.rect(screen, HAZARD_COLOR, HAZARD_ZONE)


def draw_foods(environment, screen):
    for food in environment.foods:
        x = int(food["x"])
        y = int(food["y"])

        pygame.draw.polygon(
            screen,
            FOOD_COLOR,
            [
                (x, y - FOOD_RADIUS - 1),
                (x + FOOD_RADIUS + 1, y),
                (x, y + FOOD_RADIUS + 1),
                (x - FOOD_RADIUS - 1, y),
            ]
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
    confidence_decisions = (
        stats_data["low_confidence_decisions"]
        + stats_data["high_confidence_decisions"]
    )
    low_confidence_rate = (
        stats_data["low_confidence_decisions"] / confidence_decisions * 100
        if confidence_decisions
        else 0
    )

    left_stats = [
        f"Preset: {environment.preset_name}",
        f"Population: {len(environment.agents)}",
        f"Food: {len(environment.foods)}",
        f"Avg Energy: {stats_data['average_energy']:.1f}",
        f"Births: {environment.births}",
        f"Deaths: {environment.deaths}",
        f"Lineages: {stats_data['living_lineages']}",
        f"Hazard: {'ON' if environment.hazard_enabled else 'OFF'}",
        f"Sensors: {'ON' if environment.sensor_display_enabled else 'OFF'}",
        f"Time: {environment.frame_count / FPS:.1f}s",
    ]

    right_stats = [
        "Traits",
        f"Avg Speed: {stats_data['average_speed']:.2f}",
        f"Avg Vision: {stats_data['average_vision']:.1f}",
        f"Energy Loss: {stats_data['average_energy_loss']:.3f}",
        f"Risk Tol: {stats_data['average_risk_tolerance']:.2f}",
        f"Sensor Noise: {stats_data['average_sensor_noise']:.2f}",
        f"Avg Confidence: {stats_data['average_selected_target_confidence']:.2f}",
        f"Low-Conf Rate: {low_confidence_rate:.0f}%",
        f"Avg Hazard Exp: {stats_data['average_hazard_exposure_steps']:.1f}",
        f"Avg Memory Use: {stats_data['average_memory_influenced_decisions']:.1f}",
        "",
        "Top Lineages"
    ]

    def draw_lines(lines, x, y, line_height=19):
        for line in lines:
            text_surface = font.render(line, True, TEXT_COLOR)
            screen.blit(text_surface, (x, y))
            y += line_height
        return y

    draw_lines(left_stats, 10, 10)
    y = draw_lines(right_stats, 560, 10)

    for lineage_id, count in environment.get_lineage_stats():
        lineage_color = environment.get_lineage_color(lineage_id)

        pygame.draw.rect(screen, lineage_color, (560, y + 3, 12, 12))

        text_surface = font.render(
            f"Lineage {lineage_id}: {count} agents",
            True,
            TEXT_COLOR
        )

        screen.blit(text_surface, (578, y))
        y += 19

    control_lines = [
        "Controls",
        "R = Reset",
        "H = Toggle hazard",
        "S = Toggle sensors",
        "F = Add food",
        "G = Remove food"
    ]

    draw_lines(control_lines, 10, HEIGHT - 120)
