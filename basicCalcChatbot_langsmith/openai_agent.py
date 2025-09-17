from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessageGraph
from langgraph.graph.state import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
import os
from dotenv import load_dotenv


load_dotenv()

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

os.environ["LANGSMITH_API_KEY"]=os.getenv("LANGSMITH_API_KEY")

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

model = ChatOpenAI(temperature=0)


def make_default_graph():
    """Make a simple LLM agent"""
    graph_workflow = StateGraph(State)
    def call_model(state):
        return {"messages": [model.invoke(state["messages"])]}

    graph_workflow.add_node("agent", call_model)
    graph_workflow.add_edge("agent", END)
    graph_workflow.add_edge(START, "agent")

    agent = graph_workflow.compile()
    return agent

def make_alternative_graph():
    """Make a tool-calling agent"""

    @tool
    def add(a: float, b: float):
        """Adds two numbers."""
        return a + b

    @tool
    def subtract(a: float, b: float):
        """Subtract two numbers."""
        return a - b
    
    @tool
    def multiply(a: float, b: float):
        """multiply two numbers."""
        return a * b
    
    @tool
    def divide(a: float, b: float):
        """Divide two numbers."""
        return a / b

    

    tool_node = ToolNode([add, divide, multiply, subtract])

    model_with_tools = model.bind_tools([add, divide, multiply, subtract], parallel_tool_calls=False)


    def call_model(state):
        return {"messages": [model_with_tools.invoke(state["messages"])]}

    def should_continue(state: State):
        print("Agent deciding next step:", state)
        if state["messages"][-1].tool_calls:
            return "tools"
        else:
            return END

    graph_workflow = StateGraph(State)

    graph_workflow.add_node("agent", call_model)
    graph_workflow.add_node("tools", tool_node)
    graph_workflow.add_edge(START, "agent")
    graph_workflow.add_edge("tools", "agent")

    graph_workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",  # when should_continue returns "tools"
        END: END,
    }
        )

    agent = graph_workflow.compile()
    return agent

# for tool calling and using calculator
agent=make_alternative_graph()

#for using just the llm calls for all types of operations
#agent=make_default_graph()

## to run type ===langgraph dev

## langgraph.json===this dependency is needed for langscmith to understand the config and execute accordingly