"""
Budget Tools for Travel Planning
"""
from langchain.tools import BaseTool
from typing import Optional

class BudgetCalculatorTool(BaseTool):
    """예산 계산 도구"""
    
    name: str = "calculate_budget"
    description: str = "여행 예산을 계산하고 관리합니다. 입력 형식: '예산범위, 기간, 목적지' (예: '보통 (50-100만원), 5일, 파리')"
    
    def _run(self, query: str) -> str:
        """예산 계산 실행"""
        try:
            # 입력 파싱
            parts = query.split(',', 2)
            if len(parts) >= 3:
                total_budget = parts[0].strip()
                duration_str = parts[1].strip().replace('일', '').replace('일간', '')
                destination = parts[2].strip()
                duration = int(duration_str)
            else:
                total_budget = "보통 (50-100만원)"
                duration = 5
                destination = query.strip()
            
            # 예시 계산
            accommodation_cost = 120 * duration  # 숙박비
            food_cost = 70 * duration  # 식비
            transportation_cost = 37.5  # 교통비
            activities_cost = 50 * duration  # 액티비티비
            misc_cost = 30 * duration  # 기타비용
            
            total_cost = accommodation_cost + food_cost + transportation_cost + activities_cost + misc_cost
            
            return f"""
            {destination} {duration}일 여행 예산 계산:
            
            예산 분배:
            - 숙박: €{accommodation_cost} ({duration}박)
            - 식비: €{food_cost} (일 €70)
            - 교통: €{transportation_cost} (5일 패스)
            - 액티비티: €{activities_cost} (일 €50)
            - 기타: €{misc_cost} (일 €30)
            
            총 예상 비용: €{total_cost}
            예산 범위: {total_budget}
            
            절약 팁:
            - 숙박: 게스트하우스 선택으로 30% 절약
            - 식비: 현지 마켓 이용으로 20% 절약
            - 교통: 대중교통 패스 이용
            """
        except Exception as e:
            return f"예산 계산 중 오류 발생: {str(e)}"
    
    def _arun(self, query: str):
        raise NotImplementedError("비동기 실행은 지원하지 않습니다.") 