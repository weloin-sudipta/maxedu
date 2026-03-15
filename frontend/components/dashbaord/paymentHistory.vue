<template>
  <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden animate-in fade-in duration-700">
    
    <div class="p-8 border-b border-slate-50 flex flex-col md:flex-row justify-between items-end gap-6 bg-slate-50/30">
      <div>
        <h3 class="text-[10px] font-black uppercase tracking-[0.3em] text-slate-400 mb-1">Financial Records</h3>
        <p class="text-2xl font-black text-slate-800 tracking-tight">Payment Slips</p>
      </div>

      <div class="flex gap-3 w-full md:w-auto">
        <select class="bg-white border border-slate-200 rounded-xl px-4 py-2.5 text-[10px] font-black text-slate-500 uppercase tracking-widest outline-none focus:ring-4 focus:ring-indigo-500/10 transition-all shadow-sm">
          <option>All Semesters</option>
          <option>Semester 3</option>
          <option>Semester 2</option>
        </select>
        <button class="bg-slate-900 text-white px-6 py-2.5 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-indigo-600 transition-all shadow-lg active:scale-95">
          <i class="fa fa-filter mr-2"></i> Filter
        </button>
      </div>
    </div>

    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-slate-50/50">
            <th class="px-8 py-5 th-style">Reference ID</th>
            <th class="px-8 py-5 th-style">Date</th>
            <th class="px-8 py-5 th-style text-center">Status</th>
            <th class="px-8 py-5 th-style text-right">Amount</th>
            <th class="px-8 py-5 th-style text-right">Action</th>
          </tr>
        </thead>

        <tbody class="divide-y divide-slate-50">
          <tr v-for="slip in paymentHistory" :key="slip.id" class="hover:bg-slate-50/50 transition-colors group">
            
            <td class="px-8 py-6">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center text-[10px] font-black">
                  #{{ slip.id.slice(-2) }}
                </div>
                <span class="text-xs font-black text-slate-700 uppercase tracking-tighter">{{ slip.id }}</span>
              </div>
            </td>

            <!-- <td class="px-8 py-6">
              <div class="flex flex-col">
                <span class="text-sm font-black text-slate-800">{{ slip.title }}</span>
                <span class="text-[9px] font-bold text-slate-400 uppercase tracking-widest">{{ slip.method }}</span>
              </div>
            </td> -->

            <td class="px-8 py-6">
              <span class="text-xs font-bold text-slate-500">{{ slip.date }}</span>
            </td>

            <td class="px-8 py-6 text-center">
              <span :class="getStatusStyles(slip.status)" class="px-3 py-1.5 rounded-lg text-[9px] font-black uppercase tracking-widest border shadow-sm">
                {{ slip.status }}
              </span>
            </td>

            <td class="px-8 py-6 text-right">
              <span class="text-sm font-black text-slate-900">${{ slip.amount.toLocaleString() }}</span>
            </td>

            <td class="px-8 py-6 text-right">
              <button class="w-10 h-10 rounded-xl bg-white border border-slate-200 text-slate-400 hover:text-indigo-600 hover:border-indigo-200 hover:shadow-md transition-all">
                <i class="fa fa-download"></i>
              </button>
            </td>

          </tr>
        </tbody>
      </table>
    </div>

    <div class="p-8 bg-slate-50/30 border-t border-slate-100 flex justify-between items-center">
      <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Showing last 5 transactions</p>
      <button class="text-[10px] font-black text-indigo-600 uppercase tracking-[0.2em] hover:text-slate-900 transition-colors">
        Statement of Account <i class="fa fa-arrow-right ml-2"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
const paymentHistory = [
  { id: 'PAY-8829-102', title: 'Tuition Fee - Semester 3', method: 'Online Banking', date: 'Mar 10, 2026', status: 'Completed', amount: 4500.00 },
  { id: 'PAY-8829-098', title: 'Library Membership Renewal', method: 'Credit Card', date: 'Feb 28, 2026', status: 'Completed', amount: 50.00 },
];

const getStatusStyles = (status) => {
  switch (status) {
    case 'Completed': return 'bg-green-50 text-green-600 border-green-100';
    case 'Pending': return 'bg-amber-50 text-amber-600 border-amber-100';
    case 'Refunded': return 'bg-blue-50 text-blue-600 border-blue-100';
    default: return 'bg-slate-50 text-slate-600 border-slate-100';
  }
}
</script>

<style scoped>
.th-style { 
  @apply text-[10px] font-black uppercase text-slate-400 tracking-[0.2em]; 
}
</style>