<template>
  <div class="space-y-8 p-4 lg:p-8 bg-slate-50/50 min-h-screen">
    <div class=" mx-auto">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h2 class="text-2xl font-black text-slate-800 tracking-tight">My Book Requests</h2>
          <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">Track your active and past physical book loans</p>
        </div>
        <div class="h-12 w-12 rounded-2xl bg-white shadow-sm border border-slate-200 flex items-center justify-center text-indigo-600">
          <i class="fa fa-history"></i>
        </div>
      </div>

      <div v-if="requests.length > 0" class="space-y-6">
        <div v-for="request in requests" :key="request.id" 
             class="bg-white rounded-[2.5rem] p-8 shadow-sm border border-slate-200/60 animate-in slide-in-from-bottom-4 duration-500">
          
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-10">
            <div class="flex items-center gap-4">
              <div class="h-12 w-12 rounded-2xl bg-slate-900 text-white flex items-center justify-center shadow-lg shadow-slate-200">
                <i class="fa fa-book"></i>
              </div>
              <div>
                <h3 class="text-sm font-black text-slate-800 uppercase tracking-wide">{{ request.book_name }}</h3>
                <p class="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">Requested on {{ request.date }}</p>
              </div>
            </div>
            <div :class="['px-4 py-1.5 rounded-xl text-[9px] font-black uppercase tracking-widest border shadow-sm', statusTheme(request.status).bg]">
              {{ request.status }}
            </div>
          </div>

          <div class="relative px-2">
            <div class="absolute top-5 left-0 w-full h-[3px] bg-slate-100 rounded-full"></div>
            
            <div 
              class="absolute top-5 left-0 h-[3px] bg-indigo-500 rounded-full transition-all duration-[1500ms] ease-in-out shadow-[0_0_10px_rgba(99,102,241,0.5)]"
              :style="{ width: getProgressWidth(request.status) }"
            ></div>

            <div class="relative flex justify-between">
              <div v-for="(step, index) in steps" :key="index" class="flex flex-col items-center">
                <div 
                  :class="[
                    'w-10 h-10 rounded-2xl flex items-center justify-center border-4 transition-all duration-700 z-10',
                    isStepReached(request.status, step.key) 
                      ? 'bg-indigo-600 border-white text-white rotate-[360deg] scale-110 shadow-md' 
                      : 'bg-white border-slate-50 text-slate-300'
                  ]"
                >
                  <i :class="[step.icon, 'text-xs']"></i>
                </div>
                <span :class="[
                  'mt-4 text-[9px] font-black uppercase tracking-widest transition-colors duration-500',
                  isStepReached(request.status, step.key) ? 'text-slate-800' : 'text-slate-300'
                ]">
                  {{ step.label }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="bg-white rounded-[2.5rem] p-20 text-center border border-dashed border-slate-200">
        <i class="fa fa-folder-open text-slate-100 text-6xl mb-4"></i>
        <p class="text-xs font-black text-slate-400 uppercase tracking-widest">No active requests found</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const requests = ref([]);

// Step definitions for the tracker
const steps = [
  { key: 'Pending', label: 'Requested', icon: 'fa fa-paper-plane' },
  { key: 'Issued', label: 'Approved', icon: 'fa fa-check-shield' },
  { key: 'Handover', label: 'Ready for Collection', icon: 'fa fa-handshake-o' },
  { key: 'Completed', label: 'Returned', icon: 'fa fa-archive' }
];

const getProgressWidth = (status) => {
  const mapping = { 'Pending': '0%', 'Issued': '33.33%', 'Handover': '66.66%', 'Completed': '100%' };
  return mapping[status] || '0%';
};

const isStepReached = (currentStatus, stepKey) => {
  const order = ['Pending', 'Issued', 'Handover', 'Completed'];
  return order.indexOf(currentStatus) >= order.indexOf(stepKey);
};

const statusTheme = (status) => {
  const themes = {
    'Pending': { bg: 'bg-yellow-50 text-yellow-600 border-yellow-100' },
    'Issued': { bg: 'bg-blue-50 text-blue-600 border-blue-100' },
    'Handover': { bg: 'bg-green-50 text-green-600 border-green-100' },
    'Completed': { bg: 'bg-slate-50 text-slate-500 border-slate-100' }
  };
  return themes[status] || themes['Pending'];
};

onMounted(async () => {
  // Simulate delay to show growing animation
  setTimeout(() => {
    requests.value = [
      { id: 1, book_name: 'Mathematics 101', status: 'Pending', date: 'Mar 10, 2026' },
      { id: 2, book_name: 'Physics Fundamentals', status: 'Issued', date: 'Mar 09, 2026' },
      { id: 3, book_name: 'Chemistry Lab Guide', status: 'Handover', date: 'Mar 08, 2026' },
    ];
  }, 100);
});
</script>

<style scoped>
.rotate-360 { transform: rotate(360deg); }

/* Custom animation for cards */
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-in { animation: slideUp 0.6s ease-out forwards; }
</style>