from flask import Flask, jsonify, request
from caferecommend import recommend_cafes as recommend_cafes_standard  # caferecommend.py의 함수 임포트
from chatbot import recommend_cafes  # chatbot.py의 챗봇 추천 함수
import json

app = Flask(__name__)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    user_preferences = request.json.get('preferences')
    recommendations = recommend_cafes_standard(user_preferences)
    return app.response_class(
        response=json.dumps(recommendations, ensure_ascii=False),
        mimetype='application/json'
    )

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('input')
    recommendations = recommend_cafes(user_input)
    return app.response_class(
        response=json.dumps({"recommendations": recommendations}, ensure_ascii=False),
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(debug=True, port=5001)
