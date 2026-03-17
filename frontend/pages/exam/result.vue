<template>
  <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans text-slate-900">
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

      <!-- CARD -->
      <div class="bg-white rounded-[2.5rem] border shadow-sm overflow-hidden">

        <!-- TOP -->
        <div class="p-8 border-b flex flex-col md:flex-row justify-between items-center gap-6">

          <div class="flex items-center gap-4">
            <div class="w-14 h-14 bg-slate-50 rounded-2xl flex items-center justify-center">
              <i class="fa fa-graduation-cap text-xl"></i>
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
              <p class="text-[9px] text-slate-400 uppercase">Total Score</p>
              <p class="text-2xl font-black">
                {{ studentMeta.total }}
                <span class="text-slate-300 text-sm">/{{ studentMeta.max }}</span>
              </p>
            </div>

            <div class="text-center">
              <p class="text-[9px] text-slate-400 uppercase"> Total Percentage %</p>
              <p class="text-2xl font-black text-indigo-600">
                {{ studentMeta.percentage }}%
              </p>
            </div>

          </div>
        </div>

        <!-- TABLE -->
        <div class="overflow-x-auto">
          <table class="w-full text-left">

            <thead>
              <tr class="bg-slate-50">
                <th class="p-4 text-xs">Course</th>
                <th class="p-4 text-center text-xs">Grade</th>
                <th class="p-4 text-xs">Performance</th>
                <th class="p-4 text-center text-xs">Scale</th>
                <th class="p-4 text-right text-xs">Marks</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="sub in subjects" :key="sub.id" class="border-t">

                <td class="p-4 font-bold">
                  {{ sub.name }}
                </td>

                <td class="p-4 text-center">
                  <span :class="['px-3 py-1 rounded text-white text-xs', sub.color]">
                    {{ sub.grade }}
                  </span>
                </td>

                <td class="p-4 w-[200px]">
                  <div class="h-2 bg-slate-100 rounded">
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

      <!-- FOOTER NOTE -->
      <div class="bg-indigo-50 rounded-2xl p-6 border flex gap-4">
        <i class="fa fa-info-circle text-indigo-600"></i>
        <p class="text-xs">
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