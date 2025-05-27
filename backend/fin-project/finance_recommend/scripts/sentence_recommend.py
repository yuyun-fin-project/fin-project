"""
금융 상품 추천을 위한 사용자 쿼리 예시 모음

이 파일은 finance_recommend 앱의 자연어 기반 상품 추천 시스템에서 사용할 수 있는
사용자 쿼리 예시를 제공합니다. 이 예시들은 Product 모델의 속성을 활용하여 생성되었습니다.
"""

# 기본 쿼리 예시 (상품 유형별)
DEPOSIT_QUERIES = [
    # 기본 예금 관련 쿼리
    "이율이 높은 정기예금 추천해주세요",
    "1년 만기 예금 중 이율이 가장 높은 상품",
    "단기 예금 중 금리가 좋은 상품",
    "장기 예금 추천",
    "6개월 만기 정기예금",
    "2년 이상 예치 가능한 정기예금",
    "3년 만기 고금리 예금",
    
    # 특정 조건 관련 쿼리
    "소액으로 시작할 수 있는 예금",
    "중도해지 금리가 좋은 예금",
    "만기 후 이율이 좋은 예금",
    "우대금리 조건이 있는 예금",
    "온라인 전용 정기예금",
    "특판 정기예금",
    
    # 특정 대상 관련 쿼리
    "서민을 위한 정기예금",
    "청년 우대 정기예금",
    "직장인을 위한 정기예금",
    "노년층을 위한 정기예금",
    "주부를 위한 정기예금",
    
    # 금융사 관련 쿼리
    "시중은행 정기예금",
    "지방은행 정기예금",
    "저축은행 정기예금",
    "인터넷은행 정기예금",
]

SAVINGS_QUERIES = [
    # 기본 적금 관련 쿼리
    "이율이 높은 적금 추천해주세요",
    "1년 만기 적금 중 이율이 가장 높은 상품",
    "단기 적금 중 금리가 좋은 상품",
    "장기 적금 추천",
    "6개월 만기 적금",
    "2년 이상 납입 가능한 적금",
    "3년 만기 고금리 적금",
    
    # 특정 조건 관련 쿼리
    "소액으로 시작할 수 있는 적금",
    "자유적립식 적금",
    "정액적립식 적금",
    "우대금리 조건이 있는 적금",
    "온라인 전용 적금",
    "특판 적금",
    "목돈 마련을 위한 적금",
    "결혼 자금 마련을 위한 적금",
    "주택 자금 마련을 위한 적금",
    
    # 특정 대상 관련 쿼리
    "서민을 위한 적금",
    "청년 우대 적금",
    "직장인을 위한 적금",
    "노년층을 위한 적금",
    "주부를 위한 적금",
    "학생을 위한 적금",
    
    # 금융사 관련 쿼리
    "시중은행 적금",
    "지방은행 적금",
    "저축은행 적금",
    "인터넷은행 적금",
]

# 복합 쿼리 (여러 조건 결합)
COMPLEX_QUERIES = [
    # 예금 복합 쿼리
    "1년 만기 중도해지 가능한 고금리 정기예금",
    "소액으로 가입 가능한 2년 만기 정기예금",
    "온라인 가입 가능한 3년 만기 우대금리 정기예금",
    "청년 우대 고금리 단기 정기예금",
    "서민 전용 장기 정기예금",
    "퇴직금 운용을 위한 고금리 정기예금",
    
    # 적금 복합 쿼리
    "월 10만원 납입 가능한 고금리 적금",
    "자유적립식 2년 만기 적금",
    "결혼 자금 마련을 위한 3년 만기 적금",
    "청년 우대 고금리 적금",
    "주택 자금 마련을 위한 장기 적금",
    "소액으로 시작하는 자유적립식 적금",
    "학생을 위한 소액 적금",
]

# 금융 목표 기반 쿼리
GOAL_BASED_QUERIES = [
    # 단기 목표
    "여행 자금 마련을 위한 6개월 적금",
    "결혼 자금 마련을 위한 1년 적금",
    "단기간 목돈 마련을 위한 고금리 예금",
    "긴급 자금 마련을 위한 단기 예금",
    
    # 중기 목표
    "자동차 구매를 위한 2년 적금",
    "이사 자금 마련을 위한 적금",
    "학비 마련을 위한 적금",
    "창업 자금 마련을 위한 예금",
    
    # 장기 목표
    "주택 구매를 위한 장기 적금",
    "노후 자금 마련을 위한 장기 예금",
    "자녀 교육 자금 마련을 위한 장기 적금",
    "은퇴 준비를 위한 장기 예금",
]

# 금융 상황 기반 쿼리
SITUATION_BASED_QUERIES = [
    # 수입/지출 관련
    "월급 관리를 위한 적금",
    "보너스 운용을 위한 예금",
    "고정 지출 관리를 위한 적금",
    "여유 자금 운용을 위한 예금",
    
    # 생애 주기 관련
    "대학생을 위한 적금",
    "사회 초년생을 위한 적금",
    "신혼부부를 위한 적금",
    "중년층을 위한 예금",
    "은퇴자를 위한 예금",
    
    # 특수 상황
    "이직 준비를 위한 단기 예금",
    "창업 준비를 위한 적금",
    "주택 구매 준비를 위한 적금",
    "자녀 교육비 마련을 위한 적금",
]

# 모든 쿼리 통합
ALL_QUERIES = DEPOSIT_QUERIES + SAVINGS_QUERIES + COMPLEX_QUERIES + GOAL_BASED_QUERIES + SITUATION_BASED_QUERIES

# 추천 문장 생성 함수
def get_random_query(query_type=None):
    """
    무작위 추천 문장을 반환합니다.
    
    Args:
        query_type (str, optional): 쿼리 유형 ('deposit', 'savings', 'complex', 'goal', 'situation')
                                   None인 경우 모든 쿼리 중에서 선택
    
    Returns:
        str: 추천 문장
    """
    import random
    
    if query_type == 'deposit':
        return random.choice(DEPOSIT_QUERIES)
    elif query_type == 'savings':
        return random.choice(SAVINGS_QUERIES)
    elif query_type == 'complex':
        return random.choice(COMPLEX_QUERIES)
    elif query_type == 'goal':
        return random.choice(GOAL_BASED_QUERIES)
    elif query_type == 'situation':
        return random.choice(SITUATION_BASED_QUERIES)
    else:
        return random.choice(ALL_QUERIES)

# 추천 문장 예시 출력
if __name__ == "__main__":
    print("=== 예금 관련 추천 문장 ===")
    for _ in range(3):
        print(f"- {get_random_query('deposit')}")
    
    print("\n=== 적금 관련 추천 문장 ===")
    for _ in range(3):
        print(f"- {get_random_query('savings')}")
    
    print("\n=== 복합 조건 추천 문장 ===")
    for _ in range(3):
        print(f"- {get_random_query('complex')}")
    
    print("\n=== 금융 목표 기반 추천 문장 ===")
    for _ in range(3):
        print(f"- {get_random_query('goal')}")
    
    print("\n=== 금융 상황 기반 추천 문장 ===")
    for _ in range(3):
        print(f"- {get_random_query('situation')}")