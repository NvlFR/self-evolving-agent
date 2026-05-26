import sys
import io
import traceback

class Executor:
    def execute(self, code: str):
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_output = sys.stdout = io.StringIO()
        redirected_error = sys.stderr = io.StringIO()
        
        success = False
        error_msg = None
        
        try:
            # We use a clean dictionary for globals/locals to prevent side effects
            exec_globals = {}
            exec(code, exec_globals)
            success = True
        except Exception:
            error_msg = traceback.format_exc()
            success = False
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            
        return {
            "success": success,
            "stdout": redirected_output.getvalue(),
            "stderr": redirected_error.getvalue(),
            "error": error_msg
        }
