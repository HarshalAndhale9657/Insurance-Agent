import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.query_service import query_agent

print("--- Test 1: Greeting ---")
resp1 = query_agent("Hi")
print(f"Answer: {resp1['answer']}")
print(f"Sources: {resp1['sources']}")

print("\n--- Test 2: Insurance Query ---")
resp2 = query_agent("What is the benefit of health insurance?")
print(f"Answer: {resp2['answer']}")
print(f"Sources: {resp2['sources']}")
