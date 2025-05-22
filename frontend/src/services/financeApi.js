import axios from 'axios';

const BASE_URL = '/api/finlifeapi';  // Vite 프록시 경로로 수정
const API_KEY = import.meta.env.VITE_FSS_API_KEY;

const API_ENDPOINTS = {
  deposit: '/depositProductsSearch.json',
  saving: '/savingProductsSearch.json'
};

export const getFinanceProducts = async (type) => {
  try {
    if (!API_ENDPOINTS[type]) {
      throw new Error('지원하지 않는 상품 유형입니다.');
    }

    const url = `${BASE_URL}${API_ENDPOINTS[type]}`;
    const params = {
      auth: API_KEY,
      topFinGrpNo: '020000',  // 은행권
      pageNo: '1'             // 첫 페이지
    };

    console.log('API 요청 URL:', url);
    console.log('API 파라미터:', params);

    const response = await axios({
      method: 'GET',
      url,
      params,
      timeout: 30000,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });

    if (!response.data || !response.data.result) {
      throw new Error('유효하지 않은 응답 데이터');
    }

    const { result } = response.data;

    if (result.err_cd !== '000') {
      throw new Error(`금감원 API 오류: ${result.err_msg} (${result.err_cd})`);
    }

    return {
      baseList: result.baseList || [],
      optionList: result.optionList || []
    };

  } catch (error) {
    console.error('금융상품 조회 오류:', error);
    throw error;
  }
};

// 테스트용 더미 데이터
export const getDummyData = () => ({
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
    }
  ]
}); 