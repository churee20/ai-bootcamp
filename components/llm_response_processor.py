import json
import re
from typing import Dict, Any, List, Optional
import streamlit as st
from datetime import datetime, timedelta

class LLMResponseProcessor:
    """LLM 응답 처리기"""
    
    def __init__(self):
        self.processed_data = {}
    
    def process_llm_response(self, response_text: str) -> Dict[str, Any]:
        """LLM 응답을 파싱하고 구조화된 데이터로 변환"""
        
        try:
            # JSON 추출 시도
            json_data = self._extract_json_from_response(response_text)
            
            if json_data:
                # 데이터 검증 및 보완
                validated_data = self._validate_and_enhance_data(json_data)
                self.processed_data = validated_data
                return validated_data
            else:
                # JSON이 없는 경우 텍스트 파싱
                parsed_data = self._parse_text_response(response_text)
                self.processed_data = parsed_data
                return parsed_data
                
        except Exception as e:
            st.error(f"응답 처리 중 오류가 발생했습니다: {str(e)}")
            return {"error": str(e)}
    
    def _extract_json_from_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """응답 텍스트에서 JSON 추출"""
        
        # JSON 블록 찾기
        json_pattern = r'```json\s*(.*?)\s*```'
        json_match = re.search(json_pattern, response_text, re.DOTALL)
        
        if json_match:
            json_str = json_match.group(1)
        else:
            # JSON 블록이 없는 경우 전체 텍스트에서 JSON 찾기
            json_pattern = r'\{.*\}'
            json_match = re.search(json_pattern, response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                return None
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    
    def _validate_and_enhance_data(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """JSON 데이터 검증 및 보완"""
        
        enhanced_data = {
            "itinerary": [],
            "recommendations": {},
            "total_estimated_cost": "",
            "packing_list": [],
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "data_source": "llm_response"
            }
        }
        
        # 일정 데이터 처리
        if "itinerary" in json_data:
            enhanced_data["itinerary"] = self._process_itinerary(json_data["itinerary"])
        
        # 추천사항 처리
        if "recommendations" in json_data:
            enhanced_data["recommendations"] = json_data["recommendations"]
        
        # 총 비용 처리
        if "total_estimated_cost" in json_data:
            enhanced_data["total_estimated_cost"] = json_data["total_estimated_cost"]
        
        # 준비물 목록 처리
        if "packing_list" in json_data:
            enhanced_data["packing_list"] = json_data["packing_list"]
        
        return enhanced_data
    
    def _process_itinerary(self, itinerary_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """일정 데이터 처리 및 보완"""
        
        processed_itinerary = []
        
        for day_data in itinerary_data:
            processed_day = {
                "day": day_data.get("day", 1),
                "date": self._generate_date(day_data.get("day", 1)),
                "activities": [],
                "meals": [],
                "accommodation": {},
                "summary": ""
            }
            
            # 활동 처리
            if "activities" in day_data:
                processed_day["activities"] = self._process_activities(day_data["activities"])
            
            # 식사 처리
            if "meals" in day_data:
                processed_day["meals"] = self._process_meals(day_data["meals"])
            
            # 숙박 처리
            if "accommodation" in day_data:
                processed_day["accommodation"] = day_data["accommodation"]
            
            # 일일 요약 생성
            processed_day["summary"] = self._generate_day_summary(processed_day)
            
            processed_itinerary.append(processed_day)
        
        return processed_itinerary
    
    def _process_activities(self, activities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """활동 데이터 처리"""
        
        processed_activities = []
        
        for activity in activities:
            processed_activity = {
                "time": activity.get("time", ""),
                "activity": activity.get("activity", ""),
                "location": activity.get("location", ""),
                "description": activity.get("description", ""),
                "cost": activity.get("cost", ""),
                "transportation": activity.get("transportation", ""),
                "category": self._categorize_activity(activity.get("activity", ""))
            }
            
            processed_activities.append(processed_activity)
        
        return processed_activities
    
    def _process_meals(self, meals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """식사 데이터 처리"""
        
        processed_meals = []
        
        for meal in meals:
            processed_meal = {
                "time": meal.get("time", ""),
                "restaurant": meal.get("restaurant", ""),
                "cuisine": meal.get("cuisine", ""),
                "cost": meal.get("cost", ""),
                "notes": meal.get("notes", ""),
                "meal_type": self._categorize_meal(meal.get("time", ""))
            }
            
            processed_meals.append(processed_meal)
        
        return processed_meals
    
    def _categorize_activity(self, activity_name: str) -> str:
        """활동 카테고리 분류"""
        
        activity_lower = activity_name.lower()
        
        if any(word in activity_lower for word in ["박물관", "미술관", "갤러리"]):
            return "문화"
        elif any(word in activity_lower for word in ["공원", "산", "바다", "자연"]):
            return "자연"
        elif any(word in activity_lower for word in ["쇼핑", "마켓", "몰"]):
            return "쇼핑"
        elif any(word in activity_lower for word in ["레스토랑", "카페", "음식"]):
            return "음식"
        elif any(word in activity_lower for word in ["운동", "스포츠", "액티비티"]):
            return "액티비티"
        else:
            return "기타"
    
    def _categorize_meal(self, time: str) -> str:
        """식사 유형 분류"""
        
        if "06" in time or "07" in time or "08" in time or "09" in time:
            return "아침"
        elif "11" in time or "12" in time or "13" in time:
            return "점심"
        elif "17" in time or "18" in time or "19" in time or "20" in time:
            return "저녁"
        else:
            return "간식"
    
    def _generate_date(self, day_number: int) -> str:
        """일차에 따른 날짜 생성"""
        
        # 현재 날짜 기준으로 여행 시작일을 내일로 설정
        start_date = datetime.now() + timedelta(days=1)
        travel_date = start_date + timedelta(days=day_number - 1)
        
        return travel_date.strftime("%Y-%m-%d")
    
    def _generate_day_summary(self, day_data: Dict[str, Any]) -> str:
        """일일 요약 생성"""
        
        activities_count = len(day_data.get("activities", []))
        meals_count = len(day_data.get("meals", []))
        
        summary = f"Day {day_data.get('day', 1)}: "
        
        if activities_count > 0:
            summary += f"{activities_count}개 활동, "
        
        if meals_count > 0:
            summary += f"{meals_count}회 식사"
        
        return summary
    
    def _parse_text_response(self, response_text: str) -> Dict[str, Any]:
        """텍스트 응답 파싱 (JSON이 없는 경우)"""
        
        # 간단한 텍스트 파싱 로직
        parsed_data = {
            "itinerary": [],
            "recommendations": {
                "must_visit": [],
                "hidden_gems": [],
                "local_tips": [],
                "budget_tips": []
            },
            "total_estimated_cost": "",
            "packing_list": [],
            "raw_text": response_text,
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "data_source": "text_parsing"
            }
        }
        
        # 텍스트에서 날짜별 정보 추출
        day_pattern = r'Day\s*(\d+)[:\s]*(.*?)(?=Day\s*\d+|$)'
        day_matches = re.findall(day_pattern, response_text, re.DOTALL | re.IGNORECASE)
        
        for day_num, day_content in day_matches:
            day_data = {
                "day": int(day_num),
                "date": self._generate_date(int(day_num)),
                "activities": [],
                "meals": [],
                "accommodation": {},
                "summary": f"Day {day_num}: {day_content[:100]}..."
            }
            parsed_data["itinerary"].append(day_data)
        
        return parsed_data
    
    def get_processed_data(self) -> Dict[str, Any]:
        """처리된 데이터 반환"""
        return self.processed_data
    
    def get_itinerary_summary(self) -> str:
        """일정 요약 반환"""
        
        if not self.processed_data or "itinerary" not in self.processed_data:
            return "일정 정보가 없습니다."
        
        itinerary = self.processed_data["itinerary"]
        total_days = len(itinerary)
        total_activities = sum(len(day.get("activities", [])) for day in itinerary)
        total_meals = sum(len(day.get("meals", [])) for day in itinerary)
        
        summary = f"""
        **여행 일정 요약:**
        - 총 여행 기간: {total_days}일
        - 총 활동 수: {total_activities}개
        - 총 식사 수: {total_meals}회
        - 예상 총 비용: {self.processed_data.get('total_estimated_cost', 'N/A')}
        """
        
        return summary 