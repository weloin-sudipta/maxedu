<template>
  <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans text-slate-900">
    <div class="max-w-[1440px] mx-auto space-y-6">

      <HeroHeader title="Class Schedule" :subtitle="studentGroup" icon="fa fa-graduation-cap">
        <button @click="showPdfModal = true" class="btn-icon h-12 w-12" title="Print Schedule"><i class="fa fa-print"></i></button>
        <button @click="showPdfModal = true" class="btn-primary">Download PDF</button>
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
                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">{{ period.endTime }}</span>
              </div>

              <div class="hidden md:block w-px h-12 bg-slate-100"></div>

              <div class="flex-1 text-center md:text-left">
                <div class="flex flex-col md:flex-row md:items-center gap-2 mb-1">
                  <h3 class="text-lg font-black text-slate-800 tracking-tight">{{ period.subject }}</h3>
                  <span :class="['px-2 py-0.5 rounded-md text-[9px] font-black uppercase tracking-tighter border', categoryStyles[period.type]]">
                    {{ period.type }}
                  </span>
                </div>
                <p class="text-xs font-bold text-slate-400 flex items-center justify-center md:justify-start gap-2">
                  <i class="fa fa-user-circle-o text-indigo-400"></i> {{ period.teacher }}
                </p>
              </div>

              <div class="bg-slate-50 px-6 py-3 rounded-2xl border border-slate-100 shrink-0">
                <span class="block text-[10px] font-black text-slate-300 uppercase tracking-widest mb-1 text-center">Room</span>
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

    <!-- PDF Preview Modal -->
    <div v-if="showPdfModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm transition-all duration-300">
      <div class="bg-white rounded-[2rem] shadow-2xl w-full max-w-6xl max-h-[90vh] flex flex-col overflow-hidden animate-fade-in-up">
        <div class="px-8 py-6 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <div>
            <h2 class="text-xl font-black text-slate-800 tracking-tight">Routine Matrix</h2>
            <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mt-1">Preview & Export</p>
          </div>
          <button @click="showPdfModal = false" class="w-10 h-10 rounded-2xl bg-white shadow-sm border border-slate-200 text-slate-400 hover:text-red-500 hover:border-red-200 transition-all flex items-center justify-center">
            <i class="fa fa-times"></i>
          </button>
        </div>

        <div class="p-8 overflow-y-auto flex-1 bg-white custom-scrollbar" ref="pdfContentRef">
          <div class="timetable-print-wrapper overflow-x-auto">
            <table class="w-full border-collapse text-center text-sm border border-slate-200 rounded-xl overflow-hidden shadow-sm">
              <thead>
                <tr class="bg-slate-50/80 text-slate-500 font-bold uppercase text-[10px] tracking-widest border-b border-slate-200">
                  <th class="p-5 border-r border-slate-200 bg-white shadow-sm font-black text-indigo-900 w-32">Day \ Time</th>
                  <th v-for="time in uniqueTimeSlots" :key="time" class="p-5 border-r border-slate-200 whitespace-nowrap">{{ time }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="day in weekDays" :key="day" class="border-b border-slate-100 hover:bg-slate-50/50 transition-colors">
                  <td class="p-5 border-r border-slate-200 font-black text-slate-700 bg-slate-50/50 tracking-wider shadow-[2px_0_5px_-2px_rgba(0,0,0,0.05)]">{{ day }}</td>
                  <td v-for="time in uniqueTimeSlots" :key="time" class="p-3 border-r border-slate-100 relative min-w-[140px]">
                    <div v-if="getSlot(day, time)" class="flex flex-col gap-1 items-center justify-center p-3 rounded-2xl bg-indigo-50/80 border border-indigo-100/50 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all">
                      <span class="cell-sub font-black text-indigo-900 leading-tight block whitespace-nowrap text-[13px]">{{ getSlot(day, time).subject }}</span>
                      <span class="cell-tea text-[10px] text-indigo-500 font-bold whitespace-nowrap flex items-center gap-1.5"><i class="fa fa-user opacity-50"></i>{{ getSlot(day, time).teacher }}</span>
                      <span class="cell-room text-[9px] text-slate-400 font-black uppercase tracking-widest bg-white/60 px-2 py-0.5 rounded-lg border border-slate-200">{{ getSlot(day, time).room }}</span>
                    </div>
                    <span v-else class="text-slate-200 font-bold text-2xl opacity-50">-</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="px-8 py-5 bg-slate-50/80 border-t border-slate-100 flex justify-end items-center gap-4">
          <button @click="showPdfModal = false" class="px-6 py-3 rounded-2xl font-bold text-slate-500 hover:bg-slate-200/50 hover:text-slate-700 transition-all text-xs uppercase tracking-widest">Cancel</button>
          <button @click="downloadPdf" :disabled="isDownloading" class="px-8 py-3 rounded-2xl font-black text-white bg-indigo-600 hover:bg-indigo-700 transition-all flex items-center gap-3 shadow-[0_8px_16px_-6px_rgba(79,70,229,0.4)] hover:shadow-[0_12px_20px_-6px_rgba(79,70,229,0.5)] hover:-translate-y-0.5 active:scale-95 disabled:opacity-70 disabled:pointer-events-none text-xs uppercase tracking-widest">
            <i v-if="isDownloading" class="fa fa-spinner fa-spin text-indigo-200"></i>
            <i v-else class="fa fa-download text-indigo-200"></i>
            {{ isDownloading ? 'Generating Print...' : 'Export PDF' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import HeroHeader from '~/components/ui/HeroHeader.vue';
import { useTimetable } from '~/composable/useTimetable';

const config = useRuntimeConfig();
useSeoMeta({
  title: `Timetable - ${config.public.appName}`,
  description: `Explore your academic roadmap with MaxEdu's comprehensive breakdown of subjects, chapters, and lesson details.`,
  keywords: 'subjects, chapters, lessons, learning path, academic roadmap, exam preparation'
});

const {
  activeDay,
  weekDays,
  categoryStyles,
  isLoading,
  studentGroup,
  showPdfModal,
  isDownloading,
  pdfContentRef,
  currentDaySchedule,
  uniqueTimeSlots,
  getSlot,
  fetchSchedule,
  downloadPdf,
} = useTimetable();

onMounted(fetchSchedule);
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

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  @apply bg-slate-50 rounded-full;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  @apply bg-slate-200 rounded-full hover:bg-slate-300;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px) scale(0.95); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
</style>