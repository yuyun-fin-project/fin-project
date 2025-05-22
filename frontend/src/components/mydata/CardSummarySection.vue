<template>
  <section class="kpi-section">
    <div class="kpi-card full-width">
      <h3>카드사별 총 사용 금액</h3>
      <ul class="summary-list">
        <li v-for="summary in summaries" :key="summary.org_code">
          <span class="label">{{ summary.org_name }}</span>
          <span class="amount">{{ formatAmount(summary.total) }}원</span>
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import bills from '@/data/bills.json'

const currentUserId = '8e482e4e-85ed-4708-8f85-2183f6d9dc03'

const orgNameMap: Record<string, string> = {
  SHINHAN_CARD: '신한카드',
  KAKAO: '카카오카드',
  HYUNDAI: '현대카드',
  HANA_CARD: '하나카드',
  IBK: 'IBK카드',
  LOTTE: '롯데카드',
  SAMSUNG: '삼성카드',
  WOORI_CARD: '우리카드',
  KB_CARD: '국민카드',
  BC: 'BC카드',
  SC: 'SC제일은행',
  NONGHYUP: '농협카드'
}

const grouped = bills
  .filter(bill => bill.user_id === currentUserId)
  .reduce((acc: Record<string, number>, cur) => {
    if (!acc[cur.org_code]) acc[cur.org_code] = 0
    acc[cur.org_code] += cur.charge_amt
    return acc
  }, {})

const summaries = computed(() => {
  return Object.entries(grouped).map(([org_code, total]) => ({
    org_code,
    org_name: orgNameMap[org_code] || org_code,
    total
  }))
})

const formatAmount = (amount: number) =>
  amount.toLocaleString('ko-KR')
</script>

<style scoped>
.kpi-section {
  margin-bottom: 2rem;
}

.kpi-card.full-width {
  /* width: 100%; */
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.summary-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  margin-top: 1rem;
}

.summary-list li {
  display: flex;
  flex-direction: column;
  min-width: 180px;
}

.label {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
}

.amount {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111;
}
</style>