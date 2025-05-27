import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from finance_recommend.models import Product
import re

def extract_product_features(product):
    # 상품 설명 텍스트 결합 - 모든 속성 포함
    product_text = f"""
    {product.fin_prdt_nm} 
    {product.ord_num} 
    {product.fin_prdt_cd} 
    {product.kor_co_nm} 
    {product.mtrt_int} 
    {product.spcl_cnd or ''} 
    {product.etc_note or ''} 
    {product.join_member or ''} 
    {product.join_way or ''} 
    {product.prd_type} 
    {product.join_deny or ''}
    """
    
    # 특수문자 제거 및 공백 정리
    product_text = re.sub(r'[^\w\s]', ' ', product_text)
    product_text = re.sub(r'\s+', ' ', product_text).strip()
    return product_text

def recommend_products_by_text(user_query, products, top_n=3):
    """
    사용자 쿼리와 상품 텍스트 간의 코사인 유사도를 계산하여 상위 N개 상품을 추천합니다.
    
    Args:
        user_query (str): 사용자 검색어 또는 선호도 설명
        products (QuerySet): 상품 목록
        top_n (int): 추천할 상품 수
        
    Returns:
        list: 추천 상품 목록 (각 항목은 상품 객체와 유사도 점수를 포함한 딕셔너리)
    """
    # 상품이 없는 경우 빈 리스트 반환
    if not products:
        return []
    
    # 모든 상품 텍스트 수집
    product_texts = [extract_product_features(product) for product in products]
    
    # 텍스트가 비어있는지 확인
    valid_texts = [text for text in product_texts if text.strip()]
    if not valid_texts:
        # 텍스트가 없는 경우 금리 기준으로 정렬
        product_rates = []
        for product in products:
            best_option = product.options.order_by('-intr_rate2').first()
            rate = best_option.intr_rate2 or best_option.intr_rate or 0
            product_rates.append({
                "상품명": product.fin_prdt_nm,
                "금융사": product.kor_co_nm,
                "금융상품유형": product.prd_type,
                "금리": rate,
                "유사도": 0,
                "상품설명": product.etc_note[:100] + "..." if len(product.etc_note) > 100 else product.etc_note
            })
        return sorted(product_rates, key=lambda x: x["금리"], reverse=True)[:top_n]
    
    try:
        # TF-IDF 벡터화 (불용어 설정 변경)
        vectorizer = TfidfVectorizer(
            stop_words=None,  # 불용어 제거 비활성화
            min_df=1,         # 최소 문서 빈도
            max_features=5000 # 최대 특성 수
        )
        product_vectors = vectorizer.fit_transform(product_texts)
        
        # 사용자 쿼리 벡터화 (같은 벡터라이저 사용)
        # 쿼리 전처리
        user_query = re.sub(r'[^\w\s]', ' ', user_query)
        user_query = re.sub(r'\s+', ' ', user_query).strip()
        
        user_vector = vectorizer.transform([user_query])
        
        # 코사인 유사도 계산
        similarities = cosine_similarity(user_vector, product_vectors).flatten()
        
        # 유사도 높은 순으로 정렬
        sorted_indices = np.argsort(similarities)[::-1]
        
        # 상위 N개 추천
        recommendations = []
        for idx in sorted_indices[:top_n]:
            product = products[idx]
            sim_score = similarities[idx]
            
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
            if best_option:
                rate = best_option.intr_rate2 or best_option.intr_rate or 0
            else:
                rate = 0
            
            recommendations.append({
                "상품명": product.fin_prdt_nm,
                "금융사": product.kor_co_nm,
                "금융상품유형": product.prd_type,
                "금리": rate,
                "유사도": round(float(sim_score), 4),
                "상품설명": product.etc_note[:100] + "..." if len(product.etc_note) > 100 else product.etc_note,
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
        
        return recommendations
    
    except Exception as e:
        print(f"추천 시스템 오류: {e}")
        # 오류 발생 시 금리 기준으로 정렬
        product_rates = []
        for product in products:
            best_option = product.options.order_by('-intr_rate2').first()
            if best_option:
                rate = best_option.intr_rate2 or best_option.intr_rate or 0
            else:
                rate = 0
            product_rates.append({
                "상품명": product.fin_prdt_nm,
                "금융사": product.kor_co_nm,
                "금융상품유형": product.prd_type,
                "금리": rate,
                "오류": str(e)[:100]
            })
        return sorted(product_rates, key=lambda x: x["금리"], reverse=True)[:top_n]

def recommend_products_hybrid(user_query, product_type, save_term=None, top_n=3):
    """
    텍스트 유사도와 수치 데이터를 결합한 하이브리드 추천 시스템
    
    Args:
        user_query (str): 사용자 검색어 또는 선호도 설명
        product_type (str): 상품 유형 ("D" 또는 "S")
        save_term (int, optional): 저축 기간 (개월)
        top_n (int): 추천할 상품 수
        
    Returns:
        list: 추천 상품 목록
    """
    # 상품 유형으로 필터링 (따옴표 제거)
    if product_type.startswith('"') and product_type.endswith('"'):
        product_type = product_type[1:-1]
    
    # 상품 필터링
    products = Product.objects.filter(prd_type=product_type).prefetch_related('options')
    
    # 저축 기간이 지정된 경우 해당 기간에 맞는 옵션이 있는 상품만 필터링
    if save_term is not None:
        filtered_products = []
        for product in products:
            for option in product.options.all():
                if option.save_trm and option.save_trm.isdigit() and int(option.save_trm) == save_term:
                    filtered_products.append(product)
                    break
        products = filtered_products
    
    # 텍스트 기반 추천
    return recommend_products_by_text(user_query, products, top_n)