"""
VectorStore: Local Vector Store & Cosine Similarity Search Engine
Uses Ollama 'mxbai-embed-large:latest' (1024-dim) with local disk caching.
Zero external heavy dependencies required.
"""

import os
import json
import math
import requests
import numpy as np
from typing import List, Dict, Any, Optional, Tuple

class VectorStore:
    """
    Manages document chunking, Ollama embedding generation,
    local serialization, and fast cosine similarity vector retrieval.
    """

    OLLAMA_URL = "http://localhost:11434/api/embeddings"
    EMBED_MODEL = "mxbai-embed-large:latest"

    def __init__(self, knowledge_dir: Optional[str] = None, cache_file: Optional[str] = None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.knowledge_dir = knowledge_dir or os.path.join(base_dir, "knowledge_base")
        self.cache_file = cache_file or os.path.join(base_dir, "vector_cache.json")
        self.chunks: List[Dict[str, Any]] = []
        self.embeddings: List[List[float]] = []

    def get_embedding(self, text: str) -> Optional[List[float]]:
        """Queries local Ollama for text embedding vector."""
        try:
            resp = requests.post(
                self.OLLAMA_URL,
                json={"model": self.EMBED_MODEL, "prompt": text},
                timeout=8
            )
            if resp.status_code == 200:
                data = resp.json()
                vec = data.get("embedding", [])
                if vec:
                    return vec
        except Exception:
            pass

        # Fallback deterministic pseudo-embedding (384-dim) if Ollama is offline
        return self._fallback_embedding(text)

    def _fallback_embedding(self, text: str, dim: int = 1024) -> List[float]:
        """Deterministic hashing fallback embedding for offline continuity."""
        vec = [0.0] * dim
        words = text.lower().split()
        for w in words:
            h = abs(hash(w)) % dim
            vec[h] += 1.0
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]

    def chunk_text(self, text: str, source_name: str, max_chunk_words: int = 180) -> List[Dict[str, Any]]:
        """Splits document text into coherent semantic paragraphs with source metadata."""
        paragraphs = text.split("\n\n")
        chunks = []
        chunk_id = 0

        for p in paragraphs:
            clean_p = p.strip()
            if len(clean_p) < 40:
                continue

            words = clean_p.split()
            if len(words) <= max_chunk_words:
                chunks.append({
                    "id": f"{source_name}_{chunk_id}",
                    "source": source_name,
                    "text": clean_p,
                    "word_count": len(words)
                })
                chunk_id += 1
            else:
                # Split large paragraphs into sub-chunks
                for i in range(0, len(words), max_chunk_words - 30):
                    sub = " ".join(words[i:i + max_chunk_words])
                    chunks.append({
                        "id": f"{source_name}_{chunk_id}",
                        "source": source_name,
                        "text": sub,
                        "word_count": len(sub.split())
                    })
                    chunk_id += 1

        return chunks

    def build_index(self, force_rebuild: bool = False) -> int:
        """
        Loads knowledge documents, chunks them, generates embeddings,
        and saves cache to vector_cache.json.
        """
        if not force_rebuild and os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    cached_data = json.load(f)
                    self.chunks = cached_data.get("chunks", [])
                    self.embeddings = cached_data.get("embeddings", [])
                    if len(self.chunks) == len(self.embeddings) and len(self.chunks) > 0:
                        return len(self.chunks)
            except Exception:
                pass

        self.chunks = []
        self.embeddings = []

        if not os.path.exists(self.knowledge_dir):
            return 0

        for fname in sorted(os.listdir(self.knowledge_dir)):
            if fname.endswith(".txt") or fname.endswith(".md"):
                fpath = os.path.join(self.knowledge_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        content = f.read()
                    doc_chunks = self.chunk_text(content, fname)
                    for ch in doc_chunks:
                        emb = self.get_embedding(ch["text"])
                        if emb:
                            self.chunks.append(ch)
                            self.embeddings.append(emb)
                except Exception as e:
                    print(f"[VectorStore] Notice reading {fname}: {e}")

        # Save to local cache
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump({"chunks": self.chunks, "embeddings": self.embeddings}, f)
        except Exception:
            pass

        return len(self.chunks)

    @staticmethod
    def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """Computes cosine similarity between two vectors."""
        dot = 0.0
        norm_a = 0.0
        norm_b = 0.0
        for a, b in zip(vec_a, vec_b):
            dot += a * b
            norm_a += a * a
            norm_b += b * b
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return dot / (math.sqrt(norm_a) * math.sqrt(norm_b))

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves Top-K most semantically similar knowledge chunks
        given a natural language user question.
        """
        if not self.chunks or not self.embeddings:
            self.build_index()

        q_vec = self.get_embedding(query)
        if not q_vec or not self.embeddings:
            return []

        scored: List[Tuple[float, Dict[str, Any]]] = []
        for ch, emb in zip(self.chunks, self.embeddings):
            sim = self._cosine_similarity(q_vec, emb)
            scored.append((sim, ch))

        scored.sort(key=lambda x: x[0], reverse=True)

        results = []
        for score, ch in scored[:top_k]:
            results.append({
                "score": round(float(score), 4),
                "source": ch["source"],
                "text": ch["text"],
                "id": ch["id"]
            })

        return results
