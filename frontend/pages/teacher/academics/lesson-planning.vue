<template>
  <div class="p-6 lg:p-10 max-w-7xl mx-auto custom-scrollbar animate-in fade-in slide-in-from-bottom-4 duration-500">
    <HeroHeader title="Lesson Planning" subtitle="Curriculum Tracking" icon="fa fa-map-signs">
      <div class="flex gap-2">
        <select class="bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-200 px-4 py-2 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-800 outline-none">
          <option>Data Structures (CS-101)</option>
          <option>Web Technologies (CS-201)</option>
        </select>
        <button class="bg-indigo-600 dark:bg-indigo-500 text-white px-6 py-2 rounded-xl text-xs font-black uppercase tracking-widest hover:bg-indigo-700 dark:hover:bg-indigo-600 transition-colors shadow-lg shadow-indigo-200 dark:shadow-none flex items-center gap-2"><i class="fa fa-upload"></i> Upload Material</button>
      </div>
    </HeroHeader>

    <div v-if="loading" class="mt-8">
      <UiSkeleton height="h-96" class="rounded-[2.5rem]" />
    </div>

    <div v-else class="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Syllabus Progress -->
      <div class="lg:col-span-1 space-y-6">
        <div class="bg-white dark:bg-slate-900 rounded-[2.5rem] border border-slate-100 dark:border-slate-800 shadow-sm p-8">
          <h3 class="text-xs font-black uppercase text-slate-400 dark:text-slate-500 tracking-widest mb-6 border-b border-slate-50 dark:border-slate-800/50 pb-4">Course Progress</h3>
          <div class="relative w-40 h-40 mx-auto">
             <svg class="w-full h-full -rotate-90" viewBox="0 0 36 36">
               <circle cx="18" cy="18" r="16" fill="none" class="text-slate-100 dark:text-slate-800" stroke="currentColor" stroke-width="3.5"></circle>
               <circle cx="18" cy="18" r="16" fill="none" stroke="#6366f1" stroke-width="3.5" stroke-dasharray="100" stroke-dashoffset="35" class="transition-all duration-1000 ease-out stroke-indigo-500"></circle>
             </svg>
             <div class="absolute inset-0 flex flex-col items-center justify-center">
               <span class="text-3xl font-black text-slate-800 dark:text-white">65%</span>
               <span class="text-[10px] uppercase font-bold text-slate-400 dark:text-slate-500">Completed</span>
             </div>
          </div>
          <p class="text-[11px] font-bold text-slate-500 dark:text-slate-400 text-center mt-6">You are running <span class="text-green-500">ahead of schedule</span> by 2 lectures.</p>
        </div>
      </div>

      <!-- Weekly Plan -->
      <div class="lg:col-span-2">
        <div class="bg-white dark:bg-slate-900 rounded-[2.5rem] border border-slate-100 dark:border-slate-800 shadow-sm p-8">
          <h3 class="text-xs font-black uppercase text-slate-400 dark:text-slate-500 tracking-widest mb-6">Upcoming Topics</h3>
          <div class="space-y-6">
            <div v-for="(plan, i) in lessons" :key="i" class="flex gap-6 group">
               <div class="flex flex-col items-center">
                 <div class="w-8 h-8 rounded-full flex items-center justify-center font-black text-xs transition-colors"
                      :class="plan.status === 'done' ? 'bg-green-100 text-green-500 dark:bg-green-900/40 dark:text-green-400' : 'bg-slate-100 text-slate-400 dark:bg-slate-800 dark:text-slate-500 group-hover:bg-indigo-100 group-hover:text-indigo-500 dark:group-hover:bg-indigo-900/40'">
                   {{ i + 1 }}
                 </div>
                 <div v-if="i < lessons.length - 1" class="w-px h-full bg-slate-100 dark:bg-slate-800 mt-2"></div>
               </div>
               <div class="flex-1 bg-slate-50 dark:bg-slate-800/50 p-6 rounded-2xl border border-slate-100 dark:border-slate-700/50 group-hover:border-indigo-200 dark:group-hover:border-indigo-500/30 transition-all cursor-pointer">
                 <div class="flex justify-between items-start mb-2">
                   <div>
                     <span class="text-[10px] font-black uppercase tracking-widest text-indigo-500 mb-1 block">Week {{ plan.week }}</span>
                     <h4 class="text-sm font-black text-slate-800 dark:text-slate-200">{{ plan.topic }}</h4>
                   </div>
                   <span class="px-3 py-1 bg-white dark:bg-slate-900 rounded-lg text-[9px] font-black uppercase tracking-widest border border-slate-200 dark:border-slate-700 shadow-sm"
                         :class="plan.status === 'done' ? 'text-green-500' : 'text-slate-400 dark:text-slate-500'">
                     {{ plan.status === 'done' ? 'Completed' : 'Pending' }}
                   </span>
                 </div>
                 <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed max-w-lg mb-4">{{ plan.desc }}</p>
                 <div class="flex gap-2">
                   <button v-if="plan.materials" class="flex items-center gap-2 text-[10px] font-bold text-slate-600 dark:text-slate-300 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 px-3 py-1.5 rounded-lg hover:text-indigo-600 hover:border-indigo-200 transition-colors shadow-sm">
                     <i class="fa fa-file-pdf-o text-red-400"></i> Reference.pdf
                   </button>
                   <button class="flex items-center gap-2 text-[10px] font-bold text-slate-400 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 border-dashed px-3 py-1.5 rounded-lg hover:text-indigo-600 hover:border-indigo-200 transition-colors">
                     <i class="fa fa-plus"></i> Add Material
                   </button>
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
import { ref, onMounted } from 'vue'
import HeroHeader from '~/components/ui/HeroHeader.vue'

const loading = ref(true)

const lessons = ref([
  { week: 4, topic: 'Trees and Graphs', desc: 'Introduction to non-linear data structures, binary trees, and graph traversal algorithms (BFS, DFS).', status: 'done', materials: true },
  { week: 5, topic: 'Dynamic Programming', desc: 'Solving complex problems by breaking them down into simpler subproblems. Memoization vs Tabulation.', status: 'pending', materials: false },
  { week: 6, topic: 'Greedy Algorithms', desc: 'Understanding greedy choice property. Example problems: Huffman Coding, Dijkstra’s algorithm.', status: 'pending', materials: false }
])

onMounted(() => {
  setTimeout(() => loading.value = false, 700)
})
</script>
