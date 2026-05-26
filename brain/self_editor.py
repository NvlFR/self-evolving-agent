import json
from pathlib import Path

class SelfEditor:
    def __init__(self):
        self.planner_config = Path("configs/planner.json")
        self.target_file = Path("brain/planner.py")

    def apply_change(self, mutation: str):
        # Check if it's a planner mutation
        if "planner mutation" in mutation.lower():
            return self._apply_planner_mutation(mutation)
        
        # Fallback to legacy source modification
        if not self.target_file.exists():
            return False
        content = self.target_file.read_text()
        content += f"\n# Self modification note: {mutation}\n"
        self.target_file.write_text(content)
        return True

    def _apply_planner_mutation(self, mutation: str):
        if not self.planner_config.exists():
            # Create default if missing
            default = {"include_analysis": True, "include_validation": True, "max_steps": 5}
            self.planner_config.write_text(json.dumps(default, indent=2))

        try:
            with open(self.planner_config, "r+") as f:
                config = json.load(f)
                
                if "enable include_validation" in mutation:
                    config["include_validation"] = True
                elif "disable include_analysis" in mutation:
                    config["include_analysis"] = False
                elif "increase max_steps" in mutation:
                    config["max_steps"] = min(20, config.get("max_steps", 5) + 2)
                elif "reduce max_steps" in mutation:
                    config["max_steps"] = max(1, config.get("max_steps", 5) - 2)
                
                f.seek(0)
                json.dump(config, f, indent=2)
                f.truncate()
            return True
        except:
            return False
