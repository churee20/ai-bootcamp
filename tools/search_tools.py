"""
Search Tools for Travel Planning
"""
from langchain.tools import BaseTool
from typing import Optional
import requests
import json

class SearchDestinationTool(BaseTool):
    """목적지 정보 검색 도구"""
    
    name: str = "search_destination"
    description: str = "목적지에 대한 기본 정보, 관광지, 문화 등을 검색합니다."
    
    def _run(self, destination: str) -> str:
        """목적지 정보 검색 실행"""
        try:
            # 실제 구현에서는 외부 API 사용 (예: Wikipedia, Google Places 등)
            # 여기서는 입력된 목적지 정보를 요약하여 반환
            return f"""
            {destination}에 대한 일반적인 정보:
            이 정보는 실제 검색 결과가 아닌, 목적지에 대한 일반적인 설명을 제공합니다.
            """
        except Exception as e:
            return f"목적지 검색 중 오류 발생: {str(e)}"
    
    def _arun(self, destination: str):
        raise NotImplementedError("비동기 실행은 지원하지 않습니다.")

class WeatherTool(BaseTool):
    """날씨 정보 조회 도구"""
    
    name: str = "get_weather"
    description: str = "목적지의 날씨 정보와 여행 시기별 날씨 특징을 조회합니다. 입력 형식: '목적지, 여행기간' (예: '파리, 2024년 5월 1-5일')"
    
    def _run(self, query: str) -> str:
        """날씨 정보 조회 실행"""
        try:
            # 입력 파싱
            parts = query.split(',', 1)
            if len(parts) >= 2:
                destination = parts[0].strip()
                travel_dates = parts[1].strip()
            else:
                destination = query.strip()
                travel_dates = "일반적인 여행 시기"
            
            # 실제 구현에서는 날씨 API 사용 (예: OpenWeatherMap 등)
            # 여기서는 입력된 목적지와 기간을 요약하여 반환
            return f"""
            {destination}의 {travel_dates} 날씨 정보:
            이 정보는 실제 날씨 데이터가 아닌, 일반적인 날씨 정보 요청을 나타냅니다.
            """
        except Exception as e:
            return f"날씨 정보 조회 중 오류 발생: {str(e)}"
    
    def _arun(self, query: str):
        raise NotImplementedError("비동기 실행은 지원하지 않습니다.") 