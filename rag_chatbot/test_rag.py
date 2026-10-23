"""
DermaVision RAG Chatbot CLI Test & Benchmark Script
Runs test queries against the local RAG pipeline.
"""

import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag_chatbot.rag_engine import RAGEngine
from rag_chatbot.vector_store import VectorStore

def run_rag_test():
    print("=" * 68)
    print("🤖 DERMAVISION: STANDALONE RAG CLINICAL CHATBOT TEST")
    print("=" * 68)

    print("\n[Step 1] Loading Vector Store and indexing clinical knowledge...")
    vs = VectorStore()
    count = vs.build_index()
    print(f" -> Indexed Chunks: {count} clinical knowledge chunks")

    print("\n[Step 2] Initializing RAG Engine (mxbai-embed-large + llama3.2:1b)...")
    engine = RAGEngine(vs)

    test_questions = [
        "What are the best dietary foods to eat and avoid for acne vulgaris?",
        "How can a doctor differentiate eczema from psoriasis?",
        "What are the ABCDE warning signs of melanoma skin cancer?"
    ]

    for idx, q in enumerate(test_questions, 1):
        print("\n" + "-" * 68)
        print(f"TEST QUERY #{idx}: '{q}'")
        print("-" * 68)

        res = engine.answer_query(q)

        print("\n📚 RETRIEVED SOURCES:")
        for s_idx, src in enumerate(res["sources"], 1):
            src_name = src["source"].replace(".txt", "").replace("_", " ").title()
            print(f"  • Source {s_idx}: {src_name} (Cosine Similarity: {src['score']})")

        print("\n🤖 GENERATED CLINICAL RESPONSE:")
        print(res["answer"])

    print("\n" + "=" * 68)
    print("RAG BENCHMARK & RETRIEVAL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 68)

if __name__ == "__main__":
    run_rag_test()
