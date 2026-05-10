import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autonomous Agent Sandbox")

clock = pygame.time.Clock()

agents = []

for i in range(20):
    agents.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(-2, 2),
        random.randint(-2, 2)
    ])

running = True

while running:

    screen.fill((20, 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for agent in agents:

        agent[0] += agent[2]
        agent[1] += agent[3]

        if agent[0] <= 0 or agent[0] >= WIDTH:
            agent[2] *= -1

        if agent[1] <= 0 or agent[1] >= HEIGHT:
            agent[3] *= -1

        pygame.draw.circle(screen, (0, 255, 100), (agent[0], agent[1]), 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()