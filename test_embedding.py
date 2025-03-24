from embedding import get_embedding

sentence = "Shipment is a logistics unit transported by Carrier."
vec = get_embedding(sentence)
print(f"✅ 임베딩 벡터 길이: {len(vec)}")
print(vec[:5])  # 앞부분 일부 출력