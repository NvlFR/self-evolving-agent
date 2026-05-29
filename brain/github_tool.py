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

    def create_issue(self, title, body):
        try:
            result = subprocess.run(
                ["gh", "issue", "create", "--title", title, "--body", body],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"GitHub Issue Created: {result.stdout.strip()}")
            return True
        except Exception as e:
            print(f"Error creating GitHub issue: {e}")
            return False

    def commit_and_push(self, message):
        try:
            # Generate a unique branch name for this evolution
            import time
            branch_name = f"evolution-{int(time.time())}"
            
            # Create and switch to new branch
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
            
            # Stage changes
            subprocess.run(["git", "add", "."], check=True)
            
            # Commit
            subprocess.run(["git", "commit", "-m", message], check=True)
            
            # Push new branch
            subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)
            
            # Create Pull Request
            pr_result = subprocess.run(
                ["gh", "pr", "create", "--title", message, "--body", f"Autonomous improvement from SEED System.\n\nDetails: {message}", "--base", "main"],
                capture_output=True,
                text=True,
                check=True
            )
            
            print(f"GitHub PR Created: {pr_result.stdout.strip()}")
            
            # Switch back to main for the next cycle
            subprocess.run(["git", "checkout", "main"], check=True)
            
            return True
        except Exception as e:
            if "nothing to commit" in str(e).lower():
                # If nothing to commit, just stay on main
                subprocess.run(["git", "checkout", "main"], capture_output=True)
                return True
            print(f"Error during git PR creation: {e}")
            # Ensure we are back on main even on error
            subprocess.run(["git", "checkout", "main"], capture_output=True)
            return False

    def list_issues(self):
        try:
            result = subprocess.run(
                ["gh", "issue", "list", "--json", "number,title,body", "--state", "open"],
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error listing GitHub issues: {e}")
            return []

    def close_issue(self, issue_number):
        try:
            subprocess.run(["gh", "issue", "close", str(issue_number)], check=True)
            return True
        except Exception as e:
            print(f"Error closing issue {issue_number}: {e}")
            return False

github_tool = GitHubTool()
