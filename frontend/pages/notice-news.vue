<template>
    <div class="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">

        <!-- PINNED NOTICE -->
        <div
                    class="relative bg-indigo-600 rounded-[3rem] p-10 overflow-hidden shadow-2xl shadow-indigo-200 h-[350px] flex items-center">
                    <div class="absolute top-0 left-0 h-1 bg-white/30 transition-all duration-[3000ms] ease-linear"
                        :style="{ width: progressBarWidth + '%' }" :key="currentIndex"></div>

                    <TransitionGroup name="slide-fade">
                        <div v-for="(notice, index) in pinNotices" :key="notice.id">
                            <div v-if="index === currentIndex"
                                class="relative z-10 flex flex-col md:flex-row justify-between items-center gap-6 text-white">
                                <div class="max-w-xl">
                                    <span
                                        class="bg-white/20 backdrop-blur-md px-4 py-1 rounded-full text-[10px] font-black uppercase tracking-widest">
                                        Pin of the day • {{ index + 1 }}/{{ pinNotices.length }}
                                    </span>

                                    <h2 class="text-3xl font-black mt-4 leading-tight">
                                        {{ notice.title }}
                                    </h2>

                                    <p class="mt-4 text-indigo-100/80 text-sm font-medium line-clamp-2">
                                        {{ notice.description }}
                                    </p>

                                    <button v-if="notice.link"
                                        class="mt-8 px-8 py-3 bg-white text-indigo-600 rounded-2xl text-[10px] font-black uppercase tracking-widest hover:scale-105 transition-transform">
                                        View Details
                                    </button>
                                </div>
                                <i :class="['fa', notice.icon || 'fa-bullhorn']"
                                    class="text-[8rem] opacity-10 -rotate-12 absolute -right-4 -bottom-4"></i>
                            </div>
                        </div>
                    </TransitionGroup>
                </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

            <!-- NOTICES -->
            <div class="lg:col-span-8 space-y-6">

                <div class="flex gap-2 overflow-x-auto no-scrollbar pb-2">
                    <button v-for="tag in tags" :key="tag"
                        class="px-6 py-2 bg-white rounded-xl text-[10px] font-black uppercase tracking-widest border border-slate-200 text-slate-500 hover:border-indigo-400 transition-all">
                        {{ tag }}
                    </button>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

                    <!-- NOTICE CARD -->
                    <div v-for="notice in notices" :key="notice.id"
                        class="bg-rose-50 border-2 border-rose-100 rounded-[2.5rem] p-8 flex flex-col group">

                        <div class="flex justify-between items-start mb-6">
                            <div
                                class="w-10 h-10 bg-rose-500 rounded-xl flex items-center justify-center text-white shadow-lg shadow-rose-200">
                                <i class="fa fa-bullhorn"></i>
                            </div>

                            <span class="text-[9px] font-black text-rose-500 uppercase tracking-widest">
                                Notice
                            </span>
                        </div>

                        <h3 class="text-lg font-black text-slate-800 leading-tight">
                            {{ notice.title }}
                        </h3>

                        <p class="text-xs text-slate-500 mt-4 flex-grow">
                            {{ notice.description }}
                        </p>

                        <div class="mt-8">
                            <span class="text-[10px] font-black text-slate-400">
                                {{ notice.date }}
                            </span>
                        </div>

                    </div>

                    <!-- NEWS CARD -->
                    <div v-for="item in news" :key="item.id"
                        class="bg-white border border-slate-200/60 rounded-[2.5rem] p-8 shadow-sm hover:shadow-md transition-all border-b-4 border-b-indigo-500">

                        <div class="flex items-center gap-4 mb-4">

                            <div
                                class="w-12 h-12 bg-slate-50 rounded-2xl flex items-center justify-center text-indigo-600">
                                <i class="fa fa-newspaper-o text-xl"></i>
                            </div>

                            <div>
                                <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest">
                                    News
                                </p>

                                <h3 class="text-sm font-black text-slate-800">
                                    {{ item.title }}
                                </h3>
                            </div>
                        </div>

                        <p class="text-xs text-slate-500 leading-relaxed">
                            {{ item.description }}
                        </p>

                    </div>

                </div>
            </div>

            <!-- SIDEBAR -->
            <div class="lg:col-span-4 space-y-6">

                <!-- TRENDING -->
                <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm">

                    <h3 class="text-xs font-black uppercase tracking-widest text-slate-400 mb-6">
                        Trending Topics
                    </h3>

                    <div class="space-y-4">

                        <div v-for="topic in topics" :key="topic"
                            class="p-4 bg-slate-50 rounded-2xl flex justify-between items-center group cursor-pointer hover:bg-indigo-50 transition-all">

                            <span class="text-xs font-bold text-slate-700 group-hover:text-indigo-600">
                                {{ topic }}
                            </span>

                            <i class="fa fa-arrow-right text-[10px] text-slate-300 group-hover:text-indigo-600"></i>

                        </div>

                    </div>
                </div>

                <!-- SUBMIT NOTICE -->
                <div class="bg-slate-900 rounded-[2.5rem] p-8 text-white">

                    <p class="text-[9px] font-black text-indigo-400 uppercase tracking-widest mb-2">
                        Need to post?
                    </p>

                    <h3 class="text-lg font-bold">
                        Submit a Notice
                    </h3>

                    <p class="text-xs text-slate-400 mt-2 leading-relaxed">
                        All submissions must be approved by the admin before appearing here.
                    </p>

                </div>

            </div>

        </div>
    </div>
</template>

<script setup>

import { ref, onMounted, onUnmounted } from 'vue';

const currentIndex = ref(0);
const progressBarWidth = ref(0);
let timer = null;

// Sample data for 5 pin notices
const pinNotices = ref([
    { id: 1, title: 'Annual Cultural Fest 2026', description: 'Neon Dreams registrations are now live! Join us for music and art.', link: '#', icon: 'fa-rocket' },
    { id: 2, title: 'Mid-Term Break Announcement', description: 'School will remain closed from Oct 15th to Oct 20th for autumn break.', link: '#', icon: 'fa-sun-o' },
    { id: 3, title: 'New Library Books Arrived', description: 'Over 200 new titles added to the science and fiction sections.', link: '#', icon: 'fa-book' },
    { id: 4, title: 'Sports Meet Selection', description: 'Football trials for the senior team start this Friday at 4 PM.', link: '#', icon: 'fa-trophy' },
    { id: 5, title: 'Cafeteria Menu Update', description: 'Check out our new healthy organic meal plans starting next Monday.', link: '#', icon: 'fa-cutlery' }
]);

const startTimer = () => {
    timer = setInterval(() => {
        // Reset progress bar
        progressBarWidth.value = 0;

        // Increment index or loop back to 0
        if (currentIndex.value < pinNotices.value.length - 1) {
            currentIndex.value++;
        } else {
            currentIndex.value = 0;
        }
    }, 3000);
};

onMounted(() => {
    startTimer();
    // Small delay to trigger the progress bar animation
    setTimeout(() => progressBarWidth.value = 100, 50);
});

onUnmounted(() => {
    clearInterval(timer);
});

const tags = ["All Notices", "Academic", "Sports", "Admin"]

const notices = [
    {
        id: 1,
        title: "Mid-Term Revision Classes Schedule",
        description: "Remedial classes will start tomorrow in Block C auditorium.",
        date: "12 Mar 2026"
    },
    {
        id: 2,
        title: "Library Timing Changed",
        description: "Library will remain open till 8PM from Monday.",
        date: "11 Mar 2026"
    }
]

const news = [
    {
        id: 1,
        title: "50 New AI Books Added",
        description: "Library has added new AI and Machine Learning books."
    },
    {
        id: 2,
        title: "Digital Reading Portal Launched",
        description: "Students can now read books online from the portal."
    }
]

const topics = ["#ExamPrep", "#LibraryUpdate", "#CampusFest"]

</script>