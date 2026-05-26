class ReflectionEngine:
    def reflect(self, task_result: dict):
        if not task_result.get("success"):
            return {
                "problem_detected": task_result.get("error", "unknown"),
                "proposed_fix": "improve retry strategy"
            }

        return {
            "problem_detected": None,
            "proposed_fix": None
        }
