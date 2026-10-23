"""
DermaVision Standalone RAG Clinical Chatbot
Independent Streamlit Application powered by Retrieval-Augmented Generation (Ollama).
Run on port 8502: python -m streamlit run rag_chatbot/chatbot_app.py --server.port 8502
"""

import sys
import os
import streamlit as st

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag_chatbot.rag_engine import RAGEngine
from rag_chatbot.vector_store import VectorStore

st.set_page_config(
    page_title="DermaVision RAG Medical Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 4px;
    }
    .sub-header {
        font-size: 1rem;
        color: #475569;
        margin-bottom: 20px;
    }
    .evidence-card {
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        font-size: 0.85rem;
    }
    .disclaimer-banner {
        background-color: #FFFBEB;
        border-left: 5px solid #D97706;
        padding: 12px 16px;
        border-radius: 6px;
        color: #92400E;
        font-size: 0.85rem;
        margin-top: 25px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize RAG Engine in session state
if "rag_engine" not in st.session_state:
    with st.spinner("Initializing Clinical Vector Store & Embeddings..."):
        vs = VectorStore()
        st.session_state.rag_engine = RAGEngine(vs)

if "rag_messages" not in st.session_state:
    st.session_state.rag_messages = [
        {
            "role": "assistant",
            "content": (
                "👋 Hello! I am the **DermaVision RAG Clinical Assistant**.\n\n"
                "I am grounded in evidence-based dermatological clinical guidelines covering acne, eczema, "
                "psoriasis, infections, pigmentary disorders, nutrition, and emergency red flags. "
                "How can I help you understand skin health today?"
            ),
            "sources": []
        }
    ]

# Sidebar controls
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bot.png", width=64)
    st.markdown("### **RAG Clinical Architecture**")
    st.markdown("🧠 **LLM:** `Meta Llama 3.2 (1B)` (Local Ollama)")
    st.markdown("📐 **Embeddings:** `mxbai-embed-large` (1024-dim)")
    st.markdown("📚 **Knowledge Base:** 6 Peer-Reviewed Guidelines")
    st.markdown("🔍 **Retrieval:** Cosine Similarity (Top-3 Chunks)")
    st.markdown("🔒 **Privacy:** 100% Offline (No Cloud Leakage)")

    st.markdown("---")
    st.markdown("#### **Sample Clinical Inquiries**")
    sample_queries = [
        "What are the best foods to eat and avoid for acne?",
        "How do I tell if a rash is eczema or psoriasis?",
        "What are the ABCDE melanoma warning signs?",
        "What is the first-line treatment for ringworm (tinea)?",
        "What are dermatological emergency red flags?"
    ]
    for q in sample_queries:
        if st.button(q, key=f"btn_{q[:15]}"):
            st.session_state.preset_query = q

    st.markdown("---")
    if st.button("🗑️ Clear Conversation History"):
        st.session_state.rag_messages = [
            {
                "role": "assistant",
                "content": "Conversation history cleared. What dermatological topic would you like to explore?",
                "sources": []
            }
        ]
        st.rerun()

# Main Header
st.markdown('<div class="main-header">🤖 DermaVision: RAG Clinical Chatbot</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Retrieval-Augmented Generation grounded in verified dermatological literature. '
    'Every response cites its source clinical guidelines with relevance scoring.</div>',
    unsafe_allow_html=True
)

# Display chat messages
for msg in st.session_state.rag_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📚 View Grounded Clinical Sources & Relevance Scores", expanded=False):
                for idx, src in enumerate(msg["sources"], 1):
                    src_title = src["source"].replace(".txt", "").replace("_", " ").title()
                    st.markdown(f"""
                    <div class="evidence-card">
                        <b>Source #{idx}: {src_title}</b> (Cosine Similarity: <code>{src['score']}</code>)<br>
                        <span style="color: #475569; font-size: 0.82rem;">{src['text']}</span>
                    </div>
                    """, unsafe_allow_html=True)

# Determine query input (chat input or sidebar preset button)
preset = st.session_state.pop("preset_query", None)
user_query = st.chat_input("Ask a clinical dermatology question...") or preset

if user_query:
    # Append user question
    st.session_state.rag_messages.append({"role": "user", "content": user_query, "sources": []})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Generate grounded RAG response
    with st.chat_message("assistant"):
        with st.spinner("Retrieving medical evidence & synthesizing response..."):
            rag_result = st.session_state.rag_engine.answer_query(
                query=user_query,
                chat_history=st.session_state.rag_messages
            )
            st.markdown(rag_result["answer"])

            if rag_result.get("sources"):
                with st.expander("📚 View Grounded Clinical Sources & Relevance Scores", expanded=False):
                    for idx, src in enumerate(rag_result["sources"], 1):
                        src_title = src["source"].replace(".txt", "").replace("_", " ").title()
                        st.markdown(f"""
                        <div class="evidence-card">
                            <b>Source #{idx}: {src_title}</b> (Cosine Similarity: <code>{src['score']}</code>)<br>
                            <span style="color: #475569; font-size: 0.82rem;">{src['text']}</span>
                        </div>
                        """, unsafe_allow_html=True)

            st.session_state.rag_messages.append({
                "role": "assistant",
                "content": rag_result["answer"],
                "sources": rag_result.get("sources", [])
            })

# Universal medical disclaimer banner
st.markdown("""
<div class="disclaimer-banner">
    <b>⚠️ MANDATORY CLINICAL DISCLAIMER:</b> DermaVision RAG Chatbot is an educational decision-support tool. 
    Information provided is synthesized from clinical guidelines and is not a substitute for professional medical advice, 
    diagnosis, or treatment. Always consult a licensed board-certified dermatologist for medical conditions.
</div>
""", unsafe_allow_html=True)
