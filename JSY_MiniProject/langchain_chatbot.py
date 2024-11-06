from dotenv import load_dotenv
# .env 파일에 등록된 변수(데이터)를 os 환경변수에 적용
load_dotenv()

from langchain_common.constant import CHATBOT_ROLE, CHATBOT_MESSAGE
from langchain_common.prompt import create_message
from langchain_common.chain import get_message_of_llm

# web ui/ux
import streamlit as st

st.set_page_config(
    page_title="AI 진로 상담사",
    page_icon="🎯",
    layout="wide"
)

if st.button("대화 초기화"):
    st.session_state.messages = []
    st.rerun()


st.title("🎯 AI 진로 상담사")
st.markdown("""
### 환영합니다! 
저는 당신의 진로 선택을 도와드릴 AI 상담사입니다.
성격, 흥미, 적성을 바탕으로 맞춤형 진로 상담을 제공해드립니다.
""")
st.header("상담 가이드")
st.markdown("""
1. **성격 분석**: 자신의 성격 특성을 이야기해주세요
2. **흥미 탐색**: 관심있는 분야를 알려주세요
3. **진로 추천**: AI가 맞춤형 진로를 추천해드립니다
""")

# 메세지를 저장 
# messages = {"role":"", "content":""}
#   role -> user(사용자) / assistant(AI)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 저장한 메세지를 화면에 표현 
for message in st.session_state.messages:
    if message[CHATBOT_MESSAGE.role.name] in CHATBOT_ROLE.__members__:
        with st.chat_message(message[CHATBOT_MESSAGE.role.name]):
            st.markdown(message[CHATBOT_MESSAGE.content.name])

# 사용자 입력
prompt = st.chat_input(" 입력해주세요  ")
# 사용자 입력이 있다면,
if prompt:
    user_message = create_message(role=CHATBOT_ROLE.user, prompt=prompt)
    
    # 입력값이 존재한다며, 
    if user_message:
        # 화면에 표현
        with st.chat_message(CHATBOT_ROLE.user.name):
            st.write(prompt)
        st.session_state.messages.append(user_message)

        # 챗봇 답변 
        with st.chat_message(CHATBOT_ROLE.assistant.name):
            assistant_response = st.write_stream(get_message_of_llm(prompt))
            # 이력 추가 
            st.session_state.messages.append(
                create_message(role=CHATBOT_ROLE.assistant, prompt=assistant_response))