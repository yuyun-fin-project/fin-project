# 📊 커스텀 마이데이터 API 서버 (FastAPI + PostgreSQL)

## 🔍 프로젝트 개요

본 프로젝트는 **FastAPI + PostgreSQL + SQLAlchemy** 기반의 **마이데이터 API 서버**입니다.  
공식 마이데이터 구조를 참고하여, 사용자 및 카드/청구/승인/포인트/선불/대출 데이터를 자동 생성하는 **더미 데이터 스크립트**를 제공합니다.

## 🚀 주요 기능

- 사용자(user) 및 다양한 금융 데이터 자동 생성
- Faker 기반 더미 데이터 자동 생성기 구현
- 실제 마이데이터 API 테스트 및 연동 시뮬레이션 가능
- FastAPI 기반 API 서버와 연동 테스트 가능
- pagination, 필터링, 응답 포맷 구조화 지원 예정

---

## 🧱 데이터 모델 및 생성 조건

| 데이터 종류                  | 생성 조건                           |
|---------------------------|------------------------------------|
| `users`                  | 총 100명                             |
| `cards`                  | 사용자당 1~7개 카드                   |
| `card_bills`             | 카드당 3~6개월 청구 데이터             |
| `card_approvals_domestic`| 카드당 5~50건 승인 내역               |
| `points`                 | 사용자당 1~4개 기관 포인트             |
| `prepaid_balances`       | 사용자당 0~4개 선불카드 잔액            |
| `prepaid_approvals`      | 잔액당 10~15건 승인 내역               |
| `loans_short_term`       | 사용자당 0~1건 단기대출                |
| `loans_long_term`        | 사용자당 0~1건 장기대출                |
| `org_codes`              | 18개 기관명 중 무작위 선택             |


---
### Maintainer
- Name : Edward Lee
