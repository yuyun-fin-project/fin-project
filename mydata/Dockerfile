# 1️⃣ 베이스 이미지
FROM python:3.10-slim

# 2️⃣ 작업 디렉토리
WORKDIR /app

# 3️⃣ 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ 코드 복사
COPY . .

# 5️⃣ 컨테이너 시작할 때 실행할 명령어
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]