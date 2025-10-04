from src.bloggeneration.state.state import State
from langchain_core.messages import SystemMessage

class ContentNode:
    """
    Content generation for Blog based on topic provided by user.
    """
    def __init__(self,model):
        self.model = model
        
    def generate_content(self,state):
        print("inside generate content========")
        #prompt_2 = SystemMessage(content="As an experienced content creator write a blog with 1000 words and 8 paragraph with introduction,subheadings with indexing")
        prompt_2 = SystemMessage(content='''Write an engaging blog post on using storytelling.
                                        - Begin with a scenario or real-world problem related to the topic
                                        - Explain the concepts or solutions in a narrative style
                                        - Highlight practical applications or lessons
                                        - End with a conclusion tying the story back to the topic
                                        Make the language professional yet easy to understand, and include headings.''')
        
        final1 =  {"messages":[self.model.invoke([prompt_2] + state["messages"])]}
        print("message for content======")
        print(final1)
        return final1
   