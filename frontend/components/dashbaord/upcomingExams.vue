<template>
  <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm relative overflow-hidden group">
    
    <div class="flex items-center justify-between mb-8">
      <div>
        <h3 class="text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 mb-1">Assessment Phase</h3>
        <p class="text-xl font-black text-slate-800 tracking-tight">Upcoming Exams</p>
      </div>
      <NuxtLink to="/exam/schedule" class="w-10 h-10 rounded-full bg-rose-50 flex items-center justify-center text-rose-500 shadow-sm">
        <i class="fa fa-feather"></i>
      </NuxtLink>
    </div>

    <div class="space-y-4">
      <div v-for="(exam, index) in upcomingExams" :key="exam.subject" 
           class="relative flex group/ticket">
        
        <div class="w-20 shrink-0 flex flex-col items-center justify-center p-3 rounded-l-3xl transition-colors"
             :class="index === 0 ? 'bg-rose-600 text-white' : 'bg-slate-50 text-slate-400 group-hover/ticket:bg-slate-100'">
          <span class="text-[9px] font-black uppercase tracking-tighter opacity-80">
            {{ getMonth(exam.date) }}
          </span>
          <span class="text-xl font-black leading-none my-1">
            {{ getDay(exam.date) }}
          </span>
          <span class="text-[9px] font-black uppercase tracking-widest opacity-80">
            2026
          </span>
        </div>

        <div class="relative w-[1px] border-l-2 border-dashed transition-colors"
             :class="index === 0 ? 'border-rose-400 bg-rose-600' : 'border-slate-200 bg-slate-50'">
          <div class="absolute -top-1 -left-[5px] w-2 h-2 rounded-full bg-white"></div>
          <div class="absolute -bottom-1 -left-[5px] w-2 h-2 rounded-full bg-white"></div>
        </div>

        <div class="flex-1 p-4 rounded-r-3xl border border-l-0 transition-all flex flex-col justify-center"
             :class="index === 0 ? 'bg-rose-50/50 border-rose-100' : 'bg-white border-slate-100 group-hover/ticket:border-slate-200'">
          
          <div class="flex justify-between items-start">
            <div>
              <h4 class="text-sm font-black text-slate-800 group-hover/ticket:text-rose-600 transition-colors">
                {{ exam.subject }}
              </h4>
              <p class="text-[10px] font-bold text-slate-400 uppercase tracking-tight mt-0.5">
                {{ exam.room || 'Hall A' }} • {{ exam.time || '09:00 AM' }}
              </p>
            </div>
            
            <span v-if="index === 0" class="text-[8px] font-black bg-rose-500 text-white px-2 py-0.5 rounded uppercase tracking-tighter animate-pulse">
              In {{ exam.daysLeft || '2' }} Days
            </span>
          </div>
        </div>

        <!-- <div class="absolute right-4 top-1/2 -translate-y-1/2 opacity-0 group-hover/ticket:opacity-100 transition-all">
          <i class="fa fa-external-link text-slate-300 text-xs hover:text-rose-500"></i>
        </div> -->
      </div>
    </div>

    <button class="w-full mt-6 py-3 rounded-2xl border border-slate-100 text-[9px] font-black uppercase tracking-[0.2em] text-slate-400 hover:bg-slate-900 hover:text-white hover:border-slate-900 transition-all">
      Download Hall Ticket <i class="fa fa-download ml-2"></i>
    </button>

    <i class="fa fa-graduation-cap absolute -right-6 -bottom-6 text-8xl text-slate-50 rotate-12 group-hover:text-rose-100 transition-colors pointer-events-none"></i>
  </div>
</template>

<script setup>
const props = defineProps(['upcomingExams']);

// Mock helpers for date parsing
const getMonth = (dateStr) => dateStr.split(' ')[0].substring(0, 3);
const getDay = (dateStr) => dateStr.split(' ')[1].replace(',', '');
</script>

<style scoped>
/* Added a subtle scale effect to the active ticket */
.group\/ticket:active {
  transform: scale(0.98);
}
</style>