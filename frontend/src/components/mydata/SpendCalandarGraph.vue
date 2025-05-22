<template>
  <section class="graph-section">
    <h3 class="graph-title">월별 지출 추이</h3>
    <Bar
      v-if="data?.labels?.length"
      :data="data"
      :options="chartOptions"
    />
    <p v-else class="loading-msg">데이터 로딩 중...</p>
  </section>
</template>

<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from 'chart.js'
import { defineProps } from 'vue'

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend)

defineProps<{ data?: { labels: string[]; datasets: any[] } }>()

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        callback: (value: any) => `${value.toLocaleString()}원`
      }
    }
  },
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: (context: any) => `지출: ${context.parsed.y.toLocaleString()}원`
      }
    }
  }
}


</script>

<style scoped>
.graph-section {
  width: 320px;
  aspect-ratio: 1 / 1;
  background: #fff;
  border-radius: 12px;
  padding: 0.75rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}

.graph-title {
  font-size: 0.95rem;
  text-align: center;
  margin-bottom: 0.5rem;
}

canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
