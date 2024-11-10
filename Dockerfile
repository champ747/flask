# Python 이미지 선택
FROM python:3.9

# Java 설치
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean;

# JAVA_HOME 환경 변수 설정
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV PATH $JAVA_HOME/bin:$PATH

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY . /app

# 필요한 Python 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
