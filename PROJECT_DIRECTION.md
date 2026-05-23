# EvoSense: Bio-Inspired Autonomy Sandbox - Project Direction and Development Roadmap

## Purpose

This document defines the project identity, boundaries, development roadmap, and final portfolio direction for EvoSense.

## 1. Project Identity

EvoSense is a lightweight Python/Pygame simulation for studying how simple agents adapt survival behavior under energy pressure, environmental hazards, imperfect sensing, and inherited traits.

The project uses a biological survival metaphor: agents seek food, avoid hazards, lose energy, reproduce, mutate, and form lineages.

Beneath that biological framing, EvoSense explores engineering-relevant autonomy concepts such as perception uncertainty, risk-aware decision-making, adaptive behavior, sensor limitations, and telemetry-driven analysis.

EvoSense is a bio-inspired autonomy sandbox, not a vehicle autonomy simulator.

## 2. One-Sentence Description

EvoSense is an interpretable bio-inspired autonomy simulation where evolving agents learn to survive under risk, energy pressure, sensor noise, and environmental uncertainty.

## 3. What This Project Is

- A bio-inspired autonomy simulation.
- An agent-based modeling project.
- A portfolio project for demonstrating engineering thinking around autonomy, uncertainty, and adaptive behavior.
- A lightweight experimentation framework for testing how simple decision rules affect survival and population behavior.
- A project that prioritizes interpretability, documentation, and measurable behavior over unnecessary complexity.

## 4. What This Project Is Not

- Not a vehicle autonomy simulator.
- Not a neural network or deep reinforcement learning project.
- Not a polished commercial game.
- Not a full robotics stack.
- Not a project meant to simulate realistic biology in scientific detail.

The biological setting is a metaphor for autonomy under uncertainty. It provides an accessible way to study agents that must act with limited information, incomplete sensing, risk exposure, and resource constraints.

## 5. Motivation and Engineering Relevance

Real autonomous systems rarely operate with perfect information. Robots, drones, embedded devices, autonomous vehicles, and sensor-driven systems must make decisions using noisy measurements, incomplete environmental knowledge, uncertain risk, and limited resources.

EvoSense simplifies those ideas into an interpretable simulation. Instead of modeling a full robotics or vehicle autonomy stack, it focuses on the decision-making pressures that appear across many autonomous systems: what an agent can sense, what it cannot know, what risk it should tolerate, and how its behavior changes survival outcomes over time.

## 6. Current System Capabilities

### Environment and Simulation

- Pygame-based simulation loop.
- Food spawning.
- Hazard zone.
- Agent movement.
- Energy loss.
- Agent death and reproduction.
- Multiple experiment presets such as balanced, scarce, abundant, and harsh.

### Agent Behavior

- Food seeking.
- Risk-aware target selection.
- Hazard avoidance.
- Trait-based behavior.
- Mutation and inheritance.
- Behavior influenced by speed, vision radius, energy loss rate, risk tolerance, and sensor noise.

### Bio-Inspired Evolution

- Agent IDs.
- Parent IDs.
- Lineage IDs.
- Trait inheritance.
- Trait mutation.
- Population changes over time.
- Survival pressure through energy depletion and environmental hazards.

### Autonomy and Perception

- Sensor radius.
- Sensor visualization.
- Sensor noise.
- Imperfect food perception through Gaussian position error.
- Confidence-aware food selection.
- Uncertainty tolerance.
- Risk-aware behavior around hazardous regions.

### Analytics and Interpretability

- CSV logging.
- Population plots.
- Energy plots.
- Birth/death tracking.
- Trait evolution plots.
- Sensor noise plots.
- Confidence-aware foraging plots.
- Hazard-death metrics.
- Hazard exposure metrics.
- Memory-guided foraging metrics.
- Summary reports.
- Modular architecture and documentation.

## 7. Core Technical Themes

- Imperfect Perception
- Risk-Aware Decision-Making
- Energy-Constrained Survival
- Evolutionary Adaptation
- Telemetry-Driven Interpretation
- Lightweight Modularity

## 8. Design Philosophy

- Engineering realism over flashy features.
- Interpretability over black-box complexity.
- One meaningful autonomy layer at a time.
- Clear documentation after every major feature.
- Simple, readable code.
- Measurable behavior through logs and plots.
- Smooth GitHub portfolio experience.

Guiding question:

> What autonomy concept does this add, and how will we measure its effect?

## 9. Development Boundaries

Before v4.0, the project should avoid:

- Deep reinforcement learning.
- Neural networks.
- Complex 3D graphics.
- Vehicle physics.
- Overly realistic biological modeling.
- Large external dependencies.
- Cloud backends.
- Complicated database systems.
- Fancy dashboards before the core simulation and metrics are complete.

These boundaries keep EvoSense focused on interpretable autonomy concepts, clear telemetry, and a stable portfolio-quality simulation.

## 10. Version Roadmap

### v1.0 - Basic Agent Simulation

Initial simulation foundation with moving agents, food, energy loss, survival pressure, and a Pygame loop.

### v2.0 - Evolutionary Behavior and Lineage

Trait inheritance, mutation, reproduction, parent tracking, lineage tracking, and population changes over time.

### v3.0 - Risk-Aware Survival

Hazard-aware behavior, risk tolerance, and decision rules that force agents to balance food rewards against environmental danger.

### v3.1 - Sensor Noise and Imperfect Perception

Noisy sensing added to make agent perception imperfect rather than fully reliable.

### v3.2 - Sensor Noise Analytics

Logging and plotting support for analyzing how sensor noise affects survival, energy, targeting behavior, and population outcomes.

### v3.3 - Sensor Noise Visualization

Visual simulation support for showing sensor radius, imperfect perception, and the difference between actual and perceived information.

### v3.4 - Modular Architecture Refactor

Code organization improvements that separate simulation configuration, environment logic, agent behavior, visualization, logging, plotting, and summary reporting.

### v3.5 - Confidence-Aware Foraging

Implemented feature. Agents estimate confidence in perceived food locations and use that confidence when selecting targets under noise, distance, energy pressure, and hazard risk.

### v3.5.1 - Validation Interpretation Cleanup

Implemented feature. Validation comparison and summary interpretation were updated to avoid overstating confidence effects and to clarify that zero hazard deaths do not prove hazards had no effect.

### v3.5.2 - Hazard Exposure Analytics

Implemented feature. The hazard zone now logs exposure steps, accumulated hazard energy penalties, hazard entries, and survivor-versus-dead exposure comparisons so hazard effects can be measured even when agents leave the hazard before dying.

### v3.6 - Agent Memory of Risk and Reward

Implemented feature. Agents use bounded recent memory of successful food locations and hazardous exposure locations as modest scoring factors when selecting future food targets.

### v3.7 - Experiment Comparison Mode

Planned feature. The project should support clearer comparison between experiment presets, runs, and behavioral configurations.

### v4.0 - Portfolio Release

Planned release. The project should be stable, well documented, easy to run, visually demonstrable, and positioned clearly as a bio-inspired autonomy sandbox.

## 11. v3.5 Feature Definition: Confidence-Aware Foraging

Confidence-Aware Foraging is implemented in v3.5.

Agents should not only perceive food with noisy sensors. They should estimate how confident they are in what they perceive.

Agents should balance:

- Distance to food.
- Sensor noise.
- Vision radius.
- Hazard risk.
- Risk tolerance.
- Confidence in perceived food location.

Potential metrics:

- Average perception confidence.
- Confidence of selected food target.
- Low-confidence decisions.
- High-confidence decisions.
- Relationship between confidence, survival, and reproduction.

The goal is to add a clear autonomy concept without turning the project into a black-box learning system. Confidence should be measurable, logged, and explainable.

## 12. Target Audience

Primary:

- Technical recruiters.
- Engineering hiring managers.
- Internship interviewers.
- GitHub visitors evaluating project quality.
- The project author's future self when explaining the work in interviews.

Secondary:

- Professors.
- Research mentors.
- Classmates.
- Collaborators.

## 13. GitHub Positioning

Recommended public-facing project name:

EvoSense: Bio-Inspired Autonomy Sandbox

Recommended repository name:

evosense-autonomy-sandbox

Recommended subtitle:

An interpretable simulation of evolving agents adapting under risk, energy pressure, sensor noise, and environmental uncertainty.

## 14. Resume Positioning

Potential resume bullet:

Built EvoSense, a modular Python/Pygame bio-inspired autonomy sandbox that simulates evolving agents under sensor noise, energy pressure, and environmental hazards; implemented risk-aware behavior, mutation and lineage tracking, telemetry logging, and visualization tools to analyze adaptive decision-making under uncertainty.

Shorter version:

Built a Python/Pygame bio-inspired autonomy simulator with evolving agents, sensor noise, risk-aware behavior, lineage tracking, telemetry logging, and performance visualization.

## 15. Final Success Criteria

- Clear name and identity.
- Polished README.
- Stable run commands.
- Clean modular code.
- At least three meaningful experiment presets.
- Logs capturing population, trait, lineage, sensor, and risk behavior.
- Plots explaining simulation behavior.
- Summary script translating raw logs into interpretation.
- Demo screenshot or GIF.
- Final roadmap section.
- Concise resume bullet.
- Clear distinction from future vehicle/robotics autonomy projects.

## 16. Strategic Direction Going Forward

EvoSense should continue as a bio-inspired autonomy sandbox.

A separate future project should focus on vehicle/robotics autonomy, including path planning, obstacle avoidance, sensor fusion, localization, and control.

Together, they can show both conceptual autonomy thinking and applied engineering implementation. EvoSense should remain focused on interpretable autonomy under uncertainty, while a future robotics or vehicle autonomy project can demonstrate applied control, planning, and systems integration.

## File Created

Created `PROJECT_DIRECTION.md` as the project direction and development roadmap for EvoSense. No Python files or README content were modified.
