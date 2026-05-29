import json
import os
from pathlib import Path

class SelfEditor:
    def __init__(self):
        pass

    def apply_change(self, mutation: dict):
        if not mutation or not isinstance(mutation, dict):
            return False
            
        m_type = mutation.get("type")
        file_path = mutation.get("file_path")
        code = mutation.get("code")
        
        if not file_path or not code:
            return False
            
        path = Path(file_path)
        
        # Safety check: only allow modifications within the project, 
        # specifically brain/ or runtime/ or memory/ or tasks/
        allowed_dirs = ["brain", "runtime", "memory", "tasks"]
        is_safe = any(str(path).startswith(d) for d in allowed_dirs)
        
        if not is_safe:
            print(f"Safety violation: Attempted to modify {file_path}")
            return False

        try:
            if m_type == "create_tool":
                # Create parent directories if they don't exist
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(code)
                print(f"Created new tool: {file_path}")
                return True
                
            elif m_type == "modify_file":
                # For now, we overwrite the file for simplicity in this prototype.
                # In a more advanced version, we'd use surgical replacement.
                path.write_text(code)
                print(f"Modified file: {file_path}")
                return True
                
            return False
        except Exception as e:
            print(f"Error applying change to {file_path}: {e}")
            return False
