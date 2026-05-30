import os
import litellm
import json
import requests
import re
from dotenv import load_dotenv
from brain.messenger import messenger

load_dotenv(override=True)

class LLMClient:
    def __init__(self):
        # Primary Config (Olagon)
        self.api_key = os.getenv("OLAGON_ANTHROPIC_API_KEY")
        self.base_url = os.getenv("OLAGON_ANTHROPIC_BASE_URL")
        self.model = os.getenv("OLAGON_ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620")
        
        # Fallback Config (9router)
        self.fallback_api_key = os.getenv("9ROUTER_API_KEY")
        self.fallback_base_url = os.getenv("9ROUTER_BASE_URL", "http://localhost:20128") + "/v1"
        self.model_list = [
            "gc/gemini-3-flash-preview",
            "openrouter/openrouter/owl-alpha",
            "openrouter/nvidia/nemotron-3-super-120b-a12b:free",
            "openrouter/google/gemma-4-26b-a4b-it:free",
            "openrouter/openrouter/free",
            "openrouter/google/gemma-4-31b-it:free",
            "openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
            "openrouter/nvidia/nemotron-3-nano-30b-a3b:free",
            "ollama/gpt-oss:120b",
            "ollama/minimax-m2.5"
        ]
        self.current_model_idx = 0
        self.fallback_attempts = 0 
        self.max_fallback_attempts = 3 
        
        # New: Sticky and Efficiency logic
        self.is_primary_down = False
        self.consecutive_primary_failures = 0
        self.primary_check_counter = 0
        self.current_fallback_idx = 0
        
        # Request limits
        self.total_requests = 0
        self.max_total = 300

    def completion(self, messages, response_format=None, request_type="utility"):
        result = "ERROR_QUOTA"
        
        # 1. Try Primary if it's up, or every 5 requests if it's down
        should_try_primary = not self.is_primary_down
        if self.is_primary_down:
            self.primary_check_counter += 1
            if self.primary_check_counter >= 5:
                should_try_primary = True
                self.primary_check_counter = 0
                print("🔄 Periodically re-checking Primary model...")

        if should_try_primary:
            result = self._attempt_completion(messages, self.api_key, self.base_url, self.model, request_type, is_fallback=False)
            if result != "ERROR_QUOTA" and result is not None:
                if self.is_primary_down:
                    print("✅ Primary AI is BACK UP. Resetting status.")
                    messenger.send_message("✅ *Primary AI is back online.*")
                self.is_primary_down = False
                self.consecutive_primary_failures = 0
                return result
            else:
                self.consecutive_primary_failures += 1
                if self.consecutive_primary_failures >= 2:
                    if not self.is_primary_down:
                        print("🛑 Primary AI hit multiple errors. Switching to STICKY FALLBACK mode.")
                        messenger.send_message("⚠️ *Primary AI is down. Switching to sticky fallback mode.*")
                    self.is_primary_down = True
                
                if not self.is_primary_down:
                    # If not yet "officially" down, try next fallback but don't stay there yet
                    pass 
                else:
                    # If officially down, result is already ERROR_QUOTA, loop will handle fallback
                    pass

        # 2. Try Fallbacks (Sticky mode)
        self.fallback_attempts = 0 
        
        while self.fallback_attempts < self.max_fallback_attempts:
            # Get the currently "active" fallback model
            fallback_model = self.model_list[self.current_fallback_idx]
            
            result = self._attempt_completion(messages, self.fallback_api_key, self.fallback_base_url, fallback_model, request_type, is_fallback=True)
            
            if result != "ERROR_QUOTA" and result is not None:
                # This model worked! Keep using it for the next call.
                return result
            
            # This model failed, move to the next one
            print(f"🛑 Fallback model {fallback_model} failed/limited. Moving to next.")
            self.current_fallback_idx += 1
            
            if self.current_fallback_idx >= len(self.model_list):
                self.current_fallback_idx = 0
                self.fallback_attempts += 1
                if self.fallback_attempts >= self.max_fallback_attempts:
                    print(f"🛑 All fallback models exhausted ({self.max_fallback_attempts} full cycles).")
                    messenger.send_message("⚠️ *CRITICAL: All AI fallback models exhausted.*")
                    break

        return result

    def _attempt_completion(self, messages, api_key, base_url, model, request_type, is_fallback):
        # Explicit Logging
        log_file = "logs/llm_raw.log"
        os.makedirs("logs", exist_ok=True)
        
        if self.total_requests >= self.max_total:
            print("🛑 Total request limit reached.")
            return None
        
        # Notify Telegram Request
        prefix = "[FALLBACK] " if is_fallback else ""
        prompt = messages[-1]['content']
        messenger.notify_request(f"{prefix}{request_type.upper()}", prompt)
        
        with open(log_file, "a") as f:
            f.write(f"\n--- REQUEST ({model}) ---\n{json.dumps(messages)}\n")
        
        try:
            custom_headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
            
            # Ensure model has a provider prefix for custom proxies
            full_model = model
            if base_url and "/" not in model:
                full_model = f"openai/{model}"
            elif base_url and not any(model.startswith(p) for p in ["openai/", "anthropic/", "gemini/", "vertex_ai/", "azure/"]):
                 full_model = f"openai/{model}"

            response = litellm.completion(
                model=full_model,
                messages=messages,
                api_base=base_url,
                api_key=api_key or "sk-dummy",
                headers=custom_headers
            )
            content = response.choices[0].message.content
            
            with open(log_file, "a") as f:
                f.write(f"\n--- RESPONSE ({model}) ---\n{content}\n")
            
            # Update counters
            self.total_requests += 1
            
            # Notify Telegram Response
            messenger.notify_response(f"{prefix}{request_type.upper()}", content)
            
            return content
        except Exception as e:
            err_msg = str(e).lower()
            # Catch auth errors (401), rate limits (429), and other quota issues
            if any(term in err_msg for term in ["rate", "429", "401", "authentication", "over_quota", "limit reached", "ratelimiterror", "unavailable"]):
                print(f"🛑 Error hit for model {model}: {err_msg[:100]}")
                return "ERROR_QUOTA"
            
            print(f"LLM Error (model={model}, fallback={is_fallback}): {err_msg[:100]}")
            if not is_fallback:
                messenger.send_message(f"❌ *LLM ERROR*\n{err_msg[:200]}")
            return None

    @staticmethod
    def extract_json(text):
        if not text: return ""
        
        # Markdown block detection
        json_blocks = re.findall(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if json_blocks: return json_blocks[-1].strip()
        
        # Brute force search for JSON
        best_json = ""
        for i in range(len(text)):
            if text[i] in ('{', '['):
                try:
                    obj, end = json.JSONDecoder().raw_decode(text[i:])
                    candidate = text[i:i+end].strip()
                    if len(candidate) > len(best_json): best_json = candidate
                except: continue
        return best_json if best_json else text.strip()

llm = LLMClient()
