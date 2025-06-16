"""
Travel Coordinator Agent - Multi Agent System의 메인 코디네이터
"""
from langchain.agents import AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.schema import BaseMessage
from typing import Dict, Any, List
import streamlit as st
from langchain.agents import initialize_agent, AgentType
import json
from datetime import date, timedelta
import re # Added for regex parsing
import os

# langchain_chroma를 선택적 import로 변경
try:
    from langchain_chroma import Chroma
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    Chroma = None

from config.config import get_embeddings

CHROMA_PERSIST_DIRECTORY = "./chroma_db"

class TravelCoordinatorAgent:
    """여행 계획을 조율하는 메인 Agent"""
    
    def __init__(self, llm=None, tools=None, vectorstore=None):
        """TravelCoordinatorAgent 초기화"""
        self.llm = llm
        self.tools = tools or []
        
        # API 키 확인
        self.has_api_key = bool(os.getenv('AOAI_API_KEY'))
        
        # RAG 활성화 (API 키가 있을 때만 ChromaDB 로드)
        if self.has_api_key and CHROMA_AVAILABLE:
            try:
                from config.config import get_embeddings
                self.embeddings = get_embeddings()
                if self.embeddings:
                    self.vectorstore = Chroma(persist_directory=CHROMA_PERSIST_DIRECTORY, embedding_function=self.embeddings)
                    print(f"ChromaDB 로드 성공: {CHROMA_PERSIST_DIRECTORY}")
                    print("RAG 기능이 활성화되었습니다.")
                else:
                    print("Embeddings 초기화 실패")
                    self.vectorstore = None
            except Exception as e:
                print(f"ChromaDB 로드 실패: {e}")
                self.vectorstore = None
        else:
            print("API 키가 설정되지 않아 ChromaDB를 로드하지 않습니다.")
            print("RAG 기능이 비활성화되었습니다.")
            self.vectorstore = None
        
        # Agent 초기화 (JSON 파싱 에러 처리 포함)
        if self.llm:
            try:
                # Agent용 시스템 프롬프트 정의
                system_message = """당신은 전문 여행 코디네이터입니다. 

작업 순서:
1. 필요한 도구들을 사용하여 정보를 수집하세요
2. 모든 도구 사용이 완료되면 반드시 최종 여행 계획을 작성하세요
3. 최종 응답은 상세하고 구조화된 텍스트 형식이어야 합니다

중요 규칙:
- 도구 사용 후 반드시 "Final Answer:"로 시작하는 최종 응답을 작성해야 합니다
- 최종 응답이 없으면 작업이 완료되지 않은 것입니다
- 모든 도구 사용이 끝나면 즉시 최종 응답을 생성하세요
- 중간에 멈추지 말고 완전한 여행 계획을 작성하세요
- 응답 형식은 반드시 "Final Answer:"로 시작해야 합니다
- 도구를 사용할 때는 실제로 도구를 실행하고 결과를 받아야 합니다"""
                
                agent = initialize_agent(
                    tools=self.tools,
                    llm=self.llm,
                    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                    verbose=True,
                    handle_parsing_errors=True,  # 파싱 에러 처리 활성화
                    max_iterations=5,  # 반복 횟수를 다시 늘림
                    early_stopping_method="generate",  # 조기 종료 방법
                    return_intermediate_steps=False,  # 중간 단계 반환 안함
                    max_execution_time=180,  # 최대 실행 시간 3분으로 늘림
                    agent_kwargs={"system_message": system_message}  # 시스템 메시지 추가
                )
                self.agent = agent
                print("Agent 초기화 성공")
                print(f"사용 가능한 도구들: {[tool.name for tool in self.tools]}")
            except Exception as e:
                st.warning(f"Agent 초기화 중 오류 발생: {str(e)}")
                self.agent = None
        else:
            self.agent = None
        
        print("Agent를 활성화하고 Agent 호출 모드로 실행합니다.")
    
    def plan_travel(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """여행 계획을 수립하는 메인 메서드"""
        
        try:
            # RAG 검색 (API 키가 있고 vectorstore가 있을 때만 수행)
            context_info = ""
            if self.has_api_key and self.vectorstore and user_input.get('destination'):
                try:
                    query = f"{user_input['destination']} 여행 정보 {user_input.get('travel_style', '')} {user_input.get('activities', '')}"
                    docs = self.vectorstore.similarity_search(query, k=3) # 상위 3개 문서 검색
                    context_info = "\n\n" + "\n".join([doc.page_content for doc in docs])
                    print(f"RAG 검색 완료: {len(docs)}개 문서 검색됨")
                    # st.info(f"RAG 검색된 컨텍스트: {context_info}")
                except Exception as e:
                    st.warning(f"RAG 검색 중 오류 발생: {str(e)}")
                    context_info = ""
            else:
                # API 키가 없거나 vectorstore가 없으면 RAG 검색 건너뛰기
                if not self.has_api_key:
                    print("API 키가 없어 RAG 검색을 건너뜁니다.")
                elif not self.vectorstore:
                    print("ChromaDB가 로드되지 않아 RAG 검색을 건너뜁니다.")
                context_info = ""
            
            # 프롬프트 생성
            prompt = self._format_user_input(user_input, context_info)
            
            # Agent를 통한 호출
            if self.agent:
                try:
                    print(f"Agent 호출 시작: {user_input.get('destination', 'N/A')} 여행 계획")
                    
                    # Agent를 통한 호출 (타임아웃 없이, Agent 자체 설정 사용)
                    result = self.agent.run(prompt)
                    
                    print(f"Agent 응답 수신: {len(str(result))} 문자")
                    print(f"Agent 응답 미리보기: {str(result)[:300]}...")
                    
                    # Agent 응답이 유효한지 확인
                    if result and len(str(result).strip()) > 10:
                        print("Agent 응답이 유효합니다. 파싱을 시작합니다.")
                        
                        # 응답 정리
                        result_str = str(result).strip()
                        print(f"원본 응답 길이: {len(result_str)} 문자")
                        
                        # Tool 호출만 있고 실제 응답이 없는 경우 처리
                        if "Action:" in result_str and "Final Answer:" not in result_str:
                            print("Tool 호출만 있고 최종 응답이 없습니다. 데모 데이터를 반환합니다.")
                            return self._get_demo_result(user_input)
                        
                        # "Final Answer:" 부분이 있으면 제거
                        if "Final Answer:" in result_str:
                            result_str = result_str.split("Final Answer:")[-1].strip()
                            print("Final Answer 부분을 제거했습니다.")
                        
                        # 마크다운 헤더가 있으면 그대로 사용, 없으면 추가
                        if not result_str.startswith("#"):
                            result_str = f"## 📅 여행 계획\n\n{result_str}"
                            print("마크다운 헤더를 추가했습니다.")
                        
                        print(f"정리된 응답 길이: {len(result_str)} 문자")
                        print(f"정리된 응답 미리보기: {result_str[:200]}...")
                        
                        parsed_result = self._parse_result_simple(result_str)
                        print(f"파싱 완료: {parsed_result.get('type', 'unknown')} 타입")
                        print(f"파싱된 content 길이: {len(parsed_result.get('content', ''))} 문자")
                        return parsed_result
                    else:
                        # Agent 응답이 유효하지 않으면 데모 데이터 반환
                        print("Agent 응답이 유효하지 않아 데모 데이터를 반환합니다.")
                        print(f"응답 길이: {len(str(result)) if result else 0}")
                        return self._get_demo_result(user_input)
                        
                except Exception as e:
                    st.warning(f"Agent 호출 중 오류 발생: {str(e)}")
                    print(f"Agent 오류 상세: {str(e)}")
                    print(f"오류 타입: {type(e).__name__}")
                    
                    # 파싱 오류인 경우 원본 응답을 정리해서 반환
                    if "Could not parse LLM output" in str(e) or "OutputParserException" in str(e):
                        print("파싱 오류 감지. 원본 응답을 정리하여 반환합니다.")
                        try:
                            # 오류 메시지에서 원본 응답 추출 시도
                            error_msg = str(e)
                            if "`" in error_msg:
                                # 백틱으로 둘러싸인 부분 추출
                                start = error_msg.find("`") + 1
                                end = error_msg.rfind("`")
                                if start > 0 and end > start:
                                    original_response = error_msg[start:end].strip()
                                    if len(original_response) > 10:
                                        # 응답 정리
                                        if "Final Answer:" in original_response:
                                            original_response = original_response.split("Final Answer:")[-1].strip()
                                        
                                        if not original_response.startswith("#"):
                                            original_response = f"## 📅 여행 계획\n\n{original_response}"
                                        
                                        return self._parse_result_simple(original_response)
                        except:
                            pass
                    
                    # Agent 오류 시 데모 데이터 반환
                    return self._get_demo_result(user_input)
            else:
                # Agent가 없으면 데모 데이터 반환
                print("Agent가 초기화되지 않아 데모 데이터를 반환합니다.")
                return self._get_demo_result(user_input)
                
        except Exception as e:
            st.error(f"여행 계획 수립 중 오류 발생: {str(e)}")
            return self._get_demo_result(user_input)
    
    def _get_demo_result(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """데모 결과 반환"""
        destination = user_input.get('destination', '파리')
        duration = user_input.get('duration', 5)
        travel_style = user_input.get('travel_style', '일반')
        
        st.info(f"데모 모드: {destination} {duration}일 여행 계획을 생성합니다.")

        # 데모 데이터에 동적인 날짜 추가
        itinerary_data = []
        start_date = date.today()
        
        # 목적지별 데모 활동 데이터
        demo_activities = {
            '파리': [
                {'activity': '에펠탑 방문', 'location': '에펠탑', 'cost': '€26', 'category': '문화'},
                {'activity': '루브르 박물관 관람', 'location': '루브르 박물관', 'cost': '€17', 'category': '문화'},
                {'activity': '샹젤리제 거리 산책', 'location': '샹젤리제', 'cost': '무료', 'category': '관광'},
                {'activity': '몽마르트르 언덕 방문', 'location': '몽마르트르', 'cost': '무료', 'category': '관광'},
                {'activity': '세느강 크루즈', 'location': '세느강', 'cost': '€15', 'category': '관광'}
            ],
            '로마': [
                {'activity': '콜로세움 방문', 'location': '콜로세움', 'cost': '€16', 'category': '문화'},
                {'activity': '바티칸 박물관', 'location': '바티칸', 'cost': '€17', 'category': '문화'},
                {'activity': '트레비 분수', 'location': '트레비 분수', 'cost': '무료', 'category': '관광'},
                {'activity': '스페인 광장', 'location': '스페인 광장', 'cost': '무료', 'category': '관광'},
                {'activity': '포로 로마노', 'location': '포로 로마노', 'cost': '€12', 'category': '문화'}
            ],
            '도쿄': [
                {'activity': '시부야 크로싱', 'location': '시부야', 'cost': '무료', 'category': '관광'},
                {'activity': '센소지 사원', 'location': '아사쿠사', 'cost': '무료', 'category': '문화'},
                {'activity': '도쿄 타워', 'location': '도쿄 타워', 'cost': '¥3000', 'category': '관광'},
                {'activity': '하라주쿠 쇼핑', 'location': '하라주쿠', 'cost': '변동', 'category': '쇼핑'},
                {'activity': '오다이바 관광', 'location': '오다이바', 'cost': '무료', 'category': '관광'}
            ]
        }
        
        # 기본 활동 목록 (목적지가 위에 없을 경우)
        default_activities = [
            {'activity': '도시 관광', 'location': f'{destination} 시내', 'cost': '무료', 'category': '관광'},
            {'activity': '현지 음식 체험', 'location': f'{destination} 레스토랑', 'cost': '€30', 'category': '음식'},
            {'activity': '박물관 방문', 'location': f'{destination} 박물관', 'cost': '€15', 'category': '문화'},
            {'activity': '공원 산책', 'location': f'{destination} 공원', 'cost': '무료', 'category': '관광'},
            {'activity': '쇼핑', 'location': f'{destination} 쇼핑센터', 'cost': '변동', 'category': '쇼핑'}
        ]
        
        activities = demo_activities.get(destination, default_activities)
        
        for i in range(duration):
            current_date = start_date + timedelta(days=i)
            day_activities = activities[i % len(activities):(i % len(activities)) + 2]  # 하루에 2개 활동
            
            itinerary_data.append({
                "day": i + 1,
                "date": current_date.strftime("%Y-%m-%d"),
                "activities": [
                    {
                        "time": f"09:00-11:00",
                        "activity": day_activities[0]['activity'],
                        "location": day_activities[0]['location'],
                        "description": f"{destination}의 대표적인 {day_activities[0]['category']} 활동을 체험합니다.",
                        "cost": day_activities[0]['cost'],
                        "transportation": "지하철/도보",
                        "category": day_activities[0]['category']
                    },
                    {
                        "time": f"14:00-16:00",
                        "activity": day_activities[1]['activity'] if len(day_activities) > 1 else "자유 시간",
                        "location": day_activities[1]['location'] if len(day_activities) > 1 else f"{destination} 시내",
                        "description": f"{destination}의 {day_activities[1]['category'] if len(day_activities) > 1 else '관광'} 활동을 즐깁니다.",
                        "cost": day_activities[1]['cost'] if len(day_activities) > 1 else "무료",
                        "transportation": "도보",
                        "category": day_activities[1]['category'] if len(day_activities) > 1 else "관광"
                    }
                ],
                "meals": [
                    {
                        "time": "12:00-13:30",
                        "restaurant": f"{destination} 현지 레스토랑",
                        "cuisine": "현지 전통 요리",
                        "cost": "€25-35",
                        "notes": "현지인들이 즐겨가는 맛집",
                        "meal_type": "점심"
                    }
                ],
                "accommodation": {
                    "name": f"Hotel {destination}",
                    "type": "호텔",
                    "cost": "€100-150",
                    "notes": "시내 중심가에 위치한 편리한 호텔"
                },
                "summary": f"Day {i+1}: {len(day_activities)}개 활동, 1회 식사"
            })
        
        return {
            "itinerary": itinerary_data,
            "recommendations": {
                "must_visit": [f"{destination}의 대표 관광지", f"{destination} 박물관", f"{destination} 공원"],
                "hidden_gems": [f"{destination} 현지 마켓", f"{destination} 숨겨진 카페", f"{destination} 전망대"],
                "local_tips": ["대중교통을 이용하면 편리합니다", "식사 시간을 피해 관광지를 방문하세요", "현지인처럼 여행해보세요"],
                "budget_tips": ["박물관 패스를 구매하면 할인됩니다", "현지 마켓에서 식재료를 구매하세요", "무료 관광지를 많이 활용하세요"]
            },
            "total_estimated_cost": "€400-600",
            "packing_list": ["여권", "카메라", "편한 신발", "우산", "어댑터", "현지 통화"],
            "agent_analysis": f"""
🤖 Multi Agent 데모 분석 결과:

🎯 **Travel Coordinator Agent**: {destination} {duration}일 여행 계획을 수립했습니다.
🔍 **Destination Research Agent**: {destination}의 주요 관광지와 문화 정보를 수집했습니다.
🏨 **Accommodation Agent**: 시내 중심가의 편리한 호텔을 추천했습니다.
🍽️ **Food & Dining Agent**: 현지 전통 요리를 맛볼 수 있는 레스토랑을 선별했습니다.
🚗 **Transportation Agent**: 지하철과 도보를 조합한 효율적인 교통 계획을 제안했습니다.
🎪 **Activity Planner Agent**: {destination}의 대표 관광지와 현지 체험을 포함한 일정을 계획했습니다.
💰 **Budget Manager Agent**: 총 €400-600의 예산으로 합리적인 여행 계획을 수립했습니다.

💡 **API 키 설정 방법**:
1. Azure OpenAI 서비스에서 API 키와 엔드포인트를 발급받으세요
2. 프로젝트 루트에 `.env` 파일을 생성하고 다음 정보를 입력하세요:
   ```
   AOAI_API_KEY="your_azure_openai_api_key"
   AOAI_ENDPOINT="https://your-resource.openai.azure.com/"
   AOAI_DEPLOY_GPT4O="your_deployment_name"
   AOAI_API_VERSION="2024-05-01-preview"
   AOAI_EMBEDDING_DEPLOYMENT="your_embedding_deployment_name"
   ```
3. 애플리케이션을 재시작하면 AI 기반 개인화된 여행 계획을 받을 수 있습니다.
            """
        }
    
    def _format_user_input(self, user_input: Dict[str, Any], context: str = "") -> str:
        """사용자 입력을 프롬프트 형식으로 변환 (컨텍스트 포함)"""
        
        context_section = f"\n\n참조할 여행 정보:\n{context}" if context else ""

        return f"""당신은 전문 여행 코디네이터입니다. 사용자의 요구사항에 맞는 완벽한 여행 계획을 수립해주세요.

{context_section}

여행 계획 요청:
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
- 추가 요구사항: {user_input.get('additional_notes', 'N/A')}

작업 순서:
1. 목적지 정보를 검색하세요 (search_destination 도구 사용)
2. 날씨 정보를 확인하세요 (get_weather 도구 사용)
3. 숙박, 음식, 교통, 액티비티를 계획하세요 (각각의 도구 사용)
4. 예산을 관리하세요 (budget_calculator 도구 사용)
5. 최종 일정을 최적화하세요 (itinerary_optimizer 도구 사용)

**매우 중요: 모든 도구 사용이 완료되면 반드시 "Final Answer:"로 시작하는 최종 여행 계획을 작성해주세요.**

사용 가능한 도구들:
- search_destination: 목적지 정보 검색
- get_weather: 날씨 정보 조회
- search_accommodation: 숙박 시설 검색
- search_restaurant: 레스토랑 검색
- search_transportation: 교통 수단 검색
- budget_calculator: 예산 계산
- itinerary_optimizer: 일정 최적화

최종 응답 형식:
Final Answer: [여기에 상세한 여행 계획을 작성]

여행 계획은 다음 형식으로 작성해주세요:

## 📅 여행 일정

### Day 1: [날짜]
**오전 활동:**
- 시간: [시간]
- 활동: [활동명]
- 장소: [장소]
- 설명: [상세 설명]
- 비용: [비용]
- 교통수단: [교통수단]

**점심:**
- 시간: [시간]
- 식당: [식당명]
- 요리: [요리 종류]
- 비용: [비용]
- 메모: [추가 정보]

**오후 활동:**
- 시간: [시간]
- 활동: [활동명]
- 장소: [장소]
- 설명: [상세 설명]
- 비용: [비용]
- 교통수단: [교통수단]

**숙박:**
- 숙소명: [숙소명]
- 유형: [숙소 유형]
- 비용: [비용]
- 메모: [추가 정보]

## 💡 추천사항
- 필수 방문지: [목록]
- 숨겨진 명소: [목록]
- 현지인 팁: [목록]
- 예산 절약 팁: [목록]

## 💰 총 예상 비용
[총 비용 범위]

## 🎒 준비물
[준비물 목록]

모든 도구 사용을 완료한 후 "Final Answer:"로 시작하는 완전한 여행 계획을 작성해주세요."""
    
    def _parse_result_simple(self, result: str) -> Dict[str, Any]:
        """Agent 결과를 파싱하여 구조화된 데이터로 변환 (텍스트 기반)"""
        try:
            # 텍스트 응답을 그대로 반환하되, 기본 구조는 유지
            return {
                "type": "text_response",
                "content": result,
                "status": "success",
                "message": "여행 계획이 성공적으로 생성되었습니다."
            }
        except Exception as e:
            st.error(f"응답 파싱 중 오류 발생: {str(e)}")
            return {
                "type": "error",
                "content": result,
                "status": "error",
                "message": f"응답 처리 중 오류가 발생했습니다: {str(e)}"
            } 