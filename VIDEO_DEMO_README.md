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
