import os
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from .tools import get_tools

load_dotenv()

class BenefitStationAgent:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.llm = None
        self.agent = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self._initialize_agent()
    
    def _initialize_agent(self):
        """에이전트 초기화"""
        try:
            # Gemini API 키 확인
            gemini_key = os.getenv("GEMINI_API_KEY")
            
            if gemini_key:
                print("✅ Gemini API 키 발견, Gemini 모델 사용")
                # Gemini 모델 사용 (향후 구현)
                from langchain_google_genai import ChatGoogleGenerativeAI
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-pro",
                    temperature=0.7,
                    google_api_key=gemini_key
                )
            elif self.openai_api_key:
                print("✅ OpenAI API 키 사용")
                # OpenAI LLM 초기화
                self.llm = ChatOpenAI(
                    model_name="gpt-4o",
                    temperature=0.7,
                    openai_api_key=self.openai_api_key
                )
            else:
                print("❌ AI API 키가 설정되지 않았습니다 (OpenAI 또는 Gemini 필요)")
                return
            
            # 도구 가져오기
            tools = get_tools()
            
            # 에이전트 초기화
            self.agent = initialize_agent(
                tools=tools,
                llm=self.llm,
                agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                memory=self.memory,
                verbose=True,
                max_iterations=3,
                early_stopping_method="generate"
            )
            
            print("✅ LangChain 에이전트 초기화 성공")
            
        except Exception as e:
            print(f"❌ 에이전트 초기화 실패: {e}")
    
    async def chat(self, message: str, user_id: str = "demo-user") -> str:
        """사용자 메시지에 대한 AI 응답 생성"""
        try:
            if not self.agent:
                return "죄송합니다. AI 에이전트가 초기화되지 않았습니다. OpenAI API 키를 확인해주세요."
            
            # 시스템 프롬프트 포함한 메시지 구성
            full_message = f"""
사용자 ID: {user_id}
사용자 메시지: {message}

당신은 Benefit Station의 친절한 AI 상품 추천 어시스턴트입니다.
사용자의 요청에 따라 적절한 복리후생 상품을 추천해주세요.

가능한 카테고리:
- food: 식음료 (스타벅스, 배달앱 등)
- health: 건강 (헬스장, 건강검진 등)  
- shopping: 쇼핑 (할인권, 상품권 등)
- life: 생활 (넷플릭스, 생활용품 등)
- education: 교육 (온라인 강의 등)

사용자의 요청을 분석하여 적절한 도구를 사용해 상품을 찾아 추천해주세요.
응답은 친근하고 도움이 되는 톤으로 작성해주세요.
            """
            
            response = self.agent.run(full_message)
            return response
            
        except Exception as e:
            return f"죄송합니다. 처리 중 오류가 발생했습니다: {str(e)}"
    
    def reset_memory(self):
        """대화 기록 초기화"""
        self.memory.clear()

# 전역 에이전트 인스턴스
agent_instance = None

def get_agent():
    """에이전트 인스턴스 반환"""
    global agent_instance
    if agent_instance is None:
        agent_instance = BenefitStationAgent()
    return agent_instance 