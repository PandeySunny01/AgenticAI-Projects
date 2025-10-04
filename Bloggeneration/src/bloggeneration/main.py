import streamlit as st
import json
from src.bloggeneration.ui.streamlitui.loadui import LoadStreamlitUI
from src.bloggeneration.LLM.groqllm import GroqLLM
from src.bloggeneration.graph.graph_builder import GraphBuilder
from src.bloggeneration.ui.streamlitui.display_result import DisplayResultStreamlit

# MAIN Function START
def load_bloggeneration_app():
    """
    Loads and runs the LangGraph BlogGeneration application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph, and displays the output while implementing exception handling for robustness.
    """
   
    # Load UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return

    
    BlogTopic= user_input["selected_topic"]

    st.markdown("""
    <style>
    div.stButton > button:first-child {
       background: linear-gradient(90deg, #A8C0FF, #E0E8FF);
        color: #333333;
        padding: 12px 20px;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #A8C0FF, #E0E8FF);
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)
    

    try: 
        if st.sidebar.button("✨ Generate Blog"):
                #st.success("Blog Generated!")
                    # Configure LLM
                obj_llm_config = GroqLLM(user_controls_input=user_input)
                model = obj_llm_config.get_llm_model()
                        
                if not model:
                    st.error("Error: LLM model could not be initialized.")
                    return
            
                try:
                        graph_builder=GraphBuilder(model)   
          
                        graph = graph_builder.setup_graph() 
                        #DisplayResultStreamlit(graph,BlogTopic).display_graph_on_ui()         
                        DisplayResultStreamlit(graph,BlogTopic).display_result_on_ui()
                        
               
                except Exception as e:
                    st.error(f"Error: Graph setup failed - {e}")
                    return  

    except Exception as e:
            raise ValueError(f"Error Occurred with Exception : {e}")
            