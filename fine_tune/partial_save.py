#tensorflow 구조 llm 모델 부분 저장

import tensorflow as tf
from transformers import TFAutoModel

# 예시 모델 로드
model = TFAutoModel.from_pretrained("bert-base-uncased")

# 예: 1번째 Transformer 블록의 Self-Attention query 가중치 저장
q_proj_weights = model.bert.encoder.layer[0].attention.self.query.get_weights()

# 저장 (numpy 배열로 저장)
import numpy as np
np.save("q_proj_weights.npy", q_proj_weights)


# 새 모델 로드 (동일한 구조여야 함)
new_model = TFAutoModel.from_pretrained("bert-base-uncased")

# 저장된 가중치 로드
q_proj_weights = np.load("q_proj_weights.npy", allow_pickle=True)

# 해당 레이어에 주입
new_model.bert.encoder.layer[0].attention.self.query.set_weights(q_proj_weights)

# 예: query, key, value projection 모두 저장
weights_dict = {
    "q_proj": model.bert.encoder.layer[0].attention.self.query.get_weights(),
    "k_proj": model.bert.encoder.layer[0].attention.self.key.get_weights(),
    "v_proj": model.bert.encoder.layer[0].attention.self.value.get_weights(),
}
np.save("proj_weights.npy", weights_dict)

# 나중에 불러오기
weights_dict = np.load("proj_weights.npy", allow_pickle=True).item()
new_model.bert.encoder.layer[0].attention.self.query.set_weights(weights_dict["q_proj"])