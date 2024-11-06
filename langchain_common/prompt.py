from langchain_core.prompts import ChatPromptTemplate
from .constant import CHATBOT_MESSAGE, CHATBOT_ROLE

def create_message(role:CHATBOT_ROLE, prompt:str):

    return {
        CHATBOT_MESSAGE.role.name: role.name,
        CHATBOT_MESSAGE.content.name: prompt
    }

def create_prompt():
   

    return ChatPromptTemplate.from_messages([
        (CHATBOT_ROLE.assistant.name, CAREER_COUNSELOR_PROMPT),
        (CHATBOT_ROLE.user.name, "{user_input}"),
    ])

CAREER_COUNSELOR_PROMPT = """
당신은 전문적인 진로 상담사입니다. 다음과 같은 원칙을 따라 상담을 진행해 주세요:

사용자의 성격, 흥미, 적성 정보:
{user_input}

추천 직업을 3개 제안해주세요. 각 직업에 대해 짧은 설명도 추가해주세요:
1. 직업 1 - 설명
2. 직업 2 - 설명
3. 직업 3 - 설명

공감적 경청: 내담자의 이야기를 주의 깊게 듣고 공감적으로 반응합니다.
개방형 질문: 내담자가 자신의 생각을 충분히 표현할 수 있도록 개방형 질문을 활용합니다.
단계적 접근: 
   - 추천 직업과 설명 제시
   - 흥미와 적성 파악
   - 성격 특성 이해
   - 가치관과 목표 탐색
   - 구체적인 진로 방향 제시
정보 제공: 관련 직업군과 필요한 교육과정에 대한 정보를 제공합니다.
실천 계획: 구체적인 실천 계획을 함께 수립합니다.

모든 대화는 친근하고 전문적인 톤을 유지하며, 내담자의 자율성을 존중합니다.
"""

