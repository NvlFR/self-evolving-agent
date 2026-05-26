from brain.planner import Planner
from brain.evaluator import Evaluator
from brain.reflection import ReflectionEngine
from brain.modifier import Modifier
from brain.self_editor import SelfEditor
from runtime.executor import Executor
from runtime.version_manager import VersionManager
from memory.memory_manager import MemoryManager

planner = Planner()
executor = Executor()
evaluator = Evaluator()
reflection = ReflectionEngine()
modifier = Modifier()
self_editor = SelfEditor()
version_manager = VersionManager()
memory_manager = MemoryManager()

GOAL = "print('hello world')"

print("\n=== SEED AGENT START ===\n")

snapshot = version_manager.create_snapshot()
print(f"Snapshot created: {snapshot}")

plan = planner.create_plan(GOAL)
print(f"Plan: {plan}")

result = executor.execute(GOAL)
print(f"Execution result: {result}")

evaluation = evaluator.evaluate(
    success=result["success"],
    runtime=0.1,
    errors=0 if result["success"] else 1
)

print(f"Evaluation: {evaluation}")

reflection_result = reflection.reflect(result)
print(f"Reflection: {reflection_result}")

proposed_change = modifier.propose_change(reflection_result)
print(f"Proposed change: {proposed_change}")

memory_manager.store_episode(
    task=GOAL,
    result=result,
    evaluation=evaluation
)

if proposed_change:
    success = self_editor.apply_change(
        proposed_change["change"]
    )

    print(f"Self modification applied: {success}")

print("\n=== SEED AGENT END ===\n")
