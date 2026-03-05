<template>
  <div class="space-y-6 animate-in fade-in duration-500">
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white p-6 rounded-[2rem] border border-slate-200/60 shadow-sm">
        <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Total Fees</p>
        <p class="text-2xl font-black text-slate-800">${{ totalFees.toLocaleString() }}</p>
      </div>

      <div class="bg-green-50 p-6 rounded-[2rem] border border-green-100 shadow-sm">
        <p class="text-[10px] font-black text-green-600 uppercase tracking-widest mb-1">Paid Amount</p>
        <p class="text-2xl font-black text-green-700">${{ paidAmount.toLocaleString() }}</p>
      </div>

      <div class="bg-red-50 p-6 rounded-[2rem] border border-red-100 shadow-sm">
        <p class="text-[10px] font-black text-red-600 uppercase tracking-widest mb-1">Balance Due</p>
        <p class="text-2xl font-black text-red-700">${{ balanceDue.toLocaleString() }}</p>
      </div>
    </div>

    <div class="bg-white rounded-[2.5rem] border border-slate-200/60 shadow-sm overflow-hidden">
      <div class="px-8 py-6 border-b border-slate-50 flex justify-between items-center">
        <h3 class="text-sm font-black text-slate-800 uppercase tracking-wider">Transaction History</h3>
        <button class="text-xs font-bold text-indigo-600 hover:underline">Download Statement</button>
      </div>

      <table class="w-full text-left border-collapse">
        <thead class="bg-slate-50 border-b border-slate-100">
          <tr>
            <th class="p-6 text-[10px] font-black uppercase text-slate-400">Fees Group</th>
            <th class="p-6 text-[10px] font-black uppercase text-slate-400">Due Date</th>
            <th class="p-6 text-[10px] font-black uppercase text-slate-400">Amount</th>
            <th class="p-6 text-[10px] font-black uppercase text-slate-400">Status</th>
            <th class="p-6 text-[10px] font-black uppercase text-slate-400 text-right">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-50 text-sm font-bold text-slate-700">
          <tr v-for="fee in fees" :key="fee.id" class="hover:bg-slate-50/50 transition-all">
            <td class="p-6">
              <span class="block">{{ fee.group }}</span>
              <span class="text-[10px] text-slate-400 font-medium tracking-tight">ID: {{ fee.transactionId }}</span>
            </td>
            <td class="p-6 text-slate-400 font-medium">{{ fee.date }}</td>
            <td class="p-6">${{ fee.amount.toFixed(2) }}</td>
            <td class="p-6">
              <span :class="[
                fee.status === 'Paid' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600',
                'px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-tighter'
              ]">
                {{ fee.status }}
              </span>
            </td>
            <td class="p-6 text-right">
              <button v-if="fee.status === 'Paid'" class="text-slate-400 hover:text-indigo-600 transition-colors">
                <i class="fa fa-file-pdf-o"></i>
              </button>
              <button v-else class="px-4 py-2 bg-indigo-600 text-white rounded-xl text-[10px] font-black uppercase">
                Pay Now
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

/**
 * DEMO DATA: Replace this with an API call or a Prop later.
 * When integrating, simply update this 'fees' array.
 */
const fees = ref([
  { id: 1, transactionId: 'TXN-9021', group: 'Tuition Fee (Q1)', date: '10 May 2025', amount: 1200.00, status: 'Paid' },
  { id: 2, transactionId: 'TXN-9022', group: 'Library Development', date: '15 May 2025', amount: 300.00, status: 'Paid' },
  { id: 3, transactionId: 'TXN-9045', group: 'Tuition Fee (Q2)', date: '10 Aug 2025', amount: 1200.00, status: 'Unpaid' },
  { id: 4, transactionId: 'TXN-9088', group: 'Transport Fee', date: '01 Sep 2025', amount: 450.00, status: 'Unpaid' },
]);

/**
 * COMPUTED PROPERTIES: Automatically recalculate when 'fees' data changes.
 * This ensures your summary cards always match your table.
 */
const totalFees = computed(() => {
  return fees.value.reduce((acc, curr) => acc + curr.amount, 0);
});

const paidAmount = computed(() => {
  return fees.value
    .filter(f => f.status === 'Paid')
    .reduce((acc, curr) => acc + curr.amount, 0);
});

const balanceDue = computed(() => {
  return totalFees.value - paidAmount.value;
});
</script>

<style scoped>
/* Scoped styles for horizontal table scrolling on mobile */
@media (max-width: 768px) {
  .overflow-hidden {
    overflow-x: auto;
  }
}
</style>