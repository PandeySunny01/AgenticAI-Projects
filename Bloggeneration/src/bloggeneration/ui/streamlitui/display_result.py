import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage,SystemMessage
from src.bloggeneration.nodes.title_node import TitleNode
from src.bloggeneration.nodes.content_node import ContentNode
from src.bloggeneration.state.state import State
import graphviz
from langgraph.graph import StateGraph, START,END, MessagesState
import json


class DisplayResultStreamlit:
    def __init__(self,graph,blogtopic):
        #self.usecase= usecase
        self.graph = graph
        #self.user_message = user_message
        self.blogtopic = blogtopic

    def display_result_on_ui(self):
        graph = self.graph
        
        #user_message = self.user_message
        blogtopic=self.blogtopic
        initial_state = State(messages=[HumanMessage(blogtopic)])
        #initial_state = {"messages": [user_message]}
        print("initial state")
        print(initial_state)
        res = graph.invoke(initial_state)
        # graph = graphviz.Digraph()
        print("res")
        print(res)

        # st.graphviz_chart(graph)
        # from IPython.display import Image, display
        # st.image(display(Image(graph.get_graph().draw_mermaid_png())))
        # for output in graph.stream(initial_state):
        #     for key, value in output.items():
        #         print(f"Output from node: {key}")
        #         print("------")
        #         print(value['messages'][0].content)
        #         st.write(value['messages'][0].content)
        #         print("\n------\n")
        count=0
        for message in res["messages"]:
            print("message content")
            #print(message.content)
            print("blog_topic",blogtopic)
            print("messagecontent",message)
            
            if message==blogtopic:
                print("dont write any content")
                
            else:
                message_content=message.content
                
                if(message_content==blogtopic):
                     count=count+1
                     print("inside topic=========",count)
                     st.markdown(
                        f"""
                        <div style="
                            background-color: #e6f0fa;  /* soft light blue */
                            color: #1a1a1a;
                            padding: 20px;
                            border-radius: 12px;
                            text-align: center;
                            font-size: 26px;
                            font-weight: 600;
                            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                            margin-bottom: 25px;
                        ">
                            {message_content}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                elif(count==1):   
                         print("--------subheadings------")
                         count=0           
                         st.markdown(
                        f"""
                        <div style="
                            background-color: #e6f0fa;  /* soft light blue */
                            color: #1a1a1a;
                            padding: 20px;
                            border-radius: 12px;
                            text-align: center;
                            font-size: 20px;
                            font-weight: 600;
                            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                            margin-bottom: 25px;
                        ">
                            {message_content}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                        
                else: 
                    print("-----",count,"--------")
                    print("++++++++++++++++++++++++++++++++++++++++++++")
                    print(message_content)
                    print("++++++++++++++++++++++++++++++++++++++++++++")
                    st.markdown(
                        f"""
                        <div style="
                            background-color:#F8F9FA;
                            padding:15px;
                            border-radius:15px;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                            margin-bottom:20px;
                        ">
                            {message_content}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                #st.markdown(message.content,unsafe_allow_html=True)
                #st.write(message.content)
        
            # st.title("Blog Topic")
            
            # st.write("blog content")
       
              
             
        # prompt_1 = SystemMessage(content="As an experienced writer generate one blog title.")
        # message= {"messages":[graph.invoke([prompt_1] + initial_state["messages"])]} -> dict
        #st.write(message.content)


        # title=TitleNode(model).generate_title
        # print("title==========")
        # print(title)
        # self.titleNode=TitleNode(self)
        # title=self.titleNode.generate_title
        # st.write(title)
        # self.contentNode=ContentNode(self)
        # content=self.contentNode.generate_content
        # st.write(content)




       # user_message = self.user_message
             # Prepare state and invoke the graph
        # initial_state = {"messages": [user_message]}
        # res = graph.invoke(initial_state)
        # print("res==========")
        # print(res)
        # # st.write(message.content)

        # # print("message content==========")
        # # print(message.content)
        # for message in res['messages']:
        #     if type(message) == HumanMessage:
        #         with st.chat_message("user"):
        #             st.write(message.content)
        #     elif type(message)==ToolMessage:
        #         with st.chat_message("ai"):
        #             st.write("Tool Call Start")
        #             st.write(message.content)
        #             st.write("Tool Call End")
        #     elif type(message)==AIMessage and message.content:
        #         with st.chat_message("assistant"):
        #             st.write(message.content)
    def display_graph_on_ui(self):
            self.graph_builder = graphviz.Digraph()
            # Define conditional and direct edges
            self.graph_builder.edge(START,"Title")
            print("adding start title edge")
            self.graph_builder.edge("Title", "Contents")
            print("adding title-content edge")
            self.graph_builder.edge("Contents",END)
            print("adding content-end edge")
            st.graphviz_chart(self.graph_builder)  