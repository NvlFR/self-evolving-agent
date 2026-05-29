import json
from brain.llm_client import llm
from memory.status_manager import status_manager

class MutationEngine:
    def __init__(self):
        pass

    def generate_repair_mutation(self, issue: dict):
        prompt = f"""
        You are the SEED Evolution System's Repair Engine. 
        Your goal is to fix a reported issue in the codebase.

        Reported Issue:
        Title: {issue['title']}
        Description: {issue['body']}

        Propose a specific code fix. 
        Return your proposal as a JSON object with:
        {{
            "type": "modify_file",
            "file_path": "path/to/file.py",
            "description": "Fix for issue: {issue['title']}",
            "code": "The complete fixed code for the file",
            "instruction": "Apply fix to resolve the reported issue"
        }}
        """
        messages = [{"role": "user", "content": prompt}]
        response = llm.completion(messages, request_type="evolution")
        try:
            json_str = llm.extract_json(response)
            return json.loads(json_str)
        except: return None

    def generate_mutation(self, reflection: dict = None):
        current_context = status_manager.get_context()
        prompt = f"""
        You are the SEED Evolution System's Mutation Engine. 
        {current_context}

        Your goal is to propose a code modification or a new 'tool'...

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
        response = llm.completion(messages, request_type="evolution")
        
        try:
            json_str = llm.extract_json(response)
            mutation_data = json.loads(json_str)
            return mutation_data
        except Exception as e:
            print(f"Error parsing mutation proposal: {e}")
            return None
