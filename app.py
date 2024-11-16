from flask import Flask, jsonify, request
from caferecommend import recommend_cafes as recommend_cafes_standard  # caferecommend.py의 함수 임포트
from chatbot import recommend_cafes as recommend_cafes_chatbot  # chatbot.py의 추천 함수 임포트
import json
from flask_cors import CORS  # CORS import 추가

app = Flask(__name__)
CORS(app)  # CORS 설정 추가

# 기존 카페 추천 API
@app.route('/api/recommend', methods=['POST'])
def recommend():
    user_preferences = request.json.get('categories', [])
    recommendations = recommend_cafes_standard({"categories": user_preferences})
    return app.response_class(
        response=json.dumps(recommendations, ensure_ascii=False),
        mimetype='application/json'
    )

# 챗봇 추천 API
@app.route('/api/chatbot', methods=['POST'])
def chatbot_recommend():
    user_input = request.json.get('user_input', '')
    if not user_input:
        return jsonify({"error": "user_input is required"}), 400

    recommendations = recommend_cafes_chatbot(user_input)
    return jsonify({"recommendations": recommendations})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
