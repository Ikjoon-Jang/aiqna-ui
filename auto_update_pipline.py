import os
import time
import hashlib
import logging
import requests
from update_pipeline import main as run_pipeline

# 환경 설정
RDF_FILE = "./ontology/RDF_Forwarding.xml"  # 감지할 RDF/TTL/OWL 파일명
FUSEKI_UPDATE_URL = "http://3.36.178.68:3030/dataset/data?graph=default"  # Fuseki 데이터셋 주소
CHECK_INTERVAL = 10  # 변경 감지 주기 (초)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("rdf_watch.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def get_file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def update_fuseki(rdf_path):
    with open(rdf_path, "rb") as f:
        headers = {"Content-Type": "text/turtle"}
        res = requests.post(FUSEKI_UPDATE_URL, headers=headers, data=f)
        res.raise_for_status()
    logging.info("✅ Fuseki에 RDF 업로드 완료")

def watch_rdf_file():
    if not os.path.exists(RDF_FILE):
        logging.error(f"❌ {RDF_FILE} 파일이 존재하지 않습니다.")
        return

    last_hash = get_file_hash(RDF_FILE)
    logging.info("👀 RDF 파일 변경 감지 시작...")

    while True:
        try:
            time.sleep(CHECK_INTERVAL)
            current_hash = get_file_hash(RDF_FILE)
            if current_hash != last_hash:
                logging.info("🔄 RDF 파일 변경 감지됨. 업데이트 실행 중...")
                update_fuseki(RDF_FILE)
                run_pipeline()  # update_pipeline.py의 메인 함수 실행
                last_hash = current_hash
                logging.info("✅ 변경 처리 완료")
        except Exception as e:
            logging.error(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    watch_rdf_file()
