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
        <header class="mb-8">
          <h1 class="font-serif text-2xl text-stone-900 leading-tight">My Applications</h1>
          <p class="text-xs text-stone-400 mt-1 tracking-wide">Track your submitted requests</p>
        </header>

        <!-- Workflow Tabs -->
        <div class="flex gap-1.5 flex-wrap mb-6 border-b border-stone-200 pb-0">
          <button
            v-for="(wf, i) in workflows"
            :key="wf.workflow_name"
            @click="activeTab = i"
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
              @click="activeFilter = stat.key"
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

          <!-- Section label -->
          <p class="text-[10px] text-stone-400 uppercase tracking-widest mb-3">
            {{ activeWorkflow.workflow_name }} — {{ filteredDocs.length }} records
          </p>

          <!-- Document cards -->
          <div class="flex flex-col gap-2.5">

            <div v-if="filteredDocs.length === 0" class="text-center py-12 text-stone-400">
              <div class="text-3xl mb-2">📋</div>
              <p class="text-sm">No applications here</p>
            </div>

            <div
              v-for="(doc, index) in filteredDocs"
              :key="doc.name"
              @click="toggleOpen(doc.name)"
              class="bg-white border rounded-2xl px-5 py-4 cursor-pointer transition-all animate-fade-up"
              :class="openId === doc.name ? 'border-stone-900' : 'border-stone-200 hover:border-stone-300 hover:shadow-sm'"
              :style="{ animationDelay: index * 50 + 'ms' }"
            >
              <!-- Top row -->
              <div class="flex items-center justify-between mb-3.5">
                <div class="flex items-center gap-3">
                  <div
                    class="w-9 h-9 rounded-xl flex items-center justify-center text-xs font-medium flex-shrink-0"
                    :style="{ background: stateColor(doc.workflow_state).bg, color: stateColor(doc.workflow_state).text }"
                  >
                    {{ index + 1 }}
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
                <!-- Mini tracker -->
                <div class="flex items-center flex-shrink-0">
                  <template v-for="(s, i) in stateOrder" :key="s">
                    <div
                      class="w-2 h-2 rounded-full flex-shrink-0 transition-colors"
                      :style="{ background: miniDotColor(doc.workflow_state, s, i) }"
                    ></div>
                    <div
                      v-if="i < stateOrder.length - 1"
                      class="w-4 h-px flex-shrink-0"
                      :style="{ background: isMiniLineFilled(doc.workflow_state, i) ? stateColor(stateOrder[i]).dot : '#E7E5E4' }"
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

                  <!-- Dynamic fields grid — shows any non-null field from doc except internal ones -->
                  <div class="grid grid-cols-3 gap-2 mb-3">
                    <div
                      v-for="field in docFields(doc)"
                      :key="field.key"
                      class="bg-stone-50 rounded-xl px-3 py-2.5"
                    >
                      <div class="text-[10px] text-stone-400 uppercase tracking-widest mb-1">{{ field.label }}</div>
                      <div class="text-[13px] font-medium text-stone-800 truncate">{{ field.value }}</div>
                    </div>
                  </div>

                  <!-- Full step tracker -->
                  <div class="flex items-start mb-4 mt-5">
                    <template v-for="(s, i) in stateOrder" :key="s">
                      <div class="flex flex-col items-center flex-1">
                        <div
                          class="w-7 h-7 rounded-full flex items-center justify-center text-[11px] font-medium border transition-colors"
                          :class="stepCircleClass(doc.workflow_state, s, i)"
                        >
                          <span v-if="isStepDone(doc.workflow_state, i)">✓</span>
                          <span v-else-if="isStepRejected(doc.workflow_state, s)">✕</span>
                          <span v-else>{{ i + 1 }}</span>
                        </div>
                        <div class="text-[9px] text-stone-400 mt-1.5 text-center leading-tight uppercase tracking-wide max-w-[56px]">
                          {{ shortLabel(s) }}
                        </div>
                      </div>
                      <div
                        v-if="i < stateOrder.length - 1"
                        class="flex-1 h-px mt-3.5 transition-colors"
                        :style="{ background: isStepDone(doc.workflow_state, i) ? '#22c55e' : '#E7E5E4' }"
                      ></div>
                    </template>
                  </div>

                </div>
              </transition>

            </div>
          </div>

        </template>
      </template>

      <div v-else-if="!loading" class="text-center py-16 text-sm text-stone-400">
        No workflows found.
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useWorkflow } from '~/composable/useAllWorkFlow'

const { loading, error, workflows, fetchWorkflow } = useWorkflow()

const activeTab    = ref(0)
const activeFilter = ref('all')
const openId       = ref(null)

onMounted(() => fetchWorkflow())

watch(activeTab, () => {
  activeFilter.value = 'all'
  openId.value = null
  stateColorCache.clear()
})

// --- Active workflow ---
const activeWorkflow = computed(() => workflows.value[activeTab.value] || null)

// --- Build state order from transitions ---
const stateOrder = computed(() => {
  if (!activeWorkflow.value) return []
  const { states, transitions } = activeWorkflow.value
  const allStates = states.map(s => s.state)
  const chain = []
  const visited = new Set()
  let cur = allStates[0]
  while (cur && !visited.has(cur)) {
    chain.push(cur)
    visited.add(cur)
    const next = transitions.find(t => t.state === cur && t.action !== 'Reject')
    cur = next ? next.next_state : null
  }
  allStates.forEach(s => { if (!chain.includes(s)) chain.push(s) })
  return chain
})

// --- Terminal states: no outgoing transitions ---
const terminalStates = computed(() => {
  if (!activeWorkflow.value) return new Set()
  const { states, transitions } = activeWorkflow.value
  return new Set(
    states.map(s => s.state).filter(s => !transitions.some(t => t.state === s))
  )
})

// --- Success states: doc_status === '1' ---
const successStates = computed(() => {
  if (!activeWorkflow.value) return new Set()
  return new Set(
    activeWorkflow.value.states
      .filter(s => s.doc_status === '1' || s.doc_status === 1)
      .map(s => s.state)
  )
})

// --- Rejected states: terminal but not success ---
const rejectedStates = computed(() => {
  return new Set([...terminalStates.value].filter(s => !successStates.value.has(s)))
})

// --- Stats: total + one per state that has docs ---
const stats = computed(() => {
  const docs = activeWorkflow.value?.documents || []
  const counts = {}
  docs.forEach(d => { counts[d.workflow_state] = (counts[d.workflow_state] || 0) + 1 })
  const perState = stateOrder.value
    .filter(s => counts[s] > 0)
    .map(s => ({ key: s, label: shortLabel(s), count: counts[s] }))
  return [{ key: 'all', label: 'Total', count: docs.length }, ...perState]
})

// --- Filtered docs ---
const filteredDocs = computed(() => {
  if (!activeWorkflow.value) return []
  const docs = activeWorkflow.value.documents
  if (activeFilter.value === 'all') return docs
  return docs.filter(d => d.workflow_state === activeFilter.value)
})

// --- Toggle expand ---
const toggleOpen = (id) => { openId.value = openId.value === id ? null : id }

// --- Format date ---
const formatDate = (d) => {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}

// --- Dynamic doc fields: skip internal/system keys, show readable ones ---
const SKIP_KEYS = new Set([
  'name', 'creation', 'modified', 'modified_by', 'owner', 'docstatus',
  'idx', '_user_tags', '_comments', '_assign', '_liked_by', 'amended_from',
  'student', 'workflow_state'
])

const docFields = (doc) => {
  return Object.entries(doc)
    .filter(([k, v]) => !SKIP_KEYS.has(k) && v !== null && v !== '' && v !== 0 && v !== false)
    .map(([k, v]) => ({
      key: k,
      label: k.replace(/_/g, ' '),
      value: k.includes('date') ? formatDate(v) : v
    }))
}

// --- Step logic ---
const stepIndex = (state) => stateOrder.value.indexOf(state)

const isStepDone = (docState, i) => {
  if (rejectedStates.value.has(docState)) return false
  return i < stepIndex(docState)
}

const isStepActive = (docState, i) => i === stepIndex(docState)

const isStepRejected = (docState, state) =>
  rejectedStates.value.has(docState) && state === docState

const stepCircleClass = (docState, state, i) => {
  if (isStepRejected(docState, state)) return 'bg-red-50 text-red-700 border-red-200'
  if (isStepDone(docState, i))         return 'bg-green-50 text-green-700 border-green-200'
  if (isStepActive(docState, i))       return 'bg-amber-50 text-amber-700 border-amber-200'
  return 'bg-stone-50 text-stone-400 border-stone-200'
}

// --- Mini dot tracker ---
const miniDotColor = (docState, state, i) => {
  if (isStepRejected(docState, state)) return '#f87171'
  if (isStepDone(docState, i))         return '#22c55e'
  if (isStepActive(docState, i))       return stateColor(state).dot
  return '#E7E5E4'
}

const isMiniLineFilled = (docState, i) => {
  if (rejectedStates.value.has(docState)) return false
  return i < stepIndex(docState)
}

// --- Short label for stepper ---
const shortLabel = (s) => {
  if (s.length <= 9) return s
  return s.split(' ').map(w => w[0].toUpperCase()).join('')
}

// --- Dynamic color by state index ---
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
    const idx = allStates.indexOf(state)
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