class Planner:
    def __init__(self):
        # These heuristics are intended to be modified by the agent itself later
        self.heuristics = {
            "include_analysis": True,
            "include_validation": True,
            "max_steps": 5
        }

    def create_plan(self, goal: str):
        plan = []
        
        if self.heuristics["include_analysis"]:
            plan.append(f"Analysis: Deconstructing goal - {goal}")
            
        plan.append("Task: Identify required components")
        plan.append("Task: Implement core logic")
        
        if self.heuristics["include_validation"]:
            plan.append("Validation: Test edge cases")
            
        plan.append("Completion: Finalize and return results")
        
        return plan[:self.heuristics["max_steps"]]

# Self modification note: Apply planner mutation: enable include_validation

# Self modification note: Apply planner mutation: enable include_validation

# Self modification note: Apply heuristics mutation: strict validation mode

# Self modification note: Apply heuristics mutation: optimize for reliability

# Self modification note: Apply planner mutation: reduce max_steps to 3

# Self modification note: Apply heuristics mutation: strict validation mode

# Self modification note: Apply heuristics mutation: optimize for reliability

# Self modification note: Apply planner mutation: enable include_validation

# Self modification note: Apply heuristics mutation: optimize for speed

# Self modification note: Apply heuristics mutation: strict validation mode

# Self modification note: Apply heuristics mutation: strict validation mode

# Self modification note: Apply planner mutation: disable include_analysis

# Self modification note: Apply heuristics mutation: strict validation mode

# Self modification note: Apply planner mutation: enable include_validation

# Self modification note: Apply heuristics mutation: optimize for reliability

# Self modification note: Apply heuristics mutation: optimize for reliability
