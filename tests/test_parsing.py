#!/usr/bin/env python3
"""
Simple test script for _parse_free_form_text method
"""
import os
import sys
from datetime import date, timedelta

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.coordinator import TravelCoordinatorAgent

# Mock LLM and tools for testing purposes
class MockLLM:
    def __init__(self):
        pass

    def invoke(self, input_dict):
        return {'output': ''}

class MockTools:
    def __init__(self):
        pass

def test_parse_free_form_text():
    """Test the _parse_free_form_text method"""
    print("Testing _parse_free_form_text method...")
    
    # Create coordinator agent with mock objects
    llm = MockLLM()
    tools = MockTools()
    coordinator_agent = TravelCoordinatorAgent(llm, tools)
    
    # Sample free-form text that LLM might return
    sample_text = """
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
    
    user_input = {
        'destination': '서울',
        'duration': 2,
        'travel_style': '역사, 문화, 미식'
    }
    
    try:
        # Test the parsing method
        itinerary, total_cost, agent_analysis = coordinator_agent._parse_free_form_text(sample_text, user_input)
        
        print(f"✅ Parsing successful!")
        print(f"📅 Itinerary length: {len(itinerary)}")
        print(f"💰 Total cost: {total_cost}")
        print(f"📝 Analysis length: {len(agent_analysis)}")
        
        # Verify the results
        assert len(itinerary) == 2, f"Expected 2 days, got {len(itinerary)}"
        assert itinerary[0]['day'] == 1, f"Expected day 1, got {itinerary[0]['day']}"
        assert itinerary[1]['day'] == 2, f"Expected day 2, got {itinerary[1]['day']}"
        assert "경복궁 방문" in itinerary[0]['activities'][0]['activity'], "Day 1 activity not found"
        assert "창덕궁과 후원" in itinerary[1]['activities'][0]['activity'], "Day 2 activity not found"
        assert total_cost == "약 ₩1,500,000", f"Expected cost not found, got {total_cost}"
        assert "이 일정은 여행 스타일(역사, 문화, 미식)을 고려하여 최적화되었습니다." in agent_analysis, "Analysis text not found"
        
        # Test date generation
        today = date.today()
        assert itinerary[0]['date'] == today.strftime("%Y-%m-%d"), f"Date mismatch for day 1"
        assert itinerary[1]['date'] == (today + timedelta(days=1)).strftime("%Y-%m-%d"), f"Date mismatch for day 2"
        
        print("✅ All assertions passed!")
        print("✅ _parse_free_form_text method is working correctly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_parse_free_form_text()
    if success:
        print("\n🎉 All tests passed! The parsing method is working correctly.")
    else:
        print("\n💥 Tests failed! Please check the implementation.")
        sys.exit(1) 