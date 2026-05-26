from brain.mutation_engine import MutationEngine
from brain.self_editor import SelfEditor
from runtime.version_manager import VersionManager
from runtime.rollback_manager import RollbackManager
from runtime.benchmark_runner import BenchmarkRunner
from memory.memory_manager import MemoryManager


class AutonomousLoop:
    def __init__(self):
        self.mutation_engine = MutationEngine()
        self.self_editor = SelfEditor()
        self.version_manager = VersionManager()
        self.rollback_manager = RollbackManager()
        self.benchmark_runner = BenchmarkRunner()
        self.memory_manager = MemoryManager()

    def evolve(self, iterations=3):
        evolution_history = []

        for iteration in range(iterations):
            print(f"\n=== Evolution Iteration {iteration + 1} ===")

            snapshot = self.version_manager.create_snapshot()

            mutation = self.mutation_engine.generate_mutation()
            print(f"Generated mutation: {mutation}")

            modification_success = self.self_editor.apply_change(mutation)

            benchmark_results = self.benchmark_runner.run()

            success_score = sum(
                task['score'] for task in benchmark_results
            )

            evolution_step = {
                "iteration": iteration + 1,
                "mutation": mutation,
                "modification_success": modification_success,
                "benchmark_score": success_score,
                "snapshot": snapshot
            }

            evolution_history.append(evolution_step)

            self.memory_manager.store_episode(
                task=f"evolution_iteration_{iteration + 1}",
                result=evolution_step,
                evaluation={"score": success_score}
            )

            if success_score < 1:
                print("Benchmark failed. Rolling back...")
                self.rollback_manager.rollback(snapshot)
            else:
                print("Mutation accepted.")

        return evolution_history
