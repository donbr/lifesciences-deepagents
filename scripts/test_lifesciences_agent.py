import asyncio
from apps.api.lifesciences import graph
from langchain_core.messages import HumanMessage

async def main():
    print("--- Testing Life Sciences Graph Builder Agent ---")
    
    # Test Question (CQ14-style)
    question = "What is the mechanism of Palovarotene in FOP according to literature?"
    
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
            print(f"Node Output Type: {type(value)}")
            # Enhanced Logging for Visibility
            if isinstance(value, dict) and "messages" in value and isinstance(value["messages"], list):
                last_msg = value['messages'][-1]
                
                # Check for Task Tool Calls (Subagent Activation)
                if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                    for tool_call in last_msg.tool_calls:
                        if tool_call['name'] == 'task':
                            subagent = tool_call['args'].get('subagent_type', 'unknown')
                            print(f"\n🚀 [ACTIVATING SUBAGENT]: {subagent.upper()}")
                            print(f"   Task: {tool_call['args'].get('description', 'No description contents')[:100]}...")
                
                print(f"Agent Output: {last_msg.content[:200]}...")
            else:
                 print(f"Node Output: {value}")
                
    print("\n--- Test Complete ---")

if __name__ == "__main__":
    asyncio.run(main())
