import pandas as pd
import random

# CSV 파일 경로
model_generated_summaries_file = "./model_generated_summaries_ver6.csv"
blog_full_results_file = "./blog_full_results.csv"

# 데이터셋 읽기
model_generated_summaries = pd.read_csv(model_generated_summaries_file)
blog_full_results = pd.read_csv(blog_full_results_file)

# Title을 키로 하여 요약 데이터를 매핑
summary_map = model_generated_summaries.set_index('Title')['generated_summary'].to_dict()

def get_random_blogs(n=10):
    """
    랜덤으로 n개의 블로그 데이터를 반환합니다.
    """
    results = []
    count = 0
    for _, row in blog_full_results.iterrows():
        title = row['Title']
        url = row['Link']
        summary = summary_map.get(title, "요약 정보가 없습니다.")  # 매핑된 요약 가져오기
        count+1
        results.append({
            "_id" : count
            "title": title,
            "url": url,
            "summary": summary
        })

    # 랜덤으로 n개 선택
    return random.sample(results, min(len(results), n))
