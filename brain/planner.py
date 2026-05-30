import json
from pathlib import Path
from brain.llm_client import llm

class Planner:
    def __init__(self, config_path="configs/planner.json"):
        self.config_path = Path(config_path)

    def create_plan(self, goal: str):
        prompt = f"""
        You are the SEED Evolution System's Planner.
        Your goal is to create a step-by-step execution plan for the following task:
        "{goal}"

        Break down the task into small, actionable steps.
        Return the plan as a JSON list of strings.
        Example: ["Import necessary libraries", "Define the main function", "Implement logic", "Verify results"]
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = llm.completion(messages)
        
        if not response or response == "ERROR_QUOTA":
            return [f"Deconstruct goal: {goal}", "Execute task", "Return results"]
            
        try:
            json_str = llm.extract_json(response)
            if not json_str:
                return [f"Deconstruct goal: {goal}", "Execute task", "Return results"]
            plan = json.loads(json_str)
            if isinstance(plan, list):
                return plan
            return [str(plan)]
        except Exception as e:
            print(f"Error parsing plan: {e}")
            return [f"Deconstruct goal: {goal}", "Execute task", "Return results"]
