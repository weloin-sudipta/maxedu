<template>
  <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans text-slate-900">
    <div class="max-w-[1440px] mx-auto space-y-6">

      <!-- <header class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 p-8 flex flex-col md:flex-row justify-between items-center gap-6">
        <div>
          <h1 class="text-3xl font-black tracking-tight text-slate-800">Assignments</h1>
          <p class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mt-1">Manage coursework and submissions</p>
        </div>
        
        <div class="flex gap-3">
          <div class="hidden md:flex flex-col items-end mr-4">
            <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Completion Rate</span>
            <span class="text-sm font-black text-indigo-600">85% Weekly</span>
          </div>
          <button class="btn-primary">View Archived</button>
        </div>
      </header> -->
      <HeroHeader title="Assignments" subtitle="Manage coursework and submissions" icon="fa fa-graduation-cap">
        <div class="hidden md:flex flex-col items-end mr-4">
          <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Completion Rate</span>
          <span class="text-sm font-black text-indigo-600">85% Weekly</span>
        </div>
        <button class="btn-primary">View Archived</button>
      </HeroHeader>

      <div class="flex items-center gap-2 overflow-x-auto no-scrollbar pb-2">
        <button v-for="tab in ['Active', 'Submitted', 'Overdue', 'Evaluated']" :key="tab" @click="activeTab = tab"
          :class="[
            activeTab === tab
              ? 'bg-slate-900 text-white shadow-xl shadow-slate-200'
              : 'bg-white text-slate-500 border-slate-200 hover:bg-slate-50',
            'px-8 py-3 rounded-2xl text-xs font-black uppercase tracking-widest transition-all border whitespace-nowrap'
          ]">
          {{ tab }}
        </button>
      </div>

      <div class="grid grid-cols-1 gap-4">
        <div v-for="task in filteredAssignments" :key="task.id"
          class="group bg-white rounded-[2rem] p-6 border border-slate-200/60 shadow-sm hover:border-indigo-300 transition-all flex flex-col lg:flex-row lg:items-center gap-6">

          <div class="flex items-center gap-5 lg:w-1/3">
            <div
              :class="['w-14 h-14 rounded-2xl flex items-center justify-center text-xl shrink-0 shadow-sm', task.colorClass]">
              <i :class="['fa', task.icon]"></i>
            </div>
            <div>
              <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">{{ task.subject }}</p>
              <h3
                class="text-lg font-black text-slate-800 tracking-tight group-hover:text-indigo-600 transition-colors">
                {{ task.title }}</h3>
            </div>
          </div>

          <div class="flex flex-1 items-center gap-8">
            <div class="flex flex-col">
              <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Due Date</span>
              <div class="flex items-center gap-2">
                <i class="fa fa-clock-o text-red-400 text-xs"></i>
                <span class="text-xs font-bold text-slate-600">{{ task.dueDate }}</span>
              </div>
            </div>

            <div class="hidden md:flex flex-col flex-1 max-w-[200px]">
              <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Estimated Effort</span>
              <div class="w-full bg-slate-50 h-1.5 rounded-full overflow-hidden">
                <div class="bg-indigo-400 h-full" :style="{ width: task.difficulty + '%' }"></div>
              </div>
            </div>
          </div>

          <div class="flex items-center gap-3 lg:justify-end">
            <button class="btn-icon h-11 w-11"><i class="fa fa-download"></i></button>
            <button v-if="task.status === 'Active'"
              class="px-6 py-2.5 bg-indigo-600 text-white rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-900 transition-all">
              Submit Task
            </button>
            <button v-else
              class="px-6 py-2.5 bg-slate-100 text-slate-400 rounded-xl text-[10px] font-black uppercase tracking-widest cursor-default">
              {{ task.status }}
            </button>
          </div>
        </div>

        <div v-if="filteredAssignments.length === 0"
          class="bg-white rounded-[2.5rem] p-20 border border-dashed border-slate-200 text-center">
          <i class="fa fa-check-circle text-green-200 text-5xl mb-4"></i>
          <p class="text-sm font-black text-slate-400 uppercase tracking-widest">All caught up! No {{
            activeTab.toLowerCase() }} tasks.</p>
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
    title: `Assignments - ${config.public.appName}`,
    description: `Explore your academic roadmap with MaxEdu's comprehensive breakdown of subjects, chapters, and lesson details. Strategically designed to guide your learning journey and maximize exam performance.`,
    keywords: 'subjects, chapters, lessons, learning path, academic roadmap, exam preparation'
})

const activeTab = ref('Active');

const assignments = ref([
  {
    id: 1,
    subject: 'Advanced Mathematics',
    title: 'Trigonometry Problem Set 4',
    dueDate: 'Oct 20, 2025 (11:59 PM)',
    status: 'Active',
    difficulty: 80,
    icon: 'fa-calculator',
    colorClass: 'bg-blue-50 text-blue-500'
  },
  {
    id: 2,
    subject: 'General Science',
    title: 'Atomic Structure Lab Report',
    dueDate: 'Oct 22, 2025 (04:00 PM)',
    status: 'Active',
    difficulty: 45,
    icon: 'fa-flask',
    colorClass: 'bg-purple-50 text-purple-500'
  },
  {
    id: 3,
    subject: 'English Literature',
    title: 'Analysis of Shakespearean Sonnets',
    dueDate: 'Oct 15, 2025',
    status: 'Submitted',
    difficulty: 60,
    icon: 'fa-pencil',
    colorClass: 'bg-orange-50 text-orange-500'
  },
  {
    id: 4,
    subject: 'History',
    title: 'The Industrial Revolution Essay',
    dueDate: 'Oct 10, 2025',
    status: 'Overdue',
    difficulty: 90,
    icon: 'fa-landmark',
    colorClass: 'bg-red-50 text-red-500'
  }
]);

const filteredAssignments = computed(() => {
  return assignments.value.filter(task => task.status === activeTab.value);
});
</script>

<style scoped>
.btn-primary {
  @apply px-8 py-3 bg-indigo-600 text-white rounded-2xl text-[10px] font-black uppercase tracking-[0.2em] shadow-xl shadow-indigo-100 hover:bg-indigo-700 transition-all;
}

.btn-icon {
  @apply flex items-center justify-center bg-white border border-slate-200 text-slate-400 rounded-2xl hover:text-indigo-600 transition-all shadow-sm;
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>