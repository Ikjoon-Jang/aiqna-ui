from embedding import get_embedding
from faiss_store import save_embeddings_to_faiss, search_faiss

sentences = [
    "Shipment is handled by the exporter.",
    "Sensor triggers an alert if temperature is low.",
    "Document is required for customs clearance."
]

# 1. 임베딩
embeddings = [get_embedding(s) for s in sentences]

# 2. 저장
save_embeddings_to_faiss(sentences, embeddings)

# 3. 검색
query = "Low temperature warning"
query_vec = get_embedding(query)
results = search_faiss(query_vec, k=3)

print("🔍 검색 결과:")
for r in results:
    print("-", r)
