from pathlib import Path

import pandas as pd


VALIDATION_DIR = Path("validation_runs/v3.5_confidence_validation")
PRESETS = ["balanced", "scarce", "abundant", "harsh"]
MEANINGFUL_CONFIDENCE_DIFFERENCE = 0.02


def mean_or_none(frame, column):
    if frame.empty or column not in frame.columns:
        return None
    return frame[column].mean()


def format_number(value, decimals=2):
    if value is None or pd.isna(value):
        return "n/a"
    return f"{value:.{decimals}f}"


def load_preset_summary(preset):
    preset_dir = VALIDATION_DIR / preset
    simulation_file = preset_dir / "simulation_log.csv"
    agent_file = preset_dir / "agent_log.csv"

    if not simulation_file.exists() or not agent_file.exists():
        return None

    simulation_data = pd.read_csv(simulation_file)
    agent_data = pd.read_csv(agent_file)

    if simulation_data.empty or agent_data.empty:
        return None

    survivors = agent_data[agent_data["status"] == "survived"]
    dead_agents = agent_data[agent_data["status"] == "died"]

    survivor_confidence = mean_or_none(survivors, "average_selected_target_confidence")
    dead_confidence = mean_or_none(dead_agents, "average_selected_target_confidence")
    confidence_difference = (
        survivor_confidence - dead_confidence
        if survivor_confidence is not None and dead_confidence is not None
        else None
    )

    return {
        "preset": preset,
        "start_population": simulation_data["population"].iloc[0],
        "end_population": simulation_data["population"].iloc[-1],
        "population_change": simulation_data["population"].iloc[-1] - simulation_data["population"].iloc[0],
        "start_avg_energy": simulation_data["average_energy"].iloc[0],
        "end_avg_energy": simulation_data["average_energy"].iloc[-1],
        "survivor_selected_confidence": survivor_confidence,
        "dead_selected_confidence": dead_confidence,
        "confidence_difference": confidence_difference,
        "survivor_food_eaten": mean_or_none(survivors, "food_eaten"),
        "dead_food_eaten": mean_or_none(dead_agents, "food_eaten"),
        "survivor_energy_loss": mean_or_none(survivors, "energy_loss_rate"),
        "dead_energy_loss": mean_or_none(dead_agents, "energy_loss_rate"),
    }


def print_table(rows):
    headers = [
        "preset",
        "start pop",
        "end pop",
        "pop change",
        "start energy",
        "end energy",
        "surv conf",
        "dead conf",
        "conf diff",
        "surv food",
        "dead food",
        "surv loss",
        "dead loss",
    ]

    table_rows = []
    for row in rows:
        table_rows.append([
            row["preset"],
            str(int(row["start_population"])),
            str(int(row["end_population"])),
            f"{int(row['population_change']):+d}",
            format_number(row["start_avg_energy"]),
            format_number(row["end_avg_energy"]),
            format_number(row["survivor_selected_confidence"], 3),
            format_number(row["dead_selected_confidence"], 3),
            format_number(row["confidence_difference"], 3),
            format_number(row["survivor_food_eaten"]),
            format_number(row["dead_food_eaten"]),
            format_number(row["survivor_energy_loss"], 5),
            format_number(row["dead_energy_loss"], 5),
        ])

    widths = [
        max(len(header), *(len(row[index]) for row in table_rows))
        for index, header in enumerate(headers)
    ]

    header_line = " | ".join(header.ljust(widths[index]) for index, header in enumerate(headers))
    separator = "-+-".join("-" * width for width in widths)

    print(header_line)
    print(separator)
    for row in table_rows:
        print(" | ".join(value.ljust(widths[index]) for index, value in enumerate(row)))


def print_interpretation(rows):
    comparable_rows = [
        row for row in rows
        if row["confidence_difference"] is not None
    ]

    if not comparable_rows:
        print("\nInterpretation: Confidence comparison unavailable from the validation logs.")
        return

    strongest = max(comparable_rows, key=lambda row: row["confidence_difference"])
    meaningful = [
        row for row in comparable_rows
        if row["confidence_difference"] >= MEANINGFUL_CONFIDENCE_DIFFERENCE
    ]
    weak = [
        row for row in comparable_rows
        if abs(row["confidence_difference"]) < MEANINGFUL_CONFIDENCE_DIFFERENCE
    ]

    print("\nInterpretation")
    print("-" * 60)
    if meaningful:
        preset_names = ", ".join(row["preset"] for row in meaningful)
        print(f"Confidence mattered most in {strongest['preset']} (difference {strongest['confidence_difference']:.3f}).")
        print(f"Meaningful survivor confidence advantages appeared in: {preset_names}.")
    else:
        print("No preset showed a meaningful survivor selected-confidence advantage at the 0.020 threshold.")

    if weak:
        preset_names = ", ".join(row["preset"] for row in weak)
        print(f"Confidence differences were small in: {preset_names}, suggesting resource pressure, energy efficiency, food access, or other traits likely dominated.")


def main():
    rows = []
    missing = []

    for preset in PRESETS:
        row = load_preset_summary(preset)
        if row is None:
            missing.append(preset)
        else:
            rows.append(row)

    if not rows:
        print(f"No validation data found in {VALIDATION_DIR}.")
        return

    print("EvoSense v3.5 Validation Run Comparison")
    print("=" * 60)
    print_table(rows)
    print_interpretation(rows)

    if missing:
        print(f"\nMissing or unreadable presets: {', '.join(missing)}")


if __name__ == "__main__":
    main()
