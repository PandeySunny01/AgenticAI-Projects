from langgraph.graph import StateGraph, START,END, MessagesState
from langgraph.prebuilt import tools_condition,ToolNode
from langchain_core.prompts import ChatPromptTemplate
from src.bloggeneration.state.state import State
from src.bloggeneration.nodes.title_node import TitleNode
from src.bloggeneration.nodes.content_node import ContentNode
#import graphviz
import streamlit as st
import time

class GraphBuilder:

    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)

   
    def BlogGeneration(self):
        """
        Builds a blog generator.
        This method creates a blog genrator which takes topic from user
        and generate both matching title and contents. 
        it has title and content node and direct edges between them.
     
        """

        ##Define LLM
        llm = self.llm

        #Add nodes
        self.titleNode=TitleNode(self.llm)
        print("adding title node")
        self.graph_builder.add_node("Title",self.titleNode.generate_title)
        self.contentNode=ContentNode(self.llm)
        print("adding content node")
        # st.subheader("Generating Blog Content:")
        # Progress bar
        progress_container = st.empty()
        progress_text = "⏳ Generating blog, please wait..."
        my_bar = progress_container.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.05)  # simulate work
            my_bar.progress(percent_complete + 1, text=progress_text)

         # Clear progress bar
        progress_container.empty()

        success_container = st.empty()
        success_container.success("✅ Blog Generated Successfully!")

        #success message removal afer display
        time.sleep(2)
        success_container.empty()

        self.graph_builder.add_node("Contents",self.contentNode.generate_content)

        self.graph_builder.add_edge(START,"Title")
        print("adding start title edge")
        self.graph_builder.add_edge("Title", "Contents")
        print("adding title-content edge")
        self.graph_builder.add_edge("Contents",END)
        print("adding content-end edge")
        

    def setup_graph(self):
        print("calling blog gen======")
        self.BlogGeneration()
        print("coming out of blog gen======")
        return self.graph_builder.compile()   
