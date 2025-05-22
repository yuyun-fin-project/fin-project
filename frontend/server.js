import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import axios from 'axios';

const app = express();
app.use(cors());

// API 기본 설정
const BASE_URL = 'http://finlife.fss.or.kr/finlifeapi';
const PORT = process.env.PORT || 4000;

// API 엔드포인트 매핑
const API_ENDPOINTS = {
  deposit: '/depositProductsSearch.json',
  saving: '/savingProductsSearch.json'
};

// 테스트용 더미 데이터
const dummyData = {
  result: {
    baseList: [
      {
        fin_prdt_cd: "001",
        kor_co_nm: "우리은행",
        fin_prdt_nm: "우리 주거래 우대통장",
        intr_rate: "3.5",
        save_trm: "12",
        spcl_cnd: "1000000",
        join_way: "인터넷뱅킹",
        homp_url: "https://www.wooribank.com"
      },
      {
        fin_prdt_cd: "002",
        kor_co_nm: "신한은행",
        fin_prdt_nm: "신한 스마트 정기예금",
        intr_rate: "3.8",
        save_trm: "24",
        spcl_cnd: "500000",
        join_way: "스마트뱅킹",
        homp_url: "https://www.shinhan.com"
      },
      {
        fin_prdt_cd: "003",
        kor_co_nm: "국민은행",
        fin_prdt_nm: "KB Star 정기예금",
        intr_rate: "3.6",
        save_trm: "36",
        spcl_cnd: "1000000",
        join_way: "영업점",
        homp_url: "https://www.kbstar.com"
      }
    ],
    optionList: [
      {
        fin_prdt_cd: "001",
        intr_rate: "3.8",
        intr_rate2: "4.0",
        save_trm: "12"
      },
      {
        fin_prdt_cd: "002",
        intr_rate: "4.0",
        intr_rate2: "4.2",
        save_trm: "24"
      },
      {
        fin_prdt_cd: "003",
        intr_rate: "3.9",
        intr_rate2: "4.1",
        save_trm: "36"
      }
    ]
  }
};

// 디버그 미들웨어
app.use((req, res, next) => {
  console.log('\n[요청 정보]', {
    method: req.method,
    url: req.url,
    params: req.params,
    query: req.query,
    headers: req.headers
  });
  next();
});

// 금융상품 API 프록시 엔드포인트
app.get('/api/products/:type', async (req, res) => {
  try {
    const { type } = req.params;
    const { apiKey } = req.query;

    console.log('\n[API 요청 파라미터]', {
      type,
      apiKey: apiKey ? `${apiKey.substring(0, 4)}...` : undefined
    });

    // 기본 유효성 검사
    if (!apiKey) {
      throw new Error('API 키가 필요합니다.');
    }

    if (!API_ENDPOINTS[type]) {
      throw new Error('지원하지 않는 상품 유형입니다.');
    }

    // API 요청 URL 및 파라미터 구성
    const url = `${BASE_URL}${API_ENDPOINTS[type]}`;
    const params = {
      auth: apiKey,
      topFinGrpNo: '020000',  // 은행권
      pageNo: '1'             // 첫 페이지
    };

    console.log('\n[금감원 API 요청]', {
      url,
      params: { ...params, auth: `${params.auth.substring(0, 4)}...` }
    });

    // API 호출
    const response = await axios({
      method: 'GET',
      url,
      params,
      timeout: 30000,
      headers: {
        'Accept': 'application/json'
      }
    });

    console.log('\n[금감원 API 응답]', {
      status: response.status,
      statusText: response.statusText,
      headers: response.headers,
      data: response.data
    });

    // 응답 데이터 검증
    if (!response.data || !response.data.result) {
      throw new Error('유효하지 않은 응답 데이터');
    }

    const { result } = response.data;

    // 에러 코드 확인 ('000'은 정상 응답)
    if (result.err_cd === '000') {
      // 성공 응답
      return res.json({
        status: 'success',
        data: {
          baseList: result.baseList || [],
          optionList: result.optionList || []
        }
      });
    }

    // API 에러 응답
    throw new Error(`금감원 API 오류: ${result.err_msg} (${result.err_cd})`);

  } catch (error) {
    console.error('\n[에러 발생]', {
      name: error.name,
      message: error.message,
      stack: error.stack,
      response: error.response?.data,
      config: error.config
    });

    // 에러 응답
    const statusCode = error.response?.status || 500;
    const errorResponse = {
      status: 'error',
      message: error.message,
      code: error.response?.status,
      details: error.response?.data
    };

    res.status(statusCode).json(errorResponse);
  }
});

// 서버 상태 확인 엔드포인트
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// 서버 시작
app.listen(PORT, () => {
  console.log(`
[서버 시작]
- 포트: ${PORT}
- 상태 확인: http://localhost:${PORT}/health
- API 엔드포인트: http://localhost:${PORT}/api/products/{type}?apiKey={your-api-key}
  `);
}); 
