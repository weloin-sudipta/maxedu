<template>
  <div class="min-h-screen bg-[#f8fafc] dark:bg-slate-950 p-4 lg:p-8 font-sans text-slate-900 dark:text-slate-100 transition-colors">
    <div class="max-w-[1440px] mx-auto space-y-6">

      <!-- HEADER -->
      <HeroHeader 
        :title="studentMeta.student_name || 'Performance Hub'" 
        :subtitle="`${studentMeta.academic_term || 'Consolidated Result'}`" 
        icon="fa fa-pie-chart"
      >
        <button @click="openDownloadModal('Semester Result')"
          class="px-5 py-3 bg-slate-900 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-800 flex items-center gap-2">
          <i class="fa fa-file-pdf-o"></i> Result PDF
        </button>

        <button @click="openDownloadModal('Academic Certificate')"
          class="px-5 py-3 bg-indigo-600 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest shadow-lg hover:bg-indigo-700 flex items-center gap-2">
          <i class="fa fa-certificate"></i> Certificate
        </button>
      </HeroHeader>

      <!-- LOADING STATE -->
      <div v-if="loading" class="bg-white dark:bg-slate-900 rounded-[2.5rem] p-8 border border-slate-200 dark:border-slate-800 shadow-sm dark:shadow-none space-y-8 animate-in transition-colors">
        <div class="flex items-center gap-6">
           <UiSkeleton height="h-14" width="w-14" class="rounded-2xl shrink-0" />
           <div class="space-y-3 w-full max-w-sm">
             <UiSkeleton height="h-6" width="w-3/4" />
             <UiSkeleton height="h-3" width="w-1/2" />
           </div>
        </div>
        <UiSkeleton height="h-64" class="rounded-xl w-full" />
      </div>

      <!-- CARD -->
      <div v-else-if="results.length > 0" class="bg-white dark:bg-slate-900 rounded-[2.5rem] border border-slate-200 dark:border-slate-800 shadow-sm dark:shadow-none overflow-hidden animate-in transition-colors">

        <!-- TOP -->
        <div class="p-8 border-b border-slate-100 dark:border-slate-800 flex flex-col md:flex-row justify-between items-center gap-6 transition-colors">

          <div class="flex items-center gap-4">
            <div class="w-14 h-14 bg-slate-50 dark:bg-slate-800 rounded-2xl flex items-center justify-center transition-colors">
              <i class="fa fa-graduation-cap text-xl text-slate-800 dark:text-slate-200"></i>
            </div>

            <div>
              <h2 class="text-lg font-black">
                {{ studentMeta.program }}
                <span class="text-slate-400">•</span>
                {{ studentMeta.assessment_group }}
              </h2>

              <p class="text-[10px] text-slate-400 font-bold uppercase mt-1">
                ID: {{ studentMeta.student_id }} • {{ studentMeta.academic_year }}
              </p>
            </div>
          </div>

          <!-- SUMMARY -->
          <div class="flex items-center gap-8">

            <div class="text-center">
              <p class="text-[9px] text-slate-400 dark:text-slate-500 uppercase transition-colors">Total Score</p>
              <p class="text-2xl font-black text-slate-800 dark:text-white transition-colors">
                {{ studentMeta.total }}
                <span class="text-slate-300 dark:text-slate-600 text-sm">/{{ studentMeta.max }}</span>
              </p>
            </div>

            <div class="text-center">
              <p class="text-[9px] text-slate-400 dark:text-slate-500 uppercase transition-colors"> Total Percentage %</p>
              <p class="text-2xl font-black text-indigo-600 dark:text-indigo-400 transition-colors">
                {{ studentMeta.percentage }}%
              </p>
            </div>

          </div>
        </div>

        <!-- TABLE -->
        <div class="overflow-x-auto">
          <table class="w-full text-left">

            <thead>
              <tr class="bg-slate-50 dark:bg-slate-800/50 transition-colors">
                <th class="p-4 text-xs">Course</th>
                <th class="p-4 text-center text-xs">Grade</th>
                <th class="p-4 text-xs">Performance</th>
                <th class="p-4 text-center text-xs">Scale</th>
                <th class="p-4 text-right text-xs">Marks</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="sub in subjects" :key="sub.id" class="border-t border-slate-100 dark:border-slate-800/50 transition-colors">

                <td class="p-4 font-bold">
                  {{ sub.name }}
                </td>

                <td class="p-4 text-center">
                  <span :class="['px-3 py-1 rounded text-white text-xs', sub.color]">
                    {{ sub.grade }}
                  </span>
                </td>

                <td class="p-4 w-[200px]">
                  <div class="h-2 bg-slate-100 dark:bg-slate-800 rounded transition-colors">
                    <div
                      class="h-2 rounded"
                      :class="sub.color"
                      :style="{ width: sub.percentage + '%' }"
                    ></div>
                  </div>
                </td>

                <td class="p-4 text-center text-xs font-bold">
                  {{ sub.scale }}
                </td>

                <td class="p-4 text-right font-bold">
                  {{ sub.marks }}/{{ sub.max }}
                </td>

              </tr>
            </tbody>

          </table>
        </div>

      </div>

      <!-- EMPTY STATE -->
      <div v-else class="bg-white dark:bg-slate-900 rounded-[2.5rem] p-20 text-center border border-dashed border-slate-200 dark:border-slate-800 transition-colors">
        <i class="fa fa-file-text-o text-slate-100 dark:text-slate-800/50 text-6xl mb-4 block transition-colors"></i>
        <p class="text-sm font-black text-slate-400 dark:text-slate-500 uppercase tracking-widest transition-colors">No results available</p>
      </div>

      <!-- FOOTER NOTE -->
      <div v-if="!loading && results.length > 0" class="bg-indigo-50 dark:bg-indigo-900/20 rounded-2xl p-6 border border-indigo-100 dark:border-indigo-900/30 flex gap-4 transition-colors">
        <i class="fa fa-info-circle text-indigo-600 dark:text-indigo-400"></i>
        <p class="text-xs text-slate-800 dark:text-slate-200 transition-colors">
          Transcript for <b>{{ studentMeta.student_name }}</b> as of {{ new Date().toLocaleDateString() }}
        </p>
      </div>

    </div>

    <!-- MODAL -->
    <div v-if="showModal" class="fixed inset-0 flex items-center justify-center bg-black/50">
      <div class="bg-white p-6 rounded-2xl w-[300px] text-center">
        <h3 class="font-bold mb-4">{{ downloadType }}</h3>
        <button @click="handleDownload"
          class="w-full py-3 bg-indigo-600 text-white rounded-xl">
          Download
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import HeroHeader from '~/components/ui/HeroHeader.vue'
import { useExamResults } from '~/composable/useExaminations'

const results = ref([])
const showModal = ref(false)
const downloadType = ref('')
const loading = ref(true)

/* FETCH */
onMounted(async () => {
  try {
    const data = await useExamResults()
    console.log("API 👉", data)

    if (Array.isArray(data)) {
      results.value = data
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

/* META */
const studentMeta = computed(() => {
  if (!results.value.length) return {}

  const first = results.value[0]

  const total = results.value.reduce((s, r) => s + (r.total_score || 0), 0)
  const max = results.value.reduce((s, r) => s + (r.maximum_score || 0), 0)

  return {
    student_name: first.student_name,
    academic_term: first.academic_term,
    academic_year: first.academic_year,
    program: first.program,
    assessment_group: first.assessment_group,
    student_id: first.student,
    total,
    max,
    percentage: max ? Math.round((total / max) * 100) : 0
  }
})

/* SUBJECTS */
const subjects = computed(() => {
  return results.value.map(r => ({
    id: r.name,
    name: r.course || '-',
    grade: r.grade || '-',
    marks: r.total_score || 0,
    max: r.maximum_score || 0,
    percentage: r.maximum_score
      ? Math.round((r.total_score / r.maximum_score) * 100)
      : 0,
    scale: r.grading_scale || '-',
    color: getColor(r.grade)
  }))
})

/* COLOR */
const getColor = (g) => {
  if (!g) return 'bg-slate-400'
  g = g.toUpperCase()

  if (['A', 'A+', 'O'].includes(g)) return 'bg-emerald-500'
  if (['B', 'B+'].includes(g)) return 'bg-indigo-500'
  if (['C', 'C+'].includes(g)) return 'bg-amber-500'
  return 'bg-rose-500'
}

/* MODAL */
const openDownloadModal = (type) => {
  downloadType.value = type
  showModal.value = true
}

/* DOWNLOAD */
const handleDownload = () => {
  console.log("Downloading:", downloadType.value)
  showModal.value = false
}
</script>