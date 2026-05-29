import json
from pathlib import Path

class StatusManager:
    def __init__(self, file_path="memory/status.json"):
        self.file_path = Path(file_path)
        self.status = self._load()

    def _load(self):
        if self.file_path.exists():
            with open(self.file_path, "r") as f:
                return json.load(f)
        return {"epoch": 1, "stage": "Exploration", "total_cycles": 0}

    def increment_epoch(self):
        self.status["epoch"] += 1
        self.status["total_cycles"] += 1
        # Update stage based on epoch
        if self.status["epoch"] <= 2:
            self.status["stage"] = "Initial Stability & Tools"
        elif self.status["epoch"] <= 5:
            self.status["stage"] = "Advanced Capability Expansion"
        else:
            self.status["stage"] = "Deep Optimization & Meta-Evolution"
        self._save()

    def _save(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, "w") as f:
            json.dump(self.status, f, indent=2)

    def get_context(self):
        return f"Current Epoch: {self.status['epoch']}, Evolution Stage: {self.status['stage']}"

status_manager = StatusManager()
