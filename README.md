# Lumen Travel Assistant with RAG Chat (Ho Chi Minh City)

An intelligent travel assistant for **Ho Chi Minh City**, combining user authentication via **Firebase Authentication** and grounded question answering using **Retrieval-Augmented Generation (RAG)** powered by **Ollama**.

---

## Student Information & Topic
- **Course:** Computational Thinking (CSC10014)
- **Assignment:** Practice 03 - Sign-in Travel Assistant with RAG Chat
- **Student Name:** Nguyen Ngoc Phuc Nguyen
- **Student ID:** 25127434
- **Selected City:** Ho Chi Minh City
- **Demonstration Video:** [Your YouTube / Google Drive link]

---

## Installation & Running Instructions

### 1. Environment Setup
Requires **Python 3.10+**.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Variables Configuration (`.env`)
```bash
cp .env.example .env
```

Set the values in `.env`:
```ini
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_API_KEY=your-firebase-web-api-key
OLLAMA_BASE_URL=http://localhost:11434
EMBEDDING_MODEL=embeddinggemma
CHAT_MODEL=qwen3:4b
TOP_K=3
SIMILARITY_THRESHOLD=0.25
```

### 3. Run the Streamlit Application
```bash
streamlit run app.py
```
Open browser at `http://localhost:8501`.

---

## Test Table

| No. | Test Question | Type | Expected ID | Retrieved IDs | Result | Failure Analysis (if failed) |
|:---:|:---|:---:|:---:|:---:|:---:|:---|
| 1 | What is the adult admission ticket price for Independence Palace? | Answerable | `[G01]` | `[G01]`, `[G12]`, `[G05]` | Pass | Correctly answered 40,000 VND citing `[G01]`. |
| 2 | What are the opening hours of the War Remnants Museum? | Answerable | `[G05]` | `[G05]`, `[G12]`, `[G01]` | Pass | Correctly answered 7:30 AM to 5:30 PM citing `[G05]`. |
| 3 | During which hours on weekends is Bui Vien Walking Street closed to vehicles? | Answerable | `[G11]` | `[G11]`, `[G06]`, `[G02]` | Pass | Correctly answered 7:00 PM to 2:00 AM citing `[G11]`. |
| 4 | Where can I take a boat trip to watch the sunset on the river in Saigon and how much does it cost? | Paraphrase | `[G14]` | `[G14]`, `[G06]`, `[G10]` | Pass | Correctly identified Saigon Waterbus at Bach Dang Wharf, 15,000 VND one-way, citing `[G14]`. |
| 5 | How much is the entrance ticket to Sun World Ba Na Hills? | Not in guide | `None` | `[G10]`, `[G07]`, `[G14]` | Pass | Correctly rejected: "I don't know this information as it is not currently covered in the Lumen Travel guide." |
| 6 | What time does Truong Dinh Goat Hotpot restaurant close? | Not in guide | `None` | `[G13]`, `[G15]`, `[G02]` | Pass | Correctly refused to speculate and stated the guide does not cover this restaurant. |

---

## Computational Thinking Analysis

### 1. Abstraction
- **System Inputs:** Natural language queries submitted by authenticated users.
- **System Outputs:** Factually grounded responses citing entry IDs (`[Gxx]`), accompanied by retrieved entries and their cosine similarity scores.
- **Data Modeling (`knowledge_base.json`):**
  - Retained fields: `id`, `title`, `category`, `tags`, `text`, `source`.
  - **Rationale:**
    - `id`, `title`, `text`: Provide sufficient semantic context for vector retrieval and grounded generation.
    - `category`, `tags`: Enable structured categorization and prepare foundational metadata for recommendation filtering in Assignment 04 (RAG-Rec).
    - Unstructured layout artifacts (HTML tags, raw image URLs) were omitted to preserve context window capacity and accelerate embedding computation.

### 2. Decomposition
The application decomposes into 6 sequential sub-problems:
```
[1. Sign-in]
    ↓ (Firebase Session: UID, Token)
[2. Embed User Query]
    ↓ (Query Vector)
[3. Retrieve Top-K & Score]
    ↓ (Top-K Chunks + Similarity Scores)
[4. Build Context & System Prompt]
    ↓ (Grounded Prompt)
[5. Generate via Ollama LLM]
    ↓ (Fact-based Answer with Citations)
[6. Display & Session History]
```
- **Box 1 (Sign-in):** In: Email, Password -> Out: Firebase session (`uid`, `id_token`).
- **Box 2 (Embed):** In: Query string -> Out: Dense embedding vector.
- **Box 3 (Retrieve):** In: Query Vector + Indexed KB -> Out: Top-K entries with highest Cosine Similarity.
- **Box 4 (Build Context):** In: Top-K Entries + Query -> Out: Grounded prompt enforcing the "I don't know" policy.
- **Box 5 (Generate):** In: Augmented prompt -> Out: Grounded response with `[Gxx]` citations.
- **Box 6 (Display):** In: Response text + Scores -> Out: Streamlit chat interface + expandable score inspection.

### 3. Pattern Recognition
- **Reuse from Labs 3 & 4:**
  - Client-side REST authentication with Firebase Auth (Lab 3).
  - Model embedding and generation via Ollama HTTP endpoints (Lab 4).
- **Core Pattern:** The classic **Filter -> Score -> Top-K** workflow:
  - Compute angle similarity between the query vector and document vectors (Cosine Similarity).
  - Rank in descending order and select top $K$ items.
- **Application in RAG-Rec (Assignment 4):**
  - This pattern will extend to user preferences: combining metadata filtering (by `category` or `tags`) with vector similarity scoring to recommend travel itineraries.

### 4. Algorithm Design

#### Pseudocode for answering one query:
```text
Algorithm: AnswerTravelQuery(query, indexed_kb, top_k, similarity_threshold)
    1. query_vector <- GetEmbedding(query, model="embeddinggemma")
    2. scored_list <- []
    3. FOR EACH (entry, entry_vector) IN indexed_kb DO:
           score <- CosineSimilarity(query_vector, entry_vector)
           Append (entry, score) TO scored_list
       ENDFOR
    4. SortDescendingByScore(scored_list)
    5. top_entries <- scored_list[0 : top_k]
    6. IF top_entries[0].score < similarity_threshold THEN:
           RETURN "I don't know this information as it is not currently covered in the Lumen Travel guide."
       ENDIF
    7. prompt <- ConstructPrompt(top_entries, query)
    8. answer <- OllamaChat(model="qwen3:4b", prompt)
    9. RETURN answer, top_entries
```

#### Design Decisions:
- **Selection of $K = 3$:** Each knowledge base entry is self-contained with comprehensive details (address, fee, schedule). A value of $K = 3$ provides sufficient breadth for multi-faceted or paraphrased questions without polluting the context window.
- **Two-tier Hallucination Prevention:** A strict similarity cutoff (`SIMILARITY_THRESHOLD = 0.25`) rejects irrelevant queries early without consuming LLM generation tokens. For borderline queries, a low temperature (`temperature = 0.1`) and explicit system prompt constraints force the model to declare lack of information rather than speculate.

---

## Known Limitations & AI Tools Note
- **Known Limitations:**
  - The guide currently covers 15 key landmarks in Ho Chi Minh City; unlisted smaller venues or newly established locations are not present.
  - Response latency depends on the network tunnel (Pinggy) and inference hardware hosting the Ollama server.
- **AI Tools Used:**
  - AI coding assistance was utilized for Streamlit syntax reference and prompt template drafting. Core architectural design, algorithmic pipeline, and test verification were independently validated by the student.
