# Python 이미지
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 업데이트 및 MeCab 관련 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    openjdk-11-jdk \
    g++ \
    make \
    mecab \
    mecab-ipadic-utf8 \
    mecab-ko \
    mecab-ko-dic-utf8 \
    mecab-naist-jdic \
    libmecab-dev \
    mecab-ipadic \
    mecab-jumandic \
    mecab-unidic \
    && apt-get clean

# Mecab Python 라이브러리 설치
RUN pip install konlpy mecab-python3 pymongo scikit-learn

# 프로젝트 파일 복사
COPY . .

# 환경 변수 설정
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV PATH $JAVA_HOME/bin:$PATH

# MeCab 사전 경로를 지정하여 MeCab 인스턴스 생성
ENV MECAB_LIBRARY_PATH /usr/local/lib/libmecab.so
ENV MECAB_DICDIR /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ko-dic

# 앱 실행
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
