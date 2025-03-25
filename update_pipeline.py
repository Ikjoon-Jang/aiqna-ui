import logging
from fuseki_query import (
    get_classes,
    get_object_properties,
    get_data_properties,
    get_individuals_with_literals,
    get_swrl_rules,
)
from ontology_to_text import ontology_elements_to_sentences
from embedding import get_embedding
from faiss_store import save_faiss_index
from datetime import datetime

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log", encoding="utf-8"),
        logging.StreamHandler()
    ],
)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
SENTENCE_LOG_FILE = f"sentences_{timestamp}.log"


def save_sentences_to_file(sentences, filename=SENTENCE_LOG_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        for i, sentence in enumerate(sentences, 1):
            f.write(f"{i}. {sentence}\n")
    logging.info(f"📝 자연어 문장 {len(sentences)}개를 '{filename}'에 저장 완료")


def main():
    logging.info("🚀 Fuseki에서 온톨로지 요소 가져오는 중...")
    classes = get_classes()
    object_props = get_object_properties()
    data_props = get_data_properties()
    individuals = get_individuals_with_literals()
    swrl_rules = get_swrl_rules()
    logging.info("✅ 온톨로지 요소 불러오기 완료")

    logging.info("🧠 자연어 문장으로 변환 중...")
    sentences = ontology_elements_to_sentences(
        classes, object_props, data_props, individuals, swrl_rules
    )
    logging.info(f"✅ 총 {len(sentences)}개의 문장 생성")
    save_sentences_to_file(sentences)

    logging.info("🔍 OpenAI 임베딩 생성 중...") 
    embeddings = []
    for sentence in sentences:
        try:
            emb = get_embedding(sentence)
            embeddings.append(emb)
        except Exception as e:
            logging.warning(f"❌ 임베딩 실패: '{sentence}' => {e}")

    logging.info(f"✅ 임베딩 생성 완료: {len(embeddings)}개")

    logging.info("💾 FAISS 인덱스 저장 중...")
    save_faiss_index(sentences[:len(embeddings)], embeddings)
    logging.info("✅ FAISS 인덱스 저장 완료")


if __name__ == "__main__":
    main()
