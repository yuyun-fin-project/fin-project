<template>
  <div class="p-6 rounded-2xl shadow-lg bg-white dark:bg-zinc-900">
    <h2 class="text-2xl font-bold mb-4">월별 지출 내역</h2>
    
    <table class="w-full table-auto border-collapse text-sm text-left">
      <thead>
        <tr class="bg-gray-100 dark:bg-zinc-800">
          <th class="p-2">월</th>
          <th v-for="merchant in merchants" :key="merchant" class="p-2">{{ merchant }}</th>
        </tr>
      </thead>

    </table>
  </div>
</template>

<script setup lang="ts">



// 여기에 실제 백엔드 데이터 연동 또는 props로 교체 가능
const spendingData = {
  "2025-01": { "11번가": 101728, "현대오일뱅크": 20477, "S-OIL": 2065 },
  "2025-04": {
    "LG유플러스": 120656, "G마켓": 181749, "옥션": 197033, "버스": 20163, "내과": 85211,
    "김밥천국": 37783, "메가박스": 22960, "요기요": 33214, "호텔": 23531, "맥도날드": 17190,
    "올리브영": 403000, "반디앤루니스": 171726, "GS칼텍스": 15096, "네이버쇼핑": 25803
  },
  "2025-05": {
    "필라테스": 51441, "그린카": 23851, "안과": 99344
  }
}

const merchants = Array.from(
  new Set(Object.values(spendingData).flatMap(row => Object.keys(row)))
)




const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top' as const
    },
    title: {
      display: true,
      text: '월별 지출 분석 (상호별)'
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        callback: (value: number) => value.toLocaleString() + '원'
      }
    }
  }
}
</script>

<style scoped>
table {
  border-spacing: 0;
}
th, td {
  white-space: nowrap;
}
</style>
