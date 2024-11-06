from langgraph.graph import END, START, StateGraph, MessagesState
from langagent.faiss_utill import query_subwaystations_recommendations
from typing import Literal
from langagent.model import model

# 에이전트가 recommend_subwaystations 결과만 반환하는 함수 정의
def call_model_with_recommendations(state: MessagesState):
    user_input = state['messages'][-1].content

    # 지하철역 추천 결과 가져오기
    recommendations = query_subwaystations_recommendations(user_input)
    recommendations_result = "추천 지하철역 경로:\n" + "\n".join(
        [f"{i+1}. {rec['content']}" for i, rec in enumerate(recommendations)]
    ) if recommendations else "추천 결과를 찾을 수 없습니다."

    # 모델에 전달할 최종 prompt 생성
    prompt = f"{recommendations_result}\n\n사용자가 요청한 '{user_input}'에 대해 더 자세히 설명해 주세요."
    
    # 모델에 최종 결과 전달
    response = model.invoke([{"content": prompt, "role": "assistant"}])
    return {"messages": [response]}

# 워크플로우 초기화
workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model_with_recommendations)
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

# 조건부 경로 설정 함수
def should_use_recommendations(state: MessagesState) -> Literal["agent"]:
    # 사용자 요청이 있을 때 항상 agent를 호출
    return "agent"

workflow.add_conditional_edges(START, should_use_recommendations)
