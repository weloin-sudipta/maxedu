<template>
  <div class="min-h-screen bg-stone-50 font-sans relative overflow-hidden">

    <!-- Background orbs -->
    <div class="fixed top-[-100px] right-[-100px] w-[400px] h-[400px] rounded-full bg-green-500/5 blur-[80px] pointer-events-none z-0"></div>
    <div class="fixed bottom-[100px] left-[-80px] w-[300px] h-[300px] rounded-full bg-amber-500/5 blur-[80px] pointer-events-none z-0"></div>

    <div class="relative z-10 mx-auto px-5 pt-10 pb-16">

      <!-- Header -->
      <header class="flex items-center gap-3 mb-8">
        <div class="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-stone-50 font-serif text-base tracking-wide flex-shrink-0">
          {{ initials }}
        </div>
        <div class="flex-1 min-w-0">
          <h1 class="font-serif text-xl text-stone-900 leading-tight">{{ student.name }}</h1>
          <p class="text-xs text-stone-400 mt-0.5 tracking-wide">{{ student.class }} &nbsp;·&nbsp; {{ student.id }}</p>
        </div>
        <button
          @click="showForm = true"
          class="flex items-center gap-1.5 px-4 py-2 bg-stone-900 text-stone-50 rounded-xl text-xs font-medium hover:opacity-80 transition-opacity whitespace-nowrap"
        >
          <span class="text-base leading-none">+</span>
          Apply for Leave
        </button>
      </header>

      <!-- Stat cards -->
      <div class="grid grid-cols-4 gap-2 mb-7">
        <div
          v-for="stat in stats" :key="stat.key"
          @click="filterBy(stat.key)"
          class="bg-white border rounded-2xl p-3.5 cursor-pointer transition-all hover:-translate-y-0.5"
          :class="activeFilter === stat.key ? 'border-stone-900' : 'border-stone-200'"
        >
          <div class="font-serif text-2xl leading-none mb-1" :class="statNumColor(stat.key)">{{ stat.count }}</div>
          <div class="text-[10px] text-stone-400 uppercase tracking-widest mb-2">{{ stat.label }}</div>
          <div class="h-0.5 bg-stone-100 rounded-full overflow-hidden">
            <div
              class="h-full rounded-full transition-all duration-500"
              :class="statBarColor(stat.key)"
              :style="{ width: stat.key === 'all' ? '100%' : (totalApps ? (stat.count / totalApps * 100) + '%' : '0%') }"
            ></div>
          </div>
        </div>
      </div>

      <!-- Section label -->
      <p class="text-[10px] text-stone-400 uppercase tracking-widest mb-3">My Applications</p>

      <!-- Card list -->
      <div class="flex flex-col gap-2.5">
        <div
          v-for="(app, index) in filteredApps" :key="app.id"
          @click="toggle(app.id)"
          class="bg-white border rounded-2xl px-5 py-4 cursor-pointer transition-all animate-fade-up"
          :class="openId === app.id ? 'border-stone-900' : 'border-stone-200 hover:border-stone-300 hover:shadow-sm'"
          :style="{ animationDelay: index * 50 + 'ms' }"
        >
          <!-- Top row -->
          <div class="flex items-center justify-between mb-3.5">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-xl flex items-center justify-center text-base flex-shrink-0" :class="typeIconBg(app.type)">
                {{ typeIcon(app.type) }}
              </div>
              <div>
                <div class="text-sm font-medium text-stone-900">{{ app.type }} Leave</div>
                <div class="text-[11px] text-stone-400 tracking-wide">{{ app.id }}</div>
              </div>
            </div>
            <div class="flex items-center gap-2.5">
              <span class="text-[11px] font-medium px-2.5 py-1 rounded-full" :class="badgeClass(app.state)">
                {{ app.state }}
              </span>
              <span
                class="text-xl text-stone-300 leading-none transition-transform duration-200 inline-block"
                :class="openId === app.id ? 'rotate-90' : ''"
              >›</span>
            </div>
          </div>

          <!-- Dates + mini tracker -->
          <div class="flex items-center justify-between gap-3">
            <div class="flex items-center gap-1.5 text-xs text-stone-500 flex-wrap">
              <span>{{ formatDate(app.from) }}</span>
              <span class="text-stone-300">→</span>
              <span>{{ formatDate(app.to) }}</span>
              <span class="bg-stone-100 text-stone-500 text-[10px] font-medium px-2 py-0.5 rounded-full ml-1">
                {{ days(app.from, app.to) }}d
              </span>
            </div>
            <div class="flex items-center flex-shrink-0">
              <template v-for="(desk, i) in DESKS" :key="desk">
                <div class="w-2 h-2 rounded-full flex-shrink-0 transition-colors" :class="miniDotClass(app.state, i)"></div>
                <div v-if="i < DESKS.length - 1" class="w-4 h-px flex-shrink-0 transition-colors" :class="isDone(app.state, i) ? 'bg-green-500' : 'bg-stone-200'"></div>
              </template>
            </div>
          </div>

          <!-- Expanded detail -->
          <transition
            enter-active-class="transition-all duration-200 ease-out"
            enter-from-class="opacity-0 -translate-y-1"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition-all duration-150 ease-in"
            leave-from-class="opacity-100 translate-y-0"
            leave-to-class="opacity-0 -translate-y-1"
          >
            <div v-if="openId === app.id" class="mt-4">
              <div class="h-px bg-stone-100 mb-4"></div>

              <div class="grid grid-cols-3 gap-2 mb-3">
                <div class="bg-stone-50 rounded-xl px-3 py-2.5">
                  <div class="text-[10px] text-stone-400 uppercase tracking-widest mb-1">From</div>
                  <div class="text-[13px] font-medium text-stone-800">{{ formatDate(app.from) }}</div>
                </div>
                <div class="bg-stone-50 rounded-xl px-3 py-2.5">
                  <div class="text-[10px] text-stone-400 uppercase tracking-widest mb-1">To</div>
                  <div class="text-[13px] font-medium text-stone-800">{{ formatDate(app.to) }}</div>
                </div>
                <div class="bg-stone-50 rounded-xl px-3 py-2.5">
                  <div class="text-[10px] text-stone-400 uppercase tracking-widest mb-1">Days</div>
                  <div class="text-[13px] font-medium text-stone-800">{{ days(app.from, app.to) }}</div>
                </div>
              </div>

              <div class="bg-stone-50 rounded-xl px-3 py-2.5 mb-4">
                <div class="text-[10px] text-stone-400 uppercase tracking-widest mb-1">Reason</div>
                <div class="text-[13px] text-stone-700">{{ app.reason }}</div>
              </div>

              <!-- Full step tracker -->
              <div class="flex items-start mb-4">
                <template v-for="(desk, i) in DESKS" :key="desk">
                  <div class="flex flex-col items-center flex-1">
                    <div
                      class="w-7 h-7 rounded-full flex items-center justify-center text-[11px] font-medium border transition-colors"
                      :class="stepCircleClass(app.state, i)"
                    >
                      <span v-if="isDone(app.state, i)">✓</span>
                      <span v-else-if="isRejectedHere(app.state, i)">✕</span>
                      <span v-else>{{ i + 1 }}</span>
                    </div>
                    <div class="text-[9px] text-stone-400 mt-1.5 text-center leading-tight uppercase tracking-wide max-w-[60px]">
                      {{ shortDesk(desk) }}
                    </div>
                  </div>
                  <div
                    v-if="i < DESKS.length - 1"
                    class="flex-1 h-px mt-3.5 transition-colors"
                    :class="isDone(app.state, i) ? 'bg-green-400' : 'bg-stone-200'"
                  ></div>
                </template>
              </div>

              <!-- Status message -->
              <div class="flex items-center gap-2 text-xs px-3.5 py-2.5 rounded-xl" :class="statusMsgClass(app.state)">
                {{ statusMessage(app.state) }}
              </div>
            </div>
          </transition>
        </div>

        <!-- Empty -->
        <div v-if="filteredApps.length === 0" class="text-center py-12 text-stone-400">
          <div class="text-3xl mb-2">📋</div>
          <p class="text-sm">No applications here</p>
        </div>
      </div>

      <!-- Bottom apply btn -->
      <button
        @click="showForm = true"
        class="w-full mt-4 py-3 bg-white border border-stone-200 rounded-2xl text-sm font-medium text-stone-700 hover:bg-stone-50 transition-colors"
      >
        + Apply for new leave
      </button>

    </div>

    <!-- Modal -->
    <transition
      enter-active-class="transition-opacity duration-200"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-150"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="showForm" class="fixed inset-0 bg-stone-900/50 flex items-end justify-center z-50 p-4" @click.self="showForm = false">
        <div class="bg-white rounded-3xl w-full max-w-xl p-6 max-h-[90vh] overflow-y-auto">
          <div class="flex items-center justify-between mb-6">
            <h2 class="font-serif text-xl text-stone-900">New Leave Application</h2>
            <button @click="showForm = false" class="w-8 h-8 rounded-xl border border-stone-200 text-stone-400 text-xl leading-none flex items-center justify-center hover:bg-stone-50">×</button>
          </div>

          <div class="flex flex-col gap-4">
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="text-[10px] text-stone-400 uppercase tracking-widest block mb-1.5">From Date</label>
                <input v-model="form.from" type="date" class="w-full px-3.5 py-2.5 bg-stone-50 border border-stone-200 rounded-xl text-sm text-stone-900 focus:outline-none focus:border-stone-900 transition-colors" />
              </div>
              <div>
                <label class="text-[10px] text-stone-400 uppercase tracking-widest block mb-1.5">To Date</label>
                <input v-model="form.to" type="date" class="w-full px-3.5 py-2.5 bg-stone-50 border border-stone-200 rounded-xl text-sm text-stone-900 focus:outline-none focus:border-stone-900 transition-colors" />
              </div>
            </div>

            <div>
              <label class="text-[10px] text-stone-400 uppercase tracking-widest block mb-2">Leave Type</label>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="t in leaveTypes" :key="t"
                  @click="form.type = t"
                  class="px-3.5 py-1.5 rounded-full text-xs font-medium border transition-all"
                  :class="form.type === t ? 'bg-stone-900 text-stone-50 border-stone-900' : 'bg-stone-50 text-stone-600 border-stone-200 hover:border-stone-400'"
                >{{ t }}</button>
              </div>
            </div>

            <div>
              <label class="text-[10px] text-stone-400 uppercase tracking-widest block mb-1.5">Reason</label>
              <textarea
                v-model="form.reason"
                rows="3"
                placeholder="Describe your reason..."
                class="w-full px-3.5 py-2.5 bg-stone-50 border border-stone-200 rounded-xl text-sm text-stone-900 placeholder-stone-300 focus:outline-none focus:border-stone-900 resize-none transition-colors"
              ></textarea>
            </div>

            <button
              @click="submitForm"
              class="w-full py-3.5 bg-stone-900 text-stone-50 rounded-2xl text-sm font-medium hover:opacity-85 transition-opacity"
            >
              Submit Application
            </button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useLeaveApplication } from '~/composable/useLeaveApplication'

const { submitLeave, fetchApplications, my_applications } = useLeaveApplication()

const DESKS = ['Submited', 'Pending Class Teacher', 'Pending HOD', 'Approved']

// Active state for UI
const activeFilter = ref('all')
const openId       = ref(null)
const showForm     = ref(false)
const leaveTypes   = ['Medical', 'Personal', 'Family', 'Other']
const form         = ref({ from: '', to: '', type: 'Medical', reason: '' })

// Student Info (You might want to pull this from a user store later)
const student = computed(() => {
  if (applications.value.length > 0) {
    const first = applications.value[0];
    return { name: first.student_name, class: first.student_group, id: first.student };
  }
  return { name: 'Student', class: '-', id: '-' };
})

const initials = computed(() =>
  student.value.name.split(' ').map(n => n[0]).join('').slice(0, 2)
)

// Mapped Applications: Converts API data format to Template format
const applications = computed(() => {
  return (my_applications.value || []).map(app => ({
    id: app.name,               // "EDU-SLA-..."
    from: app.from_date,        // "2026-04-19"
    to: app.to_date,            // "2026-04-22"
    type: 'General',            // API doesn't seem to provide 'type', defaulting to General
    state: app.workflow_state,  // "Pending Class Teacher" or "Approved"
    reason: app.reason,
    student_name: app.student_name,
    student_group: app.student_group,
    student: app.student
  }))
})

const totalApps = computed(() => applications.value.length)

const stats = computed(() => [
  { key: 'all',      label: 'Total',    count: applications.value.length },
  { key: 'pending',  label: 'Pending',  count: applications.value.filter(a => a.state.startsWith('Pending') || a.state === 'Draft').length },
  { key: 'approved', label: 'Approved', count: applications.value.filter(a => a.state === 'Approved').length },
  { key: 'rejected', label: 'Rejected', count: applications.value.filter(a => a.state === 'Rejected' || a.state === 'Cancelled').length },
])

const filteredApps = computed(() => {
  const apps = applications.value
  if (activeFilter.value === 'pending')  return apps.filter(a => a.state.startsWith('Pending') || a.state === 'Draft')
  if (activeFilter.value === 'approved') return apps.filter(a => a.state === 'Approved')
  if (activeFilter.value === 'rejected') return apps.filter(a => a.state === 'Rejected' || a.state === 'Cancelled')
  return apps
})

// UI Helpers
const filterBy = (f) => { activeFilter.value = f }
const toggle   = (id) => { openId.value = openId.value === id ? null : id }
const days       = (from, to) => Math.round((new Date(to) - new Date(from)) / 86400000) + 1
const formatDate = (d) => d ? new Date(d).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) : ''

// Logic for the Progress Stepper
const curIdx         = (state) => state === 'Rejected' ? 1 : DESKS.indexOf(state)
const isDone         = (state, i) => state !== 'Rejected' && i < curIdx(state)
const isActive       = (state, i) => state !== 'Rejected' && i === curIdx(state)
const isRejectedHere = (state, i) => (state === 'Rejected' || state === 'Cancelled') && i === 1

const typeIcon   = (t) => ({ Medical: '🏥', Personal: '✦', Family: '⌂', General: '📋' }[t] || '◈')
const typeIconBg = (t) => ({ Medical: 'bg-green-50', Personal: 'bg-blue-50', Family: 'bg-amber-50', General: 'bg-stone-100' }[t] || 'bg-stone-100')

const statNumColor = (key) => ({ all: 'text-stone-900', pending: 'text-amber-700', approved: 'text-green-700', rejected: 'text-red-700' }[key])
const statBarColor = (key) => ({ all: 'bg-stone-900', pending: 'bg-amber-500', approved: 'bg-green-500', rejected: 'bg-red-400' }[key])

const badgeClass = (state) => {
  if (state === 'Approved') return 'bg-green-50 text-green-800'
  if (state === 'Rejected' || state === 'Cancelled') return 'bg-red-50 text-red-800'
  if (state === 'Draft')    return 'bg-stone-100 text-stone-600'
  return 'bg-amber-50 text-amber-800'
}

const miniDotClass = (state, i) => {
  if (isRejectedHere(state, i)) return 'bg-red-400'
  if (isDone(state, i))         return 'bg-green-500'
  if (isActive(state, i))       return 'bg-amber-500'
  return 'bg-stone-200'
}

const stepCircleClass = (state, i) => {
  if (isDone(state, i))         return 'bg-green-50 text-green-700 border-green-200'
  if (isRejectedHere(state, i)) return 'bg-red-50 text-red-700 border-red-200'
  if (isActive(state, i))       return 'bg-amber-50 text-amber-700 border-amber-200'
  return 'bg-stone-50 text-stone-400 border-stone-200'
}

const shortDesk = (d) => ({ 'Draft': 'Draft', 'Pending Class Teacher': 'Teacher', 'Pending HOD': 'HOD', 'Approved': 'Approved' }[d] || d)

const statusMessage = (state) => ({
  'Approved':              '✓ Your leave has been approved.',
  'Rejected':              '✕ Your leave was not approved.',
  'Cancelled':             '✕ Your leave was cancelled.',
  'Draft':                 '○ Not submitted yet.',
  'Pending Class Teacher': '⏳ Waiting for Class Teacher to review.',
  'Pending HOD':           '⏳ Waiting for HOD to review.',
}[state] || 'Under review.')

const statusMsgClass = (state) => {
  if (state === 'Approved') return 'bg-green-50 text-green-800'
  if (state === 'Rejected' || state === 'Cancelled') return 'bg-red-50 text-red-800'
  if (state === 'Draft')    return 'bg-stone-100 text-stone-600'
  return 'bg-amber-50 text-amber-800'
}

const submitForm = async () => {
  if (!form.value.from || !form.value.to || !form.value.reason) return

  const res = await submitLeave({
    from_date: form.value.from,
    to_date: form.value.to,
    reason: form.value.reason,
    // Add other fields your API expects here
  })

  console.log("response",form.value.from,form.value.to,form.value.reason);
  

  if (res?.status === 'success') {
    await fetchApplications() // Refresh the list from server
    form.value = { from: '', to: '', type: 'Medical', reason: '' }
    showForm.value = false
  }
}

onMounted(() => {
  fetchApplications()
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');

.font-serif { font-family: 'DM Serif Display', serif !important; }
.font-sans  { font-family: 'DM Sans', sans-serif !important; }

@keyframes fade-up {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.animate-fade-up { animation: fade-up 0.3s ease both; }
</style>