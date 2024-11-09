from pymongo import MongoClient

# MongoDB 연결 설정
client = MongoClient("mongodb+srv://champ7474:gnbalpha1@cluster0.vztxs.mongodb.net/")
db = client['test']  # 데이터베이스 이름: test
collection = db['caves']  # 컬렉션 이름: caves

# atmosphere_weight와 service_weight를 고정 값으로 설정
ATMOSPHERE_WEIGHT = 0.4
SERVICE_WEIGHT = 0.6

def recommend_cafes(user_preferences):
    user_preference_categories = user_preferences.get('categories', [])
    
    # MongoDB에서 카페 데이터 가져오기
    cafes = list(collection.find({}, {'_id': 0, 'name': 1, 'category': 1, 'rating': 1}))

    # 최대 서비스 평점 정의 (기준점)
    max_service_rating = 5.0
    recommendations = []
    
    for cafe in cafes:
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
        
        # 추천 리스트에 추가
        recommendations.append({
            'name': cafe.get('name', 'Unknown'),  # 이름이 없는 경우 'Unknown'으로 표시
            'final_score': final_score
        })

    # 점수를 기준으로 카페 정렬 후 상위 30개만 반환
    recommendations = sorted(recommendations, key=lambda x: x['final_score'], reverse=True)[:30]
    
    return recommendations
