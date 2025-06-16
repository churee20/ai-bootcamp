import openai
from typing import Dict, Any, Optional
import streamlit as st
from config.config import (
    OPENAI_API_KEY, OPENAI_MODEL, DEFAULT_TEMPERATURE, MAX_TOKENS,
    get_llm, get_embeddings, get_langfuse,
    AOAI_API_KEY, AOAI_ENDPOINT, AOAI_DEPLOY_GPT4O
)

class LLMClient:
    """LLM 클라이언트 - OpenAI API와 Azure OpenAI 통신"""
    
    def __init__(self):
        self.client = None
        self.azure_llm = None
        self.langfuse = None
        self._initialize_client()
    
    def _initialize_client(self):
        """LLM 클라이언트 초기화"""
        try:
            # Azure OpenAI 우선 시도
            if all([AOAI_API_KEY, AOAI_ENDPOINT, AOAI_DEPLOY_GPT4O]):
                self.azure_llm = get_llm()
                if self.azure_llm:
                    st.success("✅ Azure OpenAI 연결 성공!")
                    return
            
            # OpenAI API 시도
            if OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here":
                self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
                st.success("✅ OpenAI API 연결 성공!")
                return
            
            # Langfuse 초기화
            self.langfuse = get_langfuse()
            if self.langfuse:
                st.info("📊 Langfuse 연결됨")
            
            # API 키가 없는 경우
            if not self.azure_llm and not self.client:
                st.warning("⚠️ OpenAI API 키가 설정되지 않았습니다.")
                st.info("💡 `.env` 파일에 `OPENAI_API_KEY` 또는 Azure OpenAI 설정을 추가해주세요.")
                st.info("💡 API 키가 없어도 UI는 정상적으로 작동하지만, AI 기능은 사용할 수 없습니다.")
                
        except Exception as e:
            st.error(f"❌ LLM 클라이언트 초기화 실패: {str(e)}")
            st.info("💡 API 키를 확인하고 다시 시도해주세요.")
    
    def generate_travel_plan(self, prompt: str) -> Optional[str]:
        """여행 계획 생성"""
        
        if not self._is_available():
            st.error("❌ LLM이 연결되지 않았습니다.")
            st.info("💡 `.env` 파일에 유효한 API 키를 설정해주세요.")
            return None
        
        try:
            with st.spinner("🤖 AI가 여행 계획을 생성하고 있습니다..."):
                if self.azure_llm:
                    # Azure OpenAI 사용
                    response = self.azure_llm.invoke(prompt)
                    return response.content
                else:
                    # OpenAI API 사용
                    response = self.client.chat.completions.create(
                        model=OPENAI_MODEL,
                        messages=[
                            {
                                "role": "system",
                                "content": "당신은 전문 여행 플래너입니다. 사용자의 요구사항에 맞는 상세하고 실용적인 여행 계획을 제공해주세요."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=DEFAULT_TEMPERATURE,
                        max_tokens=MAX_TOKENS
                    )
                    return response.choices[0].message.content
                
        except Exception as e:
            st.error(f"❌ 여행 계획 생성 중 오류가 발생했습니다: {str(e)}")
            return None
    
    def generate_alternative_plan(self, base_prompt: str, alternative_type: str) -> Optional[str]:
        """대안 여행 계획 생성"""
        
        if not self._is_available():
            st.error("❌ LLM이 연결되지 않았습니다.")
            return None
        
        try:
            with st.spinner(f"🔄 {alternative_type} 스타일의 대안 계획을 생성하고 있습니다..."):
                if self.azure_llm:
                    # Azure OpenAI 사용
                    response = self.azure_llm.invoke(base_prompt)
                    return response.content
                else:
                    # OpenAI API 사용
                    response = self.client.chat.completions.create(
                        model=OPENAI_MODEL,
                        messages=[
                            {
                                "role": "system",
                                "content": "당신은 전문 여행 플래너입니다. 기존 계획을 바탕으로 다양한 스타일의 대안을 제공해주세요."
                            },
                            {
                                "role": "user",
                                "content": base_prompt
                            }
                        ],
                        temperature=DEFAULT_TEMPERATURE,
                        max_tokens=MAX_TOKENS
                    )
                    return response.choices[0].message.content
                
        except Exception as e:
            st.error(f"❌ 대안 계획 생성 중 오류가 발생했습니다: {str(e)}")
            return None
    
    def get_weather_info(self, destination: str, duration: int) -> Optional[str]:
        """날씨 정보 요청"""
        
        if not self._is_available():
            st.error("❌ LLM이 연결되지 않았습니다.")
            return None
        
        try:
            with st.spinner("🌤️ 날씨 정보를 조회하고 있습니다..."):
                weather_prompt = f"{destination}의 {duration}일간 여행에 대한 날씨 정보와 준비사항을 알려주세요."
                
                if self.azure_llm:
                    # Azure OpenAI 사용
                    response = self.azure_llm.invoke(weather_prompt)
                    return response.content
                else:
                    # OpenAI API 사용
                    response = self.client.chat.completions.create(
                        model=OPENAI_MODEL,
                        messages=[
                            {
                                "role": "system",
                                "content": "당신은 여행 날씨 전문가입니다. 목적지의 날씨 정보와 여행 준비사항을 제공해주세요."
                            },
                            {
                                "role": "user",
                                "content": weather_prompt
                            }
                        ],
                        temperature=0.5,
                        max_tokens=1000
                    )
                    return response.choices[0].message.content
                
        except Exception as e:
            st.error(f"❌ 날씨 정보 조회 중 오류가 발생했습니다: {str(e)}")
            return None
    
    def get_local_tips(self, destination: str) -> Optional[str]:
        """현지인 팁 요청"""
        
        if not self._is_available():
            st.error("❌ LLM이 연결되지 않았습니다.")
            return None
        
        try:
            with st.spinner("🏠 현지인 팁을 수집하고 있습니다..."):
                tips_prompt = f"{destination}에 대한 현지인만 아는 팁과 정보를 알려주세요."
                
                if self.azure_llm:
                    # Azure OpenAI 사용
                    response = self.azure_llm.invoke(tips_prompt)
                    return response.content
                else:
                    # OpenAI API 사용
                    response = self.client.chat.completions.create(
                        model=OPENAI_MODEL,
                        messages=[
                            {
                                "role": "system",
                                "content": "당신은 현지 여행 전문가입니다. 관광객이 모르는 숨겨진 정보와 팁을 제공해주세요."
                            },
                            {
                                "role": "user",
                                "content": tips_prompt
                            }
                        ],
                        temperature=0.7,
                        max_tokens=1000
                    )
                    return response.choices[0].message.content
                
        except Exception as e:
            st.error(f"❌ 현지인 팁 수집 중 오류가 발생했습니다: {str(e)}")
            return None
    
    def _is_available(self) -> bool:
        """LLM 사용 가능 여부 확인"""
        return self.azure_llm is not None or self.client is not None
    
    def is_available(self) -> bool:
        """LLM 클라이언트 사용 가능 여부 확인 (기존 호환성)"""
        return self._is_available()
    
    def get_api_status(self) -> Dict[str, Any]:
        """API 상태 정보 반환"""
        return {
            "connected": self._is_available(),
            "azure_connected": self.azure_llm is not None,
            "openai_connected": self.client is not None,
            "langfuse_connected": self.langfuse is not None,
            "azure_api_key_set": bool(AOAI_API_KEY and AOAI_API_KEY != "your_azure_openai_api_key_here"),
            "openai_api_key_set": bool(OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here"),
            "model": "Azure OpenAI" if self.azure_llm else OPENAI_MODEL,
            "temperature": DEFAULT_TEMPERATURE,
            "max_tokens": MAX_TOKENS
        } 