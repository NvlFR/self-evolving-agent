class Executor:
    def execute(self, task: str):
        try:
            exec(task)
            return {
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
