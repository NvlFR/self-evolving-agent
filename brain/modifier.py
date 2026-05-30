import json
import os
from pathlib import Path
from brain.llm_client import llm
from brain.github_tool import github_tool
from brain.messenger import messenger

class ProjectManager:
    def __init__(self, projects_dir="projects"):
        self.projects_dir = Path(projects_dir)
        self.active_project_file = Path("memory/active_project.json")

    def check_for_new_projects(self):
        """Scan projects/ for README.md files that haven't been processed."""
        if not self.projects_dir.exists():
            return
            
        for project_path in self.projects_dir.iterdir():
            if project_path.is_dir() and (project_path / "README.md").exists():
                if not self._is_project_started(project_path.name):
                    self.start_new_project(project_path)
        
        # After checking for new ones, execute active project tasks
        self.execute_active_project()

    def execute_active_project(self):
        if not self.active_project_file.exists():
            return
            
        with open(self.active_project_file, "r") as f:
            state = json.load(f)
            
        if state["status"] == "completed":
            return
            
        tasks = state["tasks"]
        idx = state["current_task_index"]
        
        if idx >= len(tasks):
            state["status"] = "completed"
            messenger.send_message(f"🎉 *Project Completed:* {state['name']}")
            self._save_state(state)
            return

        current_task = tasks[idx]
        messenger.send_message(f"🛠️ *Executing Project Task:* {current_task['title']}")
        
        # 1. Research phase (if description looks complex)
        from brain.web_tool import real_world_tool
        research_data = ""
        if "research" in current_task.get("priority", "").lower() or len(current_task['description']) > 100:
            research_data = real_world_tool.search_web(current_task['title'])

        # 2. Coding phase
        code_mutation = self._generate_task_code(state["name"], current_task, research_data)
        
        if code_mutation:
            # Apply to project directory (simulated for now, would be actual file write)
            project_dir = Path(state["path"])
            file_path = project_dir / code_mutation.get("file_path", "solution.py")
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(code_mutation.get("code", "# Error generating code"))
            
            # 3. GitHub PR for the task
            github_tool.commit_and_push(
                f"Task {current_task['id']}: {current_task['title']}", 
                cwd=state["path"]
            )
            
            # 4. Advance index
            state["current_task_index"] += 1
            self._save_state(state)
            messenger.send_message(f"✅ *Task Finished:* {current_task['title']}")

    def _generate_task_code(self, project_name, task, research):
        prompt = f"""
        Kamu adalah Expert Developer yang sedang mengerjakan proyek '{project_name}'.
        Tugas: {task['title']}
        Deskripsi: {task['description']}
        Konteks Riset: {research}

        Tulis kode Python lengkap untuk mengimplementasikan tugas ini.
        Kembalikan sebagai JSON:
        {{
            "file_path": "src/module.py",
            "code": "..."
        }}
        """
        messages = [{"role": "user", "content": prompt}]
        response = llm.completion(messages, request_type="utility")
        try:
            json_str = llm.extract_json(response)
            return json.loads(json_str)
        except: return None

    def _save_state(self, state):
        with open(self.active_project_file, "w") as f:
            json.dump(state, f, indent=2)

    def _is_project_started(self, name):
        if not self.active_project_file.exists():
            return False
        with open(self.active_project_file, "r") as f:
            active = json.load(f)
            return name in active.get("completed_projects", []) or name == active.get("current_project")

    def start_new_project(self, project_dir):
        name = project_dir.name
        readme_content = (project_dir / "README.md").read_text()
        
        messenger.send_message(f"🏗️ *Memulai Proyek Baru:* {name}")
        
        # 1. Create Remote Repo
        github_tool.create_repo(name, f"Proyek otonom yang dibuat oleh SEED: {name}")
        
        # 2. Deconstruct README into Tasks
        tasks = self.generate_project_tasks(name, readme_content)
        
        # 3. Save Project State
        project_state = {
            "name": name,
            "path": str(project_dir),
            "status": "in_progress",
            "tasks": tasks,
            "current_task_index": 0
        }
        
        with open(self.active_project_file, "w") as f:
            json.dump(project_state, f, indent=2)
            
        messenger.send_message(f"📋 *Tugas Proyek Berhasil Dibuat:* {len(tasks)} tugas ditemukan.")

    def generate_project_tasks(self, name, readme):
        prompt = f"""
        Kamu adalah Senior Project Architect. 
        Pecah README Proyek berikut menjadi daftar tugas pemrograman yang granular dan bisa langsung dikerjakan.
        Tujuannya adalah mencapai status 'production-ready'.

        Proyek: {name}
        README:
        {readme}

        Kembalikan list JSON berisi objek:
        [
            {{"id": 1, "title": "Judul tugas dalam Bahasa Indonesia", "description": "Penjelasan detail dalam Bahasa Indonesia", "priority": "high"}},
            ...
        ]
        """
        messages = [{"role": "user", "content": prompt}]
        response = llm.completion(messages, request_type="utility")
        
        try:
            json_str = llm.extract_json(response)
            return json.loads(json_str)
        except:
            return [{"id": 1, "title": "Implementasi logika inti", "description": "Berdasarkan README", "priority": "high"}]

project_manager = ProjectManager()
