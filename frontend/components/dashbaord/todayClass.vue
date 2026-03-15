<template>
    <div class="space-y-6">

        <div class="flex items-center justify-between px-2">
            <h3 class="text-xl font-black text-slate-800 tracking-tight">
                Today's Schedule
            </h3>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

            <div v-for="(cls, i) in todayClasses" :key="i"
                class="bg-white p-5 rounded-[2rem] border border-slate-100 flex items-center gap-4 hover:shadow-xl transition-all">

                <div class="w-12 h-12 rounded-2xl bg-slate-50 flex flex-col items-center justify-center">

                    <i class="fa fa-clock-o text-xs"></i>
                    <span class="text-[8px] font-black uppercase">
                        Live
                    </span>

                </div>

                <div>
                    <h4 class="text-sm font-black text-slate-800">
                        {{ cls.subject }}
                    </h4>

                    <p class="text-[10px] font-bold text-slate-400 uppercase">
                        {{ cls.time }} • Room {{ cls.room }}
                    </p>

                </div>

            </div>

        </div>

    </div>
</template>

<script setup>
const props = defineProps(['todayClasses']);

</script>