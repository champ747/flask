FROM python:3.9-slim

# 기본 패키지 설치 및 mecab 관련 설치
RUN apt-get update && \
    apt-get install -y build-essential curl git && \
    apt-get install -y mecab mecab-ipadic-utf8 libmecab-dev swig mecab-ko mecab-ko-dic && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean

# JAVA_HOME 설정
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV PATH $JAVA_HOME/bin:$PATH

# MeCab 한국어 사전 경로 설정
ENV MECABKO_DIC_PATH /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ko-dic

# 파이썬 패키지 설치
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . /app

# Flask 애플리케이션 실행
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
