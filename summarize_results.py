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

    if "risk_tolerance" in group.columns:
        print(f"Avg Risk Tolerance: {group['risk_tolerance'].mean():.3f}")

    if "sensor_noise" in group.columns:
        print(f"Avg Sensor Noise: {group['sensor_noise'].mean():.3f}")

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

if "average_risk_tolerance" in simulation_data.columns:
    start_risk = simulation_data["average_risk_tolerance"].iloc[0]
    end_risk = simulation_data["average_risk_tolerance"].iloc[-1]
    print(f"Avg Risk Tolerance: {start_risk:.3f} → {end_risk:.3f}")

if "average_sensor_noise" in simulation_data.columns:
    start_noise = simulation_data["average_sensor_noise"].iloc[0]
    end_noise = simulation_data["average_sensor_noise"].iloc[-1]
    print(f"Avg Sensor Noise: {start_noise:.3f} → {end_noise:.3f}")

print_section("Lineages")
print(f"Living Lineages: {start_lineages} → {end_lineages}")

if "lineage_id" in agent_data.columns:
    aggregation_fields = {
        "total_agents": ("agent_id", "count"),
        "survivors": ("status", lambda x: (x == "survived").sum()),
        "deaths": ("status", lambda x: (x == "died").sum()),
        "avg_speed": ("speed", "mean"),
        "avg_vision": ("vision_radius", "mean"),
        "avg_energy_loss": ("energy_loss_rate", "mean"),
        "avg_food_eaten": ("food_eaten", "mean"),
        "avg_birth_count": ("birth_count", "mean"),
        "avg_lifespan": ("lifespan_seconds", "mean")
    }

    if "risk_tolerance" in agent_data.columns:
        aggregation_fields["avg_risk_tolerance"] = ("risk_tolerance", "mean")

    if "sensor_noise" in agent_data.columns:
        aggregation_fields["avg_sensor_noise"] = ("sensor_noise", "mean")

    lineage_summary = (
        agent_data
        .groupby("lineage_id")
        .agg(**aggregation_fields)
        .sort_values(by=["survivors", "total_agents"], ascending=False)
    )

    print("\nTop Lineages by Survivors")
    print("-" * 60)

    top_lineages = lineage_summary.head(5)

    for lineage_id, row in top_lineages.iterrows():
        line = (
            f"Lineage {lineage_id}: "
            f"{int(row['survivors'])} survivors, "
            f"{int(row['deaths'])} deaths, "
            f"avg speed {row['avg_speed']:.2f}, "
            f"avg vision {row['avg_vision']:.1f}, "
            f"avg energy loss {row['avg_energy_loss']:.4f}"
        )

        if "avg_risk_tolerance" in row:
            line += f", avg risk {row['avg_risk_tolerance']:.3f}"

        if "avg_sensor_noise" in row:
            line += f", avg noise {row['avg_sensor_noise']:.3f}"

        print(line)

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

    if "risk_tolerance" in agent_data.columns:
        survivor_risk = survivors["risk_tolerance"].mean()
        dead_risk = dead_agents["risk_tolerance"].mean()
        print(f"Risk Tolerance Difference: survivors {survivor_risk:.3f} vs dead {dead_risk:.3f}")

    if "sensor_noise" in agent_data.columns:
        survivor_noise = survivors["sensor_noise"].mean()
        dead_noise = dead_agents["sensor_noise"].mean()
        print(f"Sensor Noise Difference: survivors {survivor_noise:.3f} vs dead {dead_noise:.3f}")
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

print_section("Sensor Noise Analysis")

if "sensor_noise" in agent_data.columns:
    lowest_noise_agents = agent_data.nsmallest(5, "sensor_noise")
    highest_noise_agents = agent_data.nlargest(5, "sensor_noise")

    print("Lowest-Noise Agents")
    print(f"Avg Lifespan: {lowest_noise_agents['lifespan_seconds'].mean():.2f} seconds")
    print(f"Avg Food Eaten: {lowest_noise_agents['food_eaten'].mean():.2f}")
    print(f"Avg Birth Count: {lowest_noise_agents['birth_count'].mean():.2f}")

    print("\nHighest-Noise Agents")
    print(f"Avg Lifespan: {highest_noise_agents['lifespan_seconds'].mean():.2f} seconds")
    print(f"Avg Food Eaten: {highest_noise_agents['food_eaten'].mean():.2f}")
    print(f"Avg Birth Count: {highest_noise_agents['birth_count'].mean():.2f}")

    if not survivors.empty and not dead_agents.empty:
        if survivor_noise < dead_noise:
            print("\nSurvivors had lower sensor noise on average, suggesting perception accuracy helped survival.")
        elif survivor_noise > dead_noise:
            print("\nSurvivors had higher sensor noise on average, suggesting other traits outweighed perception accuracy in this run.")
        else:
            print("\nSensor noise was similar between survivors and dead agents.")
else:
    print("Sensor noise data unavailable. Run the latest main.py first.")

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

    if "sensor_noise" in agent_data.columns:
        if survivor_noise < dead_noise:
            print("Lower sensor noise appears beneficial in this run, likely because more accurate perception improved food targeting.")
        elif survivor_noise > dead_noise:
            print("Higher sensor noise did not prevent survival in this run, suggesting environment layout or other traits were more important.")