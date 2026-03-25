<template>
  <div class="p-6 lg:p-10 max-w-7xl mx-auto custom-scrollbar animate-in fade-in slide-in-from-bottom-4 duration-500">
    <HeroHeader title="My Students" subtitle="Student Directory" icon="fa fa-users">
      <div class="flex gap-4">
        <div class="bg-white dark:bg-slate-900 rounded-xl flex items-center px-4 border border-slate-200 dark:border-slate-800 focus-within:ring-2 focus-within:ring-indigo-500 shadow-sm transition-all h-10">
          <i class="fa fa-search text-slate-400"></i>
          <input type="text" placeholder="Search students..." class="w-48 bg-transparent border-none text-xs outline-none ml-2 text-slate-700 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500" />
        </div>
        <select class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl px-4 text-xs font-bold text-slate-700 dark:text-slate-200 outline-none h-10 shadow-sm">
          <option>All Sections</option>
          <option>CS-101 (Section A)</option>
        </select>
      </div>
    </HeroHeader>

    <div v-if="loading" class="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <UiSkeleton v-for="n in 8" :key="n" height="h-64" class="rounded-[2.5rem]" />
    </div>

    <div v-else class="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div v-for="student in students" :key="student.id" class="bg-white dark:bg-slate-900 rounded-[2.5rem] border border-slate-100 dark:border-slate-800 shadow-sm p-6 flex flex-col items-center text-center hover:shadow-xl hover:-translate-y-1 transition-all group cursor-pointer dark:hover:border-indigo-500/30">
        <div class="relative mb-4">
           <img :src="student.avatar" class="w-24 h-24 rounded-[1.5rem] bg-slate-200 dark:bg-slate-700 object-cover shadow-sm group-hover:scale-105 transition-transform" />
           <span class="absolute -bottom-2 -right-2 w-6 h-6 rounded-lg flex items-center justify-center border-2 border-white dark:border-slate-900 text-[10px]"
                 :class="student.status === 'Excellent' ? 'bg-green-500 text-white' : (student.status === 'At Risk' ? 'bg-red-500 text-white' : 'bg-slate-300 dark:bg-slate-600 text-slate-700 dark:text-slate-200')">
             <i class="fa" :class="student.status === 'Excellent' ? 'fa-star' : (student.status === 'At Risk' ? 'fa-warning' : 'fa-check')"></i>
           </span>
        </div>
        <h4 class="text-sm font-black text-slate-800 dark:text-slate-100 mb-1 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">{{ student.name }}</h4>
        <p class="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-4">Roll: {{ student.roll }}</p>

        <div class="w-full flex justify-between px-2 py-3 bg-slate-50 dark:bg-slate-800/50 rounded-2xl border border-slate-100 dark:border-slate-700/50 mb-4">
          <div>
            <span class="block text-[8px] font-black uppercase text-slate-400 dark:text-slate-500 tracking-widest">Attendance</span>
            <span class="text-xs font-black" :class="student.attendance < 75 ? 'text-red-500' : 'text-slate-800 dark:text-slate-200'">{{ student.attendance }}%</span>
          </div>
          <div class="w-px bg-slate-200 dark:bg-slate-700"></div>
          <div>
            <span class="block text-[8px] font-black uppercase text-slate-400 dark:text-slate-500 tracking-widest">Avg Grade</span>
            <span class="text-xs font-black" :class="student.grade < 60 ? 'text-red-500' : 'text-slate-800 dark:text-slate-200'">{{ student.grade }}%</span>
          </div>
        </div>

        <button class="w-full py-2.5 bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-300 rounded-xl text-[10px] font-black uppercase tracking-widest group-hover:bg-indigo-500 group-hover:text-white transition-colors">View Profile</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import HeroHeader from '~/components/ui/HeroHeader.vue'
import { fetchStudents } from '~/composable/useStudent'

const loading = ref(true)
const students = ref([])

onMounted(async () => {
  try {
    const res = await fetchStudents()
    console.log('API Data:', res)

    // ✅ handle frappe response (array OR { message: [] })
    const list = res?.message || res || []

    // ✅ map API → your UI format
    students.value = list.map((s, index) => ({
      id: s.name || index,
      name: s.student_name || `${s.first_name || ''} ${s.last_name || ''}`,
      roll: s.name || 'N/A',

      avatar: s.image
        ? s.image
        : `https://ui-avatars.com/api/?name=${encodeURIComponent(s.student_name || 'Student')}`,

      // 🔥 temporary values (until you connect real APIs)
      attendance: Math.floor(Math.random() * 40) + 60,
      grade: Math.floor(Math.random() * 40) + 60,

      status:
        (Math.random() * 100) > 75
          ? 'Excellent'
          : (Math.random() * 100) < 50
          ? 'At Risk'
          : 'Good'
    }))

  } catch (error) {
    console.error('Error: Please check the path and all things properly.', error)
  } finally {
    loading.value = false
  }
})
</script>
