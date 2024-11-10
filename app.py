from flask import Flask, jsonify, request
from caferecommend import recommend_cafes as recommend_cafes_standard  # caferecommend.py의 함수 임포트
import json
from flask_cors import CORS  # CORS import 추가

app = Flask(__name__)
CORS(app)  # CORS 설정 추가

@app.route('/api/recommend', methods=['POST'])
def recommend():
    user_preferences = request.json.get('categories')
    recommendations = recommend_cafes_standard(user_preferences)
    return app.response_class(
        response=json.dumps(recommendations, ensure_ascii=False),
        mimetype='application/json'

    )

if __name__ == '__main__':
    app.run(debug=True, port=5001)
