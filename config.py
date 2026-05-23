import pygame


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

MAX_AGENTS = 60

AGENT_RADIUS = 5
FOOD_RADIUS = 3
EAT_DISTANCE = 8

STARTING_ENERGY = 100

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
MIN_UNCERTAINTY_TOLERANCE = 0.00
MAX_UNCERTAINTY_TOLERANCE = 1.00

HAZARD_INFLUENCE_RADIUS = 120
MAX_POSITION_NOISE_PIXELS = 45
LOW_CONFIDENCE_THRESHOLD = 0.50
MEMORY_ENABLED = True
MAX_MEMORY_EVENTS = 12
MEMORY_REWARD_WEIGHT = 0.25
MEMORY_RISK_WEIGHT = 0.30
MEMORY_DECAY_DISTANCE = 120

LOG_INTERVAL_FRAMES = 60
SIMULATION_LOG_FILE = "data/simulation_log.csv"
AGENT_LOG_FILE = "data/agent_log.csv"

BACKGROUND_COLOR = (20, 20, 20)
FOOD_COLOR = (255, 80, 80)
TEXT_COLOR = (230, 230, 230)
HAZARD_COLOR = (90, 20, 80)
SENSOR_COLOR = (120, 120, 120)

HAZARD_ZONE = pygame.Rect(300, 200, 200, 160)
