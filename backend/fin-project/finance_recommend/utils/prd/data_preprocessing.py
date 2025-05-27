from finance_recommend.models import Product, Option
"""
DEPOSIT
"result": {
    "prdt_div": "D",
    "total_count": 39,
    "max_page_no": 1,
    "now_page_no": 1,
    "err_cd": "000",
    "err_msg": "정상",
    "baseList": [
        {
            "dcls_month": "202505",
            "fin_co_no": "0010001",
            "fin_prdt_cd": "WR0001B",
            "kor_co_nm": "우리은행",
            "fin_prdt_nm": "WON플러스예금",
            "join_way": "인터넷,스마트폰,전화(텔레뱅킹)",
            "mtrt_int": "만기 후\n- 1개월이내 : 만기시점약정이율×50%\n- 1개월초과 6개월이내: 만기시점약정이율×30%\n- 6개월초과 : 만기시점약정이율×20%\n\n※ 만기시점 약정이율 : 일반정기예금 금리",
            "spcl_cnd": "해당사항 없음",
            "join_deny": "1",
            "join_member": "실명의 개인",
            "etc_note": "- 가입기간: 1~36개월\n- 최소가입금액: 1만원 이상\n- 만기일을 일,월 단위로 자유롭게 선택 가능\n- 만기해지 시 신규일 당시 영업점과 인터넷 홈페이지에 고시된 계약기간별 금리 적용",
            "max_limit": null,
            "dcls_strt_day": "20250520",
            "dcls_end_day": null,
            "fin_co_subm_day": "202505201054"
        },
    ],
    "optionList": [
        {
            "dcls_month": "202505",
            "fin_co_no": "0010001",
            "fin_prdt_cd": "WR0001B",
            "intr_rate_type": "S",
            "intr_rate_type_nm": "단리",
            "save_trm": "1",
            "intr_rate": 2.7,
            "intr_rate2": 2.7
        },
    ],
}
SAVING
"result": {
            "prdt_div": "S",
            "total_count": 56,
            "max_page_no": 1,
            "now_page_no": 1,
            "err_cd": "000",
            "err_msg": "정상",
            "baseList": [
                {
                    "dcls_month": "202505",
                    "fin_co_no": "0010001",
                    "fin_prdt_cd": "WR0001F",
                    "kor_co_nm": "우리은행",
                    "fin_prdt_nm": "우리SUPER주거래적금",
                    "join_way": "영업점,인터넷,스마트폰,전화(텔레뱅킹)",
                    "mtrt_int": "만기 후\n- 1개월이내 : 만기시점약정이율×50%\n- 1개월초과 6개월이내: 만기시점약정이율×30%\n- 6개월초과 : 만기시점약정이율×20%\n\n※ 만기시점 약정이율 : 일반정기적금 금리",
                    "spcl_cnd": "1. 거래실적인정기간동안 입출식계좌에서 아래 각실적이 있는 월 수가 계약기간의 1/2이상인경우\n가. 급여연금이체:연 0.7%p\n나. 공과금자동이체출금 실적 :0.3%p\n다. 카드결제금액 10만원이상 출금 :연 0.3%p\n2. 상품서비스 마케팅 동의 항목 중 전화및 SMS항목을 모두 동의, 만기해지시점까지 유지:연 0.1%p\n3. 금리우대쿠폰을 적용한 경우",
                    "join_deny": "1",
                    "join_member": "실명의 개인",
                    "etc_note": "1. 가입기간 : 1년/2년/3년\n2. 가입금액 : 월 50만원 이내",
                    "max_limit": null,
                    "dcls_strt_day": "20250520",
                    "dcls_end_day": null,
                    "fin_co_subm_day": "202505201055"
                },
            ],
            "optionList": [
                {
                    "dcls_month": "202505",
                    "fin_co_no": "0010001",
                    "fin_prdt_cd": "WR0001F",
                    "intr_rate_type": "S",
                    "intr_rate_type_nm": "단리",
                    "rsrv_type": "S",
                    "rsrv_type_nm": "정액적립식",
                    "save_trm": "12",
                    "intr_rate": 2.35,
                    "intr_rate2": 3.75
                },
            ]
        }
    ]
"""


# 금융 데이터 전처리 프로세스
def data_preprocessing(data):
    if data.get("result", {}).get("prdt_div", "") == "D":
        prd_type = "D"
    else:
        prd_type = "S"
    # 금융 상품 전처리
    prd_field_names = [field.name for field in Product._meta.fields]
    cleaned_prd_list = []

    # 상품 리스트 추출
    prd_list = data.get("result", {}).get("baseList", [])
    for prd in prd_list:
        prd_temp = {}
        for key, value in prd.items():
            if key in prd_field_names or key == 'fin_co_no':
                if key == 'fin_co_no':
                    prd_temp["ord_num"] = value
                    continue
                prd_temp[key] = value
        prd_temp["prd_type"] = prd_type
        cleaned_prd_list.append(prd_temp)
    # 옵션 상품 전처리
    opt_field_names = [field.name for field in Option._meta.fields]
    opt_field_names.append('fin_prdt_cd')
    cleaned_opt_list = []
    # 옵션 리스트추출
    opt_list = data.get("result", {}).get("optionList", [])
    for opt in opt_list:
        opt_temp = {}
        for key, value in opt.items():
            if key in opt_field_names:
                opt_temp[key] = value
        cleaned_opt_list.append(opt_temp)
    return cleaned_prd_list, cleaned_opt_list
