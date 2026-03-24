<template>
  <div class="p-6 lg:p-10 max-w-7xl mx-auto custom-scrollbar animate-in fade-in slide-in-from-bottom-4 duration-500">
    <HeroHeader title="Assignments" subtitle="Manage Classwork" icon="fa fa-tasks">
      <div class="flex gap-2">
        <button class="bg-amber-500 text-white px-6 py-2 rounded-xl text-xs font-black uppercase tracking-widest hover:bg-amber-600 transition-colors shadow-lg shadow-amber-200 dark:shadow-none flex items-center gap-2"><i class="fa fa-plus"></i> New Assignment</button>
      </div>
    </HeroHeader>

    <div v-if="loading" class="mt-8">
      <UiSkeleton height="h-[500px]" class="rounded-[2.5rem]" />
    </div>

    <div v-else class="mt-8 grid grid-cols-1 lg:grid-cols-4 gap-8">
      <!-- Active Assignments List -->
      <div class="lg:col-span-4 space-y-6">
        <div v-for="task in assignments" :key="task.id" class="bg-white dark:bg-slate-900 rounded-[2.5rem] border border-slate-100 dark:border-slate-800 shadow-sm p-6 lg:p-8 flex flex-col md:flex-row items-center justify-between gap-6 hover:shadow-xl hover:border-amber-200 dark:hover:border-amber-500/30 transition-all cursor-pointer group">
          <div class="flex items-center gap-6 w-full md:w-auto">
             <div class="w-16 h-16 rounded-2xl bg-amber-50 dark:bg-amber-900/30 flex items-center justify-center shrink-0">
               <i class="fa fa-file-text-o text-2xl text-amber-500"></i>
             </div>
             <div>
               <div class="flex items-center gap-3 mb-1">
                 <h3 class="text-lg font-black text-slate-800 dark:text-slate-100 group-hover:text-amber-600 dark:group-hover:text-amber-500 transition-colors">{{ task.title }}</h3>
                 <span class="px-2 py-0.5 rounded text-[8px] font-black uppercase tracking-widest border"
                       :class="task.status === 'Active' ? 'bg-green-50 border-green-200 text-green-600 dark:bg-green-900/30 dark:border-green-800 dark:text-green-400' : 'bg-slate-100 border-slate-200 text-slate-500 dark:bg-slate-800 dark:border-slate-700 dark:text-slate-400'">
                   {{ task.status }}
                 </span>
               </div>
               <p class="text-xs font-bold text-slate-500 dark:text-slate-400 mb-2">{{ task.class }} • Due: {{ task.dueDate }}</p>
               <!-- Progress Bar -->
               <div class="w-full max-w-xs">
                 <div class="flex justify-between text-[10px] font-black uppercase tracking-widest text-slate-400 dark:text-slate-500 mb-1">
                   <span>Submitted: {{ task.submitted }}/{{ task.total }}</span>
                   <span class="text-amber-500">{{ Math.round((task.submitted/task.total)*100) }}%</span>
                 </div>
                 <div class="w-full h-1.5 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                   <div class="h-full bg-amber-500 rounded-full transition-all" :style="{ width: `${(task.submitted/task.total)*100}%` }"></div>
                 </div>
               </div>
             </div>
          </div>
          <div class="w-full md:w-auto flex flex-col items-center md:items-end gap-2 shrink-0">
             <button class="w-full md:w-auto px-6 py-3 bg-slate-800 dark:bg-slate-100 text-white dark:text-slate-900 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-black dark:hover:bg-white transition-colors">Grade Submissions</button>
             <p v-if="task.pendingGrading > 0" class="text-[10px] font-bold text-rose-500 tracking-wide">{{ task.pendingGrading }} need grading</p>
             <p v-else class="text-[10px] font-bold text-green-500 tracking-wide"><i class="fa fa-check"></i> All graded</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import HeroHeader from '~/components/ui/HeroHeader.vue'

const loading = ref(true)

const assignments = ref([
  { id: 1, title: 'JavaScript DOM Manipulation', class: 'CS-204 (Section A)', dueDate: 'Oct 30, 2026', status: 'Active', submitted: 35, total: 40, pendingGrading: 12 },
  { id: 2, title: 'Binary Search Tree Implementation', class: 'CS-101 (Section B)', dueDate: 'Nov 02, 2026', status: 'Active', submitted: 10, total: 30, pendingGrading: 0 },
  { id: 3, title: 'Database Normalization Essay', class: 'CS-302 (Section C)', dueDate: 'Oct 15, 2026', status: 'Closed', submitted: 38, total: 38, pendingGrading: 0 }
])

onMounted(() => {
  setTimeout(() => loading.value = false, 600)
})
</script>
