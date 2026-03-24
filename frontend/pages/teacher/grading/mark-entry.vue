<template>
  <div class="p-6 lg:p-10 max-w-7xl mx-auto custom-scrollbar animate-in fade-in slide-in-from-bottom-4 duration-500">
    <HeroHeader title="Mark Entry" subtitle="Speed Grader" icon="fa fa-calculator">
      <div class="flex gap-2">
        <select class="bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-200 px-4 py-2 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-800 outline-none">
          <option>Mid-Term Exam (CS-101)</option>
          <option>Final Exam (CS-201)</option>
        </select>
        <button class="bg-emerald-600 dark:bg-emerald-500 text-white px-6 py-2 rounded-xl text-xs font-black uppercase tracking-widest hover:bg-emerald-700 dark:hover:bg-emerald-600 transition-colors shadow-lg shadow-emerald-200 dark:shadow-none"><i class="fa fa-save"></i> Save Marks</button>
      </div>
    </HeroHeader>

    <div v-if="loading" class="mt-8">
      <UiSkeleton height="h-[600px]" class="rounded-[2.5rem]" />
    </div>

    <div v-else class="mt-8 bg-white dark:bg-slate-900 rounded-[2.5rem] border border-slate-100 dark:border-slate-800 shadow-sm p-4 lg:p-8 overflow-hidden">
      <!-- Notice -->
      <div class="mb-6 flex items-center justify-between bg-amber-50 dark:bg-amber-900/10 p-4 rounded-2xl border border-amber-100 dark:border-amber-800/50">
        <div class="flex items-center gap-4">
          <div class="w-10 h-10 bg-white dark:bg-slate-800 rounded-xl flex items-center justify-center shadow-sm">
            <i class="fa fa-lock text-amber-500"></i>
          </div>
          <div>
            <h4 class="text-sm font-black text-slate-800 dark:text-slate-200">Deadline: Nov 15, 2026</h4>
            <p class="text-[10px] font-bold text-slate-500 dark:text-slate-400">Marks entered after the deadline require HOD approval.</p>
          </div>
        </div>
      </div>

      <!-- Mark Grid -->
      <div class="overflow-x-auto custom-scrollbar pb-4 rounded-xl">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="border-b-2 border-slate-100 dark:border-slate-800">
              <th class="p-4 text-[10px] font-black uppercase tracking-widest text-slate-400 dark:text-slate-500 bg-slate-50 dark:bg-slate-800/50 rounded-tl-xl">Roll No</th>
              <th class="p-4 text-[10px] font-black uppercase tracking-widest text-slate-400 dark:text-slate-500 bg-slate-50 dark:bg-slate-800/50">Student Name</th>
              <th class="p-4 text-[10px] font-black uppercase tracking-widest text-slate-400 dark:text-slate-500 bg-slate-50 dark:bg-slate-800/50 w-32 border-l border-slate-200 dark:border-slate-700 text-center">Theory (70)</th>
              <th class="p-4 text-[10px] font-black uppercase tracking-widest text-slate-400 dark:text-slate-500 bg-slate-50 dark:bg-slate-800/50 w-32 text-center">Practical (30)</th>
              <th class="p-4 text-[10px] font-black uppercase tracking-widest text-slate-400 dark:text-slate-500 bg-slate-50 dark:bg-slate-800/50 w-32 text-center rounded-tr-xl">Total (100)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in students" :key="student.id" class="border-b border-slate-50 dark:border-slate-800/50 hover:bg-slate-50 dark:hover:bg-slate-800/20 transition-colors group">
              <td class="p-4 text-xs font-bold text-slate-500 dark:text-slate-400">{{ student.roll }}</td>
              <td class="p-4">
                <div class="flex items-center gap-3">
                  <img :src="student.avatar" class="w-8 h-8 rounded-full bg-slate-200 dark:bg-slate-700" />
                  <span class="text-sm font-bold text-slate-800 dark:text-slate-200">{{ student.name }}</span>
                </div>
              </td>
              <td class="p-4 border-l border-slate-50 dark:border-slate-800">
                 <input type="number" v-model="student.theory" min="0" max="70" class="w-full bg-slate-100 dark:bg-slate-800 text-center text-sm font-black text-slate-800 dark:text-slate-200 p-2 rounded-lg border border-transparent focus:border-indigo-400 dark:focus:border-indigo-500 focus:bg-white dark:focus:bg-slate-900 outline-none transition-all placeholder-slate-300 dark:placeholder-slate-600" placeholder="0">
              </td>
              <td class="p-4">
                 <input type="number" v-model="student.practical" min="0" max="30" class="w-full bg-slate-100 dark:bg-slate-800 text-center text-sm font-black text-slate-800 dark:text-slate-200 p-2 rounded-lg border border-transparent focus:border-indigo-400 dark:focus:border-indigo-500 focus:bg-white dark:focus:bg-slate-900 outline-none transition-all placeholder-slate-300 dark:placeholder-slate-600" placeholder="0">
              </td>
              <td class="p-4 text-center">
                 <span class="text-lg font-black" :class="total(student) < 40 ? 'text-red-500' : 'text-slate-800 dark:text-slate-200'">{{ total(student) }}</span>
                 <span v-if="total(student) < 40" class="block text-[8px] font-black uppercase text-red-500 mt-1">Fail</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import HeroHeader from '~/components/ui/HeroHeader.vue'

const loading = ref(true)

const students = ref([
  { id: 1, name: 'Alice Smith', roll: 'CS01', avatar: 'https://i.pravatar.cc/150?u=1', theory: 55, practical: 28 },
  { id: 2, name: 'Bob Jones', roll: 'CS02', avatar: 'https://i.pravatar.cc/150?u=2', theory: 42, practical: 25 },
  { id: 3, name: 'Charlie Brown', roll: 'CS03', avatar: 'https://i.pravatar.cc/150?u=3', theory: 20, practical: 15 },
  { id: 4, name: 'Diana Prince', roll: 'CS04', avatar: 'https://i.pravatar.cc/150?u=4', theory: 68, practical: 29 },
  { id: 5, name: 'Evan Wright', roll: 'CS05', avatar: 'https://i.pravatar.cc/150?u=5', theory: '', practical: '' }
])

const total = (s) => (parseInt(s.theory) || 0) + (parseInt(s.practical) || 0)

onMounted(() => {
  setTimeout(() => loading.value = false, 500)
})
</script>
