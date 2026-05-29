import json
from brain.llm_client import llm

class ReflectionEngine:
    def __init__(self):
        self.reflection_history = []

    def reflect_on_episodes(self, episodes: list):
        if not episodes:
            return {
                "insights": "No episode data available for reflection.",
                "hypotheses": []
            }

        # Prepare a summary of recent episodes for the LLM
        summary = []
        for e in episodes[-5:]: # Look at last 5 episodes
            summary.append({
                "task": e.get("task"),
                "success": e["evaluation"].get("success"),
                "score": e["evaluation"].get("score"),
                "mutation": e["result"].get("mutation")
            })

        prompt = f"""
        You are the SEED Evolution System's Reflection Engine.
        Analyze the following recent execution episodes and provide insights:
        {json.dumps(summary, indent=2)}

        Identify patterns of failure or success. 
        Propose hypotheses for how the agent can improve its architecture or tools.
        Return the response as a JSON object with 'insights' (string) and 'hypotheses' (list of strings).
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = llm.completion(messages)
        
        try:
            json_str = llm.extract_json(response)
            reflection = json.loads(json_str)
            self.reflection_history.append(reflection)
            return reflection
        except Exception as e:
            print(f"Error parsing reflection: {e}")
            return {
                "insights": "Error during LLM reflection. Proceeding with caution.",
                "hypotheses": ["Investigate LLM connectivity", "Simplify reflection prompt"]
            }

    def get_proposed_mutation_areas(self):
        # This could also be LLM driven, but for now we can derive it from hypotheses
        return ["core_logic", "new_tools", "planner_refinement"]
