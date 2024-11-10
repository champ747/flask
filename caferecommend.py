from pymongo import MongoClient
import requests

# MongoDB 클라이언트 설정
client = MongoClient("mongodb+srv://champ7474:gnbalpha1@cluster0.vztxs.mongodb.net/")
db = client["test"]  # MongoDB 데이터베이스 이름 입력
cafes_collection = db["caves"]  # MongoDB 컬렉션 이름 입력

# atmosphere_weight와 service_weight를 고정 값으로 설정
ATMOSPHERE_WEIGHT = 0.4
SERVICE_WEIGHT = 0.6

# 리뷰 수를 가져오는 함수
def get_review_count(cafe_id):
    url = f"https://port-0-back-m341pqyi646021b2.sel4.cloudtype.app/recommend/reviews/count/{cafe_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # 상태 코드가 200이 아닐 경우 예외 발생
        data = response.json()
        review_count = data.get('review_count', 0)  # 응답에서 리뷰 개수를 추출
        print(f"Successfully fetched review count for cafe_id {cafe_id}: {review_count}")
        return review_count
    except requests.RequestException as e:
        print(f"Error fetching review count for cafe_id {cafe_id}: {e}")
        return 0

# 특정 카페에 대한 데이터 가져오기 및 추천 점수 계산
def get_single_cafe_recommendation(cafe_id, user_preferences):
    user_preference_categories = user_preferences.get('categories', [])
    
    # MongoDB에서 해당 카페 데이터 가져오기
    cafe = cafes_collection.find_one({"_id": cafe_id}, {'_id': 1, 'name': 1, 'image': 1, 'rating': 1, 'status': 1, 'location': 1, 'category': 1})
    
    if cafe:
        review_count = get_review_count(str(cafe['_id']))  # 리뷰 개수 요청

        # 사용자 선호 category와 카페의 대표 category 비교 및 가중치 계산
        match_score = 0
        for index, user_category in enumerate(user_preference_categories):
            weight = ATMOSPHERE_WEIGHT * (len(user_preference_categories) - index)
            if user_category in cafe.get('category', []):
                match_score += weight

        # 카페의 서비스 평점 차이 계산
        max_service_rating = 5.0
        service_diff = max_service_rating - float(cafe.get('rating', 0))
        
        # 최종 점수 계산
        final_score = match_score + (service_diff * SERVICE_WEIGHT)
        
        # 결과 출력
        recommendation = {
            "id": str(cafe['_id']),
            "name": cafe.get('name', 'Unknown'),
            "image": cafe.get('image', 'https://example.com/default.jpg'),
            "rating": cafe.get('rating', 0),
            "reviews": review_count,
            "status": cafe.get('status', '정보 없음'),
            "location": cafe.get('location', '위치 정보 없음'),
            "final_score": round(final_score, 2)
        }
        print("Single Cafe Recommendation:", recommendation)
        return recommendation
    else:
        print("No cafe found with the given ID.")
        return None

# 테스트용으로 특정 카페 ID와 사용자 선호도 입력
test_cafe_id = 'your_cafe_id_here'  # 여기에 테스트할 카페의 _id 값을 입력하세요
user_preferences = {
    "categories": ["넓은", "조용한"]
}

# 추천 결과 가져오기
get_single_cafe_recommendation(test_cafe_id, user_preferences)
