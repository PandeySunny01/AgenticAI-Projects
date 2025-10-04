import streamlit as st
import os
from datetime import date

from langchain_core.messages import AIMessage,HumanMessage
from src.bloggeneration.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config=Config() #config
        self.user_controls={}

    def initialize_session(self):
        return {
        # "current_step": "requirements",
        # "requirements": "",
        # "user_stories": "",
        # "po_feedback": "",
        # "generated_code": "",
        # "review_feedback": "",
        # "decision": None
        }

    def load_streamlit_ui(self):
            

            # Set page config
            st.set_page_config(
                page_title="🤖 AI Blog Generator",
                page_icon="📝",
                layout="wide"
            )

            st.markdown(
                """
                <div style="
                    background-color: #f4f6fb;  /* light pastel gray-blue */
                    padding: 25px;
                    border-radius: 9px;
                    text-align: center;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                    margin-bottom: 20px;
                ">
                    <h1 style="
                        color: #2c3e50;  
                        font-size: 30px; 
                        font-family: 'Segoe UI', 'Helvetica Neue', 'Roboto', sans-serif;
                        font-weight: 600;
                        margin: 0;
                    ">
                        📝 AI-Powered Blog Generator
                    </h1>
                </div>
                """,
                unsafe_allow_html=True
            )
            # st.markdown(
            #     """<div style="
            #         background-color: #f4f6fb;  /* light pastel gray-blue */
            #         padding: 20px;
            #         border-radius: 8px;
            #         text-align: center;
            #         box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            #         margin-bottom: 30px;
            #     ">
            #     <h4 style='color:#6A5ACD;'>Generate high-quality blog topics effortlessly using Langraph and AI</h3>""",
            #     unsafe_allow_html=True
            # )

            # Tagline
            st.markdown(
                "<p style='text-align: center; font-size:18px; color:gray; font-style:italic;'>"
                "Generate high-quality blog topics effortlessly using Langraph"
                "</p>",
                unsafe_allow_html=True
            )

            #st.markdown("---")
            st.markdown(
                "<p style='text-align:center; font-size:20px;'>✦ ✦ ✦ ✦ ✦ ✦</p>",
                unsafe_allow_html=True
            )

            # st.write("option",option)
           
    #         st.markdown(
    #     """
    #     <div style="
    #         background-color:#F8F9FA;
    #         padding:30px;
    #         border-radius:15px;
    #         box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    #         ">
    #     """,
    #     unsafe_allow_html=True
    # )
            
            

            st.session_state.timeframe = ''
            st.session_state.IsFetchButtonClicked = False

            with st.sidebar:
                # Get options from config
                #blog_topic = st.selectbox("Select Blog topic",(self.config.get_blog_topic()),)

                # Category dropdown
                category = st.selectbox("Select Blog_Topic:", [""] + self.config.get_categories())

                # Subcategory dropdown (dynamic)
                if category:
                    subcategories = self.config.get_subcategories(category)
                    if subcategories:
                        subcategory = st.selectbox("Select Blog_SubTopic:", subcategories)
                    else:
                        subcategory = None
                else:
                    subcategory = None

                st.subheader("Your Selection")
                st.info(f"**Category:** {category or 'None'}\n**Subcategory:** {subcategory or 'None'}")

                llm_options = self.config.get_llm_option()
           
                #Combine category + subcategory as one topic
                if category and subcategory:
                    blog_topic = f"{category} - {subcategory}"
                elif category:
                    blog_topic = category
                else:
                    blog_topic = None
                self.user_controls["selected_topic"] = blog_topic
        # LLM selection
                self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)
                
                if self.user_controls["selected_llm"] == 'Groq':
                    # Model selection
                    model_options = self.config.get_groqmodel_option()
                    self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                    # API key input
                    self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key",
                                                                                                        type="password")
                    # Validate API key
                    if not self.user_controls["GROQ_API_KEY"]:
                        st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")
                    
                if "state" not in st.session_state:
                    st.session_state.state = self.initialize_session()
                
                return self.user_controls