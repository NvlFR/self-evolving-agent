import json
from pathlib import Path
from brain.llm_client import llm

class Planner:
    def __init__(self, config_path="configs/planner.json"):
        self.config_path = Path(config_path)

    def create_plan(self, goal: str):
        prompt = f"""
        Kamu adalah Perencana (Planner) Sistem Evolusi SEED.
        Tujuanmu adalah membuat rencana eksekusi langkah-demi-langkah untuk tugas berikut:
        "{goal}"

        Pecah tugas menjadi langkah-langkah kecil yang bisa langsung dikerjakan.
        Kembalikan rencana dalam bentuk list JSON berisi string dalam Bahasa Indonesia.
        Contoh: ["Import library yang dibutuhkan", "Definisikan fungsi utama", "Implementasikan logika", "Verifikasi hasil"]
        PENTING: Gunakan Bahasa Indonesia.
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = llm.completion(messages)
        
        if not response or response == "ERROR_QUOTA":
            return [f"Deconstruct goal: {goal}", "Execute task", "Return results"]
            
        try:
            json_str = llm.extract_json(response)
            if not json_str:
                return [f"Deconstruct goal: {goal}", "Execute task", "Return results"]
            plan = json.loads(json_str)
            if isinstance(plan, list):
                return plan
            return [str(plan)]
        except Exception as e:
            print(f"Error parsing plan: {e}")
            return [f"Deconstruct goal: {goal}", "Execute task", "Return results"]
