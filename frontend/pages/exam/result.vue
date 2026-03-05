<template>
  <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans text-slate-900">
    <div class="max-w-[1440px] mx-auto space-y-6">

      <HeroHeader title="Performance Hub" subtitle="Consolidated Result Matrix • 2025-26" icon="fa fa-pie-chart">
        <button @click="openDownloadModal('Semester Result')"
          class="px-5 py-3 bg-slate-900 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-800 transition-all flex items-center gap-2">
          <i class="fa fa-file-pdf-o"></i> Result
        </button>
        <button @click="openDownloadModal('Academic Certificate')"
          class="px-5 py-3 bg-indigo-600 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest shadow-lg shadow-indigo-100 hover:bg-indigo-700 transition-all flex items-center gap-2">
          <i class="fa fa-certificate"></i> Certificate
        </button>
        <button @click="openDownloadModal('Previous Records')"
          class="px-5 py-3 bg-white text-slate-600 border border-slate-200 rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-50 transition-all flex items-center gap-2">
          <i class="fa fa-history"></i> Archives
        </button>
      </HeroHeader>

      <div class="bg-white rounded-[2.5rem] border border-slate-200/60 shadow-sm overflow-hidden">
        <div class="p-8 border-b border-slate-50 flex flex-col md:flex-row justify-between items-center gap-4">
          <h2 class="text-sm font-black text-slate-800 uppercase tracking-widest">Semester IV Summary</h2>
          <div class="flex items-center gap-6">
            <div class="text-center">
              <p class="text-[9px] font-black text-slate-400 uppercase">SGPA</p>
              <p class="text-xl font-black text-indigo-600">8.92</p>
            </div>
            <div class="text-center">
              <p class="text-[9px] font-black text-slate-400 uppercase">Status</p>
              <p class="text-xl font-black text-emerald-500">PASS</p>
            </div>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50/50">
                <th class="p-6 text-[10px] font-black text-slate-400 uppercase tracking-widest">Subject Details</th>
                <th class="p-6 text-[10px] font-black text-slate-400 uppercase tracking-widest">Grade</th>
                <th class="p-6 text-[10px] font-black text-slate-400 uppercase tracking-widest">Performance Scale</th>
                <th class="p-6 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">Total Marks
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr v-for="sub in subjects" :key="sub.id" class="hover:bg-slate-50/50 transition-colors">
                <td class="p-6">
                  <p class="text-sm font-black text-slate-800">{{ sub.name }}</p>
                  <p class="text-[10px] text-slate-400 font-bold uppercase">{{ sub.code }}</p>
                </td>
                <td class="p-6">
                  <span :class="['px-3 py-1 rounded-lg text-[10px] font-black text-white shadow-sm', sub.color]">
                    {{ sub.grade }}
                  </span>
                </td>
                <td class="p-6 w-full max-w-[300px]">
                  <div class="flex items-center gap-4">
                    <div class="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                      <div :class="['h-full rounded-full transition-all duration-1000', sub.barColor]"
                        :style="{ width: sub.percentage + '%' }"></div>
                    </div>
                    <span class="text-[10px] font-black text-slate-600">{{ sub.percentage }}%</span>
                  </div>
                </td>
                <td class="p-6 text-right font-black text-slate-800 text-sm">
                  {{ sub.marks }}<span class="text-slate-300 font-bold text-[10px]">/100</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="bg-emerald-50 rounded-[2rem] p-6 border border-emerald-100 flex items-center gap-4">
        <div class="w-10 h-10 bg-emerald-500 rounded-xl flex items-center justify-center text-white">
          <i class="fa fa-info"></i>
        </div>
        <p class="text-[11px] font-bold text-emerald-800 uppercase tracking-wide">
          Note: This is a computer-generated preview. For official purposes, please download the signed digital
          certificate using the download center above.
        </p>
      </div>
    </div>

    <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm" @click="showModal = false"></div>

      <div class="relative bg-white w-full max-w-md rounded-[2.5rem] shadow-2xl overflow-hidden animate-modal">
        <div class="p-8 bg-indigo-600 text-white text-center">
          <div class="w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <i class="fa fa-lock text-2xl"></i>
          </div>
          <h3 class="text-xl font-black uppercase tracking-tight">Verify Identity</h3>
          <p class="text-[10px] font-bold opacity-80 uppercase tracking-widest mt-1">Downloading: {{ downloadType }}</p>
        </div>

        <form @submit.prevent="handleDownload" class="p-8 space-y-4">
          <div>
            <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Student Roll No.</label>
            <input type="text" v-model="form.rollNo" placeholder="e.g. 2024-UI-9912" required
              class="w-full mt-1 bg-slate-50 border border-slate-100 rounded-2xl px-5 py-3 text-xs font-bold outline-none focus:ring-4 focus:ring-indigo-500/10 transition-all" />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Semester</label>
              <select v-model="form.semester"
                class="w-full mt-1 bg-slate-50 border border-slate-100 rounded-2xl px-5 py-3 text-xs font-bold outline-none focus:ring-4 focus:ring-indigo-500/10">
                <option v-for="n in 8" :key="n" :value="n">Sem {{ n }}</option>
              </select>
            </div>
            <div>
              <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Academic Year</label>
              <select v-model="form.year"
                class="w-full mt-1 bg-slate-50 border border-slate-100 rounded-2xl px-5 py-3 text-xs font-bold outline-none focus:ring-4 focus:ring-indigo-500/10">
                <option>2023-24</option>
                <option>2024-25</option>
                <option>2025-26</option>
              </select>
            </div>
          </div>

          <div>
            <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Course Program</label>
            <input type="text" v-model="form.course" placeholder="e.g. B.Sc Design" required
              class="w-full mt-1 bg-slate-50 border border-slate-100 rounded-2xl px-5 py-3 text-xs font-bold outline-none focus:ring-4 focus:ring-indigo-500/10" />
          </div>

          <button type="submit"
            class="w-full py-4 bg-indigo-600 text-white rounded-2xl text-[11px] font-black uppercase tracking-[0.2em] shadow-lg shadow-indigo-100 hover:bg-indigo-700 transition-all mt-4">
            Verify & Download PDF
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import HeroHeader from '~/components/ui/HeroHeader.vue'

const config = useRuntimeConfig()
useSeoMeta({
    title: `Exam Result - ${config.public.appName}`,
    description: `Explore your academic roadmap with MaxEdu's comprehensive breakdown of subjects, chapters, and lesson details. Strategically designed to guide your learning journey and maximize exam performance.`,
    keywords: 'subjects, chapters, lessons, learning path, academic roadmap, exam preparation'
})

const showModal = ref(false);
const downloadType = ref('');

const form = ref({
  rollNo: '',
  semester: 4,
  year: '2025-26',
  course: ''
});

const subjects = ref([
  { id: 1, code: 'CS-401', name: 'UI Design Patterns', grade: 'O', marks: 98, percentage: 98, color: 'bg-rose-500', barColor: 'bg-rose-500' },
  { id: 2, code: 'CS-402', name: 'Advanced JavaScript', grade: 'A+', marks: 92, percentage: 92, color: 'bg-indigo-500', barColor: 'bg-indigo-500' },
  { id: 3, code: 'CS-403', name: 'Database Architecture', grade: 'A', marks: 85, percentage: 85, color: 'bg-emerald-500', barColor: 'bg-emerald-500' },
  { id: 4, code: 'CS-404', name: 'Cloud Infrastructure', grade: 'B+', marks: 74, percentage: 74, color: 'bg-amber-500', barColor: 'bg-amber-500' },
  { id: 5, code: 'CS-405', name: 'Technical Writing', grade: 'A+', marks: 90, percentage: 90, color: 'bg-indigo-500', barColor: 'bg-indigo-500' },
]);

const openDownloadModal = (type) => {
  downloadType.value = type;
  showModal.value = true;
};

const handleDownload = () => {
  alert(`Processing download for ${downloadType.value}...\nRoll No: ${form.value.rollNo}`);
  showModal.value = false;
};
</script>

<style scoped>
@keyframes modalEntry {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }

  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.animate-modal {
  animation: modalEntry 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
</style>