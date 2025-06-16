import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Dict, Any, List
from datetime import datetime

class StreamlitUI:
    """Streamlit UI 출력 클래스"""
    
    def __init__(self):
        self.setup_page_config()
    
    def setup_page_config(self):
        """페이지 설정"""
        st.set_page_config(
            page_title="AI 여행 플래너",
            page_icon="✈️",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def display_header(self):
        """헤더 표시"""
        st.title("✈️ AI 여행 플래너")
        st.markdown("---")
        st.markdown("**AI가 당신만을 위한 맞춤형 여행 계획을 만들어드립니다!**")
    
    def display_input_summary(self, summary: str):
        """입력 요약 표시"""
        st.subheader("📋 입력 정보 확인")
        st.markdown(summary)
        st.markdown("---")
    
    def display_itinerary(self, itinerary_data: List[Dict[str, Any]]):
        """여행 일정 표시"""
        st.header("🗓️ 여행 일정")
        
        if not itinerary_data:
            st.warning("일정 정보가 없습니다.")
            return
        
        # 탭으로 일정 표시
        tab_names = [f"Day {day['day']}" for day in itinerary_data]
        tabs = st.tabs(tab_names)
        
        for i, (tab, day_data) in enumerate(zip(tabs, itinerary_data)):
            with tab:
                self._display_day_itinerary(day_data)
    
    def _display_day_itinerary(self, day_data: Dict[str, Any]):
        """일일 일정 표시"""
        
        # 일일 요약
        st.subheader(f"📅 {day_data.get('date', 'N/A')} - Day {day_data.get('day', 'N/A')}")
        
        # 활동 표시
        if day_data.get('activities'):
            st.markdown("### 🎯 주요 활동")
            
            for activity in day_data['activities']:
                with st.expander(f"⏰ {activity.get('time', 'N/A')} - {activity.get('activity', 'N/A')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**📍 장소:** {activity.get('location', 'N/A')}")
                        st.markdown(f"**🚗 교통:** {activity.get('transportation', 'N/A')}")
                        st.markdown(f"**💰 비용:** {activity.get('cost', 'N/A')}")
                    
                    with col2:
                        st.markdown(f"**📝 설명:** {activity.get('description', 'N/A')}")
                        st.markdown(f"**🏷️ 카테고리:** {activity.get('category', 'N/A')}")
        
        # 식사 표시
        if day_data.get('meals'):
            st.markdown("### 🍽️ 식사")
            
            for meal in day_data['meals']:
                with st.expander(f"🍴 {meal.get('time', 'N/A')} - {meal.get('restaurant', 'N/A')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**🍽️ 음식:** {meal.get('cuisine', 'N/A')}")
                        st.markdown(f"**💰 비용:** {meal.get('cost', 'N/A')}")
                    
                    with col2:
                        st.markdown(f"**📝 메모:** {meal.get('notes', 'N/A')}")
                        st.markdown(f"**🕐 식사 유형:** {meal.get('meal_type', 'N/A')}")
        
        # 숙박 표시
        if day_data.get('accommodation'):
            st.markdown("### 🏨 숙박")
            accommodation = day_data['accommodation']
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**🏨 숙박시설:** {accommodation.get('name', 'N/A')}")
                st.markdown(f"**🏷️ 유형:** {accommodation.get('type', 'N/A')}")
            
            with col2:
                st.markdown(f"**💰 비용:** {accommodation.get('cost', 'N/A')}")
                st.markdown(f"**📝 메모:** {accommodation.get('notes', 'N/A')}")
    
    def display_recommendations(self, recommendations: Dict[str, Any]):
        """추천사항 표시"""
        st.header("💡 추천사항")
        
        if not recommendations:
            st.warning("추천사항이 없습니다.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            if recommendations.get('must_visit'):
                st.markdown("### 🎯 반드시 가봐야 할 곳")
                for place in recommendations['must_visit']:
                    st.markdown(f"• {place}")
            
            if recommendations.get('hidden_gems'):
                st.markdown("### 💎 숨겨진 명소")
                for gem in recommendations['hidden_gems']:
                    st.markdown(f"• {gem}")
        
        with col2:
            if recommendations.get('local_tips'):
                st.markdown("### 🏠 현지인 팁")
                for tip in recommendations['local_tips']:
                    st.markdown(f"• {tip}")
            
            if recommendations.get('budget_tips'):
                st.markdown("### 💰 예산 절약 팁")
                for tip in recommendations['budget_tips']:
                    st.markdown(f"• {tip}")
    
    def display_cost_summary(self, total_cost: str):
        """비용 요약 표시"""
        st.header("💰 예상 비용")
        
        if total_cost:
            st.info(f"**총 예상 비용: {total_cost}**")
        else:
            st.warning("비용 정보가 없습니다.")
    
    def display_packing_list(self, packing_list: List[str]):
        """준비물 목록 표시"""
        st.header("🎒 준비물 목록")
        
        if packing_list:
            st.markdown("여행에 필요한 준비물들입니다:")
            for item in packing_list:
                st.markdown(f"• {item}")
        else:
            st.warning("준비물 목록이 없습니다.")
    
    def display_alternative_options(self):
        """대안 옵션 버튼 표시"""
        st.header("🔄 대안 일정 생성")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            budget_btn = st.button("💰 저예산 버전", help="더 저렴한 예산으로 조정")
        
        with col2:
            luxury_btn = st.button("🌟 럭셔리 버전", help="고급스러운 여행으로 업그레이드")
        
        with col3:
            relaxed_btn = st.button("😌 느긋한 버전", help="더 여유로운 일정으로 조정")
        
        with col4:
            adventure_btn = st.button("🏃 모험 버전", help="스릴 있는 액티비티 추가")
        
        return {
            "budget": budget_btn,
            "luxury": luxury_btn,
            "relaxed": relaxed_btn,
            "adventure": adventure_btn
        }
    
    def display_additional_info_buttons(self):
        """추가 정보 버튼 표시"""
        st.header("📚 추가 정보")
        
        col1, col2 = st.columns(2)
        
        with col1:
            weather_btn = st.button("🌤️ 날씨 정보", help="목적지 날씨 정보 조회")
        
        with col2:
            local_tips_btn = st.button("🏠 현지인 팁", help="현지인만 아는 정보")
        
        return {
            "weather": weather_btn,
            "local_tips": local_tips_btn
        }
    
    def display_weather_info(self, weather_info: str):
        """날씨 정보 표시"""
        st.header("🌤️ 날씨 정보")
        st.markdown(weather_info)
    
    def display_local_tips(self, local_tips: str):
        """현지인 팁 표시"""
        st.header("🏠 현지인 팁")
        st.markdown(local_tips)
    
    def display_error(self, error_message: str):
        """오류 메시지 표시"""
        st.error(f"❌ 오류가 발생했습니다: {error_message}")
    
    def display_success(self, message: str):
        """성공 메시지 표시"""
        st.success(f"✅ {message}")
    
    def display_loading(self, message: str = "처리 중..."):
        """로딩 표시"""
        with st.spinner(message):
            pass
    
    def display_itinerary_chart(self, itinerary_data: List[Dict[str, Any]]):
        """일정 차트 표시"""
        st.header("📊 일정 분석")
        
        if not itinerary_data:
            return
        
        # 활동 카테고리별 분석
        activity_categories = []
        for day in itinerary_data:
            for activity in day.get('activities', []):
                activity_categories.append(activity.get('category', '기타'))
        
        if activity_categories:
            # 카테고리별 활동 수
            category_counts = pd.Series(activity_categories).value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("활동 카테고리 분포")
                fig1 = px.pie(
                    values=category_counts.values,
                    names=category_counts.index,
                    title="활동 유형별 분포"
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                st.subheader("일별 활동 수")
                daily_activities = [len(day.get('activities', [])) for day in itinerary_data]
                days = [f"Day {day.get('day', i+1)}" for i, day in enumerate(itinerary_data)]
                
                fig2 = px.bar(
                    x=days,
                    y=daily_activities,
                    title="일별 활동 수",
                    labels={'x': '일차', 'y': '활동 수'}
                )
                st.plotly_chart(fig2, use_container_width=True)
    
    def display_export_options(self, itinerary_data: Dict[str, Any]):
        """내보내기 옵션 표시"""
        st.header("💾 일정 내보내기")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 PDF로 내보내기"):
                st.info("PDF 내보내기 기능은 추후 구현 예정입니다.")
        
        with col2:
            if st.button("📱 이미지로 저장"):
                st.info("이미지 저장 기능은 추후 구현 예정입니다.")
        
        with col3:
            if st.button("📋 텍스트로 복사"):
                st.info("텍스트 복사 기능은 추후 구현 예정입니다.") 