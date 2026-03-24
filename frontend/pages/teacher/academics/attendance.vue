<template>
  <div class="p-6 lg:p-10 max-w-7xl mx-auto custom-scrollbar animate-in fade-in slide-in-from-bottom-4 duration-500">
    <HeroHeader title="Attendance" subtitle="Daily Register" icon="fa fa-users">
      <div class="flex gap-2">
        <select class="bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-200 px-4 py-2 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-800 outline-none focus:ring-2 focus:ring-emerald-500">
          <option>Today: Data Structures (10:00 AM)</option>
          <option>Today: Web Technologies (01:00 PM)</option>
          <option>Yesterday: System Design</option>
        </select>
        <button class="bg-emerald-600 dark:bg-emerald-500 text-white px-6 py-2 rounded-xl text-xs font-black uppercase tracking-widest hover:bg-emerald-700 dark:hover:bg-emerald-600 transition-colors shadow-lg shadow-emerald-200 dark:shadow-none">Save Register</button>
      </div>
    </HeroHeader>

    <div v-if="loading" class="mt-8">
      <UiSkeleton height="h-[600px]" class="rounded-[2.5rem]" />
    </div>

    <div v-else class="mt-8 bg-white dark:bg-slate-900 rounded-[2.5rem] border border-slate-100 dark:border-slate-800 shadow-sm p-8">
      <!-- Quick Action Bar -->
      <div class="flex justify-between items-center mb-8 bg-emerald-50 dark:bg-emerald-900/10 p-4 rounded-2xl border border-emerald-100 dark:border-emerald-800/50">
        <div class="flex items-center gap-4">
          <div class="w-10 h-10 bg-white dark:bg-slate-800 rounded-xl flex items-center justify-center shadow-sm">
            <i class="fa fa-info-circle text-emerald-500"></i>
          </div>
          <div>
            <h4 class="text-sm font-black text-slate-800 dark:text-slate-200">Mark all present by default?</h4>
            <p class="text-[10px] font-bold text-slate-500 dark:text-slate-400">Save time by only selecting absent students.</p>
          </div>
        </div>
        <button @click="markAll('present')" class="px-6 py-2 bg-emerald-500 text-white rounded-xl text-xs font-black uppercase tracking-widest hover:bg-emerald-600 transition-colors">Mark All Present</button>
      </div>

      <!-- Students List -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="student in students" :key="student.id" class="p-4 rounded-2xl border transition-all cursor-pointer flex items-center justify-between"
             :class="student.status === 'present' ? 'bg-emerald-50 border-emerald-200 dark:bg-emerald-900/20 dark:border-emerald-800' : (student.status === 'absent' ? 'bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-800' : 'bg-slate-50 border-slate-100 dark:bg-slate-800/50 dark:border-slate-700')"
             @click="toggleStatus(student)">
          <div class="flex items-center gap-3">
             <img :src="student.avatar" class="w-12 h-12 rounded-xl bg-slate-200 dark:bg-slate-700 object-cover" />
             <div>
               <p class="text-sm font-bold text-slate-800 dark:text-slate-200">{{ student.name }}</p>
               <p class="text-[10px] text-slate-400 dark:text-slate-500 font-bold tracking-widest">ID: {{ student.roll }}</p>
             </div>
          </div>
          <div class="w-8 h-8 rounded-full flex items-center justify-center transition-colors shadow-sm"
               :class="student.status === 'present' ? 'bg-emerald-500 text-white' : (student.status === 'absent' ? 'bg-red-500 text-white' : 'bg-white dark:bg-slate-800 text-slate-300 dark:text-slate-600')">
            <i class="fa text-xs" :class="student.status === 'present' ? 'fa-check' : (student.status === 'absent' ? 'fa-times' : 'fa-minus')"></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import HeroHeader from '~/components/ui/HeroHeader.vue'
import { useToast } from '~/composable/useToast'

const loading = ref(true)
const { addToast } = useToast()

const students = ref([
  { id: 1, name: 'Alice Smith', roll: 'CS01', avatar: 'https://i.pravatar.cc/150?u=1', status: null },
  { id: 2, name: 'Bob Jones', roll: 'CS02', avatar: 'https://i.pravatar.cc/150?u=2', status: null },
  { id: 3, name: 'Charlie Brown', roll: 'CS03', avatar: 'https://i.pravatar.cc/150?u=3', status: null },
  { id: 4, name: 'Diana Prince', roll: 'CS04', avatar: 'https://i.pravatar.cc/150?u=4', status: null },
  { id: 5, name: 'Evan Wright', roll: 'CS05', avatar: 'https://i.pravatar.cc/150?u=5', status: null },
  { id: 6, name: 'Fiona Gallagher', roll: 'CS06', avatar: 'https://i.pravatar.cc/150?u=6', status: null }
])

const toggleStatus = (student) => {
  if (student.status === null || student.status === 'absent') student.status = 'present'
  else student.status = 'absent'
}

const markAll = (status) => {
  students.value.forEach(s => s.status = status)
  addToast('Success', 'All students marked as present.', 'success')
}

onMounted(() => {
  setTimeout(() => loading.value = false, 600)
})
</script>
