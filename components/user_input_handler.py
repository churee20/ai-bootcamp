import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Any

class UserInputHandler:
    """사용자 입력 처리 클래스"""
    
    def __init__(self):
        # 세션 상태에서 입력 데이터 초기화
        if 'user_input_data' not in st.session_state:
            st.session_state.user_input_data = {}
    
    def collect_travel_preferences(self) -> Dict[str, Any]:
        """사용자로부터 여행 선호사항을 수집"""
        
        st.header("🎯 여행 선호사항 입력")
        
        # 기본 정보
        col1, col2 = st.columns(2)
        
        with col1:
            destination = st.text_input("목적지", placeholder="예: 파리, 프랑스", key="input_destination")
            travel_style = st.selectbox(
                "여행 스타일",
                ["휴식 위주", "문화 탐방", "액티비티", "맛집 탐방", "쇼핑", "혼합"],
                key="input_travel_style"
            )
            budget_range = st.selectbox(
                "예산 범위",
                ["저예산 (50만원 이하)", "보통 (50-100만원)", "고급 (100-200만원)", "럭셔리 (200만원 이상)"],
                key="input_budget_range"
            )
        
        with col2:
            duration = st.number_input("여행 기간 (일)", min_value=1, max_value=30, value=5, key="input_duration")
            group_size = st.number_input("인원수", min_value=1, max_value=10, value=2, key="input_group_size")
            accommodation_type = st.selectbox(
                "숙박 유형",
                ["호텔", "게스트하우스", "에어비앤비", "호스텔", "리조트", "상관없음"],
                key="input_accommodation_type"
            )
        
        # 상세 선호사항
        st.subheader("상세 선호사항")
        
        col3, col4 = st.columns(2)
        
        with col3:
            activities = st.multiselect(
                "선호하는 활동",
                ["박물관/미술관", "자연 관광", "쇼핑", "맛집 탐방", "야외 활동", 
                 "역사 유적지", "테마파크", "스파/마사지", "야간 엔터테인먼트"],
                default=["맛집 탐방", "박물관/미술관"],
                key="input_activities"
            )
            
            food_preferences = st.multiselect(
                "음식 선호사항",
                ["현지 음식", "한식", "양식", "채식", "해산물", "스테이크", "디저트"],
                default=["현지 음식"],
                key="input_food_preferences"
            )
        
        with col4:
            transportation = st.multiselect(
                "교통수단 선호",
                ["대중교통", "렌터카", "택시", "도보", "자전거", "관광버스"],
                default=["대중교통", "도보"],
                key="input_transportation"
            )
            
            pace = st.select_slider(
                "여행 페이스",
                options=["느긋하게", "보통", "빠르게"],
                value="보통",
                key="input_pace"
            )
        
        # 추가 요구사항
        additional_notes = st.text_area(
            "추가 요구사항이나 특별한 선호사항",
            placeholder="예: 반려동물 동반, 장애인 편의시설 필요, 특정 축제 참여 등",
            key="input_additional_notes"
        )
        
        # 입력 데이터를 세션 상태에 저장
        st.session_state.user_input_data = {
            "destination": destination,
            "travel_style": travel_style,
            "budget_range": budget_range,
            "duration": duration,
            "group_size": group_size,
            "accommodation_type": accommodation_type,
            "activities": activities,
            "food_preferences": food_preferences,
            "transportation": transportation,
            "pace": pace,
            "additional_notes": additional_notes
        }
        
        return st.session_state.user_input_data
    
    def validate_input(self) -> bool:
        """입력 데이터 유효성 검사"""
        data = st.session_state.user_input_data
        
        if not data.get("destination"):
            st.error("목적지를 입력해주세요.")
            return False
        
        if not data.get("activities"):
            st.error("최소 하나의 활동을 선택해주세요.")
            return False
        
        return True
    
    def get_input_summary(self) -> str:
        """입력 데이터 요약 반환"""
        data = st.session_state.user_input_data
        
        # 빈 값 처리
        destination = data.get('destination', 'N/A') if data.get('destination') else 'N/A'
        duration = data.get('duration', 'N/A') if data.get('duration') else 'N/A'
        group_size = data.get('group_size', 'N/A') if data.get('group_size') else 'N/A'
        travel_style = data.get('travel_style', 'N/A') if data.get('travel_style') else 'N/A'
        budget_range = data.get('budget_range', 'N/A') if data.get('budget_range') else 'N/A'
        accommodation_type = data.get('accommodation_type', 'N/A') if data.get('accommodation_type') else 'N/A'
        activities = ', '.join(data.get('activities', [])) if data.get('activities') else 'N/A'
        food_preferences = ', '.join(data.get('food_preferences', [])) if data.get('food_preferences') else 'N/A'
        transportation = ', '.join(data.get('transportation', [])) if data.get('transportation') else 'N/A'
        pace = data.get('pace', 'N/A') if data.get('pace') else 'N/A'
        
        summary = f"""
        **여행 정보 요약:**
        - 목적지: {destination}
        - 여행 기간: {duration}일
        - 인원수: {group_size}명
        - 여행 스타일: {travel_style}
        - 예산 범위: {budget_range}
        - 숙박 유형: {accommodation_type}
        - 선호 활동: {activities}
        - 음식 선호: {food_preferences}
        - 교통수단: {transportation}
        - 여행 페이스: {pace}
        """
        
        if data.get('additional_notes'):
            summary += f"\n- 추가 요구사항: {data.get('additional_notes')}"
        
        return summary 