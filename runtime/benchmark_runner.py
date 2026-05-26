import time
from tasks.benchmark_tasks import BENCHMARK_TASKS
from brain.planner import Planner
from runtime.executor import Executor
from brain.evaluator import Evaluator

class BenchmarkRunner:
    def __init__(self):
        self.planner = Planner()
        self.executor = Executor()
        self.evaluator = Evaluator()

    def run(self):
        results = []

        for task in BENCHMARK_TASKS:
            start_time = time.time()
            
            # 1. Plan
            plan = self.planner.create_plan(task["goal"])
            
            # 2. Execute (For now, we simulate execution of the plan's code generation)
            # In a real scenario, an LLM would generate code based on the plan.
            # For the benchmark, we'll assume the 'goal' itself might contain 
            # or imply code that can be run, or we just simulate success/failure.
            
            # For demonstration, let's say we try to execute something related to the task
            # If the goal is "Create a Python function...", we might eventually have a solver.
            # For now, we'll simulate a result.
            
            # Simulated code for the task
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
