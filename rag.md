RAG, ChromaDB 통합 방식 추천
RAG 시스템 통합은 크게 세 가지 주요 단계로 나눌 수 있습니다:
데이터 준비 및 Vector DB 구성: RAG 시스템이 참조할 지식 기반(Knowledge Base)을 정의하고, 이를 임베딩하여 ChromaDB에 저장하는 단계입니다.
Vector DB 검색 (Retrieval): 사용자 쿼리에 가장 관련성이 높은 정보를 ChromaDB에서 찾아오는 단계입니다.
LLM 프롬프트 증강 (Augmentation) 및 응답 생성: 검색된 정보를 LLM의 프롬프트에 추가하여, LLM이 이 추가 정보를 바탕으로 더 풍부하고 정확한 응답을 생성하도록 하는 단계입니다.


1. 데이터 준비 및 Vector DB 구성
지식 기반 정의: RAG 시스템이 검색할 정보를 결정해야 합니다. 
예를 들어, 다음과 같은 정보를 사용할 수 있습니다:

여행 가이드: 각 도시의 주요 명소, 맛집, 현지 팁, 교통 정보 등.
호텔/숙소 정보: 특정 호텔의 특징, 가격대, 편의시설.
액티비티 정보: 다양한 여행 활동의 세부 정보, 예약 방법.
사용자 선호도 데이터: 개인화된 여행 계획을 위한 사용자별 선호 정보.
데이터 형식: 초기에는 간단한 텍스트 파일, Markdown 파일, 또는 Python 코드 내의 리스트/딕셔너리 형태로 시작할 수 있습니다. 예를 들어, data/travel_info.txt와 같은 파일을 만들 수 있습니다.

청킹 (Chunking): 긴 문서를 LLM이 처리하기 쉬운 작은 단위의 "청크(chunk)"로 나눕니다. LangChain의 RecursiveCharacterTextSplitter 등을 활용할 수 있습니다.
임베딩 (Embedding): 각 청크를 임베딩 모델(사용 중인 text-embedding-3-large 또는 다른 OpenAI 임베딩 모델)을 사용하여 벡터(숫자 배열)로 변환합니다.

ChromaDB 저장: 생성된 벡터와 원본 텍스트 청크를 ChromaDB에 저장합니다. ChromaDB는 로컬 파일 시스템에 저장하거나, 서버-클라이언트 모드로 운영할 수 있습니다.


1.코드 수정 방안 (개요):
새 파일 생성: db/chroma_setup.py 또는 utils/rag_utils.py 같은 파일을 생성하여 ChromaDB 초기화, 데이터 로드, 청킹, 임베딩, 데이터 저장 로직을 캡슐화합니다.


config/config.py 업데이트: 임베딩 모델 관련 설정(API 키, 배포 이름)을 추가하고, ChromaDB의 저장 경로 등을 설정합니다.

2. Vector DB 검색 (Retrieval)
쿼리 임베딩: 사용자의 입력(예: 여행지, 선호 활동)이 들어오면, 이를 임베딩 모델을 사용하여 벡터로 변환합니다.
유사성 검색: 변환된 쿼리 벡터를 ChromaDB에 질의하여, 가장 유사한 벡터(즉, 가장 관련성 높은 텍스트 청크)들을 검색합니다.

코드 수정 방안 (개요):
agents/coordinator.py의 plan_travel 메서드 또는 새로운 헬퍼 메서드에 검색 로직을 통합합니다.
ChromaDB 클라이언트를 초기화하고 검색 기능을 호출하는 코드를 추가합니다.


3. LLM 프롬프트 증강 및 응답 생성
프롬프트 증강: 검색된 텍스트 청크들을 LLM의 프롬프트에 "컨텍스트" 정보로 추가합니다. 이렇게 하면 LLM은 사용자 질문에 대한 응답을 생성할 때 이 컨텍스트를 참조하게 됩니다.
LLM 호출: 증강된 프롬프트를 사용하여 LLM을 호출하고 응답을 받습니다.
코드 수정 방안 (개요):
agents/coordinator.py의 _format_user_input 메서드를 수정하여 검색된 컨텍스트를 프롬프트에 추가하도록 합니다.
프롬프트 템플릿에 컨텍스트를 삽입할 플레이스홀더를 추가합니다.


구체적인 초기 구현 추천:
가장 간단하게 시작하려면, 
travel_info.txt와 같은 간단한 텍스트 파일을 지식 기반으로 사용해 볼 수 있습니다.

추천 워크플로우:

ChromaDB 및 임베딩 설정:
config/config.py에 임베딩 모델 설정을 추가합니다. (이미 AOAI_EMBEDDING_DEPLOYMENT가 있으므로 활용 가능)
새로운 스크립트 (예: ingest_data.py)를 만들어 travel_info.txt 파일을 읽고, 청킹하고, 임베딩하여 ChromaDB에 저장합니다. 이 스크립트는 한 번만 실행하여 Vector DB를 구축합니다.

TravelCoordinatorAgent 수정:
agents/coordinator.py에서 TravelCoordinatorAgent 클래스에 ChromaDB 클라이언트를 초기화하는 로직을 추가합니다.

plan_travel 메서드 내에서 사용자 입력이 들어올 때마다 ChromaDB에서 관련 정보를 검색하는 로직을 추가합니다.

검색된 정보를 _format_user_input이 생성하는 프롬프트에 추가하여 LLM에게 전달합니다.
시작하시려면, 어떤 종류의 데이터를 RAG 시스템의 지식 기반으로 사용하고 싶은지 알려주실 수 있을까요? (예: 특정 도시의 관광 정보, 일반적인 여행 팁 등) 이에 따라 데이터 준비 및 청킹 방식을 구체화할 수 있습니다.