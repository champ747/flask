from flask import Flask, jsonify, request
from caferecommend import recommend_cafes as recommend_cafes_standard  # caferecommend.py의 함수 임포트
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

from chatbot import recommend_cafes  # chatbot.py의 함수 임포트

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('user_input', '')
    response = recommend_cafes(user_input)
    return jsonify({"recommendations": response})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
