# Autonomous Agent Sandbox

A lightweight simulation framework for studying autonomous-agent behavior under environmental constraints, imperfect sensing, adaptive traits, and risk-aware navigation.

---

## Overview

Autonomous Agent Sandbox is an experimental simulation platform designed to model how independent agents behave inside constrained environments.

The project began as a simple survival and adaptation simulation inspired by biological systems. Over time, it evolved into a broader autonomy systems sandbox focused on engineering-oriented concepts such as:

* Sensor-driven behavior
* Environmental risk assessment
* Energy-aware navigation
* Autonomous decision-making
* Adaptive trait evolution
* Experiment telemetry and analytics
* Navigation under uncertainty

The purpose of the project is not to recreate a full autonomous vehicle stack or a commercial robotics simulator. Instead, the goal is to study and visualize foundational principles that appear in real-world autonomy systems at a smaller and understandable scale.

The simulation serves as a controlled environment where agent behavior, sensing limitations, environmental pressure, and navigation strategies can be explored experimentally.

---

# Project Identity

Autonomous Agent Sandbox is now positioned as:

> A lightweight simulation framework for studying autonomous-agent behavior, environmental constraints, sensor-driven navigation, and adaptive decision-making.

The project draws inspiration from engineering domains including:

* Autonomous vehicles
* Robotics
* Swarm systems
* Embedded sensing systems
* Navigation under uncertainty
* Adaptive decision architectures
* Resource-constrained autonomous systems

As the project evolves, new features are evaluated based on whether they represent meaningful autonomy or systems-engineering concepts rather than purely visual or game-like additions.

---

# Core Engineering Concepts

The project focuses on several engineering principles commonly found in autonomous systems.

## 1. Environmental Constraints

Agents operate inside environments containing:

* Limited resources
* Hazardous regions
* Energy constraints
* Competition for survival

This models how autonomous systems must function within imperfect and constrained real-world environments.

---

## 2. Sensor-Driven Behavior

Agents rely on sensing ranges to detect resources and navigate the environment.

The simulation models:

* Detection radius
* Sensor limitations
* Imperfect perception
* Environmental awareness

This parallels how robotics and autonomous systems depend on sensor inputs such as:

* Cameras
* Radar
* LiDAR
* GPS
* Embedded sensing systems

---

## 3. Risk-Aware Navigation

Agents evaluate:

* Resource reward
* Hazard proximity
* Survival tradeoffs
* Energy efficiency

This approximates real-world autonomous decision-making where systems balance:

* Safety
* Efficiency
* Speed
* Navigation quality
* Energy usage

---

## 4. Adaptive Traits

Agents possess inheritable traits such as:

* Speed
* Vision radius
* Energy efficiency
* Risk tolerance

Traits mutate across generations, allowing different behavioral strategies to emerge over time.

This models adaptive behavior systems and evolutionary optimization concepts.

---

## 5. Telemetry and Experimentation

The system records:

* Population changes
* Energy trends
* Trait evolution
* Survival statistics
* Birth and death metrics
* Lineage information
* Agent-level data

This creates an experimentation workflow similar to simulation and analytics pipelines used in engineering research.

---

# Current Features

## Agent Simulation

* Independent autonomous agents
* Dynamic movement behavior
* Food/resource seeking
* Energy-based survival
* Reproduction system
* Trait inheritance and mutation

---

## Environmental Systems

* Hazard zones
* Configurable environments
* Resource spawning
* Environmental pressure
* Risk-aware navigation

---

## Sensor Systems

* Vision radius sensing
* Sensor visualization mode
* Environmental awareness
* Risk-based movement logic

---

## Adaptive Systems

* Evolutionary trait mutation
* Risk tolerance behavior
* Emergent survival strategies
* Lineage tracking

---

## Data Logging and Analytics

* Simulation logging
* Agent-level telemetry
* Population analysis
* Trait analysis
* Survival summaries
* Plot generation

---

# Current Architecture

The project currently operates through several primary systems.

## Simulation Engine

Handles:

* Frame updates
* Agent movement
* Environment interaction
* Rendering
* Event handling

---

## Agent System

Each agent contains:

* Position
* Velocity
* Energy
* Sensor radius
* Risk tolerance
* Movement logic
* Evolutionary traits

---

## Navigation Logic

Agents:

* Search for resources
* Evaluate hazard risk
* Move according to sensed information
* Balance reward versus danger

---

## Analytics Pipeline

The simulation exports:

* CSV experiment logs
* Agent-level data
* Plots and summaries

This allows experiment analysis after each run.

---

# Experiment Presets

The simulation currently supports multiple environment presets.

## Balanced

General-purpose environment with moderate:

* Food availability
* Hazard pressure
* Reproduction difficulty

---

## Scarce

Resource-limited environment.

Encourages:

* Competition
* Efficient navigation
* Conservative behavior

---

## Abundant

High-resource environment.

Encourages:

* Rapid reproduction
* Larger populations
* Reduced survival pressure

---

## Harsh

High-risk environment.

Encourages:

* Strong survival pressure
* Risk-sensitive navigation
* Efficient energy usage

---

# Current Project Status

The project is transitioning from:

```text
simple adaptation simulation
```

toward:

```text
autonomous systems experimentation framework
```

The system currently demonstrates:

* Sensor-based movement
* Risk-aware navigation
* Environmental adaptation
* Emergent behavior
* Autonomous survival strategies

Future development will focus on:

* Imperfect sensing
* Sensor noise
* Navigation under uncertainty
* Multi-agent interaction
* Dynamic obstacles
* Modular architecture
* Advanced telemetry
* Potential reinforcement-learning integration

---

# Important Clarification

This project is NOT currently a machine-learning system.

The simulation does not yet use:

* Neural networks
* Reinforcement learning
* Model training
* Gradient descent
* Learned policies

Instead, the project currently focuses on:

* Autonomous systems architecture
* Agent-based behavior
* Environmental interaction
* Adaptive traits
* Sensor-driven navigation
* Decision systems under constraints

Future versions may introduce machine-learning components once the autonomy and simulation foundation becomes more mature.

---

# Why This Project Matters

This project is designed to strengthen understanding of:

* Systems thinking
* Autonomous behavior
* Navigation logic
* Environmental interaction
* Engineering tradeoffs
* Simulation workflows
* Telemetry analysis
* Adaptive systems

The project is intended to function both as:

* a technical learning platform
* and a portfolio-quality engineering project

that demonstrates structured experimentation and autonomous systems reasoning.

---

# Running the Simulation

## Run Balanced Preset

```bash
python3 main.py --preset balanced
```

## Run Scarce Preset

```bash
python3 main.py --preset scarce
```

## Run Abundant Preset

```bash
python3 main.py --preset abundant
```

## Run Harsh Preset

```bash
python3 main.py --preset harsh
```

---

# Generate Experiment Plots

```bash
python3 plot_results.py
```

---

# Generate Experiment Summary

```bash
python3 summarize_results.py
```

---

# Controls

| Key | Action                      |
| --- | --------------------------- |
| R   | Reset simulation            |
| H   | Toggle hazard zone          |
| S   | Toggle sensor visualization |
| F   | Add food                    |
| G   | Remove food                 |

---

# Repository Structure

```text
autonomous-agent-sandbox/
│
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

# Long-Term Vision

The long-term direction of the project is to evolve into a small-scale autonomous systems experimentation framework capable of exploring:

* Sensor uncertainty
* Risk-aware navigation
* Multi-agent interaction
* Decision-making under constraints
* Adaptive behavior systems
* Resource-aware autonomy
* Navigation efficiency
* Autonomous systems analytics

while remaining understandable, lightweight, and experimentally flexible.

---

# Author Notes

This repository represents an ongoing engineering-learning process focused on autonomy systems, simulation architecture, and adaptive behavior experimentation.

The project intentionally evolves incrementally so that each new system can be studied, analyzed, documented, and understood before additional complexity is introduced.

The goal is not only to build the system, but also to understand the engineering concepts behind each architectural decision.
