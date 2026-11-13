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

Requires **Python 3.10+**.

### 1. Environment Setup

#### Option A: macOS & Linux
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option B: Windows (PowerShell)
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```
> *Note for PowerShell:* If script execution is blocked, enable it by running:  
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

#### Option C: Windows (Command Prompt - CMD)
```cmd
:: Create virtual environment
python -m venv .venv

:: Activate virtual environment
.venv\Scripts\activate.bat

:: Install dependencies
pip install -r requirements.txt
```

---

### 2. Environment Variables Configuration (`.env`)

Copy `.env.example` to `.env`:

- **macOS / Linux:**
  ```bash
  cp .env.example .env
  ```
- **Windows (PowerShell or CMD):**
  ```cmd
  copy .env.example .env
  ```

Configure your credentials and server endpoints in `.env`:
```ini
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_API_KEY=your-firebase-web-api-key
OLLAMA_BASE_URL=http://localhost:11434
EMBEDDING_MODEL=embeddinggemma
CHAT_MODEL=qwen3:4b
TOP_K=3
SIMILARITY_THRESHOLD=0.25
```

---

### 3. Run the Streamlit Application

With your virtual environment activated (on Windows, macOS, or Linux):
```bash
streamlit run app.py
```
*(Alternative if `streamlit` is not in PATH: `python -m streamlit run app.py`)*

Open your browser at `http://localhost:8501`.

---

## Test Table

The evaluation table below covers 7 representative test cases, including answerable questions, a paraphrase query, out-of-guide questions, and an explicit retrieval bottleneck failure case:

| No. | Test Question | Type | Expected ID | Retrieved IDs | Result | Failure Analysis (if failed) |
|:---:|:---|:---:|:---:|:---:|:---:|:---|
| 1 | What is the adult admission ticket price for Independence Palace? | Answerable | `[G01]` | `[G01]`, `[G12]`, `[G05]` | Pass | Correctly answered 40,000 VND citing `[G01]`. |
| 2 | What are the opening hours of the War Remnants Museum? | Answerable | `[G05]` | `[G05]`, `[G12]`, `[G01]` | Pass | Correctly answered 7:30 AM to 5:30 PM citing `[G05]`. |
| 3 | During which hours on weekends is Bui Vien Walking Street closed to vehicles? | Answerable | `[G11]` | `[G11]`, `[G06]`, `[G02]` | Pass | Correctly answered 7:00 PM to 2:00 AM citing `[G11]`. |
| 4 | Where can I take a boat trip to watch the sunset on the river in Saigon and how much does it cost? | Paraphrase | `[G14]` | `[G14]`, `[G06]`, `[G10]` | Pass | Correctly identified Saigon Waterbus at Bach Dang Wharf, 15,000 VND one-way, citing `[G14]`. |
| 5 | How much is the entrance ticket to Sun World Ba Na Hills? | Not in guide | `None` | `[G10]`, `[G07]`, `[G14]` | Pass | Correctly rejected: "I don't know this information as it is not currently covered in the Lumen Travel guide." |
| 6 | What time does Truong Dinh Goat Hotpot restaurant close? | Not in guide | `None` | `[G13]`, `[G15]`, `[G02]` | Pass | Correctly refused to speculate and stated the guide does not cover this restaurant. |
| 7 | List all attractions in District 1 that offer free entrance or free exterior visiting, and state their opening hours. | Multi-entry aggregation | `[G03]`, `[G04]`, `[G06]`, `[G07]`, `[G11]` | `[G03]`, `[G04]`, `[G07]` | Fail | **Failed at Retrieval Step.** The knowledge base contains 5 free attractions in District 1, but due to `TOP_K = 3`, only 3 entries were retrieved, omitting `[G06]` and `[G11]`. The generator was factually accurate but incomplete due to the retrieval bottleneck. |

---

## Computational Thinking Analysis

### 1. Abstraction
- **System Inputs:** Natural language queries submitted by authenticated users.
- **System Outputs:** Factually grounded responses citing entry IDs (`[Gxx]`), accompanied by retrieved entries and their cosine similarity scores.
- **Data Modeling (`knowledge_base.json`):**
  - Retained fields: `id`, `title`, `category`, `tags`, `text`, `source`.
  - **Rationale:**
    - `title`, `category`, `text`, and `tags`: Concatenated into a unified content representation string to compute dense semantic embeddings during indexing.
    - `id`: Deliberately excluded from the embedding vector to prevent arbitrary alphanumeric identifiers (e.g. `G01`, `G05`) from distorting semantic vector distance. Retained solely for injection into the system prompt to enforce grounded citations `[Gxx]`.
    - `source`: Retained to supply clear document provenance in the LLM prompt and enable transparent verification for users via the expandable UI panel.
    - **Omitted Details:** Omitted low-utility unstructured data for travel Q&A such as exact GPS coordinates, raw image assets, subjective visitor reviews, and lengthy restoration history. Kept strictly core factual attributes susceptible to hallucination: street addresses, operating schedules, stratified ticket prices (adult/student/child), and signature features.

### 2. Decomposition
The application decomposes into an initialization pipeline and a runtime query pipeline:

```
[One-Time Indexing (@st.cache_resource)]
knowledge_base.json (15 entries) → Dense Embeddings → Indexed KB (Cached in RAM)

[Runtime Query Pipeline]
[1. Sign-in]
    ↓ (Firebase Session: UID, Token)
[2. Embed User Query]
    ↓ (Query Vector)
[3. Retrieve Top-K & Score]
    ↓ (Top-K Chunks + Similarity Scores)
[4. Filter & Build Context]  ──(Max Score < 0.25)──→ Return "I don't know..."
    ↓ (Grounded System Prompt)
[5. Generate via Ollama LLM]
    ↓ (Fact-based Answer with [Gxx] Citations, <think> Tags Stripped)
[6. Display & Session History]
```

- **Box 1 (Sign-in):** In: Email, Password -> Out: Firebase session (`uid`, `id_token`).
- **Box 2 (Embed Query):** In: Query string -> Out: Dense query vector.
- **Box 3 (Retrieve Top-K):** In: Query Vector + Cached `Indexed KB` -> Out: Top-K entries with Cosine Similarity scores.
- **Box 4 (Filter & Build Context):** In: Top-K Entries. Evaluates similarity cutoff ($\max(\text{score}) < 0.25$): if below threshold, terminates early and returns *"I don't know..."*; otherwise, formats retrieved entries into a strict Grounded System Prompt (the user query is passed separately to Box 5).
- **Box 5 (Generate):** In: Grounded System Prompt + User Query -> Out: Factual response with `[Gxx]` citations, with `<think>` reasoning blocks removed.
- **Box 6 (Display & Session History):** In: Response text + Retrieved entries/scores -> Out: Streamlit chat interface + expandable score inspection.

### 3. Pattern Recognition
- **Knowledge Reuse from Labs 3 & 4:**
  - **From Lab 3 (`firebase_client.py` & `app.py`):** Client-side REST authentication against `identitytoolkit.googleapis.com` (`signUp`, `signInWithPassword`), safe error translation mapping (`FirebaseError`), access gating via `if "user" not in st.session_state`, and session cleanup in `forget_user()` wiping `user` and `chat_history`.
  - **From Lab 4 (`ollama_pinggy.ipynb` & `rag.py`):** Colab + Pinggy tunnel server deployment pattern, HTTP endpoint integration with `/api/embed` (`embeddinggemma`) and `/api/chat` (`qwen3:4b`), $L_2$ vector normalization, and Cosine similarity computation.
- **Core Pattern: Filter -> Score -> Top-K:**
  - **In Current System (Assignment 3):**
    - **Filter:** Candidate space restricted to 15 verified Ho Chi Minh City entries (`knowledge_base.json`) + post-retrieval threshold filter ($\max(\text{score}) \ge 0.25$) to reject out-of-scope inquiries.
    - **Score:** Pairwise similarity scoring via $\text{CosineSimilarity}(\mathbf{q}, \mathbf{e}_i)$.
    - **Top-K:** Descending score ranking and slicing top $K = 3$ entries (`scored_items[:top_k]`).
  - **In Future Extension (Assignment 4 — RAG-Rec):**
    - **Filter:** Metadata pre-filtering based on user constraints (e.g., matching preference criteria with `category` such as `"museum"`, `"street_food"` and `tags` such as `"district_1"`, `"budget"`).
    - **Score:** Combined scoring integrating semantic cosine similarity and tag-match overlap.
    - **Top-K:** Selecting top $K$ ranked attractions for personalized itinerary generation by the LLM.

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
           RETURN "I don't know this information as it is not currently covered in the Lumen Travel guide.", top_entries
       ENDIF
    7. prompt <- ConstructPrompt(top_entries)
    8. answer <- OllamaChat(model="qwen3:4b", prompt, query)
    9. RETURN CleanOutput(answer), top_entries
```

#### Design Decisions with Real Examples:
- **Selection of $K = 3$ with Real Example:** Each knowledge base entry contains comprehensive details. Setting $K = 3$ provides adequate context without diluting the prompt. For example, in Test Question 3 (*"During which hours on weekends is Bui Vien Walking Street closed to vehicles?"*), retrieving $K=3$ pulls both `[G11]` (Bui Vien Walking Street) and `[G06]` (Nguyen Hue Walking Street), enabling `qwen3:4b` to contrast Bui Vien's hours (7:00 PM - 2:00 AM on Fri, Sat, Sun) from Nguyen Hue's hours (6:00 PM - 11:00 PM on Sat, Sun) without confusion.
- **Two-tier "I don't know" Rule with Real Example:** Tier 1 checks whether $\max(\text{score}) < 0.25$. Tier 2 enforces strict prompt constraints with low temperature (`temperature = 0.1`). For example, in Test Question 6 (*"What time does Truong Dinh Goat Hotpot restaurant close?"*), dining-related keywords produce a cosine similarity $> 0.25$ against food entries `[G13]` (Xom Chieu Alley) and `[G15]` (Ho Thi Ky Market), passing Tier 1. However, at Tier 2, `qwen3:4b` verifies that the retrieved entries do not contain Truong Dinh Goat Hotpot and strictly refuses to answer, eliminating hallucination.

---

## Known Limitations & AI Tools Note
- **Known Limitations:**
  - The guide currently covers 15 key landmarks in Ho Chi Minh City; unlisted smaller venues or newly established locations are not present.
  - Multi-constraint queries requiring broad aggregation across more than 3 locations are constrained by the `TOP_K = 3` retrieval bottleneck.
  - Response latency depends on the network tunnel (Pinggy) and inference hardware hosting the Ollama server.
- **AI Tools Used:**
  - AI coding assistance was utilized for Streamlit syntax reference and prompt template drafting. Core architectural design, algorithmic pipeline, and test verification were independently validated by the student.
