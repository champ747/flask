def recommend_cafes_with_weights(user_preference_atmosphere, atmosphere_weight, service_weight):
    # 예시 데이터: 카페 리스트
    cafes = [
        {'name': 'Cafe A', 'atmosphere': 1, 'service_rating': 4.5},
        {'name': 'Cafe B', 'atmosphere': 3, 'service_rating': 4.0},
        {'name': 'Cafe C', 'atmosphere': 2, 'service_rating': 3.8},
        {'name': 'Cafe D', 'atmosphere': 5, 'service_rating': 4.8},
        {'name': 'Cafe E', 'atmosphere': 1, 'service_rating': 4.7},
        {'name': 'Cafe F', 'atmosphere': 6, 'service_rating': 4.1},
        {'name': 'Cafe G', 'atmosphere': 3, 'service_rating': 3.9},
        {'name': 'Cafe H', 'atmosphere': 4, 'service_rating': 3.5}
    ]
    
    # 최대 서비스 평점 정의 (기준점)
    max_service_rating = 5.0

    
    # 점수를 계산하여 카페별 점수를 저장할 리스트
    recommendations = []
    
    for cafe in cafes:
        # 분위기 점수 계산 (일치하면 0점, 불일치하면 1점)
        atmosphere_diff = 0 if user_preference_atmosphere == cafe['atmosphere'] else 1
        
        # 서비스 점수 계산 (높을수록 선호)
        service_diff = max_service_rating - cafe['service_rating']
        
        # 최종 점수 계산
        final_score = (atmosphere_diff * atmosphere_weight) + (service_diff * service_weight)
        
        # 카페 이름과 최종 점수를 리스트에 추가
        recommendations.append({
            'name': cafe['name'],
            'location': cafe.get('location', 'unknown'),
            'final_score': final_score
        })
    

    
    # 점수를 기준으로 카페 정렬 (오름차순으로 정렬)
    recommendations = sorted(recommendations, key=lambda x: x['final_score'])
    
    return recommendations

# 사용자가 선호하는 분위기 (범주형 값)
user_preference_atmosphere = 1  # 사용자가 선호하는 카페 분위기

# 사용자의 중요도(가중치) 설정
atmosphere_weight = 0.7
service_weight = 0.3

# 추천 결과 출력(점수가 낮으면 낮을수록 원하는 카페에 가까움)
recommendations = recommend_cafes_with_weights(user_preference_atmosphere, atmosphere_weight, service_weight)
for r in recommendations:
    print(f"카페: {r['name']}, 점수: {r['final_score']}")
