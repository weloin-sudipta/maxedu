<template>

    <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm relative overflow-hidden group">

        <div class="flex items-center justify-between mb-8 relative z-10">
            <div>
                <h3 class="text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 mb-1">
                    Mission Control
                </h3>
                <p class="text-xl font-black text-slate-800 tracking-tight">Assignment Deadlines</p>
            </div>
            <div class="flex flex-col items-end">
                <span
                    class="px-3 py-1 bg-indigo-50 text-indigo-600 rounded-full text-[10px] font-black uppercase tracking-widest border border-indigo-100">
                    {{ assignments.length }} Active
                </span>
            </div>
        </div>

        <div class="space-y-4 relative z-10">
            <div v-for="(a, index) in assignments" :key="a.title"
                class="relative flex items-center gap-5 p-5 rounded-[2rem] transition-all duration-500 group/item cursor-pointer border"
                :class="[
                    index === 0
                        ? 'bg-slate-900 border-slate-800 shadow-xl shadow-slate-200'
                        : 'bg-white border-slate-100 hover:border-indigo-200 hover:bg-slate-50/50'
                ]">

                <div class="relative shrink-0">
                    <div class="w-14 h-14 rounded-2xl flex items-center justify-center transition-transform group-hover/item:rotate-12"
                        :class="index === 0 ? 'bg-indigo-500 text-white' : 'bg-slate-100 text-slate-400'">
                        <i class="fa fa-calendar-check-o text-xl"></i>
                    </div>
                    <div v-if="index === 0"
                        class="absolute -top-2 -right-2 w-6 h-6 bg-rose-500 rounded-full border-4 border-slate-900 flex items-center justify-center">
                        <div class="w-1.5 h-1.5 bg-white rounded-full animate-ping"></div>
                    </div>
                </div>

                <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2 mb-1">
                        <span :class="index === 0 ? 'text-indigo-400' : 'text-indigo-600'"
                            class="text-[9px] font-black uppercase tracking-widest">
                            {{ a.subject }}
                        </span>
                    </div>
                    <h4 :class="index === 0 ? 'text-white' : 'text-slate-800'" class="text-sm font-black truncate">
                        {{ a.title }}
                    </h4>

                    <div class="flex items-center gap-3 mt-3">
                        <div class="flex-1 h-1 rounded-full bg-slate-200 overflow-hidden">
                            <div :class="index === 0 ? 'bg-indigo-400' : 'bg-indigo-600'" class="h-full rounded-full"
                                :style="{ width: getUrgencyPercentage(a.deadline) + '%' }"></div>
                        </div>
                        <span :class="index === 0 ? 'text-slate-400' : 'text-rose-500'"
                            class="text-[10px] font-black uppercase whitespace-nowrap">
                            {{ a.deadline }}
                        </span>
                    </div>
                </div>

                <div class="opacity-0 group-hover/item:opacity-100 transition-opacity">
                    <i :class="index === 0 ? 'text-white' : 'text-slate-300'" class="fa fa-chevron-right"></i>
                </div>
            </div>
        </div>

        <div
            class="absolute -right-10 -bottom-10 w-32 h-32 bg-slate-50 rounded-full blur-3xl group-hover:bg-indigo-50 transition-colors">
        </div>
    </div>


</template>

<script setup>
const props = defineProps(['assignments']);
// Helper to visually represent "how close" the deadline is (Mock logic)
const getUrgencyPercentage = (deadline) => {
    if (deadline.includes('Hours')) return 90;
    if (deadline.includes('Tomorrow')) return 70;
    return 40;
};
</script>


