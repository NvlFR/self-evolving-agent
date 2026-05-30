import os
import subprocess
import json
from duckduckgo_search import DDGS
from brain.messenger import messenger

class RealWorldTool:
    def __init__(self):
        self.ddgs = DDGS()

    def search_web(self, query, max_results=5):
        """Search the web for knowledge or solutions."""
        try:
            results = list(self.ddgs.text(query, max_results=max_results))
            messenger.send_message(f"🌐 *Web Research:* '{query}'\nFound {len(results)} sources.")
            return results
        except Exception as e:
            print(f"Web Search Error: {e}")
            return []

    def search_github_code(self, query):
        """Search GitHub for code snippets or libraries."""
        try:
            # Using gh cli to search repositories
            result = subprocess.run(
                ["gh", "search", "repos", query, "--limit", "3", "--json", "fullName,description,url"],
                capture_output=True,
                text=True,
                check=True
            )
            repos = json.loads(result.stdout)
            messenger.send_message(f"🐙 *GitHub Research:* '{query}'\nFound {len(repos)} relevant repos.")
            return repos
        except Exception as e:
            print(f"GitHub Search Error: {e}")
            return []

    def fetch_url(self, url):
        """Fetch raw content from a URL to learn from it."""
        import requests
        try:
            response = requests.get(url, timeout=10)
            return response.text[:5000] # Limit to 5k chars for LLM context
        except Exception as e:
            print(f"Fetch Error: {e}")
            return f"Failed to fetch {url}"

real_world_tool = RealWorldTool()
