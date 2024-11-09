from pymongo import MongoClient
from flask import Flask, jsonify, request

app = Flask(__name__)

# MongoDB 연결 설정
client = MongoClient("mongodb+srv://champ7474:gnbalpha1@cluster0.vztxs.mongodb.net/")
db = client['test']  # 데이터베이스 이름: test
collection = db['caves']  # 컬렉션 이름: caves

def recommend_cafes_with_weights(user_preference_categories, atmosphere_weight, service_weight):
    # MongoDB에서 카페 데이터 가져오기
    cafes = list(collection.find({}, {'_id': 0, 'name': 1, 'category': 1, 'rating': 1}))

    # 최대 서비스 평점 정의 (기준점)
    max_service_rating = 5.0
    recommendations = []
    
    for cafe in cafes:
        # 사용자 선호 category와 일치하는 항목의 가중치 적용
        match_score = sum([
            atmosphere_weight if category in user_preference_categories else 0 
            for category in cafe.get('category', [])
        ])

        # 서비스 평점 계산 (높을수록 선호)
        service_diff = max_service_rating - float(cafe.get('rating', 0))
        
        # 최종 점수 계산
        final_score = match_score + (service_diff * service_weight)
        
        # 추천 리스트에 추가
        recommendations.append({
            'name': cafe['name'],
            'final_score': final_score
        })

    # 점수를 기준으로 카페 정렬 후 상위 5개만 반환
    recommendations = sorted(recommendations, key=lambda x: x['final_score'])[:5]
    
    return recommendations

@app.route('/api/recommend', methods=['POST'])
def recommend():
    # 프론트엔드에서 전송한 사용자 선호도 데이터를 가져옴
    user_preferences = request.json.get('preferences')
    user_preference_categories = user_preferences.get('categories', [])
    atmosphere_weight = user_preferences.get('atmosphere_weight', 0.7)
    service_weight = user_preferences.get('service_weight', 0.3)

    # 추천 알고리즘 호출
    recommendations = recommend_cafes_with_weights(user_preference_categories, atmosphere_weight, service_weight)
    
    # 추천 결과 반환
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
