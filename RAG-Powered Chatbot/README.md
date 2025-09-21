RAG-Powered Chatbot – Chat with Your Documents

🔹 Overview

PDFChat is a Retrieval-Augmented Generation (RAG) powered chatbot that lets you upload documents (PDFs, TXT files) and ask questions in natural language.

Instead of manually searching through pages, PDFChat retrieves the most relevant chunks using a vector database and answers your queries with an LLM (GPT-4o-mini / GPT-3.5 / Groq).

🚀 Features

📂 Upload multiple documents (PDFs, TXT).

✂️ Smart text chunking for better retrieval.

🔍 Vector-based semantic search with FAISS.

🤖 LLM-powered answers with citations.

📝 Streamlit UI for easy interaction.

⚡ Extendable: add memory, multi-doc support, or other tools.


🛠️ Tech Stack

Python 3.11+

Streamlit
 – Web app framework

LangChain
 – RAG pipeline

FAISS
 – Vector search

OpenAI
 – LLM & embeddings

PyPDF
 – PDF parsing


 📦 Installation

Clone the repo:

git clone https://github.com/<your-username>/docuchat.git
cd docuchat


Create a virtual environment:


Install dependencies:
pip install -r requirements.txt


🔑 Environment Variables

Create a .env file in the root directory:
    OPENAI_API_KEY=your_openai_api_key_here

▶️ Usage

Run the app:
streamlit run app.py

Open in browser → http://localhost:8501

Upload a PDF or TXT file.

Type your question in the input box.

Get instant answers powered by RAG.

📂 Project Structure

docuchat/
│── app.py               # Streamlit UI
│── requirements.txt     # Dependencies
│── .env.example         # Example API key config
│── README.md            # Documentation


🎯 Example Queries
“Summarize this document in 3 points.”

“What does section 4.2 mean?”

“Explain this in simple terms.”

🔮 Future Improvements

Add chat history with memory

Support for Word, CSV, JSON files

Integrate Groq / Llama 3 for open-source LLMs

Deploy on Streamlit Cloud / Render

🧑‍💻 Author

Built with ❤️ by Sunny Pandey