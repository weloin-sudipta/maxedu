<template>
  <div class="bg-white rounded-3xl p-6 shadow-lg border border-slate-200 w-full max-w-sm mx-auto">

    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h3 class="text-xs font-bold uppercase tracking-wide text-slate-500">
        Attendance Overview
      </h3>
      <span class="bg-green-100 text-green-600 text-xs font-black px-3 py-1 rounded-full">#1</span>
    </div>

    <!-- Circular Percentage -->
    <div class="flex justify-center mb-6">
      <div class="relative w-36 h-36">
        <svg class="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
          <!-- Background Circle -->
          <circle
            class="text-slate-200"
            cx="18"
            cy="18"
            r="16"
            stroke-width="4"
            fill="none"
          />
          <!-- Progress Circle -->
          <circle
            class="text-green-500"
            cx="18"
            cy="18"
            r="16"
            stroke-width="4"
            fill="none"
            stroke-dasharray="100"
            :stroke-dashoffset="dashOffset"
            stroke-linecap="round"
          />
        </svg>

        <!-- Center Label -->
        <div class="absolute inset-0 flex flex-col items-center justify-center">
          <span class="text-2xl font-bold text-slate-800">{{ percentage }}%</span>
          <span class="text-xs text-slate-400">Attendance</span>
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-3 gap-4 text-center text-sm font-medium text-slate-700">
      <div>
        <p class="text-slate-400">Present</p>
        <p class="text-lg font-bold text-green-500">{{ presentDays }}</p>
      </div>
      <div>
        <p class="text-slate-400">Absent</p>
        <p class="text-lg font-bold text-red-500">{{ absentDays }}</p>
      </div>
      <div>
        <p class="text-slate-400">Leave</p>
        <p class="text-lg font-bold text-yellow-500">{{ leaveDays }}</p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'

const props = defineProps({
  attendance: {
    type: Object,
    required: true,
    default: () => ({
      present_days: 0,
      absent_days: 0,
      leave_days: 0,
      total_days: 0
    })
  }
})

const presentDays = computed(() => props.attendance.present_days || 0)
const absentDays = computed(() => props.attendance.absent_days || 0)
const leaveDays = computed(() => props.attendance.leave_days || 0)
const totalDays = computed(() => props.attendance.total_days || 0)

const percentage = computed(() => {
  if (!totalDays.value) return 0
  return Math.round((presentDays.value / totalDays.value) * 100)
})

// Circular progress dash calculation
const dashOffset = computed(() => {
  const circumference = 2 * Math.PI * 16 // r=16
  return circumference * (1 - percentage.value / 100)
})
</script>

<style scoped>
circle {
  stroke: currentColor;
  transition: stroke-dashoffset 0.6s ease;
}
</style>