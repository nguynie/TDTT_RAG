# KỊCH BẢN & HƯỚNG DẪN QUAY VIDEO DEMO (TỔNG THỜI LƯỢNG: 5:00)

Tài liệu này hướng dẫn chi tiết từng **thao tác bấm trên màn hình** và **lời thoại (script)** tương ứng cho toàn bộ video nộp bài theo đúng yêu cầu đề bài `Assignment03_Auth_RAG_Chat.pdf`.

---

## 1. Chuẩn bị trước khi bấm quay (Pre-recording Checklist)

1. **Chuẩn bị các cửa sổ trên màn hình:**
   - **Tab trình duyệt 1 (Google Colab):** Mở sẵn notebook `ollama_pinggy.ipynb` đã chạy xong tất cả các cell, cuộn sẵn đến cell cuối cùng đang hiển thị thông báo server Ollama sẵn sàng và đường link `Pinggy URL` (dạng `https://xxxxx.free.pinggy.net`).
   - **Cửa sổ VS Code (hoặc Text Editor):** Mở sẵn file `.env` chứa dòng `OLLAMA_BASE_URL=https://xxxxx.free.pinggy.net` (khớp với link Colab).
   - **Cửa sổ Terminal:** Mở sẵn terminal ở thư mục dự án `TDTT_RAG`, đã gõ sẵn lệnh `streamlit run app.py` (chỉ chờ nhấn Enter).
   - **File Notepad:** Chứa sẵn 2 câu hỏi test để copy/paste nhanh:
     - **Câu 1 (Trong cẩm nang):**
       ```text
       What is the adult admission ticket price for Independence Palace?
       ```
     - **Câu 2 (Ngoài cẩm nang):**
       ```text
       How much is the entrance ticket to Sun World Ba Na Hills?
       ```
2. **Chuẩn bị tài khoản đăng nhập:**
   - Đã có sẵn 1 tài khoản đã đăng ký trước (ví dụ: `test@example.com` / `123456`) để đăng nhập ngay mà không mất thời gian tạo mới.
3. **Mẹo hiển thị:** Phóng to trình duyệt Streamlit lên **115% - 125%** (`Ctrl + +`) để chữ và điểm số hiển thị rõ nét trên video.

---

## 2. Kịch bản chi tiết phần Demo (~1 phút 40 giây: 0:00 – 1:40)

| Thời gian | Cảnh & Thao tác trên màn hình | Lời thoại thuyết minh (Script đọc) | Ý nghĩa kỹ thuật |
| :--- | :--- | :--- | :--- |
| **0:00 - 0:10** | **Cảnh 1: Show Colab đang chạy**<br>- Màn hình quay tab Colab.<br>- Chuột lướt qua cell Ollama và cell Pinggy đang có link public. | *"Xin chào thầy cô, đây là bài tập lớn môn Tư duy tính toán. Đầu tiên, máy chủ Ollama chạy hai mô hình `embeddinggemma` và `qwen3:4b` đã được em khởi động sẵn trên Google Colab và mở đường hầm công khai qua Pinggy."* | Minh chứng dùng Ollama + Pinggy từ Lab 4. |
| **0:10 - 0:18** | **Cảnh 2: Show file `.env`**<br>- Chuyển sang màn hình VS Code.<br>- Rê chuột vào dòng `OLLAMA_BASE_URL` trong file `.env`. | *"Đường link Pinggy này cùng các khóa Firebase API đã được em cấu hình an toàn trong file `.env` chứ không hardcode trong mã nguồn."* | Minh chứng lưu URL và key trong `.env`. |
| **0:18 - 0:28** | **Cảnh 3: Gõ lệnh Streamlit**<br>- Chuyển sang Terminal.<br>- Nhấn Enter chạy lệnh `streamlit run app.py`.<br>- Trình duyệt tự mở trang web `localhost:8501`. | *"Bây giờ em tiến hành khởi chạy ứng dụng bằng lệnh `streamlit run app.py`."* | Minh chứng cách chạy ứng dụng đúng yêu cầu đề. |
| **0:28 - 0:45** | **Cảnh 4: Đăng nhập Firebase**<br>- Trình duyệt ở trang **Account Sign In**.<br>- Nhập email & mật khẩu $\rightarrow$ Bấm nút **Sign In**.<br>- Vào giao diện Chat, sidebar hiện Email và UID. | *"Giao diện chat được bảo vệ hoàn toàn bởi Firebase Authentication, chưa đăng nhập thì không thể truy cập. Em tiến hành đăng nhập bằng tài khoản email. Sau khi đăng nhập thành công, phiên làm việc được lưu trong `st.session_state`."* | Minh chứng tính năng đăng nhập & bảo vệ route. |
| **0:45 - 1:15** | **Cảnh 5: Hỏi câu trong cẩm nang (Answerable)**<br>- Dán **Câu hỏi 1** vào ô chat $\rightarrow$ Nhấn Enter.<br>- Câu trả lời hiện ra có trích dẫn `[G01]`.<br>- **Bấm mở thanh Expander** xem 3 mục Top-K và điểm Cosine. | *"Bây giờ em hỏi một câu có trong cẩm nang: 'What is the adult admission ticket price for Independence Palace?'. Hệ thống nhúng câu hỏi bằng `embeddinggemma`, tìm kiếm theo Cosine Similarity và mô hình `qwen3:4b` trả lời chính xác giá vé 40,000 VND có trích dẫn nguồn [G01]. Mở bảng tham chiếu Top-K, ta thấy mục Dinh Độc Lập [G01] đạt điểm cao nhất."* | Minh chứng RAG: Embed $\rightarrow$ Cosine $\rightarrow$ Top-K $\rightarrow$ Trích dẫn `[Gxx]`. |
| **1:15 - 1:30** | **Cảnh 6: Hỏi câu ngoài cẩm nang ("I don't know")**<br>- Thu expander lại $\rightarrow$ Dán **Câu hỏi 2** $\rightarrow$ Enter.<br>- Chờ câu trả lời: *"I don't know this information as it is not currently covered in the Lumen Travel guide."* | *"Tiếp theo, em hỏi một câu ngoài cẩm nang TP.HCM: 'How much is the entrance ticket to Sun World Ba Na Hills?'. Trợ lý không hề bịa đặt giá vé mà tuân thủ nghiêm ngặt quy tắc 'I don't know', từ chối trả lời vì thông tin không có trong cẩm nang."* | Minh chứng cơ chế chống ảo giác "I don't know". |
| **1:30 - 1:40** | **Cảnh 7: Đăng xuất (Sign out)**<br>- Rê chuột sang thanh Sidebar bên trái.<br>- Nhấp vào nút **Sign Out** $\rightarrow$ Màn hình quay về form đăng nhập. | *"Cuối cùng, em nhấn nút 'Sign Out'. Hàm `forget_user()` lập tức xóa sạch toàn bộ lịch sử trò chuyện và thông tin phiên trong `session_state`, đưa người dùng về lại màn hình đăng nhập. Phần demo tính năng của em đã hoàn thành."* | Minh chứng dọn dẹp sạch phiên và chat history. |

---

## 3. Lời thoại liền mạch phần Demo (Dành cho bạn luyện đọc)

> *"Xin chào thầy cô, đây là bài thực hành số 3 môn Tư duy tính toán: Xây dựng trợ lý du lịch TP.HCM với RAG Chat.
>
> *(Cảnh 1: Chiếu tab Colab)*  
> *Đầu tiên, máy chủ Ollama chạy hai mô hình `embeddinggemma` và `qwen3:4b` đã được em khởi động sẵn trên Google Colab và mở đường hầm công khai thông qua Pinggy.*
>
> *(Cảnh 2: Chiếu file `.env`)*  
> *Đường link Pinggy này cùng các khóa Firebase API đã được em lưu trữ an toàn trong file `.env` chứ không hardcode trong mã nguồn.*
>
> *(Cảnh 3: Gõ lệnh terminal)*  
> *Bây giờ em khởi chạy ứng dụng bằng lệnh `streamlit run app.py`.*
>
> *(Cảnh 4: Màn hình Sign In $\rightarrow$ Đăng nhập)*  
> *Giao diện chat được bảo vệ hoàn toàn bởi Firebase Authentication, người dùng bắt buộc phải đăng nhập thì mới có thể truy cập. Em tiến hành đăng nhập bằng tài khoản email. Sau khi đăng nhập thành công, phiên làm việc được lưu trong `st.session_state`.*
>
> *(Cảnh 5: Dán câu hỏi 1 $\rightarrow$ Enter $\rightarrow$ Mở Expander)*  
> *Bây giờ em sẽ hỏi một câu có trong cẩm nang du lịch: 'What is the adult admission ticket price for Independence Palace?'. Hệ thống nhúng câu hỏi qua mô hình `embeddinggemma`, tìm kiếm bằng độ đo Cosine Similarity và mô hình `qwen3:4b` trả lời chính xác giá vé 40,000 VND kèm trích dẫn mã nguồn [G01]. Mở bảng tham chiếu Top-K, ta thấy rõ các đoạn văn bản trích xuất kèm điểm số tương đồng cụ thể.*
>
> *(Cảnh 6: Dán câu hỏi 2 $\rightarrow$ Enter)*  
> *Tiếp theo, em hỏi câu thứ hai về địa điểm không có trong cẩm nang: 'How much is the entrance ticket to Sun World Ba Na Hills?'. Nhờ cơ chế kiểm soát 2 tầng, trợ lý không hề bịa đặt mà từ chối theo đúng quy tắc: 'I don't know this information as it is not currently covered in the Lumen Travel guide.'*
>
> *(Cảnh 7: Bấm nút Sign Out)*  
> *Cuối cùng, em bấm nút 'Sign Out' ở thanh bên. Ứng dụng lập tức làm sạch toàn bộ lịch sử trò chuyện và phiên đăng nhập trong `st.session_state` mà không lưu vào Firestore, sau đó đưa người dùng quay lại màn hình đăng nhập. Phần demo tính năng của em đã hoàn tất."*

---

## 4. Những lưu ý quan trọng khi quay phần Demo

1. **Thao tác lướt nhanh ở Cảnh 1 và Cảnh 2:** Chỉ cần lướt qua tab Colab (~8 giây) và file `.env` (~5 giây) để chứng minh kiến trúc Lab 4 và tính bảo mật, không cần dừng lại giải thích sâu để tránh mất thời gian.
2. **Bắt buộc phải mở Expander nguồn trích dẫn:** Khi có kết quả câu hỏi 1, hãy mở expander trong khoảng 3–5 giây để video ghi lại điểm số Cosine và mã `[G01]`.
3. **Dùng phím tắt:** Dùng `Alt + Tab` để chuyển màn hình giữa Colab $\rightarrow$ VS Code $\rightarrow$ Terminal $\rightarrow$ Trình duyệt một cách mượt mà và chuyên nghiệp.

---

## 5. KỊCH BẢN PHẦN TEST RESULTS (KẾT QUẢ KIỂM THỬ: ~1 PHÚT)

Mục 5 trong đề bài yêu cầu: *"Test results (about 1 min): one success, one failure and the step where it failed."*  
Phần này bạn cần trình bày **1 ca thành công (Success)**, **1 ca thất bại (Failure)** và giải thích rõ **nó đã thất bại ở bước nào** (missing data, retrieval hay generation).

### 5.1. Hai câu hỏi test đã chuẩn bị sẵn
Copy sẵn 2 câu này vào Notepad để dán nhanh vào app:

1. **Ca thành công (Success - Test Case 4 - Paraphrase):**
   ```text
   Where can I take a boat trip to watch the sunset on the river in Saigon and how much does it cost?
   ```
   - **Kỳ vọng:** Trích xuất đúng `[G14]` (Saigon Waterbus & Bến Bạch Đằng).
   - **Kết quả:** **Pass**. Trả lời đúng vé 15,000 VND một chiều, ngắm hoàng hôn, trích dẫn `[G14]`.

2. **Ca thất bại (Failure - Test Case 7 - Multi-entry Aggregation):**
   ```text
   List all attractions in District 1 that offer free entrance or free exterior visiting, and state their opening hours.
   ```
   - **Kỳ vọng:** Phải liệt kê đủ cả **5 địa điểm** miễn phí ở Quận 1: `[G03]` (Nhà thờ Đức Bà), `[G04]` (Bưu điện TP), `[G06]` (Phố đi bộ Nguyễn Huệ), `[G07]` (Thảo Cầm Viên cho trẻ < 1m), `[G11]` (Phố đi bộ Bùi Viện).
   - **Kết quả thực tế:** **Fail**. Do $K=3$, bước truy xuất chỉ lấy 3 mục (`[G07]`, `[G11]`, `[G06]`), bỏ sót hoàn toàn `[G03]` (Nhà thờ Đức Bà) và `[G04]` (Bưu điện TP).
   - **Bước thất bại (Failed Step):** **Failed at Retrieval Step** do giới hạn `TOP_K = 3`.

---

### 5.2. Kịch bản chi tiết từng giây (0:00 - 1:00)

| Thời gian | Thao tác trên màn hình | Lời thoại thuyết minh (Script đọc) |
| :--- | :--- | :--- |
| **0:00 - 0:25** | - Đang ở giao diện Chat (sau khi đăng nhập).<br>- Dán câu hỏi test thành công (Câu 4) $\rightarrow$ Nhấn Enter.<br>- Chờ câu trả lời hiện ra và mở expander trích dẫn `[G14]`. | *"Tiếp theo là phần báo cáo kết quả kiểm thử. Đầu tiên là một ca thành công (Success case) với câu hỏi diễn đạt gián tiếp (Paraphrase): 'Where can I take a boat trip to watch the sunset on the river in Saigon and how much does it cost?'. Hệ thống tìm kiếm ngữ nghĩa rất tốt, trích xuất chính xác mục [G14] Saigon Waterbus tại bến Bạch Đằng và trả lời đúng giá vé 15,000 VND."* |
| **0:25 - 0:50** | - Dán câu hỏi test thất bại (Câu 7) $\rightarrow$ Nhấn Enter.<br>- Khi câu trả lời hiện ra, mở expander chỉ vào 3 mục được lấy lên (`[G07]`, `[G11]`, `[G06]`). | *"Tiếp theo là một ca thất bại thực tế (Failure case) với câu hỏi tổng hợp nhiều địa điểm: 'List all attractions in District 1 that offer free entrance or free exterior visiting, and state their opening hours.'. Trong cẩm nang có tới 5 địa điểm miễn phí ở Quận 1, nhưng do K=3, hệ thống chỉ lấy được 3 mục G07, G11 và G06, làm bỏ sót hoàn toàn Nhà thờ Đức Bà G03 và Bưu điện Thành phố G04."* |
| **0:50 - 1:00** | - Dùng chuột chỉ vào bảng điểm Top-K trong expander (hoặc chuyển màn hình sang bảng Test Table trong README). | *"Hệ thống thất bại ở bước Truy xuất dữ liệu (Retrieval Step) do giới hạn TOP_K = 3. Dữ liệu trong cẩm nang có đủ (không thiếu data), mô hình qwen3:4b tổng hợp rất chính xác từ dữ liệu nhận được (không bị ảo giác), nhưng câu trả lời bị thiếu là do nút thắt cổ chai ở bước Retrieval."* |

---

### 5.3. Lời thoại liền mạch (Dành cho bạn luyện đọc)

> *"Tiếp theo là phần báo cáo kết quả kiểm thử. Trong quá trình đánh giá hệ thống với bảng kiểm thử gồm 7 trường hợp, em xin trình bày 1 ca thành công và 1 ca thất bại:
>
> *(Thao tác: Dán câu hỏi 4 và gửi)*
>
> *Đầu tiên là một ca thành công với câu hỏi diễn đạt ngữ nghĩa (Paraphrase): 'Where can I take a boat trip to watch the sunset on the river in Saigon and how much does it cost?'. Dù người dùng không nhắc trực tiếp tên địa danh, hệ thống vẫn nhúng ngữ nghĩa chính xác và trích xuất đúng mục [G14] Saigon Waterbus, trả lời trọn vẹn giá vé 15,000 VND một chiều có trích dẫn nguồn.*
>
> *(Thao tác: Dán câu hỏi 7 và gửi)*
>
> *Tiếp theo là một ca thất bại thực tế với câu hỏi tổng hợp: 'List all attractions in District 1 that offer free entrance or free exterior visiting, and state their opening hours.'. Trong cẩm nang có tới 5 địa điểm ở Quận 1 mở cửa miễn phí, nhưng do TOP_K = 3 nên hệ thống chỉ lấy được 3 mục là G07, G11 và G06, làm bỏ sót hoàn toàn Nhà thờ Đức Bà G03 và Bưu điện Thành phố G04.*
>
> *(Thao tác: Mở expander chỉ vào 3 mục Top-K)*
>
> *Phân tích nguyên nhân: Hệ thống thất bại trực tiếp ở bước Truy xuất (Retrieval Step). Cẩm nang có đầy đủ thông tin, mô hình LLM cũng tổng hợp rất chuẩn xác không bịa đặt, nhưng câu trả lời bị thiếu là do nút thắt cổ chai TOP_K = 3 chỉ lấy được 3 tài liệu liên quan nhất đưa vào prompt."*

---

## 6. KỊCH BẢN PHẦN COMPUTATIONAL THINKING ANALYSIS (~2.5 PHÚT)

Mục 5 trong đề bài yêu cầu: *"Computational Thinking analysis (about 2.5 min). Explain your own solution, not general definitions."*  
Phần này bạn trình bày trên **Slide** hoặc cuộn màn hình chiếu trực tiếp **Mục 4 trong file README.md**, nói tập trung vào giải pháp kỹ thuật cụ thể của bài làm, tuyệt đối không đọc lại định nghĩa lý thuyết.

### 6.1. Phân bổ thời gian (2.5 phút = 150 giây)

- **1. Abstraction (~35 giây):** Input/Output và cách mô hình hóa dữ liệu cẩm nang.
- **2. Decomposition (~45 giây):** 2 giai đoạn xử lý và luồng 6 hộp con.
- **3. Pattern Recognition (~35 giây):** Kế thừa Labs 3-4 và mẫu Filter $\rightarrow$ Score $\rightarrow$ Top-K.
- **4. Algorithm Design (~35 giây):** Mã giả và 2 quyết định thiết kế kèm ví dụ thực tế.

---

### 6.2. Kịch bản chi tiết từng bước & Lời thoại thuyết minh

#### Bước 1: Abstraction (Trừu tượng hóa - ~35 giây)
* **Thao tác trên màn hình:** Chiếu phần **4.1. Abstraction** trong README.md hoặc Slide mô tả cấu trúc dữ liệu `knowledge_base.json`.
* **Lời thoại:**
  > *"Sang phần Tư duy tính toán (Computational Thinking), bước đầu tiên là Abstraction.  
  > - **Input của hệ thống:** Câu hỏi tự nhiên từ người dùng đã đăng nhập.  
  > - **Output:** Câu trả lời kèm mã trích dẫn [Gxx] và bảng tham chiếu Top-K kèm điểm Cosine Similarity.  
  > - **Về dữ liệu:** Mỗi mục trong `knowledge_base.json` được tinh gọn gồm 6 trường: `id`, `title`, `category`, `tags`, `text` và `source`.  
  > Em gộp `title`, `category`, `text`, `tags` để tạo vector ngữ nghĩa toàn diện. Riêng trường `id` được cố tình loại khỏi vector để tránh các ký tự vô nghĩa như G01 làm sai lệch khoảng cách ngữ nghĩa, mà chỉ đưa vào prompt để trích dẫn. Các chi tiết rườm rà như tọa độ GPS, hình ảnh hay review chủ quan được lược bỏ, chỉ giữ lại các thuộc tính cốt lõi dễ bị chatbot bịa đặt: địa chỉ, giờ mở cửa và giá vé cụ thể."*

---

#### Bước 2: Decomposition (Phân rã bài toán - ~45 giây)
* **Thao tác trên màn hình:** Chiếu sơ đồ luồng dữ liệu (Runtime Pipeline diagram trong README).
* **Lời thoại:**
  > *"Bước thứ hai là Decomposition. Bài toán được phân rã thành 2 giai đoạn:  
  > - **Giai đoạn khởi tạo 1 lần:** Toàn bộ 15 mục cẩm nang được nhúng thành vector và lưu trong RAM nhờ `@st.cache_resource`, không phải nhúng lại mỗi lượt chat.  
  > - **Giai đoạn runtime gồm 6 bài toán con:**  
  >   1. **Sign-in:** Nhận Email/Password $\rightarrow$ Trả về Firebase session.  
  >   2. **Embed Query:** Nhận câu hỏi $\rightarrow$ Trả về Query Vector qua `embeddinggemma`.  
  >   3. **Retrieve & Score:** Tính Cosine Similarity giữa câu hỏi và cẩm nang trong RAM $\rightarrow$ Trả về Top 3 mục điểm cao nhất.  
  >   4. **Filter & Build Context:** Kiểm tra nếu điểm cao nhất $< 0.25$ thì trả ngay 'I don't know'; nếu đạt thì đóng gói vào Grounded System Prompt.  
  >   5. **Generate:** Gửi Prompt và câu hỏi tới `qwen3:4b` $\rightarrow$ Trả về câu trả lời có trích dẫn, lọc sạch thẻ suy luận think.  
  >   6. **Display & Session:** Hiển thị kết quả ra giao diện chat và expander, lưu lịch sử vào `st.session_state`."*

---

#### Bước 3: Pattern Recognition (Nhận dạng mẫu - ~35 giây)
* **Thao tác trên màn hình:** Chiếu phần **4.3. Pattern Recognition** trong README.
* **Lời thoại:**
  > *"Bước thứ ba là Pattern Recognition.  
  > - **Kế thừa từ Lab 3:** Em tái sử dụng cơ chế xác thực REST API với Firebase Auth, ánh xạ mã lỗi thân thiện, bảo vệ giao diện bằng session_state và hàm `forget_user()` dọn sạch phiên làm việc khi Sign Out.  
  > - **Kế thừa từ Lab 4:** Quy trình dựng Ollama server trên Google Colab với đường hầm Pinggy, các endpoint `/api/embed`, `/api/chat` và công thức Cosine Similarity chuẩn hóa $L_2$.  
  > - **Mẫu cốt lõi Filter $\rightarrow$ Score $\rightarrow$ Top-K:**  
  >   + Trong bài 3: **Filter** không gian 15 địa điểm TP.HCM và lọc ngưỡng hậu kiểm điểm $\ge 0.25$; **Score** bằng Cosine Similarity; **Top-K** cắt lấy 3 tài liệu cao nhất.  
  >   + Mẫu này sẽ tái xuất hiện ở Assignment 4 (RAG-Rec): **Filter** theo danh mục và tags người dùng yêu thích $\rightarrow$ **Score** kết hợp ngữ nghĩa và số tags trùng khớp $\rightarrow$ **Top-K** chọn các địa điểm tối ưu để gợi ý lịch trình."*

---

#### Bước 4: Algorithm Design (Thiết kế thuật toán - ~35 giây)
* **Thao tác trên màn hình:** Chiếu đoạn mã giả (Pseudocode) và 2 ví dụ thực tế trong README.
* **Lời thoại:**
  > *"Cuối cùng là Algorithm Design.  
  > Quy trình trả lời câu hỏi được chuẩn hóa qua thuật toán `AnswerTravelQuery` với độ phức tạp tìm kiếm tuyến tính $O(N \cdot D)$.  
  > Em đưa ra 2 quyết định thiết kế then chốt:  
  > 1. **Chọn $K = 3$:** Đủ ngữ cảnh mà không làm loãng prompt. Ví dụ ở câu hỏi về phố đi bộ Bùi Viện, $K = 3$ lấy được cả mục Bùi Viện [G11] và Nguyễn Huệ [G06], giúp mô hình phân biệt rõ giờ cấm xe của hai nơi mà không bị nhầm lẫn.  
  > 2. **Quy tắc 'I don't know' 2 tầng:** Tầng 1 chặn bằng ngưỡng điểm 0.25. Tầng 2 kiểm soát bằng System Prompt và temperature thấp (0.1). Ví dụ khi hỏi về quán lẩu dê Trương Định, từ khóa ăn uống làm điểm vượt qua Tầng 1, nhưng khi vào Tầng 2, mô hình kiểm tra 3 đoạn trích xuất không thấy quán này nên từ chối trả lời chính xác, triệt tiêu hoàn toàn hiện tượng ảo giác."*

---

## 7. TỔNG KẾT PHÂN BỔ THỜI GIAN VIDEO (CHUẨN 5:00)

| Phần | Nội dung chính | Thời lượng chuẩn | Giới hạn mốc video |
| :---: | :--- | :---: | :---: |
| **Phần 1** | **Live Demo:** Show Colab đang chạy $\rightarrow$ Show link Pinggy trong `.env` $\rightarrow$ Gõ `streamlit run app.py` $\rightarrow$ Đăng nhập $\rightarrow$ Hỏi câu trong cẩm nang (mở expander) $\rightarrow$ Hỏi câu ngoài cẩm nang (show "I don't know") $\rightarrow$ Đăng xuất. | ~1 phút 40 giây | **0:00 – 1:40** |
| **Phần 2** | **Computational Thinking:** Thuyết minh 4 bước Abstraction $\rightarrow$ Decomposition $\rightarrow$ Pattern Recognition $\rightarrow$ Algorithm Design (bám sát file README). | ~2 phút 20 giây | **1:40 – 4:00** |
| **Phần 3** | **Test Results:** Báo cáo 1 ca Pass (Câu 4 Paraphrase) và 1 ca Fail (Câu 7 Multi-entry) phân tích lỗi ở Retrieval Step do $K=3$. | ~1 phút 00 giây | **4:00 – 5:00** |
| **TỔNG** | **Toàn bộ video (Tuyệt đối không để vượt quá 5 phút)** | **5 phút 00 giây** | **Tối đa 5:00** |


