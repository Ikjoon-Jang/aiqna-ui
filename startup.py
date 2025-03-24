# startup.py

import logging
from datetime import datetime

from fuseki_query import (
    get_classes,
    get_object_properties,
    get_data_properties,
    get_swrl_rules
)
from ontology_to_text import (
    class_to_text,
    object_property_to_text,
    data_property_to_text,
    swrl_rule_to_text
)
from embedding import embed_sentences
from faiss_store import save_embeddings_to_faiss

# 로그 설정
log_filename = f"rag_pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'  # ✅ 인코딩 설정 추가
)

def extract_and_convert_to_text():
    logging.info("🔍 Fuseki에서 온톨로지 정보 추출 시작")
    class_data = get_classes()
    obj_data = get_object_properties()
    data_data = get_data_properties()
    swrl_data = get_swrl_rules()
    logging.info(f"📦 추출 완료: Class={len(class_data)}, ObjectProperty={len(obj_data)}, DataProperty={len(data_data)}, SWRL={len(swrl_data)}")

    sentences = []

    sentences += [
        class_to_text(
            c["class"]["value"],
            c.get("label", {}).get("value"),
            c.get("comment", {}).get("value")
        ) for c in class_data
    ]

    sentences += [
        object_property_to_text(
            o["property"]["value"],
            o.get("domain", {}).get("value"),
            o.get("range", {}).get("value")
        ) for o in obj_data
    ]

    sentences += [
        data_property_to_text(
            d["property"]["value"],
            d.get("domain", {}).get("value"),
            d.get("range", {}).get("value")
        ) for d in data_data
    ]

    sentences += [
        swrl_rule_to_text(rule) for rule in swrl_data
    ]

    logging.info(f"📝 자연어 문장 변환 완료: 총 {len(sentences)}개 문장")
    return sentences


def build_rag_pipeline():
    logging.info("🚀 RAG 파이프라인 실행 시작")
    print("📥 온톨로지 → 자연어 변환 중...")
    sentences = extract_and_convert_to_text()

    print(f"📄 총 {len(sentences)}개의 문장을 임베딩합니다...")
    logging.info("🔠 임베딩 시작")
    embeddings = embed_sentences(sentences)
    logging.info("🔠 임베딩 완료")

    print("💾 FAISS 인덱스에 저장 중...")
    logging.info("💾 FAISS 인덱스 저장 시작")
    save_embeddings_to_faiss(sentences, embeddings)
    logging.info("✅ FAISS 저장 완료")

    print("✅ RAG 파이프라인 구축 완료!")
    logging.info("🎉 전체 파이프라인 완료")


if __name__ == "__main__":
    build_rag_pipeline()
