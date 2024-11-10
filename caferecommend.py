from pymongo import MongoClient
from bson import ObjectId

# MongoDB 클라이언트 설정
client = MongoClient("mongodb+srv://champ7474:gnbalpha1@cluster0.vztxs.mongodb.net/")
db = client["test"]  # MongoDB 데이터베이스 이름 입력
cafes_collection = db["caves"]  # MongoDB 컬렉션 이름 입력

# atmosphere_weight와 service_weight를 고정 값으로 설정
ATMOSPHERE_WEIGHT = 0.4
SERVICE_WEIGHT = 0.6

# 모든 카페에 대해 추천 점수를 계산하는 함수
def recommend_cafes(user_preferences):
    user_preference_categories = user_preferences.get('categories', [])
    
    # MongoDB에서 모든 카페 데이터 가져오기
    cafes = list(cafes_collection.find({}, {'_id': 1, 'name': 1, 'image': 1, 'rating': 1, 'location': 1, 'category': 1}))

    # 최대 서비스 평점 정의 (기준점)
    max_service_rating = 5.0
    recommendations = []
    
    for cafe in cafes:
        cafe_id = str(cafe['_id'])  # MongoDB ObjectID를 문자열로 변환

        # 사용자 선호 category와 카페의 대표 category 비교 및 가중치 계산
        match_score = 0
        for index, user_category in enumerate(user_preference_categories):
            # 사용자 선호도 순서에 따라 가중치를 계산
            weight = ATMOSPHERE_WEIGHT * (len(user_preference_categories) - index)
            if user_category in cafe.get('category', []):
                match_score += weight

        # 카페의 서비스 평점 차이 계산
        service_diff = max_service_rating - float(cafe.get('rating', 0))
        
        # 최종 점수 계산
        final_score = match_score + (service_diff * SERVICE_WEIGHT)
        
        # 추천 리스트에 추가, 리뷰 수는 0으로 설정
        recommendations.append({
            "id": cafe_id,
            "name": cafe.get('name', 'Unknown'),
            "image": cafe.get('image', 'https://example.com/default.jpg'),
            "rating": cafe.get('rating', 0),
            "reviews": 0,  # 리뷰 수는 0으로 설정
            "location": cafe.get('location', '위치 정보 없음'),
            "final_score": round(final_score, 2)
        })

    # 점수를 기준으로 카페 정렬 후 상위 30개만 반환
    recommendations = sorted(recommendations, key=lambda x: x['final_score'], reverse=True)[:30]
    
    # 결과 반환
    return recommendations

# 테스트용으로 사용자 선호도 입력
user_preferences = {
    "categories": ["사진찍기 좋은", "사람 많은", "넓은", "조용한", "경치가 좋은", "인테리어 예쁜"]
}

# 추천 결과 가져오기
final_recommendations = recommend_cafes(user_preferences)
print("Final Top 30 Cafe Recommendations:", final_recommendations)
