#1 🧠 AI Blog Generator with Topic Selection:-

Effortlessly generate high-quality, SEO-optimized blog posts using AI.  
Select a main category in **Artificial Intelligence**, pick a **subtopic**, and generate a complete blog post — all within seconds.  
Built using **LangGraph** and **Streamlit**.

---

#2 🚀 Features

- 🧩 **Dynamic Topic Selection:**  
  Choose from multiple AI categories (e.g., Machine Learning, NLP, Computer Vision)  
  and nested subtopics like “Neural Networks”, “Transformers”, or “Image Recognition”.
  
- ✍️ **Automated Blog Generation:**  
  Instantly generate well-structured blog posts with introductions, key insights, and conclusions.

- 🎨 **Elegant Streamlit UI:**  
  User-friendly interface with progress bars and clean layout.

- ⚡ **Real-time Feedback:**  
  Displays progress during blog creation with status messages.

- 🔗 **LangGraph Integration:**  
  Handles multi-step workflow for topic understanding, content generation, and refinement.

---


#3 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| Frontend | Streamlit |
| Backend | Python |
| AI Framework | LangGraph |
| LLM Integration | OpenAI / Groq / Any LLM Provider |
| Deployment | Streamlit Cloud / Hugging Face / Localhost |

---

#4 ⚙️ Installation

i.-> Clone the Repository
```bash
git clone https://github.com/PandeySunny01/AgenticAI-Projects.git
cd Bloggeneration

ii.-> Create and Activate Virtual Environment

python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Mac/Linux

iii.-> Install Dependencies
pip install -r requirements.txt

## ▶️ Usage

Run the app locally:
streamlit run app.py
Then open your browser at:
👉 http://localhost:8501


#5🧭 How It Works

- Select a Main Category — e.g., “Machine Learning”, “Natural Language Processing”, or “Generative AI”.

- Select a Subtopic — options update dynamically based on the main category (e.g., “Neural Networks” under Machine Learning).

- Click “Generate Blog” to begin AI-driven content creation.

- The system displays a progress bar while generating.

- Once complete, a well-formatted blog post appears, ready to copy or publ

#6📂 Project Structure

Bloggeneration/
│
├── app.py                # Main Streamlit app
├── requirements.txt      # Dependencies
├── README.md             # Project documentation
├── src/ 
│   ├── bloggeneration 
            ├── ui/ # Contains Streamlit interface components (dropdowns, buttons, Progress bar, layout styling)
            ├── graph/   # Defines the LangGraph workflow connecting agents, nodes, and logic flow for blog generation
            ├── LLM/     # Manages large language model integrations (prompt templates, model configuration, API calls)
            ├── nodes/    # Holds modular node definitions for specific tasks (topic selection, blog drafting, refinement)
            └── state/    # Maintains and updates the app’s reactive state (session data, user inputs, intermediate results)

│   └── main.py  # Entry point of the app that initializes Streamlit, loads the UI layout, and displays generated blog results.
└── .env  #Stores environment variables such as API keys, model credentials, and configuration settings securely. 
              


#7 Acknowledgements

- LangGraph
- Streamlit
- OpenAI API

----------


Built with ❤️ using LangGraph and Streamlit
Create your next AI blog post in seconds.