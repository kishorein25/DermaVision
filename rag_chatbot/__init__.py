"""
DermaVision Standalone RAG-Based Clinical Chatbot Package
Powered by Ollama mxbai-embed-large (1024-dim) and Meta Llama 3.2.
"""

from .vector_store import VectorStore
from .rag_engine import RAGEngine

__all__ = [
    "VectorStore",
    "RAGEngine"
]
