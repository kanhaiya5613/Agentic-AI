import os
from typing import Optional, Literal
from typing_extensions import TypedDict
from dotenv import load_dotenv

from google import genai
from langgraph.graph import StateGraph, START, END

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

def chatbot(state: State):
    # Use 'contents' and read 'response.text' for the google-genai SDK
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=state.get("user_query"),
    )
    state["llm_output"] = response.text
    return state

# Routing function: returns exact target node names without parentheses
def evaluate_response(state: State) -> Literal["endnode", "chatbot_gemini"]:
    if True:
        return "endnode"
    return "chatbot_gemini"

def chatbot_gemini(state: State):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=state.get("user_query"),
    )
    state["llm_output"] = response.text
    return state

def endnode(state: State):
    print("Final state:", state)
    return state

# Build graph
graph_builder = StateGraph(State)

# 1. Register operational nodes only (do NOT add evaluate_response here)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

# 2. Add edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)
graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

# 3. Compile and run
graph = graph_builder.compile()

final_result = graph.invoke({"user_query": "what is 2+2?"})
print("Graph execution completed.")