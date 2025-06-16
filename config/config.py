import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

# langfuse를 선택적 import로 변경
try:
    from langfuse import Langfuse
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False
    Langfuse = None

# 환경 변수 로드 - 현재 디렉토리에서 .env 파일 찾기
load_dotenv()

# OpenAI API 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Azure OpenAI 설정
AOAI_API_KEY = os.getenv("AOAI_API_KEY")
AOAI_ENDPOINT = os.getenv("AOAI_ENDPOINT")
AOAI_DEPLOY_GPT4O = os.getenv("AOAI_DEPLOY_GPT4O")
AOAI_API_VERSION = os.getenv("AOAI_API_VERSION", "2024-05-01-preview")
AOAI_EMBEDDING_DEPLOYMENT = os.getenv("AOAI_EMBEDDING_DEPLOYMENT")

# 여행 플래너 설정
DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))

# UI 설정
PAGE_TITLE = "AI 여행 플래너"
PAGE_ICON = "✈️"
LAYOUT = "wide"

# Langfuse 설정
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

def is_valid_api_key(api_key: str) -> bool:
    """API 키가 유효한지 확인"""
    if not api_key:
        return False
    
    # 빈 문자열이나 기본값이 아닌지 확인
    invalid_values = [
        "", 
        "your_azure_openai_api_key",
        "your_openai_api_key_here",
        "your_api_key_here",
        "sk-...",
        "sk-",
        "your-",
        "placeholder"
    ]
    
    return api_key.strip() not in invalid_values

def is_valid_endpoint(endpoint: str) -> bool:
    """엔드포인트가 유효한지 확인"""
    if not endpoint:
        return False
    
    # 빈 문자열이나 기본값이 아닌지 확인
    invalid_values = [
        "",
        "https://your-resource.openai.azure.com/",
        "https://your-resource.openai.azure.com",
        "your-endpoint",
        "placeholder"
    ]
    
    return endpoint.strip() not in invalid_values

def is_valid_deployment(deployment: str) -> bool:
    """배포명이 유효한지 확인"""
    if not deployment:
        return False
    
    # 빈 문자열이나 기본값이 아닌지 확인
    invalid_values = [
        "",
        "your_deployment_name",
        "your_embedding_deployment_name",
        "your-deployment",
        "placeholder"
    ]
    
    return deployment.strip() not in invalid_values

def has_valid_azure_openai_config() -> bool:
    """Azure OpenAI 설정이 모두 유효한지 확인"""
    return (
        is_valid_api_key(AOAI_API_KEY) and
        is_valid_endpoint(AOAI_ENDPOINT) and
        is_valid_deployment(AOAI_DEPLOY_GPT4O) and
        is_valid_deployment(AOAI_EMBEDDING_DEPLOYMENT)
    )

def has_valid_openai_config() -> bool:
    """OpenAI 설정이 유효한지 확인"""
    return is_valid_api_key(OPENAI_API_KEY)

def get_llm():
    """Azure OpenAI LLM 인스턴스 반환"""
    # Azure OpenAI 설정이 모두 유효한지 확인
    if not has_valid_azure_openai_config():
        print("Azure OpenAI API 키가 설정되지 않았거나 유효하지 않습니다.")
        return None
    
    try:
        return AzureChatOpenAI(
            openai_api_key=AOAI_API_KEY,
            azure_endpoint=AOAI_ENDPOINT,
            azure_deployment=AOAI_DEPLOY_GPT4O,
            api_version=AOAI_API_VERSION,
            temperature=DEFAULT_TEMPERATURE,
        )
    except Exception as e:
        print(f"LLM 초기화 실패: {e}")
        return None

def get_embeddings():
    """Azure OpenAI Embeddings 인스턴스 반환"""
    # Azure OpenAI 설정이 모두 유효한지 확인
    if not has_valid_azure_openai_config():
        print("Azure OpenAI API 키가 설정되지 않았거나 유효하지 않습니다.")
        return None
    
    try:
        return AzureOpenAIEmbeddings(
            model=AOAI_EMBEDDING_DEPLOYMENT,
            openai_api_version=AOAI_API_VERSION,
            api_key=AOAI_API_KEY,
            azure_endpoint=AOAI_ENDPOINT,
        )
    except Exception as e:
        print(f"Embeddings 초기화 실패: {e}")
        return None

def get_langfuse():
    """Langfuse 인스턴스 반환"""
    if not LANGFUSE_AVAILABLE:
        return None
    
    if not all([LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY]):
        return None
    
    return Langfuse(
        public_key=LANGFUSE_PUBLIC_KEY,
        secret_key=LANGFUSE_SECRET_KEY,
        host=LANGFUSE_HOST
    )

# 디버깅을 위한 환경 변수 출력 (개발 시에만 사용)
def print_env_info():
    """환경 변수 정보 출력 (디버깅용)"""
    print(f"OpenAI API Key: {'설정됨' if has_valid_openai_config() else '설정되지 않음'}")
    print(f"OpenAI Model: {OPENAI_MODEL}")
    print(f"Azure OpenAI API Key: {'설정됨' if is_valid_api_key(AOAI_API_KEY) else '설정되지 않음'}")
    print(f"Azure OpenAI Endpoint: {'설정됨' if is_valid_endpoint(AOAI_ENDPOINT) else '설정되지 않음'}")
    print(f"Azure OpenAI Deployment: {'설정됨' if is_valid_deployment(AOAI_DEPLOY_GPT4O) else '설정되지 않음'}")
    print(f"Azure OpenAI Embedding Deployment: {'설정됨' if is_valid_deployment(AOAI_EMBEDDING_DEPLOYMENT) else '설정되지 않음'}")
    print(f"Temperature: {DEFAULT_TEMPERATURE}")
    print(f"Max Tokens: {MAX_TOKENS}")
    print(f"Langfuse: {'설정됨' if LANGFUSE_AVAILABLE and LANGFUSE_PUBLIC_KEY else '설정되지 않음'}")
    print(f"전체 Azure OpenAI 설정: {'유효함' if has_valid_azure_openai_config() else '유효하지 않음'}") 