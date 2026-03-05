<template>
  <div class="max-h-screen p-4 lg:p-8 font-sans text-slate-900">
    <div class="max-w-[1440px] mx-auto space-y-6">
      
      <!-- <header class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 p-8 flex flex-col md:flex-row justify-between items-center gap-6">
        <div>
          <h1 class="text-3xl font-black tracking-tight text-slate-800">Attendance Center</h1>
          <p class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mt-1">Manage and View Student Presence</p>
        </div>
        
        <div class="flex gap-3">
          <button class="btn-icon h-12 w-12" title="Download Report"><i class="fa fa-file-pdf-o"></i></button>
          <button class="btn-primary">Mark Daily Attendance</button>
        </div>
      </header> -->

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
          
          <!-- <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm">
            <h3 class="text-xs font-black uppercase text-slate-400 tracking-widest mb-6">Selected Student</h3>
            <div class="flex items-center gap-4 p-4 bg-slate-50 rounded-2xl border border-slate-100">
              <img src="https://i.pravatar.cc/150?u=edward" class="w-12 h-12 rounded-xl object-cover" />
              <div>
                <p class="text-sm font-black text-slate-800">Edward Thomas</p>
                <p class="text-[10px] font-bold text-slate-400 uppercase">Roll No: 100035</p>
              </div>
            </div>
          </div> -->

          <div class="bg-slate-900 rounded-[2.5rem] p-8 text-white shadow-xl shadow-slate-200">
            <h3 class="text-xs font-black uppercase opacity-40 mb-8 tracking-widest text-center">Monthly Score</h3>
            <div class="relative w-32 h-32 mx-auto mb-6 flex items-center justify-center">
               <svg class="w-full h-full transform -rotate-90">
                 <circle cx="64" cy="64" r="58" stroke="currentColor" stroke-width="8" fill="transparent" class="text-white/10" />
                 <circle cx="64" cy="64" r="58" stroke="currentColor" stroke-width="8" fill="transparent" class="text-indigo-500" stroke-dasharray="364.4" stroke-dashoffset="20" />
               </svg>
               <span class="absolute text-2xl font-black">94%</span>
            </div>
            <p class="text-center text-[10px] font-bold opacity-60">High attendance improves student performance by up to 12%.</p>
          </div>

          <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm">
            <h3 class="text-xs font-black uppercase text-slate-400 tracking-widest mb-6">Recent Alerts</h3>
            <div class="space-y-4">
              <div class="flex items-start gap-3">
                <div class="w-2 h-2 rounded-full bg-red-400 mt-1.5"></div>
                <div>
                  <p class="text-xs font-black text-slate-700">Absent on Oct 12</p>
                  <p class="text-[10px] text-slate-400 font-medium">Auto-SMS sent to Parent</p>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const config = useRuntimeConfig()
useSeoMeta({
    title: `Attendance - ${config.public.appName}`,
    description: `Explore your academic roadmap with MaxEdu's comprehensive breakdown of subjects, chapters, and lesson details. Strategically designed to guide your learning journey and maximize exam performance.`,
    keywords: 'subjects, chapters, lessons, learning path, academic roadmap, exam preparation'
})

// --- CALENDAR LOGIC ---
const today = new Date();
const currentMonth = ref(today.getMonth());
const currentYear = ref(today.getFullYear());

const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const weekDays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

const daysInMonth = computed(() => new Date(currentYear.value, currentMonth.value + 1, 0).getDate());
const firstDayOfMonth = computed(() => new Date(currentYear.value, currentMonth.value, 1).getDay());

const changeMonth = (step) => {
  currentMonth.value += step;
  if (currentMonth.value > 11) { currentMonth.value = 0; currentYear.value++; }
  else if (currentMonth.value < 0) { currentMonth.value = 11; currentYear.value--; }
};

const setToday = () => {
  currentMonth.value = today.getMonth();
  currentYear.value = today.getFullYear();
};

const isToday = (date) => date === today.getDate() && currentMonth.value === today.getMonth() && currentYear.value === today.getFullYear();

// --- MOCK DATA ---
const attendanceData = ref({
  '2026-2-2': 'P', '2026-2-3': 'P', '2026-2-4': 'L', '2026-2-5': 'P', '2026-2-6': 'P', '2026-2-9': 'P', '2026-2-12': 'A',
});

const getAttendanceStatus = (date) => attendanceData.value[`${currentYear.value}-${currentMonth.value}-${date}`] || null;

const getDayStatusClass = (date) => {
  const status = getAttendanceStatus(date);
  if (status === 'P') return 'bg-green-50/50 border-green-100';
  if (status === 'A') return 'bg-red-50/50 border-red-100';
  if (status === 'L') return 'bg-amber-50/50 border-amber-100';
  return 'bg-white';
};
</script>

<style scoped>
.btn-primary { @apply px-8 py-3 bg-indigo-600 text-white rounded-2xl text-[10px] font-black uppercase tracking-[0.2em] shadow-xl shadow-indigo-100 hover:bg-indigo-700 active:scale-95 transition-all; }
.btn-icon { @apply flex items-center justify-center bg-white border border-slate-200 text-slate-400 rounded-2xl hover:text-indigo-600 transition-all; }
.btn-nav { @apply w-10 h-10 flex items-center justify-center bg-white border border-slate-100 rounded-xl hover:shadow-md transition-all text-slate-400 hover:text-indigo-600; }
</style>