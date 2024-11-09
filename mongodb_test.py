from pymongo import MongoClient

# MongoDB 클라이언트 설정
client = MongoClient("mongodb+srv://champ7474:gnbalpha1@cluster0.vztxs.mongodb.net/")
db = client["your_database_name"]  # MongoDB 데이터베이스 이름 입력
cafes_collection = db["caves"]     # MongoDB 컬렉션 이름 입력

# MongoDB에서 데이터 가져오기 함수
def fetch_cafes():
    try:
        # 모든 카페 데이터 가져오기
        cafes = list(cafes_collection.find())
        
        # 가져온 데이터 출력 (콘솔에 확인용)
        print("카페 데이터를 성공적으로 가져왔습니다.")
        for cafe in cafes:
            print(cafe)  # 각 카페 데이터 출력
        return cafes

    except Exception as e:
        print("MongoDB에서 데이터를 가져오는 중 오류 발생:", e)

# 함수 호출하여 데이터 가져오기
if __name__ == "__main__":
    fetch_cafes()
