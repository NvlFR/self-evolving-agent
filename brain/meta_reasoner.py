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
        Analisa sejarah evolusi sistem SEED berikut ini:
        {json.dumps(clean_history, indent=2)}

        Berikan wawasan tingkat tinggi (high-level insights) tentang kemajuan agen, 
        identifikasi strategi mutasi yang efektif vs tidak efektif, 
        dan berikan saran peningkatan arsitektur jangka panjang.
        Kembalikan respon dalam bentuk list JSON berisi string dalam Bahasa Indonesia.
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
