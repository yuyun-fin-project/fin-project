from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from .utils.spot.spot_api import spot_api
from .utils.prd.api_call import api_call as prd_api
from .utils.prd.data_preprocessing import data_preprocessing as preprocess_prd_data
from .utils.spot.preprocessing import data_preprocessing as preprocess_spot_data
from .utils.create_spotproduct import create_all_spot_products

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Option, Gold, Oil, Carbon, SpotProductBookmark, SpotProduct, ProductBookmark
from .serializers import ProductSerializer, OptionSerializer, GoldSerializer, OilSerializer, CarbonSerializer
from .utils.cosine_similarity import recommend_products

from datetime import datetime, timedelta
from pprint import pprint
# Create your views here.
@api_view(['GET'])
def get_prd(request):
    # 호출
    deposit_json, saving_json = prd_api()
    # 전처리
    deposit_json, deposit_opt_json = preprocess_prd_data(deposit_json)
    saving_json, saving_opt_json = preprocess_prd_data(saving_json)

    # 합치기
    all_prd_json = deposit_json + saving_json
    all_opt_json = deposit_opt_json + saving_opt_json
    pprint(all_prd_json)
    # 한번에 저장
    prd_serializer = ProductSerializer(data=all_prd_json, many=True)
    if prd_serializer.is_valid(raise_exception=True):
        prd_serializer.save()
    
    opt_serializer = OptionSerializer(data=all_opt_json, many=True)
    if opt_serializer.is_valid(raise_exception=True):
        opt_serializer.save()

    return Response(
        {
            "count": len(all_prd_json),
            "results":
            {
                "prd": prd_serializer.data, 
                "opt": opt_serializer.data,
            }
        }, 
        status=status.HTTP_200_OK
        )


@api_view(['GET'])
def get_spot(request, start_date=None, end_date=None):
    from datetime import datetime, timedelta
    from django.utils import timezone

    # start_date가 없으면 GET 파라미터 확인, 최종적으로 기본값 지정
    if not start_date:
        start_date = request.GET.get('start_date', (timezone.now().date() - timedelta(days=30)).strftime("%Y%m%d"))

    # end_date도 마찬가지로 처리
    if not end_date:
        end_date = request.GET.get('end_date', timezone.now().date().strftime("%Y%m%d"))

    # 문자열을 datetime.date로 변환
    start_date = datetime.strptime(start_date, "%Y%m%d").date()
    end_date = datetime.strptime(end_date, "%Y%m%d").date()

    formatted_start_date = start_date.strftime("%Y%m%d")
    formatted_end_date = end_date.strftime("%Y%m%d")

    api_responses = spot_api(formatted_start_date, formatted_end_date)

    # serializer 세팅
    serializers = [
        (Gold, GoldSerializer, "Gold"), 
        (Oil, OilSerializer, "Oil"), 
        (Carbon, CarbonSerializer, "Carbon")
    ]

    # 응답값 자리 미리 확보
    result = [[] for _ in range(3)]  # Gold, Oil, Carbon 자리 확보
    print(api_responses)
    for idx, (response, spot) in enumerate(zip(api_responses, serializers)):
        print(f"Processing {spot[2]}...")
        try:
            # JSON 파싱 안전 처리
            try:
                data = response.json()
            except Exception as e:
                print(f"⚠️ {spot[2]} 응답 JSON 파싱 실패: {e}")
                continue  # 이 API는 건너뛰기

            spot_data = preprocess_spot_data(data, spot[0], spot[2])
            serializer = spot[1](data=spot_data, many=True)
            
            if serializer.is_valid(raise_exception=True):
                try:
                    serializer.save(spot_type=spot[2])
                    result[idx] = serializer.data  # 안전하게 자리 채우기
                except Exception as e:
                    print(f"🔥 {spot[2]} 저장 중 오류: {e}")
                    # 실패해도 자리 유지 (빈 리스트)
        except Exception as e:
            print(f"⚠️ {spot[2]} 처리 중 예외: {e}")
            # 실패해도 자리 유지 (빈 리스트)
    create_all_spot_products()
    return Response(
        {
            "items": {
                "Gold": result[0],
                "Oil": result[1],
                "Carbon": result[2]
            }
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product_bookmark(request, product_id):
    user = request.user
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    bookmark, created = ProductBookmark.objects.get_or_create(
        user=user, 
        product=product
        )
    if not created:
        bookmark.delete()
        return Response({'message': 'Bookmark removed'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Bookmark added'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def spot_bookmark(request, spot_product_id):
    user = request.user
    try:
        spot_product = SpotProduct.objects.get(pk=spot_product_id)
    except SpotProduct.DoesNotExist:
        return Response({'error': 'SpotProduct not found'}, status=status.HTTP_404_NOT_FOUND)

    bookmark, created = SpotProductBookmark.objects.get_or_create(user=user, spot_product=spot_product)
    if not created:
        bookmark.delete()
        return Response({'message': 'Bookmark removed'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Bookmark added'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def spot_bookmark_list(request):
    bookmarks = SpotProductBookmark.objects.filter(user=request.user)
    data = [
        {
            'spot_product_id': b.spot_product.id,
            'spot_product_name': b.spot_product.name,
            'spot_type': b.spot_product.spot_type,
            'created_at': b.created_at
        }
        for b in bookmarks
    ]
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_bookmark_list(request):
    bookmarks = ProductBookmark.objects.filter(user=request.user)
    data = [
        {
            'product_id': b.product.id,
            'product_name': b.product.fin_prdt_nm,
            'created_at': b.created_at,
            'prd_type': b.product.prd_type,
        }
        for b in bookmarks
    ]
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_view(request):
    # 예: GET 파라미터로 입력 받음
    preferred_type = request.GET.get("preferred_type", "D")
    join_deny = int(request.GET.get("join_deny", 1))
    save_trm = int(request.GET.get("save_trm", 12))
    target_rate = float(request.GET.get("target_rate", 0.03))
    target_rate2 = float(request.GET.get("target_rate2", 0.04))

    user_input = {
        "preferred_type": preferred_type,
        "join_deny": join_deny,
        "save_trm": save_trm,
        "target_rate": target_rate,
        "target_rate2": target_rate2
    }

    recommended = recommend_products(user_input)

    # JSON으로 상품명, 금융사명, 유사도 출력
    data = [
        {
            "상품명": r["product"].fin_prdt_nm,
            "금융사": r["product"].kor_co_nm,
            "유사도": round(r["similarity"], 4)
        } for r in recommended
    ]

    return Response(data)


