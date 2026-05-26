class SafetyGuard:
    FORBIDDEN_PATTERNS = [
        "os.system",
        "subprocess",
        "rm -rf",
        "eval(",
        "exec("
    ]

    def validate_mutation(self, mutation_text: str):
        for pattern in self.FORBIDDEN_PATTERNS:
            if pattern in mutation_text:
                return False

        return True
