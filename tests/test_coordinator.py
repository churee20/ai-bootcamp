import os
import sys
import pytest
from datetime import date, timedelta

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.coordinator import TravelCoordinatorAgent

# Mock LLM and tools for testing purposes
class MockLLM:
    def __init__(self):
        pass

    def invoke(self, input_dict):
        # For testing _parse_free_form_text, we directly return a sample string
        # In a real scenario, this would be the LLM's raw text output
        sample_free_form_text = """
#### **Day 1: 서울 도착 및 궁궐 탐방**
- **오전**: 인천 국제공항(ICN) 도착 후 서울 시내로 이동, 호텔 체크인.
- **오후**: 경복궁 방문 및 한복 체험. 국립고궁박물관 관람.
- **저녁**: 삼청동에서 전통 한정식 맛집 탐방 후 북촌 한옥마을 야경 감상.

#### **Day 2: 서울 현대와 전통의 조화**
- **오전**: 창덕궁과 후원(비원) 특별 관람. (사전 예약 필수)
- **오후**: 명동으로 이동하여 쇼핑 및 길거리 음식 체험.
- **저녁**: 남산 서울타워에서 야경 감상 및 로맨틱 디너.

총 예상 비용**: 약 ₩1,500,000
이 일정은 여행 스타일(역사, 문화, 미식)을 고려하여 최적화되었습니다. 추가 질문이나 수정 사항이 있다면 알려주세요!
"""
        return {'output': sample_free_form_text}

class MockTools:
    def __init__(self):
        pass

@pytest.fixture
def coordinator_agent():
    llm = MockLLM()
    tools = MockTools()
    return TravelCoordinatorAgent(llm, tools)

def test_parse_free_form_text(coordinator_agent):
    user_input = {
        'destination': '서울',
        'duration': 2,
        'travel_style': '역사, 문화, 미식'
    }

    # Use the sample text directly from MockLLM for testing
    sample_text = coordinator_agent.llm.invoke({'input': ''})['output']

    itinerary, total_cost, agent_analysis = coordinator_agent._parse_free_form_text(sample_text, user_input)

    assert len(itinerary) == 2
    assert itinerary[0]['day'] == 1
    assert "경복궁 방문" in itinerary[0]['activities'][0]['activity']
    assert itinerary[1]['day'] == 2
    assert "창덕궁과 후원" in itinerary[1]['activities'][0]['activity']
    assert total_cost == "약 ₩1,500,000"
    assert "이 일정은 여행 스타일(역사, 문화, 미식)을 고려하여 최적화되었습니다." in agent_analysis

    # Test date generation for parsed itinerary (should be dynamic)
    today = date.today()
    assert itinerary[0]['date'] == today.strftime("%Y-%m-%d")
    assert itinerary[1]['date'] == (today + timedelta(days=1)).strftime("%Y-%m-%d") 