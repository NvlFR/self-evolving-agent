from runtime.autonomous_loop import AutonomousLoop
from brain.meta_reasoner import MetaReasoner
from memory.status_manager import status_manager

def run_evolution():
    print(f"\n=== SEED EVOLUTION SYSTEM START ({status_manager.get_context()}) ===\n")

    loop = AutonomousLoop()
    meta_reasoner = MetaReasoner()

    # Limit to 5 seed evolution (iterations)
    history = loop.evolve(iterations=5)

    print("\n=== EVOLUTION HISTORY ===\n")
    for step in history:
        print(step)

    print("\n=== META REASONING ===\n")
    insights = meta_reasoner.analyze_evolution(history)

    for insight in insights:
        print(f"- {insight}")

    # Update status for next 5-hour cycle
    status_manager.increment_epoch()
    print(f"\n=== SEED EVOLUTION SYSTEM END. Next Stage Prepared. ===\n")

if __name__ == "__main__":
    run_evolution()
