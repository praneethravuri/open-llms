from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer, DataCollatorForSeq2Seq
from datasets import load_dataset
import numpy as np
import os
import torch

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

def train_model():
    model_name = "sshleifer/distilbart-cnn-12-6"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)

    # Load the SQuAD dataset
    dataset = load_dataset("squad")

    # Split the dataset: 80% for training and 20% for validation
    train_test_split = dataset["train"].train_test_split(test_size=0.2)
    train_data = train_test_split["train"]
    val_data = train_test_split["test"]

    # Preprocess the data
    def preprocess_function(examples):
        inputs = [q.strip() for q in examples["question"]]
        targets = [a["text"][0].strip() for a in examples["answers"]]
        model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding="max_length")
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(targets, max_length=128, truncation=True, padding="max_length")
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized_train = train_data.map(preprocess_function, batched=True)
    tokenized_val = val_data.map(preprocess_function, batched=True)

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    training_args = Seq2SeqTrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        weight_decay=0.01,
        save_total_limit=3,
        num_train_epochs=3,
        predict_with_generate=True
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_val,
        data_collator=data_collator
    )

    trainer.train()
    model.save_pretrained("./app/models/distilbart_cnn_12_6")
    tokenizer.save_pretrained("./app/models/distilbart_cnn_12_6")

if __name__ == "__main__":
    train_model()
