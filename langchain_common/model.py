from langchain_openai import ChatOpenAI

def create_llm(model_id: str = "gpt-4o-mini"):
    try:
        return ChatOpenAI(
            model=model_id
        )
    except Exception as e:
        raise ValueError(f"모델 생성 중 오류 발생: {e}")  # 오류 발생 시 적절한 메시지
