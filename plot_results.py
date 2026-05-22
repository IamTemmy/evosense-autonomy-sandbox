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

plt.figure(figsize=(10, 5))
plt.plot(data["time_seconds"], data["population"])
plt.title(f"Population Over Time - Preset: {preset_name}")
plt.xlabel("Time (seconds)")
plt.ylabel("Population")
plt.grid(True)
plt.savefig(f"{PLOTS_FOLDER}/population_plot.png")
plt.close()

plt.figure(figsize=(10, 5))
plt.plot(data["time_seconds"], data["average_energy"])
plt.title(f"Average Energy Over Time - Preset: {preset_name}")
plt.xlabel("Time (seconds)")
plt.ylabel("Average Energy")
plt.grid(True)
plt.savefig(f"{PLOTS_FOLDER}/energy_plot.png")
plt.close()

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

plt.figure(figsize=(10, 5))
plt.plot(data["time_seconds"], data["average_speed"], label="Speed")
plt.plot(data["time_seconds"], data["average_vision"], label="Vision Radius")
plt.plot(data["time_seconds"], data["average_energy_loss"], label="Energy Loss")
if "average_risk_tolerance" in data.columns:
    plt.plot(data["time_seconds"], data["average_risk_tolerance"], label="Risk Tolerance")
if "average_sensor_noise" in data.columns:
    plt.plot(data["time_seconds"], data["average_sensor_noise"], label="Sensor Noise")
if "average_uncertainty_tolerance" in data.columns:
    plt.plot(data["time_seconds"], data["average_uncertainty_tolerance"], label="Uncertainty Tolerance")
plt.title(f"Trait Evolution Over Time - Preset: {preset_name}")
plt.xlabel("Time (seconds)")
plt.ylabel("Trait Value")
plt.legend()
plt.grid(True)
plt.savefig(f"{PLOTS_FOLDER}/trait_evolution_plot.png")
plt.close()

if "average_sensor_noise" in data.columns:
    plt.figure(figsize=(10, 5))
    plt.plot(data["time_seconds"], data["average_sensor_noise"])
    plt.title(f"Average Sensor Noise Over Time - Preset: {preset_name}")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Average Sensor Noise")
    plt.grid(True)
    plt.savefig(f"{PLOTS_FOLDER}/sensor_noise_plot.png")
    plt.close()

if (
    "average_perception_confidence" in data.columns
    and "average_selected_target_confidence" in data.columns
):
    plt.figure(figsize=(10, 5))
    plt.plot(data["time_seconds"], data["average_perception_confidence"], label="Avg Perceived Food Confidence")
    plt.plot(data["time_seconds"], data["average_selected_target_confidence"], label="Avg Selected Target Confidence")
    plt.title(f"Confidence-Aware Foraging Over Time - Preset: {preset_name}")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Confidence")
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{PLOTS_FOLDER}/confidence_foraging_plot.png")
    plt.close()

if (
    "low_confidence_decisions" in data.columns
    and "high_confidence_decisions" in data.columns
):
    plt.figure(figsize=(10, 5))
    plt.plot(data["time_seconds"], data["low_confidence_decisions"], label="Low Confidence Decisions")
    plt.plot(data["time_seconds"], data["high_confidence_decisions"], label="High Confidence Decisions")
    plt.title(f"Confidence Decision Counts - Preset: {preset_name}")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Cumulative Decisions")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{PLOTS_FOLDER}/confidence_decisions_plot.png")
    plt.close()

if (
    "total_hazard_exposure_steps" in data.columns
    and "total_hazard_energy_penalty" in data.columns
):
    plt.figure(figsize=(10, 5))
    plt.plot(data["time_seconds"], data["total_hazard_exposure_steps"], label="Cumulative Exposure Steps")
    plt.plot(data["time_seconds"], data["total_hazard_energy_penalty"], label="Cumulative Energy Penalty")
    plt.title(f"Hazard Exposure Over Time - Preset: {preset_name}")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Cumulative Total")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{PLOTS_FOLDER}/hazard_exposure_plot.png")
    plt.close()

print("Plots generated successfully.")
print(f"Preset: {preset_name}")
print(f"Saved in: {PLOTS_FOLDER}/")
