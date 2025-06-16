"""
Food Tools for Travel Planning
"""
from langchain.tools import BaseTool
from typing import Optional

class RestaurantSearchTool(BaseTool):
    """레스토랑 검색 도구"""
    
    name: str = "search_restaurants"
    description: str = "목적지의 레스토랑을 검색하고 추천합니다. 입력 형식: '목적지, 음식선호' (예: '파리, 현지 음식, 프랑스 전통')"
    
    def _run(self, query: str) -> str:
        """레스토랑 검색 실행"""
        try:
            # 입력 파싱
            parts = query.split(',', 1)
            if len(parts) >= 2:
                destination = parts[0].strip()
                food_preferences = parts[1].strip()
            else:
                destination = query.strip()
                food_preferences = "현지 음식"
            
            return f"""
            {destination}의 레스토랑 추천:
            - 음식 선호: {food_preferences}
            
            추천 레스토랑:
            1. Le Bistrot Parisien (프랑스 전통) - €35/인
            2. La Crêperie (크레페) - €15/인
            3. Le Petit Café (카페) - €20/인
            
            총 식비: €70/인/일 (3식 기준)
            """
        except Exception as e:
            return f"레스토랑 검색 중 오류 발생: {str(e)}"
    
    def _arun(self, query: str):
        raise NotImplementedError("비동기 실행은 지원하지 않습니다.") 