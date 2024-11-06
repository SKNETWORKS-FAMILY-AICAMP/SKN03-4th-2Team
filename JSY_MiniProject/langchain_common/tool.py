from typing import Annotated, Literal, TypedDict
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_openai.chat_models import ChatOpenAI

from operator import itemgetter
from typing import Literal

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

from .model import create_llm




# class AgentState(TypedDict):
#    input: str
#    chat_history: list[BaseMessage] # 대화 내용 중 '이전 메시지' 목록
#    agent_outcome: Union[AgentAction, AgentFinish, None] # 유효한 유형으로 `None`이 필요
#    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]



