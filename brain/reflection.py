import json

class ReflectionEngine:
    def __init__(self):
        self.reflection_history = []

    def reflect_on_episodes(self, episodes: list):
        failures = [e for e in episodes if not e["evaluation"].get("success")]
        
        if not failures:
            return {
                "insights": "No failures detected in recent episodes. System stable.",
                "hypotheses": []
            }

        # Simple pattern matching for errors
        error_counts = {}
        for f in failures:
            err = f["result"].get("error", "unknown")
            # Extract first line of error or first 50 chars
            err_summary = str(err).split('\n')[0][:50]
            error_counts[err_summary] = error_counts.get(err_summary, 0) + 1

        top_error = max(error_counts, key=error_counts.get)
        
        insight = f"Detected repeated failure: '{top_error}' ({error_counts[top_error]} times)."
        
        hypotheses = [
            f"Fixing '{top_error}' will improve overall success rate.",
            "Adjusting planner heuristics might reduce this type of error."
        ]
        
        reflection = {
            "insights": insight,
            "hypotheses": hypotheses,
            "failure_count": len(failures)
        }
        
        self.reflection_history.append(reflection)
        return reflection

    def get_proposed_mutation_areas(self):
        if not self.reflection_history:
            return ["planner", "retry_logic"]
            
        # Logic to decide what to mutate based on reflections
        return ["planner", "heuristics"]
