<template>
  <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans text-slate-900">
    <div class="max-w-[1440px] mx-auto space-y-6">

      <!-- <header class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 p-8 flex flex-col lg:flex-row justify-between items-center gap-6">
        <div class="flex items-center gap-4">
          <div class="w-14 h-14 bg-indigo-600 rounded-2xl flex items-center justify-center text-white shadow-xl shadow-indigo-100">
            <i class="fa fa-file-text text-2xl"></i>
          </div>
          <div>
            <h1 class="text-3xl font-black tracking-tight text-slate-800">Document Repository</h1>
            <p class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mt-1">Download Syllabus, Notes & Previous Papers</p>
          </div>
        </div>

        <div class="w-full lg:w-96 relative">
          <i class="fa fa-search absolute left-4 top-1/2 -translate-y-1/2 text-slate-300"></i>
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Search by file name or subject..." 
            class="w-full bg-slate-50 border border-slate-100 rounded-2xl pl-12 pr-4 py-3 text-xs font-bold text-slate-700 outline-none focus:ring-4 focus:ring-indigo-500/10 transition-all"
          />
        </div>
      </header> -->
      <HeroHeader title="Document Repository" subtitle="Download Syllabus, Notes & Previous Papers"
        icon="fa fa-file-text" searchable v-model:search="searchQuery"
        searchPlaceholder="Search by file name or subject..." />

      <div class="flex gap-3 overflow-x-auto no-scrollbar pb-2">
        <button v-for="cat in categories" :key="cat.name" @click="activeCategory = cat.name" :class="[
          activeCategory === cat.name ? 'bg-slate-900 text-white shadow-xl shadow-slate-200' : 'bg-white text-slate-500 border-slate-200 hover:bg-slate-50',
          'px-6 py-3 rounded-2xl text-[10px] font-black uppercase tracking-widest border transition-all flex items-center gap-3 whitespace-nowrap'
        ]">
          <i :class="['fa', cat.icon]"></i>
          {{ cat.name }}
        </button>
      </div>

      <div class="grid grid-cols-1 gap-4">
        <div v-for="file in filteredFiles" :key="file.id"
          class="group bg-white rounded-[2rem] p-5 border border-slate-200/60 shadow-sm hover:border-indigo-300 transition-all flex flex-col md:flex-row items-center gap-6">

          <div :class="['w-16 h-16 rounded-2xl flex items-center justify-center text-2xl shrink-0', file.bgColor]">
            <i :class="['fa text-white', file.icon]"></i>
          </div>

          <div class="flex-1 text-center md:text-left">
            <div class="flex flex-col md:flex-row md:items-center gap-2 mb-1">
              <h3 class="text-base font-black text-slate-800 tracking-tight">{{ file.title }}</h3>
              <span
                class="px-2 py-0.5 bg-slate-50 text-slate-400 text-[9px] font-black uppercase rounded border border-slate-100">{{
                  file.type }}</span>
            </div>
            <div class="flex flex-wrap justify-center md:justify-start gap-4">
              <span class="text-[10px] font-bold text-indigo-500 uppercase tracking-widest">{{ file.subject }}</span>
              <span class="text-[10px] font-bold text-slate-300 uppercase tracking-widest"><i
                  class="fa fa-database mr-1"></i> {{ file.size }}</span>
              <span class="text-[10px] font-bold text-slate-300 uppercase tracking-widest"><i
                  class="fa fa-calendar-o mr-1"></i> {{ file.date }}</span>
            </div>
          </div>

          <div class="flex items-center gap-3 shrink-0">
            <button
              class="w-12 h-12 flex items-center justify-center bg-slate-50 text-slate-400 rounded-xl hover:bg-slate-900 hover:text-white transition-all shadow-sm">
              <i class="fa fa-eye"></i>
            </button>
            <button
              class="px-6 py-3 bg-indigo-600 text-white rounded-xl text-[10px] font-black uppercase tracking-widest shadow-lg shadow-indigo-100 hover:bg-indigo-700 transition-all">
              <i class="fa fa-download mr-2"></i> Download
            </button>
          </div>
        </div>

        <div v-if="filteredFiles.length === 0"
          class="bg-white rounded-[2.5rem] p-20 border border-dashed border-slate-200 text-center">
          <i class="fa fa-folder-open-o text-slate-100 text-6xl mb-4"></i>
          <p class="text-sm font-black text-slate-400 uppercase tracking-widest">No documents found in this category.
          </p>
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
    title: `Study Materials - ${config.public.appName}`,
    description: `Explore your academic roadmap with MaxEdu's comprehensive breakdown of subjects, chapters, and lesson details. Strategically designed to guide your learning journey and maximize exam performance.`,
    keywords: 'subjects, chapters, lessons, learning path, academic roadmap, exam preparation'
})

const activeCategory = ref('All Files');
const searchQuery = ref('');

const categories = [
  { name: 'All Files', icon: 'fa-th-large' },
  { name: 'Syllabus', icon: 'fa-map-o' },
  { name: 'Lecture Notes', icon: 'fa-file-text-o' },
  { name: 'Question Bank', icon: 'fa-bank' },
  { name: 'Lab Manuals', icon: 'fa-flask' }
];

const files = ref([
  { id: 1, title: 'Calculus Ch 4: Differentiation Rules', subject: 'Mathematics', type: 'PDF', size: '2.4 MB', date: 'Oct 12, 2025', category: 'Lecture Notes', icon: 'fa-file-pdf-o', bgColor: 'bg-red-500' },
  { id: 2, title: 'Annual Physics Syllabus 2025-26', subject: 'Physics', type: 'DOCX', size: '1.1 MB', date: 'Sep 30, 2025', category: 'Syllabus', icon: 'fa-file-word-o', bgColor: 'bg-blue-500' },
  { id: 3, title: 'Chemistry Lab Safety Protocol', subject: 'Chemistry', type: 'PDF', size: '800 KB', date: 'Oct 05, 2025', category: 'Lab Manuals', icon: 'fa-flask', bgColor: 'bg-green-500' },
  { id: 4, title: 'Mid-Term History Sample Papers', subject: 'History', type: 'ZIP', size: '15 MB', date: 'Oct 08, 2025', category: 'Question Bank', icon: 'fa-file-archive-o', bgColor: 'bg-amber-500' },
  { id: 5, title: 'English Poetry Analysis Notes', subject: 'English', type: 'PDF', size: '3.2 MB', date: 'Oct 14, 2025', category: 'Lecture Notes', icon: 'fa-file-pdf-o', bgColor: 'bg-red-500' }
]);

const filteredFiles = computed(() => {
  return files.value.filter(f => {
    const matchesCat = activeCategory.value === 'All Files' || f.category === activeCategory.value;
    const matchesSearch = f.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      f.subject.toLowerCase().includes(searchQuery.value.toLowerCase());
    return matchesCat && matchesSearch;
  });
});
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>