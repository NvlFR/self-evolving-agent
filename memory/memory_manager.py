import json
from pathlib import Path
from datetime import datetime


class MemoryManager:
    def __init__(self, memory_path="memory/episodes.json"):
        self.memory_path = Path(memory_path)

        if not self.memory_path.exists():
            self.memory_path.write_text("[]")

    def load_memories(self):
        with open(self.memory_path, "r") as f:
            return json.load(f)

    def store_episode(self, task, result, evaluation):
        memories = self.load_memories()

        memories.append({
            "timestamp": datetime.utcnow().isoformat(),
            "task": task,
            "result": result,
            "evaluation": evaluation
        })

        with open(self.memory_path, "w") as f:
            json.dump(memories, f, indent=2)
