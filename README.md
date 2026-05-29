# SEED — Self-Evolving Experiment in Autonomous Design

> A minimal recursive self-improvement system that observes, reflects, mutates, and evolves its own architecture over time.

---

## Overview

SEED is a research-grade autonomous agent experiment built around one core question:

> *Can a small system understand itself, modify itself, and improve itself — without human intervention?*

The system runs an autonomous evolution loop: it executes tasks, evaluates its own performance, reflects on failure patterns, proposes targeted mutations to its own logic, applies those changes, benchmarks the result, and either keeps or rolls back the modification.

This is not a chatbot. It is not an automation framework. It is a minimal architecture for studying **recursive self-improvement** and **stability under self-modification**.

---

## Problem

Most autonomous AI systems are static after deployment:

- They cannot identify *why* they fail
- They cannot adapt internal logic based on observed performance
- They have no mechanism to preserve improvements across generations
- Manual tuning is required every time behavior needs to change
- There is no feedback loop between execution results and system design

The result: agents that plateau early, degrade silently, and require constant human intervention to stay effective.

---

## Solution

SEED implements a closed-loop evolution pipeline:

1. **Observe** — load episodic memory from previous runs
2. **Reflect** — analyze failure patterns and extract insights
3. **Mutate** — generate a targeted modification proposal
4. **Validate** — run the mutation through a safety guard
5. **Snapshot** — version the current state before applying changes
6. **Apply** — self-edit the planner or heuristic configuration
7. **Benchmark** — run standardized tasks and score the result
8. **Select** — keep the mutation if score ≥ 0.6, rollback otherwise
9. **Remember** — store the episode, update the self-model

Each iteration produces a versioned snapshot, a benchmark score, and an updated internal self-representation tracking strengths, weaknesses, and active hypotheses.

---

## Key Features

| Feature | Description |
|---|---|
| Autonomous Evolution Loop | Runs N iterations of observe → mutate → evaluate → select |
| Self-Editor | Applies code-level and config-level mutations to its own modules |
| Mutation Engine | Generates targeted mutation proposals based on reflection output |
| Adaptive Evaluator | Scores iterations with context-aware metrics and repetition penalties |
| Reflection Engine | Analyzes episodic memory to extract behavioral insights |
| Version Manager | Creates timestamped snapshots before every modification |
| Rollback Manager | Reverts to last stable snapshot when a generation is rejected |
| Safety Guard | Validates mutations before application — blocks unsafe changes |
| Self-Model Memory | Maintains a live JSON representation of strengths, weaknesses, and hypotheses |
| Episodic Memory | Persists full iteration history across runs |
| Task Generator | Dynamically generates benchmark tasks with configurable difficulty |
| Meta Reasoner | Analyzes the full evolution history to surface cross-iteration insights |

---

## System Workflow

```
START
  │
  ▼
Load Episodic Memory
  │
  ▼
Reflection Engine → Extract Insights
  │
  ▼
Mutation Engine → Propose Change
  │
  ▼
Safety Guard → Validate Mutation
  │         └── BLOCKED → Skip Iteration
  ▼
Version Manager → Create Snapshot
  │
  ▼
Self-Editor → Apply Mutation
  │
  ▼
Benchmark Runner → Execute Tasks
  │
  ▼
Adaptive Evaluator → Score Result
  │
  ├── Score ≥ 0.6 → Accept Generation
  │                  └── Update Self-Model (strength)
  │
  └── Score < 0.6 → Reject Generation
                     └── Rollback to Snapshot
                     └── Update Self-Model (weakness)
  │
  ▼
Memory Manager → Store Episode
  │
  ▼
Next Iteration / END
```

---

## Architecture

```
self-evolving-agent/
│
├── main.py                    # Entry point — runs evolution loop + meta reasoning
│
├── brain/                     # Cognitive layer
│   ├── planner.py             # Generates task execution plans from heuristics
│   ├── reflection.py          # Analyzes episodic memory for behavioral patterns
│   ├── modifier.py            # Base modification interface
│   ├── self_editor.py         # Applies mutations to source files and configs
│   ├── mutation_engine.py     # Generates mutation proposals from reflection output
│   ├── adaptive_evaluator.py  # Context-aware scoring with repetition penalties
│   ├── meta_reasoner.py       # Cross-iteration analysis of evolution history
│   └── config_mutator.py      # Mutates JSON config files (planner heuristics)
│
├── runtime/                   # Execution layer
│   ├── autonomous_loop.py     # Main evolution orchestrator
│   ├── executor.py            # Task execution engine
│   ├── benchmark_runner.py    # Runs standardized benchmark tasks
│   ├── version_manager.py     # Creates timestamped snapshots
│   ├── rollback_manager.py    # Reverts to previous snapshot on failure
│   └── safety_guard.py        # Validates mutations before application
│
├── memory/                    # Persistence layer
│   ├── memory_manager.py      # Stores and loads episodic memory
│   ├── self_model_manager.py  # Manages the live self-model JSON
│   ├── episodes.json          # Full episodic history (auto-generated)
│   └── self_model.json        # Live self-representation (strengths/weaknesses)
│
├── tasks/                     # Task layer
│   ├── task_generator.py      # Dynamically generates tasks by difficulty
│   ├── benchmark_tasks.py     # Static benchmark task definitions
│   └── generated_tasks.json   # Auto-generated task pool
│
├── configs/                   # Mutable configuration
│   ├── planner.json           # Planner heuristics (mutated at runtime)
│   └── evaluator.json         # Evaluator thresholds
│
├── versions/                  # Snapshot archive (auto-generated)
│   └── snapshot_<timestamp>/  # Versioned brain state per iteration
│
└── specs/                     # Design documentation
    ├── requirements.md
    ├── design.md
    └── tasks.md
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12+ |
| LLM Integration | OpenAI API, LiteLLM |
| Agent Orchestration | LangGraph |
| Data Validation | Pydantic v2 |
| Configuration | python-dotenv |
| Terminal Output | Rich |
| Persistence | JSON (episodic memory, self-model, snapshots) |
| Versioning | File-based snapshot system |

---

## Results / Impact

Based on observed evolution runs:

- **40+ versioned snapshots** generated across a single session — full rollback capability at every step
- **Planner heuristics mutated 12+ times** autonomously — zero manual intervention
- **Self-model updated in real time** — strengths and weaknesses tracked across generations
- **Repetition penalty system** reduces redundant mutations by applying score penalties to repeated proposals
- **Safety guard blocks unsafe mutations** before they reach the file system
- Benchmark scoring converges toward higher-reliability configurations over successive iterations
- The system identified `planner` mutations as the highest-impact change class autonomously, recording this as a hypothesis in the self-model

---

## Security / Scalability

**Safety Constraints (by design):**

- `SafetyGuard` validates every mutation before application — unsafe patterns are blocked
- The agent cannot access payment systems, external networks, or disable its own logging
- Evaluator integrity is protected — the scoring module is not in the mutation target set
- Rollback is always available — no mutation is permanent until it passes the benchmark threshold

**Scalability Design:**

- Snapshot system scales linearly — each iteration adds one versioned directory
- Episodic memory is append-only JSON — can be replaced with a vector store for semantic retrieval
- Mutation engine is stateless — parallelizable across multiple agent instances
- Config-based heuristics allow behavior changes without code modification

**Observability:**

- Full evolution history logged per iteration (mutation, score, snapshot reference, evaluation context)
- Self-model JSON provides a human-readable audit trail of what the system learned
- Rich terminal output with per-iteration status during execution

---

## Installation / Quick Start

**Prerequisites:**

- Python 3.12+
- OpenAI API key (or compatible LiteLLM provider)

**Setup:**

```bash
git clone https://github.com/your-username/self-evolving-agent.git
cd self-evolving-agent

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

**Environment:**

```bash
cp .env.example .env
# Edit .env and set your API key:
# OPENAI_API_KEY=sk-...
```

**Run:**

```bash
python main.py
```

The system will run 5 evolution iterations by default, printing each step to the terminal and writing snapshots, episodes, and self-model updates to disk.

**Adjust iteration count in `main.py`:**

```python
history = loop.evolve(iterations=10)  # Run 10 generations
```

---

## Project Structure

| Path | Responsibility |
|---|---|
| `brain/` | All cognitive logic — planning, reflection, mutation, evaluation |
| `runtime/` | Execution infrastructure — loop orchestration, benchmarking, versioning, safety |
| `memory/` | Persistence — episodic history, self-model, snapshot archive |
| `tasks/` | Task definitions and dynamic task generation |
| `configs/` | Mutable runtime configuration (mutated by the agent itself) |
| `versions/` | Auto-generated snapshot archive — one directory per iteration |
| `specs/` | Design documents and requirements |

---

## Future Improvements

- **Persistent vector memory** — replace JSON episodic store with a vector database for semantic retrieval across thousands of episodes
- **Multi-agent competition** — run N agents in parallel with different mutation strategies, select the best-performing lineage
- **Mutation engine v2** — LLM-generated mutations targeting any module, not just planner heuristics
- **Benchmark environment expansion** — domain-specific task suites (code generation, reasoning, planning)
- **Dashboard** — real-time visualization of evolution scores, mutation history, and self-model state
- **Autonomous tool generation** — agent generates new utility modules and integrates them into its own runtime
- **Architecture redesign capability** — allow the agent to propose structural changes to its own module graph
- **RAG-enhanced reflection** — retrieve semantically similar past episodes to improve mutation quality

---

## Demo / Screenshots

**Evolution loop terminal output:**

```
=== Evolution Iteration 1 ===
Reflection insight: ['No strong patterns yet. Explore broadly.']
Proposed mutation: Apply planner mutation: enable include_validation
Iteration final score: 0.85
Selection pressure: Generation accepted.

=== Evolution Iteration 2 ===
Reflection insight: ['Planner mutations show consistent improvement.']
Proposed mutation: Apply heuristics mutation: optimize for reliability
Iteration final score: 0.90
Selection pressure: Generation accepted.
```

**Self-model after 5 iterations (`memory/self_model.json`):**

```json
{
  "strengths": [
    "Successful evolution: Apply planner mutation: enable include_validation",
    "Successful evolution: Apply heuristics mutation: optimize for reliability"
  ],
  "weaknesses": [
    "limited planning",
    "no persistent strategy optimization"
  ],
  "active_goals": ["improve task success rate"],
  "hypotheses": [
    "Mutations involving 'planner' seem highly effective."
  ]
}
```

**Snapshot archive structure:**

```
versions/
├── snapshot_20260526_173624/       # Iteration 1 baseline
├── snapshot_20260526_173639_387304/ # Post-mutation v1
├── snapshot_20260526_173719_509271/ # Post-mutation v2
└── snapshot_20260526_175759_606438/ # Latest accepted generation
```

---

## Conclusion

SEED demonstrates that a minimal Python system — without fine-tuning, without external orchestration platforms, without human-in-the-loop feedback — can implement a functional recursive self-improvement loop.

The core insight: **stability under self-modification requires versioning, safety constraints, and selection pressure**. Without all three, self-modification degrades into noise. With all three, the system converges toward better configurations over successive generations.

This architecture is a foundation. The next step is scaling the mutation surface, expanding the benchmark environment, and introducing multi-agent competition — moving from a single evolving agent toward an evolutionary system.

---

**License:** MIT · **Status:** Active Research · **Version:** V2 — Self Modification
