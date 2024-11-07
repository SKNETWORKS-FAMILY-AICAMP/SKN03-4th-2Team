from langchain_core.prompts import ChatPromptTemplate
from .constant import CHATBOT_MESSAGE, CHATBOT_ROLE
from langchain_core.messages import SystemMessage
from langchain_core.prompts import MessagesPlaceholder

def create_message(role: CHATBOT_ROLE, prompt: str):
    if not isinstance(prompt, str) or len(prompt.strip()) == 0:
        raise ValueError("프롬프트는 빈 문자열일 수 없습니다.")  # 빈 문자열 검사
    return {CHATBOT_MESSAGE.role.name: role.name, CHATBOT_MESSAGE.content.name: prompt}

def create_prompt(user_input: str):
    if not isinstance(user_input, str) or len(user_input.strip()) == 0:
        raise ValueError("사용자 입력은 빈 문자열일 수 없습니다.")  # 사용자 입력 검사
    return ChatPromptTemplate.from_messages([
        (CHATBOT_ROLE.system.name, "질문이 최근 정보(2023년 이후)를 요구하는 경우 검색 결과를 우선 제공해야 합니다."),
        (CHATBOT_ROLE.user.name, user_input),
    ])

def messages_prompt():
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="당신은 유용한 도우미입니다. 2023년 이후의 정보가 필요한 질문에는 스스로 답변을 생성하는 대신 검색 결과를 사용하여 응답하세요."
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
