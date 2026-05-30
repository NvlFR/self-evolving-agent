import os
import litellm
import requests
import json
from dotenv import load_dotenv
from brain.messenger import messenger

load_dotenv(override=True)

class LLMClient:
    def __init__(self):
        # Primary Config (Anthropic via Proxy)
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.base_url = os.getenv("ANTHROPIC_BASE_URL")
        self.model = os.getenv("ANTHROPIC_MODEL", "cu/claude-4.5-sonnet")
        
        # Fallback Config (9router)
        self.fallback_api_key = "sk-d0e1cbd475c97b59-35bcoc-46bcde6c"
        self.fallback_base_url = "http://192.168.100.111:20128/v1"
        self.model_list = self._fetch_model_list()
        self.current_model_idx = 0
        
        self.total_requests = 0
        self.max_total = 300

    def _fetch_model_list(self):
        try:
            url = f"{self.fallback_base_url}/models"
            headers = {"Authorization": f"Bearer {self.fallback_api_key}"}
            response = requests.get(url, headers=headers, timeout=5)
            data = response.json()
            return [m["id"] for m in data["data"]]
        except Exception as e:
            print(f"Gagal mengambil daftar model: {e}")
            return ["cu/claude-4.5-sonnet", "kr/claude-sonnet-4.5-agentic"]

    def completion(self, messages, response_format=None, request_type="utility"):
        # 1. Coba Primary
        result = self._attempt_completion(messages, self.api_key, self.base_url, self.model, request_type, is_fallback=False)
        
        # 2. Coba Fallback kalau error quota/rate limit
        while result == "ERROR_QUOTA" and self.current_model_idx < len(self.model_list):
            fallback_model = self.model_list[self.current_model_idx]
            self.current_model_idx += 1
            
            messenger.send_message(f"⚠️ *Model Utama limit, switch ke:* `{fallback_model}`")
            result = self._attempt_completion(messages, self.fallback_api_key, self.fallback_base_url, fallback_model, request_type, is_fallback=True)
            
        return result

    def _attempt_completion(self, messages, api_key, base_url, model, request_type, is_fallback):
        if self.total_requests >= self.max_total:
            return None
        
        try:
            custom_headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
            
            response = litellm.completion(
                model=model,
                messages=messages,
                api_base=base_url,
                api_key=api_key or "sk-dummy",
                headers=custom_headers
            )
            content = response.choices[0].message.content
            self.total_requests += 1
            return content
            
        except Exception as e:
            err = str(e).lower()
            if any(key in err for key in ["429", "rate", "over_quota", "unavailable", "limit"]):
                return "ERROR_QUOTA"
            
            print(f"Error fatal LLM: {err}")
            if not is_fallback:
                messenger.send_message(f"❌ *LLM ERROR*\n{err[:200]}")
            return None

    @staticmethod
    def extract_json(text):
        if not text: return ""
        import re, json
        json_blocks = re.findall(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if json_blocks: return json_blocks[-1].strip()
        return text.strip()

llm = LLMClient()
