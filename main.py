import streamlit as st
from typing import Dict, Any

# 컴포넌트 import - 직접 import (__init__.py 사용하지 않음)
from components.user_input_handler import UserInputHandler
from components.llm_prompt_generator import LLMPromptGenerator
from components.llm_client import LLMClient
from components.llm_response_processor import LLMResponseProcessor
from ui.streamlit_ui import StreamlitUI

class TravelPlannerAgent:
    """AI 여행 플래너 Agent 메인 클래스"""
    
    def __init__(self):
        self.ui = StreamlitUI()
        self.input_handler = UserInputHandler()
        self.prompt_generator = LLMPromptGenerator()
        self.llm_client = LLMClient()
        self.response_processor = LLMResponseProcessor()
        
        # 세션 상태 초기화
        if 'travel_data' not in st.session_state:
            st.session_state.travel_data = None
        if 'processed_data' not in st.session_state:
            st.session_state.processed_data = None
    
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
            st.header("⚙️ 설정")
            
            # API 상태 확인
            api_status = self.llm_client.get_api_status()
            
            if api_status["connected"]:
                if api_status["azure_connected"]:
                    st.success("✅ Azure OpenAI 연결됨")
                    st.info(f"🤖 모델: {api_status['model']}")
                else:
                    st.success("✅ OpenAI API 연결됨")
                    st.info(f"🤖 모델: {api_status['model']}")
                
                if api_status["langfuse_connected"]:
                    st.info("📊 Langfuse 연결됨")
            else:
                if api_status["azure_api_key_set"] or api_status["openai_api_key_set"]:
                    st.error("❌ API 연결 실패")
                    st.info("💡 API 키를 확인해주세요.")
                else:
                    st.warning("⚠️ API 키 미설정")
                    st.info("💡 `.env` 파일에 API 키를 설정하면 AI 기능을 사용할 수 있습니다.")
            
            st.markdown("---")
            
            # 사용법 안내
            st.header("📖 사용법")
            st.markdown("""
            1. 여행 선호사항을 입력하세요
            2. '여행 계획 생성' 버튼을 클릭하세요
            3. AI가 맞춤형 일정을 만들어드립니다
            4. 필요시 대안 일정을 요청할 수 있습니다
            """)
            
            st.markdown("---")
            
            # 초기화 버튼
            if st.button("🔄 새로 시작"):
                self._reset_session()
                st.rerun()
    
    def _main_content(self):
        """메인 컨텐츠 처리"""
        
        # 1단계: 사용자 입력 수집
        if not st.session_state.travel_data:
            self._handle_user_input()
        
        # 2단계: 입력 확인 및 여행 계획 생성
        elif not st.session_state.processed_data:
            self._handle_travel_plan_generation()
        
        # 3단계: 결과 표시 및 추가 기능
        else:
            self._handle_results_display()
    
    def _handle_user_input(self):
        """사용자 입력 처리"""
        
        # 사용자 입력 수집
        travel_data = self.input_handler.collect_travel_preferences()
        
        # 입력 검증
        if self.input_handler.validate_input():
            st.session_state.travel_data = travel_data
            
            # 입력 요약 표시
            summary = self.input_handler.get_input_summary()
            self.ui.display_input_summary(summary)
            
            # 여행 계획 생성 버튼
            if st.button("🚀 여행 계획 생성", type="primary"):
                st.rerun()
    
    def _handle_travel_plan_generation(self):
        """여행 계획 생성 처리"""
        
        if not st.session_state.travel_data:
            st.error("여행 데이터가 없습니다.")
            return
        
        # 입력 요약 표시
        summary = self.input_handler.get_input_summary()
        self.ui.display_input_summary(summary)
        
        # LLM 클라이언트 확인
        if not self.llm_client.is_available():
            st.warning("⚠️ OpenAI API가 연결되지 않아 AI 기능을 사용할 수 없습니다.")
            st.info("💡 `.env` 파일에 유효한 OpenAI API 키를 설정해주세요.")
            
            # 데모 데이터로 일정 표시
            if st.button("🎭 데모 일정 보기"):
                self._show_demo_itinerary()
            return
        
        # 프롬프트 생성
        prompt = self.prompt_generator.generate_travel_prompt(st.session_state.travel_data)
        
        # LLM 응답 생성
        llm_response = self.llm_client.generate_travel_plan(prompt)
        
        if llm_response:
            # 응답 처리
            processed_data = self.response_processor.process_llm_response(llm_response)
            st.session_state.processed_data = processed_data
            
            # 성공 메시지
            self.ui.display_success("여행 계획이 성공적으로 생성되었습니다!")
            
            # 결과 표시
            st.rerun()
        else:
            st.error("여행 계획 생성에 실패했습니다.")
    
    def _show_demo_itinerary(self):
        """데모 일정 표시"""
        demo_data = {
            "itinerary": [
                {
                    "day": 1,
                    "date": "2024-01-15",
                    "activities": [
                        {
                            "time": "09:00-11:00",
                            "activity": "에펠탑 방문",
                            "location": "파리, 프랑스",
                            "description": "파리의 상징적인 랜드마크를 방문하여 도시의 아름다운 전경을 감상합니다.",
                            "cost": "€26",
                            "transportation": "지하철",
                            "category": "문화"
                        },
                        {
                            "time": "12:00-13:30",
                            "activity": "현지 레스토랑에서 점심",
                            "location": "몽마르트르",
                            "description": "전통적인 프랑스 요리를 맛볼 수 있는 현지 레스토랑에서 식사합니다.",
                            "cost": "€35",
                            "transportation": "도보",
                            "category": "음식"
                        }
                    ],
                    "meals": [
                        {
                            "time": "12:00-13:30",
                            "restaurant": "Le Bistrot Parisien",
                            "cuisine": "프랑스 전통 요리",
                            "cost": "€35",
                            "notes": "현지인들이 즐겨가는 맛집",
                            "meal_type": "점심"
                        }
                    ],
                    "accommodation": {
                        "name": "Hotel de Paris",
                        "type": "호텔",
                        "cost": "€120",
                        "notes": "시내 중심가에 위치한 편리한 호텔"
                    },
                    "summary": "Day 1: 2개 활동, 1회 식사"
                }
            ],
            "recommendations": {
                "must_visit": ["루브르 박물관", "노트르담 대성당", "샹젤리제 거리"],
                "hidden_gems": ["몽마르트르 언덕", "생제르맹 데 프레", "라틴 구역"],
                "local_tips": ["지하철을 이용하면 편리합니다", "식사 시간을 피해 관광지를 방문하세요"],
                "budget_tips": ["박물관 패스를 구매하면 할인됩니다", "현지 마켓에서 식재료를 구매하세요"]
            },
            "total_estimated_cost": "€500",
            "packing_list": ["여권", "카메라", "편한 신발", "우산", "어댑터"]
        }
        
        st.session_state.processed_data = demo_data
        st.success("🎭 데모 일정이 표시됩니다!")
        st.rerun()
    
    def _handle_results_display(self):
        """결과 표시 및 추가 기능 처리"""
        
        if not st.session_state.processed_data:
            st.error("처리된 데이터가 없습니다.")
            return
        
        data = st.session_state.processed_data
        
        # 입력 요약 표시
        summary = self.input_handler.get_input_summary()
        self.ui.display_input_summary(summary)
        
        # 여행 일정 표시
        if data.get('itinerary'):
            self.ui.display_itinerary(data['itinerary'])
        
        # 추천사항 표시
        if data.get('recommendations'):
            self.ui.display_recommendations(data['recommendations'])
        
        # 비용 요약 표시
        if data.get('total_estimated_cost'):
            self.ui.display_cost_summary(data['total_estimated_cost'])
        
        # 준비물 목록 표시
        if data.get('packing_list'):
            self.ui.display_packing_list(data['packing_list'])
        
        # 일정 분석 차트 표시
        if data.get('itinerary'):
            self.ui.display_itinerary_chart(data['itinerary'])
        
        # 대안 일정 생성 옵션 (API가 연결된 경우에만)
        if self.llm_client.is_available():
            alternative_buttons = self.ui.display_alternative_options()
            self._handle_alternative_requests(alternative_buttons)
            
            # 추가 정보 버튼
            additional_buttons = self.ui.display_additional_info_buttons()
            self._handle_additional_info_requests(additional_buttons)
        else:
            st.info("💡 API 키를 설정하면 대안 일정 생성과 추가 정보 조회가 가능합니다.")
        
        # 내보내기 옵션
        self.ui.display_export_options(data)
    
    def _handle_alternative_requests(self, buttons: Dict[str, bool]):
        """대안 일정 요청 처리"""
        
        for alternative_type, clicked in buttons.items():
            if clicked:
                self._generate_alternative_plan(alternative_type)
                break
    
    def _generate_alternative_plan(self, alternative_type: str):
        """대안 계획 생성"""
        
        if not st.session_state.travel_data:
            st.error("여행 데이터가 없습니다.")
            return
        
        # 대안 프롬프트 생성
        prompt = self.prompt_generator.generate_alternative_prompt(
            st.session_state.travel_data, 
            alternative_type
        )
        
        # LLM 응답 생성
        llm_response = self.llm_client.generate_alternative_plan(prompt, alternative_type)
        
        if llm_response:
            # 응답 처리
            processed_data = self.response_processor.process_llm_response(llm_response)
            
            # 대안 데이터를 세션에 저장
            st.session_state.processed_data = processed_data
            
            # 성공 메시지
            alternative_names = {
                "budget": "저예산",
                "luxury": "럭셔리",
                "relaxed": "느긋한",
                "adventure": "모험"
            }
            self.ui.display_success(f"{alternative_names.get(alternative_type, alternative_type)} 버전의 일정이 생성되었습니다!")
            
            # 결과 표시
            st.rerun()
        else:
            st.error("대안 계획 생성에 실패했습니다.")
    
    def _handle_additional_info_requests(self, buttons: Dict[str, bool]):
        """추가 정보 요청 처리"""
        
        for info_type, clicked in buttons.items():
            if clicked:
                self._get_additional_info(info_type)
                break
    
    def _get_additional_info(self, info_type: str):
        """추가 정보 조회"""
        
        if not st.session_state.travel_data:
            st.error("여행 데이터가 없습니다.")
            return
        
        destination = st.session_state.travel_data.get('destination', '')
        duration = st.session_state.travel_data.get('duration', 1)
        
        if info_type == "weather":
            weather_info = self.llm_client.get_weather_info(destination, duration)
            if weather_info:
                self.ui.display_weather_info(weather_info)
        
        elif info_type == "local_tips":
            local_tips = self.llm_client.get_local_tips(destination)
            if local_tips:
                self.ui.display_local_tips(local_tips)
    
    def _reset_session(self):
        """세션 상태 초기화"""
        st.session_state.travel_data = None
        st.session_state.processed_data = None

def main():
    """메인 함수"""
    
    # AI 여행 플래너 Agent 실행
    agent = TravelPlannerAgent()
    agent.run()

if __name__ == "__main__":
    main() 