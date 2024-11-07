# # 프롬프트를 구성하는 데 사용되는 클래스입니다.
# from langchain_core.prompts import ChatPromptTemplate
# # 앞서 정의한 상수를 가져와서 역할과 메시지 속성을 사용합니다.
# from .constant import CHATBOT_MESSAGE, CHATBOT_ROLE
# # 서로 다른 종류의 메시지를 표현하기 위한 클래스입니다.
# from langchain_core.messages import SystemMessage
# # MessagesPlaceholder: 메시지의 자리 표시자를 만드는 데 사용됩니다
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# def create_message(role:CHATBOT_ROLE, prompt:str):

#     return {
#         CHATBOT_MESSAGE.role.name: role.name,
#         CHATBOT_MESSAGE.content.name: prompt
#     }

# # 프롬프트 생성
# def create_prompt():
#     return ChatPromptTemplate.from_messages([
#         (CHATBOT_ROLE.assistant.name, "최신정보를 물어볼땐 2023년이후 정보이기때문에 챗봇으로 응답하지말고 검색결과를 통해 응답해줘"),
#         (CHATBOT_ROLE.user.name, "{user_input}"),
#     ])


# def messages_prompt():
#     return  ChatPromptTemplate.from_messages(
#     [
#         SystemMessage(
#             content="You are a helpful assistant. Answer all questions to the best of your ability."
#         ),
#         MessagesPlaceholder(variable_name="messages"),
#     ]
# )

