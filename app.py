from flask import Flask, jsonify, request
from caferecommend import recommend_cafes as recommend_cafes_standard  # caferecommend.py의 함수 임포트
from chatbot import recommend_cafes as recommend_cafes_chatbot  # chatbot.py의 추천 함수 임포트
from flask_cors import CORS  # CORS import 추가
import json

# Flask 앱 초기화
app = Flask(__name__)
CORS(app)  # CORS 설정 추가

# 카페 추천 API
@app.route('/api/recommend', methods=['POST'])
def recommend():
    """
    사용자 선호도를 기반으로 카페를 추천하는 API
    """
    try:
        user_preferences = request.json.get('categories', [])
        if not isinstance(user_preferences, list):
            return jsonify({"error": "categories must be a list"}), 400

        # 카페 추천 함수 호출
        recommendations = recommend_cafes_standard({"categories": user_preferences})
        return app.response_class(
            response=json.dumps(recommendations, ensure_ascii=False),
            mimetype='application/json'
        )
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# 챗봇 추천 API
@app.route('/api/chatbot', methods=['POST'])
def chatbot_recommend():
    try:
        user_input = request.json.get('user_input', '').strip()
        if not user_input:
            return jsonify({"error": "user_input is required"}), 400

        recommendations = recommend_cafes_chatbot(user_input)
        return app.response_class(
            response=json.dumps({"recommendations": recommendations}, ensure_ascii=False),
            mimetype='application/json'
        )
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# Flask 서버 실행
if __name__ == '__main__':
    app.run(debug=True, port=5001)
