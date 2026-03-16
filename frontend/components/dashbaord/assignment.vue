<template>
  <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">

    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h3 class="text-xs font-black uppercase tracking-wide text-slate-400">Assignments</h3>
      <NuxtLink to="/academics/assignments" class="text-indigo-500 text-xs font-bold hover:underline">
        View All
      </NuxtLink>
    </div>

    <!-- Assignment List -->
    <div class="space-y-4">
      <div
        v-for="assignment in assignments"
        :key="assignment.name"
        class="flex justify-between items-center p-4 bg-slate-50 rounded-xl border border-slate-100"
      >

        <!-- Info Section -->
        <div class="flex-1">
          <p class="text-sm font-bold text-slate-800">{{ assignment.title }}</p>
          <p class="text-[10px] text-slate-400 mt-1">
            Topic: {{ assignment.topic_name || 'N/A' }}
          </p>
          <p class="text-[10px] text-slate-400 mt-0.5">
            Course: {{ assignment.course_name || assignment.course || 'N/A' }}
          </p>
          <p class="text-[10px] text-slate-400 mt-0.5">
            Due: {{ formatDate(assignment.due_date) }}
          </p>
        </div>

        <!-- Status Badge -->
        <div>
          <span 
            class="px-2 py-1 text-[10px] font-bold rounded-lg uppercase"
            :class="getStatusBadgeClass(assignment.status)"
          >
            {{ assignment.status || 'Pending' }}
          </span>
        </div>

      </div>

      <div v-if="assignments.length === 0" class="text-center text-sm text-slate-400 py-6">
        No upcoming assignments
      </div>
    </div>

  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  assignments: {
    type: Array,
    default: () => []
  }
})

// Format ISO date string to readable format
const formatDate = (dateStr) => {
  if (!dateStr) return '--'
  const dateObj = new Date(dateStr)
  return dateObj.toLocaleDateString('default', { day: '2-digit', month: 'short', year: 'numeric' })
}

// Status badge classes
const getStatusBadgeClass = (status) => {
  switch ((status || '').toLowerCase()) {
    case 'submitted': return 'bg-green-100 text-green-600'
    case 'active': return 'bg-yellow-100 text-yellow-600'
    case 'pending': return 'bg-slate-100 text-slate-600'
    default: return 'bg-slate-100 text-slate-600'
  }
}
</script>

<style scoped>
div.flex:hover {
  transform: scale(1.01);
  transition: transform 0.2s ease;
}
</style>