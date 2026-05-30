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
        Kamu adalah Mesin Refleksi (Reflection Engine) Sistem Evolusi SEED.
        Analisa episode eksekusi terbaru berikut dan berikan wawasan (insight):
        {json.dumps(summary, indent=2)}

        Identifikasi pola kegagalan atau keberhasilan. 
        Usulkan hipotesa tentang bagaimana agen bisa meningkatkan arsitektur atau tool-nya.
        Kembalikan respon dalam objek JSON dengan 'insights' (string) dan 'hypotheses' (list string).
        PENTING: Semua teks 'insights' dan 'hypotheses' HARUS dalam Bahasa Indonesia.
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = llm.completion(messages)
        
        if not response or response == "ERROR_QUOTA":
            return {
                "insights": "Quota reached or LLM error. Skipping reflection.",
                "hypotheses": []
            }
            
        try:
            json_str = llm.extract_json(response)
            if not json_str:
                return {
                    "insights": "Empty LLM response. Skipping reflection.",
                    "hypotheses": []
                }
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
