import os
import litellm
from dotenv import load_dotenv

load_dotenv(override=True)

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.base_url = os.getenv("ANTHROPIC_BASE_URL")
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620")
        
        # litellm expects custom base urls to be passed in a specific way or via environment
        # For anthropic compatible proxies, we can often just set the base_url.
        # However, litellm might need 'anthropic/' prefix if it's using the anthropic provider logic.
        self.full_model_name = f"anthropic/{self.model}"

    def completion(self, messages, response_format=None):
        try:
            response = litellm.completion(
                model=self.full_model_name,
                messages=messages,
                api_key=self.api_key,
                base_url=self.base_url,
                response_format=response_format
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM Error: {e}")
            return None

    @staticmethod
    def extract_json(text):
        if not text:
            return None
        
        # Try to find JSON block
        if "```json" in text:
            try:
                return text.split("```json")[1].split("```")[0].strip()
            except: pass
        if "```" in text:
            try:
                return text.split("```")[1].split("```")[0].strip()
            except: pass
            
        # Try to find the first '[' or '{' and last ']' or '}'
        start_curly = text.find('{')
        start_bracket = text.find('[')
        
        start = -1
        if start_curly != -1 and (start_bracket == -1 or start_curly < start_bracket):
            start = start_curly
            end = text.rfind('}')
        elif start_bracket != -1:
            start = start_bracket
            end = text.rfind(']')
            
        if start != -1 and end != -1 and end > start:
            return text[start:end+1].strip()
            
        return text.strip()

llm = LLMClient()
