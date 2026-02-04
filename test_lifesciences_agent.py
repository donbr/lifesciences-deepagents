import asyncio
from apps.api.graphs.lifesciences import graph
from langchain_core.messages import HumanMessage

async def main():
    print("--- Testing Life Sciences Graph Builder Agent ---")
    
    # Test Question (CQ14-style)
    question = "What are the synthetic lethal partners of TP53?"
    
    print(f"Question: {question}")
    print("Invoking graph...")
    
    input_state = {
        "messages": [HumanMessage(content=question)],
        "question": question,
        "current_phase": "ANCHOR"
    }
    
    async for output in graph.astream(input_state):
        for key, value in output.items():
            print(f"\n--- Node: {key} ---")
            # print(value)
            if "messages" in value:
                print(f"Agent Output: {value['messages'][-1].content[:200]}...") # Truncate for readability
                
    print("\n--- Test Complete ---")

if __name__ == "__main__":
    asyncio.run(main())
