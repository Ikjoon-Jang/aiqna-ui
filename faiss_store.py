# faiss_store.py

import faiss
import numpy as np
import pickle
from typing import List, Tuple

VECTOR_SIZE = 1536  # OpenAI embedding vector size (e.g., text-embedding-ada-002)
INDEX_FILE = "faiss_index.index"
META_FILE = "faiss_metadata.pkl"

# 문장 + 벡터를 FAISS 인덱스와 메타데이터로 저장
def save_embeddings_to_faiss(sentences: List[str], embeddings: List[List[float]]):
    vectors = np.array(embeddings, dtype="float32")
    index = faiss.IndexFlatL2(VECTOR_SIZE)
    index.add(vectors)

    faiss.write_index(index, INDEX_FILE)

    with open(META_FILE, "wb") as f:
        pickle.dump(sentences, f)

    print(f"✅ 저장 완료: {len(sentences)}개 문장을 FAISS에 저장했습니다.")

# FAISS와 문장 메타데이터 불러오기
def load_faiss_index() -> Tuple[faiss.IndexFlatL2, List[str]]:
    index = faiss.read_index(INDEX_FILE)
    with open(META_FILE, "rb") as f:
        sentences = pickle.load(f)
    return index, sentences

# 질의 벡터에 대해 유사한 문장 top-k 검색
def search_faiss(query_vector: List[float], k: int = 5) -> List[str]:
    index, sentences = load_faiss_index()
    query = np.array([query_vector], dtype="float32")
    distances, indices = index.search(query, k)
    return [sentences[i] for i in indices[0]]

save_faiss_index = save_embeddings_to_faiss