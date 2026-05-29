import json
from brain.llm_client import llm

class MutationEngine:
    def __init__(self):
        pass

    def generate_mutation(self, reflection: dict = None):
        prompt = f"""
        You are the SEED Evolution System's Mutation Engine. 
        Your goal is to propose a code modification or a new 'tool' (Python class/function) 
        to improve the agent's performance or capabilities.

        Current Reflection/Analysis:
        {json.dumps(reflection, indent=2) if reflection else "No previous reflection. Focus on general improvement."}

        Propose a specific change. The change should be one of:
        1. 'modify_file': Change existing code in a file.
        2. 'create_tool': Create a new Python file in the 'brain/' directory with a new capability.

        Return your proposal as a JSON object with:
        {{
            "type": "modify_file" | "create_tool",
            "file_path": "path/to/file.py",
            "description": "Brief explanation",
            "code": "The complete new code or the specific replacement code",
            "instruction": "Instructions for applying the change"
        }}
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = llm.completion(messages)
        
        try:
            json_str = llm.extract_json(response)
            mutation_data = json.loads(json_str)
            return mutation_data
        except Exception as e:
            print(f"Error parsing mutation proposal: {e}")
            return None
