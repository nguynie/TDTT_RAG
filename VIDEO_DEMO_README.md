# KỊCH BẢN & HƯỚNG DẪN QUAY VIDEO DEMO (PHẦN DEMO: ~1.5 PHÚT)

Tài liệu này hướng dẫn chi tiết từng **thao tác bấm trên màn hình** và **lời thoại (script)** tương ứng cho phần **Demo chức năng** (Mục 5 trong đề bài: *"Demo about 1.5 min: sign in, ask one answerable question (show the sources), ask one question not in the guide, then sign out"*).

---

## 1. Chuẩn bị trước khi bấm quay (Pre-recording Checklist)

1. **Khởi động server & app:**
   - Đảm bảo máy chủ Ollama + Pinggy đang chạy và URL trong file `.env` còn hiệu lực.
   - Chạy Streamlit: `streamlit run app.py`.
   - Mở trình duyệt tại `http://localhost:8501`.
   - **Mẹo giao diện:** Nhấn `Ctrl` + `+` (hoặc `Cmd` + `+`) để phóng to trình duyệt lên **110% - 125%** giúp chữ, điểm số và mã trích dẫn hiển thị rõ ràng trên video.
2. **Chuẩn bị tài khoản & câu hỏi mẫu:**
   - Dùng 1 tài khoản đã đăng ký trước (ví dụ: `test@example.com` / `123456`) để đăng nhập ngay mà không mất thời gian tạo mới.
   - Mở sẵn 1 file Notepad chứa sẵn 2 câu hỏi test để **Copy - Paste**, tránh việc gõ phím chậm làm video vượt quá thời gian 1.5 phút:
     - **Câu 1 (Có trong cẩm nang):**
       ```text
       What is the adult admission ticket price for Independence Palace?
       ```
     - **Câu 2 (Không có trong cẩm nang):**
       ```text
       How much is the entrance ticket to Sun World Ba Na Hills?
       ```

---

## 2. Kịch bản chi tiết từng giây (0:00 - 1:30)

| Thời gian | Thao tác trên màn hình | Lời thoại thuyết minh (Script đọc) | Điểm số cần nhấn mạnh |
| :--- | :--- | :--- | :--- |
| **0:00 - 0:15** | - Màn hình đang ở trang **Account Sign In**.<br>- Nhập email & mật khẩu.<br>- Bấm nút **Sign In**. | *"Xin chào thầy cô, đây là ứng dụng Lumen Travel Assistant cho TP.HCM. Đầu tiên, tính năng chat được bảo vệ hoàn toàn bằng Firebase Authentication. Người dùng bắt buộc phải đăng nhập thì mới vào được hệ thống. Em sẽ tiến hành đăng nhập bằng tài khoản email và mật khẩu."* | Cho thấy cơ chế chặn truy cập chưa đăng nhập. |
| **0:15 - 0:45** | - Đăng nhập thành công, màn hình chuyển sang trang Chat.<br>- Thanh sidebar hiển thị Email và UID.<br>- Dán **Câu hỏi 1** vào ô chat $\rightarrow$ Nhấn Enter. | *"Sau khi đăng nhập thành công, phiên làm việc được lưu trong `st.session_state`. Bây giờ em sẽ hỏi một câu có trong cẩm nang du lịch: 'What is the adult admission ticket price for Independence Palace?' (Giá vé người lớn tham quan Dinh Độc Lập là bao nhiêu?)."* | Câu hỏi hợp lệ (Answerable query). |
| **0:45 - 1:05** | - Câu trả lời hiện ra.<br>- Dùng chuột rê vào mã trích dẫn `[G01]`.<br>- Bấm mở mục **Retrieved Travel Guide References & Scores (Top-K)** để xem 3 mục và điểm cosine similarity. | *"Hệ thống đã nhúng câu hỏi bằng embeddinggemma, lấy ra top 3 mục liên quan nhất và mô hình qwen3:4b đã trả lời chính xác giá vé 40,000 VND có trích dẫn mã nguồn [G01]. Mở bảng tham chiếu, ta thấy mục Dinh Độc Lập [G01] đạt điểm Cosine Similarity cao nhất là hơn 0.7."* | Trích dẫn nguồn `[Gxx]`, điểm Cosine Similarity của Top-K. |
| **1:05 - 1:20** | - Dán **Câu hỏi 2** vào ô chat $\rightarrow$ Nhấn Enter.<br>- Chờ câu trả lời hiện ra: *"I don't know this information as it is not currently covered in the Lumen Travel guide."* | *"Tiếp theo, em sẽ hỏi một câu về địa điểm không thuộc TP.HCM và không có trong cẩm nang: 'How much is the entrance ticket to Sun World Ba Na Hills?'. Trợ lý không hề tự bịa giá vé mà tuân thủ nghiêm ngặt quy tắc 'I don't know', từ chối trả lời do thông tin không nằm trong cẩm nang của Lumen Travel."* | Quy tắc chống ảo giác "I don't know". |
| **1:20 - 1:35** | - Rê chuột sang thanh Sidebar bên trái.<br>- Nhấp vào nút **Sign Out**.<br>- Màn hình quay trở lại form đăng nhập. | *"Cuối cùng, em nhấn nút 'Sign Out' ở thanh bên. Hàm `forget_user()` ngay lập tức xóa sạch thông tin người dùng và lịch sử chat trong `session_state`, đảm bảo ứng dụng không lưu trữ trái phép dữ liệu vào cơ sở dữ liệu. Phần demo chức năng của em đến đây là hoàn thành."* | Xóa session, xóa chat history khi Sign Out. |

---

## 3. Lời thoại liền mạch (Dành cho bạn luyện đọc trước khi quay)

> *"Xin chào thầy cô, đây là ứng dụng Lumen Travel Assistant cho TP.HCM. Đầu tiên, tính năng chat được bảo vệ hoàn toàn bằng Firebase Authentication, người dùng bắt buộc phải đăng nhập thì mới có thể truy cập.*
>
> *(Thao tác: Bấm Sign In)*
>
> *Sau khi đăng nhập thành công, thông tin phiên được lưu an toàn trong `st.session_state`. Bây giờ, em sẽ hỏi câu đầu tiên có trong cẩm nang:*
>
> *(Thao tác: Dán câu hỏi 1 và gửi)*
>
> *Hệ thống nhúng câu hỏi qua mô hình `embeddinggemma`, tìm kiếm bằng độ đo Cosine Similarity và mô hình `qwen3:4b` trả lời chính xác giá vé 40,000 VND kèm trích dẫn mã [G01]. Mở bảng tham chiếu Top-K, ta thấy rõ các đoạn thông tin liên quan cùng điểm số tương đồng cụ thể.*
>
> *(Thao tác: Mở expander rồi thu lại, dán câu hỏi 2 và gửi)*
>
> *Tiếp theo, em hỏi câu thứ hai về địa điểm không có trong cẩm nang: 'How much is the entrance ticket to Sun World Ba Na Hills?'. Nhờ cơ chế kiểm soát 2 tầng, trợ lý không hề bịa đặt mà trả lời chính xác câu mẫu: 'I don't know this information as it is not currently covered in the Lumen Travel guide.'*
>
> *(Thao tác: Bấm nút Sign Out)*
>
> *Cuối cùng, em bấm nút 'Sign Out'. Ứng dụng lập tức làm sạch toàn bộ lịch sử trò chuyện và phiên đăng nhập trong `st.session_state` mà không lưu vào Firestore, sau đó đưa người dùng quay lại màn hình đăng nhập. Phần demo của em đã hoàn tất."*

---

## 4. Những lỗi cần tránh khi quay phần Demo

1. **Nói quá dài vượt quá 1 phút 30 giây:**
   - Tổng thời lượng cả video tối đa là 5 phút (nội dung sau 5:00 không được chấm). Hãy giữ phần demo khoảng **1:20 - 1:30** để dành 2.5 phút cho phần phân tích 4 bước Computational Thinking và 1 phút cho phần kết quả kiểm thử (Test Results).
2. **Quên mở Expander nguồn trích dẫn:**
   - Đề bài ghi rõ: *"show which guide entries it used... show the retrieved entries and their scores, e.g. in an expandable panel"*. Khi trả lời xong Câu 1, **bắt buộc phải nhấp mở expander** trong khoảng 3–5 giây để video ghi lại điểm số và trích dẫn.
3. **Gõ chữ thủ công quá chậm:**
   - Hãy dùng `Ctrl + C` và `Ctrl + V` từ Notepad vào ô chat để video mượt mà và tiết kiệm thời gian.

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
   - **Kết quả thực tế:** **Fail**. Chỉ lấy được 3 địa điểm (`[G03]`, `[G04]`, `[G07]`), bỏ sót `[G06]` và `[G11]`.
   - **Bước thất bại (Failed Step):** **Failed at Retrieval Step** do giới hạn `TOP_K = 3`.

---

### 5.2. Kịch bản chi tiết từng giây (0:00 - 1:00)

| Thời gian | Thao tác trên màn hình | Lời thoại thuyết minh (Script đọc) |
| :--- | :--- | :--- |
| **0:00 - 0:25** | - Đang ở giao diện Chat (sau khi đăng nhập).<br>- Dán câu hỏi test thành công (Câu 4) $\rightarrow$ Nhấn Enter.<br>- Chờ câu trả lời hiện ra và mở expander trích dẫn `[G14]`. | *"Tiếp theo là phần báo cáo kết quả kiểm thử. Đầu tiên là một ca thành công (Success case) với câu hỏi diễn đạt gián tiếp (Paraphrase): 'Where can I take a boat trip to watch the sunset on the river in Saigon and how much does it cost?'. Hệ thống tìm kiếm ngữ nghĩa rất tốt, trích xuất chính xác mục [G14] Saigon Waterbus tại bến Bạch Đằng và trả lời đúng giá vé 15,000 VND."* |
| **0:25 - 0:50** | - Dán câu hỏi test thất bại (Câu 7) $\rightarrow$ Nhấn Enter.<br>- Khi câu trả lời hiện ra, mở expander chỉ vào 3 mục được lấy lên (`[G03]`, `[G04]`, `[G07]`). | *"Tiếp theo là một ca thất bại thực tế (Failure case) với câu hỏi tổng hợp nhiều địa điểm: 'List all attractions in District 1 that offer free entrance or free exterior visiting, and state their opening hours.'. Trong cẩm nang có tới 5 địa điểm miễn phí ở Quận 1, nhưng câu trả lời chỉ liệt kê được 3 địa điểm là G03, G04 và G07, bỏ sót phố đi bộ Nguyễn Huệ G06 và Bùi Viện G11."* |
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
> *Tiếp theo là một ca thất bại thực tế với câu hỏi tổng hợp: 'List all attractions in District 1 that offer free entrance or free exterior visiting, and state their opening hours.'. Trong cẩm nang có tới 5 địa điểm ở Quận 1 mở cửa miễn phí, nhưng trợ lý chỉ trả lời được 3 địa điểm là G03, G04 và G07, làm sót mất phố đi bộ Nguyễn Huệ G06 và Bùi Viện G11.*
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
| **Phần 1** | **Live Demo:** Đăng nhập $\rightarrow$ Hỏi 1 câu có trong cẩm nang (mở expander) $\rightarrow$ Hỏi 1 câu ngoài cẩm nang (show "I don't know") $\rightarrow$ Đăng xuất. | ~1 phút 30 giây | **0:00 – 1:30** |
| **Phần 2** | **Computational Thinking:** Thuyết minh 4 bước Abstraction $\rightarrow$ Decomposition $\rightarrow$ Pattern Recognition $\rightarrow$ Algorithm Design (bám sát file README). | ~2 phút 30 giây | **1:30 – 4:00** |
| **Phần 3** | **Test Results:** Báo cáo 1 ca Pass (Câu 4 Paraphrase) và 1 ca Fail (Câu 7 Multi-entry) phân tích lỗi ở Retrieval Step do $K=3$. | ~1 phút 00 giây | **4:00 – 5:00** |
| **TỔNG** | **Toàn bộ video (Tuyệt đối không để vượt quá 5 phút)** | **5 phút 00 giây** | **Tối đa 5:00** |


