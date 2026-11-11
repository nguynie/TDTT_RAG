import json
from pathlib import Path
import re
from typing import Any, Dict, List, Tuple

import numpy as np
import requests

from config import CHAT_MODEL, EMBEDDING_MODEL, OLLAMA_BASE_URL, SIMILARITY_THRESHOLD, TOP_K

OLLAMA_TIMEOUT = 120


class RAGError(Exception):
    """User-safe exception for RAG pipeline errors."""
    pass


def _clean_llm_output(text: str) -> str:
    """Strip <think>...</think> reasoning blocks from model responses."""
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return cleaned.strip()


def load_knowledge_base(file_path: str = "knowledge_base.json") -> List[Dict[str, Any]]:
    """Load travel knowledge base from JSON file."""
    path = Path(file_path)
    if not path.is_file():
        path = Path(__file__).resolve().parent / file_path
    if not path.is_file():
        raise RAGError(f"Knowledge base file not found: {file_path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Knowledge base data must be a list of entries.")
        return data
    except Exception as e:
        raise RAGError(f"Error reading knowledge base: {e}") from e


def get_embedding(text: str, base_url: str = OLLAMA_BASE_URL, model: str = EMBEDDING_MODEL) -> np.ndarray:
    """Compute embedding vector using Ollama embedding API."""
    if not text.strip():
        raise RAGError("Cannot compute embedding for empty text.")

    cleaned_url = base_url.rstrip("/")
    if not cleaned_url:
        raise RAGError("Ollama URL is not configured. Please check your .env file.")

    try:
        res = requests.post(
            f"{cleaned_url}/api/embed",
            json={"model": model, "input": text},
            timeout=OLLAMA_TIMEOUT,
        )
        # Fallback to legacy endpoint only if /api/embed is not found on older Ollama versions
        if res.status_code == 404 and "model" not in res.text.lower():
            res = requests.post(
                f"{cleaned_url}/api/embeddings",
                json={"model": model, "prompt": text},
                timeout=OLLAMA_TIMEOUT,
            )
    except requests.RequestException as e:
        raise RAGError(f"Unable to connect to Ollama server at {cleaned_url}. Check network or Pinggy tunnel.") from e

    if res.status_code in (502, 503, 504):
        raise RAGError(f"Ollama server via tunnel ({cleaned_url}) is unreachable (HTTP {res.status_code}).")
    if res.status_code != 200:
        raise RAGError(f"Ollama embedding error (HTTP {res.status_code}): {res.text}")

    data = res.json()
    embeddings = data.get("embeddings") or ([data.get("embedding")] if data.get("embedding") else [])
    if embeddings and isinstance(embeddings, list) and embeddings[0]:
        arr = np.array(embeddings[0], dtype=np.float32)
        norm = np.linalg.norm(arr)
        return arr / norm if norm > 0 else arr

    raise RAGError(f"Ollama server returned no embedding for model '{model}'. Verify model is pulled.")


def index_knowledge_base(kb: List[Dict[str, Any]], base_url: str = OLLAMA_BASE_URL) -> List[Tuple[Dict[str, Any], np.ndarray]]:
    """Compute embeddings for all knowledge base items."""
    indexed = []
    for item in kb:
        tags_str = ", ".join(item.get("tags", [])) if item.get("tags") else ""
        content_to_embed = f"{item['title']} - {item.get('category', '')}: {item['text']} {tags_str}".strip()
        vec = get_embedding(content_to_embed, base_url=base_url)
        indexed.append((item, vec))
    return indexed


def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors."""
    dot = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(dot / (norm1 * norm2))


def retrieve_relevant_entries(
    query: str,
    indexed_kb: List[Tuple[Dict[str, Any], np.ndarray]],
    base_url: str = OLLAMA_BASE_URL,
    top_k: int = TOP_K,
) -> List[Tuple[Dict[str, Any], float]]:
    """Retrieve top-k relevant entries for a given query sorted by cosine similarity."""
    if not query.strip():
        return []

    q_vec = get_embedding(query, base_url=base_url)
    scored_items = []
    for item, item_vec in indexed_kb:
        score = cosine_similarity(q_vec, item_vec)
        scored_items.append((item, score))

    scored_items.sort(key=lambda x: x[1], reverse=True)
    return scored_items[:top_k]


def build_system_prompt(retrieved_entries: List[Tuple[Dict[str, Any], float]]) -> str:
    """Construct system prompt enforcing factual grounding and citations."""
    context_chunks = []
    for item, _ in retrieved_entries:
        context_chunks.append(
            f"Entry [{item['id']}] - {item['title']} (Category: {item.get('category', 'general')}):\n"
            f"{item['text']}\n"
            f"(Source: {item.get('source', 'Lumen Travel')})"
        )

    context_str = "\n\n".join(context_chunks)

    prompt = (
        "You are the official AI travel assistant of Lumen Travel specializing in Ho Chi Minh City tourism.\n\n"
        "CORE RULES (STRICT COMPLIANCE REQUIRED):\n"
        "1. You may ONLY answer based on the information provided in the [TRAVEL GUIDE CONTEXT] below.\n"
        "2. Every factual statement (address, admission fee, opening hours, history, food, etc.) MUST cite its corresponding entry ID in square brackets, e.g. [G01], [G02], [G05].\n"
        "3. 'I DON'T KNOW' RULE: If the user's question asks about places, prices, services, or details NOT contained in [TRAVEL GUIDE CONTEXT], you MUST answer exactly: 'I don't know this information as it is not currently covered in the Lumen Travel guide.' Never guess, speculate, or introduce external knowledge.\n"
        "4. Reply in clear, polite, and concise English.\n\n"
        "=== [TRAVEL GUIDE CONTEXT] ===\n"
        f"{context_str}\n"
        "=== END CONTEXT ==="
    )
    return prompt


def generate_rag_answer(
    query: str,
    retrieved_entries: List[Tuple[Dict[str, Any], float]],
    base_url: str = OLLAMA_BASE_URL,
    chat_model: str = CHAT_MODEL,
) -> str:
    """Generate final answer using Ollama model."""
    cleaned_url = base_url.rstrip("/")
    if not cleaned_url:
        raise RAGError("Ollama URL is not configured in .env.")

    max_score = retrieved_entries[0][1] if retrieved_entries else 0.0
    if max_score < SIMILARITY_THRESHOLD:
        return "I don't know this information as it is not currently covered in the Lumen Travel guide."

    system_prompt = build_system_prompt(retrieved_entries)

    payload = {
        "model": chat_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        "stream": False,
        "options": {
            "temperature": 0.1,
        },
    }

    try:
        res = requests.post(f"{cleaned_url}/api/chat", json=payload, timeout=OLLAMA_TIMEOUT)
        if res.status_code in (502, 503, 504):
            raise RAGError(f"Ollama server via tunnel ({cleaned_url}) is unreachable (HTTP {res.status_code}).")
        if res.status_code == 200:
            data = res.json()
            content = data.get("message", {}).get("content", "").strip()
            if content:
                return _clean_llm_output(content)
    except requests.RequestException:
        pass

    gen_payload = {
        "model": chat_model,
        "prompt": f"{system_prompt}\n\nUser: {query}\nAssistant:",
        "stream": False,
        "options": {
            "temperature": 0.1,
        },
    }

    try:
        res = requests.post(f"{cleaned_url}/api/generate", json=gen_payload, timeout=OLLAMA_TIMEOUT)
        if res.status_code in (502, 503, 504):
            raise RAGError(f"Ollama server via tunnel ({cleaned_url}) is unreachable (HTTP {res.status_code}).")
        if res.status_code == 200:
            data = res.json()
            content = data.get("response", "").strip()
            if content:
                return _clean_llm_output(content)
        else:
            raise RAGError(f"Ollama returned error status {res.status_code}: {res.text}")
    except requests.RequestException as e:
        raise RAGError(f"Unable to connect to Ollama server at {cleaned_url}: {e}") from e

    raise RAGError("No response received from generation model.")
