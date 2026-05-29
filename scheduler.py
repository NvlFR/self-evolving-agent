import time
import subprocess
from brain.messenger import messenger
from memory.status_manager import status_manager

def start_scheduler():
    cycle_interval = 5 * 3600 # 5 Hours
    
    messenger.send_message("🤖 *SEED Scheduler Started*\nSistem akan berjalan setiap 5 jam.")
    
    while True:
        try:
            current_ctx = status_manager.get_context()
            messenger.send_message(f"🔄 *Starting New Evolution Cycle*\n{current_ctx}")
            
            # Run the evolution process
            subprocess.run(["python3", "main.py"], check=True)
            
            messenger.send_message(f"😴 *Evolution Cycle Complete.*\nMenunggu 5 jam untuk tahap berikutnya.")
            
        except Exception as e:
            print(f"Scheduler Error: {e}")
            messenger.send_message(f"⚠️ *Scheduler Error*\n{str(e)}")
            
        time.sleep(cycle_interval)

if __name__ == "__main__":
    start_scheduler()
