class SafetyGuard:
    FORBIDDEN_PATTERNS = [
        "rm -rf",
        "shred",
        "format ",
        "/dev/sda",
        "/dev/vda",
        "mkfs",
        "chmod 777",
        "chown root"
    ]
    
    IMMUTABLE_FILES = [
        "runtime/safety_guard.py",
        "runtime/rollback_manager.py",
        "main.py",
        "requirements.txt"
    ]

    def validate_mutation(self, mutation: dict):
        if not isinstance(mutation, dict):
            return True
            
        code = mutation.get("code") or ""
        description = mutation.get("description") or ""
        file_path = mutation.get("file_path") or ""
        
        # 1. Protection for immutable core system files
        for immutable in self.IMMUTABLE_FILES:
            if immutable in file_path:
                print(f"⚠️ Safety block: Attempted to modify immutable core file '{file_path}'")
                return False

        # 2. Check code and description for forbidden destructive patterns
        for pattern in self.FORBIDDEN_PATTERNS:
            if pattern in code or pattern in description:
                print(f"⚠️ Safety block: Destructive pattern '{pattern}' detected.")
                return False

        return True
