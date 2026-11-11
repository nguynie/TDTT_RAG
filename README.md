# 🏙️ Lumen Travel Assistant with RAG Chat (TP. Hồ Chí Minh)

Dự án Trợ lý Du lịch Thông minh dành cho **Thành phố Hồ Chí Minh**, kết hợp xác thực người dùng bằng **Firebase Authentication** và hệ thống hỏi đáp chính xác bằng kỹ thuật **RAG (Retrieval-Augmented Generation)** với **Ollama**.

---

## 📌 Thông tin sinh viên & Đề tài
- **Môn học:** Tư duy tính toán (Computational Thinking - CSC10014)
- **Bài tập:** Practice 03 - Sign-in Travel Assistant with RAG Chat
- **Họ và tên sinh viên:** *(Điền họ tên của bạn vào đây)*
- **Mã số sinh viên (MSSV):** *(Điền MSSV của bạn vào đây)*
- **Thành phố lựa chọn:** **TP. Hồ Chí Minh (TP.HCM)**
- **Video Demonstration:** [Đường dẫn YouTube / Google Drive của bạn]

---

## 🛠️ Hướng dẫn cài đặt và Khởi chạy

### 1. Chuẩn bị môi trường
Yêu cầu hệ điều hành có cài đặt **Python 3.10+**.

Tạo và kích hoạt môi trường ảo (virtual environment):
```bash
python3 -m venv .venv
source .venv/bin/activate   # Trên Linux/macOS
# Hoặc .venv\Scripts\activate trên Windows
```

Cài đặt các gói thư viện cần thiết:
```bash
pip install -r requirements.txt
```

### 2. Cấu hình biến môi trường (`.env`)
Sao chép file `.env.example` thành `.env`:
```bash
cp .env.example .env
```
Điền các giá trị thực tế vào file `.env`:
```ini
# Firebase Authentication (lấy từ Firebase Console > Project Settings)
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_API_KEY=your-firebase-web-api-key

# Địa chỉ máy chủ Ollama (hoặc đường dẫn Pinggy tunnel từ Lab 4)
OLLAMA_BASE_URL=http://localhost:11434

# Tên mô hình
EMBEDDING_MODEL=embeddinggemma
CHAT_MODEL=qwen3:4b

# Tham số RAG
TOP_K=3
SIMILARITY_THRESHOLD=0.25
```

> **Lưu ý quan trọng:** Không bao giờ commit file `.env` lên GitHub (file này đã được đưa vào `.gitignore`).

### 3. Chạy ứng dụng Streamlit
```bash
streamlit run app.py
```
Sau đó truy cập trình duyệt tại địa chỉ: `http://localhost:8501`.

---

## 📊 Bảng kiểm thử (Test Table)

Dưới đây là kết quả kiểm thử trên 6 câu hỏi tiêu biểu (3 câu có trong cẩm nang, 1 câu diễn đạt lại - paraphrase, 2 câu ngoài cẩm nang):

| STT | Câu hỏi kiểm thử | Loại câu hỏi | Expected ID | Retrieved IDs | Kết quả | Phân tích lỗi (nếu sai) |
|:---:|:---|:---:|:---:|:---:|:---:|:---|
| **1** | Giá vé tham quan Dinh Độc Lập cho người lớn là bao nhiêu? | Trực tiếp | `[G01]` | `[G01]`, `[G12]`, `[G05]` | ✅ Đúng | Trả lời chính xác 40.000 VNĐ, trích dẫn `[G01]`. |
| **2** | Giờ mở cửa của Bảo tàng Chứng tích Chiến tranh? | Trực tiếp | `[G05]` | `[G05]`, `[G12]`, `[G01]` | ✅ Đúng | Trả lời chính xác 7:30 - 17:30, trích dẫn `[G05]`. |
| **3** | Phố đi bộ Bùi Viện cấm xe vào khung giờ nào cuối tuần? | Trực tiếp | `[G11]` | `[G11]`, `[G06]`, `[G02]` | ✅ Đúng | Trả lời chính xác từ 19:00 đến 2:00 sáng hôm sau, trích dẫn `[G11]`. |
| **4** | Ở Sài Gòn muốn đi tàu ngắm hoàng hôn trên sông thì đi ở đâu và giá vé thế nào? | Paraphrase (Diễn đạt lại) | `[G14]` | `[G14]`, `[G06]`, `[G10]` | ✅ Đúng | Nhận diện đúng tuyến buýt sông Saigon Waterbus tại Bến Bạch Đằng, giá 15.000 VNĐ/lượt, trích dẫn `[G14]`. |
| **5** | Giá vé vào cổng Sun World Bà Nà Hills là bao nhiêu? | Ngoài cẩm nang (Địa điểm Đà Nẵng) | Không có (`None`) | `[G10]`, `[G07]`, `[G14]` (Điểm tương đồng thấp) | ✅ Đúng | Trợ lý trả lời: "Tôi không biết thông tin này vì cẩm nang du lịch Lumen Travel hiện chưa cập nhật." (Không đoán mò). |
| **6** | Lẩu dê Trương Định mở cửa đến mấy giờ? | Ngoài cẩm nang (Quán ăn ngoài danh mục) | Không có (`None`) | `[G13]`, `[G15]`, `[G02]` | ✅ Đúng | Trợ lý từ chối trả lời vì cẩm nang chưa cập nhật thông tin quán này. |

---

## 🧠 Phân tích 4 trụ cột Tư duy tính toán (Computational Thinking)

### 1. Trừu tượng hóa (Abstraction)
- **Input của hệ thống:** Câu hỏi bằng ngôn ngữ tự nhiên từ người dùng đã đăng nhập.
- **Output của hệ thống:** Câu trả lời chuẩn xác chỉ dựa trên ngữ cảnh kèm trích dẫn ID mục (`[Gxx]`) và danh sách mục tham khảo kèm điểm tương đồng (Cosine Similarity Score).
- **Mô hình hóa dữ liệu cẩm nang (`knowledge_base.json`):**
  - Giữ lại các trường: `id`, `title`, `category`, `tags`, `text`, `source`.
  - **Lý do:**
    - `id`, `title`, `text`: Đầy đủ ngữ nghĩa để thực hiện tìm kiếm vector và cung cấp ngữ cảnh cho LLM.
    - `category`, `tags`: Hỗ trợ phân loại địa điểm và phục vụ làm tiền đề cho hệ thống gợi ý du lịch (Assignment 04 - RAG-Rec).
    - Lược bỏ các thông tin rườm rà (hình ảnh thô, mã HTML) để giữ context gọn gàng, tăng tốc độ xử lý embedding.

### 2. Phân rã bài toán (Decomposition)
Hệ thống được chia thành 6 module/bài toán con nối tiếp:
```
[1. Sign-in]
    ↓ (User Token / Email)
[2. Embed User Query]
    ↓ (Query Vector)
[3. Retrieve Top-K & Score]
    ↓ (Top-k Relevant Chunks + Scores)
[4. Build Context & System Prompt]
    ↓ (Augmented Prompt)
[5. Generate via Ollama LLM]
    ↓ (Strict Fact-based Answer)
[6. Display & Session History]
```
- **Hộp 1 (Sign-in):** In: Email, Password $\rightarrow$ Out: Firebase Session (`uid`, `token`).
- **Hộp 2 (Embed):** In: Chuỗi câu hỏi $\rightarrow$ Out: Vector số thực biểu diễn ngữ nghĩa.
- **Hộp 3 (Retrieve):** In: Query Vector + Indexed KB $\rightarrow$ Out: Danh sách Top-K mục có Cosine Similarity cao nhất.
- **Hộp 4 (Build Context):** In: Top-K Entries + Query $\rightarrow$ Out: Prompt kèm quy tắc không bịa đặt.
- **Hộp 5 (Generate):** In: Prompt $\rightarrow$ Out: Câu trả lời văn bản kèm trích dẫn.
- **Hộp 6 (Display):** In: Output văn bản + Scores $\rightarrow$ Out: Giao diện chat Streamlit + Expander điểm số.

### 3. Nhận diện mẫu (Pattern Recognition)
- **Kế thừa từ Lab 3 & Lab 4:**
  - Mô hình xác thực Client-side REST API với Firebase Auth (Lab 3).
  - Kết nối mô hình nhúng và sinh qua Ollama API (Lab 4).
- **Mẫu thiết kế (Design Pattern):** Mẫu kinh điển **Filter $\rightarrow$ Score $\rightarrow$ Top-K**:
  - Tính điểm tương đồng góc giữa vector câu hỏi và từng vector tài liệu (Cosine Similarity).
  - Sắp xếp giảm dần và lấy $K$ kết quả cao nhất.
- **Áp dụng tiếp trong RAG-Rec (Assignment 4):**
  - Mẫu này sẽ tiếp tục được mở rộng khi người dùng đưa ra sở thích (vd: thích `museum`, ngân sách $< 50k$), hệ thống sẽ kết hợp *Metadata Filtering* (theo `category`, `tags`) cùng với *Vector Scoring* để xếp hạng địa điểm đề xuất.

### 4. Thiết kế thuật toán (Algorithm Design)

#### Mã giả (Pseudocode) xử lý một câu hỏi:
```text
Thuật toán: TraCuuRAG(cau_hoi, danh_sach_cam_nang, top_k, nguong_similarity)
    1. query_vector ← LayEmbedding(cau_hoi, model="embeddinggemma")
    2. danh_sach_diem ← []
    3. FOR MOI (muc, vector_muc) TRONG danh_sach_cam_nang DO:
           diem ← TinhCosineSimilarity(query_vector, vector_muc)
           Them (muc, diem) VAO danh_sach_diem
       ENDFOR
    4. SapXepGiamDanTheoDiem(danh_sach_diem)
    5. top_entries ← danh_sach_diem[0 : top_k]
    6. IF top_entries[0].diem < nguong_similarity THEN:
           RETURN "Tôi không biết thông tin này vì cẩm nang chưa cập nhật."
       ENDIF
    7. prompt_ngu_canh ← TaoPrompt(top_entries, cau_hoi)
    8. cau_tra_loi ← GoiOllamaChat(model="qwen3:4b", prompt_ngu_canh)
    9. RETURN cau_tra_loi, top_entries
```

#### Quyết định thiết kế (Design Decision):
- **Chọn $K = 3$:** Vì các đoạn văn trong cẩm nang về một địa điểm đã chứa trọn vẹn thông tin (địa chỉ, giá vé, giờ mở cửa). Lựa chọn $K=3$ cung cấp đủ ngữ cảnh cho các câu hỏi so sánh hoặc diễn đạt lại mà không làm bão hòa context window của mô hình `qwen3:4b`.
- **Ngưỡng tương đồng kết hợp System Prompt chống đoán mò:** Đặt ngưỡng `SIMILARITY_THRESHOLD = 0.25` kết hợp System Prompt với nhiệt độ `temperature = 0.1`. Khi câu hỏi hoàn toàn lạc đề, điểm số thấp sẽ kích hoạt phản hồi "Tôi không biết" ngay lập tức, tiết kiệm thời gian gọi LLM.

---

## ⚠️ Hạn chế đã biết (Known Limitations) & AI Tools
- **Hạn chế đã biết:**
  - Cẩm nang hiện tại giới hạn ở 15 địa điểm nổi bật của TP.HCM; các hàng quán nhỏ hoặc địa điểm mới xuất hiện chưa được cập nhật.
  - Tốc độ sinh phản hồi phụ thuộc vào băng thông và cấu hình máy chủ chạy Ollama (Pinggy tunnel).
- **Công cụ AI hỗ trợ:**
  - Sử dụng AI Coding Assistant để tham khảo cú pháp Streamlit và viết prompt cho LLM. Toàn bộ logic giải thuật, tích hợp và kiểm thử do sinh viên tự hoàn thiện và kiểm soát.
