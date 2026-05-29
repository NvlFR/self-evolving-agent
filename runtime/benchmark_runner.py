import time
import json
from pathlib import Path
from tasks.benchmark_tasks import BENCHMARK_TASKS
from brain.planner import Planner
from runtime.executor import Executor
from brain.evaluator import Evaluator
from brain.llm_client import llm

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
            print(f"  - Running task: {task['goal']}")
            start_time = time.time()
            
            # 1. Plan
            plan = self.planner.create_plan(task["goal"])
            
            # 2. Generate Code based on Plan and Goal
            prompt = f"""
            You are the SEED Evolution System's Coder.
            Task: {task['goal']}
            Plan: {json.dumps(plan)}

            Write a Python script to solve this task. 
            Include necessary print statements to verify the output.
            Return ONLY the Python code. No markdown formatting.
            """
            messages = [{"role": "user", "content": prompt}]
            code = llm.completion(messages)
            
            if code and "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif code and "```" in code:
                code = code.split("```")[1].split("```")[0].strip()

            # 3. Execute
            execution_result = self.executor.execute(code if code else "")
            
            end_time = time.time()
            runtime = end_time - start_time
            
            # 4. Evaluate
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
