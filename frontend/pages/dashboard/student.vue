<template>
    <main class="flex-1 overflow-y-auto p-6 lg:p-10 custom-scrollbar bg-[#f8fafc]">

        <!-- HERO -->
        <div class="relative bg-white rounded-[2.5rem] p-8 lg:p-12 overflow-hidden shadow-md mb-10">
            <div class="relative z-10 flex flex-col lg:flex-row justify-between items-center gap-8">

                <div class="max-w-xl text-center lg:text-left">

                    <span class="text-indigo-400 text-[10px] font-black uppercase tracking-[0.3em] mb-4 block">
                        Student Overview
                    </span>

                    <h1 class="text-3xl lg:text-5xl font-black text-black leading-tight mb-4">
                        Welcome back, <br />

                        <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">
                            {{ dashboardData?.student_info?.name || 'Scholar' }}!
                        </span>

                    </h1>

                    <p class="text-slate-400 text-sm font-medium leading-relaxed">
                        Your academic progress this week is looking excellent.
                    </p>

                </div>

                <!-- BIGGER IMAGE -->
                <img :src="walkingStudent" alt="Student" class="w-80 lg:w-[420px] object-contain" />

            </div>

            <div class="absolute -right-20 -top-20 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl"></div>

        </div>


        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

            <!-- LEFT SIDE -->
            <div class="lg:col-span-8 space-y-8">
                <CurrentProgram :program-data="programData" @click="showModal = true" />
                <TodayClass :todayClasses="todayClasses" />
                <UpcomingExams :upcomingExams="upcomingExams" />
                <Assignment :assignments="assignments" />
                <PaymentHistory />
            </div>


            <!-- RIGHT SIDE -->
            <div class="lg:col-span-4 space-y-8">

                <!-- ATTENDANCE -->
                <Attendance :attendance="attendanceData" />
                <StopWatch />
                <!-- <BookRecommendetion :recommendedBooks="recommendedBooks" /> -->
                <CampusNotice :notices="notices" />
                <AcademicCalendar />
                <!-- <Event /> -->
            </div>

        </div>

    </main>

    <!-- CURRICULUM MODAL -->

    <div v-if="showModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50">

        <div class="bg-white w-full max-w-3xl rounded-[2rem] shadow-2xl p-8 relative">

            <!-- CLOSE -->

            <button @click="showModal = false" class="absolute top-5 right-5 text-slate-400 hover:text-black">

                <i class="fa fa-times"></i>

            </button>


            <!-- HEADER -->

            <h2 class="text-2xl font-black text-slate-800 mb-2">

                {{ programData.name }}

            </h2>

            <p class="text-xs text-slate-400 mb-6">

                Semester {{ programData.semester }}

            </p>


            <!-- PROGRAM DESCRIPTION -->

            <div class="mb-6">

                <h3 class="text-xs font-black uppercase text-slate-400 mb-2">

                    Program Overview

                </h3>

                <p class="text-sm text-slate-600">

                    {{ programData.description }}

                </p>

            </div>


            <!-- SUBJECTS -->

            <div>

                <h3 class="text-xs font-black uppercase text-slate-400 mb-4">

                    Curriculum Subjects

                </h3>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

                    <div v-for="subject in programData.subjects" :key="subject.name"
                        class="p-4 bg-slate-50 rounded-xl border border-slate-100 flex justify-between">

                        <span class="font-bold text-slate-700 text-sm">

                            {{ subject.name }}

                        </span>

                        <span class="text-xs text-indigo-500 font-bold">

                            {{ subject.credits }} Credits

                        </span>

                    </div>

                </div>

            </div>


            <!-- FOOTER -->

            <div class="mt-8 flex justify-end">

                <button @click="showModal = false"
                    class="px-6 py-2 bg-indigo-600 text-white rounded-xl text-xs font-bold">

                    Close

                </button>

            </div>

        </div>

    </div>
</template>


<script setup>
import { ref, computed } from 'vue'
import walkingStudent from '~/assets/images/student-walking-nobg.gif'
import CurrentProgram from '~/components/dashbaord/currentProgram.vue'
import { useStudentDashboard } from '~/composable/userDashboard'
import Assignment from '~/components/dashbaord/assignment.vue'
import UpcomingExams from '~/components/dashbaord/upcomingExams.vue'
import TodayClass from '~/components/dashbaord/todayClass.vue'
import StopWatch from '~/components/dashbaord/stopWatch.vue'
import AcademicCalendar from '~/components/dashbaord/academicCalendar.vue'
import PaymentHistory from '~/components/dashbaord/paymentHistory.vue'
import Attendance from '~/components/dashbaord/attendance.vue'
import BookRecommendetion from '~/components/dashbaord/bookRecommendetion.vue'
import CampusNotice from '~/components/dashbaord/campusNotice.vue'
import Event from '~/components/dashbaord/event.vue'
import { useAssignments } from '~/composable/useAssignments'
import { useTimetable } from '~/composable/useTimetable'
import { useNotices } from '~/composable/useNotices'

const { dashboardData, loading, error, loadDashboard } = useStudentDashboard()
const { assignments, fetchAssignments } = useAssignments()
const showModal = ref(false)

// class schedule data
const { activeDay, weekDays, currentDaySchedule: todayClasses, fetchSchedule } = useTimetable()
const today = new Date().toLocaleDateString('en-US', { weekday: 'long' })
if (weekDays.includes(today)) activeDay.value = today


// notice data
const { notices: allNotices, fetchNotices } = useNotices()
const notices = computed(() => allNotices.value.slice(0, 3))


/* PROGRAM DATA */
const programData = computed(() => {
    const studentInfo = dashboardData.value?.student_info
    const courses = dashboardData.value?.courses || []

    if (!studentInfo) return {}

    return {
        name: studentInfo.program || 'N/A',
        semester: studentInfo.semester || 'N/A',
        endDate: "June 24, 2026",
        daysRemaining: 112,
        description: `A comprehensive program for ${studentInfo.program || 'your studies'}, focusing on your academic growth.`,
        subjects: courses.map(c => ({
            name: c.name || c.code || 'Unnamed Subject',
            code: c.code || c.id || '',
            credits: 1,
            teacher: c.teacher || 'TBD',
            grade: c.grade || 'N/A',
            next_class: c.next_class || null
        }))
    }
})


/* UPCOMING EXAMS DATA */
const upcomingExams = computed(() => {
  const today = new Date()
  const upcommingExamination = dashboardData.value?.assessments || []

  return upcommingExamination
    .map(a => ({
      id: a.id,
      subject: a.title,       
      date: a.date,             
      description: a.description,
      day: a.day,
      month: a.month
    }))
    .filter(a => new Date(a.date) >= today)
    .sort((a, b) => new Date(a.date) - new Date(b.date)) 
})

/* BOOKS */
const recommendedBooks = ref([
    {
        title: 'Atomic Habits',
        author: 'James Clear',
        cover: 'https://m.media-amazon.com/images/I/513Y5o-DYtL.jpg'
    },
    {
        title: 'Deep Work',
        author: 'Cal Newport',
        cover: 'https://m.media-amazon.com/images/I/41f4oFz3u-L.jpg'
    }
])

// attendance data
const attendanceData = computed(() => {
  const att = dashboardData.value?.attendance
  if (!att) return {
    present_days: 0,
    absent_days: 0,
    leave_days: 0,
    total_days: 0
  }

  return {
    present_days: att.present_days,
    absent_days: att.absent_days,
    leave_days: att.leave_days,
    total_days: att.total_days
  }
})

onMounted(() => {
    loadDashboard()
    fetchAssignments()
    fetchSchedule()
    fetchNotices()  
})
</script>


<style scoped>
.custom-scrollbar::-webkit-scrollbar {
    width: 5px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #e2e8f0;
    border-radius: 10px;
}

.transition-all {
    transition: all .3s cubic-bezier(.4, 0, .2, 1);
}
</style>