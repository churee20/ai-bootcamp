# 각 Agent가 사용할 Tools
- SearchDestinationTool: 목적지 정보 검색
- WeatherTool: 날씨 정보 조회
- AccommodationSearchTool: 숙박 시설 검색
- RestaurantSearchTool: 식당 검색
- TransportationTool: 교통 정보 조회
- BudgetCalculatorTool: 예산 계산
- ItineraryOptimizerTool: 일정 최적화

Agent 역할 분담
🤖 Travel Coordinator Agent (메인 코디네이터)
├── 🎯 Destination Research Agent (목적지 조사)
├── 🏨 Accommodation Agent (숙박 전문)
├── 🍽️ Food & Dining Agent (음식 전문)
├── 🚗 Transportation Agent (교통 전문)
├── 🎪 Activity Planner Agent (액티비티 계획)
└── 💰 Budget Manager Agent (예산 관리)

전체 여행 계획 조율
다른 Agent들과의 협력 관리
최종 결과 통합

목적지 기본 정보 수집
관광지, 문화, 언어 정보

호텔, 게스트하우스 검색
예약 가능성 확인
가격 비교

레스토랑, 카페 추천
현지 음식 정보
예약 및 가격 정보

교통수단 정보
경로 최적화
비용 계산

관광지 일정 계획
액티비티 추천
시간 최적화

전체 예산 관리
카테고리별 비용 분배
절약 방안 제시
🔧 ReAct Tools 구성
SearchDestinationTool: 목적지 정보 검색
WeatherTool: 날씨 정보 조회
AccommodationSearchTool: 숙박 시설 검색
RestaurantSearchTool: 식당 검색
TransportationTool: 교통 정보 조회
BudgetCalculatorTool: 예산 계산
ItineraryOptimizerTool: 일정 최적화
🚀 실행 방법
Apply to README.md
Run
# 의존성 설치
pip install -r requirements_multi_agent.txt

# Multi Agent 버전 실행
python -m streamlit run main_multi_agent.py
🔄 다음 단계
LangGraph 적용: Agent 간 워크플로우 정의
실제 API 연동: 외부 서비스와의 연동
대화형 Agent: 사용자와의 실시간 대화
학습 기능: 사용자 피드백을 통한 개선
이제 main_multi_agent.py를 실행하여 Multi Agent 시스템을 테스트해보세요! 🎯