import os
import subprocess
import json

def init_project():
    base = 'task-tracker'
    dirs = ['src', 'tests', 'data']
    for d in dirs:
        os.makedirs(os.path.join(base, d), exist_ok=True)
    subprocess.run(['npm', 'init', '-y'], cwd=base)
    deps = ['commander', 'chalk', 'jest']
    subprocess.run(['npm', 'install'] + deps, cwd=base)
    print('Done')

if __name__ == '__main__':
    init_project()
