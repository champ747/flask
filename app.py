from flask import Flask, jsonify, request
from caferecommend import recommend_cafes  # caferecommend.py의 함수 임포트

app = Flask(__name__)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    # 프론트엔드에서 전송한 사용자 선호도 데이터를 가져옴
    user_preferences = request.json.get('preferences')
    
    # 추천 알고리즘 호출
    recommendations = recommend_cafes(user_preferences)
    
    # 추천 결과 반환
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
