import os
import pandas as pd
import matplotlib.pyplot as plt

LOG_FILE = "data/simulation_log.csv"
PLOTS_FOLDER = "plots"

os.makedirs(PLOTS_FOLDER, exist_ok=True)

data = pd.read_csv(LOG_FILE)

if "preset" in data.columns and len(data["preset"]) > 0:
    preset_name = data["preset"].iloc[0]
else:
    preset_name = "unknown"

# -----------------------------
# Population Plot
# -----------------------------
plt.figure(figsize=(10, 5))
plt.plot(data["time_seconds"], data["population"])
plt.title(f"Population Over Time - Preset: {preset_name}")
plt.xlabel("Time (seconds)")
plt.ylabel("Population")
plt.grid(True)

plt.savefig(f"{PLOTS_FOLDER}/population_plot.png")
plt.close()

# -----------------------------
# Energy Plot
# -----------------------------
plt.figure(figsize=(10, 5))
plt.plot(data["time_seconds"], data["average_energy"])
plt.title(f"Average Energy Over Time - Preset: {preset_name}")
plt.xlabel("Time (seconds)")
plt.ylabel("Average Energy")
plt.grid(True)

plt.savefig(f"{PLOTS_FOLDER}/energy_plot.png")
plt.close()

# -----------------------------
# Births and Deaths Plot
# -----------------------------
plt.figure(figsize=(10, 5))
plt.plot(data["time_seconds"], data["births"], label="Births")
plt.plot(data["time_seconds"], data["deaths"], label="Deaths")

plt.title(f"Births and Deaths Over Time - Preset: {preset_name}")
plt.xlabel("Time (seconds)")
plt.ylabel("Count")
plt.legend()
plt.grid(True)

plt.savefig(f"{PLOTS_FOLDER}/births_deaths_plot.png")
plt.close()

# -----------------------------
# Trait Evolution Plot
# -----------------------------
plt.figure(figsize=(10, 5))

plt.plot(data["time_seconds"], data["average_speed"], label="Speed")
plt.plot(data["time_seconds"], data["average_vision"], label="Vision Radius")
plt.plot(data["time_seconds"], data["average_energy_loss"], label="Energy Loss")

plt.title(f"Trait Evolution Over Time - Preset: {preset_name}")
plt.xlabel("Time (seconds)")
plt.ylabel("Trait Value")
plt.legend()
plt.grid(True)

plt.savefig(f"{PLOTS_FOLDER}/trait_evolution_plot.png")
plt.close()

print("Plots generated successfully.")
print(f"Preset: {preset_name}")
print(f"Saved in: {PLOTS_FOLDER}/")