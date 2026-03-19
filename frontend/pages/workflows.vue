<template>
  <div class="min-h-screen bg-stone-50 font-sans relative overflow-hidden">

    <div class="fixed top-[-100px] right-[-100px] w-[400px] h-[400px] rounded-full bg-green-500/5 blur-[80px] pointer-events-none z-0"></div>
    <div class="fixed bottom-[100px] left-[-80px] w-[300px] h-[300px] rounded-full bg-amber-500/5 blur-[80px] pointer-events-none z-0"></div>

    <div class="relative z-10 mx-auto px-5 pt-10 pb-16">

      <!-- Loading -->
      <div v-if="loading" class="flex items-center justify-center py-20">
        <div class="w-6 h-6 border-2 border-stone-300 border-t-stone-700 rounded-full animate-spin mr-3"></div>
        <span class="text-sm text-stone-400">Loading workflows...</span>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-2xl px-4 py-3">
        {{ error }}
      </div>

      <template v-else-if="workflows.length">

        <!-- Header -->
        <header class="flex items-center gap-3 mb-8">
          <div class="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-stone-50 font-serif text-base tracking-wide flex-shrink-0">
            {{ initials }}
          </div>
          <div class="flex-1 min-w-0">
            <h1 class="font-serif text-xl text-stone-900 leading-tight">{{ studentInfo.name }}</h1>
            <p class="text-xs text-stone-400 mt-0.5 tracking-wide">
              {{ studentInfo.class }} &nbsp;·&nbsp; {{ studentInfo.id }}
            </p>
          </div>
          <button
            v-if="isLeaveTab"
            @click="showForm = true"
            class="flex items-center gap-1.5 px-4 py-2 bg-stone-900 text-stone-50 rounded-xl text-xs font-medium hover:opacity-80 transition-opacity whitespace-nowrap"
          >
            <span class="text-base leading-none">+</span>
            Apply for Leave
          </button>
        </header>

        <!-- Workflow Tabs -->
        <div class="flex gap-1.5 flex-wrap mb-6 border-b border-stone-200 pb-0">
          <button
            v-for="(wf, i) in workflows"
            :key="wf.workflow_name"
            @click="switchTab(i)"
            class="px-4 py-2 text-sm border-b-2 -mb-px transition-all"
            :class="activeTab === i
              ? 'border-stone-900 text-stone-900 font-medium'
              : 'border-transparent text-stone-400 hover:text-stone-600'"
          >
            {{ wf.workflow_name }}
          </button>
        </div>

        <template v-if="activeWorkflow">

          <!-- Stat cards -->
          <div class="grid gap-2 mb-7" :style="{ gridTemplateColumns: `repeat(${stats.length}, minmax(0, 1fr))` }">
            <div
              v-for="stat in stats"
              :key="stat.key"
              @click="selectFilter(stat.key)"
              class="bg-white border rounded-2xl p-3.5 cursor-pointer transition-all hover:-translate-y-0.5"
              :class="activeFilter === stat.key ? 'border-stone-900' : 'border-stone-200'"
            >
              <div
                class="font-serif text-2xl leading-none mb-1"
                :style="{ color: stat.key === 'all' ? '#1c1917' : stateColor(stat.key).text }"
              >{{ stat.count }}</div>
              <div class="text-[10px] text-stone-400 uppercase tracking-widest mb-2">{{ stat.label }}</div>
              <div class="h-0.5 bg-stone-100 rounded-full overflow-hidden">
                <div
                  class="h-full rounded-full transition-all duration-500"
                  :style="{
                    width: stat.key === 'all' ? '100%' : (activeWorkflow.documents.length ? (stat.count / activeWorkflow.documents.length * 100) + '%' : '0%'),
                    background: stat.key === 'all' ? '#1c1917' : stateColor(stat.key).dot
                  }"
                ></div>
              </div>
            </div>
          </div>

          <!-- Section label + page info -->
          <div class="flex items-center justify-between mb-3">
            <p class="text-[10px] text-stone-400 uppercase tracking-widest">
              {{ activeWorkflow.workflow_name }} — {{ filteredDocs.length }} records
            </p>
            <p v-if="totalPages > 1" class="text-[10px] text-stone-400 uppercase tracking-widest">
              Page {{ currentPage }} of {{ totalPages }}
            </p>
          </div>

          <!-- Document cards -->
          <div class="flex flex-col gap-2.5">

            <div v-if="filteredDocs.length === 0" class="text-center py-12 text-stone-400">
              <div class="text-3xl mb-2">📋</div>
              <p class="text-sm">No applications here</p>
            </div>

            <div
              v-for="(doc, index) in paginatedDocs"
              :key="doc.name"
              @click="toggleOpen(doc.name)"
              class="bg-white border rounded-2xl px-5 py-4 cursor-pointer transition-all animate-fade-up"
              :class="openId === doc.name ? 'border-stone-900' : 'border-stone-200 hover:border-stone-300 hover:shadow-sm'"
              :style="{ animationDelay: index * 40 + 'ms' }"
            >
              <!-- Top row -->
              <div class="flex items-center justify-between mb-3.5">
                <div class="flex items-center gap-3">
                  <div
                    class="w-9 h-9 rounded-xl flex items-center justify-center text-xs font-medium flex-shrink-0"
                    :style="{ background: stateColor(doc.workflow_state).bg, color: stateColor(doc.workflow_state).text }"
                  >
                    {{ (currentPage - 1) * PAGE_SIZE + index + 1 }}
                  </div>
                  <div>
                    <div class="text-sm font-medium text-stone-900">{{ activeWorkflow.document_type }}</div>
                    <div class="text-[11px] text-stone-400 tracking-wide font-mono">{{ doc.name }}</div>
                  </div>
                </div>
                <div class="flex items-center gap-2.5">
                  <span
                    class="text-[11px] font-medium px-2.5 py-1 rounded-full"
                    :style="{ background: stateColor(doc.workflow_state).bg, color: stateColor(doc.workflow_state).text }"
                  >
                    {{ doc.workflow_state }}
                  </span>
                  <span
                    class="text-xl text-stone-300 leading-none transition-transform duration-200 inline-block"
                    :class="openId === doc.name ? 'rotate-90' : ''"
                  >›</span>
                </div>
              </div>

              <!-- Dates + mini dot tracker -->
              <div class="flex items-center justify-between gap-3">
                <div class="flex items-center gap-1.5 text-xs text-stone-500 flex-wrap">
                  <span v-if="doc.from_date">{{ formatDate(doc.from_date) }}</span>
                  <span v-if="doc.from_date && doc.to_date" class="text-stone-300">→</span>
                  <span v-if="doc.to_date">{{ formatDate(doc.to_date) }}</span>
                  <span
                    v-if="doc.total_leave_days > 0"
                    class="bg-stone-100 text-stone-500 text-[10px] font-medium px-2 py-0.5 rounded-full ml-1"
                  >{{ doc.total_leave_days }}d</span>
                </div>
                <!-- Mini tracker dots -->
                <div class="flex items-center flex-shrink-0">
                  <template v-for="(s, i) in stateOrder" :key="s">
                    <div
                      class="w-2 h-2 rounded-full flex-shrink-0 transition-colors"
                      :style="{ background: miniDotColor(doc.workflow_state, s, i) }"
                    ></div>
                    <div
                      v-if="i < stateOrder.length - 1"
                      class="w-4 h-px flex-shrink-0"
                      :style="{ background: isMiniLineFilled(doc.workflow_state, i) ? '#22c55e' : '#E7E5E4' }"
                    ></div>
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
                <div v-if="openId === doc.name" class="mt-4">
                  <div class="h-px bg-stone-100 mb-4"></div>

                  <!-- Dynamic fields -->
                  <div class="grid grid-cols-3 gap-2 mb-5">
                    <div
                      v-for="field in docFields(doc)"
                      :key="field.key"
                      class="bg-stone-50 rounded-xl px-3 py-2.5"
                    >
                      <div class="text-[10px] text-stone-400 uppercase tracking-widest mb-1">{{ field.label }}</div>
                      <div class="text-[13px] font-medium text-stone-800 truncate">{{ field.value }}</div>
                    </div>
                  </div>

                  <!-- Full step tracker with full state names -->
                  <div class="flex items-start">
                    <template v-for="(s, i) in stateOrder" :key="s">
                      <div class="flex flex-col items-center flex-1">
                        <div
                          class="w-7 h-7 rounded-full flex items-center justify-center text-[11px] font-medium border transition-colors"
                          :class="stepCircleClass(doc.workflow_state, s, i)"
                        >
                          <span v-if="isStepRejected(doc.workflow_state, s)">✕</span>
                          <span v-else-if="isStepDone(doc.workflow_state, i)">✓</span>
                          <span v-else>{{ i + 1 }}</span>
                        </div>
                        <!-- Full state name — wraps naturally -->
                        <div class="text-[9px] text-stone-400 mt-1.5 text-center leading-tight uppercase tracking-wide w-full px-1">
                          {{ s }}
                        </div>
                      </div>
                      <div
                        v-if="i < stateOrder.length - 1"
                        class="flex-1 h-px mt-3.5 flex-shrink-0"
                        :style="{ background: isLineFilled(doc.workflow_state, i) ? '#22c55e' : '#E7E5E4' }"
                      ></div>
                    </template>
                  </div>

                </div>
              </transition>
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="flex items-center justify-between mt-6 gap-2">
            <button
              @click="goToPage(currentPage - 1)"
              :disabled="currentPage === 1"
              class="flex items-center gap-1 px-4 py-2 bg-white border border-stone-200 rounded-xl text-sm text-stone-600 hover:bg-stone-50 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
            >
              ‹ Prev
            </button>

            <div class="flex items-center gap-1">
              <template v-for="page in pageNumbers" :key="page">
                <span v-if="page === '...'" class="px-1.5 text-stone-300 text-sm select-none">…</span>
                <button
                  v-else
                  @click="goToPage(page)"
                  class="w-8 h-8 rounded-lg text-xs font-medium transition-all"
                  :class="page === currentPage
                    ? 'bg-stone-900 text-stone-50'
                    : 'bg-white border border-stone-200 text-stone-500 hover:bg-stone-50'"
                >{{ page }}</button>
              </template>
            </div>

            <button
              @click="goToPage(currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="flex items-center gap-1 px-4 py-2 bg-white border border-stone-200 rounded-xl text-sm text-stone-600 hover:bg-stone-50 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
            >
              Next ›
            </button>
          </div>

          <!-- Bottom apply button — leave tab only -->
          <button
            v-if="isLeaveTab"
            @click="showForm = true"
            class="w-full mt-4 py-3 bg-white border border-stone-200 rounded-2xl text-sm font-medium text-stone-700 hover:bg-stone-50 transition-colors"
          >
            + Apply for new leave
          </button>

        </template>
      </template>

      <div v-else-if="!loading" class="text-center py-16 text-sm text-stone-400">
        No workflows found.
      </div>

    </div>

    <!-- Leave Application Modal -->
    <transition
      enter-active-class="transition-opacity duration-200"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-150"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="showForm"
        class="fixed inset-0 bg-stone-900/50 flex items-end justify-center z-50 p-4"
        @click.self="closeForm"
      >
        <div class="bg-white rounded-3xl w-full max-w-xl p-6 max-h-[90vh] overflow-y-auto">

          <!-- Modal header -->
          <div class="flex items-center justify-between mb-6">
            <h2 class="font-serif text-xl text-stone-900">New Leave Application</h2>
            <button
              @click="closeForm"
              class="w-8 h-8 rounded-xl border border-stone-200 text-stone-400 text-xl leading-none flex items-center justify-center hover:bg-stone-50"
            >×</button>
          </div>

          <!-- Top error banner -->
          <transition
            enter-active-class="transition-all duration-200 ease-out"
            enter-from-class="opacity-0 -translate-y-1"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition-all duration-150"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
          >
            <div
              v-if="formError"
              class="mb-4 bg-red-50 border border-red-200 text-red-700 text-xs rounded-xl px-3.5 py-2.5 flex items-start gap-2"
            >
              <span class="mt-0.5 flex-shrink-0">⚠</span>
              <span>{{ formError }}</span>
            </div>
          </transition>

          <div class="flex flex-col gap-4">

            <!-- Date range -->
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="text-[10px] text-stone-400 uppercase tracking-widest block mb-1.5">
                  From Date <span class="text-red-400">*</span>
                </label>
                <input
                  v-model="form.from_date"
                  :min="today"
                  type="date"
                  @change="onFromDateChange"
                  class="w-full px-3.5 py-2.5 bg-stone-50 border rounded-xl text-sm text-stone-900 focus:outline-none focus:border-stone-900 transition-colors"
                  :class="fieldErrors.from_date ? 'border-red-300 bg-red-50' : 'border-stone-200'"
                />
                <p v-if="fieldErrors.from_date" class="text-[10px] text-red-500 mt-1 pl-1">
                  {{ fieldErrors.from_date }}
                </p>
              </div>
              <div>
                <label class="text-[10px] text-stone-400 uppercase tracking-widest block mb-1.5">
                  To Date <span class="text-red-400">*</span>
                </label>
                <input
                  v-model="form.to_date"
                  type="date"
                  :min="minToDate"
                  @change="clearFieldError('to_date')"
                  class="w-full px-3.5 py-2.5 bg-stone-50 border rounded-xl text-sm text-stone-900 focus:outline-none focus:border-stone-900 transition-colors"
                  :class="fieldErrors.to_date ? 'border-red-300 bg-red-50' : 'border-stone-200'"
                />
                <p v-if="fieldErrors.to_date" class="text-[10px] text-red-500 mt-1 pl-1">
                  {{ fieldErrors.to_date }}
                </p>
              </div>
            </div>

            <!-- Duration preview -->
            <div
              v-if="form.from_date && form.to_date && !fieldErrors.to_date && leaveDays > 0"
              class="flex items-center gap-2 text-xs text-stone-500 bg-stone-50 rounded-xl px-3.5 py-2.5"
            >
              <span class="text-stone-400">Duration:</span>
              <span class="font-medium text-stone-800">{{ leaveDays }} day{{ leaveDays > 1 ? 's' : '' }}</span>
              <span class="text-stone-300 mx-1">·</span>
              <span>{{ formatDate(form.from_date) }} → {{ formatDate(form.to_date) }}</span>
            </div>

            <!-- Leave type — optional -->
            <div>
              <label class="text-[10px] text-stone-400 uppercase tracking-widest block mb-2">
                Leave Type
                <span class="normal-case tracking-normal text-stone-300 ml-1 font-sans text-[10px]">(optional)</span>
              </label>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="t in leaveTypes"
                  :key="t"
                  @click="form.leave_type = form.leave_type === t ? '' : t"
                  class="px-3.5 py-1.5 rounded-full text-xs font-medium border transition-all"
                  :class="form.leave_type === t
                    ? 'bg-stone-900 text-stone-50 border-stone-900'
                    : 'bg-stone-50 text-stone-600 border-stone-200 hover:border-stone-400'"
                >{{ t }}</button>
              </div>
            </div>

            <!-- Reason — mandatory -->
            <div>
              <label class="text-[10px] text-stone-400 uppercase tracking-widest block mb-1.5">
                Reason <span class="text-red-400">*</span>
              </label>
              <textarea
                v-model="form.reason"
                rows="3"
                placeholder="Describe your reason..."
                @input="clearFieldError('reason')"
                class="w-full px-3.5 py-2.5 bg-stone-50 border rounded-xl text-sm text-stone-900 placeholder-stone-300 focus:outline-none focus:border-stone-900 resize-none transition-colors"
                :class="fieldErrors.reason ? 'border-red-300 bg-red-50' : 'border-stone-200'"
              ></textarea>
              <p v-if="fieldErrors.reason" class="text-[10px] text-red-500 mt-1 pl-1">
                {{ fieldErrors.reason }}
              </p>
            </div>

            <!-- Submit -->
            <button
              @click="submitForm"
              :disabled="formSubmitting"
              class="w-full py-3.5 bg-stone-900 text-stone-50 rounded-2xl text-sm font-medium hover:opacity-85 transition-opacity disabled:opacity-50"
            >
              <span v-if="formSubmitting" class="flex items-center justify-center gap-2">
                <span class="w-4 h-4 border-2 border-stone-50/30 border-t-stone-50 rounded-full animate-spin"></span>
                Submitting...
              </span>
              <span v-else>Submit Application</span>
            </button>

          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useWorkflow }         from '~/composable/useAllWorkFlow'
import { useLeaveApplication } from '~/composable/useLeaveApplication'

const { loading, error, workflows, fetchWorkflow } = useWorkflow()
const { submitLeave } = useLeaveApplication()

const today = computed(() => new Date().toISOString().split('T')[0])

// ─── UI state ─────────────────────────────────────────────────────────────────
const activeTab    = ref(0)
const activeFilter = ref('all')
const openId       = ref(null)
const currentPage  = ref(1)
const PAGE_SIZE    = 5

// ─── Form state ───────────────────────────────────────────────────────────────
const showForm       = ref(false)
const formSubmitting = ref(false)
const formError      = ref('')
const fieldErrors    = ref({})
const leaveTypes     = ['Medical', 'Personal', 'Family', 'Other']
const form           = ref({ from_date: '', to_date: '', leave_type: '', reason: '' })

onMounted(() => fetchWorkflow())

// ─── Tab switch ───────────────────────────────────────────────────────────────
const switchTab = (i) => {
  activeTab.value    = i
  activeFilter.value = 'all'
  openId.value       = null
  currentPage.value  = 1
  stateColorCache.clear()
}

const selectFilter = (key) => {
  activeFilter.value = key
  currentPage.value  = 1
  openId.value       = null
}

const toggleOpen = (id) => {
  openId.value = openId.value === id ? null : id
}

const goToPage = (p) => {
  if (p < 1 || p > totalPages.value) return
  currentPage.value = p
  openId.value      = null
}

// ─── Active workflow ──────────────────────────────────────────────────────────
const activeWorkflow = computed(() => workflows.value[activeTab.value] || null)

const isLeaveTab = computed(() =>
  activeWorkflow.value?.document_type === 'Student Leave Application'
)

// ─── Student info from first doc ─────────────────────────────────────────────
const studentInfo = computed(() => {
  const docs = activeWorkflow.value?.documents || []
  if (docs.length) {
    return {
      name:  docs[0].student_name  || 'Student',
      class: docs[0].student_group || '—',
      id:    docs[0].student       || '—',
    }
  }
  return { name: 'Student', class: '—', id: '—' }
})

const initials = computed(() =>
  studentInfo.value.name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
)

// ─── State order (main chain + terminal states appended) ──────────────────────
const stateOrder = computed(() => {
  if (!activeWorkflow.value) return []
  const { states, transitions } = activeWorkflow.value
  const allStates = states.map(s => s.state)
  const chain     = []
  const visited   = new Set()
  let cur         = allStates[0]
  while (cur && !visited.has(cur)) {
    chain.push(cur)
    visited.add(cur)
    const next = transitions.find(t => t.state === cur && t.action !== 'Reject')
    cur = next ? next.next_state : null
  }
  allStates.forEach(s => { if (!chain.includes(s)) chain.push(s) })
  return chain
})

// States with no outgoing transitions
const terminalStates = computed(() => {
  if (!activeWorkflow.value) return new Set()
  const { states, transitions } = activeWorkflow.value
  return new Set(states.map(s => s.state).filter(s => !transitions.some(t => t.state === s)))
})

// States where doc_status = 1 (submitted/approved)
const successStates = computed(() => {
  if (!activeWorkflow.value) return new Set()
  return new Set(
    activeWorkflow.value.states
      .filter(s => s.doc_status === '1' || s.doc_status === 1)
      .map(s => s.state)
  )
})

// Terminal states that are NOT success = rejected/cancelled
const rejectedStates = computed(() =>
  new Set([...terminalStates.value].filter(s => !successStates.value.has(s)))
)

// ─── Stats: total + one per state with docs ───────────────────────────────────
const stats = computed(() => {
  const docs   = activeWorkflow.value?.documents || []
  const counts = {}
  docs.forEach(d => { counts[d.workflow_state] = (counts[d.workflow_state] || 0) + 1 })
  const perState = stateOrder.value
    .filter(s => counts[s] > 0)
    .map(s => ({ key: s, label: s, count: counts[s] }))
  return [{ key: 'all', label: 'Total', count: docs.length }, ...perState]
})

// ─── Filtered + paginated ─────────────────────────────────────────────────────
const filteredDocs = computed(() => {
  if (!activeWorkflow.value) return []
  const docs = activeWorkflow.value.documents
  if (activeFilter.value === 'all') return docs
  return docs.filter(d => d.workflow_state === activeFilter.value)
})

const totalPages = computed(() =>
  Math.max(1, Math.ceil(filteredDocs.value.length / PAGE_SIZE))
)

const paginatedDocs = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filteredDocs.value.slice(start, start + PAGE_SIZE)
})

// Smart page number list with ellipsis
const pageNumbers = computed(() => {
  const total = totalPages.value
  const cur   = currentPage.value
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1)
  const pages  = new Set([1, total, cur, cur - 1, cur + 1].filter(p => p >= 1 && p <= total))
  const sorted = [...pages].sort((a, b) => a - b)
  const result = []
  sorted.forEach((p, i) => {
    if (i > 0 && p - sorted[i - 1] > 1) result.push('...')
    result.push(p)
  })
  return result
})

// ─── Date helpers ─────────────────────────────────────────────────────────────
const formatDate = (d) => {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}

const leaveDays = computed(() => {
  if (!form.value.from_date || !form.value.to_date) return 0
  const diff = (new Date(form.value.to_date) - new Date(form.value.from_date)) / 86400000
  return diff >= 0 ? diff + 1 : 0
})

// to_date must be strictly after from_date
const minToDate = computed(() => {
  if (!form.value.from_date) return ''
  const d = new Date(form.value.from_date)
  d.setDate(d.getDate() + 1)
  return d.toISOString().split('T')[0]
})

const onFromDateChange = () => {
  clearFieldError('from_date')
  if (form.value.to_date && form.value.to_date <= form.value.from_date) {
    form.value.to_date        = ''
    fieldErrors.value.to_date = 'To date must be after from date'
  }
}

// ─── Form validation ──────────────────────────────────────────────────────────
const clearFieldError = (key) => {
  const errs = { ...fieldErrors.value }
  delete errs[key]
  fieldErrors.value = errs
  if (!Object.keys(errs).length) formError.value = ''
}

const validateForm = () => {
  const errors = {}
  if (!form.value.from_date) {
    errors.from_date = 'From date is required'
  }
  if (!form.value.to_date) {
    errors.to_date = 'To date is required'
  } else if (form.value.from_date && form.value.to_date <= form.value.from_date) {
    errors.to_date = 'To date must be after from date'
  }
  if (!form.value.reason?.trim()) {
    errors.reason = 'Reason is required'
  }
  return errors
}

const closeForm = () => {
  showForm.value    = false
  formError.value   = ''
  fieldErrors.value = {}
  form.value        = { from_date: '', to_date: '', leave_type: '', reason: '' }
}

const submitForm = async () => {
  formError.value   = ''
  fieldErrors.value = {}

  const errors = validateForm()
  if (Object.keys(errors).length) {
    fieldErrors.value = errors
    formError.value   = 'Please fill in all required fields before submitting.'
    return
  }

  formSubmitting.value = true
  try {
    const res = await submitLeave({
      from_date: form.value.from_date,
      to_date:   form.value.to_date,
      reason:    form.value.reason.trim(),
    })

    if (res?.status === 'success') {
      await fetchWorkflow()
      closeForm()
    } else {
      formError.value = res?.message || 'Submission failed. Please try again.'
    }
  } catch (e) {
    formError.value = e.message || 'Something went wrong.'
  } finally {
    formSubmitting.value = false
  }
}

// ─── Doc fields (dynamic, skip internals) ────────────────────────────────────
const SKIP_KEYS = new Set([
  'name', 'creation', 'modified', 'modified_by', 'owner', 'docstatus',
  'idx', '_user_tags', '_comments', '_assign', '_liked_by', 'amended_from',
  'student', 'workflow_state',
])

const docFields = (doc) =>
  Object.entries(doc)
    .filter(([k, v]) => !SKIP_KEYS.has(k) && v !== null && v !== '' && v !== 0 && v !== false)
    .map(([k, v]) => ({
      key:   k,
      label: k.replace(/_/g, ' '),
      value: k.includes('date') ? formatDate(v) : String(v),
    }))

// ─── Step tracker logic ───────────────────────────────────────────────────────
const stepIndex = (state) => stateOrder.value.indexOf(state)

const isStepDone = (docState, i) => {
  if (rejectedStates.value.has(docState)) return false
  // For success state: all steps up to AND including current are done (all show ✓)
  if (successStates.value.has(docState))  return i <= stepIndex(docState)
  return i < stepIndex(docState)
}

const isStepActive = (docState, i) =>
  !rejectedStates.value.has(docState) &&
  !successStates.value.has(docState) &&
  i === stepIndex(docState)

const isStepRejected = (docState, state) =>
  rejectedStates.value.has(docState) && state === docState

const stepCircleClass = (docState, state, i) => {
  if (isStepRejected(docState, state)) return 'bg-red-50 text-red-700 border-red-200'
  if (isStepDone(docState, i))         return 'bg-green-50 text-green-700 border-green-200'
  if (isStepActive(docState, i))       return 'bg-amber-50 text-amber-700 border-amber-200'
  return 'bg-stone-50 text-stone-400 border-stone-200'
}

// Connecting line between steps
const isLineFilled = (docState, i) => {
  if (rejectedStates.value.has(docState)) return false
  return isStepDone(docState, i)
}

// ─── Mini dot tracker ─────────────────────────────────────────────────────────
const miniDotColor = (docState, state, i) => {
  if (isStepRejected(docState, state)) return '#f87171'
  if (isStepDone(docState, i))         return '#22c55e'
  if (isStepActive(docState, i))       return stateColor(state).dot
  return '#E7E5E4'
}

const isMiniLineFilled = (docState, i) => {
  if (rejectedStates.value.has(docState)) return false
  return isStepDone(docState, i)
}

// ─── Dynamic color assignment by state index ──────────────────────────────────
const COLOR_RAMPS = [
  { bg: '#F1EFE8', text: '#444441', dot: '#888780' },
  { bg: '#FAEEDA', text: '#854F0B', dot: '#EF9F27' },
  { bg: '#E6F1FB', text: '#185FA5', dot: '#378ADD' },
  { bg: '#EAF3DE', text: '#3B6D11', dot: '#639922' },
  { bg: '#EEEDFE', text: '#534AB7', dot: '#7F77DD' },
  { bg: '#E1F5EE', text: '#0F6E56', dot: '#1D9E75' },
  { bg: '#FBEAF0', text: '#993556', dot: '#D4537E' },
  { bg: '#FAECE7', text: '#993C1D', dot: '#D85A30' },
  { bg: '#FCEBEB', text: '#A32D2D', dot: '#E24B4A' },
]

const stateColorCache = new Map()

const stateColor = (state) => {
  if (!stateColorCache.has(state)) {
    const allStates = activeWorkflow.value?.states.map(s => s.state) || []
    const idx       = allStates.indexOf(state)
    stateColorCache.set(state, COLOR_RAMPS[(idx >= 0 ? idx : 0) % COLOR_RAMPS.length])
  }
  return stateColorCache.get(state) ?? COLOR_RAMPS[0]
}
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