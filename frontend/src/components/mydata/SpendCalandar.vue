<template>
  <section class="calendar-section" ref="dropdownContainer">
    <h3 class="calendar-title">소비 캘린더</h3>

    <div class="month-navigation">
      <button @click="goToPrevMonth" class="arrow-btn" :disabled="!canGoPrev">
        ‹
      </button>
      <div class="month-label" @click="toggleMonthDropdown">
        {{ selectedMonthLabel }}
        <div v-if="showDropdown" class="month-dropdown">
          <div
            v-for="option in monthOptions"
            :key="option.value"
            @click="
              () => {
                selectMonth(option.value);
                showDropdown = false;
              }
            "
            class="dropdown-option"
          >
            {{ option.label }}
          </div>
        </div>
      </div>
      <button @click="goToNextMonth" class="arrow-btn" :disabled="!canGoNext">
        ›
      </button>
    </div>
    <p class="summary">
      <strong>{{ formatAmount(totalExpense) }}원</strong>
      <br />
      <span :class="{ increase: diff > 0, decrease: diff < 0 }">
        {{ diffText }}
      </span>
    </p>

    <div class="calendar-grid">
      <div
        v-for="n in firstDayOffset"
        :key="'empty-' + n"
        class="calendar-day empty"
      ></div>
      <div v-for="day in monthDays" :key="day.date" class="calendar-day">
        <span class="date">{{ Number(day.day) }}</span>
        <span class="income" v-if="day.income"
          >+{{ formatAmount(day.income) }}</span
        >
        <span class="expense" v-if="day.expense"
          >-{{ formatAmount(day.expense) }}</span
        >
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import approvals from "../../data/approvals.json";

const currentUserId = "8e482e4e-85ed-4708-8f85-2183f6d9dc03";
const now = new Date();
const currentMonth = `${now.getFullYear()}${String(now.getMonth() + 1).padStart(
  2,
  "0"
)}`;

const selectedMonth = ref(currentMonth);
const showDropdown = ref(false);
const dropdownContainer = ref<HTMLElement | null>(null);

const handleClickOutside = (event: MouseEvent) => {
  if (
    dropdownContainer.value &&
    !dropdownContainer.value.contains(event.target as Node)
  ) {
    showDropdown.value = false;
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside);
});

const monthOptions = Array.from({ length: 6 }, (_, i) => {
  const date = new Date(now.getFullYear(), now.getMonth() - i, 1);
  const value = `${date.getFullYear()}${String(date.getMonth() + 1).padStart(
    2,
    "0"
  )}`;
  const label = `${date.getFullYear()}년 ${date.getMonth() + 1}월`;
  return { value, label };
});

const selectedMonthLabel = computed(() => {
  const option = monthOptions.find((o) => o.value === selectedMonth.value);
  return option?.label ?? "";
});

const toggleMonthDropdown = () => (showDropdown.value = !showDropdown.value);
const selectMonth = (month: string) => {
  selectedMonth.value = month;
};

const canGoPrev = computed(() =>
  monthOptions.some((m) => m.value < selectedMonth.value)
);
const canGoNext = computed(() => selectedMonth.value < currentMonth);

const goToPrevMonth = () => {
  const currentIdx = monthOptions.findIndex(
    (m) => m.value === selectedMonth.value
  );
  if (currentIdx < monthOptions.length - 1) {
    selectedMonth.value = monthOptions[currentIdx + 1].value;
  }
};

const goToNextMonth = () => {
  const currentIdx = monthOptions.findIndex(
    (m) => m.value === selectedMonth.value
  );
  if (currentIdx > 0) {
    selectedMonth.value = monthOptions[currentIdx - 1].value;
  }
};

const daysInMonth = computed(() => {
  const year = Number(selectedMonth.value.slice(0, 4));
  const month = Number(selectedMonth.value.slice(4));
  return new Date(year, month, 0).getDate();
});

const firstDayOffset = computed(() => {
  const year = Number(selectedMonth.value.slice(0, 4));
  const month = Number(selectedMonth.value.slice(4)) - 1;
  return new Date(year, month, 1).getDay();
});

const monthData = computed(() => {
  const map: Record<string, { income: number; expense: number }> = {};
  approvals.forEach((item) => {
    if (item.user_id === currentUserId) {
      const month = item.approved_dtime.slice(0, 6);
      const day = item.approved_dtime.slice(6, 8);
      if (month === selectedMonth.value) {
        if (!map[day]) map[day] = { income: 0, expense: 0 };
        if (item.pay_type === "00") {
          map[day].income += item.approved_amt;
        } else {
          map[day].expense += item.approved_amt;
        }
      }
    }
  });
  return map;
});

const monthDays = computed(() => {
  return Array.from({ length: daysInMonth.value }, (_, i) => {
    const day = String(i + 1).padStart(2, "0");
    const data = monthData.value[day] || { income: 0, expense: 0 };
    return {
      day,
      date: `${selectedMonth.value}-${day}`,
      ...data,
    };
  });
});

const formatAmount = (amount: number) => amount.toLocaleString("ko-KR");

const totalExpense = computed(() =>
  Object.values(monthData.value).reduce((sum, day) => sum + day.expense, 0)
);

const prevMonth = computed(() => {
  const year = Number(selectedMonth.value.slice(0, 4));
  const month = Number(selectedMonth.value.slice(4, 6));
  const prev = new Date(year, month - 2);
  return `${prev.getFullYear()}${String(prev.getMonth() + 1).padStart(2, "0")}`;
});

const prevMonthExpense = computed(() => {
  let total = 0;
  approvals.forEach((item) => {
    if (
      item.user_id === currentUserId &&
      item.pay_type !== "00" &&
      item.approved_dtime.startsWith(prevMonth.value)
    ) {
      total += item.approved_amt;
    }
  });
  return total;
});

const diff = computed(() => totalExpense.value - prevMonthExpense.value);
const diffText = computed(() => {
  const abs = Math.abs(diff.value);
  const text = formatAmount(abs) + "원";
  return `전월대비 ${text} ${diff.value > 0 ? "더 썼어요" : "덜 썼어요"}`;
});
</script>

<style scoped>
.calendar-section {
  width: 320px;
  aspect-ratio: 1 / 1;
  margin: 0 auto;
  background: #fff;
  padding: 0.75rem;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
}

.calendar-title {
  font-size: 1rem;
  margin-bottom: 0.25rem;
  text-align: center;
}

.summary {
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
  text-align: center;
}

.summary .increase {
  color: red;
  font-weight: bold;
}
.summary .decrease {
  color: blue;
  font-weight: bold;
}

.month-navigation {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
  gap: 0.5rem;
  position: relative;
}

.arrow-btn {
  background: none;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  color: #333;
  padding: 0.2rem;
}

.month-label {
  cursor: pointer;
  font-weight: bold;
  font-size: 0.85rem;
  position: relative;
  user-select: none;
}

.month-dropdown {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  background-color: #fff;
  border: 1px solid #ccc;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 10;
  border-radius: 6px;
  overflow: hidden;
  width: max-content;
  min-width: 100px;
  text-align: center;
}

.dropdown-option {
  padding: 0.4rem 0.75rem;
  font-size: 0.8rem;
  cursor: pointer;
  white-space: nowrap;
}
.dropdown-option:hover {
  background-color: #f0f0f0;
}

.calendar-grid {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.3rem;
}

.calendar-day {
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 0.25rem 0.15rem;
  text-align: center;
  font-size: 0.6rem;
  color: #444;
  min-height: 38px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
}

.calendar-day.empty {
  background: transparent;
  border: none;
}

.date {
  font-weight: bold;
  font-size: 0.65rem;
}

.income {
  margin-top: 0.1rem;
  color: #1e88e5;
  font-weight: 600;
  font-size: 0.6rem;
}
.expense {
  color: #d32f2f;
  font-weight: 600;
  font-size: 0.6rem;
  margin-top: 0.1rem;
}
</style>
