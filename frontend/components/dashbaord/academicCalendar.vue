<template>
  <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200 shadow-sm overflow-hidden">

    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h3 class="text-[10px] font-black uppercase tracking-[0.3em] text-slate-400 mb-1">
          Academic Timeline
        </h3>
        <p class="text-xl font-black text-slate-800 tracking-tight">
          {{ monthYear }}
        </p>
      </div>

      <div class="flex gap-2">
        <button @click="prevMonth"
          class="w-8 h-8 rounded-xl bg-slate-50 flex items-center justify-center text-slate-400 hover:bg-indigo-600 hover:text-white">
          <i class="fa fa-chevron-left text-[10px]"></i>
        </button>

        <button @click="nextMonth"
          class="w-8 h-8 rounded-xl bg-slate-50 flex items-center justify-center text-slate-400 hover:bg-indigo-600 hover:text-white">
          <i class="fa fa-chevron-right text-[10px]"></i>
        </button>
      </div>
    </div>

    <!-- Week Days -->
    <div class="grid grid-cols-7 gap-2 mb-6">
      <div v-for="day in weekDays" :key="day"
        class="text-center text-[10px] font-black text-slate-300 uppercase py-2">
        {{ day }}
      </div>

      <!-- Calendar Days -->
      <div v-for="date in calendarDays"
        :key="date.date || Math.random()"
        @click="selectDate(date)"
        class="relative aspect-square flex flex-col items-center justify-center rounded-2xl cursor-pointer border"
        :class="[
          date.isToday ? 'bg-indigo-600 text-white scale-110' : 'hover:bg-slate-50',
          selectedDate === date.date ? 'ring-2 ring-indigo-400' : '',
          date.events.length ? 'font-bold' : ''
        ]"
        :title="date.events.map(e => e.title).join(', ')"
      >
        <span class="text-xs">{{ date.day }}</span>

        <!-- Event Dots -->
        <div v-if="date.events.length" class="absolute bottom-2 flex gap-0.5">
          <div v-for="e in date.events"
            :key="e.title + e.date"
            class="w-1 h-1 rounded-full"
            :class="{
              'bg-rose-400': e.type === 'exam',
              'bg-amber-400': e.type === 'holiday',
              'bg-indigo-400': e.type === 'event',
              'bg-green-400': e.type === 'assignment',
              'bg-white': date.isToday
            }">
          </div>
        </div>
      </div>
    </div>

    <!-- Selected Day -->
    <div class="border-t pt-6">
      <p class="text-[10px] font-black text-slate-400 uppercase mb-4">
        Selected Day Events
      </p>

      <div v-if="selectedEvents.length === 0" class="text-xs text-slate-400">
        No events for this day
      </div>

      <div v-for="item in selectedEvents"
        :key="item.title + item.date"
        class="flex items-center gap-4 mb-3">

        <div class="w-10 h-10 rounded-2xl flex items-center justify-center"
          :class="getTypeStyles(item.type)">
          <i :class="item.icon" class="text-xs"></i>
        </div>

        <div>
          <h4 class="text-xs font-bold text-slate-800">{{ item.title }}</h4>
          <p class="text-[10px] text-slate-400 uppercase">{{ item.type }}</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue"

import { useExamination } from '~/composable/useExaminations'
import { useEvents } from '~/composable/useEvents'
import { useHolidays } from '~/composable/useHolidays'
import { useAssignments } from '~/composable/useAssignments'

/* ---------------- DATA ---------------- */

const { fetchExams, exams } = useExamination()
const { loadEvents, events: frappeEvents } = useEvents()
const { assignments, fetchAssignments } = useAssignments()
const { holidays, fetchHolidays } = useHolidays()

/* ---------------- STATE ---------------- */

const weekDays = ["S","M","T","W","T","F","S"]

const today = new Date()
const currentMonth = ref(today.getMonth())
const currentYear = ref(today.getFullYear())

const selectedDate = ref(null)
const selectedEvents = ref([])

/* ---------------- NORMALIZED DATA ---------------- */

const examEvents = computed(() =>
  (exams.value || []).map(e => ({
    date: e.date,
    title: e.subject,
    type: "exam",
    icon: "fa fa-pencil"
  }))
)

const otherEvents = computed(() =>
  (frappeEvents.value || []).map(e => ({
    date: e.fullDate,   // ✅ FIXED
    title: e.title,     // ✅ FIXED
    type: "event",
    icon: "fa fa-microphone"
  }))
)

const assignmentEvents = computed(() =>
  (assignments.value || []).map(a => ({
    date: a.due_date,   // ✅ ADDED
    title: a.title,
    type: "assignment",
    icon: "fa fa-book"
  }))
)

/* ---------------- MERGE ---------------- */

const allEvents = computed(() => [
  ...examEvents.value,
  ...otherEvents.value,
  ...assignmentEvents.value,
  ...holidays.value
])

/* ---------------- UI ---------------- */

const monthYear = computed(() =>
  new Date(currentYear.value, currentMonth.value)
    .toLocaleString("default",{month:"long",year:"numeric"})
)

const calendarDays = computed(() => {
  const days = []

  const firstDay = new Date(currentYear.value, currentMonth.value,1).getDay()
  const totalDays = new Date(currentYear.value, currentMonth.value+1,0).getDate()

  for(let i=0;i<firstDay;i++){
    days.push({day:"",date:null,events:[]})
  }

  for(let d=1; d<=totalDays; d++){
    const dateStr = `${currentYear.value}-${String(currentMonth.value+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`

    const dayEvents = allEvents.value.filter(e => e.date === dateStr)

    const isToday =
      d===today.getDate() &&
      currentMonth.value===today.getMonth() &&
      currentYear.value===today.getFullYear()

    days.push({
      day:d,
      date:dateStr,
      events:dayEvents,
      isToday
    })
  }

  return days
})

/* ---------------- ACTIONS ---------------- */

const selectDate = (date) => {
  if(!date.date) return
  selectedDate.value = date.date
  selectedEvents.value = date.events
}

const prevMonth = () => {
  if(currentMonth.value===0){
    currentMonth.value=11
    currentYear.value--
  } else currentMonth.value--
}

const nextMonth = () => {
  if(currentMonth.value===11){
    currentMonth.value=0
    currentYear.value++
  } else currentMonth.value++
}

const getTypeStyles = (type) => {
  if(type==="exam") return "bg-rose-50 text-rose-500"
  if(type==="holiday") return "bg-amber-50 text-amber-500"
  if(type==="assignment") return "bg-green-50 text-green-500"
  return "bg-indigo-50 text-indigo-500"
}

/* ---------------- FETCH ---------------- */

onMounted(() => {
  fetchExams()
  loadEvents()
  fetchAssignments()
  fetchHolidays(currentYear.value)
})

watch(currentYear, (year) => {
  fetchHolidays(year)
})

</script>