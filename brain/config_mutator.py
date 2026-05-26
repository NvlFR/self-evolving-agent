import json
import random
from pathlib import Path


class ConfigMutator:
    def __init__(self):
        self.planner_config = Path("configs/planner.json")

    def mutate_planner_config(self):
        config = json.loads(self.planner_config.read_text())

        mutation = random.choice([
            "include_analysis",
            "include_validation"
        ])

        config[mutation] = not config[mutation]

        self.planner_config.write_text(
            json.dumps(config, indent=2)
        )

        return f"planner config mutation: toggle {mutation}"
