# SKN03-4th-2Team
팀명 : F4

# 다이어트 챗봇 프로젝트

이 프로젝트는 사용자가 다이어트와 관련된 질문을 할 수 있는 챗봇 시스템을 구현한 것입니다. 이 챗봇은 OpenAI 모델과 LangChain 라이브러리를 활용하여 사용자의 질문에 대한 답변을 생성하며, Streamlit을 사용하여 웹 인터페이스를 제공합니다.

## 기술 스택

- **Python 3.x**
- **Streamlit**: 웹 애플리케이션 인터페이스
- **LangChain**: LLM(대형 언어 모델)을 활용한 에이전트 구축 및 실행
- **OpenAI GPT-4**: 대화형 AI 모델
- **FAISS**: 텍스트 검색 및 유사도 검색을 위한 벡터 데이터베이스
- **TavilySearch**: 외부 데이터 소스를 통한 검색 기능

## 프로젝트 구조

```bash
├── agent.py               # LangChain 에이전트 생성 및 실행
├── agentstate_option.py   # 에이전트 상태 정의
├── client.py              # OpenAI 모델 클라이언트 설정
├── model_parameter.py     # 모델 파라미터 설정
├── prompt.py              # Prompt 설정
├── response_handler.py    # LLM 응답 처리 및 워크플로우 실행
├── retriever.py           # 다이어트 관련 문서 검색 도구 설정
├── tools.py               # 외부 도구 및 검색 기능 설정
├── workflow.py            # 에이전트 실행 흐름 설정
├── dietapp.py             # Streamlit 웹 애플리케이션 실행
└── .env                   # 환경 변수 설정
```

## 그래프 구조 
![LangGraph](PJY_MiniProject/images/langgraph.png)


## 실행 사진 
![image](PJY_MiniProject/images/다이어트챗봇_결과사진_1.png)

![image2](PJY_MiniProject/images/다이어트챗봇_결과사진_2.png)