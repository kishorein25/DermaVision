import os
import json
import subprocess
import urllib.request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434"
LLM_MODEL = "llama3.2:1b"
EMBED_MODEL = "mxbai-embed-large"

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def check_ollama():
    try:
        urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=3)
        return True
    except Exception:
        return False


def _load_kb():
    path = os.path.join(DATA_DIR, "medical_kb.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_embeddings(text):
    payload = json.dumps({"model": EMBED_MODEL, "prompt": text}).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/embeddings",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("embedding", [])


def _cosine(a, b):
    if not a or not b:
        return 0.0
    import math
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def embed_knowledge_base():
    kb = _load_kb()
    entries = []
    for category, qas in kb.items():
        for item in qas:
            text = item["question"] + " " + item["answer"]
            entries.append({
                "category": category,
                "question": item["question"],
                "answer": item["answer"],
                "source": item.get("source", "AI Health Knowledge Base"),
                "embedding": _get_embeddings(text),
            })
    return entries


def retrieve_context(query, top_k=3):
    entries = embed_knowledge_base()
    query_emb = _get_embeddings(query)
    scored = []
    for e in entries:
        score = _cosine(query_emb, e["embedding"])
        scored.append((score, e))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [e for _, e in scored[:top_k]]


def generate_answer(question, context_entries):
    context_text = ""
    for e in context_entries:
        context_text += f"Q: {e['question']}\nA: {e['answer']}\n\n"

    prompt = (
        "You are a helpful AI skin health assistant answering general health questions. "
        "Use ONLY the provided context to answer. Be clear and helpful, and remind the "
        "user that they should consult a doctor for medical advice.\n\n"
        f"CONTEXT:\n{context_text}\n"
        f"QUESTION: {question}\n"
        "ANSWER:"
    )

    payload = json.dumps({
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3, "num_ctx": 2048},
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("response", "I couldn't generate a response. Please try again.")


def chat(question):
    if not check_ollama():
        return {
            "error": "Ollama is not running. Please start Ollama (from Start Menu) then try again.",
            "success": False,
        }
    try:
        context = retrieve_context(question)
        answer = generate_answer(question, context)
        return {
            "answer": answer,
            "sources": [e["source"] for e in context],
            "success": True,
        }
    except Exception as e:
        logger.warning("Chat error: %s", e)
        return {"error": str(e), "success": False}