<template>
  <div class="min-h-screen bg-[#f8fafc] dark:bg-slate-950 p-4 lg:p-8 font-sans text-slate-900 dark:text-slate-100 transition-colors">
    <div class="max-w-[1440px] mx-auto space-y-6">

      <HeroHeader title="Document Repository" subtitle="Download Syllabus, Notes & Previous Papers"
        icon="fa fa-file-text" searchable v-model:search="searchQuery"
        searchPlaceholder="Search by file name or subject..." />

      <div class="flex gap-3 overflow-x-auto no-scrollbar pb-2">
        <button v-for="cat in categories" :key="cat.name" @click="activeCategory = cat.name" :class="[
          activeCategory === cat.name ? 'bg-slate-900 dark:bg-indigo-600 text-white shadow-xl shadow-slate-200 dark:shadow-none' : 'bg-white dark:bg-slate-900 text-slate-500 dark:text-slate-400 border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800',
          'px-6 py-3 rounded-2xl text-[10px] font-black uppercase tracking-widest border transition-all flex items-center gap-3 whitespace-nowrap'
        ]">
          <i :class="['fa', cat.icon]"></i>
          {{ cat.name }}
        </button>
      </div>

      <div v-if="loading" class="grid grid-cols-1 gap-4 mt-6">
        <UiSkeleton height="h-24" v-for="i in 3" :key="i" />
      </div>

      <div v-else class="grid grid-cols-1 gap-4 animate-in">
        <UiCard v-for="file in filteredFiles" :key="file.name" padding="p-5" rounded="rounded-[2rem]"
          class="group hover:border-indigo-300 dark:hover:border-indigo-600/50 transition-all flex flex-col md:flex-row items-center gap-6">

          <div
            :class="['w-16 h-16 rounded-2xl flex items-center justify-center text-2xl shrink-0', getFileBgColor(file.file_type)]">
            <i :class="['fa text-white', getFileIcon(file.file_type)]"></i>
          </div>

          <div class="flex-1 text-center md:text-left">
            <div class="flex flex-col md:flex-row md:items-center gap-2 mb-1">
              <h3 class="text-base font-black text-slate-800 dark:text-slate-200 tracking-tight transition-colors">{{ file.title }}</h3>
              <span
                class="px-2 py-0.5 bg-slate-50 dark:bg-slate-800/50 text-slate-400 dark:text-slate-500 text-[9px] font-black uppercase rounded border border-slate-100 dark:border-slate-700/50 transition-colors">{{
                  file.file_type || 'FILE' }}</span>
            </div>
            <div class="flex flex-wrap justify-center md:justify-start gap-4">
              <span class="text-[10px] font-bold text-indigo-500 dark:text-indigo-400 uppercase tracking-widest transition-colors">{{ file.course_name ||
                file.course }}</span>
              <span v-if="file.topic_name" class="text-[10px] font-bold text-emerald-500 dark:text-emerald-400 uppercase tracking-widest transition-colors">{{
                file.topic_name }}</span>
              <span v-if="file.file_size" class="text-[10px] font-bold text-slate-300 dark:text-slate-600 uppercase tracking-widest transition-colors"><i
                  class="fa fa-database mr-1"></i> {{ file.file_size }}</span>
              <span v-if="file.upload_date" class="text-[10px] font-bold text-slate-300 dark:text-slate-600 uppercase tracking-widest transition-colors"><i
                  class="fa fa-calendar-o mr-1"></i> {{ formatDate(file.upload_date) }}</span>
            </div>
          </div>

          <div class="flex items-center gap-3 shrink-0">
            <!-- Preview -->
            <a v-if="file.file" :href="getFileUrl(file.file)" target="_blank"
              class="w-12 h-12 flex items-center justify-center bg-slate-50 dark:bg-slate-800 text-slate-400 dark:text-slate-500 rounded-xl hover:bg-slate-900 dark:hover:bg-slate-700 hover:text-white dark:hover:text-slate-200 transition-all shadow-sm dark:shadow-none">
              <i class="fa fa-eye"></i>
            </a>

            <!-- Download -->
            <a v-if="file.file" :href="getFileUrl(file.file, true)"
              class="px-6 py-3 bg-indigo-600 text-white rounded-xl text-[10px] font-black uppercase tracking-widest shadow-lg shadow-indigo-100 dark:shadow-none hover:bg-indigo-700 dark:hover:bg-indigo-500 transition-all">
              <i class="fa fa-download mr-2"></i> Download
            </a>
          </div>
        </UiCard>

        <UiCard v-if="filteredFiles.length === 0" padding="p-20"
          class="border-dashed dark:border-slate-800 text-center transition-colors">
          <i class="fa fa-folder-open-o text-slate-100 dark:text-slate-800/50 text-6xl mb-4 transition-colors"></i>
          <p class="text-sm font-black text-slate-400 dark:text-slate-500 uppercase tracking-widest transition-colors">No documents found in this category.
          </p>
        </UiCard>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import HeroHeader from '~/components/ui/HeroHeader.vue'
import { useStudyMaterials } from '~/composable/useStudyMaterials'

const config = useRuntimeConfig()
useSeoMeta({
  title: `Study Materials - ${config.public.appName}`,
})

const { materials, loading, fetchMaterials } = useStudyMaterials()

const activeCategory = ref('All Files');
const searchQuery = ref('');

const categories = [
  { name: 'All Files', icon: 'fa-th-large' },
  { name: 'Syllabus', icon: 'fa-map-o' },
  { name: 'Lecture Notes', icon: 'fa-file-text-o' },
  { name: 'Question Bank', icon: 'fa-bank' },
  { name: 'Lab Manuals', icon: 'fa-flask' }
];

onMounted(() => {
  fetchMaterials()
})

const filteredFiles = computed(() => {
  return materials.value.filter(f => {
    const matchesCat = activeCategory.value === 'All Files' || f.category === activeCategory.value;
    const matchesSearch = f.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (f.course_name || '').toLowerCase().includes(searchQuery.value.toLowerCase());
    return matchesCat && matchesSearch;
  });
});

const getFileIcon = (type) => {
  const map = { PDF: 'fa-file-pdf-o', DOCX: 'fa-file-word-o', DOC: 'fa-file-word-o', ZIP: 'fa-file-archive-o', XLSX: 'fa-file-excel-o', PPT: 'fa-file-powerpoint-o', PPTX: 'fa-file-powerpoint-o' }
  return map[type] || 'fa-file-o'
}

const getFileBgColor = (type) => {
  const map = { PDF: 'bg-red-500', DOCX: 'bg-blue-500', DOC: 'bg-blue-500', ZIP: 'bg-amber-500', XLSX: 'bg-green-500', PPT: 'bg-orange-500', PPTX: 'bg-orange-500' }
  return map[type] || 'bg-slate-500'
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const getFileUrl = (filePath, isDownload = false) => {
  if (!filePath) return ''

  if (filePath.startsWith('http')) return filePath

  // ✅ Always use API for download
  if (isDownload) {
    return `${config.public.apiBaseUrl}/api/method/frappe.utils.file_manager.download_file?file_url=${encodeURIComponent(filePath)}`
  }

  // Preview (normal)
  return `${config.public.apiBaseUrl}${filePath}`
}


</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>
