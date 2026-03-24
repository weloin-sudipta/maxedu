<template>
  <div class="bg-white rounded-[2rem] border border-slate-100 shadow-sm p-6 flex flex-col gap-5">

    <!-- HEADER -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-gradient-to-br from-amber-500 to-amber-400 rounded-[0.85rem] flex items-center justify-center text-white text-sm shadow-lg shadow-amber-200">
          <i class="fa fa-pencil-square-o"></i>
        </div>
        <div>
          <h6 class="text-sm font-black text-slate-800 leading-tight tracking-tight">Assignments</h6>
          <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{{ assignments.length }} tasks</span>
        </div>
      </div>
      <NuxtLink to="/academics/assignments"
        class="text-[10px] font-black text-indigo-600 uppercase tracking-widest bg-indigo-50 hover:bg-indigo-100 transition-colors px-3 py-1.5 rounded-full flex items-center gap-1.5">
        View all <i class="fa fa-arrow-right text-[9px]"></i>
      </NuxtLink>
    </div>

    <!-- LIST -->
    <div v-if="assignments && assignments.length > 0" class="flex flex-col">
      <div v-for="(assignment, index) in assignments" :key="assignment.name"
        class="flex items-start gap-3 py-3 group cursor-pointer">

        <!-- DOT + LINE -->
        <div class="flex flex-col items-center flex-shrink-0 w-4 pt-1">
          <div class="relative w-3.5 h-3.5 flex-shrink-0">
            <div class="absolute inset-0 rounded-full border-2 border-slate-200"></div>
            <div class="absolute inset-[3px] rounded-full" :class="getDotColor(assignment.status)"></div>
          </div>
          <div v-if="index < assignments.length - 1"
            class="w-px flex-1 min-h-[20px] mt-1 bg-gradient-to-b from-slate-200 to-transparent"></div>
        </div>

        <!-- CONTENT -->
        <div class="flex-1 min-w-0">
          <p class="text-[13px] font-black text-slate-800 group-hover:text-indigo-600 transition-colors truncate leading-tight mb-0.5">
            {{ assignment.title }}
          </p>
          <p class="text-[11px] text-slate-400 leading-relaxed">
            {{ assignment.course_name || assignment.course || 'N/A' }}
            <span v-if="assignment.topic_name"> · {{ assignment.topic_name }}</span>
          </p>
          <p class="text-[10px] text-slate-400 mt-0.5">
            Due: <span class="font-bold text-slate-500">{{ formatDate(assignment.due_date) }}</span>
          </p>
        </div>

        <!-- STATUS BADGE -->
        <span class="text-[9px] font-black uppercase tracking-widest px-2 py-1 rounded-full flex-shrink-0"
          :class="getStatusBadgeClass(assignment.status)">
          {{ assignment.status || 'Pending' }}
        </span>

      </div>
    </div>

    <!-- EMPTY STATE -->
    <div v-else class="flex flex-col items-center gap-2 py-8 text-slate-300">
      <i class="fa fa-check-circle-o text-2xl"></i>
      <p class="text-[10px] font-black uppercase tracking-widest">No upcoming assignments</p>
    </div>

  </div>
</template>

<script setup>
const props = defineProps({
  assignments: {
    type: Array,
    default: () => []
  }
})

const formatDate = (dateStr) => {
  if (!dateStr) return '--'
  return new Date(dateStr).toLocaleDateString('default', { day: '2-digit', month: 'short', year: 'numeric' })
}

const getDotColor = (status) => {
  switch ((status || '').toLowerCase()) {
    case 'submitted': return 'bg-green-500'
    case 'active':    return 'bg-amber-500'
    case 'pending':   return 'bg-slate-400'
    default:          return 'bg-slate-400'
  }
}

const getStatusBadgeClass = (status) => {
  switch ((status || '').toLowerCase()) {
    case 'submitted': return 'bg-green-50 text-green-600'
    case 'active':    return 'bg-amber-50 text-amber-600'
    case 'pending':   return 'bg-slate-100 text-slate-500'
    default:          return 'bg-slate-100 text-slate-500'
  }
}
</script>