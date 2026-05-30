class SafetyGuard:
    FORBIDDEN_PATTERNS = [
        "os.system",
        "rm -rf",
        "eval(",
        "exec("
    ]

    def validate_mutation(self, mutation: dict):
        if not isinstance(mutation, dict):
            return True # Or handle legacy string mutations if needed
            
        code = mutation.get("code") or ""
        description = mutation.get("description") or ""
        
        # Check code and description for forbidden patterns
        for pattern in self.FORBIDDEN_PATTERNS:
            if pattern in code or pattern in description:
                return False

        return True
