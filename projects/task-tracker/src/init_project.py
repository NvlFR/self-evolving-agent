import os
import json

def init_task_tracker_project(base_dir="task-tracker"):
    """Inisialisasi struktur proyek task-tracker."""
    
    # Struktur direktori
    dirs = [
        "",
        "src",
        "src/modules",
        "src/modules/auth",
        "src/modules/tasks",
        "src/modules/notifications",
        "tests",
        "tests/unit",
        "tests/integration",
        "config",
        "docs",
    ]
    
    for d in dirs:
        path = os.path.join(base_dir, d)
        os.makedirs(path, exist_ok=True)
        print(f"[DIR]  {path}/")
    
    # package.json
    package_json = {
        "name": "task-tracker",
        "version": "1.0.0",
        "description": "Aplikasi task tracking sederhana",
        "main": "index.js",
        "scripts": {
            "start": "node index.js",
            "test": "node --test tests/"
        },
        "keywords": ["task", "tracker", "productivity"],
        "author": "ZOO Developer",
        "license": "MIT",
        "dependencies": {},
        "devDependencies": {}
    }
    
    pkg_path = os.path.join(base_dir, "package.json")
    with open(pkg_path, "w") as f:
        json.dump(package_json, f, indent=2)
    print(f"[FILE] {pkg_path}")
    
    # index.js (entry point utama)
    index_js = """const { AuthModule } = require('./src/modules/auth/auth');
const { TaskModule } = require('./src/modules/tasks/tasks');
const { NotificationModule } = require('./src/modules/notifications/notifications');

async function main() {
    console.log('Task Tracker v1.0.0');
    console.log('====================');

    const auth = new AuthModule();
    const tasks = new TaskModule();
    const notifications = new NotificationModule();

    await auth.init();
    await tasks.init();
    await notifications.init();

    console.log('Semua modul berhasil diinisialisasi.');
}

main().catch(console.error);
"""
    
    index_path = os.path.join(base_dir, "index.js")
    with open(index_path, "w") as f:
        f.write(index_js)
    print(f"[FILE] {index_path}")
    
    # Modul auth
    auth_init = """// src/modules/auth/index.js
const AuthModule = require('./auth');
module.exports = { AuthModule };
"""
    auth_mod = """// src/modules/auth/auth.js
class AuthModule {
    constructor() {
        this.user = null;
    }

    async init() {
        console.log('[Auth] Modul autentikasi diinisialisasi.');
    }

    async login(username, password) {
        console.log(`[Auth] Login: ${username}`);
        this.user = { username };
        return this.user;
    }

    async logout() {
        console.log('[Auth] Logout.');
        this.user = null;
    }
}

module.exports = { AuthModule };
"""
    
    auth_dir = os.path.join(base_dir, "src", "modules", "auth")
    with open(os.path.join(auth_dir, "index.js"), "w") as f:
        f.write(auth_init)
    with open(os.path.join(auth_dir, "auth.js"), "w") as f:
        f.write(auth_mod)
    print(f"[FILE] {auth_dir}/index.js")
    print(f"[FILE] {auth_dir}/auth.js")
    
    # Modul tasks
    tasks_init = """// src/modules/tasks/index.js
const TaskModule = require('./tasks');
module.exports = { TaskModule };
"""
    tasks_mod = """// src/modules/tasks/tasks.js
class TaskModule {
    constructor() {
        this.tasks = [];
    }

    async init() {
        console.log('[Tasks] Modul task diinisialisasi.');
    }

    addTask(title, description) {
        const task = { id: this.tasks.length + 1, title, description, done: false };
        this.tasks.push(task);
        console.log(`[Tasks] Ditambahkan: ${title}`);
        return task;
    }

    listTasks() {
        return this.tasks;
    }

    completeTask(id) {
        const task = this.tasks.find(t => t.id === id);
        if (task) task.done = true;
        return task;
    }
}

module.exports = { TaskModule };
"""
    
    tasks_dir = os.path.join(base_dir, "src", "modules", "tasks")
    with open(os.path.join(tasks_dir, "index.js"), "w") as f:
        f.write(tasks_init)
    with open(os.path.join(tasks_dir, "tasks.js"), "w") as f:
        f.write(tasks_mod)
    print(f"[FILE] {tasks_dir}/index.js")
    print(f"[FILE] {tasks_dir}/tasks.js")
    
    # Modul notifications
    notif_init = """// src/modules/notifications/index.js
const NotificationModule = require('./notifications');
module.exports = { NotificationModule };
"""
    notif_mod = """// src/modules/notifications/notifications.js
class NotificationModule {
    constructor() {
        this.enabled = true;
    }

    async init() {
        console.log('[Notifications] Modul notifikasi diinisialisasi.');
    }

    notify(message) {
        if (this.enabled) {
            console.log(`[Notifications] ${message}`);
        }
    }
}

module.exports = { NotificationModule };
"""
    
    notif_dir = os.path.join(base_dir, "src", "modules", "notifications")
    with open(os.path.join(notif_dir, "index.js"), "w") as f:
        f.write(notif_init)
    with open(os.path.join(notif_dir, "notifications.js"), "w") as f:
        f.write(notif_mod)
    print(f"[FILE] {notif_dir}/index.js")
    print(f"[FILE] {notif_dir}/notifications.js")
    
    # README
    readme = """# Task Tracker
\n## Deskripsi\nAplikasi task tracking sederhana.\n\n## Instalasi\n```bash\nnpm install\n```\n\n## Menjalankan\n```bash\nnpm start\n```\n\n## Struktur Proyek\n```\ntask-tracker/\n├── index.js\n├── package.json\n├── src/\n│   └── modules/\n│       ├── auth/\n│       ├── tasks/\n│       └── notifications/\n├── tests/\n│   ├── unit/\n│   └── integration/\n├── config/\n└── docs/\n```\n"""
    
    readme_path = os.path.join(base_dir, "README.md")
    with open(readme_path, "w") as f:
        f.write(readme)
    print(f"[FILE] {readme_path}")
    
    print("\n✅ Proyek 'task-tracker' berhasil diinisialisasi!")

if __name__ == "__main__":
    init_task_tracker_project()
