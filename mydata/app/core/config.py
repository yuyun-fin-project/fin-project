# core/config.py

import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings

# .env 파일에서 환경 변수 로드
# 프로젝트 루트 디렉토리에 있는 .env 파일을 찾아 환경 변수로 로드합니다.
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    """
    애플리케이션 설정을 관리하는 클래스입니다.
    환경 변수에서 값을 로드하며, 기본값을 제공합니다.
    """
    # 프로젝트 기본 정보
    PROJECT_NAME: str = "Custom MyData API"  # 프로젝트 이름
    PROJECT_VERSION: str = "1.0.0"  # 프로젝트 버전

    # 데이터베이스 연결 설정
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")  # PostgreSQL 사용자 이름
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")  # PostgreSQL 비밀번호
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")  # PostgreSQL 서버 주소 (기본값: localhost)
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")  # PostgreSQL 포트 (기본값: 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "mydata_db")  # 데이터베이스 이름 (기본값: mydata_db)

    # JWT 인증 설정
    SECRET_KEY: str = os.getenv("SECRET_KEY")  # JWT 서명을 위한 시크릿 키
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")  # JWT 암호화 알고리즘 (기본값: HS256)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))  # 액세스 토큰 만료 시간(분) (기본값: 60분)

    # 데이터베이스 URL 생성
    # PostgreSQL 연결을 위한 URL 포맷: postgresql://사용자이름:비밀번호@서버주소:포트/데이터베이스이름
    DATABASE_URL: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

# 전역 설정 인스턴스 생성
settings = Settings()