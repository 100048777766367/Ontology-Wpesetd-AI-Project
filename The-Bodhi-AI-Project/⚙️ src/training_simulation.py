# -*- coding: utf-8 -*-
"""
training_simulation.py

Mô phỏng pipeline huấn luyện (fine-tuning) cho dự án Bodhi-AI.
Kịch bản này thực hiện các bước sau:
1. Tải và tiền xử lý bộ dữ liệu huấn luyện (`train.jsonl`, `validation.jsonl`).
2. Khởi tạo Tokenizer và Mô hình Ngôn ngữ nền (pre-trained).
3. Thiết lập các tham số huấn luyện (Training Arguments).
4. Khởi tạo và chạy đối tượng `Trainer` của Hugging Face.
5. Đánh giá mô hình và lưu lại checkpoint tốt nhất.

Đây là kịch bản mô phỏng cho "Ngày T+1 -> T+3" trong lộ trình dự án.
"""

import json
import logging
from pathlib import Path
import torch # type: ignore
from transformers import ( # type: ignore
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq,
    Trainer,
    TrainingArguments,
)
from datasets import Dataset # type: ignore

# --- Giai Đoạn 1: Thiết Lập & Chuẩn Bị ---

# Thiết lập logging để theo dõi tiến trình
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_and_prepare_datasets(train_path: str, valid_path: str) -> (Dataset, Dataset): # type: ignore
    """
    Đọc các tệp tin .jsonl và chuyển chúng thành đối tượng Dataset của Hugging Face.
    """
    logger.info(f"Đang tải dữ liệu từ {train_path} và {valid_path}...")
    try:
        train_records = [json.loads(line) for line in Path(train_path).read_text(encoding='utf-8').splitlines()]
        valid_records = [json.loads(line) for line in Path(valid_path).read_text(encoding='utf-8').splitlines()]
        
        train_dataset = Dataset.from_list(train_records)
        valid_dataset = Dataset.from_list(valid_records)
        logger.info(f"Tải thành công: {len(train_dataset)} mẫu huấn luyện, {len(valid_dataset)} mẫu kiểm định.")
        return train_dataset, valid_dataset
    except FileNotFoundError as e:
        logger.error(f"Lỗi: Không tìm thấy tệp dữ liệu. {e}")
        raise
    except Exception as e:
        logger.error(f"Lỗi khi đọc hoặc xử lý tệp dữ liệu: {e}")
        raise


def tokenize_function(examples, tokenizer, max_input_length=256, max_target_length=128):
    """
    Hàm Tokenization: Chuyển đổi văn bản thành các ID số mà mô hình có thể hiểu.
    Input được xây dựng bằng cách ghép `question` và `thought_process`.
    """
    # Xây dựng input prompt theo cấu trúc đã thống nhất
    inputs = [f"question: {q}\nthought_process: {tp}" for q, tp in zip(examples["question"], examples["thought_process"])]
    targets = [ans for ans in examples["answer"]]

    # Tokenize input và target
    model_inputs = tokenizer(inputs, max_length=max_input_length, truncation=True, padding="max_length")
    labels = tokenizer(targets, max_length=max_target_length, truncation=True, padding="max_length")

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# --- Giai Đoạn 2: Thực Thi Huấn Luyện ---

def main():
    """
    Hàm chính điều khiển toàn bộ pipeline huấn luyện.
    """
    # 1. Tải dữ liệu
    # Giả định các tệp dữ liệu nằm trong thư mục con `data/`
    train_dataset, valid_dataset = load_and_prepare_datasets("data/level_1_foundation.jsonl", "data/validation.jsonl") # Ví dụ chỉ dùng level 1

    # 2. Khởi tạo Tokenizer và Model
    model_name = "google/flan-t5-small"  # Mô hình nền được chọn để mô phỏng
    logger.info(f"Đang khởi tạo tokenizer và mô hình từ '{model_name}'...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # 3. Áp dụng Tokenization cho toàn bộ dữ liệu
    logger.info("Đang token hóa dữ liệu...")
    tokenized_train_ds = train_dataset.map(lambda x: tokenize_function(x, tokenizer), batched=True)
    tokenized_valid_ds = valid_dataset.map(lambda x: tokenize_function(x, tokenizer), batched=True)
    
    # Loại bỏ các cột không cần thiết để tăng tốc độ huấn luyện
    tokenized_train_ds = tokenized_train_ds.remove_columns(train_dataset.column_names)
    tokenized_valid_ds = tokenized_valid_ds.remove_columns(valid_dataset.column_names)


    # 4. Thiết lập Data Collator (để padding động, tối ưu bộ nhớ)
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    # 5. Định nghĩa các tham số huấn luyện (Training Arguments)
    logger.info("Đang thiết lập các tham số huấn luyện...")
    training_args = TrainingArguments(
        output_dir="checkpoints",                 # Thư mục lưu checkpoints
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
        learning_rate=2e-5,
        weight_decay=0.01,
        
        # Cấu hình đánh giá và lưu trữ
        evaluation_strategy="epoch",              # Đánh giá sau mỗi epoch
        save_strategy="epoch",                    # Lưu checkpoint sau mỗi epoch
        logging_strategy="epoch",                 # Ghi log sau mỗi epoch
        load_best_model_at_end=True,              # Tự động tải lại model tốt nhất khi kết thúc
        metric_for_best_model="eval_loss",        # Tiêu chí chọn model tốt nhất
        greater_is_better=False,                  # Vì loss càng nhỏ càng tốt
        
        # Cấu hình khác
        push_to_hub=False,
        report_to="none",                         # Tắt báo cáo lên các dịch vụ bên ngoài
    )

    # 6. Khởi tạo đối tượng `Trainer`
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train_ds,
        eval_dataset=tokenized_valid_ds,
        tokenizer=tokenizer,
        data_collator=data_collator,
        # compute_metrics có thể được bỏ qua nếu chỉ dựa vào `eval_loss`
    )

    # --- Giai Đoạn 3: Chạy và Lưu Kết Quả ---
    
    # 7. Bắt đầu quá trình huấn luyện
    logger.info("--- Bắt đầu quá trình huấn luyện (Mô phỏng Ngày T+1 -> T+3) ---")
    train_result = trainer.train()
    logger.info("--- Quá trình huấn luyện đã hoàn tất ---")

    # 8. Đánh giá cuối cùng và ghi lại log
    logger.info("Đang thực hiện đánh giá cuối cùng trên tập validation...")
    final_metrics = trainer.evaluate()
    logger.info(f"Kết quả đánh giá cuối cùng: {final_metrics}")
    
    # Hiển thị lịch sử loss (ví dụ)
    for log in trainer.state.log_history:
        if 'loss' in log:
            logger.info(f"Epoch {log['epoch']}: Training Loss = {log['loss']:.4f}")
        if 'eval_loss' in log:
            logger.info(f"Epoch {log['epoch']}: Validation Loss = {log['eval_loss']:.4f}")

    # 9. Lưu lại mô hình và tokenizer tốt nhất
    best_model_dir = "fine_tuned_model_v1"
    logger.info(f"Đang lưu mô hình tốt nhất vào thư mục '{best_model_dir}'...")
    trainer.save_model(best_model_dir)
    tokenizer.save_pretrained(best_model_dir)
    logger.info(f"Mô hình đã được lưu. Hoàn tất pipeline.")


if __name__ == "__main__":
    main()