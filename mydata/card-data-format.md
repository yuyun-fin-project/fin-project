# 커스텀 마이데이터 API 더미데이터 구조 (표 형식)

## 1. API 목록 개요

| 구분 | API ID | API 명 | 용도 | HTTP Method | URI |
|------|--------|--------|------|-------------|-----|
| 소비 | 카드-001 | 카드 목록 조회 | 보유 카드 목록 | GET | /v1/card/cards |
| 소비 | 카드-008 | 국내 승인내역 조회 | 카드 사용내역 | GET | /v1/card/cards/{card_id}/approval-domestic |
| 소비 | 카드-004 | 청구 기본정보 조회 | 월별 청구액 | GET | /v1/card/bills |
| 소비 | 선불-004 | 선불카드 승인내역 조회 | 선불카드 사용내역 | POST | /v1/card/prepaid/approval |
| 자산 | 카드-003 | 포인트 정보 조회 | 포인트 잔액 | GET | /v1/card/points |
| 자산 | 카드-011 | 단기대출 정보 조회 | 현금서비스 잔액 | GET | /v1/card/loans/short-term |
| 자산 | 카드-012 | 장기대출 정보 조회 | 카드론 잔액 | GET | /v1/card/loans/long-term |
| 자산 | 선불-002 | 선불카드 잔액정보 조회 | 선불카드 잔액 | POST | /v1/card/prepaid/balance |

## 2. 카드-001: 카드 목록 조회

### Request Parameters
| 파라미터명 | 필수여부 | 타입 | 설명 |
|-----------|----------|------|------|
| org_code | Y | string | 기관코드 |
| search_timestamp | N | number | 조회 타임스탬프 |
| next_page | N | string | 다음 페이지 기준개체 |
| limit | Y | number | 최대조회갯수 |

### Response Fields
| 필드명 | 필수여부 | 타입 | 설명 | 예시값 |
|--------|----------|------|------|--------|
| rsp_code | Y | string | 응답코드 | "00000" |
| rsp_msg | Y | string | 응답메시지 | "정상처리" |
| search_timestamp | Y | string | 조회 타임스탬프 | "20240301120000" |
| card_cnt | Y | number | 보유카드수 | 2 |
| card_list | Y | array | 보유카드목록 | - |
| └ card_id | Y | string | 카드 식별자 | "CARD_001" |
| └ card_num | Y | string | 카드번호(마스킹) | "1234********5678" |
| └ is_consent | Y | boolean | 전송요구 여부 | true |
| └ card_name | Y | string | 카드상품명 | "삼성카드 taptap O" |
| └ card_member | Y | string | 본인/가족 구분 | "1" |
| └ card_type | Y | string | 카드 구분 | "01" |

## 3. 카드-008: 국내 승인내역 조회

### Request Parameters
| 파라미터명 | 필수여부 | 타입 | 설명 |
|-----------|----------|------|------|
| org_code | Y | string | 기관코드 |
| from_date | Y | string | 조회 시작일자 |
| to_date | Y | string | 조회 종료일자 |
| next_page | N | string | 다음 페이지 기준개체 |
| limit | Y | number | 최대조회갯수 |

### Response Fields
| 필드명 | 필수여부 | 타입 | 설명 | 예시값 |
|--------|----------|------|------|--------|
| rsp_code | Y | string | 응답코드 | "00000" |
| rsp_msg | Y | string | 응답메시지 | "정상처리" |
| approved_cnt | Y | number | 국내승인목록수 | 3 |
| approved_list | Y | array | 국내승인목록 | - |
| └ approved_num | Y | string | 승인번호 | "12345678" |`
| └ approved_dtime | Y | string | 승인일시 | "202402151030" |
| └ status | Y | string | 결제상태 | "01" (승인) |
| └ pay_type | Y | string | 사용구분 | "01" (신용) |
| └ merchant_name | N | string | 가맹점명 | "스타벅스 강남역점" |
| └ merchant_regno | N | string | 사업자등록번호 | "123-45-67890" |
| └ approved_amt | Y | number | 이용금액 | 5500 |
| └ total_install_cnt | N | number | 전체 할부회차 | null |

## 4. 카드-004: 청구 기본정보 조회

### Request Parameters
| 파라미터명 | 필수여부 | 타입 | 설명 |
|-----------|----------|------|------|
| org_code | Y | string | 기관코드 |
| from_month | Y | string | 시작년월 |
| to_month | Y | string | 종료년월 |
| next_page | N | string | 다음 페이지 기준개체 |
| limit | Y | number | 최대조회갯수 |

### Response Fields
| 필드명 | 필수여부 | 타입 | 설명 | 예시값 |
|--------|----------|------|------|--------|
| rsp_code | Y | string | 응답코드 | "00000" |
| rsp_msg | Y | string | 응답메시지 | "정상처리" |
| bill_cnt | Y | number | 청구목록수 | 2 |
| bill_list | Y | array | 청구목록 | - |
| └ seqno | N | string | 결제순번 | null |
| └ charge_amt | Y | number | 월별 청구금액 | 450000 |
| └ charge_day | Y | string | 결제일 | "15" |
| └ charge_month | Y | string | 청구년월 | "202402" |
| └ paid_out_date | Y | string | 결제년월일 | "20240315" |

## 5. 카드-003: 포인트 정보 조회

### Request Parameters
| 파라미터명 | 필수여부 | 타입 | 설명 |
|-----------|----------|------|------|
| org_code | Y | string | 기관코드 |
| search_timestamp | Y | number | 조회 타임스탬프 |

### Response Fields
| 필드명 | 필수여부 | 타입 | 설명 | 예시값 |
|--------|----------|------|------|--------|
| rsp_code | Y | string | 응답코드 | "00000" |
| rsp_msg | Y | string | 응답메시지 | "정상처리" |
| search_timestamp | Y | string | 조회 타임스탬프 | "20240301120000" |
| point_cnt | Y | number | 포인트수 | 1 |
| point_list | Y | array | 포인트목록 | - |
| └ point_name | Y | string | 포인트명 | "삼성카드 포인트" |
| └ remain_point_amt | Y | number | 잔여포인트 | 15230 |
| └ expiring_point_amt | Y | number | 소멸예정 포인트 | 1200 |

## 6. 선불-002: 선불카드 잔액정보 조회

### Request Body
| 파라미터명 | 필수여부 | 타입 | 설명 |
|-----------|----------|------|------|
| org_code | Y | string | 기관코드 |
| pp_id | Y | string | 선불카드식별자 |
| search_timestamp | Y | string | 조회 타임스탬프 |

### Response Fields
| 필드명 | 필수여부 | 타입 | 설명 | 예시값 |
|--------|----------|------|------|--------|
| rsp_code | Y | string | 응답코드 | "00000" |
| rsp_msg | Y | string | 응답메시지 | "정상처리" |
| search_timestamp | N | string | 조회 타임스탬프 | "20240301120000" |
| total_balance_amt | Y | number | 총잔액 | 35600 |
| charge_balance_amt | N | number | 충전포인트 잔액 | 30000 |
| reserve_balance_amt | N | number | 적립포인트 잔액 | 5600 |
| reserve_due_amt | N | number | 적립예정 | 1000 |
| exp_due_amt | Y | number | 소멸예정 | 500 |

## 7. 카드-011: 단기대출 정보 조회

### Request Parameters
| 파라미터명 | 필수여부 | 타입 | 설명 |
|-----------|----------|------|------|
| org_code | Y | string | 기관코드 |
| search_timestamp | Y | number | 조회 타임스탬프 |

### Response Fields
| 필드명 | 필수여부 | 타입 | 설명 | 예시값 |
|--------|----------|------|------|--------|
| rsp_code | Y | string | 응답코드 | "00000" |
| rsp_msg | Y | string | 응답메시지 | "정상처리" |
| search_timestamp | N | string | 조회 타임스탬프 | "20240301120000" |
| short_term_cnt | Y | number | 단기대출 목록수 | 1 |
| short_term_list | Y | array | 단기대출목록 | - |
| └ loan_dtime | Y | string | 이용일시 | "20240220150000" |
| └ loan_amt | Y | number | 이용금액 | 300000 |
| └ balance_amt | Y | number | 단기대출잔액 | 280000 |
| └ pay_due_date | Y | string | 결제예정일 | "20240315" |
| └ int_rate | Y | number | 이자율 | 15.9 |

## 8. 카드-012: 장기대출 정보 조회

### Request Parameters
| 파라미터명 | 필수여부 | 타입 | 설명 |
|-----------|----------|------|------|
| org_code | Y | string | 기관코드 |
| search_timestamp | Y | number | 조회 타임스탬프 |

### Response Fields
| 필드명 | 필수여부 | 타입 | 설명 | 예시값 |
|--------|----------|------|------|--------|
| rsp_code | Y | string | 응답코드 | "00000" |
| rsp_msg | Y | string | 응답메시지 | "정상처리" |
| search_timestamp | N | string | 조회 타임스탬프 | "20240301120000" |
| long_term_cnt | Y | number | 장기대출 목록수 | 1 |
| long_term_list | Y | array | 장기대출목록 | - |
| └ loan_num | Y | string | 대출번호 | "LN2024001" |
| └ loan_dtime | Y | string | 대출일시 | "20230515" |
| └ loan_type | N | string | 대출종류 | "신용대출" |
| └ loan_name | Y | string | 상품명 | "KB국민 마이핏 대출" |
| └ loan_amt | Y | number | 이용금액 | 10000000 |
| └ int_rate | Y | number | 이자율 | 12.5 |
| └ exp_date | Y | string | 만기일 | "20260515" |
| └ balance_amt | Y | number | 장기대출 잔액 | 8500000 |
| └ repay_method | Y | string | 상환방법 | "01" |
| └ int_amt | Y | number | 상환액 중 이자 | 104166 |