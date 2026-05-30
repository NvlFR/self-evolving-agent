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
from brain.modifier import project_manager

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
        
        # 0. Check for New Projects from User
        project_manager.check_for_new_projects()
        
        # 0. Self-Repair: Check for open issues to fix before starting new evolution
        open_issues = github_tool.list_issues()
        if open_issues:
            messenger.send_message(f"🛠️ *Mode Perbaikan Otomatis*\nMenemukan {len(open_issues)} issue untuk diperbaiki.")
            for issue in open_issues[:2]: # Fix top 2 issues to avoid loop bloat
                repair_mutation = self.mutation_engine.generate_repair_mutation(issue)
                if repair_mutation and self.safety_guard.validate_mutation(repair_mutation):
                    if self.self_editor.apply_change(repair_mutation):
                        github_tool.close_issue(issue["number"])
                        github_tool.commit_and_push(f"Perbaikan otomatis: {issue['title']}")
                        messenger.send_message(f"✅ *Issue Berhasil Diperbaiki:* {issue['title']}")

        for iteration in range(iterations):
            print(f"\n=== Iterasi Evolusi {iteration + 1} ===")
            
            # Force execute project tasks
            project_manager.execute_active_project()

            # Generate new tasks for this iteration
            new_tasks = self.task_generator.generate_tasks(count=2, difficulty=iteration + 1)
            if new_tasks:
                task_list = "\n".join([f"- {t['goal']}" for t in new_tasks])
                messenger.send_message(f"📝 *Tugas Baru Dibuat:*\n{task_list}")

            # 1. Reflection (Analyze previous episodes)
            episodes = self.memory_manager.load_memories()
            reflection = self.reflection_engine.reflect_on_episodes(episodes)
            print(f"Hasil refleksi: {reflection['insights']}")
            messenger.send_message(f"🧠 *Pengetahuan/Insight Baru:*\n{reflection['insights']}")

            # 2. Mutation Generation
            mutation = self.mutation_engine.generate_mutation(reflection)
            print(f"Usulan mutasi: {mutation}")
            
            if mutation == "ERROR_QUOTA":
                print("🛑 Kuota habis saat pembuatan mutasi. Melewati iterasi.")
                continue

            if mutation and mutation.get("type") == "research":
                from brain.web_tool import real_world_tool
                query = mutation.get("query", "cara meningkatkan agen AI")
                
                # Perform research
                web_results = real_world_tool.search_web(query)
                git_results = real_world_tool.search_github_code(query)
                
                # Feed research back to AI for an actual code change
                research_context = f"Hasil riset untuk '{query}':\nWeb: {web_results}\nGitHub: {git_results}"
                messenger.send_message(f"🧪 *Sedang Melakukan Riset:* {query}\nMengirim hasil riset ke otak...")
                
                reflection["research_data"] = research_context
                mutation = self.mutation_engine.generate_mutation(reflection)
                print(f"Mutasi setelah riset: {mutation}")

            if not mutation:
                # Only create issue if it's a real failure, not a quota error
                if reflection.get("insights") != "Quota reached or LLM error. Skipping reflection.":
                    github_tool.create_issue(
                        f"Evolusi Gagal - Iterasi {iteration + 1}",
                        f"Mesin Mutasi gagal menghasilkan usulan.\nRefleksi: {reflection['insights']}"
                    )
                continue

            # 3. Safety Check
            if not self.safety_guard.validate_mutation(mutation):
                print("Mutasi diblokir oleh Safety Guard!")
                github_tool.create_issue(
                    f"Pelanggaran Keamanan - Iterasi {iteration + 1}",
                    f"Mutasi diblokir: {mutation.get('description', 'Tanpa deskripsi')}"
                )
                continue

            # 4. Snapshot
            snapshot = self.version_manager.create_snapshot()

            # 5. Apply Modification
            modification_success = self.self_editor.apply_change(mutation)
            if modification_success:
                desc = mutation.get('description', 'Peningkatan diri')
                github_tool.commit_and_push(f"Evolusi Iterasi {iteration + 1} (Uji Coba): {desc}")
                messenger.send_message(f"🚀 *Mutasi Diterapkan & Push:*\n{desc}\nPengujian dimulai sekarang...")

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
                print(f"Menerapkan penalti pengulangan: -{penalty:.2f}")
                success_score -= penalty

            print(f"Skor akhir iterasi: {success_score:.2f}")

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
                task=f"evolusi_iterasi_{iteration + 1}",
                result=evolution_step,
                evaluation=evaluation
            )

            # 8. Keep or Rollback
            if success_score < 0.6: 
                print("Tekanan seleksi: Generasi ditolak. Melakukan rollback...")
                self.rollback_manager.rollback(snapshot)
                self.self_model_manager.update_weakness(f"Generasi ditolak: {mutation}")
                github_tool.commit_and_push(f"Rollback Iterasi {iteration + 1}: Performa di bawah ambang batas ({success_score:.2f})")
                github_tool.create_issue(
                    f"Rollback Evolusi - Iteration {iteration + 1}",
                    f"Skor: {success_score:.2f}. Mutasi ditolak dan dibatalkan.\nMutasi: {mutation.get('description')}"
                )
            else:
                print("Tekanan seleksi: Generasi diterima.")
                self.self_model_manager.update_strength(f"Evolusi berhasil: {mutation}")
                github_tool.commit_and_push(f"Evolusi Iterasi {iteration + 1} (Terkonfirmasi): {mutation.get('description')}")

        return evolution_history
