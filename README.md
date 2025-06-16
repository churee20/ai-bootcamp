# ✈️ AI 여행 플래너 (Multi-Agent System with RAG)

## 💡 프로젝트 개요

이 프로젝트는 Multi-Agent System과 RAG (Retrieval Augmented Generation) 기술을 활용하여 사용자 맞춤형 여행 계획을 수립하는 AI 여행 플래너 애플리케이션입니다. Streamlit 기반의 사용자 친화적인 인터페이스를 제공하며, Azure OpenAI 모델과 ChromaDB를 사용하여 풍부하고 정확한 여행 정보를 제공합니다.

## ✨ 주요 기능

*   **사용자 맞춤형 여행 계획**: 목적지, 여행 기간, 인원수, 여행 스타일, 예산 범위, 선호 활동 등 다양한 사용자 입력을 바탕으로 개인화된 여행 계획을 수립합니다.
*   **RAG (Retrieval Augmented Generation) 통합**: ChromaDB에 저장된 풍부한 여행 정보(예: 스위스 도시별 관광 정보, 일반 여행 팁)를 검색하여 LLM의 답변을 증강시킵니다. 이를 통해 LLM은 더욱 정확하고 상세한 컨텍스트 기반의 응답을 생성합니다.
*   **Multi-Agent Coordination**: `TravelCoordinatorAgent`가 각 여행 계획 단계(목적지 조사, 숙박, 음식, 교통, 액티비티, 예산 관리 등)를 조율하여 최적화된 일정을 생성합니다.
*   **동적 일정 생성**: 여행 기간에 따라 날짜가 동적으로 생성되어 실제 여행 일정을 시뮬레이션합니다.
*   **Streamlit UI**: 직관적이고 사용하기 쉬운 웹 인터페이스를 통해 여행 계획을 입력하고 결과를 시각적으로 확인합니다.
*   **Azure OpenAI 연동**: Azure OpenAI Service의 LLM (gpt-4o) 및 임베딩 모델 (text-embedding-3-large)을 활용하여 고품질의 AI 기능을 제공합니다.

## 🚀 시작하기

### 📋 1. 의존성 설치

프로젝트를 실행하기 전에 필요한 Python 패키지들을 설치합니다:

```bash
pip install -r requirements.txt
```

### 🔑 2. 환경 변수 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 환경 변수들을 설정합니다. Azure OpenAI 서비스에서 필요한 키와 엔드포인트 정보를 입력해야 합니다.

```dotenv
# Azure OpenAI 설정
AOAI_API_KEY="[YOUR_AZURE_OPENAI_API_KEY]"
AOAI_ENDPOINT="https://[YOUR_AZURE_OPENAI_RESOURCE_NAME].openai.azure.com/"
AOAI_DEPLOY_GPT4O="[YOUR_GPT4O_DEPLOYMENT_NAME]"
AOAI_API_VERSION="2024-05-01-preview" # 또는 현재 사용 중인 API 버전
AOAI_EMBEDDING_DEPLOYMENT="[YOUR_EMBEDDING_DEPLOYMENT_NAME]"

# Langfuse 설정 (선택 사항 - 사용하지 않을 경우 비워둡니다)
LANGFUSE_PUBLIC_KEY="[YOUR_LANGFUSE_PUBLIC_KEY]"
LANGFUSE_SECRET_KEY="[YOUR_LANGFUSE_SECRET_KEY]"
LANGFUSE_HOST="https://cloud.langfuse.com"

# 기타 설정
DEFAULT_TEMPERATURE="0.7"
MAX_TOKENS="2000"
```

**주의**: 
- `AOAI_ENDPOINT`는 반드시 `https://`로 시작하는 완전한 URL이어야 합니다.
- API 키가 설정되지 않으면 데모 모드로 동작합니다.
- API 키를 설정하면 AI 기반 개인화된 여행 계획을 받을 수 있습니다.

### 📊 3. ChromaDB 데이터 구축

RAG 기능을 위해 ChromaDB에 여행 정보를 임베딩하고 저장해야 합니다. 다음 스크립트를 실행하여 Vector DB를 구축합니다. 이 과정은 **한 번만 실행**하면 됩니다.

```bash
python ingest_data.py
```

성공적으로 완료되면 프로젝트 루트에 `./chroma_db` 디렉토리가 생성됩니다.

### ▶️ 4. 애플리케이션 실행

모든 설정과 데이터 구축이 완료되었다면, 다음 명령어를 사용하여 Streamlit 애플리케이션을 실행합니다.

```bash
python -m streamlit run main_multi_agent.py
```

명령어를 실행하면 로컬 URL이 터미널에 표시됩니다. 해당 URL을 웹 브라우저에 붙여넣어 AI 여행 플래너를 사용할 수 있습니다.

## 📁 프로젝트 폴더 구조

```
. # 프로젝트 루트
├── agents/              # Multi-Agent System 로직 (TravelCoordinatorAgent 등)
│   ├── __init__.py
│   └── coordinator.py
├── components/          # 사용자 입력, LLM 프롬프트/응답 처리 등 핵심 컴포넌트
│   ├── __init__.py
│   └── ...
├── config/              # 환경 설정 및 LLM/임베딩 모델 초기화
│   ├── __init__.py
│   └── config.py
├── data/                # RAG를 위한 원본 데이터 (travel_info.txt)
│   └── travel_info.txt
├── tools/               # Agent가 사용하는 외부 도구 정의
│   ├── __init__.py
│   └── ...
├── ui/                  # Streamlit UI 컴포넌트
│   ├── __init__.py
│   └── streamlit_ui.py
├── chroma_db/           # ChromaDB 데이터 저장 디렉토리
├── tests/               # 테스트 코드
├── 캡처/                # UI/결과 예시 이미지
├── main_multi_agent.py  # 멀티에이전트 메인 실행 파일
├── main.py              # 단일 에이전트 실행 파일
├── ingest_data.py       # ChromaDB 구축 스크립트
├── requirements.txt     # Python 의존성 목록
├── requirements_multi_agent.txt
├── .env                 # 환경 변수 설정 파일
└── README.md            # 프로젝트 설명 (현재 파일)
```

## 🎯 주요 기능

### 1. 사용자 입력 처리
- 목적지, 여행 기간, 인원수 입력
- 여행 스타일 및 예산 범위 선택
- 선호하는 활동, 음식, 교통수단 선택
- 추가 요구사항 입력

### 2. AI 여행 계획 생성
- OpenAI GPT 모델을 활용한 맞춤형 일정 생성
- Azure OpenAI 지원
- 시간대별 상세한 활동 계획
- 예산에 맞는 추천 장소 및 식당
- 교통수단 및 숙박 옵션 포함

### 3. 대안 일정 생성
- 저예산 버전
- 럭셔리 버전
- 느긋한 버전
- 모험 버전

### 4. 추가 정보 제공
- 목적지 날씨 정보
- 현지인만 아는 팁
- 숨겨진 명소 추천
- 예산 절약 팁

### 5. 시각화 및 분석
- 일정 분석 차트
- 활동 카테고리별 분포
- 일별 활동 수 그래프

## 🏗️ 아키텍처

```
[사용자 입력]
   ↓
[LLM 프롬프트 생성/입력 검증]
   ↓
[Multi-Agent 시스템 (여행 조율, 역할별 Agent)]
   ↓
[RAG: ChromaDB에서 정보 검색]
   ↓
[LLM 응답/후처리]
   ↓
[Streamlit UI 시각화]
```

## 🔧 주요 컴포넌트

*   **`main_multi_agent.py`**: 
    *   메인 Streamlit 애플리케이션 실행 파일. 
    *   사용자 입력 처리 및 여행 계획 생성 워크플로우를 조율합니다. 
    *   `TravelCoordinatorAgent` 및 UI 컴포넌트와 상호작용합니다.

*   **`agents/`**: 
    *   **`coordinator.py`**: `TravelCoordinatorAgent`를 포함하며, Multi-Agent System의 핵심 조율자 역할을 합니다. 사용자 요청을 기반으로 다양한 도구 및 RAG 시스템을 활용하여 여행 계획을 수립하고, LLM과 상호작용합니다.

*   **`config/`**: 
    *   **`config.py`**: 환경 변수(`AOAI_API_KEY`, `AOAI_ENDPOINT` 등)를 관리하고, LLM(`AzureChatOpenAI`) 및 임베딩 모델(`AzureOpenAIEmbeddings`) 인스턴스를 초기화하는 함수를 제공합니다.

*   **`tools/`**: 
    *   Agent가 특정 작업을 수행하는 데 사용하는 외부 도구들을 정의합니다. (예: 검색, 숙박, 음식, 교통, 예산 관련 도구)

*   **`data/`**: 
    *   **`travel_info.txt`**: RAG 시스템을 위한 원본 지식 기반 데이터를 포함합니다. 이 데이터는 임베딩되어 ChromaDB에 저장됩니다.

*   **`ingest_data.py`**: 
    *   `data/travel_info.txt` 파일을 읽고, 문서를 청킹하며, 임베딩하여 ChromaDB에 저장하는 스크립트입니다. RAG 시스템을 위한 Vector DB를 초기 구축하는 데 사용됩니다.

*   **`chroma_db/`**: 
    *   ChromaDB가 임베딩된 벡터 데이터와 원본 텍스트 청크를 저장하는 디렉토리입니다. RAG 검색 시 이 디렉토리의 데이터를 활용합니다.

*   **`tests/`**: 
    *   `tests/test_coordinator.py` 등에서 핵심 파싱/로직 테스트 가능
    *   `test_parsing.py`로 파싱 로직 단위 테스트 가능

*   **`캡처/`**: 
    *   UI/결과 예시 이미지

*   **`main.py`**: 
    *   단일 에이전트 실행 파일

## 🧪 테스트

- `tests/test_coordinator.py` 등에서 핵심 파싱/로직 테스트 가능
- `test_parsing.py`로 파싱 로직 단위 테스트 가능

## 🎨 UI 특징

- 반응형, 단계별 진행, 일차별 탭, 차트 시각화, 상세 정보 확장 등

## 🔒 보안/개인정보

- API 키는 .env로 관리, 사용자 입력은 세션 내 임시 저장

## 🛠️ 문제 해결

- `ModuleNotFoundError: No module named 'langchain_openai'` 등 패키지 에러 발생 시
  ```bash
  pip install langchain-openai
  ```
- 실행 중 에러 메시지는 복사해서 문의

## 📈 향후 개선/확장

- 실시간 API 연동, 모바일/PWA, 다국어, OAuth, 고급 분석 등은 `future_improvements.md` 참고

## 🛠️ 문제 해결

- `ModuleNotFoundError: No module named 'langchain_openai'` 등 패키지 에러 발생 시
  ```bash
  pip install langchain-openai
  ```
- 실행 중 에러 메시지는 복사해서 문의

## 📈 향후 개선/확장

- 실시간 API 연동, 모바일/PWA, 다국어, OAuth, 고급 분석 등은 `future_improvements.md` 참고

## 🛠️ 문제 해결

- `ModuleNotFoundError: No module named 'langchain_openai'` 등 패키지 에러 발생 시
  ```bash
  pip install langchain-openai
  ```
- 실행 중 에러 메시지는 복사해서 문의

## 📈 향후 개선/확장

- 실시간 API 연동, 모바일/PWA, 다국어, OAuth, 고급 분석 등은 `future_improvements.md` 참고

**문의/기여/피드백 환영! 즐거운 여행 되세요! ✈️**