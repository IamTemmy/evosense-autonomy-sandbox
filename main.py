import argparse

import pygame

from config import FPS, PRESETS
from environment import SimulationEnvironment
from logging_system import log_surviving_agents
from visualization import (
    draw_agent,
    draw_background,
    draw_foods,
    draw_stats,
    initialize_display,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Run the Autonomous Agent Sandbox simulation.")
    parser.add_argument(
        "--preset",
        choices=PRESETS.keys(),
        default="balanced",
        help="Experiment preset to run: balanced, scarce, abundant, or harsh."
    )
    return parser.parse_args()


def handle_events(environment):
    running = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                environment.reset()

            if event.key == pygame.K_h:
                environment.toggle_hazard()

            if event.key == pygame.K_s:
                environment.toggle_sensor_display()

            if event.key == pygame.K_f:
                environment.add_food()

            if event.key == pygame.K_g:
                environment.remove_food()

    return running


def run():
    args = parse_args()
    screen, clock, font = initialize_display()

    environment = SimulationEnvironment(args.preset, PRESETS[args.preset])
    environment.reset()

    running = True

    while running:
        environment.begin_frame()

        draw_background(environment, screen)
        running = handle_events(environment)
        draw_foods(environment, screen)

        for agent in environment.update_agents():
            draw_agent(environment, screen, agent)

        environment.log_frame_if_due()
        draw_stats(environment, screen, font)

        pygame.display.flip()
        clock.tick(FPS)

    log_surviving_agents(environment)
    pygame.quit()


if __name__ == "__main__":
    run()
