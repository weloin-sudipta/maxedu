<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-950 transition-colors duration-300 p-4 lg:p-8 font-sans text-slate-900">
    <div class="max-w-6xl mx-auto space-y-8">

      <div v-if="loading" class="animate-pulse space-y-8">
        <div class="h-64 bg-white dark:bg-slate-900 rounded-[2.5rem] border border-slate-200 dark:border-slate-800"></div>
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div class="lg:col-span-2 h-80 bg-white dark:bg-slate-900 rounded-[2.5rem]"></div>
          <div class="h-80 bg-indigo-600/20 rounded-[2.5rem]"></div>
        </div>
      </div>

      <template v-else>
        <header class="bg-white dark:bg-slate-900 rounded-[2.5rem] shadow-sm border border-slate-200/60 dark:border-slate-800 p-6 transition-all">
          <div class="flex flex-col md:flex-row items-center gap-8">
            <div class="relative group">
              <div class="w-32 h-32 rounded-[2rem] overflow-hidden ring-4 ring-slate-50 dark:ring-slate-800 shadow-lg bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center">
                <img v-if="teacher.photo" :src="teacher.photo" class="w-full h-full object-cover" />
                <span v-else class="text-3xl font-black text-indigo-600 dark:text-indigo-400">
                  {{ teacher.name.charAt(0) }}{{ teacher.lastName.charAt(0) }}
                </span>
              </div>
              <div class="absolute -bottom-2 -right-2 bg-emerald-500 w-8 h-8 rounded-xl flex items-center justify-center text-white border-4 border-white dark:border-slate-900 shadow-md">
                <i class="fas fa-check text-[10px]"></i>
              </div>
            </div>

            <div class="flex-1 text-center md:text-left">
              <div class="space-y-1 mb-4">
                <h1 class="text-3xl font-black tracking-tight text-slate-800 dark:text-white">
                  {{ teacher.title }} {{ teacher.name }} {{ teacher.lastName }}
                </h1>
                <p class="text-indigo-600 dark:text-indigo-400 font-bold text-sm tracking-wide">
                  {{ teacher.designation }} • {{ teacher.department }}
                </p>
              </div>

              <div class="flex flex-wrap justify-center md:justify-start gap-6">
                <div class="flex flex-col">
                  <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Employee ID</span>
                  <span class="font-bold text-slate-700 dark:text-slate-200">#{{ teacher.empId }}</span>
                </div>
                <div class="w-px h-8 bg-slate-100 dark:bg-slate-800 hidden md:block"></div>
                <div class="flex flex-col">
                  <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Joining Date</span>
                  <span class="font-bold text-slate-700 dark:text-slate-200">{{ teacher.joiningDate }}</span>
                </div>
                <div class="w-px h-8 bg-slate-100 dark:bg-slate-800 hidden md:block"></div>
                <div class="flex flex-col">
                  <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Status</span>
                  <span class="text-emerald-500 font-black text-xs uppercase tracking-tighter">On Duty</span>
                </div>
              </div>
            </div>

            <div class="flex gap-2">
              <button class="p-3 rounded-2xl bg-slate-50 dark:bg-slate-800 text-slate-400 hover:text-indigo-600 transition-colors border border-slate-200 dark:border-slate-700">
                <i class="fas fa-envelope"></i>
              </button>
              <button class="px-6 py-3 bg-slate-900 dark:bg-indigo-600 text-white rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-indigo-600 transition-all shadow-lg">
                Edit Profile
              </button>
            </div>
          </div>
        </header>

        <main class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-in fade-in duration-700">
          
          <div class="lg:col-span-2 space-y-6">
            <section class="bg-white dark:bg-slate-900 rounded-[2.5rem] p-8 border border-slate-200/60 dark:border-slate-800 shadow-sm">
              <div class="flex items-center gap-3 mb-8">
                <div class="w-1.5 h-6 bg-indigo-600 dark:bg-indigo-400 rounded-full"></div>
                <h3 class="text-lg font-black text-slate-800 dark:text-white tracking-tight">Professional Credentials</h3>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div v-for="(val, label) in teacher.credentials" :key="label" class="space-y-1">
                  <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">{{ label }}</p>
                  <p class="text-sm font-bold text-slate-700 dark:text-slate-200">{{ val }}</p>
                </div>
              </div>
            </section>

            <section class="bg-white dark:bg-slate-900 rounded-[2.5rem] p-8 border border-slate-200/60 dark:border-slate-800 shadow-sm">
              <h3 class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-6">Contact Information</h3>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="p-4 bg-slate-50 dark:bg-slate-800/40 rounded-2xl border border-slate-100 dark:border-slate-800">
                  <p class="text-[9px] font-black text-indigo-500 uppercase mb-1">Work Email</p>
                  <p class="text-xs font-bold dark:text-slate-300 break-all">{{ teacher.email }}</p>
                </div>
                <div class="p-4 bg-slate-50 dark:bg-slate-800/40 rounded-2xl border border-slate-100 dark:border-slate-800">
                  <p class="text-[9px] font-black text-indigo-500 uppercase mb-1">Mobile</p>
                  <p class="text-xs font-bold dark:text-slate-300">{{ teacher.phone }}</p>
                </div>
                <div class="p-4 bg-slate-50 dark:bg-slate-800/40 rounded-2xl border border-slate-100 dark:border-slate-800">
                  <p class="text-[9px] font-black text-indigo-500 uppercase mb-1">Room No</p>
                  <p class="text-xs font-bold dark:text-slate-300">{{ teacher.roomNo }}</p>
                </div>
              </div>
            </section>
          </div>

          <div class="space-y-6">
            <div class="bg-indigo-600 dark:bg-indigo-700 rounded-[2.5rem] p-8 text-white shadow-xl shadow-indigo-100 dark:shadow-none">
              <p class="text-[10px] font-black uppercase tracking-[0.2em] opacity-60 mb-1">Weekly Workload</p>
              <h4 class="text-4xl font-black mb-6">{{ teacher.weeklyHours }}<span class="text-lg opacity-50">hrs</span></h4>
              
              <div class="space-y-4 pt-4 border-t border-white/10">
                <div class="flex justify-between items-center text-xs font-bold">
                  <span class="opacity-70">Syllabus Progress</span>
                  <span>{{ teacher.syllabusProgress }}%</span>
                </div>
                <div class="w-full bg-indigo-500 rounded-full h-1.5">
                  <div class="bg-white h-1.5 rounded-full transition-all duration-1000" :style="{ width: teacher.syllabusProgress + '%' }"></div>
                </div>
              </div>
            </div>

            <div class="bg-white dark:bg-slate-900 rounded-[2.5rem] p-8 border border-slate-200/60 dark:border-slate-800">
              <h3 class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-6">Assigned Classes</h3>
              <div class="space-y-3">
                <div v-for="cls in teacher.classes" :key="cls" class="flex items-center gap-3 p-3 rounded-xl bg-slate-50 dark:bg-slate-800/50 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 transition-colors border border-transparent hover:border-indigo-100 dark:hover:border-indigo-800 cursor-default">
                  <div class="w-8 h-8 rounded-lg bg-white dark:bg-slate-900 flex items-center justify-center text-xs font-black text-indigo-600 shadow-sm">
                    {{ cls.split(' ')[0] }}
                  </div>
                  <span class="text-xs font-bold text-slate-700 dark:text-slate-200 uppercase">{{ cls }}</span>
                </div>
              </div>
            </div>
          </div>

        </main>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const loading = ref(false)

const teacher = ref({
  title: 'Dr.',
  name: 'Sarah',
  lastName: 'Anderson',
  empId: 'TEA-2024-089',
  designation: 'Senior Faculty',
  department: 'Mathematics & Science',
  joiningDate: '12 Aug 2021',
  email: 's.anderson@academy.edu',
  phone: '+1 (555) 902-3412',
  roomNo: 'Lab 402-B',
  weeklyHours: 32,
  syllabusProgress: 78,
  photo: null, // Add URL here
  credentials: {
    'Highest Qualification': 'Ph.D. in Applied Mathematics',
    'Specialization': 'Quantum Mechanics & Algebra',
    'Experience': '12 Years Professional Teaching',
    'License No': 'STATE-EDU-99201'
  },
  classes: [
    'Grade 10 - Section A (Physics)',
    'Grade 11 - Section B (Advanced Math)',
    'Grade 12 - Section A (Calculus)',
    'Grade 9 - Section C (General Science)'
  ]
})
</script>

<style scoped>
.animate-in {
  animation: slideUp 0.6s ease-out forwards;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Custom Scrollbar for navigation if needed */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>