"""RAG module for Lumen Travel Assistant.
Implements embedding computation, cosine similarity retrieval, and generation with Ollama.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import requests

from config import CHAT_MODEL, EMBEDDING_MODEL, OLLAMA_BASE_URL, SIMILARITY_THRESHOLD, TOP_K

OLLAMA_TIMEOUT = 120


class RAGError(Exception):
    """User-safe exception for RAG pipeline errors."""
    pass


def load_knowledge_base(file_path: str = "knowledge_base.json") -> List[Dict[str, Any]]:
    """Load knowledge base from JSON file."""
    path = Path(file_path)
    if not path.is_file():
        path = Path(__file__).resolve().parent / file_path
    if not path.is_file():
        raise RAGError(f"Không tìm thấy file cẩm nang: {file_path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Dữ liệu knowledge base phải là một danh sách.")
        return data
    except Exception as e:
        raise RAGError(f"Lỗi khi đọc knowledge_base.json: {e}") from e


def get_embedding(text: str, base_url: str = OLLAMA_BASE_URL, model: str = EMBEDDING_MODEL) -> np.ndarray:
    """Compute embedding vector using Ollama's embedding API.
    Supports both /api/embeddings and /api/embed endpoints.
    """
    if not text.strip():
        raise RAGError("Không thể tính embedding cho văn bản trống.")

    cleaned_url = base_url.rstrip("/")
    if not cleaned_url:
        raise RAGError("Ollama URL chưa được cấu hình. Vui lòng kiểm tra file .env.")

    # 1. Try legacy /api/embeddings endpoint
    try:
        res = requests.post(
            f"{cleaned_url}/api/embeddings",
            json={"model": model, "prompt": text},
            timeout=OLLAMA_TIMEOUT,
        )
        if res.status_code == 200:
            vec = res.json().get("embedding")
            if vec and isinstance(vec, list):
                arr = np.array(vec, dtype=np.float32)
                norm = np.linalg.norm(arr)
                return arr / norm if norm > 0 else arr
    except requests.RequestException:
        pass

    # 2. Try newer /api/embed endpoint
    try:
        res = requests.post(
            f"{cleaned_url}/api/embed",
            json={"model": model, "input": text},
            timeout=OLLAMA_TIMEOUT,
        )
        if res.status_code == 200:
            data = res.json()
            embeddings = data.get("embeddings") or [data.get("embedding")]
            if embeddings and isinstance(embeddings, list) and embeddings[0]:
                arr = np.array(embeddings[0], dtype=np.float32)
                norm = np.linalg.norm(arr)
                return arr / norm if norm > 0 else arr
    except requests.RequestException as e:
        raise RAGError(f"Không thể kết nối đến máy chủ Ollama tại {cleaned_url}. Kiểm tra server hoặc kết nối mạng.") from e

    raise RAGError(f"Máy chủ Ollama không trả về embedding với model '{model}'. Kiểm tra model đã được tải chưa.")


def index_knowledge_base(kb: List[Dict[str, Any]], base_url: str = OLLAMA_BASE_URL) -> List[Tuple[Dict[str, Any], np.ndarray]]:
    """Compute and cache embeddings for all knowledge base items."""
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
    """Retrieve top-k relevant entries for a given query with similarity scores."""
    if not query.strip():
        return []

    q_vec = get_embedding(query, base_url=base_url)
    scored_items = []
    for item, item_vec in indexed_kb:
        score = cosine_similarity(q_vec, item_vec)
        scored_items.append((item, score))

    # Sort descending by cosine similarity score
    scored_items.sort(key=lambda x: x[1], reverse=True)
    return scored_items[:top_k]


def build_system_prompt(retrieved_entries: List[Tuple[Dict[str, Any], float]]) -> str:
    """Construct a strict system prompt preventing hallucination and enforcing citations."""
    context_chunks = []
    for item, score in retrieved_entries:
        context_chunks.append(
            f"Mục [{item['id']}] - {item['title']} (Chủ đề: {item.get('category', 'Chung')}):\n"
            f"{item['text']}\n"
            f"(Nguồn: {item.get('source', 'Lumen Travel')})"
        )

    context_str = "\n\n".join(context_chunks)

    prompt = (
        "Bạn là trợ lý du lịch AI chính thức của Lumen Travel chuyên cung cấp thông tin du lịch về TP. Hồ Chí Minh.\n\n"
        "QUY TẮC CỐT LÕI (BẮT BUỘC TUÂN THỦ NGHIÊM NGẶT):\n"
        "1. Bạn CHỈ ĐƯỢC PHÉP trả lời dựa trên các thông tin có trong phần [NGỮ CẢNH CẨM NANG] bên dưới.\n"
        "2. Mọi thông tin cung cấp (địa chỉ, giá vé, giờ mở cửa, lịch sử, ẩm thực,...) PHẢI kèm mã định danh mục tương ứng trong ngoặc vuông, ví dụ: [G01], [G02], [G05].\n"
        "3. NGUYÊN TẮC 'TÔI KHÔNG BIẾT' (I DON'T KNOW): Nếu câu hỏi của người dùng hỏi về địa điểm, giá cả, dịch vụ, hoặc thông tin KHÔNG có trong [NGỮ CẢNH CẨM NANG], bạn PHẢI trả lời chính xác: 'Tôi không biết thông tin này vì cẩm nang du lịch Lumen Travel hiện chưa cập nhật.' Tuyệt đối KHÔNG ĐƯỢC đoán mò, KHÔNG tự suy diễn, và KHÔNG dùng kiến thức bên ngoài.\n"
        "4. Trả lời bằng tiếng Việt lịch sự, tự nhiên, súc tích và đúng trọng tâm câu hỏi.\n\n"
        "=== [NGỮ CẢNH CẨM NANG] ===\n"
        f"{context_str}\n"
        "=== HẾT NGỮ CẢNH ==="
    )
    return prompt


def generate_rag_answer(
    query: str,
    retrieved_entries: List[Tuple[Dict[str, Any], float]],
    base_url: str = OLLAMA_BASE_URL,
    chat_model: str = CHAT_MODEL,
) -> str:
    """Generate final answer using Ollama qwen3:4b model."""
    cleaned_url = base_url.rstrip("/")
    if not cleaned_url:
        raise RAGError("Ollama URL chưa được cấu hình trong .env.")

    # Check if all scores are lower than minimum threshold
    max_score = retrieved_entries[0][1] if retrieved_entries else 0.0
    if max_score < SIMILARITY_THRESHOLD:
        return "Tôi không biết thông tin này vì cẩm nang du lịch Lumen Travel hiện chưa cập nhật."

    system_prompt = build_system_prompt(retrieved_entries)

    # 1. Try /api/chat
    payload = {
        "model": chat_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        "stream": False,
        "options": {
            "temperature": 0.1,  # Low temperature for factual consistency
        },
    }

    try:
        res = requests.post(f"{cleaned_url}/api/chat", json=payload, timeout=OLLAMA_TIMEOUT)
        if res.status_code == 200:
            data = res.json()
            content = data.get("message", {}).get("content", "").strip()
            if content:
                return content
    except requests.RequestException:
        pass

    # 2. Fallback to /api/generate
    gen_payload = {
        "model": chat_model,
        "prompt": f"{system_prompt}\n\nNgười dùng: {query}\nTrợ lý:",
        "stream": False,
        "options": {
            "temperature": 0.1,
        },
    }

    try:
        res = requests.post(f"{cleaned_url}/api/generate", json=gen_payload, timeout=OLLAMA_TIMEOUT)
        if res.status_code == 200:
            data = res.json()
            content = data.get("response", "").strip()
            if content:
                return content
        else:
            raise RAGError(f"Ollama trả về mã lỗi {res.status_code}: {res.text}")
    except requests.RequestException as e:
        raise RAGError(f"Không thể kết nối đến máy chủ Ollama tại {cleaned_url}. Chi tiết: {e}") from e

    raise RAGError("Không nhận được câu trả lời từ mô hình sinh.")
