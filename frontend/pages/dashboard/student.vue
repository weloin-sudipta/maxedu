<template>
    <main class="flex-1 overflow-y-auto p-6 lg:p-10 custom-scrollbar bg-[#f8fafc]">

        <!-- HERO -->
        <div class="relative bg-white rounded-[2.5rem] p-8 lg:p-12 overflow-hidden shadow-2xl mb-10">
            <div class="relative z-10 flex flex-col lg:flex-row justify-between items-center gap-8">

                <div class="max-w-xl text-center lg:text-left">

                    <span class="text-indigo-400 text-[10px] font-black uppercase tracking-[0.3em] mb-4 block">
                        Student Overview
                    </span>

                    <h1 class="text-3xl lg:text-5xl font-black text-black leading-tight mb-4">
                        Welcome back, <br />

                        <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">
                            {{ profileData?.firstName || 'Scholar' }}!
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
                <Attendance />
                <StopWatch />
                <BookRecommendetion :recommendedBooks="recommendedBooks" />
                <CampusNotice :notices="notices" />
                <AcademicCalendar />
                <Event />
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

const { dashboardData, loading, error, loadDashboard } = useStudentDashboard()
const showModal = ref(false)

/* PROGRAM DATA */

// const programData = ref({
//     name: 'Computer Science',
//     semester: 'Semester 3',
//     endDate: 'June 24 2026'
// })
const programData = computed(() => {
    const studentInfo = dashboardData.value?.student_info

    return studentInfo ? {
        name: studentInfo.program,
        semester: studentInfo.semester,
        endDate: "June 24, 2026",
        daysRemaining: 112,
        description: "A comprehensive program focusing on the intersection of visual design, user experience research, and modern front-end engineering frameworks.",
        subjects: dashboardData.value?.courses?.map(c => ({
            code: c.code,
            title: c.name,
            credits: 1
        })) || []
    } : {}
})


/* TODAY CLASSES */

const todayClasses = ref([
    {
        subject: 'Mathematics',
        time: '09:00 AM',
        room: '204'
    },
    {
        subject: 'Physics',
        time: '11:00 AM',
        room: '105'
    },
    {
        subject: 'Computer Science',
        time: '02:00 PM',
        room: 'Lab 3'
    }
])


/* UPCOMING EXAMS */

const upcomingExams = ref([
    {
        subject: 'Mathematics',
        date: '12 May'
    },
    {
        subject: 'Physics',
        date: '18 May'
    },
    {
        subject: 'Computer Science',
        date: '21 May'
    }
])

const notices = [
    { id: 1, title: 'Library Hours Updated', desc: 'Open until 11:00 PM during exam week.', dotColor: 'bg-green-500' },
    { id: 2, title: 'New Sports Club Registration', desc: 'Sign up via the portal by Friday.', dotColor: 'bg-indigo-500' },
]
/* BOOKS */

const recommendedBooks = ref([
    {
        title: 'Clean Code',
        author: 'Robert C. Martin',
        cover: 'https://m.media-amazon.com/images/I/41xShlnTZTL.jpg'
    },
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


const assignments = ref([
    {
        title: 'Algorithm Analysis Report',
        subject: 'Computer Science',
        deadline: 'Due May 15'
    },
    {
        title: 'Physics Lab Report',
        subject: 'Physics',
        deadline: 'Due May 18'
    },
    {
        title: 'Linear Algebra Worksheet',
        subject: 'Mathematics',
        deadline: 'Due May 20'
    }
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

.transition-all {
    transition: all .3s cubic-bezier(.4, 0, .2, 1);
}
</style>