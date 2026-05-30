import json
from brain.llm_client import llm

class MetaReasoner:
    def analyze_evolution(self, evolution_history):
        if not evolution_history:
            return ["No evolution history to analyze."]

        # Clean history for prompt
        clean_history = []
        for step in evolution_history:
            clean_history.append({
                "iteration": step.get("iteration"),
                "mutation": str(step.get("mutation")),
                "score": step.get("benchmark_score")
            })

        prompt = f"""
        Analyze the following evolution history of the SEED system:
        {json.dumps(clean_history, indent=2)}

        Provide high-level insights into the agent's progress, 
        identify effective vs ineffective mutation strategies, 
        and suggest long-term architectural improvements.
        Return the response as a JSON list of strings.
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = llm.completion(messages, request_type="meta")
        
        if not response or response == "ERROR_QUOTA":
            return [f"Overall evolution score: {evolution_history[-1]['benchmark_score']:.2f}"]
            
        try:
            json_str = llm.extract_json(response)
            if not json_str:
                return [f"Overall evolution score: {evolution_history[-1]['benchmark_score']:.2f}"]
            insights = json.loads(json_str)
            if isinstance(insights, list):
                return insights
            return [str(insights)]
        except Exception as e:
            print(f"Error parsing meta reasoning: {e}")
            return [f"Overall evolution score: {evolution_history[-1]['benchmark_score']:.2f}"]
