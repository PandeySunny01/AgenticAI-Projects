import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self,user_controls_input):
        self.user_controls_input=user_controls_input

    def get_llm_model(self):
        try:
            groq_api_key=self.user_controls_input['GROQ_API_KEY']
            print("taking groq value============")
            print(groq_api_key)
            selected_groq_model=self.user_controls_input['selected_groq_model']
            print("taking groq model")
            if groq_api_key=='' and os.environ["GROQ_API_KEY"] =='':
                st.error("Please Enter the Groq API KEY")

            print("enetring chatgroq func")
            llm = ChatGroq(api_key =groq_api_key, model=selected_groq_model)
            print("leaving chatgroq func")
        except Exception as e:
            raise ValueError(f"Error Occurred with Exception : {e}")
        return llm