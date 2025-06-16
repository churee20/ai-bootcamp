"""
Accommodation Tools for Travel Planning
"""
from langchain.tools import BaseTool
from typing import Optional

class AccommodationSearchTool(BaseTool):
    """숙박 시설 검색 도구"""
    
    name: str = "search_accommodation"
    description: str = "목적지의 숙박 시설을 검색하고 추천합니다. 입력 형식: '목적지, 예산범위, 숙박유형' (예: '파리, 보통 (50-100만원), 호텔')"
    
    def _run(self, query: str) -> str:
        """숙박 시설 검색 실행"""
        try:
            # 입력 파싱
            parts = query.split(',', 2)
            if len(parts) >= 3:
                destination = parts[0].strip()
                budget_range = parts[1].strip()
                accommodation_type = parts[2].strip()
            else:
                destination = query.strip()
                budget_range = "보통 (50-100만원)"
                accommodation_type = "호텔"
            
            return f"""
            {destination}의 숙박 추천:
            - 예산 범위: {budget_range}
            - 숙박 유형: {accommodation_type}
            
            추천 숙박시설:
            1. Hotel de Paris (호텔) - €120/박
            2. Le Petit Bistrot (게스트하우스) - €60/박
            3. Cozy Airbnb (에어비앤비) - €80/박
            
            총 숙박 비용: €{120 * 5} (5박 기준)
            """
        except Exception as e:
            return f"숙박 검색 중 오류 발생: {str(e)}"
    
    def _arun(self, query: str):
        raise NotImplementedError("비동기 실행은 지원하지 않습니다.") 