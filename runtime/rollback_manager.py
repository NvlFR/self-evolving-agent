from pathlib import Path
import shutil


class RollbackManager:
    def rollback(self, snapshot_path: str, target_dir: str = "brain"):
        target = Path(target_dir)

        if target.exists():
            shutil.rmtree(target)

        shutil.copytree(snapshot_path, target)

        return True
