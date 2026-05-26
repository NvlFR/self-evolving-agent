import time
import json
from pathlib import Path
from tasks.benchmark_tasks import BENCHMARK_TASKS
from brain.planner import Planner
from runtime.executor import Executor
from brain.evaluator import Evaluator

class BenchmarkRunner:
    def __init__(self, generated_tasks_path="tasks/generated_tasks.json"):
        self.planner = Planner()
        self.executor = Executor()
        self.evaluator = Evaluator()
        self.generated_tasks_path = Path(generated_tasks_path)

    def run(self):
        all_tasks = BENCHMARK_TASKS.copy()

        # Add generated tasks if they exist
        if self.generated_tasks_path.exists():
            try:
                with open(self.generated_tasks_path, "r") as f:
                    all_tasks.extend(json.load(f))
            except:
                pass

        results = []

        for task in all_tasks:
            start_time = time.time()
            
            # 1. Plan
            plan = self.planner.create_plan(task["goal"])
            
            # 2. Execute (Simulated)
            simulated_code = f"# Task: {task['id']}\nprint('Executing task: {task['goal']}')"
            execution_result = self.executor.execute(simulated_code)
            
            end_time = time.time()
            runtime = end_time - start_time
            
            # 3. Evaluate
            evaluation = self.evaluator.evaluate(
                success=execution_result["success"],
                runtime=runtime,
                errors=1 if not execution_result["success"] else 0
            )
            
            results.append({
                "task_id": task["id"],
                "success": execution_result["success"],
                "score": evaluation["score"],
                "runtime": runtime,
                "stdout": execution_result["stdout"],
                "stderr": execution_result["stderr"],
                "error": execution_result["error"]
            })

        return results
