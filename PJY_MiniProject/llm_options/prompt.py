from langchain import hub
from langchain_core.prompts import ChatPromptTemplate

def get_prompt():
    prompt = hub.pull("hwchase17/openai-functions-agent")

    # 또는 PromptTemplate 객체와 결합하려면 아래와 같이 하세요
    additional_prompt = ChatPromptTemplate.from_template("\n\nYou are a helpful assistant. You must answer in Korean.")
    formatted_prompt = additional_prompt.format()  # 템플릿을 실제 텍스트로 변환

    # 두 텍스트를 결합하려면
    combined_prompt = prompt + formatted_prompt

    return combined_prompt
