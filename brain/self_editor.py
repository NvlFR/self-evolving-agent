from pathlib import Path


class SelfEditor:
    def __init__(self):
        self.target_file = Path("brain/planner.py")

    def apply_change(self, change_description: str):
        if not self.target_file.exists():
            return False

        content = self.target_file.read_text()

        content += f"\n# Self modification note: {change_description}\n"

        self.target_file.write_text(content)

        return True
