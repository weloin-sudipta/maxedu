<template>
    <div class="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">

        <!-- PINNED NOTICE -->
        <div
            class="relative bg-indigo-600 rounded-[3rem] p-10 overflow-hidden shadow-2xl shadow-indigo-200 h-[350px] flex items-center">

            <div class="absolute top-0 left-0 h-1 bg-white/30 transition-all duration-[3000ms] ease-linear"
                :style="{ width: progressBarWidth + '%' }" :key="currentIndex">
            </div>

            <TransitionGroup name="slide-fade" tag="div">
                <div v-for="(notice, index) in pinNotices" :key="notice.id" v-show="index === currentIndex"
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

                        <button
                            class="mt-8 px-8 py-3 bg-white text-indigo-600 rounded-2xl text-[10px] font-black uppercase tracking-widest hover:scale-105 transition-transform"
                            @click="goToNotice(notice.slug)">
                            View Details
                        </button>

                    </div>

                    <i :class="['fa', notice.icon || 'fa-bullhorn']"
                        class="text-[8rem] opacity-10 -rotate-12 absolute -right-4 -bottom-4">
                    </i>

                </div>
            </TransitionGroup>

        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

            <!-- NOTICES -->
            <div class="lg:col-span-8 space-y-6">

                <!-- TAG FILTER -->
                <div class="flex gap-2 overflow-x-auto no-scrollbar pb-2">
                    <button v-for="tag in tags" :key="tag" @click="selectedTag = tag"
                        :class="[
                            selectedTag === tag 
                                ? 'border-indigo-400 text-indigo-600 bg-indigo-50' 
                                : 'border-slate-200 text-slate-500 bg-white',
                            'px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest border hover:border-indigo-400 transition-all'
                        ]">
                        {{ tag }}
                    </button>
                </div>

                <!-- NOTICE GRID -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

                    <div v-for="notice in filteredNotices" :key="notice.id"
                        class="bg-white border-2 border-slate-100 rounded-[2.5rem] p-8 flex flex-col group shadow-md hover:shadow-xl transition-shadow">

                        <div class="flex justify-between items-start mb-6">

                            <div
                                class="w-10 h-10 bg-indigo-500 rounded-xl flex items-center justify-center text-white shadow-lg">
                                <i :class="['fa', notice.icon || 'fa-bullhorn']"></i>
                            </div>

                            <span
                                class="bg-indigo-50 text-indigo-600 px-4 py-1 rounded-full text-[10px] font-black uppercase tracking-widest">
                                {{ notice.category || notice.type }}
                            </span>

                        </div>

                        <h3 class="text-xl font-black text-slate-900 mb-2">
                            {{ notice.title }}
                        </h3>

                        <p class="text-slate-500 text-sm mb-4 line-clamp-2">
                            {{ notice.description }}
                        </p>

                        <span class="text-[10px] font-black text-slate-400 mb-2">
                            {{ notice.date }}
                        </span>

                        <button
                            class="mt-auto px-6 py-2 bg-indigo-600 text-white rounded-xl text-[10px] font-black uppercase tracking-widest hover:scale-105 transition-transform"
                            @click="goToNotice(notice.slug)">
                            View Details
                        </button>

                    </div>

                </div>

                <!-- NEWS SECTION -->
                <div class="space-y-4">

                    <h3 class="text-xs font-black uppercase tracking-widest text-slate-400">
                        Latest News
                    </h3>

                    <div v-for="item in news" :key="item.id"
                        class="bg-white border border-slate-200/60 rounded-[2.5rem] p-6 shadow-sm hover:shadow-md transition-all border-b-4 border-b-indigo-500">

                        <div class="flex items-center gap-4 mb-3">

                            <div
                                class="w-10 h-10 bg-slate-50 rounded-xl flex items-center justify-center text-indigo-600">
                                <i class="fa fa-newspaper-o"></i>
                            </div>

                            <h3 class="text-sm font-black text-slate-800">
                                {{ item.title }}
                            </h3>

                        </div>

                        <p class="text-xs text-slate-500">
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
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNotices } from '~/composable/useNotices'

const router = useRouter()

const { pinNotices, tags, news, topics, selectedTag, filteredNotices, fetchNotices } = useNotices()

const currentIndex = ref(0)
const progressBarWidth = ref(0)
let timer = null

const startTimer = () => {
  progressBarWidth.value = 0
  setTimeout(() => { progressBarWidth.value = 100 }, 50)

  timer = setInterval(() => {
    if (!pinNotices.value || pinNotices.value.length === 0) return
    currentIndex.value = (currentIndex.value + 1) % pinNotices.value.length
    progressBarWidth.value = 0
    setTimeout(() => { progressBarWidth.value = 100 }, 50)
  }, 6000)
}

function goToNotice(slug) {
  if (!slug) return
  router.push(`/notices/${slug}`)
}

onMounted(() => {
  startTimer()
  fetchNotices()
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>