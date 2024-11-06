from langchain_openai import ChatOpenAI

# 모델 생성
def create_llm(model_id:str="gpt-4o-mini"):
    return ChatOpenAI(
        model=model_id
    )
