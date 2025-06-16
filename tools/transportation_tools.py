"""
Transportation Tools for Travel Planning
"""
from langchain.tools import BaseTool
from typing import Optional

class TransportationTool(BaseTool):
    """교통 정보 조회 도구"""
    
    name: str = "get_transportation"
    description: str = "목적지의 교통 정보를 조회합니다. 입력 형식: '목적지, 교통수단선호' (예: '파리, 대중교통, 도보')"
    
    def _run(self, query: str) -> str:
        """교통 정보 조회 실행"""
        try:
            # 입력 파싱
            parts = query.split(',', 1)
            if len(parts) >= 2:
                destination = parts[0].strip()
                transportation_preferences = parts[1].strip()
            else:
                destination = query.strip()
                transportation_preferences = "대중교통"
            
            return f"""
            {destination}의 교통 정보:
            - 선호 교통수단: {transportation_preferences}
            
            교통 옵션:
            1. 지하철 - €2.10/회, 1일 패스 €7.50
            2. 버스 - €2.10/회
            3. 택시 - €15-25/회
            4. 렌터카 - €50/일
            5. 도보 - 무료
            
            추천: 지하철 1일 패스 + 도보 조합
            총 교통비: €37.50 (5일 기준)
            """
        except Exception as e:
            return f"교통 정보 조회 중 오류 발생: {str(e)}"
    
    def _arun(self, query: str):
        raise NotImplementedError("비동기 실행은 지원하지 않습니다.") 