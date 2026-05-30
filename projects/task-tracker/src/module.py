"""
Task Tracker - Main Module

This module handles the core project initialization and directory structure setup
for the task-tracker project.
"""
import os
import json
from pathlib import Path


def create_project_structure(base_dir="task-tracker"):
    """
    Creates the boilerplate project structure with necessary directories and files.
    
    Args:
        base_dir (str): The root directory for the project.
    
    Returns:
        dict: A dictionary containing the paths of created directories and files.
    """
    # Define directory structure
    directories = [
        os.path.join(base_dir, "src"),
        os.path.join(base_dir, "tests"),
        os.path.join(base_dir, "data"),
    ]
    
    # Create directories
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create entry point main file
    main_file = os.path.join(base_dir, "src", "main.py")
    main_code = '''#!/usr/bin/env python3
"""Entry point for the task-tracker application."""

def main():
    print("Task Tracker is running!")

if __name__ == "__main__":
    main()
'''
    with open(main_file, "w") as f:
        f.write(main_code)
    print(f"Created file: {main_file}")
    
    # Create requirements file
    requirements_file = os.path.join(base_dir, "requirements.txt")
    requirements_content = "# Dependencies for task-tracker project"
    with open(requirements_file, "w") as f:
        f.write(requirements_content)
    print(f"Created file: {requirements_file}")
    
    # Create README
    readme_file = os.path.join(base_dir, "README.md")
    readme_content = "# Task Tracker\n\nA simple task tracking application."
    with open(readme_file, "w") as f:
        f.write(readme_content)
    print(f"Created file: {readme_file}")
    
    return {
        "directories": directories,
        "files": [main_file, requirements_file, readme_file]
    }


if __name__ == "__main__":
    create_project_structure()
