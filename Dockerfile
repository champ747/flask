# 기본 이미지
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    openjdk-11-jdk \
    g++ \
    make \
    mecab \
    mecab-ko \
    mecab-ko-dic \
    && apt-get clean

# konlpy와 추가 Python 라이브러리 설치
RUN pip install konlpy pymongo scikit-learn

# 프로젝트 파일 복사
COPY . .

# 환경 변수 설정
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV PATH $JAVA_HOME/bin:$PATH

# 앱 실행
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
