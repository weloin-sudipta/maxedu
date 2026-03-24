<template>
  <div class="p-6 lg:p-10 max-w-7xl mx-auto custom-scrollbar animate-in fade-in slide-in-from-bottom-4 duration-500">
    <HeroHeader title="My Classes" subtitle="Assigned Sections" icon="fa fa-users">
      <div class="flex gap-2">
        <button class="bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-400 px-4 py-2 rounded-xl text-xs font-black uppercase tracking-widest hover:bg-indigo-100 transition-colors border border-transparent dark:border-indigo-800">Filter by Term</button>
      </div>
    </HeroHeader>

    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
      <UiSkeleton v-for="n in 3" :key="n" height="h-48" class="rounded-[2.5rem]" />
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
      <div v-for="cls in classes" :key="cls.id" class="bg-white dark:bg-slate-900 rounded-[2.5rem] border border-slate-100 dark:border-slate-800 p-8 shadow-sm hover:shadow-xl hover:border-indigo-200 dark:hover:border-indigo-500/30 transition-all group cursor-pointer">
        <div class="flex justify-between items-start mb-6">
          <div class="w-12 h-12 rounded-2xl bg-indigo-50 dark:bg-indigo-900/30 flex items-center justify-center group-hover:bg-indigo-500 transition-colors">
            <i class="fa fa-book text-indigo-500 dark:text-indigo-400 group-hover:text-white transition-colors"></i>
          </div>
          <span class="px-3 py-1 bg-slate-50 dark:bg-slate-800 rounded-full text-[10px] font-black uppercase text-slate-500 dark:text-slate-400 tracking-widest border border-slate-100 dark:border-slate-700">Sec {{ cls.section }}</span>
        </div>

        <h3 class="text-xl font-black text-slate-800 dark:text-slate-100 mb-1 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">{{ cls.subject }}</h3>
        <p class="text-xs font-bold text-slate-400 dark:text-slate-500 mb-6 flex items-center gap-2"><i class="fa fa-map-marker"></i> Room {{ cls.room }}</p>

        <div class="flex justify-between items-end border-t border-slate-50 dark:border-slate-800/50 pt-4">
          <div>
            <span class="block text-[10px] uppercase font-black text-slate-400 dark:text-slate-500 tracking-widest mb-1">Students</span>
            <span class="text-lg font-black text-slate-800 dark:text-slate-200">{{ cls.students }}</span>
          </div>
          <div class="text-right">
            <span class="block text-[10px] uppercase font-black text-slate-400 dark:text-slate-500 tracking-widest mb-1">Avg Grade</span>
            <span class="text-lg font-black" :class="cls.avgGrade >= 75 ? 'text-green-500' : 'text-amber-500'">{{ cls.avgGrade }}%</span>
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

const classes = ref([
  { id: 1, subject: 'Computer Networks', section: 'A1', room: '302', students: 45, avgGrade: 82 },
  { id: 2, subject: 'Data Structures', section: 'B2', room: 'Lab 4', students: 30, avgGrade: 71 },
  { id: 3, subject: 'Web Technologies', section: 'A3', room: 'Audit. 1', students: 60, avgGrade: 88 }
])

onMounted(() => {
  setTimeout(() => loading.value = false, 800)
})
</script>
