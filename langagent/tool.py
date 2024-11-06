from langchain_core.tools import tool

@tool
def search(query: str):
    """출발지랑 도착지 검색하면 거기로 갈 수 있는 가장 빠른 지하철 경로 말해줘"""
    """사용자 입력을 분석하여 가장 빠른 지하철 경로를 추정합니다.
        입력 예시: '강남역에서 서울역까지 가는 가장 빠른 경로', '서울에서 강남까지 대중교통'
    """ 
    if "강남역에서 서울역" in query.lower() or "강남에서 서울역 가는 법" in query.lower(): 
        return "2호선 강남역 (교대역 방면) 빠른 환승 6-1 -> 4호선 사당역 (총신대입구(이수)역 방면) 환승 빠른 하차 3-3-> 서울역 하차 " 
    return "가장 빠른 지하철 이동 경로와 빠른 환승 열차 번호 제시"

tools = [search]
