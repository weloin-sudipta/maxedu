<template>
    <div class="space-y-6">

        <div class="flex items-center justify-between px-2">
            <h3 class="text-xl font-black text-slate-800 dark:text-white tracking-tight">
                Today's Schedule
            </h3>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

            <div v-for="(cls, i) in todayClasses" :key="i"
                class="bg-white dark:bg-slate-900 p-5 rounded-[2rem] border border-slate-100 dark:border-slate-800 flex items-center gap-4 hover:shadow-xl dark:shadow-none transition-all">

                <div class="w-12 h-12 rounded-2xl bg-slate-50 dark:bg-slate-800/50 flex flex-col items-center justify-center">

                    <i class="fa fa-clock-o text-xs text-slate-500 dark:text-slate-400"></i>
                    <span class="text-[8px] font-black uppercase text-slate-500 dark:text-slate-400">
                        Live
                    </span>

        </div>

                <div>
                    <h4 class="text-sm font-black text-slate-800 dark:text-slate-200">
                        {{ cls.subject }}
                    </h4>

                    <p class="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase">
                        {{ cls.time }} • Room {{ cls.room }}
                    </p>

                </div>

        <!-- LIVE PING DECORATION -->
        <div v-if="getStatus(cls) === 'live'"
          class="absolute top-3 right-3 w-2 h-2">
          <span class="absolute inset-0 rounded-full bg-green-400 animate-ping opacity-75"></span>
          <span class="absolute inset-0 rounded-full bg-green-500"></span>
        </div>

      </div>
    </div>

    <!-- EMPTY STATE -->
    <div v-else class="bg-white rounded-[2rem] border border-dashed border-slate-200 p-12 flex flex-col items-center gap-2 text-slate-300">
      <i class="fa fa-coffee text-2xl"></i>
      <p class="text-[10px] font-black uppercase tracking-widest">No classes today</p>
    </div>

  </div>
</template>

<script setup>
const props = defineProps(['todayClasses'])

const getStatus = (cls) => {
  const now = new Date()
  const toMinutes = (t) => {
    if (!t) return null
    const [h, m] = t.split(':').map(Number)
    return h * 60 + m
  }

  const start = toMinutes(cls.startTime || cls.time)
  const end   = toMinutes(cls.endTime)
  const curr  = now.getHours() * 60 + now.getMinutes()

  if (start === null) return 'upcoming'
  if (end && curr > end) return 'done'
  if (curr >= start && (!end || curr <= end)) return 'live'
  return 'upcoming'
}
</script>