<template>
  <main class="flex-1 overflow-y-auto p-6 lg:p-10 custom-scrollbar bg-transparent transition-colors duration-300">

    <!-- HERO SECTION -->
    <div class="relative bg-white dark:bg-slate-900 rounded-[2.5rem] p-8 lg:p-12 overflow-hidden shadow-sm dark:shadow-none border border-transparent dark:border-slate-800 mb-10 transition-colors">
      <div class="relative z-10 flex flex-col lg:flex-row justify-between items-center gap-8">
        
        <div class="max-w-xl text-center lg:text-left">
          <span class="text-indigo-500 dark:text-indigo-400 text-[10px] font-black uppercase tracking-[0.3em] mb-4 block">
            Faculty Control Center
          </span>
          
          <h1 class="text-3xl lg:text-5xl font-black text-slate-900 dark:text-white leading-tight mb-4 transition-colors">
            Hello, <br />
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 to-purple-500">
                Prof. {{ teacherInfo?.name || 'Educator' }}!
            </span>
          </h1>

          <p class="text-slate-500 dark:text-slate-400 text-sm font-medium leading-relaxed mb-6">
            You have {{ todayClasses.length }} classes scheduled today. Your class attendance is looking excellent.
          </p>
          
          <div class="flex gap-8 justify-center lg:justify-start border-t border-slate-100 dark:border-slate-800 pt-6">
            <div>
              <p class="text-2xl font-black text-slate-800 dark:text-slate-200">{{ todayClasses.length }}</p>
              <p class="text-[10px] uppercase font-bold text-slate-400 tracking-widest">Classes Today</p>
            </div>
            <div class="border-l border-slate-100 dark:border-slate-800 pl-8">
              <p class="text-2xl font-black text-slate-800 dark:text-slate-200">12</p>
              <p class="text-[10px] uppercase font-bold text-slate-400 tracking-widest">Pending Tasks</p>
            </div>
          </div>
        </div>

        <img src="~/assets/images/student-walking-nobg.gif" alt="Teacher" class="w-80 lg:w-[380px] object-contain relative z-10" />
      </div>
      
      <!-- Decorative BLUR -->
      <div class="absolute -right-20 -top-20 w-96 h-96 bg-indigo-500/10 dark:bg-indigo-500/5 rounded-full blur-3xl"></div>
    </div>

    <!-- MAIN GRID LAYOUT -->
    <div class="grid grid-cols-1 xl:grid-cols-12 gap-8">
       <!-- LEFT COLUMN -->
       <div class="xl:col-span-8 space-y-8">
          <DailyRoutine :classes="todayClasses" />
          <GradingQueue :pendingItems="pendingGrading" />
       </div>
       
       <!-- RIGHT COLUMN -->
       <div class="xl:col-span-4 space-y-8">
          <AttendanceCard :unMarkedStudents="unMarkedStudents" />
          <Announcements :recentNotices="recentNotices" />
       </div>
    </div>

  </main>
</template>

<script setup>
import { ref } from 'vue'
import DailyRoutine from '~/components/dashboard/teacher/DailyRoutine.vue'
import GradingQueue from '~/components/dashboard/teacher/GradingQueue.vue'
import AttendanceCard from '~/components/dashboard/teacher/AttendanceCard.vue'
import Announcements from '~/components/dashboard/teacher/Announcements.vue'

// Teacher info mock
const teacherInfo = ref({ name: 'Sudipta Ghosh', department: 'Computer Science' })

// Mock data references
const todayClasses = ref([
    { subject: 'Data Structures', time: '10:00 AM', room: 'Lab 1', section: 'Section A' },
    { subject: 'Web Technologies', time: '01:00 PM', room: 'Room 302', section: 'Section C' },
    { subject: 'System Design', time: '03:30 PM', room: 'Audit. 1', section: 'Section B' }
])

const pendingGrading = ref([
    { id: 1, title: 'JavaScript Fundamentals Quiz', class_name: 'CS-101', submissions: 45 },
    { id: 2, title: 'UI Design Prototype', class_name: 'CS-204', submissions: 12 },
    { id: 3, title: 'Database Schema Design', class_name: 'CS-302', submissions: 30 }
])

const unMarkedStudents = ref([
    { id: 1, name: 'Alice Smith', roll: '22', avatar: 'https://i.pravatar.cc/150?u=1' },
    { id: 2, name: 'Bob Jones', roll: '23', avatar: 'https://i.pravatar.cc/150?u=2' },
    { id: 3, name: 'Charlie Brown', roll: '24', avatar: 'https://i.pravatar.cc/150?u=3' },
    { id: 4, name: 'Diana Prince', roll: '25', avatar: 'https://i.pravatar.cc/150?u=4' }
])

const recentNotices = ref([
    { id: 1, title: 'Mid-Term Exam Syllabus', desc: 'Please upload your mid-term syllabus directly to the portal for review.', date: 'Today, 09:00 AM' },
    { id: 2, title: 'Faculty Meetup', desc: 'Join us for a brief touchbase meeting in the staff room on Friday.', date: 'Yesterday, 04:30 PM' }
])

</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
    width: 5px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #e2e8f0;
    border-radius: 10px;
}
</style>