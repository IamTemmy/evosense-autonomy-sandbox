# EvoSense: Bio-Inspired Autonomy Sandbox

An interpretable simulation of evolving agents adapting under risk, energy pressure, sensor noise, and environmental uncertainty.

---

## Project Identity

EvoSense is a lightweight Python/Pygame simulation for studying how simple agents adapt survival behavior under energy pressure, environmental hazards, imperfect sensing, and inherited traits.

The project uses a biological survival metaphor: agents seek food, avoid hazards, lose energy, reproduce, mutate, and form lineages. Beneath that biological framing, EvoSense explores engineering-relevant autonomy concepts such as perception uncertainty, risk-aware decision-making, adaptive behavior, sensor limitations, and telemetry-driven analysis.

The recommended repository name for a future GitHub rename is:

```text
evosense-autonomy-sandbox
```

EvoSense should be understood as a bio-inspired autonomy sandbox, not a vehicle autonomy simulator. A separate future project can focus directly on vehicle or robotics autonomy.

---

## What This Project Is

* A bio-inspired autonomy simulation.
* An agent-based modeling project.
* A portfolio project for demonstrating engineering thinking around autonomy, uncertainty, and adaptive behavior.
* A lightweight experimentation framework for testing how simple decision rules affect survival and population behavior.
* A project that prioritizes interpretability, documentation, and measurable behavior over unnecessary complexity.

---

## What This Project Is Not

* Not a vehicle autonomy simulator.
* Not a neural network or deep reinforcement learning project.
* Not a polished commercial game.
* Not a full robotics stack.
* Not a project meant to simulate realistic biology in scientific detail.

---

## Design Philosophy

* Engineering realism over flashy features.
* Interpretability over black-box complexity.
* One meaningful autonomy layer at a time.
* Clear documentation after every major feature.
* Simple, readable code.
* Measurable behavior through logs and plots.

---

## Current Features

### Environment and Simulation

* Configurable environment presets.
* Food/resource spawning.
* Hazard zones.
* Environmental pressure through scarcity, hazards, and energy loss.
* Reset and runtime controls for simulation interaction.

### Agent Behavior

* Independent agents with position, velocity, and energy.
* Dynamic movement behavior.
* Food/resource seeking.
* Energy-based survival.
* Reproduction system.
* Hazard avoidance movement.
* Risk-aware food selection.
* Confidence-aware foraging.

### Bio-Inspired Evolution

* Inheritable traits.
* Trait mutation across generations.
* Speed variation.
* Vision radius variation.
* Energy efficiency variation.
* Risk tolerance variation.
* Uncertainty tolerance variation.
* Lineage tracking.
* Emergent survival strategies.

### Autonomy and Perception

* Vision radius sensing.
* Sensor noise.
* Imperfect perception.
* Interpretable food-location confidence scores.
* Sensor visualization mode.
* Environmental awareness.
* Risk-based movement logic.
* Navigation under uncertainty.

### Analytics and Interpretability

* Simulation logging.
* Agent-level telemetry.
* Population analysis.
* Trait analysis.
* Survival summaries.
* Birth and death metrics.
* Lineage analysis.
* Sensor noise analysis.
* Confidence-aware foraging analysis.
* Hazard exposure analytics.
* Memory-guided foraging analysis.
* v3.5.1 validation comparison and more cautious confidence/hazard interpretation.
* Plot generation.

---

## Core Concepts

### Energy Pressure

Agents lose energy as they move and survive by finding food. This creates a simple but measurable pressure that shapes survival, reproduction, and population behavior.

### Environmental Risk

Hazards introduce danger into the environment. Agents must balance the reward of nearby resources against the risk of entering or approaching hazardous regions.

Hazard analysis now tracks exposure, not only deaths that occur inside the hazard zone. Agent logs include time spent in the hazard, accumulated hazard energy penalty, and hazard entries so delayed hazard effects can be inspected.

### Imperfect Sensing

Agents do not operate with perfect knowledge. Vision radius and sensor noise create perception limits that affect food targeting, hazard avoidance, and survival outcomes.

### Confidence-Aware Foraging

Agents estimate confidence for perceived food targets using distance, sensor noise, and hazard proximity. Food selection balances distance, confidence, hazard risk, risk tolerance, and an inherited uncertainty-tolerance trait.

### Agent Memory of Risk and Reward

Agents keep bounded recent memory of food locations where they succeeded and hazard locations where they were exposed. Food selection now includes a modest memory reward near recent successful food areas and a modest memory risk penalty near remembered hazardous areas.

### Inherited Traits

Agents pass traits to offspring with mutation. Over time, population behavior can shift as different trait combinations survive under different environmental presets.

### Telemetry-Driven Analysis

The project records population trends, energy values, trait distributions, survival outcomes, lineage data, sensor-noise effects, and confidence-aware foraging metrics so behavior can be inspected after each run.

---

## Experiment Presets

### Balanced

General-purpose environment with moderate:

* Food availability.
* Hazard pressure.
* Reproduction difficulty.

### Scarce

Resource-limited environment.

Encourages:

* Competition.
* Efficient navigation.
* Conservative behavior.

### Abundant

High-resource environment.

Encourages:

* Rapid reproduction.
* Larger populations.
* Reduced survival pressure.

### Harsh

High-risk environment.

Encourages:

* Strong survival pressure.
* Risk-sensitive navigation.
* Efficient energy usage.

---

## Running the Simulation

### Run Balanced Preset

```bash
python3 main.py --preset balanced
```

### Run Scarce Preset

```bash
python3 main.py --preset scarce
```

### Run Abundant Preset

```bash
python3 main.py --preset abundant
```

### Run Harsh Preset

```bash
python3 main.py --preset harsh
```

---

## Generate Experiment Plots

```bash
python3 plot_results.py
```

---

## Generate Experiment Summary

```bash
python3 summarize_results.py
```

### Compare v3.5 Validation Presets

```bash
python3 compare_validation_runs.py
```

---

## Controls

| Key | Action                      |
| --- | --------------------------- |
| R   | Reset simulation            |
| H   | Toggle hazard zone          |
| S   | Toggle sensor visualization |
| F   | Add food                    |
| G   | Remove food                 |

---

## Version Roadmap

* v1.0 — Basic Agent Simulation
* v2.0 — Evolutionary Behavior and Lineage
* v3.0 — Risk-Aware Survival
* v3.1 — Sensor Noise and Imperfect Perception
* v3.2 — Sensor Noise Analytics
* v3.3 — Sensor Noise Visualization
* v3.4 — Modular Architecture Refactor
* v3.5 — Confidence-Aware Foraging (implemented)
* v3.5.1 — Validation Interpretation Cleanup (implemented)
* v3.5.2 — Hazard Exposure Analytics (implemented)
* v3.6 — Agent Memory of Risk and Reward (implemented)
* v3.7 — Experiment Comparison Mode
* v4.0 — Portfolio Release

---

## Current Architecture

The project has been refactored into multiple files to improve readability, maintainability, and engineering structure.

### `main.py`

Main simulation entry point.

Responsible for:

* Parsing command-line preset arguments.
* Initializing the simulation.
* Running the main loop.
* Coordinating agents, environment, logging, and visualization.

### `config.py`

Stores shared configuration values.

Includes:

* Screen size.
* Frame rate.
* Experiment presets.
* Agent constants.
* Mutation limits.
* Colors.
* File paths.

### `agents.py`

Handles agent behavior and traits.

Includes:

* Agent creation.
* Trait inheritance.
* Mutation.
* Sensor noise.
* Uncertainty tolerance.
* Risk-aware food selection.
* Confidence-aware food selection.
* Memory-guided food selection.
* Hazard avoidance movement.

### `environment.py`

Handles environment-related logic.

Includes:

* Food creation.
* Hazard calculations.
* Hazard risk estimation.
* Environment geometry helpers.

### `logging_system.py`

Handles experiment telemetry.

Includes:

* Simulation log initialization.
* Agent log initialization.
* Population-level logging.
* Agent-level survival/death logging.
* Hazard exposure and penalty telemetry.
* Memory-guided foraging telemetry.

### `visualization.py`

Handles rendering and dashboard display.

Includes:

* Drawing agents.
* Drawing food.
* Drawing hazards.
* Drawing sensor radius overlays.
* Drawing simulation statistics.

### `plot_results.py`

Generates visual plots from simulation logs.

Includes:

* Population plots.
* Energy plots.
* Births/deaths plots.
* Trait evolution plots.
* Sensor noise plots.
* Confidence-aware foraging plots.
* Hazard exposure plots.
* Memory-guided foraging plots.

### `summarize_results.py`

Generates a terminal-based experiment summary.

Includes:

* Population analysis.
* Survivor vs dead-agent comparison.
* Lineage analysis.
* Sensor noise analysis.
* Confidence-aware foraging analysis.
* Hazard exposure analysis.
* Interpretation of experiment outcomes.

---

## Repository Structure

```text
evosense-autonomy-sandbox/
|
├── main.py
├── config.py
├── agents.py
├── environment.py
├── logging_system.py
├── visualization.py
├── plot_results.py
├── summarize_results.py
├── data/
├── plots/
├── README.md
└── .gitignore
```

---

## Future Direction

EvoSense will remain focused on bio-inspired autonomy: simple agents, interpretable rules, imperfect sensing, environmental risk, energy pressure, inherited traits, and measurable population behavior.

A separate future project can focus directly on vehicle or robotics autonomy with domain-specific concerns such as maps, trajectories, controllers, sensors, planning stacks, and hardware-oriented constraints. Keeping that work separate allows EvoSense to stay lightweight, readable, and focused on the survival metaphor that makes its behavior easy to inspect.

Near-term EvoSense development should continue adding one meaningful autonomy layer at a time, with documentation and analytics updated after each major feature.
