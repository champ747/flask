# Python 3.9 slim 버전을 기반으로 Docker 이미지를 생성
FROM python:3.9-slim

# 작업 디렉터리 설정
WORKDIR /app

# 필요한 시스템 패키지 설치
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    mecab \
    mecab-ipadic-utf8 \
    mecab-naist-jdic \
    mecab-ko \
    mecab-ko-dic-utf8 \
    libmecab-dev \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# mecab-ko-dic의 설정 파일 복사
RUN ln -s /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ko-dic /usr/local/lib/mecab/dic/mecab-ko-dic

# Python 라이브러리 설치
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . /app

# Gunicorn을 사용해 서버 실행
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
