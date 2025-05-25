from mydata.models import Card
from mydata.serializers import CardSerializer

# 응답 형식
''' 
{
    "msg": "data_generate_success",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzM1ODkwZTMtMDBmMS00MjUwLWIxYzEtODUyYzcwZjk5ZTI5IiwiZXhwIjoxNzQ3ODM0NDk1fQ.7mRRz2GkpMJ4StOYkpBGDnxOHHahGQqDSwGiml-_2Sg",
    "data": [
        {
            "card_num": "502090473849",
            "card_name": "THE iD. PLATINUM(포인트)",
            "card_type": "01",
            "org_code": "SAMSUNG",
            "user_id": "735890e3-00f1-4250-b1c1-852c70f99e29",
            "is_consent": true,
            "card_id": "CARD_3079a9a7",
            "card_member": "1"
        },
        ...
    ]
}
'''

# 모델 필드
'''
    card_id = models.CharField(max_length=100, primary_key=True, help_text="카드 식별자")
    card_num = models.CharField(max_length=20, help_text="카드번호")
    card_name = models.CharField(max_length=100, help_text="카드상품명")
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES, help_text="카드구분")
    owner_type = models.CharField(max_length=10, choices=OWNER_TYPE_CHOICES, help_text="본인/가족 구분")
    org_code = models.CharField(max_length=20, help_text="기관명")
'''

# 마이 데이터 전처리 프로세스
def data_preprocessing(data):
    # 카드 리스트 담기
    card_field_names = [field.name for field in Card._meta.fields]
    cleaned_card_list = []
    # 상품 리스트 추출
    card_list = data.get("data", {})
    jwt_token = data.get("access_token", {})
    for card in card_list:
        card_temp = {}
        for key, value in card.items():
            if key in card_field_names:
                card_temp[key] = value
        cleaned_card_list.append(card_temp)
    print(cleaned_card_list)
    # 카드 정보 저장
    serializer = CardSerializer(data=cleaned_card_list, many=True)
    if serializer.is_valid():
        serializer.save()
    
    return serializer.data, jwt_token