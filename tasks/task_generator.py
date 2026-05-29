import json
import random
from pathlib import Path
from brain.llm_client import llm

class TaskGenerator:
    def __init__(self, tasks_path="tasks/generated_tasks.json"):
        self.tasks_path = Path(tasks_path)

    def generate_tasks(self, count=3, difficulty=1):
        existing_tasks = self.load_existing_tasks()
        
        prompt = f"""
        Generate {count} unique programming or logic tasks for an AI agent to solve.
        The difficulty level is {difficulty} (1-10).
        Each task should have a unique 'goal' and a suggested 'difficulty'.
        Return the response as a JSON list of objects with 'goal' and 'difficulty' keys.
        Example:
        [
          {{"goal": "Write a function to calculate the Fibonacci sequence up to n terms", "difficulty": 2}},
          {{"goal": "Implement a basic neural network from scratch in pure Python", "difficulty": 8}}
        ]
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = llm.completion(messages)
        
        try:
            json_str = llm.extract_json(response)
            new_tasks_data = json.loads(json_str)
            new_tasks = []
            for item in new_tasks_data:
                task_id = f"gen_task_{len(existing_tasks) + len(new_tasks) + 1}"
                new_tasks.append({
                    "id": task_id,
                    "goal": item["goal"],
                    "difficulty": item["difficulty"]
                })
                
            self.save_tasks(existing_tasks + new_tasks)
            return new_tasks
        except Exception as e:
            print(f"Error parsing LLM response for tasks: {e}")
            return []

    def load_existing_tasks(self):
        if not self.tasks_path.exists():
            return []
        try:
            with open(self.tasks_path, "r") as f:
                return json.load(f)
        except:
            return []

    def save_tasks(self, tasks):
        with open(self.tasks_path, "w") as f:
            json.dump(tasks, f, indent=2)
