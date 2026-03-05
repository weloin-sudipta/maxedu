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
        <button class="btn-primary">+ Create New Event</button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <div class="lg:col-span-8 space-y-6">
        <div class="flex gap-2 overflow-x-auto no-scrollbar pb-2">
          <button 
            v-for="filter in filters" :key="filter"
            @click="activeFilter = filter"
            :class="[
              activeFilter === filter ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-100' : 'bg-white text-slate-500 border-slate-200',
              'px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest border transition-all whitespace-nowrap'
            ]"
          >
            {{ filter }}
          </button>
        </div>

        <div v-for="event in filteredEvents" :key="event.id" 
             class="bg-white rounded-[2.5rem] p-6 border border-slate-200/60 shadow-sm flex flex-col md:flex-row gap-6 hover:shadow-md transition-all group">
          <div class="flex flex-col items-center justify-center bg-slate-50 rounded-3xl w-full md:w-24 h-24 border border-slate-100 shrink-0">
            <span class="text-[10px] font-black text-indigo-500 uppercase tracking-widest">{{ event.month }}</span>
            <span class="text-3xl font-black text-slate-800">{{ event.day }}</span>
          </div>

          <div class="flex-1">
            <div class="flex justify-between items-start mb-2">
              <span :class="['px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-tighter border', categoryStyles[event.category]]">
                {{ event.category }}
              </span>
              <span class="text-[10px] font-bold text-slate-400"><i class="fa fa-clock-o mr-1"></i> {{ event.time }}</span>
            </div>
            <h3 class="text-lg font-black text-slate-800 group-hover:text-indigo-600 transition-colors">{{ event.title }}</h3>
            <p class="text-xs font-medium text-slate-500 mt-2 leading-relaxed line-clamp-2">{{ event.description }}</p>
            
            <div class="flex items-center gap-4 mt-4">
              <div class="flex items-center gap-1 text-[10px] font-bold text-slate-400">
                <i class="fa fa-map-marker text-indigo-400"></i> {{ event.location }}
              </div>
              <div class="flex -space-x-2">
                <img v-for="i in 3" :key="i" :src="`https://i.pravatar.cc/150?u=${event.id+i}`" class="w-6 h-6 rounded-full border-2 border-white" />
                <div class="w-6 h-6 rounded-full bg-slate-100 border-2 border-white flex items-center justify-center text-[8px] font-black">+{{ event.attendees }}</div>
              </div>
            </div>
          </div>

          <div class="flex md:flex-col justify-end gap-2 shrink-0">
            <button class="btn-action-gray"><i class="fa fa-share-alt"></i></button>
            <button class="btn-action-indigo">Join</button>
          </div>
        </div>
      </div>

      <div class="lg:col-span-4 space-y-6">
        <div class="bg-slate-900 rounded-[2.5rem] p-8 text-white shadow-xl">
          <h3 class="text-xs font-black uppercase tracking-widest opacity-40 mb-6">Important Deadlines</h3>
          <div class="space-y-6">
            <div v-for="deadline in deadlines" :key="deadline.id" class="flex gap-4">
              <div class="w-1 h-10 bg-indigo-500 rounded-full"></div>
              <div>
                <p class="text-xs font-bold">{{ deadline.title }}</p>
                <p class="text-[10px] opacity-50 font-medium">{{ deadline.date }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm">
          <h3 class="text-xs font-black uppercase tracking-widest text-slate-400 mb-6">Activity Tags</h3>
          <div class="flex flex-wrap gap-2">
            <span v-for="tag in ['Sports', 'Music', 'Science', 'Workshop', 'Holiday']" :key="tag" 
                  class="px-3 py-1 bg-slate-50 text-slate-500 text-[10px] font-bold rounded-lg border border-slate-100">
              #{{ tag }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showCalendarModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm shadow-2xl" @click="showCalendarModal = false"></div>
      
      <div class="relative bg-white w-full max-w-md rounded-[2.5rem] shadow-2xl overflow-hidden animate-modal">
        <div class="p-8 border-b border-slate-100 flex justify-between items-center">
          <div>
            <h3 class="text-xl font-black text-slate-800 tracking-tight">October 2025</h3>
            <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest mt-1">Event Master View</p>
          </div>
          <button @click="showCalendarModal = false" class="w-10 h-10 bg-slate-50 text-slate-400 rounded-2xl hover:text-rose-500 transition-colors">
            <i class="fa fa-times"></i>
          </button>
        </div>

        <div class="p-8">
          <div class="grid grid-cols-7 gap-2 mb-4">
            <div v-for="day in ['S', 'M', 'T', 'W', 'T', 'F', 'S']" :key="day" class="text-center text-[10px] font-black text-slate-300 uppercase">
              {{ day }}
            </div>
          </div>
          
          <div class="grid grid-cols-7 gap-2">
            <div v-for="i in 3" :key="'empty'+i" class="h-10"></div>
            
            <div v-for="date in 31" :key="date" 
                 :class="[
                   isEventDate(date) ? 'bg-indigo-50 text-indigo-600 border-indigo-100 shadow-sm' : 'text-slate-400 hover:bg-slate-50',
                   'h-10 rounded-xl flex flex-col items-center justify-center text-xs font-bold border border-transparent transition-all cursor-pointer relative'
                 ]">
              {{ date }}
              <div v-if="isEventDate(date)" class="absolute bottom-1.5 w-1 h-1 bg-indigo-500 rounded-full"></div>
            </div>
          </div>
        </div>

        <div class="px-8 pb-8">
          <div class="bg-slate-50 rounded-2xl p-4 border border-slate-100">
            <p class="text-[9px] font-black text-slate-400 uppercase mb-3">Today's Focus</p>
            <div class="flex items-center gap-3">
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
import { ref, computed } from 'vue';

const showCalendarModal = ref(false);
const activeFilter = ref('All Events');
const filters = ['All Events', 'Upcoming', 'Ongoing', 'Workshops', 'Sports'];

const categoryStyles = {
  Academic: 'bg-indigo-50 text-indigo-600 border-indigo-100',
  Sports: 'bg-green-50 text-green-600 border-green-100',
  Arts: 'bg-purple-50 text-purple-600 border-purple-100',
  Holiday: 'bg-red-50 text-red-600 border-red-100'
};

const events = ref([
  { id: 1, day: '14', month: 'OCT', title: 'Annual Inter-School Athletics', category: 'Sports', time: '09:00 AM', location: 'Main Stadium', attendees: 45, description: 'Compete in various track and field events. Registration closes this Friday.', status: 'Upcoming' },
  { id: 2, day: '18', month: 'OCT', title: 'Robotics & AI Workshop', category: 'Academic', time: '10:30 AM', location: 'Lab 04', attendees: 12, description: 'Hands-on experience with the new Nano Banana 2 processing models.', status: 'Upcoming' },
  { id: 3, day: '25', month: 'OCT', title: 'Autumn Music Festival', category: 'Arts', time: '04:00 PM', location: 'School Auditorium', attendees: 89, description: 'A celebration of classical and modern music performed by our students.', status: 'Upcoming' },
]);

const deadlines = ref([
  { id: 1, title: 'Term 1 Fee Payment', date: 'Due in 2 days' },
  { id: 2, title: 'Science Project Submission', date: 'Oct 20, 2025' },
  { id: 3, title: 'Winter Camp Registration', date: 'Oct 22, 2025' },
]);

const isEventDate = (date) => {
  return events.value.some(e => parseInt(e.day) === date);
};

const filteredEvents = computed(() => {
  if (activeFilter.value === 'All Events') return events.value;
  return events.value.filter(e => e.category === activeFilter.value || e.status === activeFilter.value);
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