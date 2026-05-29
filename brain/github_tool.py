import os
import subprocess
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
            # Stage changes
            subprocess.run(["git", "add", "."], check=True)
            
            # Commit
            subprocess.run(["git", "commit", "-m", message], check=True)
            
            # Push
            subprocess.run(["git", "push"], check=True)
            
            print(f"GitHub Updated: {message}")
            return True
        except Exception as e:
            # If nothing to commit, it's not really an error for the evolution loop
            if "nothing to commit" in str(e).lower():
                return True
            print(f"Error during git update: {e}")
            return False

github_tool = GitHubTool()
