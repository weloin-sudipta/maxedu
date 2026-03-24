<template>
  <div class="bg-white rounded-[2rem] border border-slate-100 shadow-sm p-6 flex flex-col gap-5">

    <!-- HEADER -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-gradient-to-br from-green-500 to-emerald-400 rounded-[0.85rem] flex items-center justify-center text-white text-sm shadow-lg shadow-green-200">
          <i class="fa fa-bar-chart"></i>
        </div>
        <div>
          <h6 class="text-sm font-black text-slate-800 leading-tight tracking-tight">Attendance</h6>
          <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{{ totalDays }} total days</span>
        </div>
      </div>
      <span class="text-[10px] font-black uppercase tracking-widest px-3 py-1.5 rounded-full"
        :class="percentage >= 75 ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-500'">
        {{ percentage >= 75 ? 'Good' : 'Low' }}
      </span>
    </div>

    <!-- CIRCULAR PROGRESS -->
    <div class="flex justify-center py-2">
      <div class="relative w-36 h-36">
        <svg class="w-full h-full -rotate-90" viewBox="0 0 36 36">
          <!-- Track -->
          <circle cx="18" cy="18" r="16" fill="none" stroke="#f1f5f9" stroke-width="3.5" />
          <!-- Progress -->
          <circle cx="18" cy="18" r="16" fill="none"
            :stroke="percentage >= 75 ? '#22c55e' : '#ef4444'"
            stroke-width="3.5"
            stroke-linecap="round"
            :stroke-dasharray="`${circumference}`"
            :stroke-dashoffset="dashOffset"
            class="transition-all duration-700 ease-out" />
        </svg>

        <!-- Center -->
        <div class="absolute inset-0 flex flex-col items-center justify-center">
          <span class="text-3xl font-black text-slate-800 leading-none">{{ percentage }}%</span>
          <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">Present</span>
        </div>
      </div>
    </div>

    <!-- DOT + LINE STATS -->
    <div class="flex flex-col">

      <div class="flex items-start gap-3 py-3 group">
        <div class="flex flex-col items-center flex-shrink-0 w-4 pt-1">
          <div class="relative w-3.5 h-3.5 flex-shrink-0">
            <div class="absolute inset-0 rounded-full border-2 border-slate-200"></div>
            <div class="absolute inset-[3px] rounded-full bg-green-500"></div>
          </div>
          <div class="w-px flex-1 min-h-[20px] mt-1 bg-gradient-to-b from-slate-200 to-transparent"></div>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-[13px] font-black text-slate-800 leading-tight mb-0.5">Present Days</p>
          <p class="text-[11px] text-slate-400">Days attended in class</p>
        </div>
        <span class="text-sm font-black text-green-500 flex-shrink-0 pt-0.5">{{ presentDays }}</span>
      </div>

      <div class="flex items-start gap-3 py-3 group">
        <div class="flex flex-col items-center flex-shrink-0 w-4 pt-1">
          <div class="relative w-3.5 h-3.5 flex-shrink-0">
            <div class="absolute inset-0 rounded-full border-2 border-slate-200"></div>
            <div class="absolute inset-[3px] rounded-full bg-red-500"></div>
          </div>
          <div class="w-px flex-1 min-h-[20px] mt-1 bg-gradient-to-b from-slate-200 to-transparent"></div>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-[13px] font-black text-slate-800 leading-tight mb-0.5">Absent Days</p>
          <p class="text-[11px] text-slate-400">Days missed without leave</p>
        </div>
        <span class="text-sm font-black text-red-500 flex-shrink-0 pt-0.5">{{ absentDays }}</span>
      </div>

      <div class="flex items-start gap-3 py-3 group">
        <div class="flex flex-col items-center flex-shrink-0 w-4 pt-1">
          <div class="relative w-3.5 h-3.5 flex-shrink-0">
            <div class="absolute inset-0 rounded-full border-2 border-slate-200"></div>
            <div class="absolute inset-[3px] rounded-full bg-amber-400"></div>
          </div>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-[13px] font-black text-slate-800 leading-tight mb-0.5">Leave Days</p>
          <p class="text-[11px] text-slate-400">Approved leave taken</p>
        </div>
        <span class="text-sm font-black text-amber-500 flex-shrink-0 pt-0.5">{{ leaveDays }}</span>
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