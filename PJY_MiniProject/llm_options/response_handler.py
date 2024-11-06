from .client import get_client
from .tools import get_tools
from .agent import create_agent, is_agent_finish, agent_excute
from .workflow import build_workflow
from .prompt import get_prompt

def response_from_llm(prompt, message_history=None):
    if message_history is None:
        message_history = []

    message_history.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    tools = get_tools()
    agent_runnable = create_agent(get_client(), tools, get_prompt())

    inputs = {
        "input": prompt,
        "chat_history": message_history,
        "intermediate_steps": []
    }

    # 에이전트 실행
    agent_outcome = agent_runnable.invoke(inputs)

    # 에이전트 완료 상태 확인
    if is_agent_finish(agent_outcome):
        return agent_outcome.return_values['output']

    output = agent_excute(agent_outcome, tools)

    # 상태 그래프 설정 및 실행
    workflow = build_workflow(agent_runnable)
    app = workflow.compile()
    output = app.invoke(inputs)

    agent_outcome = output.get("agent_outcome").return_values['output']

    return agent_outcome
