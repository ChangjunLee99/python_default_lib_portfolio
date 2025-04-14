from safetensors import safe_open
from safetensors.torch import save_file
from transformers import AutoModelForCausalLM
import torch

# 저장할 레이어 리스트
layer_names = ["q_proj", "k_proj", "v_proj", "up_proj", "down_proj", "o_proj", "gate_proj"]

# 모델 로드
model_path = '/models/Llama-3.2:3B'
model = AutoModelForCausalLM.from_pretrained(model_path)

# 레이어 추출
layers_to_save = {}
for name, param in model.named_parameters():
    if any(layer_name in name for layer_name in layer_names):
        layers_to_save[name] = param.detach().cpu()

# `safetensors`로 저장
output_path = '/models/Llama-3.2:3B.safetensors'

save_file(layers_to_save, output_path)
# with safe_open(output_path, 'wb') as f:
#     for name, tensor in layers_to_save.items():
#         f.write(name, tensor)  # 텐서를 safetensors 포맷으로 저장
