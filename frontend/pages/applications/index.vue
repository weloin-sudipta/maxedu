<template>
  <main class="flex-1 overflow-y-auto p-6 lg:p-10 custom-scrollbar bg-[#f8fafc] dark:bg-slate-950 transition-colors">

    <!-- Header -->
    <div class="relative bg-white dark:bg-slate-900 rounded-[2.5rem] p-8 lg:p-10 shadow-md dark:shadow-none mb-10 border border-slate-100 dark:border-slate-800 transition-colors">
      <div class="flex flex-col lg:flex-row justify-between items-center gap-6">
        <div class="max-w-xl text-center lg:text-left">
          <span class="text-indigo-400 text-[10px] font-black uppercase tracking-[0.3em] mb-4 block">
            Request Desk
          </span>
          <h1 class="text-3xl lg:text-4xl font-black text-black dark:text-white leading-tight mb-2 transition-colors">
            Submit an
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-500">
              Application
            </span>
          </h1>
          <p class="text-slate-400 dark:text-slate-500 text-sm font-medium transition-colors">
            Need a leave, a new resource, or an improvement? Your voice matters.
          </p>
        </div>

        <button @click="showForm = true"
          class="px-8 py-4 bg-slate-900 dark:bg-slate-800 text-white rounded-2xl font-bold text-sm hover:scale-105 transition-all shadow-lg dark:shadow-none">
          Create New Request
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

      <!-- LEFT -->
      <div class="lg:col-span-8 space-y-6">
        <h3 class="text-lg font-black text-slate-800 dark:text-slate-100 flex items-center gap-2 transition-colors">
          <div class="w-2 h-6 bg-indigo-500 rounded-full"></div>
          Live Tracking
        </h3>

        <!-- Skeleton Loading -->
        <div v-if="loading && myApplications.length === 0" class="flex flex-col gap-6">
          <div v-for="i in 3" :key="i" class="bg-white dark:bg-slate-900 rounded-[2rem] p-6 border border-slate-100 dark:border-slate-800 shadow-sm dark:shadow-none flex flex-col gap-4 transition-colors">
              <div class="flex justify-between items-start">
                  <div class="space-y-3 w-full max-w-sm">
                      <UiSkeleton height="h-6" width="w-20" class="rounded-full" />
                      <UiSkeleton height="h-6" width="w-3/4" />
                      <UiSkeleton height="h-3" width="w-1/2" />
                  </div>
                  <UiSkeleton height="h-8" width="w-24" class="rounded-full shrink-0" />
              </div>
              <UiSkeleton height="h-16" class="mt-4 rounded-xl" />
          </div>
        </div>

        <!-- ✅ FIXED LOOP -->
        <div v-else v-for="app in displayedApplications" :key="app.id"
          class="bg-white dark:bg-slate-900 rounded-[2rem] p-6 border border-slate-100 dark:border-slate-800 shadow-sm dark:shadow-none hover:shadow-md dark:hover:shadow-none transition-all animate-in fade-in">

          <div class="flex justify-between items-start mb-6">
            <div>
              <UiStatusBadge :status="app.type" size="sm" class="mb-2" />
              <h4 class="text-lg font-bold text-slate-800 dark:text-slate-100 mt-2 transition-colors">
                {{ app.subject }}
              </h4>
              <p class="text-xs text-slate-400 dark:text-slate-500 transition-colors">
                ID: #{{ app.id }} • Submitted on {{ app.date }}
              </p>
            </div>

            <UiStatusBadge :status="app.status" size="lg" />
          </div>

          <!-- ✅ WORKFLOW TIMELINE -->
          <div class="relative flex justify-between items-center mt-6">
            <div class="absolute h-1 bg-slate-100 dark:bg-slate-800 transition-colors w-full top-1/2 -translate-y-1/2 z-0"></div>

            <div v-for="(step, index) in app.workflow" :key="index"
              class="relative z-10 flex flex-col items-center text-xs">

              <div
                :class="[
                  'w-10 h-10 flex items-center justify-center rounded-full transition-colors',
                  step.state === 'approved' ? 'bg-green-500 text-white' :
                  step.state === 'pending' ? 'bg-amber-400 text-white' :
                  'bg-slate-200 dark:bg-slate-800 text-slate-500 dark:text-slate-400'
                ]">
                <i :class="step.icon"></i>
              </div>

              <span class="mt-2 text-slate-500 dark:text-slate-400 transition-colors">{{ step.role }}</span>
            </div>
          </div>
        </div>

        <!-- ✅ READ MORE BUTTON OUTSIDE LOOP -->
        <div v-if="visibleLimit < myApplications.length" class="flex justify-center pt-4">
          <button @click="loadMore"
            class="group flex items-center gap-3 px-10 py-4 bg-white dark:bg-slate-900 border-2 border-slate-100 dark:border-slate-800 text-slate-600 dark:text-slate-300 rounded-2xl font-bold text-sm hover:border-indigo-500 dark:hover:border-indigo-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-all shadow-sm dark:shadow-none">
            <span>Load More</span>
            <i class="fa fa-chevron-down text-[10px] group-hover:translate-y-1 transition-transform"></i>
          </button>
        </div>

      </div>

      <!-- RIGHT -->
      <div class="lg:col-span-4 space-y-8">
        <div class="bg-gradient-to-br from-slate-900 to-slate-800 dark:from-slate-800 dark:to-slate-900 rounded-[2rem] p-8 text-white transition-colors">
          <h4 class="text-xl text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-500 font-black mb-4">
            Request Policy
          </h4>

          <ul class="space-y-4 text-slate-300 dark:text-slate-400 text-sm transition-colors">
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

    <ApplicationsNewRequestModal v-model="showForm" @submitted="fetchApplications" />
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { call } from '~/composable/useFrappeFetch'

const showForm = ref(false)
const visibleLimit = ref(5)
const loading = ref(false)

const myApplications = ref([])

const fetchApplications = async () => {
  loading.value = true
  try {
    const res = await call('maxedu.desk_approval.doctype.application.application.get_user_applications')
    myApplications.value = res || []
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchApplications()
})

const displayedApplications = computed(() => {
  return myApplications.value.slice(0, visibleLimit.value)
})

const loadMore = () => {
  visibleLimit.value += 5
}

const statusColor = (status) => {
  if (status === 'Approved') return 'bg-green-100 text-green-600'
  if (status === 'Pending' || status === 'In Progress') return 'bg-amber-100 text-amber-600'
  return 'bg-slate-100 text-slate-500'
}
</script>