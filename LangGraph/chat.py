from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

from dotenv import load_dotenv
load_dotenv()

llm = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google_genai",
)
class State(TypedDict):
    messages: Annotated[list, add_messages ]

def chatbot(state: State):
    response = llm.invoke(state.get("messages"))
    return { "messages": [response] }

def sample_node(state: State):
    print("\n\nInside sample node", state)
    return { "messages": ["where are you from?"] }

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sample", sample_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sample")
graph_builder.add_edge("sample", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages":["hii,how are you?"]}))
print("\n\nupdated_state", updated_state)

# (START) -> (chatbot) -> (sample_node) -> (END)

# State = { messages: ["Hello! How can I assist you today}
# node runs: chatbot(state: ["hello! How can I assist you today?"])-> ["where are you from?"]
# state = { "messages": ["Hello! How can I assist you today?", "where are you from?"] }