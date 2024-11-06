from langchain_core.prompts import ChatPromptTemplate
from .constant import CHATBOT_MESSAGE, CHATBOT_ROLE
from langchain_core.messages import SystemMessage
from langchain_core.prompts import MessagesPlaceholder


def create_message(role: CHATBOT_ROLE, prompt: str):
    return {CHATBOT_MESSAGE.role.name: role.name, CHATBOT_MESSAGE.content.name: prompt}


def create_prompt(user_input: str):
    return ChatPromptTemplate.from_messages(
        [
            (
                CHATBOT_ROLE.assistant.name,
                "질문이 최근 정보를 요구하는 경우 검색 결과를 우선 제공해야 합니다.",
            ),
            (CHATBOT_ROLE.user.name, user_input),
        ]
    )


def messages_prompt():
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""
    검색하는 url 링크 별로 내용을 요약해서 알려줘
    """
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
