import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from finance_recommend.models import Product
from scipy.spatial.distance import cdist

# def product_to_vector(product):
#     prd_type = 1 if product.prd_type == "D" else 0
#     join_deny = int(product.join_deny) if product.join_deny else 1

#     # 옵션 중 최고 금리 선택 (없으면 0)
#     best_option = product.options.order_by('-intr_rate2').first()
#     if best_option:
#         save_trm = int(best_option.save_trm) if best_option.save_trm and best_option.save_trm.isdigit() else 0
#         intr_rate = best_option.intr_rate or 0
#         intr_rate2 = best_option.intr_rate2 or 0
#     else:
#         save_trm = 0
#         intr_rate = 0
#         intr_rate2 = 0

#     return [prd_type, join_deny, save_trm, intr_rate, intr_rate2]

# def user_to_vector(preferred_type, join_deny, save_trm, target_rate, target_rate2):
#     prd_type = 1 if preferred_type == "D" else 0
#     return [prd_type, join_deny, save_trm, target_rate, target_rate2]

# def recommend_products(user_input, top_n=3):
#     user_vec = user_to_vector(
#         user_input["preferred_type"],
#         user_input["join_deny"],
#         user_input["save_trm"],
#         user_input["target_rate"],
#         user_input["target_rate2"]
#     )
#     user_vec = np.array(user_vec).reshape(1, -1)

#     products = Product.objects.prefetch_related('options').all()
#     product_list = []
#     vectors = []

#     for product in products:
#         vector = product_to_vector(product)
#         vectors.append(vector)
#         product_list.append(product)

#     product_vectors = np.array(vectors)
#     similarities = cosine_similarity(user_vec, product_vectors).flatten()

#     # 유사도 높은 순으로 정렬
#     sorted_indices = np.argsort(similarities)[::-1]
#     top_products = [product_list[i] for i in sorted_indices[:top_n]]

#     # 유사도 함께 반환
#     recommendations = []
#     for idx in sorted_indices[:top_n]:
#         product = product_list[idx]
#         sim_score = similarities[idx]
#         recommendations.append({
#             "product": product,
#             "similarity": sim_score
#         })

#     return recommendations

def product_to_vector(product):
    prd_type_num = 1 if product.prd_type == "D" else 2

    # 옵션 중 최고 금리 선택
    best_option = product.options.order_by('-intr_rate2').first()
    if best_option:
        save_trm = int(best_option.save_trm) if best_option.save_trm and best_option.save_trm.isdigit() else 0
    else:
        save_trm = 0

    # 간단히 월 저축 가능액은 상품 속성으로 없으므로 평균값 임의 사용
    monthly_saving = 50  # 예시 (혹은 DB 컬럼으로 확장할 수 있어!)

    return [prd_type_num, save_trm, monthly_saving]

def user_to_vector(product_type, save_trm, monthly_saving):
    prd_type_num = 1 if product_type == "D" else 2
    return [prd_type_num, save_trm, monthly_saving]

def recommend_products(user_input, top_n=3):
    user_vec = user_to_vector(
        user_input["product_type"],
        user_input["save_trm"],
        user_input["monthly_saving"]
    )
    user_vec = np.array(user_vec).reshape(1, -1)

    products = Product.objects.prefetch_related('options').all()
    product_list = []
    vectors = []

    for product in products:
        vector = product_to_vector(product)
        vectors.append(vector)
        product_list.append(product)

    product_vectors = np.array(vectors)
    distances = cdist(user_vec, product_vectors, metric='euclidean').flatten()

    sorted_indices = np.argsort(distances)
    recommendations = []
    for idx in sorted_indices[:top_n]:
        product = product_list[idx]
        distance = round(float(distances[idx]), 4)
        recommendations.append({
            "product": product,
            "distance": distance
        })

    return recommendations