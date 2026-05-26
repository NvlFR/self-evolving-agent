from brain.mutation_engine import MutationEngine
from brain.self_editor import SelfEditor
from runtime.version_manager import VersionManager
from runtime.rollback_manager import RollbackManager
from runtime.benchmark_runner import BenchmarkRunner
from memory.memory_manager import MemoryManager
from brain.adaptive_evaluator import AdaptiveEvaluator
from brain.reflection import ReflectionEngine
from runtime.safety_guard import SafetyGuard
from memory.self_model_manager import SelfModelManager

class AutonomousLoop:
    def __init__(self):
        self.mutation_engine = MutationEngine()
        self.self_editor = SelfEditor()
        self.version_manager = VersionManager()
        self.rollback_manager = RollbackManager()
        self.benchmark_runner = BenchmarkRunner()
        self.memory_manager = MemoryManager()
        self.evaluator = AdaptiveEvaluator()
        self.reflection_engine = ReflectionEngine()
        self.safety_guard = SafetyGuard()
        self.self_model_manager = SelfModelManager()

    def evolve(self, iterations=3):
        evolution_history = []

        for iteration in range(iterations):
            print(f"\n=== Evolution Iteration {iteration + 1} ===")

            # 1. Reflection (Analyze previous episodes)
            episodes = self.memory_manager.load_memories()
            reflection = self.reflection_engine.reflect_on_episodes(episodes)
            print(f"Reflection insight: {reflection['insights']}")

            # 2. Mutation Generation
            mutation = self.mutation_engine.generate_mutation(reflection)
            print(f"Proposed mutation: {mutation}")

            # 3. Safety Check
            if not self.safety_guard.validate_mutation(mutation):
                print("Mutation blocked by safety guard!")
                continue

            # 4. Snapshot
            snapshot = self.version_manager.create_snapshot()

            # 5. Apply Modification
            modification_success = self.self_editor.apply_change(mutation)

            # 6. Benchmark & Evaluate
            benchmark_results = self.benchmark_runner.run()
            
            # Aggregate scores
            avg_success = sum(1 for res in benchmark_results if res["success"]) / len(benchmark_results)
            avg_runtime = sum(res["runtime"] for res in benchmark_results) / len(benchmark_results)
            
            evaluation = self.evaluator.evaluate_with_context(
                success=avg_success > 0.5, # Simplified success criteria
                runtime=avg_runtime,
                errors=0 # Simplified
            )
            
            success_score = evaluation["score"]
            print(f"Iteration score: {success_score:.2f}")

            evolution_step = {
                "iteration": iteration + 1,
                "mutation": mutation,
                "modification_success": modification_success,
                "benchmark_score": success_score,
                "snapshot": snapshot,
                "evaluation": evaluation
            }

            evolution_history.append(evolution_step)

            # 7. Memory Storage
            self.memory_manager.store_episode(
                task=f"evolution_iteration_{iteration + 1}",
                result=evolution_step,
                evaluation=evaluation
            )

            # 8. Keep or Rollback
            if success_score < 0.5: # Threshold for rollback
                print("Performance degraded. Rolling back...")
                self.rollback_manager.rollback(snapshot)
                self.self_model_manager.update_weakness(f"Failed mutation: {mutation}")
            else:
                print("Evolution step accepted.")
                self.self_model_manager.update_strength(f"Successful mutation: {mutation}")

        return evolution_history
