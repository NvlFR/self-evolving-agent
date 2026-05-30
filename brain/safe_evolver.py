"""
safe_evolver.py - Evolution guard layer. Freeze pipeline when score high.
Produces complete executable Python code only. No placeholders.
Rewritten from scratch based on post-mortem of evolution_epoch_seed_02.md findings.
"""

import ast
import copy
import hashlib
import importlib
import inspect
import textwrap
from pathlib import Path
from typing import Any, Optional


class SafeEvolver:
    """Evolution controller that protects high-performing agents."""

    SCORE_THRESHOLD = 1.0

    def __init__(self, target_path: str, score_threshold: float = 1.0):
        self.target_path = Path(target_path)
        self.score_threshold = score_threshold
        self._target_module = None

    def load_target(self):
        """Import target module for mutation."""
        import sys
        brain_dir = str(self.target_path.parent)
        if brain_dir not in sys.path:
            sys.path.insert(0, brain_dir)
        module_name = self.target_path.stem
        self._target_module = importlib.import_module(module_name)
        return self._target_module

    def should_skip_mutation(self, current_score: float) -> bool:
        """Guard: skip all mutation if score exceeds threshold."""
        if current_score > self.score_threshold:
            return True
        return False

    def validate_code_complete(self, code: str) -> bool:
        """Ensure generated code is syntactically valid Python."""
        try:
            compile(code, str(self.target_path), "exec")
            ast.parse(code)
            return True
        except (SyntaxError, ValueError):
            return False

    def validate_no_placeholders(self, code: str) -> bool:
        """Reject code containing pseudo-instruction placeholders."""
        bad_patterns = [
            "# ... existing code ...",
            "# MODIFIKASI",
            "# TAMBAHKAN",
            "# TODO",
            "# placeholder",
            "# PLACEHOLDER",
            "... existing ...",
        ]
        for pattern in bad_patterns:
            if pattern.lower() in code.lower():
                return False
        return True

    def read_current_code(self) -> str:
        """Read full content of target file."""
        return self.target_path.read_text()

    def write_full_file(self, new_code: str) -> None:
        """Write complete file. Never write snippets."""
        if not self.validate_code_complete(new_code):
            raise ValueError("[ABORT] Generated code is not complete Python."
                             " Cannot write incomplete file.")
        if not self.validate_no_placeholders(new_code):
            raise ValueError("[ABORT] Code contains placeholder/pseudo-instruction markers."
                             " Generate real implementation.")
        self.target_path.write_text(new_code)

    def maybe_evolve(self, current_score: float, proposed_code: Optional[str] = None) -> dict:
        """Main entry: decide whether to evolve or freeze."""
        result = {
            "action": "frozen",
            "reason": "",
            "score": current_score,
            "threshold": self.score_threshold,
        }

        if self.should_skip_mutation(current_score):
            result["reason"] = (
                f"Score {current_score} > threshold {self.score_threshold}. "
                "Mutation skipped. Architecture preserved."
            )
            return result

        if proposed_code is None:
            result["action"] = "no_candidate"
            result["reason"] = "No proposed code provided. Nothing to do."
            return result

        if self.validate_code_complete(proposed_code) and self.validate_no_placeholders(proposed_code):
            self.write_full_file(proposed_code)
            result["action"] = "evolved"
            result["reason"] = "Code passed validation. File replaced."
        else:
            result["action"] = "rejected"
            result["reason"] = "Generated code failed completeness or placeholder check."

        return result


def get_fitness_with_novelty_separated(
    agent_result: dict,
    novelty_archive: list,
) -> dict:
    """
    Compute fitness with novelty as secondary criterion, NOT additive term.
    Prevents inferior but novel agents from beating objectively better ones.
    """
    primary_fitness = agent_result.get("score", 0.0)

    novelty_estimate = 0.0
    if novelty_archive:
        agent_repr = hashlib.md5(
            str(agent_result.get("decision_log", "")).encode()
        ).hexdigest()
        novelty_estimate = 0.1 if agent_repr not in novelty_archive else 0.0
        novelty_archive.append(agent_repr)

    return {
        "primary_fitness": primary_fitness,
        "novelty_estimate": novelty_estimate,
        "combined_for_display": primary_fitness + novelty_estimate,
        "selection_key": primary_fitness,
        "novelty_used_for_tiebreak_only": True,
    }


def main():
    """Demo guard behavior."""
    demo_score = 1.03
    threshold = SafeEvolver.SCORE_THRESHOLD

    if demo_score > threshold:
        print(f"[GUARD] Skor {demo_score} > {threshold}. Mutasi dibekukan.")
        print("[GUARD] Arsitektur dipertahankan. Tidak ada modifikasi.")
    else:
        print(f"[EVOLVE] Skor {demo_score} <= {threshold}. Mutasi diizinkan.")


if __name__ == "__main__":
    main()
