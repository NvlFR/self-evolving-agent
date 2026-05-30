import os
import litellm
from dotenv import load_dotenv
from brain.messenger import messenger

load_dotenv(override=True)

class LLMClient:
    def __init__(self):
        # Primary Config
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
        import requests
        try:
            url = f"{self.fallback_base_url}/models"
            headers = {"Authorization": f"Bearer {self.fallback_api_key}"}
            response = requests.get(url, headers=headers, timeout=5)
            data = response.json()
            # Return list of model IDs, filter out some if needed
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
        
        # Notify Telegram Request (only once)
        if not is_fallback or (is_fallback and self.current_model_idx == 1):
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
            
            # Update counters
            self.total_requests += 1
            if request_type == "evolution":
                self.evolution_requests += 1
            elif request_type == "meta":
                self.meta_requests += 1

            # Log raw response
            with open("logs/llm_raw.log", "a") as f:
                f.write(f"\n--- PROMPT ({request_type}, model={model}, fallback={is_fallback}) ---\n{messages[-1]['content'][:200]}...\n")
                f.write(f"--- RESPONSE ---\n{content}\n")
            
            # Notify Telegram
            if not is_fallback or (is_fallback and self.current_model_idx == 1):
                messenger.notify_response(request_type.upper(), content)
            
            return content
        except litellm.RateLimitError:
            return "ERROR_QUOTA"
        except Exception as e:
            err_msg = str(e)
            if "over_quota" in err_msg.lower() or "limit reached" in err_msg.lower() or "ratelimiterror" in err_msg.lower():
                return "ERROR_QUOTA"
            print(f"LLM Error (model={model}, fallback={is_fallback}): {err_msg}")
            if not is_fallback:
                messenger.send_message(f"❌ *LLM ERROR*\n{err_msg}")
            return None

    @staticmethod
    def extract_json(text):
        if not text:
            return ""
        
        import json
        import re

        # Strategy 1: Look for JSON code blocks (markdown)
        # We take the LAST one because reasoning often includes example blocks first
        json_blocks = re.findall(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if json_blocks:
            return json_blocks[-1].strip()
            
        json_blocks = re.findall(r"```\s*(.*?)\s*```", text, re.DOTALL)
        if json_blocks:
            for block in reversed(json_blocks):
                candidate = block.strip()
                if candidate.startswith(("{", "[")):
                    return candidate

        # Strategy 2: Search for the last valid JSON object/list using JSONDecoder
        # This is more robust against conversational filler
        best_json = ""
        
        # We search from the end to find the most likely "final" answer
        for i in range(len(text)):
            char = text[i]
            if char in ('{', '['):
                try:
                    # Attempt to decode starting from this position
                    decoder = json.JSONDecoder()
                    obj, end_index = decoder.raw_decode(text[i:])
                    # If we found a valid object, it's a candidate
                    # We keep looking to find the *last* one or the most complete one
                    candidate = text[i:i+end_index].strip()
                    if len(candidate) > len(best_json):
                        best_json = candidate
                except (json.JSONDecodeError, ValueError):
                    continue
        
        if best_json:
            return best_json
            
        return text.strip()

llm = LLMClient()
