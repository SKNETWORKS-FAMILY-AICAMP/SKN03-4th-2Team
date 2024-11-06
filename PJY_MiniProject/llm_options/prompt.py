from langchain import hub

def get_hub_prompt():
    prompt = hub.pull("hwchase17/openai-functions-agent")

    return prompt