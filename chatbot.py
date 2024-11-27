from kiwipiepy import Kiwi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient

# MongoDB 클라우드 연결 설정
client = MongoClient("mongodb+srv://suyeon10187:gnbalpha1@cluster0.vztxs.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true")
db = client['test']  # 데이터베이스 이름
collection = db['caves']  # 컬렉션 이름

# Kiwi 초기화 및 사용자 사전 추가
kiwi = Kiwi()

# 사용자 사전 등록
location_keywords = [
    # 중구
    '교동', '동성로', '삼덕동', '남산동', '대봉동', '달성공원', '계산동', '서문시장',
    # 서구
    '내당동', '비산동', '평리동', '중리동', '상리동',
    # 동구
    '동촌', '방촌', '신암동', '신천동', '효목동', '지묘동', '불로동', '각산동', '안심',
    # 북구
    '칠성동', '침산동', '복현동', '검단동', '산격동', '노원동', '동변동', '읍내동', '구암동', '대현동', '관음동', '태전동', '국우동',
    # 남구
    '봉덕동', '대명동', '이천동', '대덕산성', '앞산',
    # 수성구
    '수성못', '범어동', '만촌동', '수성동', '황금동', '지산동', '범물동', '파동', '상동', '중동', '두산동', '고산동',
    # 달서구
    '상인동', '월성동', '진천동', '대곡동', '도원동', '송현동', '용산동', '이곡동', '신당동', '성서', '호산동',
    # 달성군
    '화원읍', '옥포읍', '현풍읍', '가창면', '구지면', '하빈면', '논공읍', '유가읍', '다사읍',
    # 기타 주요 지역
     '김광석길', '앞산', '동촌', '이월드', '칠곡', '팔공산', '북성로'
]

custom_keywords = [
# 중구
    '교동', '동성로', '삼덕동', '남산동', '대봉동', '달성공원', '계산동', '서문시장',
    # 서구
    '내당동', '비산동', '평리동', '중리동', '상리동',
    # 동구
    '동촌', '방촌', '신암동', '신천동', '효목동', '지묘동', '불로동', '각산동', '안심',
    # 북구
    '칠성동', '침산동', '복현동', '검단동', '산격동', '노원동', '동변동', '읍내동', '구암동', '대현동', '관음동', '태전동', '국우동',
    # 남구
    '봉덕동', '대명동', '이천동', '대덕산성', '앞산',
    # 수성구
    '수성못', '범어동', '만촌동', '수성동', '황금동', '지산동', '범물동', '파동', '상동', '중동', '두산동', '고산동',
    # 달서구
    '상인동', '월성동', '진천동', '대곡동', '도원동', '송현동', '용산동', '이곡동', '신당동', '성서', '호산동',
    # 달성군
    '화원읍', '옥포읍', '현풍읍', '가창면', '구지면', '하빈면', '논공읍', '유가읍', '다사읍',
    # 기타 주요 지역
    '김광석길', '앞산', '동촌', '이월드', '칠곡', '팔공산', '북성로',
    # 조용한 키워드
    '조용','조용한'
]
for keyword in custom_keywords:
    kiwi.add_user_word(keyword, 'NNG')  # 일반 명사로 추가

# 리뷰와 카테고리 키워드를 형태소로 분석하는 함수
def tokenize_with_weights(reviews, categories):
    tokens = []
    for review in reviews:
        if isinstance(review, str):
            result = kiwi.tokenize(review)
            tokens.extend([word for word, tag, _, _ in result if tag in ['NNG', 'VA', 'NNP']])
    tokens.extend(categories)
    return ' '.join(tokens)

# 사용자 입력에서 명사와 형용사 추출
def process_user_input(user_input):
    tokens = [word for word, tag, _, _ in kiwi.tokenize(user_input) if tag in ['NNG', 'VA', 'NNP']]
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

# 추천 함수 (Flask API와 연동 가능하도록 수정)
def recommend_cafes(user_input):
    processed_input = process_user_input(user_input)

    # 지역명 추출
    location = None
    tokens = processed_input.split()
    for token in tokens:
        if token in location_keywords:
            location = token
            break

    # '조용한' 입력 포함 시 필터링
    contains_quiet = "조용한" in tokens
    if contains_quiet:
        filtered_cafes = [cafe for cafe in cafes if cafe.get('is_quiet', False)]
    else:
        filtered_cafes = cafes

    # 지역명 필터링
    if location:
        filtered_cafes = [cafe for cafe in filtered_cafes if location in cafe['address']]

    # TF-IDF 유사도 계산
    if filtered_cafes:
        similarities = calculate_tfidf_similarity(processed_input, filtered_cafes)
        top_cafes = sorted(zip(filtered_cafes, similarities), key=lambda x: x[1], reverse=True)

        # 중복 제거 및 상위 5개 선택
        seen = set()
        unique_cafes = []
        for cafe, similarity in top_cafes:
            if cafe['name'] not in seen:
                unique_cafes.append((cafe, similarity))
                seen.add(cafe['name'])
        if len(unique_cafes) < 3:
            extra_cafes = [cafe for cafe in cafes if cafe['name'] not in seen]
            unique_cafes.extend(zip(extra_cafes, [0] * (3 - len(unique_cafes))))

        recommendations = [{"name": cafe['name'], "address": cafe['address']} for cafe, _ in unique_cafes[:5]]
    else:
        recommendations = []

    return recommendations
