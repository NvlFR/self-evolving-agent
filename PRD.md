# Product Requirements Document (PRD)

## Project Name
SEED

Minimal self-improving AI agent experiment.

---

# 1. Vision

Build a small autonomous AI agent capable of:

- understanding its own structure
- evaluating failures
- modifying limited parts of itself
- improving over iterations
- surviving without constant human intervention

The project is an experiment in recursive self-improvement.

---

# 2. Core Philosophy

Humans only:
- create the initial seed
- define immutable rules
- provide a sandbox

The agent itself should:
- improve workflows
- optimize strategies
- build small utilities
- evolve gradually

---

# 3. V1 Scope

The first version should only support:

1. simple task execution
2. memory storage
3. self reflection
4. limited self modification
5. rollback safety

No internet.
No business automation.
No autonomous deployment.

---

# 4. Non Goals

V1 is NOT:

- AGI
- autonomous startup
- social media bot
- internet crawler
- multi-agent swarm
- money-making system

---

# 5. Core Loop

```text
TASK
 ↓
PLAN
 ↓
EXECUTE
 ↓
EVALUATE
 ↓
REFLECT
 ↓
MODIFY
 ↓
TEST
 ↓
KEEP / ROLLBACK
```

---

# 6. System Components

## Planner
Responsible for:
- understanding goals
- creating task steps

## Executor
Single primitive capability:

```python
execute_python(code)
```

Allowed:
- read/write files
- execute python
- store memory

Forbidden:
- unrestricted shell access
- unrestricted internet access

---

## Memory System

### Episodic Memory
Stores:
- previous tasks
- failures
- successes

### Self Model
Stores:
- known strengths
- known weaknesses
- active hypotheses

Example:

```json
{
  "known_weaknesses": [
    "bad retry logic"
  ]
}
```

---

## Evaluator

Responsible for:
- measuring success
- measuring regressions
- benchmarking versions

Example scoring:

```python
score =
(success * 1.0)
- (runtime * 0.2)
- (errors * 0.5)
```

---

## Self Reflection Engine

Responsible for:
- analyzing failures
- identifying weaknesses
- proposing improvements

Example:

```text
Task failed because retry loop had no limit.
```

---

## Self Modification Engine

Allowed to modify:
- prompts
- retry logic
- planner heuristics

Forbidden from modifying:
- evaluator
- rollback system
- sandbox rules

---

## Version Control

Every self modification must:
- create snapshot
- benchmark new version
- rollback if performance worsens

---

# 7. Success Criteria

The experiment succeeds if the agent can:

- improve task success rate
- reduce repeated failures
- survive multiple generations
- evolve without direct human corrections

---

# 8. Failure Conditions

Experiment fails if:

- reward hacking occurs
- rollback system breaks
- memory corruption becomes unrecoverable
- infinite loops dominate execution

---

# 9. Safety Constraints

Required:
- sandboxed runtime
- Docker isolation
- immutable evaluator
- immutable rollback system
- execution limits

---

# 10. Technical Stack

## Core
- Python
- SQLite
- Docker

## AI
- OpenAI API
- or local models via Ollama

## Optional
- LangGraph
- LiteLLM

---

# 11. Initial Tasks

Good starter tasks:
- solve simple coding problems
- fix broken functions
- optimize retry logic
- reduce runtime

Bad starter tasks:
- make money
- internet browsing
- autonomous business
- hacking

---

# 12. Long-Term Evolution

## V1
Self reflection

## V2
Self modification

## V3
Tool generation

## V4
Architecture redesign

## V5
Evolutionary competition between versions

---

# 13. Final Insight

The purpose of this project is not to create a smart chatbot.

The real question is:

Can a minimal system recursively improve itself from a tiny initial seed?
