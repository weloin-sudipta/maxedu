<template>
  <div class="space-y-6 animate-in fade-in duration-500">

    <div v-if="loading" class="text-center py-12">
      <i class="fa fa-spinner fa-spin text-indigo-400 text-2xl"></i>
      <p class="text-xs text-slate-400 mt-2">Loading attendance data...</p>
    </div>

    <template v-else>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="stat in attendanceStats" :key="stat.label"
             :class="['p-6 rounded-[2rem] border shadow-sm', stat.bgClass]">
          <p :class="['text-[10px] font-black uppercase tracking-widest mb-1', stat.textClass]">{{ stat.label }}</p>
          <p :class="['text-2xl font-black', stat.textClass]">{{ stat.value }}</p>
        </div>
      </div>

      <div class="bg-white rounded-[2.5rem] border border-slate-200/60 shadow-sm overflow-hidden">
        <div class="px-8 py-6 border-b border-slate-50 flex justify-between items-center">
          <h3 class="text-sm font-black text-slate-800 uppercase tracking-wider">Attendance Register</h3>
          <div class="flex gap-2">
             <span class="flex items-center gap-1 text-[10px] font-bold text-slate-400"><i class="fa fa-circle text-green-500"></i> Present</span>
             <span class="flex items-center gap-1 text-[10px] font-bold text-slate-400"><i class="fa fa-circle text-red-500"></i> Absent</span>
             <span class="flex items-center gap-1 text-[10px] font-bold text-slate-400"><i class="fa fa-circle text-amber-500"></i> Leave</span>
          </div>
        </div>

        <table class="w-full text-left border-collapse">
          <thead class="bg-slate-50">
            <tr>
              <th class="p-6 text-[10px] font-black uppercase text-slate-400">Month</th>
              <th class="p-6 text-[10px] font-black uppercase text-slate-400">P</th>
              <th class="p-6 text-[10px] font-black uppercase text-slate-400">A</th>
              <th class="p-6 text-[10px] font-black uppercase text-slate-400">L</th>
              <th class="p-6 text-[10px] font-black uppercase text-slate-400 text-right">Percentage</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50 text-sm font-bold text-slate-700">
            <tr v-for="month in attendanceLog" :key="month.name" class="hover:bg-slate-50/50">
              <td class="p-6 font-black text-slate-800">{{ month.name }}</td>
              <td class="p-6 text-green-600">{{ month.present }}</td>
              <td class="p-6 text-red-500">{{ month.absent }}</td>
              <td class="p-6 text-amber-500">{{ month.leave }}</td>
              <td class="p-6 text-right">
                <div class="flex items-center justify-end gap-3">
                  <span class="text-xs">{{ month.percent }}%</span>
                  <div class="w-16 bg-slate-100 h-1.5 rounded-full overflow-hidden">
                    <div class="bg-indigo-600 h-full" :style="{ width: month.percent + '%' }"></div>
                  </div>
                </div>
              </td>
            </tr>
            <tr v-if="attendanceLog.length === 0">
              <td colspan="5" class="p-6 text-center text-slate-400 text-xs">No attendance records found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAttendanceSummary } from '~/composable/useAttendance'

const { summary, loading, fetchSummary } = useAttendanceSummary()

onMounted(() => {
  fetchSummary()
})

const attendanceStats = computed(() => {
  if (!summary.value) {
    return [
      { label: 'Attendance Rate', value: '--%', bgClass: 'bg-indigo-600', textClass: 'text-white' },
      { label: 'Total Present', value: '-- Days', bgClass: 'bg-white', textClass: 'text-slate-800' },
      { label: 'Total Absent', value: '-- Days', bgClass: 'bg-red-50 border-red-100', textClass: 'text-red-600' },
      { label: 'Medical Leave', value: '-- Days', bgClass: 'bg-amber-50 border-amber-100', textClass: 'text-amber-600' },
    ]
  }
  const s = summary.value
  return [
    { label: 'Attendance Rate', value: `${s.rate}%`, bgClass: 'bg-indigo-600', textClass: 'text-white' },
    { label: 'Total Present', value: `${s.total_present} Days`, bgClass: 'bg-white', textClass: 'text-slate-800' },
    { label: 'Total Absent', value: `${String(s.total_absent).padStart(2, '0')} Days`, bgClass: 'bg-red-50 border-red-100', textClass: 'text-red-600' },
    { label: 'Medical Leave', value: `${String(s.total_leave).padStart(2, '0')} Days`, bgClass: 'bg-amber-50 border-amber-100', textClass: 'text-amber-600' },
  ]
})

const attendanceLog = computed(() => {
  return summary.value?.months || []
})
</script>
