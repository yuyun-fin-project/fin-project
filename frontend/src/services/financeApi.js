import axios from 'axios';

export const getFinanceProducts = async (type) => {
  try {
    const response = await axios.get('/finrecom/');

    if (!response.data || !response.data.results) {
      throw new Error('유효하지 않은 응답 데이터');
    }

    const { prd: baseList = [], opt: optionList = [] } = response.data.results;

    // 상품 유형에 따라 필터링
    const filteredBaseList = baseList.filter(item => {
      if (type === 'deposit') return item.prd_type === 'D';
      if (type === 'saving') return item.prd_type === 'S';
      return true;
    });

    // 응답 데이터 가공
    const processedBaseList = filteredBaseList.map(item => {
      // 해당 상품의 옵션들 찾기
      const productOptions = optionList.filter(opt => opt.prd === item.id);

      // 최고 금리 계산
      const maxRate = productOptions.length > 0
        ? Math.max(...productOptions.map(opt => {
            const baseRate = parseFloat(opt.intr_rate) || 0;
            const specialRate = parseFloat(opt.intr_rate2) || 0;
            return Math.max(baseRate, specialRate);
          }))
        : 0;

      // 가입기간 추출
      let period = null;
      if (productOptions.length > 0) {
        // 옵션에서 가입기간이 있는 경우
        const uniquePeriods = [...new Set(productOptions.map(opt => parseInt(opt.save_trm) || 12))];
        if (uniquePeriods.length === 1) {
          // 모든 옵션의 가입기간이 동일한 경우
          period = uniquePeriods[0];
        } else {
          // 여러 가입기간이 있는 경우 가장 짧은 기간 선택
          period = Math.min(...uniquePeriods);
        }
      }

      // 옵션에서 가입기간을 찾지 못한 경우 상품 정보에서 추출 시도
      if (!period && item.etc_note) {
        const periodMatches = [
          // "6개월" 형식
          item.etc_note.match(/가입기간\s*:\s*(\d+)개월/i),
          // "6~12개월" 형식
          item.etc_note.match(/가입기간\s*:\s*(\d+)\s*~\s*\d+개월/i),
          // "개월" 이 포함된 첫 번째 숫자
          item.etc_note.match(/(\d+)\s*개월/i)
        ].find(match => match !== null);

        if (periodMatches) {
          period = parseInt(periodMatches[1]);
        }
      }

      // 기본값 설정
      if (!period) {
        period = 12;
      }

      // 최소 가입금액 추출
      let minAmount = 0;
      if (item.etc_note) {
        const matches = item.etc_note.match(/최소[가입금액|예치금액]?\s*:\s*(\d+)[만]?원/i);
        if (matches) {
          minAmount = parseInt(matches[1]) * (matches[0].includes('만원') ? 10000 : 1);
        } else {
          // 다른 형식의 금액 표기 찾기
          const amountMatches = item.etc_note.match(/(\d+)[만]?원/);
          if (amountMatches) {
            minAmount = parseInt(amountMatches[1]) * (amountMatches[0].includes('만원') ? 10000 : 1);
          }
        }
      }

      return {
        id: item.id,
        name: item.fin_prdt_nm,
        bank_name: item.kor_co_nm,
        bank_code: item.fin_co_no,
        type: item.prd_type,
        interest_rate: maxRate,
        period: period,
        min_amount: minAmount,
        join_way: item.join_way,
        etc_note: item.etc_note,
        join_member: item.join_member,
        options: productOptions.map(opt => ({
          id: opt.id,
          save_trm: parseInt(opt.save_trm) || 12,
          intr_rate: parseFloat(opt.intr_rate) || 0,
          intr_rate2: parseFloat(opt.intr_rate2) || 0,
          intr_rate_type: opt.intr_rate_type,
          intr_rate_type_nm: opt.intr_rate_type_nm
        }))
      };
    });

    return {
      baseList: processedBaseList,
      optionList: optionList
        .filter(opt => filteredBaseList.some(prd => prd.id === opt.prd))
        .map(item => ({
          id: item.id,
          prd: item.prd,
          save_trm: parseInt(item.save_trm) || 12,
          intr_rate: parseFloat(item.intr_rate) || 0,
          intr_rate2: parseFloat(item.intr_rate2) || 0,
          intr_rate_type: item.intr_rate_type,
          intr_rate_type_nm: item.intr_rate_type_nm
        }))
    };

  } catch (error) {
    console.error('금융상품 조회 오류:', error);
    // 에러 발생 시 더미 데이터 반환
    if (process.env.NODE_ENV === 'development') {
      console.log('개발 환경에서 더미 데이터 사용');
      return getDummyData();
    }
    throw error;
  }
};

// 테스트용 더미 데이터
export const getDummyData = () => ({
  baseList: [
    {
      id: "001",
      name: "우리 주거래 우대통장",
      bank_name: "우리은행",
      bank_code: "001",
      type: "D",
      interest_rate: 4.0,
      period: 12,
      min_amount: 1000000,
      join_way: "인터넷뱅킹",
      etc_note: "최소가입금액: 100만원\n가입기간: 12개월",
      join_member: "제한없음",
      options: [
        {
          id: 1,
          save_trm: 12,
          intr_rate: 3.8,
          intr_rate2: 4.0,
          intr_rate_type: "S",
          intr_rate_type_nm: "단리"
        }
      ]
    },
    {
      id: "002",
      name: "신한 스마트 정기예금",
      bank_name: "신한은행",
      bank_code: "002",
      type: "D",
      interest_rate: 4.2,
      period: 24,
      min_amount: 500000,
      join_way: "스마트뱅킹",
      etc_note: "최소가입금액: 50만원\n가입기간: 24개월",
      join_member: "제한없음",
      options: [
        {
          id: 2,
          save_trm: 24,
          intr_rate: 4.0,
          intr_rate2: 4.2,
          intr_rate_type: "S",
          intr_rate_type_nm: "단리"
        }
      ]
    }
  ],
  optionList: [
    {
      id: 1,
      prd: "001",
      save_trm: 12,
      intr_rate: 3.8,
      intr_rate2: 4.0,
      intr_rate_type: "S",
      intr_rate_type_nm: "단리"
    },
    {
      id: 2,
      prd: "002",
      save_trm: 24,
      intr_rate: 4.0,
      intr_rate2: 4.2,
      intr_rate_type: "S",
      intr_rate_type_nm: "단리"
    }
  ]
}); 