import os
import litellm
from dotenv import load_dotenv
from brain.messenger import messenger

load_dotenv(override=True)

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.base_url = os.getenv("ANTHROPIC_BASE_URL")
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620")
        self.full_model_name = f"anthropic/{self.model}"
        
        # Request limits
        self.evolution_requests = 0
        self.meta_requests = 0
        self.total_requests = 0
        
        self.max_evolution = 100 
        self.max_meta = 20
        self.max_total = 300

    def completion(self, messages, response_format=None, request_type="utility"):
        # request_type: "evolution", "meta", "utility"
        
        # Enforce limits
        if self.total_requests >= self.max_total:
            print(f"🛑 Global LLM request limit reached ({self.max_total}).")
            return None
        
        if request_type == "evolution" and self.evolution_requests >= self.max_evolution:
            print(f"🛑 Evolution request limit reached ({self.max_evolution}).")
            return None
            
        if request_type == "meta" and self.meta_requests >= self.max_meta:
            print(f"🛑 Meta Reasoning request limit reached ({self.max_meta}).")
            return None

        # Notify Telegram Request
        prompt = messages[-1]['content']
        messenger.notify_request(request_type.upper(), prompt)
        
        try:
            response = litellm.completion(
                model=self.full_model_name,
                messages=messages,
                api_key=self.api_key,
                base_url=self.base_url,
                response_format=response_format
            )
            content = response.choices[0].message.content
            
            # Update counters
            self.total_requests += 1
            if request_type == "evolution":
                self.evolution_requests += 1
            elif request_type == "meta":
                self.meta_requests += 1

            # Log raw response for debugging
            with open("logs/llm_raw.log", "a") as f:
                f.write(f"\n--- PROMPT ({request_type}) ---\n{prompt[:200]}...\n")
                f.write(f"--- RESPONSE ---\n{content}\n")
            
            # Notify Telegram Response
            messenger.notify_response(request_type.upper(), content)
            
            return content
        except Exception as e:
            err_msg = str(e)
            print(f"LLM Error: {err_msg}")
            
            # Check for quota error
            if "over_quota" in err_msg.lower() or "limit reached" in err_msg.lower():
                messenger.send_message(f"⌛ *QUOTA REACHED*\nSistem akan skip sisa tugas di siklus ini.")
                return "ERROR_QUOTA"
                
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
