from runtime.autonomous_loop import AutonomousLoop
from brain.meta_reasoner import MetaReasoner

print("\n=== SEED EVOLUTION SYSTEM START ===\n")

loop = AutonomousLoop()
meta_reasoner = MetaReasoner()

history = loop.evolve(iterations=5)

print("\n=== EVOLUTION HISTORY ===\n")

for step in history:
    print(step)

print("\n=== META REASONING ===\n")

insights = meta_reasoner.analyze_evolution(history)

for insight in insights:
    print(f"- {insight}")

print("\n=== SEED EVOLUTION SYSTEM END ===\n")
