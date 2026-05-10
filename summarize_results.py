import pandas as pd

SIMULATION_LOG_FILE = "data/simulation_log.csv"
AGENT_LOG_FILE = "data/agent_log.csv"

simulation_data = pd.read_csv(SIMULATION_LOG_FILE)
agent_data = pd.read_csv(AGENT_LOG_FILE)

if simulation_data.empty:
    print("No simulation data found.")
    exit()

if agent_data.empty:
    print("No agent-level data found.")
    exit()


def print_section(title):
    print("\n" + title)
    print("-" * 60)


def summarize_group(label, group):
    if group.empty:
        print(f"{label}: No agents in this group.")
        return

    print(f"{label}")
    print(f"Count: {len(group)}")
    print(f"Avg Lifespan: {group['lifespan_seconds'].mean():.2f} seconds")
    print(f"Avg Speed: {group['speed'].mean():.3f}")
    print(f"Avg Vision Radius: {group['vision_radius'].mean():.3f}")
    print(f"Avg Energy Loss Rate: {group['energy_loss_rate'].mean():.5f}")
    print(f"Avg Food Eaten: {group['food_eaten'].mean():.2f}")
    print(f"Avg Birth Count: {group['birth_count'].mean():.2f}")
    print(f"Avg Final Energy: {group['final_energy'].mean():.2f}")


preset = simulation_data["preset"].iloc[0] if "preset" in simulation_data.columns else "unknown"

start_population = simulation_data["population"].iloc[0]
end_population = simulation_data["population"].iloc[-1]
max_population = simulation_data["population"].max()
min_population = simulation_data["population"].min()

final_births = simulation_data["births"].iloc[-1]
final_deaths = simulation_data["deaths"].iloc[-1]

start_energy = simulation_data["average_energy"].iloc[0]
end_energy = simulation_data["average_energy"].iloc[-1]
max_energy = simulation_data["average_energy"].max()
min_energy = simulation_data["average_energy"].min()

start_speed = simulation_data["average_speed"].iloc[0]
end_speed = simulation_data["average_speed"].iloc[-1]

start_vision = simulation_data["average_vision"].iloc[0]
end_vision = simulation_data["average_vision"].iloc[-1]

start_energy_loss = simulation_data["average_energy_loss"].iloc[0]
end_energy_loss = simulation_data["average_energy_loss"].iloc[-1]

start_lineages = simulation_data["living_lineages"].iloc[0]
end_lineages = simulation_data["living_lineages"].iloc[-1]

duration = simulation_data["time_seconds"].iloc[-1]

survivors = agent_data[agent_data["status"] == "survived"]
dead_agents = agent_data[agent_data["status"] == "died"]

print("\nAUTONOMOUS AGENT SANDBOX — EXPERIMENT SUMMARY")
print("=" * 60)

print(f"Preset: {preset}")
print(f"Duration: {duration:.1f} seconds")

print_section("Population")
print(f"Start Population: {start_population}")
print(f"End Population: {end_population}")
print(f"Max Population: {max_population}")
print(f"Min Population: {min_population}")

print_section("Births and Deaths")
print(f"Total Births: {final_births}")
print(f"Total Deaths: {final_deaths}")

print_section("Energy")
print(f"Start Avg Energy: {start_energy:.2f}")
print(f"End Avg Energy: {end_energy:.2f}")
print(f"Max Avg Energy: {max_energy:.2f}")
print(f"Min Avg Energy: {min_energy:.2f}")

print_section("Population-Level Trait Shift")
print(f"Avg Speed: {start_speed:.2f} → {end_speed:.2f}")
print(f"Avg Vision: {start_vision:.2f} → {end_vision:.2f}")
print(f"Avg Energy Loss: {start_energy_loss:.4f} → {end_energy_loss:.4f}")

print_section("Lineages")
print(f"Living Lineages: {start_lineages} → {end_lineages}")

if "lineage_id" in agent_data.columns:
    lineage_summary = (
        agent_data
        .groupby("lineage_id")
        .agg(
            total_agents=("agent_id", "count"),
            survivors=("status", lambda x: (x == "survived").sum()),
            deaths=("status", lambda x: (x == "died").sum()),
            avg_speed=("speed", "mean"),
            avg_vision=("vision_radius", "mean"),
            avg_energy_loss=("energy_loss_rate", "mean"),
            avg_food_eaten=("food_eaten", "mean"),
            avg_birth_count=("birth_count", "mean"),
            avg_lifespan=("lifespan_seconds", "mean")
        )
        .sort_values(by=["survivors", "total_agents"], ascending=False)
    )

    print("\nTop Lineages by Survivors")
    print("-" * 60)

    top_lineages = lineage_summary.head(5)

    for lineage_id, row in top_lineages.iterrows():
        print(
            f"Lineage {lineage_id}: "
            f"{int(row['survivors'])} survivors, "
            f"{int(row['deaths'])} deaths, "
            f"avg speed {row['avg_speed']:.2f}, "
            f"avg vision {row['avg_vision']:.1f}, "
            f"avg energy loss {row['avg_energy_loss']:.4f}"
        )

print_section("Survivor Trait Profile")
summarize_group("Surviving Agents", survivors)

print_section("Dead Agent Trait Profile")
summarize_group("Dead Agents", dead_agents)

print_section("Survivors vs Dead Agents")

if not survivors.empty and not dead_agents.empty:
    survivor_speed = survivors["speed"].mean()
    dead_speed = dead_agents["speed"].mean()

    survivor_vision = survivors["vision_radius"].mean()
    dead_vision = dead_agents["vision_radius"].mean()

    survivor_energy_loss = survivors["energy_loss_rate"].mean()
    dead_energy_loss = dead_agents["energy_loss_rate"].mean()

    survivor_food = survivors["food_eaten"].mean()
    dead_food = dead_agents["food_eaten"].mean()

    survivor_births = survivors["birth_count"].mean()
    dead_births = dead_agents["birth_count"].mean()

    print(f"Speed Difference: survivors {survivor_speed:.3f} vs dead {dead_speed:.3f}")
    print(f"Vision Difference: survivors {survivor_vision:.3f} vs dead {dead_vision:.3f}")
    print(f"Energy Loss Difference: survivors {survivor_energy_loss:.5f} vs dead {dead_energy_loss:.5f}")
    print(f"Food Eaten Difference: survivors {survivor_food:.2f} vs dead {dead_food:.2f}")
    print(f"Birth Count Difference: survivors {survivor_births:.2f} vs dead {dead_births:.2f}")
else:
    print("Not enough survivor/death contrast for comparison.")

print_section("Hazard Death Analysis")

if not dead_agents.empty and "died_in_hazard" in dead_agents.columns:
    hazard_deaths = dead_agents[dead_agents["died_in_hazard"] == True]
    hazard_death_rate = len(hazard_deaths) / len(dead_agents) * 100

    print(f"Deaths Inside Hazard: {len(hazard_deaths)}")
    print(f"Percent of Deaths Inside Hazard: {hazard_death_rate:.1f}%")
else:
    print("No dead agents recorded or hazard data unavailable.")

print_section("Interpretation")

if end_population > start_population:
    print("Population increased, suggesting the environment supported reproduction and survival.")
elif end_population < start_population:
    print("Population decreased, suggesting the environment applied strong survival pressure.")
else:
    print("Population stayed stable, suggesting a rough balance between survival and death.")

if end_energy > start_energy:
    print("Average energy increased, suggesting agents were generally successful at finding food.")
elif end_energy < start_energy:
    print("Average energy decreased, suggesting food access or environmental pressure was challenging.")
else:
    print("Average energy remained stable.")

if end_lineages < start_lineages:
    print("Some lineages disappeared, suggesting selection pressure favored certain inherited traits.")
else:
    print("Lineage diversity remained stable during this run.")

if not survivors.empty and not dead_agents.empty:
    if survivor_vision > dead_vision:
        print("Survivors had higher average vision, suggesting sensing range may have helped survival.")
    elif survivor_vision < dead_vision:
        print("Dead agents had higher average vision, suggesting vision alone was not enough to survive.")

    if survivor_energy_loss < dead_energy_loss:
        print("Survivors had lower energy loss rates, suggesting energy efficiency helped survival.")
    elif survivor_energy_loss > dead_energy_loss:
        print("Survivors had higher energy loss rates, suggesting other traits or food access mattered more.")

    if survivor_food > dead_food:
        print("Survivors ate more food on average, suggesting food access was a major survival factor.")