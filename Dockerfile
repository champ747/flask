# 베이스 이미지로 Python 3.9 사용
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

# Python 패키지 설치
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY . /app

# Gunicorn으로 애플리케이션 실행
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
