# PHÂN TÍCH TƯ DUY TÍNH TOÁN (COMPUTATIONAL THINKING ANALYSIS)
## Dự án: Lumen Travel Assistant - Trợ lý du lịch TP.HCM với RAG Chat

Tài liệu này trình bày giải pháp kỹ thuật của dự án theo 4 bước Tư duy tính toán (Computational Thinking) theo đúng yêu cầu tại Mục 5 của đề bài (`Assignment03_Auth_RAG_Chat.pdf`): *"Explain your own solution, not general definitions"* (Giải thích giải pháp cụ thể của bạn, không nêu định nghĩa chung chung).

---

### 1. Abstraction (Trừu tượng hóa)

Bước trừu tượng hóa tập trung vào việc xác định ranh giới bài toán, xác định chính xác dữ liệu đầu vào, đầu ra của hệ thống và tinh gọn dữ liệu cẩm nang du lịch:

* **Đầu vào của hệ thống (System Inputs):** Câu hỏi bằng ngôn ngữ tự nhiên từ người dùng đã đăng nhập thành công qua Firebase Authentication (ví dụ: giờ mở cửa, giá vé tham quan, địa chỉ các địa danh tại TP.HCM).
* **Đầu ra của hệ thống (System Outputs):** 
  - Câu trả lời tự nhiên được kiểm chứng thực tế (grounded response), bắt buộc trích dẫn mã định danh nguồn trong ngoặc vuông (ví dụ: `[G01]`, `[G05]`).
  - Danh sách các đoạn trích dẫn cẩm nang được lấy lên (Top-K entries) kèm theo điểm số tương đồng góc Cosine Similarity tương ứng (hiển thị trực quan trong thanh mở rộng `st.expander`).
* **Mô hình hóa dữ liệu cẩm nang (`knowledge_base.json`):**
  - **Các trường được giữ lại (Retained fields):** Mỗi mục cẩm nang được biểu diễn bằng 6 trường: `id`, `title`, `category`, `tags`, `text`, `source`.
  - **Lý do lựa chọn từng trường (Rationale):**
    - `title`, `category`, `text`, và `tags`: Được nối lại thành một chuỗi văn bản đại diện hợp nhất (`content_to_embed = f"{title} - {category}: {text} {tags}"`) để tạo vector nhúng ngữ nghĩa dày đặc (dense embedding) bằng mô hình `embeddinggemma` trong bước lập chỉ mục (indexing).
    - `id`: Cố tình **loại bỏ** khỏi chuỗi nhúng vector để tránh các ký tự mã hóa ngẫu nhiên (như `G01`, `G05`) làm sai lệch khoảng cách vector trong không gian ngữ nghĩa. Trường `id` được giữ lại chỉ nhằm mục đích đưa vào System Prompt để ép LLM trích dẫn minh bạch nguồn gốc thông tin `[Gxx]`.
    - `source`: Được giữ lại nhằm cung cấp xuất xứ tài liệu minh bạch trong prompt cho LLM và hiển thị nguồn kiểm chứng cho người dùng trên giao diện mở rộng (`st.expander`).
  - **Các chi tiết được lược bỏ (Omitted Details):** Lược bỏ các dữ liệu phi cấu trúc có giá trị thấp đối với việc hỏi đáp du lịch như tọa độ GPS kinh/vĩ độ, file ảnh thô, bình luận/đánh giá chủ quan từ khách tham quan, và lịch sử trùng tu dài dòng. Chỉ giữ lại đúng các thuộc tính sự thật cốt lõi hay bị chatbot bịa đặt (hallucination): địa chỉ cụ thể, khung giờ hoạt động, bảng giá vé phân tầng (người lớn / học sinh / trẻ em) và đặc điểm nổi bật.

---

### 2. Decomposition (Phân rã bài toán)

Hệ thống được chia tách thành **2 giai đoạn chính**: Quy trình lập chỉ mục một lần (One-Time Indexing) và Quy trình xử lý truy vấn thời gian thực (Runtime Query Pipeline) gồm chuỗi 6 bài toán con:

```
[Khởi tạo 1 lần (@st.cache_resource)]
knowledge_base.json (15 mục) → Nhúng vector → Indexed KB (Lưu cache trong RAM)

[Luồng xử lý truy vấn thời gian thực]
[Hộp 1: Đăng nhập (Sign-in)]
    ↓ (Phiên Firebase: UID, ID Token)
[Hộp 2: Nhúng câu hỏi (Embed User Query)]
    ↓ (Query Vector)
[Hộp 3: Truy xuất Top-K & Chấm điểm (Retrieve Top-K & Score)]
    ↓ (Top-K Chunks + Điểm Cosine Similarity)
[Hộp 4: Lọc & Xây dựng ngữ cảnh (Filter & Build Context)] ──(Điểm max < 0.25)──→ Trả về "I don't know..."
    ↓ (Grounded System Prompt)
[Hộp 5: Sinh câu trả lời qua Ollama LLM (Generate via LLM)]
    ↓ (Câu trả lời trích dẫn [Gxx], lọc sạch thẻ <think>)
[Hộp 6: Hiển thị & Lưu lịch sử phiên (Display & Session History)]
```

#### Chi tiết Đầu vào (In) và Đầu ra (Out) của từng hộp:

* **Hộp Khởi tạo (One-Time KB Indexing):** 
  - *In:* File `knowledge_base.json` (15 mục du lịch TP.HCM).
  - *Out:* Danh sách các cặp `(entry, entry_vector)` được lưu cố định trong RAM qua decorator `@st.cache_resource` của Streamlit, giúp ứng dụng không phải nhúng lại toàn bộ cẩm nang ở mỗi lượt chat.
* **Hộp 1 (Sign-in):** 
  - *In:* Email, Mật khẩu từ giao diện người dùng.
  - *Out:* Phiên làm việc Firebase (`uid`, `id_token`, `email`). Nếu chưa đăng nhập, cổng giao diện chat bị khóa hoàn toàn.
* **Hộp 2 (Embed User Query):** 
  - *In:* Chuỗi văn bản câu hỏi của người dùng (`query`).
  - *Out:* Vector biểu diễn ngữ nghĩa dày đặc 768 chiều (`query_vector`) được tạo bởi mô hình `embeddinggemma` trên Ollama.
* **Hộp 3 (Retrieve Top-K & Score):** 
  - *In:* `query_vector` + `Indexed KB` lấy từ bộ nhớ RAM.
  - *Out:* Danh sách 3 mục có điểm số tương đồng góc Cosine cao nhất kèm điểm số tương ứng.
* **Hộp 4 (Filter & Build Context):** 
  - *In:* Danh sách Top-K mục và điểm số.
  - *Out:* 
    - Nếu điểm cao nhất $\max(\text{score}) < 0.25$: Ngắt luồng sớm và trả về câu thông báo chuẩn: *"I don't know this information as it is not currently covered in the Lumen Travel guide."*
    - Nếu đạt ngưỡng: Đóng gói các đoạn văn bản trích xuất thành **Grounded System Prompt** với các ràng buộc nghiêm ngặt (câu hỏi `query` được truyền riêng sang Hộp 5).
* **Hộp 5 (Generate via LLM):** 
  - *In:* Grounded System Prompt + User Query gửi qua endpoint `/api/chat` tới mô hình `qwen3:4b` (`temperature = 0.1`).
  - *Out:* Chuỗi câu trả lời hoàn chỉnh, có trích dẫn mã `[Gxx]`, đã được bóc tách và lọc bỏ sạch các khối thẻ suy luận `<think>...</think>`.
* **Hộp 6 (Display & Session History):** 
  - *In:* Câu trả lời của LLM + Danh sách trích dẫn Top-K và điểm số.
  - *Out:* Render tin nhắn lên giao diện Streamlit, hiển thị thanh mở rộng `st.expander` chứa căn cứ tham chiếu, và cập nhật vào `st.session_state["chat_history"]`.

---

### 3. Pattern Recognition (Nhận dạng mẫu)

#### 3.1. Kế thừa kiến thức và mẫu thiết kế từ Lab 3 và Lab 4:
* **Tái sử dụng từ Lab 3 (`firebase_client.py` & `app.py`):**
  - Cơ chế gọi REST API phía client trực tiếp đến Google Identity Toolkit (`identitytoolkit.googleapis.com`) cho 2 tác vụ `signUp` và `signInWithPassword`.
  - Mẫu bao bọc xử lý ngoại lệ `FirebaseError`, ánh xạ các mã lỗi kỹ thuật (như `EMAIL_EXISTS`, `INVALID_LOGIN_CREDENTIALS`) thành thông báo tiếng Anh thân thiện.
  - Cơ chế bảo vệ định tuyến (route gating) bằng session state: `if "user" not in st.session_state: render_auth_page() else: render_chat_page()`.
  - Mẫu làm sạch phiên làm việc trong hàm `forget_user()`: xóa bỏ hoàn toàn `user` và `chat_history` khi người dùng bấm Sign Out, đảm bảo không lưu trái phép dữ liệu vào Firestore.
* **Tái sử dụng từ Lab 4 (`ollama_pinggy.ipynb` & `rag.py`):**
  - Quy trình 4 bước dựng máy chủ Ollama trên Google Colab với GPU T4 kết hợp mở đường hầm bảo mật Pinggy SSH để cung cấp public HTTPS URL.
  - Tích hợp chuẩn các endpoint của Ollama: `/api/embed` (với `embeddinggemma`) và `/api/chat` (với `qwen3:4b`).
  - Quy tắc chuẩn hóa vector độ dài đơn vị $L_2$ (`arr / np.linalg.norm(arr)`) và công thức tính độ tương đồng góc Cosine.

#### 3.2. Mẫu kiến trúc cốt lõi: Filter $\rightarrow$ Score $\rightarrow$ Top-K:
* **Trong bài hiện tại (Assignment 3 - Sign-in RAG Chat):**
  - **Filter (Lọc):** Giới hạn không gian tìm kiếm trong phạm vi 15 địa điểm đã kiểm duyệt của TP.HCM (`knowledge_base.json`), kết hợp bộ lọc ngưỡng hậu kiểm ($\max(\text{score}) \ge 0.25$) để loại bỏ các câu hỏi hoàn toàn lạc đề.
  - **Score (Chấm điểm):** Chấm điểm từng cặp vector giữa câu hỏi và cẩm nang bằng hàm $\text{CosineSimilarity}(\mathbf{q}, \mathbf{e}_i)$.
  - **Top-K (Lấy phần tử cao nhất):** Sắp xếp danh sách điểm theo thứ tự giảm dần và cắt lấy $K = 3$ mục đầu tiên (`scored_items[:top_k]`).
* **Sẽ tái xuất hiện trong bài tiếp theo (Assignment 4 — RAG-Rec):**
  - **Filter (Lọc):** Lọc trước dữ liệu (metadata pre-filtering) dựa trên các ràng buộc và sở thích của người dùng (khớp trường `category` như `"museum"`, `"street_food"` và `tags` như `"district_1"`, `"budget"`).
  - **Score (Chấm điểm):** Chấm điểm kết hợp (hybrid scoring) giữa độ tương đồng ngữ nghĩa Cosine Similarity và mức độ trùng khớp các tags người dùng quan tâm.
  - **Top-K (Lấy phần tử cao nhất):** Chọn ra $K$ địa điểm tối ưu nhất để đưa vào LLM sinh lịch trình và lời khuyên du lịch cá nhân hóa.

---

### 4. Algorithm Design (Thiết kế thuật toán)

#### 4.1. Mã giả (Pseudocode) cho quy trình trả lời một câu hỏi:

```text
Thuật toán: AnswerTravelQuery(query, indexed_kb, top_k, similarity_threshold)
    Đầu vào: 
        - query: chuỗi câu hỏi của người dùng
        - indexed_kb: danh sách các cặp (entry, entry_vector) đã lưu trong cache
        - top_k: số lượng tài liệu trích xuất tối đa (mặc định = 3)
        - similarity_threshold: ngưỡng tương đồng tối thiểu (mặc định = 0.25)
    Đầu ra: 
        - answer: câu trả lời hoàn chỉnh
        - top_entries: danh sách các mục trích xuất kèm điểm số

    1. query_vector <- GetEmbedding(query, model="embeddinggemma")
    2. scored_list <- []
    3. VỚI MỖI (entry, entry_vector) TRONG indexed_kb THỰC HIỆN:
           score <- CosineSimilarity(query_vector, entry_vector)
           Thêm (entry, score) VÀO scored_list
       HẾT VÒNG LẶP
    4. Sắp xếp scored_list theo score GIẢM DẦN
    5. top_entries <- scored_list[0 : top_k]
    6. NẾU top_entries[0].score < similarity_threshold THÌ:
           TRẢ VỀ "I don't know this information as it is not currently covered in the Lumen Travel guide.", top_entries
       HẾT NẾU
    7. prompt <- ConstructSystemPrompt(top_entries)
    8. raw_answer <- OllamaChat(model="qwen3:4b", prompt, query)
    9. answer <- StripThinkBlocks(raw_answer)
   10. TRẢ VỀ answer, top_entries
```

*Độ phức tạp thuật toán:* 
- Bước nhúng câu hỏi: $O(L)$ với $L$ là độ dài câu hỏi.
- Bước tính độ tương đồng: $O(N \cdot D)$ với $N = 15$ (số mục cẩm nang) và $D = 768$ (số chiều vector). Vì $N$ nhỏ nên thời gian tìm kiếm ở bước này là tức thì ($< 5\text{ ms}$).

---

#### 4.2. Hai quyết định thiết kế then chốt kèm ví dụ thực tế:

1. **Quyết định lựa chọn $K = 3$ với ví dụ thực tế:**
   - *Cơ sở thiết kế:* Mỗi mục trong cẩm nang có độ dài từ 50–90 từ chứa rất nhiều thông tin chi tiết (địa chỉ, giá vé từng nhóm tuổi, giờ mở/đóng cửa). Việc thiết lập $K = 3$ cung cấp vừa đủ ngữ cảnh cần thiết cho mô hình suy luận mà không làm tràn hay loãng prompt (prompt dilution), đồng thời giữ tốc độ phản hồi qua đường hầm Pinggy ở mức tối ưu.
   - *Ví dụ thực tế:* Ở Câu kiểm thử số 3 (*"During which hours on weekends is Bui Vien Walking Street closed to vehicles?"*), việc lấy $K=3$ cho phép hệ thống trích xuất đồng thời cả mục Phố đi bộ Bùi Viện `[G11]` và mục Phố đi bộ Nguyễn Huệ `[G06]`. Nhờ có đầy đủ ngữ cảnh của cả 2 phố đi bộ trong prompt, mô hình `qwen3:4b` dễ dàng đối chiếu và phân biệt chính xác giờ cấm xe của Bùi Viện (`7:00 PM - 2:00 AM` tối Thứ 6, Thứ 7, Chủ Nhật) với giờ cấm xe của Nguyễn Huệ (`6:00 PM - 11:00 PM` tối Thứ 7, Chủ Nhật) mà không bị nhầm lẫn.

2. **Quy tắc "I don't know" 2 tầng phòng ngự với ví dụ thực tế:**
   - *Cơ sở thiết kế:* Nhằm triệt tiêu hoàn toàn rủi ro bịa đặt thông tin (hallucination) thường gặp ở các chatbot thông thường, hệ thống áp dụng cơ chế bảo vệ 2 tầng:
     - **Tầng 1 (Ngưỡng số học tại Python):** Kiểm tra xem điểm tương đồng cao nhất $\max(\text{score}) < 0.25$ hay không. Nếu câu hỏi hoàn toàn lạc đề (ví dụ: hỏi về Bà Nà Hills ở Đà Nẵng), điểm tương đồng cao nhất chỉ đạt $\sim 0.18$, hệ thống ngắt ngay lập tức mà không gửi request sang LLM, tiết kiệm tài nguyên GPU.
     - **Tầng 2 (Ràng buộc mô hình tại Prompt & Tham số):** Ép System Prompt với luật số 3 nghiêm ngặt kết hợp nhiệt độ thấp `temperature = 0.1` để mô hình suy luận tất định.
   - *Ví dụ thực tế:* Ở Câu kiểm thử số 6 (*"What time does Truong Dinh Goat Hotpot restaurant close?"*), do câu hỏi có chứa các từ khóa về ẩm thực/nhà hàng nên điểm Cosine Similarity với các mục đồ ăn như `[G13]` (Hẻm 200 Xóm Chiếu) và `[G15]` (Chợ Hồ Thi Kỷ) vẫn đạt $\sim 0.35$ (lọt qua Tầng 1). Tuy nhiên, khi đi vào Tầng 2, mô hình kiểm tra 3 đoạn văn bản nhận được không hề nhắc đến quán Lẩu dê Trương Định nên đã nghiêm túc tuân thủ luật và từ chối trả lời theo đúng câu mẫu quy định, bảo toàn 100% tính xác thực (groundedness).
