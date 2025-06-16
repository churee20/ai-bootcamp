"""
AI 여행 플래너 - Multi Agent System with LangChain & LangGraph
"""
import streamlit as st
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.schema import BaseMessage
from langchain.agents import initialize_agent, AgentType
import json
from datetime import date, timedelta # Moved from inside functions

# 기존 컴포넌트 import
from components.user_input_handler import UserInputHandler
from ui.streamlit_ui import StreamlitUI

# 새로운 Multi Agent System import
from agents import TravelCoordinatorAgent
from tools import (
    SearchDestinationTool, WeatherTool, AccommodationSearchTool,
    RestaurantSearchTool, TransportationTool, BudgetCalculatorTool,
    ItineraryOptimizerTool
)

class MultiAgentTravelPlanner:
    """Multi Agent 기반 여행 플래너"""
    
    def __init__(self):
        self.ui = StreamlitUI()
        self.input_handler = UserInputHandler()
        self.llm = self._initialize_llm()
        self.tools = self._initialize_tools()
        # RAG 활성화를 위해 vectorstore 파라미터 제거
        self.coordinator_agent = TravelCoordinatorAgent(self.llm, self.tools)
        
        # 세션 상태 초기화
        if 'travel_data' not in st.session_state:
            st.session_state.travel_data = None
        if 'processed_data' not in st.session_state:
            st.session_state.processed_data = None
        if 'agent_conversation' not in st.session_state:
            st.session_state.agent_conversation = []
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 'input'  # 'input', 'planning', 'results'
        if 'user_input_data' not in st.session_state:
            st.session_state.user_input_data = {}
    
    def _initialize_llm(self):
        """LLM 초기화"""
        try:
            # Azure OpenAI 우선 시도 (ChatOpenAI 사용)
            import config.config as config
            
            # Azure OpenAI 설정이 유효한지 확인
            if config.has_valid_azure_openai_config():
                return AzureChatOpenAI(
                    azure_endpoint=config.AOAI_ENDPOINT,
                    azure_deployment=config.AOAI_DEPLOY_GPT4O,
                    openai_api_version=config.AOAI_API_VERSION,
                    temperature=0.7,
                    api_key=config.AOAI_API_KEY
                )
            
            # OpenAI API 시도
            if config.has_valid_openai_config():
                return ChatOpenAI(
                    model=config.OPENAI_MODEL,
                    temperature=0.7,
                    api_key=config.OPENAI_API_KEY
                )
            
            # API 키가 없는 경우 데모 모드로 동작
            st.info("🤖 API 키가 설정되지 않아 데모 모드로 동작합니다.")
            return None
            
        except Exception as e:
            st.warning(f"⚠️ LLM 초기화 실패: {str(e)}")
            st.info("💡 데모 모드로 동작합니다.")
            return None
    
    def _initialize_tools(self):
        """ReAct Tools 초기화"""
        return [
            SearchDestinationTool(),
            WeatherTool(),
            AccommodationSearchTool(),
            RestaurantSearchTool(),
            TransportationTool(),
            BudgetCalculatorTool(),
            ItineraryOptimizerTool()
        ]
    
    def run(self):
        """메인 실행 함수"""
        
        # UI 헤더 표시
        self.ui.display_header()
        
        # 사이드바에 설정 정보 표시
        self._display_sidebar()
        
        # 메인 컨텐츠
        self._main_content()
    
    def _display_sidebar(self):
        """사이드바 표시"""
        with st.sidebar:
            st.header("🤖 Multi Agent System")
            
            # 진행 단계 표시
            st.subheader("📋 진행 단계")
            steps = {
                'input': '1️⃣ 여행 정보 입력',
                'planning': '2️⃣ Agent 계획 수립',
                'results': '3️⃣ 결과 확인'
            }
            
            for step, label in steps.items():
                if st.session_state.current_step == step:
                    st.markdown(f"**{label}** ✅")
                else:
                    st.markdown(f"{label}")
            
            st.markdown("---")
            
            # Agent 상태 표시
            if self.llm:
                st.success("✅ LLM 연결됨")
                st.info("🤖 Multi Agent System 활성화")
            else:
                st.warning("⚠️ LLM 연결 실패")
                st.info("💡 API 키 설정 방법:")
                st.markdown("""
                1. Azure OpenAI 서비스에서 API 키 발급
                2. 프로젝트 루트에 `.env` 파일 생성
                3. 다음 정보 입력:
                   ```
                   AOAI_API_KEY="your_api_key"
                   AOAI_ENDPOINT="https://your-resource.openai.azure.com/"
                   AOAI_DEPLOY_GPT4O="your_deployment"
                   ```
                4. 애플리케이션 재시작
                """)
            
            st.markdown("---")
            
            # Agent 정보
            st.header("🎯 Agent 구성")
            st.markdown("""
            - **Travel Coordinator**: 메인 조율자
            - **Destination Researcher**: 목적지 조사
            - **Accommodation Agent**: 숙박 전문
            - **Food & Dining Agent**: 음식 전문
            - **Transportation Agent**: 교통 전문
            - **Activity Planner**: 액티비티 계획
            - **Budget Manager**: 예산 관리
            """)
            
            st.markdown("---")
            
            # 사용법 안내
            st.header("📖 사용법")
            st.markdown("""
            1. 여행 선호사항을 입력하세요
            2. '🤖 Multi Agent 실행' 버튼을 클릭하세요
            3. Multi Agent가 협력하여 일정을 만듭니다
            4. Agent들의 대화 과정을 확인할 수 있습니다
            """)
            
            st.markdown("---")
            
            # 초기화 버튼
            if st.button("🔄 새로 시작"):
                self._reset_session()
                st.rerun()
    
    def _main_content(self):
        """메인 컨텐츠 처리"""
        
        # 현재 단계에 따라 다른 화면 표시
        if st.session_state.current_step == 'input':
            self._handle_user_input()
        elif st.session_state.current_step == 'planning':
            self._handle_multi_agent_planning()
        elif st.session_state.current_step == 'results':
            self._handle_results_display()
    
    def _handle_user_input(self):
        """사용자 입력 처리"""
        
        st.header("🎯 1단계: 여행 정보 입력")
        st.markdown("여행하고 싶은 목적지와 선호사항을 입력해주세요.")
        
        # 사용자 입력 수집
        travel_data = self.input_handler.collect_travel_preferences()
        
        # 입력 검증
        if self.input_handler.validate_input():
            st.session_state.travel_data = travel_data
            
            # 입력 요약 표시
            summary = self.input_handler.get_input_summary()
            self.ui.display_input_summary(summary)
            
            # Multi Agent 실행 버튼
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🤖 Multi Agent 실행", type="primary", use_container_width=True):
                    st.session_state.current_step = 'planning'
                    st.rerun()
    
    def _handle_multi_agent_planning(self):
        """Multi Agent 여행 계획 생성"""
        
        st.header("🤖 2단계: Multi Agent 계획 수립")
        
        if not st.session_state.travel_data:
            st.error("여행 데이터가 없습니다.")
            st.button("← 이전 단계로", on_click=self._go_back_to_input)
            return
        
        # 입력 요약 표시
        summary = self.input_handler.get_input_summary()
        self.ui.display_input_summary(summary)
        
        # Agent 대화 과정 표시
        st.subheader("🤖 Agent 협력 과정")
        
        # 진행 상태 표시
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 단계별 진행 상황 표시
        steps = [
            "🔍 목적지 정보 수집 중...",
            "🌤️ 날씨 정보 확인 중...",
            "🏨 숙박 옵션 검색 중...",
            "🍽️ 음식점 추천 중...",
            "🚗 교통 계획 수립 중...",
            "🎪 액티비티 계획 중...",
            "💰 예산 최적화 중...",
            "📋 최종 일정 정리 중..."
        ]
        
        for i, step in enumerate(steps):
            status_text.text(step)
            progress_bar.progress((i + 1) / len(steps))
            st.empty()  # 잠시 대기 효과
        
        # Coordinator Agent 실행
        with st.spinner("Multi Agent들이 여행 계획을 수립하고 있습니다..."):
            result = self.coordinator_agent.plan_travel(st.session_state.travel_data)
            
            if result and result.get('status') != 'error':
                st.session_state.processed_data = result
                st.success("✅ Multi Agent 여행 계획이 완성되었습니다!")
                
                # 다음 단계로 이동 버튼
                if st.button("📋 결과 확인하기", type="primary"):
                    st.session_state.current_step = 'results'
                    st.rerun()
            else:
                st.error("여행 계획 생성에 실패했습니다.")
                if result and result.get('type') == 'error':
                    st.error(f"오류: {result.get('message', '알 수 없는 오류')}")
                st.button("← 이전 단계로", on_click=self._go_back_to_input)
    
    def _handle_results_display(self):
        """결과 표시 및 추가 기능 처리"""
        
        st.header("📋 3단계: 여행 계획 결과")
        
        if not st.session_state.processed_data:
            st.error("처리된 데이터가 없습니다.")
            st.button("← 이전 단계로", on_click=self._go_back_to_planning)
            return
        
        data = st.session_state.processed_data
        
        # 입력 요약 표시
        summary = self.input_handler.get_input_summary()
        self.ui.display_input_summary(summary)
        
        # 텍스트 기반 응답 처리
        if data.get('type') == 'text_response':
            st.subheader("🤖 Multi Agent 여행 계획")
            
            # Agent 응답 내용 표시
            content = data.get('content', '응답 내용이 없습니다.')
            
            # "Final Answer:" 부분이 있으면 제거하고 깔끔하게 표시
            if "Final Answer:" in content:
                content = content.split("Final Answer:")[-1].strip()
            
            # 마크다운으로 표시 (전체 내용을 표시)
            st.markdown(content)
            
            # Tool 실행 결과 분석 및 표시
            if "Action:" in data.get('content', ''):
                st.markdown("---")
                st.subheader("🔧 Tool 실행 결과")
                
                # Tool 실행 과정 표시
                tool_content = data.get('content', '')
                if "Action:" in tool_content:
                    st.info("🤖 Agent가 다음 도구들을 사용했습니다:")
                    
                    # Tool 사용 목록 추출
                    import re
                    actions = re.findall(r'Action: (\w+)', tool_content)
                    if actions:
                        for i, action in enumerate(actions, 1):
                            st.markdown(f"{i}. **{action}**")
                    
                    # Tool 실행 결과가 있는지 확인
                    if "Observation:" in tool_content:
                        st.success("✅ 도구들이 성공적으로 실행되었습니다.")
                    else:
                        st.warning("⚠️ 도구 실행이 완료되지 않았습니다.")
            
            # 성공 메시지 표시
            if data.get('status') == 'success':
                st.success(data.get('message', '여행 계획이 성공적으로 생성되었습니다!'))
        
        # 에러 응답 처리
        elif data.get('type') == 'error':
            st.error(f"오류 발생: {data.get('message', '알 수 없는 오류')}")
            st.text_area("원본 응답:", data.get('content', ''), height=200)
        
        # 기존 JSON 형식 응답 처리 (하위 호환성)
        else:
            # Agent 분석 결과 표시
            if data.get('agent_analysis'):
                st.subheader("🤖 Agent 분석 결과")
                st.markdown(data['agent_analysis'])
                st.markdown("---")
            
            # 여행 일정 표시
            if data.get('itinerary'):
                st.subheader("📅 여행 일정")
                self.ui.display_itinerary(data['itinerary'])
                
                # 일정 요약 정보 표시
                st.markdown("---")
                st.subheader("📋 일정 요약")
                total_days = len(data['itinerary'])
                total_activities = sum(len(day.get('activities', [])) for day in data['itinerary'])
                total_meals = sum(len(day.get('meals', [])) for day in data['itinerary'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("총 여행 일수", f"{total_days}일")
                with col2:
                    st.metric("총 활동 수", f"{total_activities}개")
                with col3:
                    st.metric("총 식사 수", f"{total_meals}회")
            
            # 추천사항 표시
            if data.get('recommendations'):
                st.subheader("💡 추천사항")
                self.ui.display_recommendations(data['recommendations'])
            
            # 비용 요약 표시
            if data.get('total_estimated_cost'):
                st.subheader("💰 비용 요약")
                self.ui.display_cost_summary(data['total_estimated_cost'])
            
            # 준비물 목록 표시
            if data.get('packing_list'):
                st.subheader("🎒 준비물 목록")
                self.ui.display_packing_list(data['packing_list'])
            
            # 일정 분석 차트 표시
            if data.get('itinerary'):
                st.subheader("📊 일정 분석")
                self.ui.display_itinerary_chart(data['itinerary'])
            
            # 데이터 품질 정보 표시
            st.markdown("---")
            st.subheader("📈 데이터 품질")
            
            quality_metrics = []
            if data.get('itinerary'):
                quality_metrics.append("✅ 여행 일정")
            if data.get('recommendations'):
                quality_metrics.append("✅ 추천사항")
            if data.get('total_estimated_cost'):
                quality_metrics.append("✅ 비용 정보")
            if data.get('packing_list'):
                quality_metrics.append("✅ 준비물 목록")
            if data.get('agent_analysis'):
                quality_metrics.append("✅ Agent 분석")
            
            if quality_metrics:
                st.success("다음 정보들이 포함된 완전한 여행 계획입니다:")
                for metric in quality_metrics:
                    st.markdown(f"• {metric}")
            else:
                st.warning("기본적인 여행 계획 정보만 포함되어 있습니다.")
    
    def _go_back_to_input(self):
        """입력 단계로 돌아가기"""
        st.session_state.current_step = 'input'
    
    def _go_back_to_planning(self):
        """계획 단계로 돌아가기"""
        st.session_state.current_step = 'planning'
    
    def _reset_session(self):
        """세션 상태 초기화"""
        st.session_state.travel_data = None
        st.session_state.processed_data = None
        st.session_state.agent_conversation = []
        st.session_state.current_step = 'input'
        st.session_state.user_input_data = {}

def main():
    """메인 함수"""
    
    # Multi Agent 여행 플래너 실행
    planner = MultiAgentTravelPlanner()
    planner.run()

if __name__ == "__main__":
    main() 