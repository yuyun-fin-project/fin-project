# (1) 베이스 이미지
FROM python:3.11

# (2) 작업 디렉토리 설정
WORKDIR /app

# (3) 프로젝트 파일 복사
COPY . /app

# (4) 필요한 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt\
 && pip install uvicorn 

# (5) Django static 파일 수집 (운영환경에서 필요)
RUN python manage.py collectstatic --noinput

# (6) Uvicorn으로 실행
CMD ["uvicorn", "fin_project.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
