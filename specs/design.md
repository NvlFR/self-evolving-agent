# SEED — System Design

## High-Level Architecture

```text
                ┌─────────────────┐
                │  SELF MODEL     │
                └────────┬────────┘
                         │
                         ▼

┌──────────┐     ┌─────────────┐     ┌─────────────┐
│ PLANNER  │────▶│ EXECUTOR    │────▶│ EVALUATOR   │
└──────────┘     └─────────────┘     └─────────────┘
                         │                    │
                         ▼                    ▼
                 ┌─────────────┐     ┌─────────────┐
                 │ REFLECTION  │────▶│ MODIFIER    │
                 └─────────────┘     └─────────────┘
                                                │
                                                ▼
                                        ┌─────────────┐
                                        │ VERSIONING  │
                                        └─────────────┘
```

---

# Component Design

## Planner

### Responsibility
Generate structured plans.

---

## Executor

### Responsibility
Execute runtime actions.

---

## Evaluator

### Responsibility
Measure generation quality.

### Metrics
- success rate
- runtime
- benchmark score

---

## Reflection Engine

### Responsibility
Analyze failures.

---

## Modifier

### Responsibility
Apply controlled mutations.

---

## Mutation Engine

### Responsibility
Generate controlled mutations.

---

## Memory System

### Episodic Memory
Stores:
- tasks
- results
- evaluations

### Self Model
Stores:
- strengths
- weaknesses
- hypotheses

---

## Version Manager

### Responsibility
Maintain generation lineage.

---

## Rollback Manager

### Responsibility
Recover failed generations.

---

## Autonomous Loop

### Responsibility
Run continuous evolution cycles.

### Cycle

```text
mutate
→ benchmark
→ evaluate
→ reflect
→ keep/rollback
→ repeat
```

---

# Safety Model

## Forbidden Operations
- unrestricted shell access
- evaluator modification
- rollback removal
- external payment access

## Required Protections
- snapshot before mutation
- rollback support
- mutation validation
- execution logging
