"""
Itinerary Tools for Travel Planning
"""
from langchain.tools import BaseTool
from typing import Optional

class ItineraryOptimizerTool(BaseTool):
    """일정 최적화 도구"""
    
    name: str = "optimize_itinerary"
    description: str = "여행 일정을 최적화하고 효율적인 경로를 제안합니다. 입력 형식: '목적지, 기간, 활동' (예: '파리, 5일, 박물관/미술관, 맛집 탐방')"
    
    def _run(self, query: str) -> str:
        """일정 최적화 실행"""
        try:
            # 입력 파싱
            parts = query.split(',', 2)
            if len(parts) >= 3:
                destination = parts[0].strip()
                duration_str = parts[1].strip().replace('일', '').replace('일간', '')
                activities = parts[2].strip()
                duration = int(duration_str)
            else:
                destination = query.strip()
                duration = 5
                activities = "일반적인 관광"
            
            # 하드코딩된 파리 일정 대신, 입력 정보를 요약하여 반환
            return f"Received request to optimize a {duration} day trip to {destination} with activities: {activities}. The agent should now proceed to plan the itinerary based on this information."
        except Exception as e:
            return f"일정 최적화 중 오류 발생: {str(e)}"
    
    def _arun(self, query: str):
        raise NotImplementedError("비동기 실행은 지원하지 않습니다.") 