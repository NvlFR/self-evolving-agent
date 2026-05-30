import os
import litellm
import requests
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
        
        # Request limits
        self.evolution_requests = 0
        self.meta_requests = 0
        self.total_requests = 0
        self.max_evolution = 100 
        self.max_meta = 20
        self.max_total = 300

    def _fetch_model_list(self):
        try:
            url = f"{self.fallback_base_url}/models"
            headers = {"Authorization": f"Bearer {self.fallback_api_key}"}
            response = requests.get(url, headers=headers, timeout=5)
            data = response.json()
            return [m["id"] for m in data["data"]]
        except Exception as e:
            print(f"Error fetching model list: {e}")
            return ["cu/claude-4.5-sonnet", "kr/claude-sonnet-4.5-agentic"]

    def completion(self, messages, response_format=None, request_type="utility"):
        # 1. Try Primary
        result = self._attempt_completion(messages, self.api_key, self.base_url, self.model, request_type, is_fallback=False)
        
        # 2. Try Fallbacks
        while result == "ERROR_QUOTA" and self.current_model_idx < len(self.model_list):
            fallback_model = self.model_list[self.current_model_idx]
            self.current_model_idx += 1
            
            print(f"Primary quota exceeded. Switching to fallback model: {fallback_model}...")
            messenger.send_message(f"⚠️ *Primary Quota Exceeded. Switched to Fallback Model:* `{fallback_model}`")
            
            result = self._attempt_completion(messages, self.fallback_api_key, self.fallback_base_url, fallback_model, request_type, is_fallback=True)
            
        return result

    def _attempt_completion(self, messages, api_key, base_url, model, request_type, is_fallback):
        # Enforce limits
        if self.total_requests >= self.max_total:
            print(f"🛑 Global LLM request limit reached ({self.max_total}).")
            return None
        
        # Notify Telegram Request
        if not is_fallback:
            prompt = messages[-1]['content']
            messenger.notify_request(request_type.upper(), prompt)
        
        try:
            custom_headers = {}
            if api_key:
                custom_headers["Authorization"] = f"Bearer {api_key}"
            
            response = litellm.completion(
                model=model,
                messages=messages,
                api_base=base_url,
                api_key=api_key or "sk-dummy",
                headers=custom_headers
            )
            content = response.choices[0].message.content
            
            self.total_requests += 1
            if request_type == "evolution": self.evolution_requests += 1
            elif request_type == "meta": self.meta_requests += 1

            if not is_fallback: messenger.notify_response(request_type.upper(), content)
            
            return content
        except Exception as e:
            err_msg = str(e).lower()
            # Force fallback for ALL rate limits, 429s, and unavailabilities
            if any(term in err_msg for term in ["rate", "429", "over_quota", "limit reached", "ratelimiterror", "unavailable"]):
                return "ERROR_QUOTA"
                
            print(f"LLM Error (model={model}): {err_msg}")
            if not is_fallback:
                messenger.send_message(f"❌ *LLM ERROR*\n{err_msg[:200]}")
            return None

    @staticmethod
    def extract_json(text):
        if not text: return ""
        import json, re
        
        # Strategy: Look for the *last* valid JSON object/list
        best_json = ""
        for i in range(len(text)):
            if text[i] in ('{', '['):
                try:
                    obj, end_index = json.JSONDecoder().raw_decode(text[i:])
                    candidate = text[i:i+end_index].strip()
                    if len(candidate) > len(best_json): best_json = candidate
                except: continue
        return best_json if best_json else text.strip()

llm = LLMClient()
