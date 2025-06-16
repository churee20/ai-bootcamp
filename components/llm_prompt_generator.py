from typing import Dict, Any

class LLMPromptGenerator:
    """LLM 프롬프트 생성기"""
    
    def __init__(self):
        self.base_prompt_template = """
당신은 전문 여행 플래너입니다. 다음 정보를 바탕으로 맞춤형 여행 일정을 만들어주세요.

**여행 정보:**
{travel_info}

**요구사항:**
- 일정은 {duration}일 동안의 상세한 계획이어야 합니다
- 각 날짜별로 시간대별 활동을 구체적으로 제시해주세요
- 예산 범위({budget_range})에 맞는 추천을 해주세요
- {travel_style} 스타일에 맞는 일정을 구성해주세요
- 선호하는 활동과 음식을 반영해주세요
- 교통수단과 숙박 옵션을 포함해주세요

**출력 형식:**
다음 JSON 형식으로 응답해주세요:

{{
    "itinerary": [
        {{
            "day": 1,
            "date": "YYYY-MM-DD",
            "activities": [
                {{
                    "time": "09:00-10:30",
                    "activity": "활동명",
                    "location": "장소",
                    "description": "상세 설명",
                    "cost": "예상 비용",
                    "transportation": "교통수단"
                }}
            ],
            "meals": [
                {{
                    "time": "12:00-13:00",
                    "restaurant": "식당명",
                    "cuisine": "음식 종류",
                    "cost": "예상 비용",
                    "notes": "특별한 점"
                }}
            ],
            "accommodation": {{
                "name": "숙박시설명",
                "type": "숙박 유형",
                "cost": "예상 비용",
                "notes": "특별한 점"
            }}
        }}
    ],
    "recommendations": {{
        "must_visit": ["반드시 가봐야 할 곳들"],
        "hidden_gems": ["숨겨진 명소들"],
        "local_tips": ["현지인 팁들"],
        "budget_tips": ["예산 절약 팁들"]
    }},
    "total_estimated_cost": "총 예상 비용",
    "packing_list": ["준비물 목록"]
}}

**중요한 점:**
- 현실적이고 실행 가능한 일정을 만들어주세요
- 여행자의 선호사항을 최대한 반영해주세요
- 예산과 시간을 고려한 합리적인 계획을 제시해주세요
- 현지 문화와 관습을 고려한 추천을 해주세요
"""
    
    def generate_travel_prompt(self, user_input: Dict[str, Any]) -> str:
        """사용자 입력을 바탕으로 여행 계획 프롬프트 생성"""
        
        # 여행 정보 구성
        travel_info = f"""
        - 목적지: {user_input.get('destination', 'N/A')}
        - 여행 기간: {user_input.get('duration', 'N/A')}일
        - 인원수: {user_input.get('group_size', 'N/A')}명
        - 여행 스타일: {user_input.get('travel_style', 'N/A')}
        - 예산 범위: {user_input.get('budget_range', 'N/A')}
        - 숙박 유형: {user_input.get('accommodation_type', 'N/A')}
        - 선호 활동: {', '.join(user_input.get('activities', []))}
        - 음식 선호: {', '.join(user_input.get('food_preferences', []))}
        - 교통수단: {', '.join(user_input.get('transportation', []))}
        - 여행 페이스: {user_input.get('pace', 'N/A')}
        """
        
        if user_input.get('additional_notes'):
            travel_info += f"\n- 추가 요구사항: {user_input.get('additional_notes')}"
        
        # 프롬프트 생성
        prompt = self.base_prompt_template.format(
            travel_info=travel_info,
            duration=user_input.get('duration', 'N/A'),
            budget_range=user_input.get('budget_range', 'N/A'),
            travel_style=user_input.get('travel_style', 'N/A')
        )
        
        return prompt
    
    def generate_alternative_prompt(self, user_input: Dict[str, Any], alternative_type: str) -> str:
        """대안 일정 생성 프롬프트"""
        
        alternative_prompts = {
            "budget": """
            기존 일정을 더 저렴한 예산으로 조정해주세요. 
            무료 관광지, 할인 정보, 저렴한 식당 등을 포함해주세요.
            """,
            "luxury": """
            기존 일정을 더 럭셔리한 버전으로 업그레이드해주세요.
            고급 호텔, 미슐랭 레스토랑, 프리미엄 액티비티 등을 포함해주세요.
            """,
            "relaxed": """
            기존 일정을 더 느긋한 페이스로 조정해주세요.
            휴식 시간을 충분히 포함하고, 스트레스 없는 일정으로 만들어주세요.
            """,
            "adventure": """
            기존 일정을 더 모험적인 버전으로 변경해주세요.
            스릴 있는 액티비티, 오프더비트 경험, 현지인과의 교류 등을 포함해주세요.
            """
        }
        
        base_prompt = self.generate_travel_prompt(user_input)
        alternative_prompt = alternative_prompts.get(alternative_type, "")
        
        return base_prompt + "\n\n" + alternative_prompt
    
    def generate_weather_prompt(self, destination: str, duration: int) -> str:
        """날씨 정보 요청 프롬프트"""
        return f"""
        {destination}의 {duration}일간 여행에 대한 날씨 정보와 준비사항을 알려주세요.
        
        다음 정보를 포함해주세요:
        - 계절별 평균 기온과 강수량
        - 여행 시기별 날씨 특징
        - 날씨에 따른 준비물 추천
        - 날씨가 여행 계획에 미치는 영향
        - 대안 계획 제안
        """
    
    def generate_local_tips_prompt(self, destination: str) -> str:
        """현지인 팁 요청 프롬프트"""
        return f"""
        {destination}에 대한 현지인만 아는 팁과 정보를 알려주세요.
        
        다음 정보를 포함해주세요:
        - 관광객이 모르는 숨겨진 명소
        - 현지인들이 즐겨가는 식당과 카페
        - 관광객 함정 피하는 방법
        - 현지 문화와 예절
        - 교통 이용 팁
        - 쇼핑 팁
        - 안전 주의사항
        """ 