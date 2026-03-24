<template>
  <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 shadow-sm dark:shadow-none border border-slate-200 dark:border-slate-800 transition-colors w-full max-w-sm mx-auto">

    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h3 class="text-xs font-bold uppercase tracking-wide text-slate-500 dark:text-slate-400">
        Attendance Overview
      </h3>
      <span class="bg-green-100 dark:bg-green-900/20 text-green-600 dark:text-green-400 text-xs font-black px-3 py-1 rounded-full">#1</span>
    </div>

    <!-- CIRCULAR PROGRESS -->
    <div class="flex justify-center py-2">
      <div class="relative w-36 h-36">
        <svg class="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
          <!-- Background Circle -->
          <circle
            class="text-slate-200 dark:text-slate-800 transition-colors"
            cx="18"
            cy="18"
            r="16"
            stroke-width="4"
            fill="none"
          />
          <!-- Progress Circle -->
          <circle
            cx="18"
            cy="18"
            r="16"
            stroke-width="4"
            fill="none"
            stroke-dasharray="100"
            :stroke-dashoffset="dashOffset"
            class="transition-all duration-700 ease-out" />
        </svg>

        <!-- Center -->
        <div class="absolute inset-0 flex flex-col items-center justify-center">
          <span class="text-2xl font-bold text-slate-800 dark:text-white">{{ percentage }}%</span>
          <span class="text-xs text-slate-400 dark:text-slate-500">Attendance</span>
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-3 gap-4 text-center text-sm font-medium text-slate-700 dark:text-slate-300">
      <div>
        <p class="text-slate-400 dark:text-slate-500">Present</p>
        <p class="text-lg font-bold text-green-500 dark:text-green-400">{{ presentDays }}</p>
      </div>
      <div>
        <p class="text-slate-400 dark:text-slate-500">Absent</p>
        <p class="text-lg font-bold text-red-500 dark:text-red-400">{{ absentDays }}</p>
      </div>
      <div>
        <p class="text-slate-400 dark:text-slate-500">Leave</p>
        <p class="text-lg font-bold text-yellow-500 dark:text-yellow-400">{{ leaveDays }}</p>
      </div>

    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'

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
const absentDays  = computed(() => props.attendance.absent_days  || 0)
const leaveDays   = computed(() => props.attendance.leave_days   || 0)
const totalDays   = computed(() => props.attendance.total_days   || 0)

const percentage = computed(() => {
  if (!totalDays.value) return 0
  return Math.round((presentDays.value / totalDays.value) * 100)
})

const circumference = computed(() => 2 * Math.PI * 16)

const dashOffset = computed(() => {
  return circumference.value * (1 - percentage.value / 100)
})
</script>