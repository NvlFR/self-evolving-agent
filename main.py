from brain.planner import Planner
from brain.evaluator import Evaluator
from brain.reflection import ReflectionEngine
from brain.modifier import Modifier
from runtime.executor import Executor

planner = Planner()
executor = Executor()
evaluator = Evaluator()
reflection = ReflectionEngine()
modifier = Modifier()

GOAL = "print('hello world')"

plan = planner.create_plan(GOAL)

result = executor.execute(GOAL)

evaluation = evaluator.evaluate(
    success=result["success"],
    runtime=0.1,
    errors=0 if result["success"] else 1
)

reflection_result = reflection.reflect(result)

proposed_change = modifier.propose_change(reflection_result)

print("PLAN:", plan)
print("RESULT:", result)
print("EVALUATION:", evaluation)
print("REFLECTION:", reflection_result)
print("PROPOSED CHANGE:", proposed_change)
