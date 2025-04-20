#pip install transformers peft datasets accelerate bitsandbytes trl

from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, TextStreamer
from peft import get_peft_model, LoraConfig, TaskType
from datasets import Dataset
import torch
import pandas as pd

# 데이터 로드 및 전처리
data = pd.read_json("/models/dataset.json", lines=True)
data['Context_length'] = data['Context'].apply(len)
filtered_data = data[data['Context_length'] <= 1000]

# 모델 로드 (Hugging Face 형식으로)
BASE_MODEL = "/models/Llama-3.2-3B"
output_dir = "/models/3B_category_001"
data_size = 1200
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, load_in_4bit=True, device_map="auto")
max_seq_length = 2048

# PEFT (LoRA) 구성
lora_config = LoraConfig(
    r=16,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "up_proj", "down_proj", "o_proj", "gate_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# 프롬프트 포맷
data_prompt = ''
with open("/models/data_prompt.txt", "r",encoding="utf-8") as f:
    data_prompt=f.read()

tokenizer.pad_token = tokenizer.eos_token
EOS_TOKEN = tokenizer.eos_token

def formatting_prompt(examples):
    inputs       = examples["Context"]
    outputs      = examples["Response"]
    texts = []
    for input_, output in zip(inputs, outputs):
        text = data_prompt.format(input_, output) + EOS_TOKEN
        texts.append(text)

    tokenized_inputs = tokenizer(texts, padding="max_length", truncation=True, max_length=max_seq_length)

    return {
        "input_ids": tokenized_inputs["input_ids"],
        "attention_mask": tokenized_inputs["attention_mask"],
        "labels": tokenized_inputs["input_ids"],  # 학습에서는 labels가 필요
    }

# 데이터셋 변환
full_dataset = Dataset.from_pandas(filtered_data)
full_dataset = full_dataset.shuffle(seed=65).select(range(data_size))

# 80% 학습, 20% 테스트로 분할
train_test = full_dataset.train_test_split(test_size=0.2)

# 데이터 확인
training_data = train_test["train"]
test_dataset = train_test["test"]

training_data = training_data.map(formatting_prompt, batched=True)
test_dataset = test_dataset.map(formatting_prompt, batched=True)

# 학습 인자 설정
training_args = TrainingArguments(
    output_dir=output_dir,
    num_train_epochs=2,
    per_device_train_batch_size=16,
    gradient_accumulation_steps=8,
    learning_rate=3e-4,
    weight_decay=0.01,
    warmup_steps=10,
    logging_steps=1,
    fp16=torch.cuda.is_available(),  # FP16 지원 여부 확인
    optim="adamw_torch",
    seed=0,
    report_to="none"
)

# Trainer 실행
from trl import SFTTrainer

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=training_data,
    args=training_args,
)

trainer.train()

test_results = trainer.predict(test_dataset)
# 추론
text = ''
with open("/models/query.txt", "r",encoding="utf-8") as f:
    text=f.read()

prompt = data_prompt.format(text, "")
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=5020, repetition_penalty=1.2, no_repeat_ngram_size=3)
decoded = tokenizer.decode(outputs[0], skip_special_tokens=True) 
#answer = decoded.split("### Response:")[-1].strip()
answer = decoded.split("### Response:")[-1].strip().split("\n")[0].strip()
print("Answer:", answer)

# 모델 저장
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
