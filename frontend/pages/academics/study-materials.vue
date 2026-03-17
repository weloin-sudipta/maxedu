<template>
  <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans text-slate-900">
    <div class="max-w-[1440px] mx-auto space-y-6">

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

      <div v-if="loading" class="text-center py-20">
        <i class="fa fa-spinner fa-spin text-indigo-400 text-3xl"></i>
        <p class="text-xs text-slate-400 mt-3 font-bold uppercase">Loading study materials...</p>
      </div>

      <div v-else class="grid grid-cols-1 gap-4">
        <div v-for="file in filteredFiles" :key="file.name"
          class="group bg-white rounded-[2rem] p-5 border border-slate-200/60 shadow-sm hover:border-indigo-300 transition-all flex flex-col md:flex-row items-center gap-6">

          <div
            :class="['w-16 h-16 rounded-2xl flex items-center justify-center text-2xl shrink-0', getFileBgColor(file.file_type)]">
            <i :class="['fa text-white', getFileIcon(file.file_type)]"></i>
          </div>

          <div class="flex-1 text-center md:text-left">
            <div class="flex flex-col md:flex-row md:items-center gap-2 mb-1">
              <h3 class="text-base font-black text-slate-800 tracking-tight">{{ file.title }}</h3>
              <span
                class="px-2 py-0.5 bg-slate-50 text-slate-400 text-[9px] font-black uppercase rounded border border-slate-100">{{
                  file.file_type || 'FILE' }}</span>
            </div>
            <div class="flex flex-wrap justify-center md:justify-start gap-4">
              <span class="text-[10px] font-bold text-indigo-500 uppercase tracking-widest">{{ file.course_name ||
                file.course }}</span>
              <span v-if="file.topic_name" class="text-[10px] font-bold text-emerald-500 uppercase tracking-widest">{{
                file.topic_name }}</span>
              <span v-if="file.file_size" class="text-[10px] font-bold text-slate-300 uppercase tracking-widest"><i
                  class="fa fa-database mr-1"></i> {{ file.file_size }}</span>
              <span v-if="file.upload_date" class="text-[10px] font-bold text-slate-300 uppercase tracking-widest"><i
                  class="fa fa-calendar-o mr-1"></i> {{ formatDate(file.upload_date) }}</span>
            </div>
          </div>

          <div class="flex items-center gap-3 shrink-0">
            <!-- Preview -->
            <a v-if="file.file" :href="getFileUrl(file.file)" target="_blank"
              class="w-12 h-12 flex items-center justify-center bg-slate-50 text-slate-400 rounded-xl hover:bg-slate-900 hover:text-white transition-all shadow-sm">
              <i class="fa fa-eye"></i>
            </a>

            <!-- Download -->
            <a v-if="file.file" :href="getFileUrl(file.file, true)"
              class="px-6 py-3 bg-indigo-600 text-white rounded-xl text-[10px] font-black uppercase tracking-widest shadow-lg shadow-indigo-100 hover:bg-indigo-700 transition-all">
              <i class="fa fa-download mr-2"></i> Download
            </a>
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
