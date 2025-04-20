from transformers import TrainingArguments, TextStreamer
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments
)
import torch

#테스트할 모델 경로
model_path="/models/3B_category_004"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    device_map="auto",
).to("cuda")
text = ''
#테스트할 텍스트 경로
with open("/models/query.txt", "r",encoding="utf-8") as f:

    text=f.read()

input_ids = tokenizer(text, return_tensors="pt").to("cuda")
outputs = model.generate(**input_ids)
decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
#answer = decoded.split("### Response:")[-1].strip()
print("TOTAL:",decoded)
answer = decoded.split("### Response:")[-1].strip().split("\n")[0].strip()
print("Answer:", answer)
