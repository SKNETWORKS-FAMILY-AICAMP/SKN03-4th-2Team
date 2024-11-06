import openai
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.prompts import PromptTemplate
from langchain import LLMChain

# .env 파일에서 환경 변수 불러오기
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 모델 초기화 (tools 없이 설정)
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
