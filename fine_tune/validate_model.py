# evaluate.py
from transformers import AutoTokenizer, AutoModelForCausalLM
from datasets import load_dataset, Dataset
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import torch

# 모델 및 토크나이저 로드
output_dir = "/models/3B_category_004"
model = AutoModelForCausalLM.from_pretrained(output_dir, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(output_dir)

# 평가용 데이터셋 로드
df = pd.read_json("/models/dataset.json", lines=True)
df = df[df['Context'].apply(len) <= 1000]
df = df.sample(n=100)  # 간단히 100건만 사용
dataset = Dataset.from_pandas(df)

# prompt 포맷 불러오기
with open("/models/data_prompt.txt", "r", encoding="utf-8") as f:
    prompt_format = f.read()

# 정답 및 예측 저장용
y_true = []
y_pred = []

for example in dataset:
    context = example["Context"]
    label = example["Response"]  # or label field if classification
    prompt = prompt_format.format(context, "")

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=512, repetition_penalty=1.2, no_repeat_ngram_size=3)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    result = decoded.split("### Response:")[-1].strip().split("\n")[0]

    y_true.append(label.strip())
    y_pred.append(result.strip())

# 정확도 또는 간단한 텍스트 유사도 측정
from sklearn.metrics import accuracy_score
acc = accuracy_score(y_true, y_pred)
print(f"Accuracy: {acc:.4f}")

# 상세 보고서
print(classification_report(y_true, y_pred))
