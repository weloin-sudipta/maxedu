<template>
  <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans text-slate-900">
    <div class="max-w-[1440px] mx-auto space-y-6">

      <HeroHeader title="Assignments" subtitle="Manage coursework and submissions" icon="fa fa-graduation-cap">
        <div class="hidden md:flex flex-col items-end mr-4">
          <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Completion Rate</span>
          <span class="text-sm font-black text-indigo-600">{{ completionRate }}% Weekly</span>
        </div>
      </HeroHeader>

      <div class="flex items-center gap-2 overflow-x-auto no-scrollbar pb-2">
        <button v-for="tab in ['Active', 'Submitted', 'Overdue', 'Evaluated']" :key="tab" @click="activeTab = tab"
          :class="[
            activeTab === tab
              ? 'bg-slate-900 text-white shadow-xl shadow-slate-200'
              : 'bg-white text-slate-500 border-slate-200 hover:bg-slate-50',
            'px-8 py-3 rounded-2xl text-xs font-black uppercase tracking-widest transition-all border whitespace-nowrap'
          ]">
          {{ tab }}
          <span v-if="getTabCount(tab) > 0" class="ml-2 px-2 py-0.5 rounded-full text-[9px]"
            :class="activeTab === tab ? 'bg-white/20' : 'bg-slate-100'">{{ getTabCount(tab) }}</span>
        </button>
      </div>

      <div v-if="loading" class="text-center py-20">
        <i class="fa fa-spinner fa-spin text-indigo-400 text-3xl"></i>
        <p class="text-xs text-slate-400 mt-3 font-bold uppercase">Loading assignments...</p>
      </div>

      <div v-else class="grid grid-cols-1 gap-4">
        <div v-for="task in filteredAssignments" :key="task.name"
          class="group bg-white rounded-[2rem] p-6 border border-slate-200/60 shadow-sm hover:border-indigo-300 transition-all flex flex-col lg:flex-row lg:items-center gap-6">

          <div class="flex items-center gap-5 lg:w-1/3">
            <div
              :class="['w-14 h-14 rounded-2xl flex items-center justify-center text-xl shrink-0 shadow-sm', getStatusColor(task.status)]">
              <i :class="['fa', getSubjectIcon(task.course_name)]"></i>
            </div>
            <div>
              <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">{{ task.course_name || task.course }}</p>
              <h3
                class="text-lg font-black text-slate-800 tracking-tight group-hover:text-indigo-600 transition-colors">
                {{ task.title }}</h3>
            </div>
          </div>

          <div class="flex flex-1 items-center gap-8">
            <div class="flex flex-col">
              <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Due Date</span>
              <div class="flex items-center gap-2">
                <i class="fa fa-clock-o text-red-400 text-xs"></i>
                <span class="text-xs font-bold text-slate-600">{{ formatDate(task.due_date) }}</span>
              </div>
            </div>

            <div class="hidden md:flex flex-col flex-1 max-w-[200px]">
              <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Estimated Effort</span>
              <div class="w-full bg-slate-50 h-1.5 rounded-full overflow-hidden">
                <div class="bg-indigo-400 h-full" :style="{ width: (task.difficulty || 50) + '%' }"></div>
              </div>
            </div>
          </div>

          <div class="flex items-center gap-3 lg:justify-end">
            <a v-if="task.assignment_file" :href="task.assignment_file" download class="btn-icon h-11 w-11">
              <i class="fa fa-download"></i>
            </a>
            <button v-if="task.status === 'Active'" @click="handleSubmit(task)"
              class="px-6 py-2.5 bg-indigo-600 text-white rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-900 transition-all">
              Submit Task
            </button>
            <span v-else-if="task.status === 'Evaluated'" class="px-4 py-2 bg-green-50 text-green-600 rounded-xl text-[10px] font-black uppercase">
              Score: {{ task.evaluated_score || '--' }}
            </span>
            <span v-else
              class="px-6 py-2.5 bg-slate-100 text-slate-400 rounded-xl text-[10px] font-black uppercase tracking-widest cursor-default">
              {{ task.status }}
            </span>
          </div>
        </div>

        <div v-if="filteredAssignments.length === 0"
          class="bg-white rounded-[2.5rem] p-20 border border-dashed border-slate-200 text-center">
          <i class="fa fa-check-circle text-green-200 text-5xl mb-4"></i>
          <p class="text-sm font-black text-slate-400 uppercase tracking-widest">All caught up! No {{
            activeTab.toLowerCase() }} tasks.</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import HeroHeader from '~/components/ui/HeroHeader.vue'
import { useAssignments } from '~/composable/useAssignments'

import {useAdmitCard} from '~/composable/useAdmitCard'

const {fetchAdmit} = useAdmitCard()

const config = useRuntimeConfig()
useSeoMeta({
    title: `Assignments - ${config.public.appName}`,
})

const { assignments, loading, fetchAssignments, submitAssignment } = useAssignments()

const activeTab = ref('Active');

onMounted(() => {
  fetchAssignments(),
  fetchAdmit()
})

const filteredAssignments = computed(() => {
  return assignments.value.filter(task => task.status === activeTab.value);
});

const getTabCount = (tab) => {
  return assignments.value.filter(t => t.status === tab).length
}

const completionRate = computed(() => {
  const total = assignments.value.length
  if (total === 0) return 0
  const done = assignments.value.filter(a => a.status === 'Submitted' || a.status === 'Evaluated').length
  return Math.round((done / total) * 100)
})

const handleSubmit = async (task) => {
  if (confirm(`Submit "${task.title}"?`)) {
    const res = await submitAssignment(task.name)
    if (res?.status === 'success') {
      task.status = 'Submitted'
      alert('Assignment submitted successfully!')
    } else {
      alert('Failed to submit: ' + (res?.error || 'Unknown error'))
    }
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '--'
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const getStatusColor = (status) => {
  const map = {
    Active: 'bg-blue-50 text-blue-500',
    Submitted: 'bg-green-50 text-green-500',
    Overdue: 'bg-red-50 text-red-500',
    Evaluated: 'bg-purple-50 text-purple-500',
  }
  return map[status] || 'bg-slate-50 text-slate-500'
}

const getSubjectIcon = (name) => {
  if (!name) return 'fa-book'
  const n = name.toLowerCase()
  if (n.includes('math')) return 'fa-calculator'
  if (n.includes('physic')) return 'fa-bolt'
  if (n.includes('chem')) return 'fa-flask'
  if (n.includes('bio')) return 'fa-leaf'
  if (n.includes('english') || n.includes('liter')) return 'fa-pencil'
  if (n.includes('history')) return 'fa-university'
  if (n.includes('computer') || n.includes('science')) return 'fa-laptop'
  return 'fa-book'
}
</script>

<style scoped>
.btn-primary {
  @apply px-8 py-3 bg-indigo-600 text-white rounded-2xl text-[10px] font-black uppercase tracking-[0.2em] shadow-xl shadow-indigo-100 hover:bg-indigo-700 transition-all;
}

.btn-icon {
  @apply flex items-center justify-center bg-white border border-slate-200 text-slate-400 rounded-2xl hover:text-indigo-600 transition-all shadow-sm;
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>
