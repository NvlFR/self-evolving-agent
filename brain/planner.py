import json
from pathlib import Path

class Planner:
    def __init__(self, config_path="configs/planner.json"):
        self.config_path = Path(config_path)
        self.heuristics = self._load_config()

    def _load_config(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, "r") as f:
                    return json.load(f)
            except:
                pass
        
        # Default heuristics
        return {
            "include_analysis": True,
            "include_validation": True,
            "max_steps": 5
        }

    def create_plan(self, goal: str):
        # Reload config in case it changed due to mutation
        self.heuristics = self._load_config()
        
        plan = []
        
        if self.heuristics.get("include_analysis", True):
            plan.append(f"Analysis: Deconstructing goal - {goal}")
            
        plan.append("Task: Identify required components")
        plan.append("Task: Implement core logic")
        
        if self.heuristics.get("include_validation", True):
            plan.append("Validation: Test edge cases")
            
        plan.append("Completion: Finalize and return results")
        
        max_steps = self.heuristics.get("max_steps", 5)
        return plan[:max_steps]

# Self modification note: Apply heuristics mutation: strict validation mode

# Self modification note: Apply heuristics mutation: strict validation mode

# Self modification note: Apply heuristics mutation: optimize for speed

# Self modification note: Apply heuristics mutation: optimize for speed

# Self modification note: Apply heuristics mutation: optimize for reliability

# Self modification note: Apply heuristics mutation: optimize for speed

# Self modification note: Apply heuristics mutation: optimize for speed

# Self modification note: Apply heuristics mutation: optimize for reliability

# Self modification note: Apply heuristics mutation: optimize for reliability

# Self modification note: Apply heuristics mutation: optimize for speed

# Self modification note: Apply heuristics mutation: optimize for reliability
