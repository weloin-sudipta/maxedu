<template>
  <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans text-slate-900">
    <div class="max-w-[1440px] mx-auto space-y-6">

      <HeroHeader title="Exam Roadmap" :subtitle="`Academic Session ${studentYear}`" icon="fa fa-calendar-check-o">
        <button @click="activeTab = 'confirmed'"
          :class="[activeTab === 'confirmed' ? 'bg-white shadow-md text-rose-600' : 'text-slate-400 hover:text-slate-600']"
          class="px-6 py-2.5 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all flex items-center gap-2">
          <i class="fa fa-check-circle"></i> Confirmed
        </button>
        <button @click="activeTab = 'tentative'"
          :class="[activeTab === 'tentative' ? 'bg-white shadow-md text-amber-600' : 'text-slate-400 hover:text-slate-600']"
          class="px-6 py-2.5 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all flex items-center gap-2">
          <i class="fa fa-clock-o"></i> Tentative
        </button>
      </HeroHeader>

      <div v-if="activeTab === 'confirmed'" class="space-y-6 animate-in slide-in-from-left duration-400">
        <div class="px-6 flex items-center gap-3">
          <span class="w-2 h-2 rounded-full bg-rose-500"></span>
          <h2 class="text-xs font-black text-slate-400 uppercase tracking-widest">Fixed Schedule • Hall Tickets Issued
          </h2>
        </div>

        <div v-for="exam in confirmedExams" :key="exam.id"
          class="group bg-white rounded-[2.5rem] p-2 border border-slate-200/60 shadow-sm hover:border-rose-300 transition-all flex flex-col md:flex-row items-stretch">
          <div
            class="md:w-32 bg-rose-600 rounded-[2rem] m-2 flex flex-col items-center justify-center text-white p-4 shadow-lg shadow-rose-200">
            <span class="text-[10px] font-black uppercase tracking-widest opacity-80">{{ exam.month }}</span>
            <span class="text-4xl font-black my-1">{{ exam.day }}</span>
            <span class="text-[10px] font-black uppercase tracking-widest px-2 py-1 bg-white/20 rounded-lg">{{
              exam.dayName }}</span>
          </div>

          <div class="flex-1 p-6 flex flex-col md:flex-row items-center gap-6">
            <div class="flex-1">
              <h3 class="text-xl font-black text-slate-800 tracking-tight text-center md:text-left">{{ exam.subject }}
              </h3>
              <div class="flex flex-wrap justify-center md:justify-start gap-6 mt-3">
                <div class="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-widest">
                  <i class="fa fa-clock-o text-rose-400"></i> {{ exam.time }}
                </div>
                <div class="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-widest">
                  <i class="fa fa-map-marker text-rose-400"></i> {{ exam.room }}
                </div>
                <div class="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-widest">
                  <i class="fa fa-book text-rose-400"></i> {{ exam.course }}
                </div>
              </div>
            </div>
            <button
              class="px-6 py-3 bg-slate-900 text-white rounded-2xl text-[9px] font-black uppercase tracking-widest hover:scale-105 transition-transform shadow-lg">
              Download Admit Card
            </button>
          </div>
        </div>

        <div v-if="confirmedExams.length === 0" class="text-center py-20 text-slate-400 font-bold uppercase text-xs tracking-widest">
           No confirmed exams found.
        </div>
      </div>

      <div v-if="activeTab === 'tentative'"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-in slide-in-from-right duration-400">
        <div class="col-span-full px-6 flex items-center gap-3 mb-2">
          <span class="w-2 h-2 rounded-full bg-amber-500"></span>
          <h2 class="text-xs font-black text-slate-400 uppercase tracking-widest">Expected Windows • Subject to Final Approval</h2>
        </div>

        <div v-for="exam in tentativeExams" :key="exam.id"
          class="bg-white/60 backdrop-blur-md rounded-[2.5rem] p-8 border border-amber-100 shadow-sm relative overflow-hidden group hover:bg-white transition-all">
          <div class="relative z-10">
            <div class="flex justify-between items-start mb-6">
              <div class="w-12 h-12 bg-amber-100 text-amber-600 rounded-2xl flex items-center justify-center text-xl">
                <i class="fa fa-hourglass-half"></i>
              </div>
              <span class="px-3 py-1 bg-amber-50 text-amber-600 text-[8px] font-black uppercase rounded-full border border-amber-100">Draft Schedule</span>
            </div>
            <h3 class="text-lg font-black text-slate-800 tracking-tight mb-2">{{ exam.subject }}</h3>
            <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-6">Expected: {{ exam.expectedWeek }}</p>
          </div>
          <i class="fa fa-calendar-o absolute -right-4 -bottom-4 text-7xl opacity-5"></i>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import HeroHeader from '~/components/ui/HeroHeader.vue'
import { useExams } from '~/composable/useExaminations';

const config = useRuntimeConfig()
useSeoMeta({
    title: `Exam Schedule - ${config.public.appName}`,
})

const activeTab = ref('confirmed');
const confirmedExams = ref([]);
const studentYear = ref('2025-26');

const tentativeExams = ref([
  { id: 101, subject: 'Cloud Infrastructure', expectedWeek: '3rd Week of April', probability: 85 },
  { id: 102, subject: 'Database Management', expectedWeek: 'Last Week of April', probability: 70 }
]);

// Helper to format 24h time to 12h
const formatTime = (timeStr) => {
  if (!timeStr) return '';
  const [h, m] = timeStr.split(':');
  const hour = parseInt(h);
  const ampm = hour >= 12 ? 'PM' : 'AM';
  const displayHour = hour % 12 || 12;
  return `${displayHour}:${m} ${ampm}`;
};

onMounted(async () => {
  try {
    const response = await useExams();
    // Handling the array inside the PromiseResult
    const data = Array.isArray(response) ? response : [];

    if (data.length > 0) {
      studentYear.value = data[0].academic_year;
      
      confirmedExams.value = data.map((item, index) => {
        const dateObj = new Date(item.date);
        
        return {
          id: item.exam_id || index,
          subject: item.subject,
          course: item.course, // Added to show the specific course
          // Date Transformations
          month: dateObj.toLocaleString('default', { month: 'short' }).toUpperCase(),
          day: dateObj.getDate().toString().padStart(2, '0'),
          dayName: dateObj.toLocaleString('default', { weekday: 'long' }).toUpperCase(),
          // Time Transformation
          time: `${formatTime(item.start_time)} - ${formatTime(item.end_time)}`,
          room: item.room.replace('HTL-ROOM-', 'Room '), // Cleaning up the string
          seat: 'TBA' // Not provided in backend yet
        };
      });
    }
  } catch (error) {
    console.error("Error loading exams:", error);
  }
});
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #d9dee3; border-radius: 10px; }
@keyframes slideInLeft { from { opacity: 0; transform: translateX(-30px); } to { opacity: 1; transform: translateX(0); } }
@keyframes slideInRight { from { opacity: 0; transform: translateX(30px); } to { opacity: 1; transform: translateX(0); } }
.animate-in { animation-fill-mode: both; }
.slide-in-from-left { animation: slideInLeft 0.4s ease-out; }
.slide-in-from-right { animation: slideInRight 0.4s ease-out; }
</style>