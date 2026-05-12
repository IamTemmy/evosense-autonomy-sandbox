# Autonomous Agent Sandbox

A lightweight simulation framework for studying autonomous agents, environmental constraints, sensor-driven behavior, risk-aware navigation, and adaptive decision-making.

This project began as a simple agent-based ecosystem simulation and is evolving into a small-scale autonomy systems sandbox. The goal is to model how independent agents sense their environment, make decisions under constraints, respond to hazards, manage energy, and adapt over time.

This project explores how autonomous entities behave inside dynamic environments with:
- resource scarcity
- energy constraints
- survival pressure
- reproduction
- environmental interaction

The long-term goal is to evolve this sandbox into a broader experimentation platform for:
- autonomous systems
- swarm intelligence
- environmental simulations
- adaptive behavior modeling
- robotics concepts
- ecosystem simulations
- digital twin experimentation

---

# Current Features

## Autonomous Agents
- Agents move independently inside a bounded environment
- Agents detect nearby food and move toward it
- Agents consume energy over time
- Agents die if energy reaches zero

## Resource System
- Food spawns dynamically across the environment
- Agents gain energy when consuming food
- Resource scarcity affects survival rates

## Adaptive Population
- Successful agents reproduce
- Population size changes dynamically
- Agents visually scale based on energy level

## Simulation Dashboard
Real-time statistics:
- population count
- food count
- average energy
- births
- deaths

---

# Technologies Used

- Python
- Pygame
- Math / vector calculations
- Git + GitHub

---

# How To Run

## Clone Repository

```bash
git clone https://github.com/IamTemmy/autonomous-agent-sandbox.git
cd autonomous-agent-sandbox
```

## Install Dependencies

```bash
python3 -m pip install pygame
```

## Run Simulation

```bash
python3 main.py
```

---

# Development Timeline

## v0.1
- Initial autonomous movement system

## v0.2
- Fixed zero-velocity agents

## v0.3
- Added food/resource entities

## v0.4
- Added food consumption system

## v0.5
- Added energy and death mechanics

## v0.6
- Added food-seeking behavior

## v0.7
- Added energy-based size scaling

## v0.8
- Tuned scarcity and survival balancing

## v0.9
- Added reproduction system

## v1.0
- Added real-time simulation dashboard

---

# Future Goals

- Environmental hazard zones
- Evolutionary traits
- Speed variation between agents
- Neural-network-driven agents
- Reinforcement learning experiments
- Sensor simulation systems
- Multi-species ecosystem interactions
- Autonomous robotics behavior experiments

---

# Vision

This project began as an exploration into how simple autonomous entities interact with changing environments.

The broader vision is to develop a modular experimentation sandbox for studying adaptation, survival, intelligence, and autonomous behavior in dynamic systems.


---

# Engineering Interpretation

Although the simulation uses simple 2D visuals, the underlying system models several engineering and autonomy-related concepts.

## Autonomous Agents

Each agent operates independently inside the environment. Agents move without centralized control and make local decisions based on nearby resources. This creates a simplified model of autonomous behavior where individual entities react to changing conditions in real time.

## Resource-Constrained Survival

Agents continuously lose energy and must locate food to survive. This introduces resource pressure similar to real engineering systems such as:
- battery-powered robots
- autonomous drones
- distributed sensor systems
- autonomous vehicles operating under energy constraints

The simulation demonstrates how survival and performance are affected by limited resources.

## Environmental Stressors

The purple hazard zone represents a dangerous environmental region. It can be interpreted as:
- pollution
- low oxygen
- difficult terrain
- heat zones
- toxic exposure
- disaster-affected areas

Agents that remain inside the zone lose energy faster, allowing the environment itself to influence survival outcomes.

## Evolutionary Traits

Agents now possess inherited traits:
- movement speed
- vision radius
- energy consumption rate

When agents reproduce, offspring inherit traits from their parent with slight mutations. Over time, populations may shift toward traits that improve survival.

This introduces a simplified evolutionary system where environmental pressure affects which traits become dominant.

## Lineage Tracking

Each original lineage is assigned a color. Offspring inherit similar colors with slight mutations, allowing family groups to be visually tracked across generations.

The lineage leaderboard shows which family groups are dominating the ecosystem.

## Connection to Autonomy and Engineering

This project is not yet a full autonomous vehicle simulator. However, it demonstrates several foundational ideas related to autonomy and intelligent systems:

- decentralized agents
- local sensing
- environmental interaction
- survival optimization
- adaptation under constraints
- population-level system behavior
- emergent dynamics

The long-term direction of the project is to evolve this sandbox toward more advanced autonomous-system concepts such as:
- obstacle avoidance
- sensor uncertainty
- path planning
- decision weighting
- reinforcement learning
- swarm coordination

---

# Current Limitations

- The simulation currently operates in 2D space.
- Agents do not yet perform true path planning.
- Agents do not learn from experience.
- Hazard interaction is still relatively simple.
- The lineage leaderboard does not yet visually map lineage IDs to colors.
- No persistent data logging exists yet.

---

# Near-Term Roadmap

## v1.9 — Lineage Color Legend
Display lineage colors directly beside leaderboard entries for easier interpretation.

## v2.0 — Data Logging
Save ecosystem statistics over time:
- population
- births
- deaths
- energy
- traits
- lineage performance

## v2.1 — Simulation Graphs
Generate plots showing how the ecosystem evolves over time.

## v2.2 — Trait Analysis
Analyze which inherited traits correlate with survival and reproduction.

## v2.3 — Advanced Autonomy Systems
Introduce:
- obstacle avoidance
- sensor-based navigation
- risk-aware movement
- autonomous decision systems
- environmental path planning




*********************Temmy**************************
