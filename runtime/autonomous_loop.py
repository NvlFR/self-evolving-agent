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
from tasks.task_generator import TaskGenerator
from brain.github_tool import github_tool
from brain.messenger import messenger

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
        self.task_generator = TaskGenerator()

    def evolve(self, iterations=3):
        evolution_history = []
        
        # 0. Self-Repair: Check for open issues to fix before starting new evolution
        open_issues = github_tool.list_issues()
        if open_issues:
            messenger.send_message(f"🛠️ *Autonomous Repair Mode*\nFound {len(open_issues)} issues to fix.")
            for issue in open_issues[:2]: # Fix top 2 issues to avoid loop bloat
                repair_mutation = self.mutation_engine.generate_repair_mutation(issue)
                if repair_mutation and self.safety_guard.validate_mutation(repair_mutation):
                    if self.self_editor.apply_change(repair_mutation):
                        github_tool.close_issue(issue["number"])
                        github_tool.commit_and_push(f"Auto-repair: {issue['title']}")
                        messenger.send_message(f"✅ *Fixed Issue:* {issue['title']}")

        for iteration in range(iterations):
            print(f"\n=== Evolution Iteration {iteration + 1} ===")

            # Generate new tasks for this iteration
            new_tasks = self.task_generator.generate_tasks(count=2, difficulty=iteration + 1)
            if new_tasks:
                task_list = "\n".join([f"- {t['goal']}" for t in new_tasks])
                messenger.send_message(f"📝 *New Tasks Generated:*\n{task_list}")

            # 1. Reflection (Analyze previous episodes)
            episodes = self.memory_manager.load_memories()
            reflection = self.reflection_engine.reflect_on_episodes(episodes)
            print(f"Reflection insight: {reflection['insights']}")
            messenger.send_message(f"🧠 *New Knowledge/Insight:*\n{reflection['insights']}")

            # 2. Mutation Generation
            mutation = self.mutation_engine.generate_mutation(reflection)
            print(f"Proposed mutation: {mutation}")
            
            if mutation == "ERROR_QUOTA":
                print("🛑 Quota reached during mutation generation. Skipping iteration.")
                continue

            if not mutation:
                # Only create issue if it's a real failure, not a quota error
                if reflection.get("insights") != "Quota reached or LLM error. Skipping reflection.":
                    github_tool.create_issue(
                        f"Evolution Failed - Iteration {iteration + 1}",
                        f"Mutation Engine failed to generate a proposal.\nReflection: {reflection['insights']}"
                    )
                continue

            # 3. Safety Check
            if not self.safety_guard.validate_mutation(mutation):
                print("Mutation blocked by safety guard!")
                github_tool.create_issue(
                    f"Safety Violation - Iteration {iteration + 1}",
                    f"Mutation blocked: {mutation.get('description', 'No description')}"
                )
                continue

            # 4. Snapshot
            snapshot = self.version_manager.create_snapshot()

            # 5. Apply Modification
            modification_success = self.self_editor.apply_change(mutation)
            if modification_success:
                desc = mutation.get('description', 'Self-improvement')
                github_tool.commit_and_push(f"Evolution Iteration {iteration + 1} (Trial): {desc}")
                messenger.send_message(f"🚀 *Mutation Applied & Pushed:*\n{desc}\nTesting starts now...")

            # 6. Benchmark & Evaluate
            benchmark_results = self.benchmark_runner.run()
            
            # Aggregate scores
            avg_success = sum(1 for res in benchmark_results if res["success"]) / len(benchmark_results)
            avg_runtime = sum(res["runtime"] for res in benchmark_results) / len(benchmark_results)
            
            evaluation = self.evaluator.evaluate_with_context(
                success=avg_success > 0.7, 
                runtime=avg_runtime,
                errors=0 
            )
            
            success_score = evaluation["score"]
            
            # Selection Pressure: Penalize repeated mutations
            mutation_count = sum(1 for step in evolution_history if step["mutation"] == mutation)
            if mutation_count > 0:
                penalty = 0.1 * mutation_count
                print(f"Applying repetition penalty: -{penalty:.2f}")
                success_score -= penalty

            print(f"Iteration final score: {success_score:.2f}")

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
            if success_score < 0.6: 
                print("Selection pressure: Generation rejected. Rolling back...")
                self.rollback_manager.rollback(snapshot)
                self.self_model_manager.update_weakness(f"Rejected generation: {mutation}")
                github_tool.commit_and_push(f"Rollback Iteration {iteration + 1}: Performance below threshold ({success_score:.2f})")
                github_tool.create_issue(
                    f"Evolution Rollback - Iteration {iteration + 1}",
                    f"Score: {success_score:.2f}. Mutation rejected and rolled back.\nMutation: {mutation.get('description')}"
                )
            else:
                print("Selection pressure: Generation accepted.")
                self.self_model_manager.update_strength(f"Successful evolution: {mutation}")
                github_tool.commit_and_push(f"Evolution Iteration {iteration + 1} (Confirmed): {mutation.get('description')}")

        return evolution_history
