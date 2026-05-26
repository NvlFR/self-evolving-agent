import json
from pathlib import Path


class SelfModelManager:
    def __init__(self, model_path="memory/self_model.json"):
        self.model_path = Path(model_path)

    def load(self):
        with open(self.model_path, "r") as f:
            return json.load(f)

    def update_weakness(self, weakness: str):
        model = self.load()

        if weakness not in model["weaknesses"]:
            model["weaknesses"].append(weakness)

        self._save(model)

    def update_strength(self, strength: str):
        model = self.load()

        if strength not in model["strengths"]:
            model["strengths"].append(strength)

        self._save(model)

    def _save(self, model):
        with open(self.model_path, "w") as f:
            json.dump(model, f, indent=2)
