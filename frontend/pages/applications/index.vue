<template>
  <main class="flex-1 overflow-y-auto p-6 lg:p-10 custom-scrollbar bg-[#f8fafc]">

    <!-- Header -->
    <div class="relative bg-white rounded-[2.5rem] p-8 lg:p-10 shadow-md mb-10 border border-slate-100">
      <div class="flex flex-col lg:flex-row justify-between items-center gap-6">
        <div class="max-w-xl text-center lg:text-left">
          <span class="text-indigo-400 text-[10px] font-black uppercase tracking-[0.3em] mb-4 block">
            Request Desk
          </span>
          <h1 class="text-3xl lg:text-4xl font-black text-black leading-tight mb-2">
            Submit an
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-500">
              Application
            </span>
          </h1>
          <p class="text-slate-400 text-sm font-medium">
            Need a leave, a new resource, or an improvement? Your voice matters.
          </p>
        </div>

        <button @click="showForm = true"
          class="px-8 py-4 bg-slate-900 text-white rounded-2xl font-bold text-sm hover:scale-105 transition-all shadow-lg">
          Create New Request
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

      <!-- LEFT -->
      <div class="lg:col-span-8 space-y-6">
        <h3 class="text-lg font-black text-slate-800 flex items-center gap-2">
          <div class="w-2 h-6 bg-indigo-500 rounded-full"></div>
          Live Tracking
        </h3>

        <!-- ✅ FIXED LOOP -->
        <div v-for="app in displayedApplications" :key="app.id"
          class="bg-white rounded-[2rem] p-6 border border-slate-100 shadow-sm hover:shadow-md transition-all">

          <div class="flex justify-between items-start mb-6">
            <div>
              <span
                class="px-3 py-1 bg-indigo-50 text-indigo-600 rounded-full text-[10px] font-bold uppercase">
                {{ app.type }}
              </span>
              <h4 class="text-lg font-bold text-slate-800 mt-2">
                {{ app.subject }}
              </h4>
              <p class="text-xs text-slate-400">
                ID: #{{ app.id }} • Submitted on {{ app.date }}
              </p>
            </div>

            <div :class="statusColor(app.status)"
              class="px-4 py-2 rounded-xl text-xs font-black uppercase">
              {{ app.status }}
            </div>
          </div>

          <!-- ✅ WORKFLOW TIMELINE -->
          <div class="relative flex justify-between items-center mt-6">
            <div class="absolute h-1 bg-slate-100 w-full top-1/2 -translate-y-1/2 z-0"></div>

            <div v-for="(step, index) in app.workflow" :key="index"
              class="relative z-10 flex flex-col items-center text-xs">

              <div
                :class="[
                  'w-10 h-10 flex items-center justify-center rounded-full',
                  step.state === 'approved' ? 'bg-green-500 text-white' :
                  step.state === 'pending' ? 'bg-amber-400 text-white' :
                  'bg-slate-200 text-slate-500'
                ]">
                <i :class="step.icon"></i>
              </div>

              <span class="mt-2 text-slate-500">{{ step.role }}</span>
            </div>
          </div>
        </div>

        <!-- ✅ READ MORE BUTTON OUTSIDE LOOP -->
        <div v-if="visibleLimit < myApplications.length" class="flex justify-center pt-4">
          <button @click="loadMore"
            class="group flex items-center gap-3 px-10 py-4 bg-white border-2 border-slate-100 text-slate-600 rounded-2xl font-bold text-sm hover:border-indigo-500 hover:text-indigo-600 transition-all shadow-sm">
            <span>Load More</span>
            <i class="fa fa-chevron-down text-[10px] group-hover:translate-y-1 transition-transform"></i>
          </button>
        </div>

      </div>

      <!-- RIGHT -->
      <div class="lg:col-span-4 space-y-8">
        <div class="bg-gradient-to-br from-slate-900 to-slate-800 rounded-[2rem] p-8 text-white">
          <h4 class="text-xl text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-500 font-black mb-4">
            Request Policy
          </h4>

          <ul class="space-y-4 text-slate-300 text-sm">
            <li class="flex gap-3">
              <i class="fa fa-check-circle text-indigo-400 mt-1"></i>
              <span>Leave requests must be submitted 24 hours in advance.</span>
            </li>
            <li class="flex gap-3">
              <i class="fa fa-check-circle text-indigo-400 mt-1"></i>
              <span>Improvement requests require at least 5 student signatures.</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <ApplicationsNewRequestModal v-model="showForm" />
  </main>
</template>

<script setup>
import { ref, computed } from 'vue'

const showForm = ref(false)
const visibleLimit = ref(5)

const myApplications = ref([
  {
    id: 'REQ-8821',
    type: 'Leave Application',
    subject: 'Sick Leave for 2 Days',
    date: 'Mar 18, 2026',
    status: 'In Progress',
    workflow: [
      { role: 'Student', icon: 'fa fa-user', state: 'approved' },
      { role: 'Class Teacher', icon: 'fa fa-user-tie', state: 'approved' },
      { role: 'HOD', icon: 'fa fa-building', state: 'pending' },
      { role: 'Principal', icon: 'fa fa-award', state: 'waiting' }
    ]
  },
  {
    id: 'REQ-7712',
    type: 'Improvement',
    subject: 'Extra Python Lab Sessions',
    date: 'Mar 15, 2026',
    status: 'Approved',
    workflow: [
      { role: 'Student', icon: 'fa fa-user', state: 'approved' },
      { role: 'Class Teacher', icon: 'fa fa-user-tie', state: 'approved' },
      { role: 'HOD', icon: 'fa fa-building', state: 'approved' },
      { role: 'Principal', icon: 'fa fa-award', state: 'approved' }
    ]
  }

])

const displayedApplications = computed(() => {
  return myApplications.value.slice(0, visibleLimit.value)
})

const loadMore = () => {
  visibleLimit.value += 5
}

const statusColor = (status) => {
  if (status === 'Approved') return 'bg-green-100 text-green-600'
  if (status === 'In Progress') return 'bg-amber-100 text-amber-600'
  return 'bg-slate-100 text-slate-500'
}
</script>