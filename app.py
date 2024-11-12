from flask import Flask, jsonify, request
from caferecommend import recommend_cafes as recommend_cafes_standard  # caferecommend.py의 함수 임포트
import json
from flask_cors import CORS  # CORS import 추가

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # 모든 도메인에 대해 /api/* 경로 허용

@app.route('/api/recommend', methods=['POST'])
def recommend():
    user_preferences = request.json  # request.json이 이미 딕셔너리인지 확인
    if not isinstance(user_preferences, dict):
        user_preferences = {"categories": user_preferences}  # user_preferences가 리스트인 경우 딕셔너리로 감싸기

    recommendations = recommend_cafes_standard(user_preferences)
    return app.response_class(
        response=json.dumps(recommendations, ensure_ascii=False),
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.run(debug=True, port=5001)
