<template>
  <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans text-slate-900">
    <div class="max-w-[1440px] mx-auto space-y-6">

      <!-- <header class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 p-8 flex flex-col md:flex-row justify-between items-center gap-6">
        <div>
          <h1 class="text-3xl font-black tracking-tight text-slate-800">Class Schedule</h1>
          <p class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mt-1">Academic Timetable • Section A</p>
        </div>
        
        <div class="flex gap-3">
          <button class="btn-icon h-12 w-12" title="Print Schedule"><i class="fa fa-print"></i></button>
          <button class="btn-primary">Download PDF</button>
        </div>
      </header> -->
      <HeroHeader title="Class Schedule" subtitle="Academic Timetable • Section A" icon="fa fa-graduation-cap">
        <button class="btn-icon h-12 w-12" title="Print Schedule"><i class="fa fa-print"></i></button>
        <button class="btn-primary">Download PDF</button>
      </HeroHeader>

      <nav class="flex items-center gap-2 overflow-x-auto no-scrollbar pb-2">
        <button v-for="day in weekDays" :key="day" @click="activeDay = day" :class="[
          activeDay === day
            ? 'bg-slate-900 text-white shadow-xl shadow-slate-200'
            : 'bg-white text-slate-500 border-slate-200 hover:bg-slate-50',
          'px-8 py-3 rounded-2xl text-xs font-black uppercase tracking-widest transition-all border whitespace-nowrap'
        ]">
          {{ day }}
        </button>
      </nav>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

        <div class="lg:col-span-8 space-y-4">
          <div v-if="currentDaySchedule.length > 0" class="space-y-4">
            <div v-for="(period, index) in currentDaySchedule" :key="index"
              class="group relative bg-white rounded-[2rem] p-6 border border-slate-200/60 shadow-sm flex flex-col md:flex-row items-center gap-6 hover:border-indigo-200 transition-all">

              <div class="w-full md:w-32 flex flex-col items-center md:items-start shrink-0">
                <span class="text-sm font-black text-slate-800">{{ period.startTime }}</span>
                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">{{ period.endTime
                  }}</span>
              </div>

              <div class="hidden md:block w-px h-12 bg-slate-100"></div>

              <div class="flex-1 text-center md:text-left">
                <div class="flex flex-col md:flex-row md:items-center gap-2 mb-1">
                  <h3 class="text-lg font-black text-slate-800 tracking-tight">{{ period.subject }}</h3>
                  <span
                    :class="['px-2 py-0.5 rounded-md text-[9px] font-black uppercase tracking-tighter border', categoryStyles[period.type]]">
                    {{ period.type }}
                  </span>
                </div>
                <p class="text-xs font-bold text-slate-400 flex items-center justify-center md:justify-start gap-2">
                  <i class="fa fa-user-circle-o text-indigo-400"></i> {{ period.teacher }}
                </p>
              </div>

              <div class="bg-slate-50 px-6 py-3 rounded-2xl border border-slate-100 shrink-0">
                <span
                  class="block text-[10px] font-black text-slate-300 uppercase tracking-widest mb-1 text-center">Room</span>
                <span class="block text-sm font-black text-slate-700 text-center">{{ period.room }}</span>
              </div>
            </div>
          </div>

          <div v-else class="bg-white rounded-[2.5rem] p-20 border border-dashed border-slate-200 text-center">
            <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4">
              <i class="fa fa-coffee text-slate-300"></i>
            </div>
            <p class="text-sm font-black text-slate-400 uppercase tracking-widest">No classes scheduled for today</p>
          </div>
        </div>

        <div class="lg:col-span-4 space-y-6">
          <div class="bg-indigo-600 rounded-[2.5rem] p-8 text-white shadow-xl shadow-indigo-100">
            <p class="text-[10px] font-black uppercase tracking-widest opacity-60 mb-6">Class Coordinator</p>
            <div class="flex items-center gap-4">
              <img src="https://i.pravatar.cc/150?u=teacher"
                class="w-14 h-14 rounded-2xl border-2 border-indigo-400 shadow-lg" />
              <div>
                <p class="text-lg font-black leading-tight">Prof. Sarah Jenkins</p>
                <p class="text-xs font-medium opacity-70">sarah.j@school.edu</p>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm">
            <h3 class="text-xs font-black uppercase text-slate-400 tracking-widest mb-6">Weekly Load</h3>
            <div class="space-y-4">
              <div v-for="stat in ['Core Subjects: 18h', 'Labs: 4h', 'Extracurricular: 2h']" :key="stat"
                class="flex items-center gap-3">
                <div class="w-1.5 h-1.5 rounded-full bg-indigo-500"></div>
                <span class="text-xs font-bold text-slate-600">{{ stat }}</span>
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
import HeroHeader from '~/components/ui/HeroHeader.vue'

const config = useRuntimeConfig()
useSeoMeta({
    title: `Timetable - ${config.public.appName}`,
    description: `Explore your academic roadmap with MaxEdu's comprehensive breakdown of subjects, chapters, and lesson details. Strategically designed to guide your learning journey and maximize exam performance.`,
    keywords: 'subjects, chapters, lessons, learning path, academic roadmap, exam preparation'
})

const activeDay = ref('Monday');
const weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

const categoryStyles = {
  'Lecture': 'bg-indigo-50 text-indigo-600 border-indigo-100',
  'Lab': 'bg-green-50 text-green-600 border-green-100',
  'Break': 'bg-slate-50 text-slate-400 border-slate-100',
  'Activity': 'bg-amber-50 text-amber-600 border-amber-100'
};

/**
 * STATIC DATA
 * Later, you can replace this with: 
 * timetableData.value = await api.getTimetable()
 */
const timetableData = ref({
  'Monday': [
    { startTime: '08:30 AM', endTime: '09:30 AM', subject: 'Advanced Mathematics', teacher: 'Dr. Robert Fox', room: 'Room 302', type: 'Lecture' },
    { startTime: '09:30 AM', endTime: '10:30 AM', subject: 'Physics Practical', teacher: 'Prof. Albert G.', room: 'Lab 01', type: 'Lab' },
    { startTime: '10:30 AM', endTime: '11:00 AM', subject: 'Short Break', teacher: 'N/A', room: 'Cafeteria', type: 'Break' },
    { startTime: '11:00 AM', endTime: '12:00 PM', subject: 'English Literature', teacher: 'Ms. Emily Blunt', room: 'Room 105', type: 'Lecture' }
  ],
  'Tuesday': [
    { startTime: '08:30 AM', endTime: '09:30 AM', subject: 'Chemistry', teacher: 'Dr. Walter White', room: 'Room 204', type: 'Lecture' },
    { startTime: '09:30 AM', endTime: '10:30 AM', subject: 'Computer Science', teacher: 'Mr. Alan Turing', room: 'IT Suite 2', type: 'Lab' }
  ],
  // Add other days as needed...
  'Sunday': []
});

// Filter schedule based on active button
const currentDaySchedule = computed(() => {
  return timetableData.value[activeDay.value] || [];
});
</script>

<style scoped>
.btn-primary {
  @apply px-8 py-3 bg-indigo-600 text-white rounded-2xl text-[10px] font-black uppercase tracking-[0.2em] shadow-xl shadow-indigo-100 hover:bg-indigo-700 transition-all active:scale-95;
}

.btn-icon {
  @apply flex items-center justify-center bg-white border border-slate-200 text-slate-400 rounded-2xl hover:text-indigo-600 transition-all shadow-sm;
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>