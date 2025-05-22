from mydata.models import Card, CardApproval, CardBill, CardBillDetail


# 마이 데이터 전처리 프로세스
def data_preprocessing(data):
    # 카드 리스트 담기
    prd_field_names = [field.name for field in DepositProducts._meta.fields]
    cleaned_prd_list = []
    # 상품 리스트 추출
    prd_list = data.get("result", {}).get("baseList", [])
    for prd in prd_list:
        prd_temp = {}
        for key, value in prd.items():
            if key in prd_field_names:
                prd_temp[key] = value
        cleaned_prd_list.append(prd_temp)
    # 옵션 상품 전처리
    opt_field_names = [field.name for field in DepositOptions._meta.fields]
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