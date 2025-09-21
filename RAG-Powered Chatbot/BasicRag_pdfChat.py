# app.py
import os
import streamlit as st
from dotenv import load_dotenv
from typing import List

# LangChain imports
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.schema import Document

# Utility
import tempfile
import uuid

# Load environment variables from .env if present
load_dotenv()

# --- Config ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.warning("OPENAI_API_KEY not found in environment. Set it in .env or environment variables.")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")  # adjustable
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")  # adjustable / fallback

st.set_page_config(page_title="PDFChat — RAG Chatbot", layout="wide")
st.title("📚 PDFChat — Chat with your documents")
st.markdown(
    "Upload PDFs / TXT files, index them, then ask questions. "
    "Answers are retrieval-augmented and show the top retrieved chunks as citations."
)

# --- Initialize session state ---
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "docs_indexed" not in st.session_state:
    st.session_state.docs_indexed = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of dicts: {"query":..., "answer":..., "sources":[...]}
if "last_index_id" not in st.session_state:
    st.session_state.last_index_id = None

# --- Sidebar: settings & upload ---
with st.sidebar:
    st.header("Indexing Options")
    chunk_size = st.number_input("Chunk size", min_value=100, max_value=2000, value=800, step=100)
    chunk_overlap = st.number_input("Chunk overlap", min_value=0, max_value=500, value=150, step=50)
    top_k = st.number_input("Number of retrieved chunks (k)", min_value=1, max_value=10, value=3)
    st.markdown("---")
    st.header("Upload documents")
    uploaded_files = st.file_uploader(
        "Upload PDF or TXT files (multiple)",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        help="You can upload several files; they will be chunked and indexed."
    )
    st.markdown("---")
    st.header("Index / Reset")
    index_btn = st.button("Index uploaded files")
    reset_btn = st.button("Reset index and history")

# --- Reset handler ---
if reset_btn:
    st.session_state.vectorstore = None
    st.session_state.docs_indexed = []
    st.session_state.chat_history = []
    st.success("Cleared index and chat history.")

# --- Helper functions ---

def load_documents(files) -> List[Document]:
    """
    Load uploaded files into LangChain Document objects.
    For PDFs, use PyPDFLoader; for TXT, use TextLoader (we write to a temp file first).
    """
    docs: List[Document] = []
    for f in files:
        try:
            if f.type == "application/pdf" or f.name.lower().endswith(".pdf"):
                # PyPDFLoader accepts a path or file-like; Streamlit gives bytes, so write tmp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(f.getvalue())
                    tmp_path = tmp.name
                loader = PyPDFLoader(tmp_path)
                loaded = loader.load()
                # PyPDFLoader attaches metadata like {"source": path, "page": i}
                docs.extend(loaded)
            else:
                # TXT or others: write temp file and use TextLoader
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as tmp:
                    tmp.write(f.getvalue().decode("utf-8", errors="ignore"))
                    tmp_path = tmp.name
                loader = TextLoader(tmp_path, encoding="utf-8")
                loaded = loader.load()
                docs.extend(loaded)
        except Exception as e:
            st.error(f"Failed to load {f.name}: {e}")
    return docs

def build_vectorstore(docs: List[Document], chunk_size: int, chunk_overlap: int):
    """
    Split documents, embed, and build FAISS vectorstore.
    Returns the vectorstore instance and a unique index id.
    """
    if not docs:
        st.error("No documents to index.")
        return None, None

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(docs)

    # Add useful metadata for citations: ensure 'source' exists and set an id
    for c in chunks:
        if "source" not in (c.metadata or {}):
            c.metadata = {**(c.metadata or {}), "source": c.metadata.get("source", "uploaded") if c.metadata else "uploaded"}
        # add a short id to track chunk
        c.metadata = {**c.metadata, "chunk_id": str(uuid.uuid4())}

    # Embeddings & FAISS
    embeddings = OpenAIEmbeddings()  # reads OPENAI_API_KEY from env
    try:
        vectorstore = FAISS.from_documents(chunks, embeddings)
    except Exception as e:
        st.error(f"Failed to build FAISS index: {e}")
        return None, None

    index_id = str(uuid.uuid4())
    return vectorstore, index_id

def get_qa_chain(vectorstore):
    """
    Create a RetrievalQA chain using ChatOpenAI and the provided vectorstore retriever.
    """
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0.0)
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")
    return qa

def answer_query(qa_chain, query: str):
    """
    Run the query through the retriever+LLM chain and also return the top retrieved chunks for citation.
    """
    # Use retriever to fetch top docs for citation
    retriever = qa_chain.retriever
    docs = retriever.get_relevant_documents(query)  # top-k docs
    # Run LLM with the retriever (chain will itself call retriever internally), but we'll call qa_chain.run to get the answer
    try:
        answer = qa_chain.run(query)
    except Exception as e:
        st.error(f"Error generating answer: {e}")
        return None, docs

    return answer, docs

# --- Indexing flow ---
if index_btn:
    if not uploaded_files:
        st.warning("Please upload files before indexing.")
    else:
        with st.spinner("Loading documents..."):
            docs = load_documents(uploaded_files)
        if not docs:
            st.error("No documents loaded.")
        else:
            st.info(f"Loaded {len(docs)} document objects. Building index...")
            vs, idx_id = build_vectorstore(docs, chunk_size, chunk_overlap)
            if vs:
                st.session_state.vectorstore = vs
                # store simple record of filenames indexed
                st.session_state.docs_indexed = [f.name for f in uploaded_files]
                st.session_state.last_index_id = idx_id
                st.success(f"Indexed {len(docs)} document pages/chunks. Index id: {idx_id}")

# --- Main chat UI ---
st.markdown("---")
st.subheader("Ask your documents")

col1, col2 = st.columns([3, 1])

with col1:
    user_query = st.text_input("Enter a question and press Enter", key="user_query")
    if st.button("Ask") or (user_query and st.session_state.get("trigger_enter", False)):
        st.session_state["trigger_enter"] = False
        if not user_query:
            st.warning("Please type a question.")
        elif st.session_state.vectorstore is None:
            st.warning("No index found. Upload documents and press 'Index uploaded files'.")
        else:
            with st.spinner("Searching documents and generating answer..."):
                qa_chain = get_qa_chain(st.session_state.vectorstore)
                answer, sources = answer_query(qa_chain, user_query)
                if answer is not None:
                    # store in history
                    source_summaries = []
                    for s in sources[:top_k]:
                        src = s.metadata.get("source", "unknown")
                        # if page available in metadata, include it
                        page = s.metadata.get("page") or s.metadata.get("page_number") or None
                        snippet = s.page_content[:400].strip().replace("\n", " ")
                        source_summaries.append({"source": src, "page": page, "snippet": snippet})
                    st.session_state.chat_history.append({
                        "query": user_query,
                        "answer": answer,
                        "sources": source_summaries
                    })

with col2:
    st.markdown("**Index status**")
    if st.session_state.vectorstore:
        st.success(f"Indexed files: {len(st.session_state.docs_indexed)}")
        st.write(st.session_state.docs_indexed)
        st.markdown(f"Index id: `{st.session_state.last_index_id}`")
    else:
        st.info("No index yet. Upload & Index files to begin.")

# --- Display chat history (most recent first) ---
st.markdown("---")
st.subheader("Conversation")
if not st.session_state.chat_history:
    st.info("No conversation yet. Ask a question after indexing documents.")
else:
    for entry in reversed(st.session_state.chat_history):
        st.markdown(f"**Q:** {entry['query']}")
        st.markdown(f"**A:** {entry['answer']}")
        if entry.get("sources"):
            st.markdown("**Citations:**")
            for s in entry["sources"]:
                page_info = f" (page {s['page']})" if s["page"] else ""
                st.markdown(f"- `{s['source']}`{page_info}: _{s['snippet']}_")
        st.markdown("---")

# --- Footer / notes ---
st.write("⚠️ Notes: This is a demo RAG system. The accuracy of answers depends on your documents and the LLM.")
st.write("Tip: If your pdfs are large, increase chunk_size to reduce number of chunks, or use caching/persistent vector DB for production.")
