import random

class MutationEngine:
    def __init__(self):
        self.mutation_strategies = {
            "planner": [
                "increase max_steps to 10",
                "disable include_analysis",
                "enable include_validation",
                "reduce max_steps to 3"
            ],
            "heuristics": [
                "optimize for speed",
                "optimize for reliability",
                "strict validation mode"
            ]
        }

    def generate_mutation(self, reflection: dict = None):
        if reflection and "hypotheses" in reflection:
            # In a real scenario, we'd use LLM to translate hypothesis to code change.
            # Here we pick a strategy that matches the proposed areas.
            areas = ["planner", "heuristics"]
            area = random.choice(areas)
            mutation = random.choice(self.mutation_strategies[area])
            return f"Apply {area} mutation: {mutation}"
            
        return random.choice(self.mutation_strategies["planner"])
