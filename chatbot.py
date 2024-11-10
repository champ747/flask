import json
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient

# MongoDB 클라우드 연결 설정
client = MongoClient("mongodb+srv://champ7474:gnbalpha1@cluster0.vztxs.mongodb.net/")
db = client['test']                       # 데이터베이스 이름
collection = db['caves']                 # 컬렉션 이름

# 형태소 분석기 초기화
okt = Okt()

# 리뷰와 카테고리 키워드를 형태소로 분석하는 함수 (가중치 없이)
def tokenize_with_weights(reviews, categories):
    tokens = []

    # 리뷰 텍스트에서 명사와 형용사만 추출
    for review in reviews:
        if isinstance(review, str):
            tokens.extend([word for word, tag in okt.pos(review) if tag in ['Noun', 'Adjective']])

    # 각 카테고리를 가중치 없이 한 번씩 추가
    tokens.extend(categories)

    return ' '.join(tokens)

# MongoDB에서 데이터 가져오기
def load_data_from_mongo():
    data = collection.find()  # 모든 문서 가져오기
    cafes = []
    for entry in data:
        reviews = [entry.get('review1', ''), entry.get('review2', ''), entry.get('review3', '')]
        categories = entry.get('category', [])
        tokenized_text = tokenize_with_weights(reviews, categories)
        cafes.append({
            'name': entry['name'],
            'address': entry['address'],
            'tokenized_text': tokenized_text,
            'is_quiet': '조용한' in categories
        })
    return cafes

# MongoDB에서 로드한 데이터
cafes = load_data_from_mongo()

# 사용자 입력을 형태소로 분석하는 함수
def process_user_input(user_input):
    tokens = [word for word, tag in okt.pos(user_input) if tag in ['Noun', 'Adjective']]
    return ' '.join(tokens)

# TF-IDF 유사도 계산 함수
def calculate_tfidf_similarity(user_input, cafes):
    documents = [cafe['tokenized_text'] for cafe in cafes] + [user_input]
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()
    user_vector = vectors[-1]
    cafe_vectors = vectors[:-1]
    similarities = cosine_similarity([user_vector], cafe_vectors)[0]
    return similarities

# 추천 함수
def recommend_cafes_from_chatbot(user_input):
    processed_input = process_user_input(user_input)

    # 지역명 추출
    location_keywords = [
        '교동', '동성로', '반월당', '북구', '서구', '김광석길', '수성못',
        '앞산', '서문시장', '이월드', '북성로', '수성구', '남구', '달서구',
        '대봉', '삼덕', '침산', '상인', '신매', '시지', '범어',
        '대현', '산격', '평리', '두류', '월성', '내당', '대봉동', '삼덕동', '침산동', '상인동', '신매동', '범어동',
        '대현동', '산격동', '평리동', '두류동', '월성동', '내당동'
    ]
    location = None
    tokens = processed_input.split()
    for token in tokens:
        if token in location_keywords:
            location = token
            break

    # '조용' 입력 포함 시 조용한 속성 필터링
    filtered_cafes = [cafe for cafe in cafes if cafe['is_quiet']] if "조용" in tokens else cafes

    # 지역명 필터링: 주소나 이름에 해당 지역명이 포함된 경우 필터링
    if location:
        filtered_cafes = [cafe for cafe in filtered_cafes if location in cafe['address'] or location in cafe['name']]

    # 필터링된 카페에 대해 TF-IDF 유사도 계산
    if filtered_cafes:
        similarities = calculate_tfidf_similarity(processed_input, filtered_cafes)
        top_cafes = sorted(zip(filtered_cafes, similarities), key=lambda x: x[1], reverse=True)

        # 중복된 카페 제거
        seen = set()
        unique_cafes = []
        for cafe, similarity in top_cafes:
            if cafe['name'] not in seen:
                unique_cafes.append((cafe, similarity))
                seen.add(cafe['name'])

        # 3개 미만일 경우, 나머지를 일반 카페로 채우기
        if len(unique_cafes) < 3:
            extra_cafes = [cafe for cafe in cafes if cafe['name'] not in seen]
            unique_cafes.extend(zip(extra_cafes, [0] * (3 - len(unique_cafes))))

        recommendations = [f"{cafe['name']} (주소: {cafe['address']})" for cafe, _ in unique_cafes[:3]]
    else:
        recommendations = ["추천할 카페가 없습니다."]

    return f"추천하는 카페는 다음과 같습니다:\n" + '\n'.join(recommendations)

# 추천 반복 실행
while True:
    user_input = input("원하는 분위기와 지역을 나타내는 단어나 형용사를 입력해 주세요 (종료하려면 'exit' 입력): ")
    if user_input.lower() == "exit":
        break

    recommendations = recommend_cafes(user_input)
    print(f"\n{recommendations}\n")
