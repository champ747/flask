from pymongo import MongoClient
import requests

# MongoDB 클라이언트 설정
client = MongoClient("mongodb+srv://champ7474:gnbalpha1@cluster0.vztxs.mongodb.net/")
db = client["test"]
cafes_collection = db["caves"]

ATMOSPHERE_WEIGHT = 0.4
SERVICE_WEIGHT = 0.6

# 리뷰 수를 가져오는 함수 (예: 더미 함수로 설정)
def get_review_count(cafe_id):
    return 0  # 백엔드 연결이 되지 않으므로 기본값 0 사용

# 모든 카페에 대해 추천 점수를 계산하는 함수
def recommend_cafes(user_preferences):
    cafes = list(cafes_collection.find({}, {'_id': 1, 'name': 1, 'image': 1, 'rating': 1, 'location': 1, 'category': 1}))

    max_service_rating = 5.0
    recommendations = []

    for cafe in cafes:
        cafe_id = str(cafe['_id'])
        review_count = get_review_count(cafe_id)

        match_score = sum(
            ATMOSPHERE_WEIGHT * (len(user_preferences) - index)
            for index, user_category in enumerate(user_preferences)
            if user_category in cafe.get('category', [])
        )
        
        # 카페의 평점 (rating)을 숫자로 변환하여 사용
        service_rating = float(cafe.get('rating', 0))
        service_diff = max_service_rating - service_rating
        final_score = match_score + (service_diff * SERVICE_WEIGHT)
        
        recommendations.append({
            "id": cafe_id,
            "name": cafe.get('name', 'Unknown'),
            "image": cafe.get('image', 'https://example.com/default.jpg'),
            "rating": service_rating,
            "reviews": review_count,
            "location": cafe.get('location', '위치 정보 없음'),
            "final_score": round(final_score, 2)
        })

    recommendations = sorted(recommendations, key=lambda x: x['final_score'], reverse=True)[:30]
    return recommendations
