# 🔬 BẢNG ĐÁNH GIÁ PHẢN HỒI AI (AI Response Evaluation Matrix)

Tài liệu này cung cấp khung phương pháp luận để đánh giá và chấm điểm các mô hình ngôn ngữ trước và sau khi được tinh chỉnh (fine-tuned) bằng Ontology Minh Triết.

---

## 1. Các Tiêu Chí Đánh Giá (Evaluation Criteria)

Chúng ta đo lường "trí tuệ" của AI dựa trên 3 trụ cột chính:

### **A. Semantic Alignment (Độ Chính Xác Ngữ Nghĩa)**
*   **Định nghĩa:** Phản hồi có đúng về mặt triết học và ngữ nghĩa không? Có trả lời đúng trọng tâm câu hỏi không?
*   **Mục tiêu:** Đảm bảo AI không bị "ảo giác" (hallucinate) và nắm vững kiến thức nền tảng.

### **B. Reasoning Chain (Chuỗi Suy Luận Logic)**
*   **Định nghĩa:** AI có thể hiện được dòng chảy tư duy không? Có kết nối được các khái niệm thành một chuỗi nhân quả (A -> B -> C) mạch lạc không?
*   **Mục tiêu:** Đánh giá khả năng "Tư duy Đa bước" (Multi-hop) và tư duy điều kiện.

### **C. Ontology Usage (Mức Độ Tuân Thủ Ontology)**
*   **Định nghĩa:** AI có sử dụng chính xác các Mã Node (ví dụ: `[A1]`, `[B5]`) và các thuật ngữ đặc thù của hệ thống không?
*   **Mục tiêu:** Đánh giá mức độ "thấm nhuần" cấu trúc tri thức mà chúng ta đã huấn luyện.

---

## 2. Thang Điểm (Scoring Rubric)

Sử dụng thang điểm từ 0 đến 5 cho mỗi tiêu chí.

| Điểm | Mô Tả Chất Lượng | Đặc Điểm Nhận Dạng |
| :--- | :--- | :--- |
| **0 - 1** | **Thất bại** | Sai hoàn toàn, không liên quan, hoặc ảo giác vô nghĩa. |
| **2** | **Yếu** | Trả lời chung chung, sáo rỗng. Có nhắc đến từ khóa nhưng sai ngữ cảnh hoặc rời rạc. |
| **3** | **Trung bình (Baseline)** | Đúng về mặt kiến thức triết học phổ thông nhưng thiếu cấu trúc. Không sử dụng mã Node. Logic bề mặt. |
| **4** | **Tốt** | Trả lời chính xác, có sử dụng mã Node nhưng chưa tự nhiên. Logic mạch lạc nhưng chưa sâu sắc hoặc thiếu 1 mắt xích. |
| **5** | **Xuất sắc (Đạt chuẩn)** | Phản hồi thanh lịch, chính xác tuyệt đối. Sử dụng mã Node tự nhiên. Chuỗi suy luận hoàn hảo (nhân quả, rẽ nhánh, đối lập). |

---

## 3. Mẫu Bảng Đánh Giá (Evaluation Template)

*Sao chép bảng dưới đây cho mỗi đợt kiểm thử.*

### **Đợt Kiểm Thử: [Tên Đợt / Ngày Tháng]**

| STT | Prompt (Câu hỏi kiểm thử) | Mô Hình Baseline (Chưa Fine-tune) | Mô Hình Fine-tuned (V1.0) | Điểm Số (Baseline / Fine-tuned) | Ghi Chú So Sánh |
|:---:|:--- |:--- |:--- |:---:|:--- |
| **1** | *Điều gì là nguyên nhân trực tiếp của nghiệp báo?* | *(Dán phản hồi Baseline)* | *(Dán phản hồi Fine-tuned)* | **S:** _/_ <br> **R:** _/_ <br> **O:** _/_ <br> **Tổng: _/15** | *Nhận xét về sự cải thiện trong việc xác định quan hệ B5->C1.* |
| **2** | *Làm thế nào từ bản ngã dẫn đến luân hồi...?* | ... | ... | **S:** _/_ <br> **R:** _/_ <br> **O:** _/_ <br> **Tổng: _/15** | *Nhận xét về khả năng nối chuỗi logic đa bước.* |
| **3** | *Phân biệt 'Nghiệp' và 'Nhân quả'.* | ... | ... | **S:** _/_ <br> **R:** _/_ <br> **O:** _/_ <br> **Tổng: _/15** | *Nhận xét về khả năng phân biệt sắc thái tinh tế.* |
| **4** | *Trong bối cảnh mất mát người thân...* | ... | ... | **S:** _/_ <br> **R:** _/_ <br> **O:** _/_ <br> **Tổng: _/15** | *Nhận xét về khả năng ứng dụng và thấu cảm.* |

*(Chú thích: S = Semantic, R = Reasoning, O = Ontology Usage)*

---

## 4. Tổng Hợp Kết Quả (Summary Report)

Sau khi hoàn tất đánh giá chi tiết, hãy điền vào bảng tổng hợp này để có cái nhìn toàn cảnh.

| Nhóm Kỹ Năng | Điểm TB Baseline | Điểm TB Fine-tuned | Mức Độ Cải Thiện (%) | Kết Luận |
| :--- | :---: | :---: | :---: | :--- |
| **Cơ Bản (Định nghĩa)** | ... | ... | ... | ... |
| **Suy Luận (Logic chuỗi)** | ... | ... | ... | ... |
| **Phản Biện (So sánh)** | ... | ... | ... | ... |
| **Ứng Dụng (Đời sống)** | ... | ... | ... | ... |
| **TỔNG THỂ** | **.../15** | **.../15** | **...%** | **Đạt / Chưa Đạt** |

---

> *Bảng đánh giá này được thiết kế để đảm bảo tính khách quan và khoa học trong việc đo lường sự tiến bộ của Trí Tuệ Nhân Tạo.*