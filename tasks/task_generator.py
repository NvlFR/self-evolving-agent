import json
import random
from pathlib import Path

class TaskGenerator:
    def __init__(self, tasks_path="tasks/generated_tasks.json"):
        self.tasks_path = Path(tasks_path)
        self.base_tasks = [
            "calculate factorial of {n}",
            "find prime numbers up to {n}",
            "sort a list of {n} random integers",
            "reverse a string of length {n}",
            "check if {n} is a palindrome"
        ]

    def generate_tasks(self, count=3, difficulty=1):
        existing_tasks = self.load_existing_tasks()
        new_tasks = []
        
        for i in range(count):
            base = random.choice(self.base_tasks)
            n = random.randint(10 * difficulty, 100 * difficulty)
            task_goal = base.format(n=n)
            
            # Avoid simple duplicates
            if any(t["goal"] == task_goal for t in existing_tasks):
                continue
                
            task_id = f"gen_task_{len(existing_tasks) + len(new_tasks) + 1}"
            new_tasks.append({
                "id": task_id,
                "goal": task_goal,
                "difficulty": difficulty
            })
            
        self.save_tasks(existing_tasks + new_tasks)
        return new_tasks

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
