from src.bloggeneration.state.state import State
from langchain_core.messages import SystemMessage

class TitleNode:
    """
    Basic Blog Generation implementation.
    """
    def __init__(self,model):
         self.model=model

    def generate_title(self,state):
        print("inside generate title========")
        prompt_1 = SystemMessage(content="As an experienced writer generate only one blog title heading in bold fomrat and font aerial.")
        final1 =  {"messages":[self.model.invoke([prompt_1] + state["messages"])]}
        print("message for title======")
        print(final1)
        return final1
