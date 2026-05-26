class Modifier:
    def propose_change(self, reflection_result: dict):
        if reflection_result.get("problem_detected"):
            return {
                "target": "planner",
                "change": reflection_result.get("proposed_fix")
            }

        return None
