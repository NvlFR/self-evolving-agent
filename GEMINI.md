# SEED — Self-Evolving-Agent

SEED is a research-style experiment in building a minimal recursive self-improving AI agent. The goal is to create a system that can understand its own architecture, evaluate its performance, and autonomously modify itself to improve over time.

## Project Overview

- **Vision:** A system that grows from a small "seed" into a more capable agent through continuous self-modification and benchmarking.
- **Core Loop:** `Mutate` → `Benchmark` → `Evaluate` → `Reflect` → `Keep/Rollback` → `Repeat`.
- **Technologies:** Python, LiteLLM/OpenAI, LangGraph, Pydantic, Rich.

## Architecture

The project is organized into several key modules:

### Brain (`brain/`)
Responsible for the "cognitive" functions of the agent.
- `planner.py`: Generates structured plans for tasks.
- `mutation_engine.py`: Generates proposed changes to the agent's own code (currently a placeholder).
- `self_editor.py`: Applies code modifications to the codebase.
- `reflection.py`: Analyzes failures and proposes improvements.
- `evaluator.py`: Measures the success and efficiency of task execution.
- `meta_reasoner.py`: Analyzes the evolution history to find long-term patterns.

### Runtime (`runtime/`)
Orchestrates the execution and evolution cycles.
- `autonomous_loop.py`: The main loop that drives the evolution process.
- `executor.py`: Handles the execution of actions (e.g., running Python code).
- `benchmark_runner.py`: Runs a suite of tasks to evaluate the performance of a version.
- `version_manager.py` & `rollback_manager.py`: Manages snapshots and reverts the codebase if a mutation fails validation.
- `safety_guard.py`: Enforces constraints on what the agent can modify or access.

### Memory (`memory/`)
Stores the agent's experience and self-understanding.
- `memory_manager.py`: Manages episodic memory (logs of previous tasks and results).
- `self_model_manager.py`: Manages the "self-model" (`self_model.json`), which tracks the agent's perceived strengths, weaknesses, and hypotheses.

### Specs & Tasks (`specs/`, `tasks/`)
- `PRD.md` & `design.md`: Core documentation of the project's vision and architecture.
- `benchmark_tasks.py`: Defines the tasks used to measure agent performance.

## Building and Running

### Prerequisites
- Python 3.10+
- OpenAI API Key (if using LLM features)

### Installation
```bash
pip install -r requirements.txt
```

### Execution
To start the autonomous evolution loop:
```bash
python main.py
```

## Development Conventions

- **Type Safety:** Use Pydantic for structured data models and ensure proper type hinting.
- **Modularity:** Keep logic strictly separated between `brain`, `runtime`, and `memory`.
- **Safety First:** Never modify the `Evaluator`, `RollbackManager`, or `SafetyGuard` modules. These are the "immutable" constraints of the system.
- **CLI Feedback:** Use the `rich` library for clean and informative terminal output.
- **Testing:** New features should be accompanied by benchmark tasks in `tasks/` to ensure they can be autonomously evaluated.

## Current Status (V1)
The project is currently in an early stage. Many components (like the `MutationEngine` and `BenchmarkRunner`) are implemented as placeholders or minimal implementations. Future work focuses on integrating LLMs for real code generation and expanding the benchmark suite.
