from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.http import Http404

from .utils.cosine_similarity import recommend_products_hybrid
from .utils.spot.spot_api import spot_api
from .utils.prd.api_call import api_call as prd_api
# from .utils.prd.api_call import api_call_all_pages as prd_api_all_pages
from .utils.prd.data_preprocessing import data_preprocessing as preprocess_prd_data
from .utils.spot.preprocessing import data_preprocessing as preprocess_spot_data
from .utils.create_spotproduct import create_all_spot_products

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Option, Gold, Oil, Carbon, SpotProductBookmark, SpotProduct, ProductBookmark
from .serializers import ProductSerializer, OptionSerializer, GoldSerializer, OilSerializer, CarbonSerializer, RecommendInputSerializer
from .utils.cosine_similarity import recommend_products_by_text

from datetime import datetime, timedelta
from pprint import pprint
# Create your views here.
@api_view(['GET'])
def get_prd(request):
    # 쿼리 파라미터 가져오기
    bank = request.GET.get('bank', '').strip()
    product_type = request.GET.get('product_type', '').strip()
    sort_by = request.GET.get('sort_by', 'rate_desc').strip()
    
    # 기본 쿼리셋
    products = Product.objects.all()
    
    # 은행명 필터링
    if bank:
        products = products.filter(kor_co_nm__icontains=bank)
    
    # 상품 유형 필터링
    if product_type:
        products = products.filter(prd_type=product_type)
    
    # 모든 상품과 해당 옵션 정보를 리스트로 변환
    product_list = []
    for product in products:
        # 해당 상품의 모든 옵션 가져오기
        options = Option.objects.filter(prd=product)
        max_rate = 0
        
        # 최대 금리 계산
        for option in options:
            try:
                rate = float(option.intr_rate2) if option.intr_rate2 else float(option.intr_rate) if option.intr_rate else 0
                max_rate = max(max_rate, rate)
            except (ValueError, TypeError):
                continue
        
        product_list.append({
            'product': product,
            'max_rate': max_rate
        })
    
    # 정렬 적용
    if sort_by == 'rate_desc':
        product_list.sort(key=lambda x: x['max_rate'], reverse=True)
    elif sort_by == 'rate_asc':
        product_list.sort(key=lambda x: x['max_rate'])
    elif sort_by == 'bank':
        product_list.sort(key=lambda x: x['product'].kor_co_nm)
    
    # 정렬된 상품 ID 리스트 생성
    sorted_product_ids = [item['product'].id for item in product_list]
    
    # 정렬된 순서대로 상품과 옵션 가져오기
    from django.db.models import Case, When
    preserved_order = Case(*[When(id=id, then=pos) for pos, id in enumerate(sorted_product_ids)])
    prd = Product.objects.filter(id__in=sorted_product_ids).order_by(preserved_order)
    opt = Option.objects.filter(prd__in=sorted_product_ids)

    if not Product.objects.exists() or not Option.objects.exists():
        # 호출
        deposit_responses, saving_responses = prd_api()
        # 전처리
        for deposit in deposit_responses:
            deposit_json, deposit_opt_json = preprocess_prd_data(deposit)
            prd_serializer = ProductSerializer(data=deposit_json, many=True)
            if prd_serializer.is_valid(raise_exception=True):
                prd_serializer.save()
            
            opt_serializer = OptionSerializer(data=deposit_opt_json, many=True)
            if opt_serializer.is_valid(raise_exception=True):
                opt_serializer.save()

        for saving in saving_responses:
            saving_json, saving_opt_json = preprocess_prd_data(saving)
            prd_serializer = ProductSerializer(data=saving_json, many=True)
            if prd_serializer.is_valid(raise_exception=True):
                prd_serializer.save()
            
            opt_serializer = OptionSerializer(data=saving_opt_json, many=True)
            if opt_serializer.is_valid(raise_exception=True):
                opt_serializer.save()        
        prd = Product.objects.prefetch_related('options').all()
        opt = Option.objects.all()
    # 한번에 저장
    # prd_serializer = ProductSerializer(data=all_prd_json, many=True)
    # if prd_serializer.is_valid(raise_exception=True):
    #     prd_serializer.save()
    
    # opt_serializer = OptionSerializer(data=all_opt_json, many=True)
    # if opt_serializer.is_valid(raise_exception=True):
    #     opt_serializer.save()
    prd_serializer = ProductSerializer(prd, many=True)
    opt_serializer = OptionSerializer(opt, many=True)

    return Response(
        {
            "results":
            {
                "prd":prd_serializer.data,
                "opt":opt_serializer.data,
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
# @permission_classes([IsAuthenticated])
def recommend_view(request):
    product_type = request.GET.get("product_type", "D")
    user_query = request.GET.get("query", "")
    save_term = request.GET.get("save_term")
    
    if save_term and save_term.isdigit():
        save_term = int(save_term)
    else:
        save_term = None
    
    # 사용자 쿼리가 있는 경우 텍스트 기반 추천
    if user_query:
        recommendations = recommend_products_hybrid(
            user_query=user_query,
            product_type=product_type,
            save_term=save_term
        )
        return Response(recommendations)
    
    # 쿼리가 없는 경우 기존 방식대로 금리 기반 추천
    products = Product.objects.filter(prd_type=product_type).prefetch_related('options')

    product_rates = []
    for product in products:
        # 모든 금리 옵션 정보 가져오기
        options_data = []
        for option in product.options.all():
            options_data.append({
                'save_trm': option.save_trm,
                'intr_rate': option.intr_rate,
                'intr_rate2': option.intr_rate2,
                'intr_rate_type': option.intr_rate_type,
                'intr_rate_type_nm': option.intr_rate_type_nm
            })
        
        # 최고 금리 옵션 찾기 (표시용)
        best_option = product.options.order_by('-intr_rate2').first()
        rate = best_option.intr_rate2 or best_option.intr_rate or 0
        
        product_rates.append({
            "상품명": product.fin_prdt_nm,
            "금융사": product.kor_co_nm,
            "금융상품유형": product.prd_type,
            "금리": rate,
            "originalProduct": {
                "id": product.id,
                "fin_prdt_nm": product.fin_prdt_nm,
                "kor_co_nm": product.kor_co_nm,
                "prd_type": product.prd_type,
                "join_way": product.join_way,
                "join_deny": product.join_deny,
                "join_member": product.join_member,
                "etc_note": product.etc_note,
                "options": options_data
            }
        })

    top_products = sorted(product_rates, key=lambda x: x["금리"], reverse=True)[:3]

    return Response(top_products)

""" 쿼리문 생성하는 함수 일단 안 씀"""
@api_view(['GET'])
def get_recommendation_queries(request):
    """
    자연어 기반 금융 상품 추천 시스템을 위한 추천 쿼리 문장을 제공합니다.
    
    쿼리 파라미터:
    - type: 쿼리 유형 (deposit, savings, complex, goal, situation)
    - count: 반환할 쿼리 수 (기본값: 5)
    """
    from .scripts.sentence_recommend import get_random_query, ALL_QUERIES, DEPOSIT_QUERIES, SAVINGS_QUERIES, COMPLEX_QUERIES, GOAL_BASED_QUERIES, SITUATION_BASED_QUERIES
    
    query_type = request.GET.get('type')
    count = int(request.GET.get('count', 5))
    
    # 쿼리 타입에 따라 다른 목록 반환
    if query_type == 'all':
        # 모든 카테고리에서 랜덤 선택
        import random
        queries = random.sample(ALL_QUERIES, min(count, len(ALL_QUERIES)))
    elif query_type == 'deposit':
        import random
        queries = random.sample(DEPOSIT_QUERIES, min(count, len(DEPOSIT_QUERIES)))
    elif query_type == 'savings':
        import random
        queries = random.sample(SAVINGS_QUERIES, min(count, len(SAVINGS_QUERIES)))
    elif query_type == 'complex':
        import random
        queries = random.sample(COMPLEX_QUERIES, min(count, len(COMPLEX_QUERIES)))
    elif query_type == 'goal':
        import random
        queries = random.sample(GOAL_BASED_QUERIES, min(count, len(GOAL_BASED_QUERIES)))
    elif query_type == 'situation':
        import random
        queries = random.sample(SITUATION_BASED_QUERIES, min(count, len(SITUATION_BASED_QUERIES)))
    else:
        # 기본값: 각 카테고리에서 1개씩 선택
        import random
        queries = []
        queries.append(random.choice(DEPOSIT_QUERIES))
        queries.append(random.choice(SAVINGS_QUERIES))
        queries.append(random.choice(COMPLEX_QUERIES))
        queries.append(random.choice(GOAL_BASED_QUERIES))
        queries.append(random.choice(SITUATION_BASED_QUERIES))
        # count가 5보다 크면 추가 쿼리 랜덤 선택
        if count > 5:
            additional = random.sample(ALL_QUERIES, min(count - 5, len(ALL_QUERIES)))
            queries.extend(additional)
    
    return Response({'queries': queries})
