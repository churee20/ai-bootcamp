"""
Budget Manager Agent - 예산 관리 전문 Agent
"""
from typing import Dict, Any

class BudgetManagerAgent:
    """예산 관리 전문 Agent"""
    
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
    
    def manage_budget(self, total_budget: str, categories: Dict[str, float]) -> Dict[str, Any]:
        """예산 관리"""
        return {
            "budget_breakdown": {
                "accommodation": "숙박 비용",
                "food": "식비",
                "transportation": "교통비",
                "activities": "액티비티 비용",
                "misc": "기타 비용"
            },
            "savings_tips": ["절약 팁"],
            "splurge_recommendations": ["특별 지출 추천"],
            "total_estimated": "총 예상 비용"
        } 