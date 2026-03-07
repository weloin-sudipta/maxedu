<template>
  <div class="max-h-screen p-4 lg:p-8 font-sans text-slate-900">
    <div class="max-w-[1440px] mx-auto space-y-6">

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

        <div class="lg:col-span-8 space-y-6">
          <div class="bg-white rounded-[2.5rem] border border-slate-200/60 shadow-sm overflow-hidden mb-6">

            <div class="p-8 border-b border-slate-50 flex justify-between items-center">
              <div class="flex items-center gap-4">
                <div class="w-12 h-12 bg-indigo-600 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-indigo-100">
                  <i class="fa fa-calendar text-xl"></i>
                </div>
                <h2 class="text-xl font-black text-slate-800 tracking-tight">
                  {{ monthNames[currentMonth] }} <span class="text-slate-300">{{ currentYear }}</span>
                </h2>
              </div>

              <div class="flex items-center gap-2 bg-slate-50 p-1.5 rounded-2xl">
                <button @click="changeMonth(-1)" class="btn-nav"><i class="fa fa-chevron-left"></i></button>
                <button @click="setToday" class="px-4 py-2 text-[10px] font-black uppercase text-slate-500 hover:text-indigo-600 transition-colors">Today</button>
                <button @click="changeMonth(1)" class="btn-nav"><i class="fa fa-chevron-right"></i></button>
              </div>
            </div>

            <div class="p-8">
              <div v-if="loading" class="text-center py-12">
                <i class="fa fa-spinner fa-spin text-indigo-400 text-2xl"></i>
                <p class="text-xs text-slate-400 mt-2">Loading attendance...</p>
              </div>
              <template v-else>
                <div class="grid grid-cols-7 mb-6">
                  <div v-for="day in weekDays" :key="day" class="text-center text-[10px] font-black text-slate-300 uppercase tracking-widest">{{ day }}</div>
                </div>

                <div class="grid grid-cols-7 gap-3">
                  <div v-for="empty in firstDayOfMonth" :key="'empty-'+empty" class="aspect-square"></div>

                  <div v-for="date in daysInMonth" :key="date"
                       class="aspect-square rounded-[1.5rem] border border-slate-50 flex flex-col items-center justify-center relative transition-all cursor-pointer hover:shadow-md"
                       :class="getDayStatusClass(date)">

                    <span class="text-xs font-black" :class="isToday(date) ? 'text-indigo-600' : 'text-slate-400'">{{ date }}</span>

                    <div class="mt-2">
                      <div v-if="getAttendanceStatus(date) === 'P'" class="w-1.5 h-1.5 bg-green-500 rounded-full"></div>
                      <div v-else-if="getAttendanceStatus(date) === 'A'" class="w-1.5 h-1.5 bg-red-400 rounded-full"></div>
                      <div v-else-if="getAttendanceStatus(date) === 'L'" class="w-1.5 h-1.5 bg-amber-500 rounded-full"></div>
                    </div>
                  </div>
                </div>
              </template>
            </div>

            <div class="px-8 py-4 bg-slate-50/50 border-t border-slate-50 flex gap-6">
              <div v-for="l in ['Present', 'Absent', 'Leave']" :key="l" class="flex items-center gap-2">
                <span :class="['w-2 h-2 rounded-full', l === 'Present' ? 'bg-green-500' : l === 'Absent' ? 'bg-red-400' : 'bg-amber-500']"></span>
                <span class="text-[10px] font-black text-slate-400 uppercase tracking-tighter">{{ l }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="lg:col-span-4 space-y-6">

          <div class="bg-slate-900 rounded-[2.5rem] p-8 text-white shadow-xl shadow-slate-200">
            <h3 class="text-xs font-black uppercase opacity-40 mb-8 tracking-widest text-center">Monthly Score</h3>
            <div class="relative w-32 h-32 mx-auto mb-6 flex items-center justify-center">
               <svg class="w-full h-full transform -rotate-90">
                 <circle cx="64" cy="64" r="58" stroke="currentColor" stroke-width="8" fill="transparent" class="text-white/10" />
                 <circle cx="64" cy="64" r="58" stroke="currentColor" stroke-width="8" fill="transparent" class="text-indigo-500"
                   :stroke-dasharray="364.4"
                   :stroke-dashoffset="364.4 - (364.4 * monthlyPercent / 100)" />
               </svg>
               <span class="absolute text-2xl font-black">{{ monthlyPercent }}%</span>
            </div>
            <p class="text-center text-[10px] font-bold opacity-60">High attendance improves student performance by up to 12%.</p>
          </div>

          <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm">
            <h3 class="text-xs font-black uppercase text-slate-400 tracking-widest mb-6">Attendance Summary</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-[10px] font-black text-slate-400 uppercase">Total Present</span>
                <span class="text-sm font-black text-green-600">{{ monthlyPresent }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-[10px] font-black text-slate-400 uppercase">Total Absent</span>
                <span class="text-sm font-black text-red-500">{{ monthlyAbsent }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-[10px] font-black text-slate-400 uppercase">Leave</span>
                <span class="text-sm font-black text-amber-500">{{ monthlyLeave }}</span>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useAttendance } from '~/composable/useAttendance'

const config = useRuntimeConfig()
useSeoMeta({
    title: `Attendance - ${config.public.appName}`,
})

const { attendanceMap, loading, fetchAttendance } = useAttendance()

const today = new Date();
const currentMonth = ref(today.getMonth());
const currentYear = ref(today.getFullYear());

const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const weekDays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

const daysInMonth = computed(() => new Date(currentYear.value, currentMonth.value + 1, 0).getDate());
const firstDayOfMonth = computed(() => new Date(currentYear.value, currentMonth.value, 1).getDay());

const loadAttendanceData = () => {
  fetchAttendance(currentMonth.value, currentYear.value)
}

onMounted(() => {
  loadAttendanceData()
})

const changeMonth = (step) => {
  currentMonth.value += step;
  if (currentMonth.value > 11) { currentMonth.value = 0; currentYear.value++; }
  else if (currentMonth.value < 0) { currentMonth.value = 11; currentYear.value--; }
  loadAttendanceData()
};

const setToday = () => {
  currentMonth.value = today.getMonth();
  currentYear.value = today.getFullYear();
  loadAttendanceData()
};

const isToday = (date) => date === today.getDate() && currentMonth.value === today.getMonth() && currentYear.value === today.getFullYear();

const getAttendanceStatus = (date) => attendanceMap.value[`${currentYear.value}-${currentMonth.value}-${date}`] || null;

const getDayStatusClass = (date) => {
  const status = getAttendanceStatus(date);
  if (status === 'P') return 'bg-green-50/50 border-green-100';
  if (status === 'A') return 'bg-red-50/50 border-red-100';
  if (status === 'L') return 'bg-amber-50/50 border-amber-100';
  return 'bg-white';
};

const monthlyPresent = computed(() => Object.values(attendanceMap.value).filter(v => v === 'P').length)
const monthlyAbsent = computed(() => Object.values(attendanceMap.value).filter(v => v === 'A').length)
const monthlyLeave = computed(() => Object.values(attendanceMap.value).filter(v => v === 'L').length)
const monthlyPercent = computed(() => {
  const total = monthlyPresent.value + monthlyAbsent.value + monthlyLeave.value
  return total > 0 ? Math.round((monthlyPresent.value / total) * 100) : 0
})
</script>

<style scoped>
.btn-primary { @apply px-8 py-3 bg-indigo-600 text-white rounded-2xl text-[10px] font-black uppercase tracking-[0.2em] shadow-xl shadow-indigo-100 hover:bg-indigo-700 active:scale-95 transition-all; }
.btn-icon { @apply flex items-center justify-center bg-white border border-slate-200 text-slate-400 rounded-2xl hover:text-indigo-600 transition-all; }
.btn-nav { @apply w-10 h-10 flex items-center justify-center bg-white border border-slate-100 rounded-xl hover:shadow-md transition-all text-slate-400 hover:text-indigo-600; }
</style>
