<template>
  <div class="p-6 lg:p-10 max-w-7xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-500">

    <!-- ── Header ─────────────────────────────────────────────────────────── -->
    <HeroHeader title="My Students" subtitle="Program Enrollments" icon="fa fa-users">
      <div class="flex gap-3 flex-wrap">

        <!-- Search -->
        <div class="bg-white dark:bg-slate-900 rounded-xl flex items-center px-4 border border-slate-200 dark:border-slate-800 focus-within:ring-2 focus-within:ring-indigo-500 shadow-sm transition-all h-10">
          <i class="fa fa-search text-slate-400 text-xs"></i>
          <input
            v-model="search"
            type="text"
            placeholder="Search by name or ID..."
            class="w-48 bg-transparent border-none text-xs outline-none ml-2 text-slate-700 dark:text-slate-200 placeholder-slate-400"
          />
          <button v-if="search" @click="search = ''" class="ml-1 text-slate-300 hover:text-slate-500">
            <i class="fa fa-times-circle text-xs"></i>
          </button>
        </div>

        <!-- Program filter -->
        <select
          v-model="selectedProgram"
          class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl px-4 text-xs font-bold text-slate-700 dark:text-slate-200 outline-none h-10 shadow-sm"
        >
          <option value="">All Programs</option>
          <option v-for="prog in uniquePrograms" :key="prog" :value="prog">{{ prog }}</option>
        </select>

        <!-- Term filter -->
        <select
          v-model="selectedTerm"
          class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl px-4 text-xs font-bold text-slate-700 dark:text-slate-200 outline-none h-10 shadow-sm"
        >
          <option value="">All Terms</option>
          <option v-for="term in uniqueTerms" :key="term" :value="term">{{ term }}</option>
        </select>

      </div>
    </HeroHeader>

    <!-- Result count -->
    <p v-if="!loading" class="mt-4 text-xs text-slate-400 dark:text-slate-500 font-semibold">
      Showing <span class="text-indigo-500 font-black">{{ filtered.length }}</span> of {{ enrollments.length }} students
    </p>

    <!-- ── Loading Skeleton ───────────────────────────────────────────────── -->
    <div v-if="loading" class="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
      <div v-for="n in 8" :key="n" class="rounded-[2rem] bg-slate-100 dark:bg-slate-800 animate-pulse h-64" />
    </div>

    <!-- ── Empty State ────────────────────────────────────────────────────── -->
    <div v-else-if="filtered.length === 0" class="mt-20 flex flex-col items-center gap-3 text-slate-400">
      <div class="w-16 h-16 rounded-2xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center">
        <i class="fa fa-user-slash text-2xl"></i>
      </div>
      <p class="text-sm font-bold">No students match your filters</p>
      <button @click="clearFilters" class="text-xs text-indigo-500 font-black hover:underline">Clear filters</button>
    </div>

    <!-- ── Cards Grid ─────────────────────────────────────────────────────── -->
    <div v-else class="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
      <div
        v-for="(enr, i) in filtered"
        :key="enr.name"
        class="group bg-white dark:bg-slate-900 rounded-[2rem] border border-slate-100 dark:border-slate-800 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 cursor-pointer overflow-hidden flex flex-col"
      >

        <!-- Colour accent top bar -->
        <div class="h-1.5 w-full flex-shrink-0" :class="accentBg(i)" />

        <div class="p-5 flex flex-col flex-1">

          <!-- Avatar + name -->
          <div class="flex flex-col items-center text-center mb-4">
            <div
              class="w-16 h-16 rounded-2xl flex items-center justify-center text-white text-xl font-black shadow mb-3 group-hover:scale-105 transition-transform"
              :class="accentBg(i)"
            >
              {{ initials(enr.student_name) }}
            </div>
            <h4 class="text-sm font-black text-slate-800 dark:text-slate-100 leading-tight group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
              {{ enr.student_name }}
            </h4>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-0.5">
              {{ enr.student }}
            </p>
          </div>

          <!-- Info pills -->
          <div class="space-y-2 flex-1">

            <!-- Program -->
            <div class="flex items-center gap-2 bg-slate-50 dark:bg-slate-800/60 rounded-xl px-3 py-2">
              <i class="fa fa-graduation-cap text-[10px] text-indigo-400 w-3"></i>
              <div class="min-w-0">
                <span class="block text-[8px] font-black uppercase tracking-widest text-slate-400">Program</span>
                <span class="text-xs font-bold text-slate-700 dark:text-slate-200 truncate block">{{ enr.program }}</span>
              </div>
            </div>

            <!-- Academic Year -->
            <div class="flex items-center gap-2 bg-slate-50 dark:bg-slate-800/60 rounded-xl px-3 py-2">
              <i class="fa fa-calendar text-[10px] text-blue-400 w-3"></i>
              <div class="min-w-0">
                <span class="block text-[8px] font-black uppercase tracking-widest text-slate-400">Academic Year</span>
                <span class="text-xs font-bold text-slate-700 dark:text-slate-200">{{ enr.academic_year }}</span>
              </div>
            </div>

            <!-- Term -->
            <div class="flex items-center gap-2 bg-slate-50 dark:bg-slate-800/60 rounded-xl px-3 py-2">
              <i class="fa fa-bookmark text-[10px] text-emerald-400 w-3"></i>
              <div class="min-w-0">
                <span class="block text-[8px] font-black uppercase tracking-widest text-slate-400">Term</span>
                <span class="text-xs font-bold text-slate-700 dark:text-slate-200 truncate block">{{ enr.academic_term }}</span>
              </div>
            </div>

            <!-- Enrollment Date -->
            <div class="flex items-center gap-2 bg-slate-50 dark:bg-slate-800/60 rounded-xl px-3 py-2">
              <i class="fa fa-clock-o text-[10px] text-amber-400 w-3"></i>
              <div class="min-w-0">
                <span class="block text-[8px] font-black uppercase tracking-widest text-slate-400">Enrolled On</span>
                <span class="text-xs font-bold text-slate-700 dark:text-slate-200">{{ formatDate(enr.enrollment_date) }}</span>
              </div>
              <!-- Enrollment ID -->
              <span class="ml-auto text-[8px] font-black text-slate-400 bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 px-1.5 py-0.5 rounded-lg whitespace-nowrap">
                {{ enr.name }}
              </span>
            </div>

          </div>

          <!-- CTA Button -->
          <button
            class="mt-4 w-full py-2.5 rounded-xl text-[10px] font-black uppercase tracking-widest border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 group-hover:bg-indigo-500 group-hover:border-indigo-500 group-hover:text-white transition-all duration-200"
          >
            View Profile
          </button>

        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import HeroHeader from '~/components/ui/HeroHeader.vue'
import { fetchStudents } from '~/composable/useStudent'

// ── state ──────────────────────────────────────────────────────────────────────
const loading      = ref(true)
const enrollments  = ref([])   // raw API array — stored as-is, no mapping needed
const search       = ref('')
const selectedProgram = ref('')
const selectedTerm    = ref('')

// ── accent colours ─────────────────────────────────────────────────────────────
const accents = ['bg-indigo-500','bg-violet-500','bg-blue-500','bg-emerald-500','bg-rose-500','bg-amber-500','bg-cyan-500','bg-pink-500']
const accentBg = (i) => accents[i % accents.length]

// ── helpers ────────────────────────────────────────────────────────────────────
const initials = (name = '') =>
  name.trim().split(/\s+/).slice(0, 2).map(w => w[0]?.toUpperCase() ?? '').join('')

const formatDate = (d) =>
  d ? new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) : '—'

const clearFilters = () => {
  search.value = ''
  selectedProgram.value = ''
  selectedTerm.value = ''
}

// ── filter options (derived from real data) ────────────────────────────────────
const uniquePrograms = computed(() =>
  [...new Set(enrollments.value.map(e => e.program).filter(Boolean))]
)
const uniqueTerms = computed(() =>
  [...new Set(enrollments.value.map(e => e.academic_term).filter(Boolean))]
)

// ── filtered list ──────────────────────────────────────────────────────────────
const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()

  return enrollments.value.filter(e => {
    // search: match student_name OR student ID OR program
    const matchSearch =
      !q ||
      e.student_name?.toLowerCase().includes(q) ||
      e.student?.toLowerCase().includes(q) ||
      e.program?.toLowerCase().includes(q)

    // program dropdown filter
    const matchProgram = !selectedProgram.value || e.program === selectedProgram.value

    // term dropdown filter
    const matchTerm = !selectedTerm.value || e.academic_term === selectedTerm.value

    return matchSearch && matchProgram && matchTerm
  })
})

// ── fetch ──────────────────────────────────────────────────────────────────────
onMounted(async () => {
  try {
    // fetchStudents composable already unwraps { message: [...] }
    // and always returns a plain array
    enrollments.value = await fetchStudents()
  } catch (err) {
    console.error('Failed to load enrollments:', err)
  } finally {
    loading.value = false
  }
})
</script>