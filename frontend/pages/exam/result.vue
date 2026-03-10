<template>
  <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans text-slate-900">
    <div class="max-w-[1440px] mx-auto space-y-6">

      <HeroHeader 
        :title="studentMeta.student_name || 'Performance Hub'" 
        :subtitle="`${studentMeta.academic_term || 'Consolidated Result'}`" 
        icon="fa fa-pie-chart"
      >
        <button @click="openDownloadModal('Semester Result')"
          class="px-5 py-3 bg-slate-900 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-800 transition-all flex items-center gap-2">
          <i class="fa fa-file-pdf-o"></i> Result PDF
        </button>
        <button @click="openDownloadModal('Academic Certificate')"
          class="px-5 py-3 bg-indigo-600 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest shadow-lg shadow-indigo-100 hover:bg-indigo-700 transition-all flex items-center gap-2">
          <i class="fa fa-certificate"></i> Certificate
        </button>
      </HeroHeader>

      <div class="bg-white rounded-[2.5rem] border border-slate-200/60 shadow-sm overflow-hidden animate-in">
        <div class="p-8 border-b border-slate-50 flex flex-col md:flex-row justify-between items-center gap-6">
          <div class="flex items-center gap-4">
            <div class="w-14 h-14 bg-slate-50 rounded-2xl flex items-center justify-center text-slate-400 border border-slate-100">
              <i class="fa fa-graduation-cap text-xl"></i>
            </div>
            <div>
              <h2 class="text-lg font-black text-slate-800 tracking-tight">{{ studentMeta.program }}</h2>
              <p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest mt-1">
                Student ID: {{ studentMeta.student_id }} • {{ studentMeta.academic_year }}
              </p>
            </div>
          </div>
          
          <div class="flex items-center gap-8">
            <div class="text-center">
              <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-1">Total Score</p>
              <p class="text-2xl font-black text-slate-800">{{ studentMeta.totalAggregate }}<span class="text-slate-300 text-sm">/{{ studentMeta.totalMax }}</span></p>
            </div>
            <div class="w-px h-10 bg-slate-100 hidden md:block"></div>
            <div class="text-center">
              <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-1">Percentage</p>
              <p class="text-2xl font-black text-indigo-600">{{ studentMeta.avgPerc }}%</p>
            </div>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50/50">
                <th class="p-6 text-[10px] font-black text-slate-400 uppercase tracking-widest">Course & Exam Group</th>
                <th class="p-6 text-[10px] font-black text-slate-400 uppercase tracking-widest text-center">Grade</th>
                <th class="p-6 text-[10px] font-black text-slate-400 uppercase tracking-widest">Performance Visual</th>
                <th class="p-6 text-[10px] font-black text-slate-400 uppercase tracking-widest text-center">Grading Scale</th>
                <th class="p-6 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">Marks Obtained</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr v-for="sub in subjects" :key="sub.id" class="hover:bg-indigo-50/20 transition-colors group">
                <td class="p-6">
                  <p class="text-base font-black text-slate-800 capitalize group-hover:text-indigo-600 transition-colors">{{ sub.name }}</p>
                  <div class="flex items-center gap-2 mt-1">
                    <!-- <span class="text-[9px] bg-slate-100 text-slate-500 px-2 py-0.5 rounded font-bold uppercase">{{ sub.examGroup }}</span> -->
                    <span class="text-[9px] text-slate-300 font-bold">•</span>
                    <span class="text-[9px] text-slate-400 font-bold uppercase">Ref: {{ sub.id.split('-').pop() }}</span>
                  </div>
                </td>
                
                <td class="p-6 text-center">
                  <div :class="['w-10 h-10 mx-auto rounded-xl flex items-center justify-center text-sm font-black text-white shadow-sm', sub.color]">
                    {{ sub.grade }}
                  </div>
                </td>

                <td class="p-6 w-full max-w-[280px]">
                  <div class="space-y-2">
                    <div class="flex justify-between items-center">
                      <span class="text-[9px] font-black text-slate-400 uppercase">Efficiency</span>
                      <span class="text-[10px] font-black text-slate-700">{{ sub.percentage }}%</span>
                    </div>
                    <div class="h-2 bg-slate-100 rounded-full overflow-hidden">
                      <div :class="['h-full rounded-full transition-all duration-1000', sub.color]"
                        :style="{ width: sub.percentage + '%' }"></div>
                    </div>
                  </div>
                </td>

                <td class="p-6 text-center">
                  <p class="text-[10px] font-bold text-slate-500 uppercase">{{ sub.scale }}</p>
                </td>

                <td class="p-6 text-right">
                  <p class="font-black text-slate-800 text-base">{{ sub.marks }}</p>
                  <p class="text-slate-300 font-bold text-[10px] uppercase">Out of {{ sub.maxMarks }}</p>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="bg-indigo-50 rounded-[2rem] p-6 border border-indigo-100 flex items-start md:items-center gap-5">
        <div class="w-12 h-12 bg-white rounded-2xl flex items-center justify-center text-indigo-600 shadow-sm shrink-0">
          <i class="fa fa-info-circle text-xl"></i>
        </div>
        <div>
          <p class="text-[11px] font-bold text-indigo-900 uppercase tracking-widest">Official Academic Transcript Disclaimer</p>
          <p class="text-[10px] font-medium text-indigo-700/70 uppercase mt-1">
            This transcript shows results for <strong>{{ studentMeta.student_name }}</strong> as of {{ new Date().toLocaleDateString() }}. 
            Data synchronized from Assessment Plan records.
          </p>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm" @click="showModal = false"></div>
      <div class="relative bg-white w-full max-w-md rounded-[2.5rem] shadow-2xl overflow-hidden animate-modal">
        <div class="p-8 bg-indigo-600 text-white text-center">
          <div class="w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <i class="fa fa-cloud-download text-2xl"></i>
          </div>
          <h3 class="text-xl font-black uppercase tracking-tight">Export Data</h3>
          <p class="text-[10px] font-bold opacity-80 uppercase tracking-widest mt-1">{{ downloadType }}</p>
        </div>
        <form @submit.prevent="handleDownload" class="p-8 space-y-4">
          <button type="submit" class="w-full py-4 bg-indigo-600 text-white rounded-2xl text-[11px] font-black uppercase tracking-[0.2em] shadow-lg hover:bg-indigo-700 transition-all">
            Confirm & Download
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import HeroHeader from '~/components/ui/HeroHeader.vue'
import { useExamResults } from '~/composable/useExaminations';

const config = useRuntimeConfig()
useSeoMeta({
    title: `Exam Results - ${config.public.appName}`,
})

const showModal = ref(false);
const downloadType = ref('');
const subjects = ref([]);
const studentMeta = ref({
  student_name: '',
  academic_term: '',
  academic_year: '',
  program: '',
  student_id: '',
  totalAggregate: 0,
  totalMax: 0,
  avgPerc: 0
});

// Logic to color grades based on your API (A, B, C etc)
const getColorByGrade = (grade) => {
  const g = grade?.toUpperCase();
  if (['A', 'A+', 'O'].includes(g)) return 'bg-emerald-500'; // Success
  if (['B', 'B+'].includes(g)) return 'bg-indigo-500';      // Good
  if (['C', 'C+'].includes(g)) return 'bg-amber-500';       // Average
  if (['D', 'P'].includes(g)) return 'bg-orange-500';       // Pass
  return 'bg-rose-500';                                     // Fail/Low
};

const openDownloadModal = (type) => {
  downloadType.value = type;
  showModal.value = true;
};

const handleDownload = () => {
  showModal.value = false;
};

onMounted(async () => {
  try {
    const result = await useExamResults();
    
    if (result && result.length > 0) {
      const first = result[0];
      
      // Calculate Aggregates
      let totalObtained = 0;
      let totalPossible = 0;

      subjects.value = result.map((item, index) => {
        const perc = (item.total_score / item.maximum_score) * 100;
        totalObtained += item.total_score;
        totalPossible += item.maximum_score;

        return {
          id: item.name, 
          examGroup: item.assessment_group, // "12 class exam"
          name: item.course,                // "Biology/Physics"
          grade: item.grade || 'N/A',
          marks: item.total_score,
          maxMarks: item.maximum_score,
          percentage: Math.round(perc),
          scale: item.grading_scale,
          color: getColorByGrade(item.grade)
        };
      });

      studentMeta.value = {
        student_name: first.student_name,
        academic_term: first.academic_term,
        academic_year: first.academic_year,
        program: first.program,
        student_id: first.student,
        totalAggregate: totalObtained,
        totalMax: totalPossible,
        avgPerc: Math.round((totalObtained / totalPossible) * 100)
      };
    }
  } catch (error) {
    console.error("Error fetching Exam Results:", error);
  }
});
</script>

<style scoped>
.animate-in {
  animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes modalEntry {
  from { opacity: 0; transform: scale(0.9) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
.animate-modal {
  animation: modalEntry 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
</style>