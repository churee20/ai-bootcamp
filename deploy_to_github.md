# GitHub 업로드 가이드

## 🚀 GitHub에 프로젝트 업로드하기

### 방법 1: GitHub Desktop 사용 (권장)

1. **GitHub Desktop 설치**
   - https://desktop.github.com/ 에서 다운로드
   - 설치 후 GitHub 계정으로 로그인

2. **저장소 생성**
   - GitHub Desktop에서 "New Repository" 클릭
   - Repository name: `ai-bootcamp`
   - Description: `AI Travel Planner with Multi-Agent System and RAG`
   - Local path: 현재 프로젝트 폴더 선택
   - "Create Repository" 클릭

3. **파일 추가 및 커밋**
   - 모든 소스 코드 파일들이 자동으로 추가됨
   - Commit message: "Initial commit: AI Travel Planner"
   - "Commit to main" 클릭

4. **GitHub에 푸시**
   - "Publish repository" 클릭
   - Repository를 public으로 설정
   - "Publish Repository" 클릭

### 방법 2: GitHub CLI 사용

1. **GitHub CLI 설치**
   ```bash
   # Windows (with winget)
   winget install GitHub.cli
   
   # 또는 https://cli.github.com/ 에서 다운로드
   ```

2. **로그인 및 저장소 생성**
   ```bash
   gh auth login
   gh repo create ai-bootcamp --public --description "AI Travel Planner with Multi-Agent System and RAG"
   ```

3. **파일 추가 및 푸시**
   ```bash
   git add .
   git commit -m "Initial commit: AI Travel Planner"
   git push -u origin main
   ```

### 방법 3: 웹 브라우저에서 직접 업로드

1. **GitHub에서 새 저장소 생성**
   - https://github.com/new 접속
   - Repository name: `ai-bootcamp`
   - Description: `AI Travel Planner with Multi-Agent System and RAG`
   - Public 선택
   - "Create repository" 클릭

2. **파일 업로드**
   - "uploading an existing file" 클릭
   - 프로젝트 폴더의 모든 파일을 드래그 앤 드롭
   - Commit message 입력
   - "Commit changes" 클릭

## 📁 업로드할 파일 목록

### 핵심 파일들
- `main_multi_agent.py` - 메인 애플리케이션
- `main.py` - 기본 버전
- `requirements_multi_agent.txt` - 의존성 목록
- `requirements.txt` - 기본 의존성
- `README.md` - 프로젝트 문서
- `setup_instructions.md` - 설정 가이드
- `.gitignore` - Git 제외 파일 목록

### 디렉토리들
- `agents/` - Multi-Agent 시스템
- `tools/` - ReAct 도구들
- `config/` - 설정 파일들
- `components/` - UI 컴포넌트
- `ui/` - Streamlit UI
- `data/` - RAG 데이터
- `tests/` - 테스트 파일들

### 문서 파일들
- `Agent.md` - Agent 설명
- `rag.md` - RAG 시스템 설명
- `user_flow_diagram.py` - 플로우 다이어그램 생성기
- `ingest_data.py` - RAG 데이터 수집
- `test_parsing.py` - 파싱 테스트

### 제외할 파일들 (자동으로 제외됨)
- `.venv/` - 가상환경
- `chroma_db/` - 벡터 데이터베이스
- `__pycache__/` - Python 캐시
- `.env` - 환경 변수 (보안상 제외)

## 🔧 업로드 후 설정

### 1. 저장소 설정
- README.md가 자동으로 표시됨
- Topics 추가: `ai`, `travel`, `streamlit`, `langchain`, `rag`, `multi-agent`

### 2. 환경 변수 설정 (로컬에서)
```bash
# .env 파일 생성
echo "AOAI_API_KEY=your_key_here" > .env
echo "AOAI_ENDPOINT=your_endpoint_here" >> .env
# ... 기타 설정
```

### 3. 의존성 설치
```bash
pip install -r requirements_multi_agent.txt
```

### 4. 애플리케이션 실행
```bash
python -m streamlit run main_multi_agent.py
```

## 📝 저장소 설명

### 프로젝트 개요
AI 여행 플래너는 Multi-Agent System과 RAG(Retrieval-Augmented Generation) 기술을 활용하여 사용자 맞춤형 여행 계획을 수립하는 애플리케이션입니다.

### 주요 기능
- 🤖 Multi-Agent System: 7개의 전문 Agent가 협력
- 🔍 RAG 시스템: ChromaDB와 Azure OpenAI 임베딩
- 🌐 Streamlit UI: 사용자 친화적인 웹 인터페이스
- 🎯 맞춤형 계획: 개인 선호도 기반 여행 계획
- 📊 실시간 진행: 단계별 진행 상황 표시

### 기술 스택
- **AI/ML**: Azure OpenAI, LangChain, ChromaDB
- **Web Framework**: Streamlit
- **Language**: Python 3.8+
- **Architecture**: Multi-Agent System, RAG

### 사용 방법
1. 저장소 클론
2. 가상환경 생성 및 의존성 설치
3. API 키 설정 (.env 파일)
4. 애플리케이션 실행
5. 여행 정보 입력 및 계획 생성

## 🎯 다음 단계

업로드 완료 후:
1. README.md 업데이트
2. Issues 템플릿 생성
3. GitHub Actions 워크플로우 설정 (선택사항)
4. 프로젝트 위키 생성 (선택사항)
5. 릴리즈 노트 작성

## 📞 지원

문제가 발생하면:
1. GitHub Issues에서 검색
2. 새로운 Issue 생성
3. README.md의 트러블슈팅 섹션 참조 