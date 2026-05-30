import os
import subprocess
import json
from dotenv import load_dotenv

load_dotenv(override=True)

class GitHubTool:
    def __init__(self):
        self.token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
        if self.token:
            # Authenticate gh cli with the token
            try:
                subprocess.run(
                    ["gh", "auth", "login", "--with-token"],
                    input=self.token.encode(),
                    check=True,
                    capture_output=True
                )
            except Exception as e:
                print(f"GitHub Auth Error: {e}")

    def create_issue(self, title, body, cwd=None):
        try:
            result = subprocess.run(
                ["gh", "issue", "create", "--title", title, "--body", body],
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd
            )
            print(f"GitHub Issue Created: {result.stdout.strip()}")
            return True
        except Exception as e:
            print(f"Error creating GitHub issue: {e}")
            return False

    def create_repo(self, name, description, private=False):
        try:

            visibility = "--private" if private else "--public"
            subprocess.run(
                ["gh", "repo", "create", name, visibility, "--description", description],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"GitHub Repo Created: {name}")
            return True
        except subprocess.CalledProcessError as e:
            if "already exists" in e.stderr:
                print(f"GitHub Repo '{name}' already exists (caught by creation error).")
                return True
            print(f"Error creating GitHub repo: {e.stderr}")
            return False


            print(f"Error creating GitHub repo: {e}")

            # Cek apakah repo sudah ada
            subprocess.run(["gh", "repo", "view", name], capture_output=True, check=True)
            print(f"GitHub Repo '{name}' already exists.")
            return True
        except subprocess.CalledProcessError:
            # Repo tidak ditemukan, lanjut buat baru
            try:
                visibility = "--private" if private else "--public"
                subprocess.run(
                    ["gh", "repo", "create", name, visibility, "--description", description, "--confirm"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                print(f"GitHub Repo Created: {name}")
                return True
            except Exception as e:
                print(f"Error creating GitHub repo: {e}")
                return False
        except Exception as e:
            print(f"Error checking GitHub repo: {e}")

            return False

    def commit_and_push(self, message, cwd=None):
        try:
            import time
            branch_name = f"evolution-{int(time.time())}"
            subprocess.run(["git", "checkout", "-b", branch_name], check=True, cwd=cwd)
            subprocess.run(["git", "add", "."], check=True, cwd=cwd)
            subprocess.run(["git", "commit", "-m", message], check=True, cwd=cwd)
            subprocess.run(["git", "push", "-u", "origin", branch_name], check=True, cwd=cwd)
            
            pr_result = subprocess.run(
                ["gh", "pr", "create", "--title", message, "--body", f"Autonomous improvement from SEED System.\n\nDetails: {message}", "--base", "main"],
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd
            )
            print(f"GitHub PR Created: {pr_result.stdout.strip()}")
            subprocess.run(["git", "checkout", "main"], check=True, cwd=cwd)
            return True
        except Exception as e:
            if "nothing to commit" in str(e).lower():
                subprocess.run(["git", "checkout", "main"], capture_output=True, cwd=cwd)
                return True
            print(f"Error during git PR creation: {e}")
            subprocess.run(["git", "checkout", "main"], capture_output=True, cwd=cwd)
            return False

    def list_issues(self, cwd=None):
        try:
            result = subprocess.run(
                ["gh", "issue", "list", "--json", "number,title,body", "--state", "open"],
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd
            )
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error listing GitHub issues: {e}")
            return []

    def close_issue(self, issue_number, cwd=None):
        try:
            subprocess.run(["gh", "issue", "close", str(issue_number)], check=True, cwd=cwd)
            return True
        except Exception as e:
            print(f"Error closing issue {issue_number}: {e}")
            return False

github_tool = GitHubTool()
