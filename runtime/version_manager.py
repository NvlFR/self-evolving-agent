import shutil
from pathlib import Path
from datetime import datetime


class VersionManager:
    def __init__(self, source_dir="brain", versions_dir="versions"):
        self.source_dir = Path(source_dir)
        self.versions_dir = Path(versions_dir)

        self.versions_dir.mkdir(exist_ok=True)

    def create_snapshot(self):
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        snapshot_path = self.versions_dir / f"snapshot_{timestamp}"

        shutil.copytree(self.source_dir, snapshot_path)

        return str(snapshot_path)
