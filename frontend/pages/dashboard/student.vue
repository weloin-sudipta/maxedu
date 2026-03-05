<template>
    <main class="flex-1 overflow-y-auto p-6 pt-4 custom-scrollbar">
        <div class="mb-6 grid grid-cols-1 md:grid-cols-12 gap-6 bg-transparent">
            <div
                class="col-span-12 md:col-span-8 border-b md:border-b-0 md:border-r border-gray-200 pb-6 md:pb-0 md:pr-6">
                <h5 class="text-xl text-gray-600 mb-2">Welcome back, <span class="font-semibold text-gray-900">{{ profileData?.firstName || 'User' }} {{
                        profileData?.lastName || '' }}
                        👋🏻</span></h5>
                <p class="text-gray-500 max-w-md mb-6">Your progress this week is Awesome. let's keep it up and get a
                    lot of points reward!</p>

                <div class="flex flex-wrap gap-6">
                    <div class="flex items-center gap-4">
                        <div class="w-12 h-12 flex items-center justify-center bg-indigo-100 rounded-lg">
                            <img src="/laptop.svg" alt="Laptop Icon" class="w-6 h-6" />
                        </div>
                        <div>
                            <p class="text-sm font-medium text-gray-500">Hours Spent</p>
                            <h5 class="text-indigo-600 font-bold text-lg">34h</h5>
                        </div>
                    </div>
                    <div class="flex items-center gap-4">
                        <div class="w-12 h-12 flex items-center justify-center bg-cyan-100 rounded-lg">
                            <img src="/lightbulb.svg" alt="Lightbulb Icon" class="w-6 h-6" />
                        </div>
                        <div>
                            <p class="text-sm font-medium text-gray-500">Test Results</p>
                            <h5 class="text-cyan-600 font-bold text-lg">82%</h5>
                        </div>
                    </div>
                    <div class="flex items-center gap-4">
                        <div class="w-12 h-12 flex items-center justify-center bg-orange-100 rounded-lg">
                            <img src="/check.svg" alt="Check Icon" class="w-6 h-6" />
                        </div>
                        <div>
                            <p class="text-sm font-medium text-gray-500">Course Completed</p>
                            <h5 class="text-orange-600 font-bold text-lg">14</h5>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-span-12 md:col-span-4 md:pl-6 flex items-center justify-between">
                <div>
                    <h5 class="font-semibold text-gray-800 mb-1">Time Spendings</h5>
                    <p class="text-gray-400 text-sm mb-4">Weekly report</p>
                    <div class="flex items-center gap-2">
                        <h5 class="text-xl font-bold">231<span class="text-gray-400 font-normal">h</span> 14<span
                                class="text-gray-400 font-normal">m</span></h5>
                        <span
                            class="px-2 py-0.5 text-xs font-semibold text-green-600 bg-green-100 rounded-full">+18.4%</span>
                    </div>
                </div>
                <div id="leadsReportChart"
                    class="w-32 h-32 bg-gray-50 rounded-full border-4 border-indigo-50"></div>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-12 gap-6">

            <div class="col-span-12 md:col-span-8 bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                <div class="p-5 border-b border-gray-50 flex justify-between items-center bg-indigo-50/30">
                    <div>
                        <h6 class="font-bold text-gray-800">My Current Program</h6>
                        <p class="text-xs text-gray-500">Academic Year 2025-2026</p>
                    </div>
                    <button @click="showModal = true"
                        class="bg-indigo-600 text-white px-4 py-1.5 rounded-lg text-xs font-bold hover:bg-indigo-700 transition-all shadow-md">
                        View Full Details
                    </button>
                </div>
                <div class="p-5 grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="space-y-3">
                        <p class="text-lg font-bold text-gray-900 leading-tight">{{ programData.name }}</p>
                        <div class="flex items-center gap-2 text-sm text-gray-600">
                            <span class="px-2 py-0.5 bg-gray-100 rounded text-xs">Full-Time</span>
                            <span>Semester {{ programData.semester }}</span>
                        </div>
                        <div class="mt-4">
                            <div class="flex justify-between text-xs mb-1">
                                <span class="text-gray-500">Curriculum Progress</span>
                                <span class="font-bold text-indigo-600">78%</span>
                            </div>
                            <div class="w-full bg-gray-100 h-2 rounded-full">
                                <div class="bg-indigo-500 h-2 rounded-full" style="width: 78%"></div>
                            </div>
                        </div>
                    </div>
                    <div
                        class="bg-orange-50 border border-orange-100 rounded-xl p-4 flex flex-col justify-center items-center text-center">
                        <p class="text-[10px] uppercase font-bold text-orange-400 mb-1">Course Completion Date</p>
                        <p class="text-lg font-bold text-orange-700">{{ programData.endDate }}</p>
                        <div
                            class="mt-2 text-[10px] px-3 py-1 bg-white text-orange-600 rounded-full font-bold shadow-sm">
                            {{ programData.daysRemaining }} Days Remaining
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-span-12 md:col-span-4 space-y-6">
                <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
                    <h6 class="font-bold text-gray-800 mb-4 flex items-center gap-2">
                        <i class="fa fa-file-text-o text-orange-500"></i> Upcoming Exams
                    </h6>
                    <div v-for="exam in exams" :key="exam.id"
                        class="mb-3 last:mb-0 p-3 bg-orange-50 rounded-lg border border-orange-100">
                        <div class="flex justify-between items-start">
                            <div>
                                <p class="text-sm font-bold text-orange-900">{{ exam.title }}</p>
                                <p class="text-xs text-orange-700">{{ exam.date }}</p>
                            </div>
                            <span class="text-[10px] bg-orange-200 text-orange-800 px-2 py-1 rounded">{{ exam.daysLeft
                                }} days left</span>
                        </div>
                    </div>
                </div>

            </div>

            <div class="col-span-12 md:col-span-4 bg-white p-5 rounded-xl shadow-sm border border-gray-100">
                <div class="flex justify-between items-center mb-4">
                    <h6 class="font-bold text-gray-800">Today's Classes</h6>
                    <span class="text-indigo-600 text-xs font-semibold cursor-pointer">View Schedule</span>
                </div>
                <div class="space-y-4">
                    <div v-for="(cls, i) in todayClasses" :key="i"
                        class="flex gap-4 p-3 rounded-lg hover:bg-gray-50 transition-colors border-l-4"
                        :class="cls.color">
                        <div class="flex-1">
                            <p class="text-sm font-bold text-gray-800">{{ cls.subject }}</p>
                            <p class="text-xs text-gray-500">{{ cls.time }} • Room {{ cls.room }}</p>
                        </div>
                        <div class="text-right">
                            <span
                                class="text-[10px] font-bold px-2 py-1 bg-white rounded shadow-sm border border-gray-100">{{
                                    cls.type }}</span>
                        </div>
                    </div>
                </div>
            </div>


            <div class="col-span-12 md:col-span-4 space-y-6">
                <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
                    <h6 class="font-bold text-gray-800 mb-4 flex items-center gap-2">
                        <i class="fa fa-tasks text-blue-500"></i> Assignment Deadlines
                    </h6>
                    <div v-for="task in assignments" :key="task.id" class="flex items-center gap-3 mb-4">
                        <div class="w-2 h-2 rounded-full bg-blue-500"></div>
                        <div class="flex-1">
                            <p class="text-sm text-gray-700 font-medium">{{ task.name }}</p>
                            <div class="w-full bg-gray-100 h-1.5 rounded-full mt-1">
                                <div class="bg-blue-500 h-1.5 rounded-full" :style="{ width: task.progress + '%' }">
                                </div>
                            </div>
                        </div>
                        <p class="text-[10px] font-bold text-gray-400">{{ task.due }}</p>
                    </div>
                </div>
                <!-- <div class="bg-gradient-to-r from-red-500 to-pink-600 p-5 rounded-xl shadow-md text-white">
                    <div class="flex justify-between items-center mb-2">
                        <p class="text-xs uppercase font-bold opacity-80">Fee Reminder</p>
                        <i class="fa fa-exclamation-triangle"></i>
                    </div>
                    <h4 class="text-2xl font-bold">$1,250.00</h4>
                    <p class="text-xs mt-1">Due Date: March 15, 2026</p>
                    <button
                        class="mt-4 w-full bg-white text-red-600 py-2 rounded-lg font-bold text-sm shadow-sm hover:bg-gray-100 transition-colors">
                        Pay Now
                    </button>
                </div> -->

            </div>

            <div class="col-span-12 md:col-span-4 space-y-6">

                <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
                    <h6 class="font-bold text-gray-800 mb-4">Campus Notices</h6>
                    <div class="relative pl-6 border-l-2 border-gray-100 space-y-6">
                        <div v-for="notice in notices" :key="notice.id" class="relative">
                            <div class="absolute -left-[31px] top-1 w-4 h-4 rounded-full border-4 border-white"
                                :class="notice.dotColor"></div>
                            <p class="text-xs font-bold text-gray-800">{{ notice.title }}</p>
                            <p class="text-[11px] text-gray-500 mt-1">{{ notice.desc }}</p>
                        </div>
                    </div>
                </div>

                <div class="bg-indigo-900 p-5 rounded-xl shadow-sm text-white relative overflow-hidden">
                    <div class="relative z-10">
                        <h6 class="font-bold mb-1">Annual Tech Fest</h6>
                        <p class="text-xs opacity-70 mb-4">Join the biggest event of the year.</p>
                        <div class="flex -space-x-2">
                            <img v-for="i in 4" :key="i" :src="`https://i.pravatar.cc/100?img=${i + 10}`"
                                class="w-8 h-8 rounded-full border-2 border-indigo-900" />
                            <div
                                class="w-8 h-8 rounded-full bg-indigo-700 border-2 border-indigo-900 flex items-center justify-center text-[10px] font-bold">
                                +12</div>
                        </div>
                    </div>
                    <i class="fa fa-calendar absolute -right-4 -bottom-4 text-8xl text-white opacity-10"></i>
                </div>
            </div>

        </div>

        <AppModal v-model="showModal" title="Program Curriculum">

            <div class="mb-6">
                <p class="text-sm text-gray-500 uppercase font-bold tracking-widest mb-2">
                    About this Program
                </p>
                <p class="text-gray-700 leading-relaxed">
                    {{ programData.description }}
                </p>
            </div>

            <div class="space-y-4">
                <p class="text-sm text-gray-500 uppercase font-bold tracking-widest">
                    Enrolled Subjects
                </p>

                <div v-for="sub in programData.subjects" :key="sub.code"
                    class="flex justify-between items-center p-4 bg-gray-50 rounded-xl border border-gray-100">
                    <div>
                        <p class="font-bold text-gray-800">{{ sub.title }}</p>
                        <p class="text-xs text-gray-500">
                            {{ sub.code }} • {{ sub.credits }} Credits
                        </p>
                    </div>
                    <span class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-[10px] font-bold">
                        In Progress
                    </span>
                </div>
            </div>

            <!-- Footer Slot -->
            <template #footer>
                <button @click="showModal = false"
                    class="bg-gray-800 text-white px-6 py-2 rounded-xl font-bold text-sm">
                    Close
                </button>
            </template>

        </AppModal>
    </main>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import ApexCharts from 'apexcharts'
import AppModal from '~/components/ui/AppModal.vue'
import { useUserProfile } from '~/composable/useUserProfile'

const { profileData } = useUserProfile()
const showModal = ref(false)
const programData = ref({
    name: "Bachelor of Science in UI/UX Design & Development",
    semester: "4th Semester",
    endDate: "June 24, 2026",
    daysRemaining: 112,
    description: "A comprehensive program focusing on the intersection of visual design, user experience research, and modern front-end engineering frameworks.",
    subjects: [
        { code: "CS401", title: "Advanced User Research", credits: 4 },
        { code: "DS202", title: "Design Systems & Components", credits: 3 },
        { code: "FE305", title: "Vue.js Framework Mastery", credits: 5 },
        { code: "MT101", title: "Quantitative Design Analysis", credits: 3 }
    ]
})

const todayClasses = [
    { subject: 'Advanced Mathematics', time: '09:00 AM', room: '302-A', color: 'border-indigo-500' },
    { subject: 'UI/UX Design Principles', time: '11:30 AM', room: 'Lab 04', color: 'border-cyan-500' },
    { subject: 'Database Management', time: '02:00 PM', room: '201-B', color: 'border-orange-500' },
]

const exams = [
    { id: 1, title: 'Data Structures Mid-Term', date: 'March 06, 2026', daysLeft: 2 },
    { id: 2, title: 'English Literature Proficiency', date: 'March 12, 2026', daysLeft: 8 },
]

const assignments = [
    { id: 1, name: 'Marketing Research Paper', progress: 75, due: 'Tomorrow' },
    { id: 2, name: 'Figma Dashboard Prototype', progress: 40, due: 'Fri' },
]

const notices = [
    { id: 1, title: 'Library Hours Updated', desc: 'Open until 11:00 PM during exam week.', dotColor: 'bg-green-500' },
    { id: 2, title: 'New Sports Club Registration', desc: 'Sign up via the portal by Friday.', dotColor: 'bg-indigo-500' },
]
onMounted(() => {
    const options = {
        series: [23, 35, 10, 20, 35, 23],
        chart: {
            type: 'donut',
            height: 140
        },
        colors: [
            '#5BB420',
            '#67CB24',
            '#72E128',
            '#8EE753',
            '#AAED7E',
            '#C7F3A9'
        ],
        dataLabels: {
            enabled: false
        },
        legend: {
            show: false
        },
        stroke: {
            width: 0
        },
        plotOptions: {
            pie: {
                donut: {
                    size: '65%',
                    labels: {
                        show: true,
                        total: {
                            show: true,
                            label: 'Total',
                            formatter: () => '231h'
                        }
                    }
                }
            }
        }
    }

    const chart = new ApexCharts(
        document.querySelector("#leadsReportChart"),
        options
    )

    chart.render()
})
</script>

<style>
/* Exact Sneat Color Matches */
body {
    background-color: #f5f5f9;
}

.custom-scrollbar::-webkit-scrollbar {
    width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #d9dee3;
    border-radius: 10px;
}
</style>