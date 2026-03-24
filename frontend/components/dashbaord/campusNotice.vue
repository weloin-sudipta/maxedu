<template>
    <div class="bg-white rounded-[2rem] border border-slate-100 shadow-sm p-6 flex flex-col gap-5">

        <!-- HEADER -->
        <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-gradient-to-br from-indigo-500 to-indigo-400 rounded-[0.85rem] flex items-center justify-center text-white text-sm shadow-lg shadow-indigo-200">
                    <i class="fa fa-bell"></i>
                </div>
                <div>
                    <h6 class="text-sm font-black text-slate-800 leading-tight tracking-tight">Campus Notices</h6>
                    <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Latest updates</span>
                </div>
            </div>
            <NuxtLink to="/notices"
                class="text-[10px] font-black text-indigo-600 uppercase tracking-widest bg-indigo-50 hover:bg-indigo-100 transition-colors px-3 py-1.5 rounded-full flex items-center gap-1.5">
                View all <i class="fa fa-arrow-right text-[9px]"></i>
            </NuxtLink>
        </div>

        <!-- LIST -->
        <div v-if="notices && notices.length > 0" class="flex flex-col">
            <div v-for="(notice, index) in notices" :key="notice.id"
                class="flex items-start gap-3 py-3 group cursor-pointer"
                @click="goToNotice(notice.slug)">  <!-- ✅ -->

                <!-- DOT + LINE -->
                <div class="flex flex-col items-center flex-shrink-0 w-4 pt-1">
                    <div class="relative w-3.5 h-3.5 flex-shrink-0">
                        <div class="absolute inset-0 rounded-full border-2 border-slate-200"></div>
                        <div class="absolute inset-[3px] rounded-full" :class="notice.dotColor || 'bg-indigo-500'"></div>
                    </div>
                    <div v-if="index < notices.length - 1"
                        class="w-px flex-1 min-h-[20px] mt-1 bg-gradient-to-b from-slate-200 to-transparent"></div>
                </div>

                <!-- CONTENT -->
                <div class="flex-1 min-w-0">
                    <p class="text-[13px] font-black text-slate-800 group-hover:text-indigo-600 transition-colors truncate leading-tight mb-0.5">
                        {{ notice.title }}
                    </p>
                    <p class="text-[11px] text-slate-400 leading-relaxed line-clamp-2">
                        {{ notice.desc || notice.description }}
                    </p>
                    <span v-if="notice.category"
                        class="inline-block mt-1.5 text-[9px] font-black uppercase tracking-widest text-indigo-500 bg-indigo-50 px-2 py-0.5 rounded-full">
                        {{ notice.category }}
                    </span>
                </div>

                <!-- ARROW -->
                <i class="fa fa-chevron-right text-[10px] text-slate-300 group-hover:text-indigo-400 group-hover:translate-x-0.5 transition-all pt-1 flex-shrink-0"></i>

            </div>
        </div>

        <!-- EMPTY STATE -->
        <div v-else class="flex flex-col items-center gap-2 py-8 text-slate-300">
            <i class="fa fa-bell-slash-o text-2xl"></i>
            <p class="text-[10px] font-black uppercase tracking-widest">No notices right now</p>
        </div>

    </div>
</template>

<script setup>
import { useRouter } from 'vue-router' 

const props = defineProps(['notices'])

const router = useRouter()  

function goToNotice(slug) { 
    if (!slug) return
    router.push(`/notices/${slug}`)
}
</script>