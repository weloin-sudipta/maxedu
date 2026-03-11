<template>
  <div class="space-y-6 animate-in fade-in duration-500">
    
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-8 rounded-[2.5rem] border border-slate-200/60 shadow-sm">
      <div>
        <h2 class="text-2xl font-black text-slate-800 tracking-tight">School Events & Calendar</h2>
        <p class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mt-1">Academic Year 2025-26</p>
      </div>
      <div class="flex gap-2">
        <button @click="showCalendarModal = true" class="btn-icon h-12 w-12">
          <i class="fa fa-calendar-o"></i>
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="flex flex-col items-center gap-4">
        <div class="w-10 h-10 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
        <p class="text-xs font-bold text-slate-400 uppercase tracking-widest">Loading events...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="errorMessage" class="bg-red-50 rounded-[2.5rem] p-8 border border-red-100 text-center">
      <i class="fa fa-exclamation-triangle text-red-400 text-2xl mb-3"></i>
      <p class="text-sm font-bold text-red-600">{{ errorMessage }}</p>
      <button @click="loadEvents" class="mt-4 px-6 py-2 bg-red-100 text-red-700 rounded-xl text-xs font-bold hover:bg-red-200 transition-colors">Retry</button>
    </div>

    <template v-else>
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div class="lg:col-span-8 space-y-6">
          <div class="flex gap-2 overflow-x-auto no-scrollbar pb-2">
            <button 
              v-for="filter in dynamicFilters" :key="filter"
              @click="activeFilter = filter"
              :class="[
                activeFilter === filter ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-100' : 'bg-white text-slate-500 border-slate-200',
                'px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest border transition-all whitespace-nowrap'
              ]"
            >
              {{ filter }}
            </button>
          </div>

          <!-- Empty State -->
          <div v-if="filteredEvents.length === 0" class="bg-white rounded-[2.5rem] p-12 border border-slate-200/60 shadow-sm text-center">
            <i class="fa fa-calendar-check-o text-slate-300 text-4xl mb-4"></i>
            <p class="text-sm font-bold text-slate-500">No events found</p>
            <p class="text-xs text-slate-400 mt-1">{{ activeFilter === 'All Events' ? 'There are no events scheduled yet.' : `No events match the "${activeFilter}" filter.` }}</p>
          </div>

          <div v-for="event in filteredEvents" :key="event.id" 
               class="bg-white rounded-[2.5rem] p-6 border border-slate-200/60 shadow-sm flex flex-col md:flex-row gap-6 hover:shadow-md transition-all group">
            <div class="flex flex-col items-center justify-center bg-slate-50 rounded-3xl w-full md:w-24 h-24 border border-slate-100 shrink-0">
              <span class="text-[10px] font-black text-indigo-500 uppercase tracking-widest">{{ event.month }}</span>
              <span class="text-3xl font-black text-slate-800">{{ event.day }}</span>
            </div>

            <div class="flex-1">
              <div class="flex justify-between items-start mb-2">
                <div class="flex flex-wrap gap-1">
                  <span v-for="tag in event.tags" :key="tag"
                    :class="['px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-tighter border', getCategoryStyle(tag)]">
                    {{ tag }}
                  </span>
                  <span v-if="event.tags.length === 0"
                    :class="['px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-tighter border', categoryStyles.General]">
                    General
                  </span>
                </div>
                <span v-if="event.time" class="text-[10px] font-bold text-slate-400 whitespace-nowrap ml-2">
                  <i class="fa fa-clock-o mr-1"></i> {{ event.time }}
                </span>
              </div>
              <h3 class="text-lg font-black text-slate-800 group-hover:text-indigo-600 transition-colors">{{ event.title }}</h3>
              <p v-if="event.description" class="text-xs font-medium text-slate-500 mt-2 leading-relaxed line-clamp-2">{{ event.description }}</p>
              
              <div class="flex items-center gap-4 mt-4">
                <div v-if="event.location" class="flex items-center gap-1 text-[10px] font-bold text-slate-400">
                  <i class="fa fa-map-marker text-indigo-400"></i> {{ event.location }}
                </div>
                <div v-if="event.programs && event.programs.length > 0" class="flex items-center gap-1 text-[10px] font-bold text-slate-400">
                  <i class="fa fa-graduation-cap text-purple-400"></i> {{ event.programs.join(', ') }}
                </div>
              </div>
            </div>

            <!-- <div class="flex md:flex-col justify-end gap-2 shrink-0">
              <button class="btn-action-gray"><i class="fa fa-share-alt"></i></button>
              <button class="btn-action-indigo">View</button>
            </div> -->
          </div>
        </div>

        <div class="lg:col-span-4 space-y-6">
          <!-- Upcoming Deadlines -->
          <div class="bg-slate-900 rounded-[2.5rem] p-8 text-white shadow-xl">
            <h3 class="text-xs font-black uppercase tracking-widest opacity-40 mb-6">Upcoming Events</h3>
            <div v-if="upcomingDeadlines.length > 0" class="space-y-6">
              <div v-for="deadline in upcomingDeadlines" :key="deadline.id" class="flex gap-4">
                <div class="w-1 h-10 bg-indigo-500 rounded-full"></div>
                <div>
                  <p class="text-xs font-bold">{{ deadline.title }}</p>
                  <p class="text-[10px] opacity-50 font-medium">{{ deadline.date }}</p>
                </div>
              </div>
            </div>
            <div v-else class="text-xs opacity-40 font-medium">No upcoming events in the next 7 days</div>
          </div>

          <!-- Activity Tags -->
          <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm">
            <h3 class="text-xs font-black uppercase tracking-widest text-slate-400 mb-6">Activity Tags</h3>
            <div v-if="eventTags.length > 0" class="flex flex-wrap gap-2">
              <span v-for="tag in eventTags" :key="tag" 
                    @click="activeFilter = tag"
                    :class="[
                      activeFilter === tag ? 'bg-indigo-50 text-indigo-600 border-indigo-100' : 'bg-slate-50 text-slate-500 border-slate-100',
                      'px-3 py-1 text-[10px] font-bold rounded-lg border cursor-pointer hover:bg-indigo-50 hover:text-indigo-600 transition-colors'
                    ]">
                #{{ tag }}
              </span>
            </div>
            <p v-else class="text-xs text-slate-400">No tags available</p>
          </div>
        </div>
      </div>
    </template>

    <!-- Calendar Modal -->
    <div v-if="showCalendarModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm shadow-2xl" @click="showCalendarModal = false"></div>
      
      <div class="relative bg-white w-full max-w-md rounded-[2.5rem] shadow-2xl overflow-hidden animate-modal">
        <div class="p-8 border-b border-slate-100 flex justify-between items-center">
          <div class="flex items-center gap-4">
            <button @click="changeMonth(-1)" class="w-8 h-8 bg-slate-50 text-slate-400 rounded-xl hover:text-indigo-600 transition-colors flex items-center justify-center">
              <i class="fa fa-chevron-left text-xs"></i>
            </button>
            <div>
              <h3 class="text-xl font-black text-slate-800 tracking-tight">{{ currentMonthName }} {{ currentYear }}</h3>
              <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest mt-1">Event Calendar</p>
            </div>
            <button @click="changeMonth(1)" class="w-8 h-8 bg-slate-50 text-slate-400 rounded-xl hover:text-indigo-600 transition-colors flex items-center justify-center">
              <i class="fa fa-chevron-right text-xs"></i>
            </button>
          </div>
          <button @click="showCalendarModal = false" class="w-10 h-10 bg-slate-50 text-slate-400 rounded-2xl hover:text-rose-500 transition-colors">
            <i class="fa fa-times"></i>
          </button>
        </div>

        <div class="p-8">
          <div class="grid grid-cols-7 gap-2 mb-4">
            <div v-for="(day, idx) in ['S', 'M', 'T', 'W', 'T', 'F', 'S']" :key="'day-' + idx" class="text-center text-[10px] font-black text-slate-300 uppercase">
              {{ day }}
            </div>
          </div>
          
          <div class="grid grid-cols-7 gap-2">
            <div v-for="i in firstDayOfMonth" :key="'empty'+i" class="h-10"></div>
            
            <div v-for="date in daysInMonth" :key="date" 
                 :class="[
                   isEventDateForCalendar(date) ? 'bg-indigo-50 text-indigo-600 border-indigo-100 shadow-sm' : 
                   isToday(date) ? 'bg-slate-900 text-white' :
                   'text-slate-400 hover:bg-slate-50',
                   'h-10 rounded-xl flex flex-col items-center justify-center text-xs font-bold border border-transparent transition-all cursor-pointer relative'
                 ]">
              {{ date }}
              <div v-if="isEventDateForCalendar(date)" class="absolute bottom-1.5 w-1 h-1 bg-indigo-500 rounded-full"></div>
            </div>
          </div>
        </div>

        <div class="px-8 pb-8">
          <div class="bg-slate-50 rounded-2xl p-4 border border-slate-100">
            <p class="text-[9px] font-black text-slate-400 uppercase mb-3">Today's Events</p>
            <div v-if="todaysEvents.length > 0" class="space-y-2">
              <div v-for="ev in todaysEvents" :key="ev.id" class="flex items-center gap-3">
                <div class="w-2 h-2 rounded-full bg-indigo-500"></div>
                <div>
                  <p class="text-xs font-black text-slate-700">{{ ev.title }}</p>
                  <p v-if="ev.time" class="text-[10px] text-slate-400">{{ ev.time }}</p>
                </div>
              </div>
            </div>
            <div v-else class="flex items-center gap-3">
              <div class="w-2 h-2 rounded-full bg-emerald-500"></div>
              <p class="text-xs font-black text-slate-700">No events scheduled for today</p>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useEvents } from '~/composable/useEvents';

const {
  events,
  eventTags,
  loading,
  errorMessage,
  categoryStyles,
  getCategoryStyle,
  loadEvents,
  dynamicFilters,
  getFilteredEvents,
  upcomingDeadlines,
  todaysEvents,
  isEventDate,
} = useEvents();

const showCalendarModal = ref(false);
const activeFilter = ref('All Events');
const calendarDate = ref(new Date());

// Use composable's filter helper
const filteredEvents = getFilteredEvents(activeFilter);

// Calendar helpers
const currentMonthName = computed(() => calendarDate.value.toLocaleString('default', { month: 'long' }));
const currentYear = computed(() => calendarDate.value.getFullYear());
const daysInMonth = computed(() => new Date(calendarDate.value.getFullYear(), calendarDate.value.getMonth() + 1, 0).getDate());
const firstDayOfMonth = computed(() => new Date(calendarDate.value.getFullYear(), calendarDate.value.getMonth(), 1).getDay());

const changeMonth = (delta) => {
  const d = new Date(calendarDate.value);
  d.setMonth(d.getMonth() + delta);
  calendarDate.value = d;
};

const isEventDateForCalendar = (date) => isEventDate(date, calendarDate);

const isToday = (date) => {
  const today = new Date();
  return calendarDate.value.getFullYear() === today.getFullYear()
    && calendarDate.value.getMonth() === today.getMonth()
    && date === today.getDate();
};

onMounted(() => {
  loadEvents();
});
</script>

<style scoped>
.btn-primary { @apply px-6 py-3 bg-indigo-600 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest shadow-xl shadow-indigo-100 hover:bg-indigo-700 transition-all; }
.btn-icon { @apply flex items-center justify-center bg-white border border-slate-200 text-slate-400 rounded-2xl hover:text-indigo-600 hover:border-indigo-100 transition-all; }
.btn-action-gray { @apply w-10 h-10 flex items-center justify-center bg-slate-50 text-slate-400 rounded-xl hover:bg-slate-900 hover:text-white transition-all; }
.btn-action-indigo { @apply px-5 py-2 bg-indigo-50 text-indigo-600 rounded-xl text-[10px] font-black uppercase hover:bg-indigo-600 hover:text-white transition-all; }
.no-scrollbar::-webkit-scrollbar { display: none; }

@keyframes modalEntry {
    from { opacity: 0; transform: scale(0.9) translateY(20px); }
    to { opacity: 1; transform: scale(1) translateY(0); }
}
.animate-modal { animation: modalEntry 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
</style>