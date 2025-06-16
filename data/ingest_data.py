import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from config.config import get_embeddings # config.py에서 임베딩 함수 임포트

# ChromaDB 저장 경로
CHROMA_PERSIST_DIRECTORY = "./chroma_db"

def ingest_data():
    print("데이터 임베딩 및 ChromaDB 저장 시작...")

    # 1. 문서 로드
    loader = TextLoader("data/travel_info.txt", encoding="utf-8")
    documents = loader.load()

    # 2. 문서 청킹
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    texts = text_splitter.split_documents(documents)
    print(f"총 {len(texts)}개의 청크로 분할되었습니다.")

    # 3. 임베딩 모델 초기화
    embeddings = get_embeddings()
    if embeddings is None:
        print("임베딩 모델 초기화에 실패했습니다. 환경 변수를 확인해주세요.")
        return

    # 4. ChromaDB에 저장
    print("ChromaDB에 임베딩 저장 중...")
    vectorstore = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=CHROMA_PERSIST_DIRECTORY
    )
    vectorstore.persist()
    print(f"ChromaDB에 데이터 저장이 완료되었습니다. 경로: {CHROMA_PERSIST_DIRECTORY}")

if __name__ == "__main__":
    # ChromaDB 저장 디렉토리 생성 (없으면)
    if not os.path.exists(CHROMA_PERSIST_DIRECTORY):
        os.makedirs(CHROMA_PERSIST_DIRECTORY)
    ingest_data() 