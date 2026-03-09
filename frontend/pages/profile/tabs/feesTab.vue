<template>
  <div class="space-y-6 animate-in fade-in duration-500">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white p-6 rounded-[2rem] border border-slate-200/60 shadow-sm">
        <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Total Fees</p>
        <p class="text-2xl font-black text-slate-800">₹{{ totalFees.toLocaleString() }}</p>
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
          <template v-for="fee in fees" :key="fee.id">
            <tr 
              @click="toggleExpand(fee.id)" 
              class="hover:bg-slate-50/50 transition-all cursor-pointer"
              :class="{'bg-slate-50/80': expandedId === fee.id}"
            >
              <td class="p-6">
                <div class="flex items-center gap-3">
                   <i :class="['fa', expandedId === fee.id ? 'fa-chevron-down' : 'fa-chevron-right', 'text-[10px] text-indigo-500 transition-transform']"></i>
                   <div>
                     <span class="block">{{ fee.group }}</span>
                     <span class="text-[10px] text-slate-400 font-medium tracking-tight">ID: {{ fee.transactionId }}</span>
                   </div>
                </div>
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
              <td class="p-6 text-right space-x-3">
                <button @click.stop="downloadFee(fee)" class="text-slate-400 hover:text-indigo-600 transition-colors p-2">
                  <i class="fa fa-download"></i>
                </button>
                <button v-if="fee.status === 'Unpaid'" class="px-4 py-2 bg-indigo-600 text-white rounded-xl text-[10px] font-black uppercase">
                  Pay Now
                </button>
              </td>
            </tr>

            <tr v-if="expandedId === fee.id">
              <td colspan="5" class="bg-slate-50/30 p-0">
                <div class="px-14 py-6 border-l-4 border-indigo-500 animate-in slide-in-from-top-2 duration-300">
                  <h4 class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-4">Fee Breakout</h4>
                  <div class="space-y-3">
                    <div v-for="(item, index) in fee.breakout" :key="index" class="flex justify-between max-w-md border-b border-slate-100 pb-2">
                      <span class="text-slate-600 font-medium">{{ item.label }}</span>
                      <span class="text-slate-800">${{ item.value.toFixed(2) }}</span>
                    </div>
                    <div class="flex justify-between max-w-md pt-2">
                      <span class="text-indigo-600 font-black uppercase text-[10px]">Total</span>
                      <span class="text-indigo-600 font-black">${{ fee.amount.toFixed(2) }}</span>
                    </div>
                  </div>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { getFees } from '~/composable/useProfile'

const expandedId = ref(null);
const fees = ref([]) 

// Transform backend data to match template structure
const transformFees = (data) => {
  if (!data || !data.components) return [];

  return data.components.map((component, index) => ({
    id: index + 1, // unique id for v-for
    group: component.fees_category,
    transactionId: data.feesId,
    amount: component.amount,
    status: data.outstanding_amount === 0 ? 'Paid' : 'Unpaid',
    date: data.due_date,
    breakout: data.components.map(c => ({
      label: c.fees_category,
      value: c.amount
    }))
  }));
}

onMounted(async () => {
  try {
    const data = await getFees()
    fees.value = transformFees(data)
    console.log("Transformed Student Fees:", fees.value)
  } catch (error) {
    console.error("Error fetching fees:", error)
  }
})

const toggleExpand = (id) => {
  expandedId.value = expandedId.value === id ? null : id;
};

const downloadFee = (fee) => {
  alert(`Downloading Receipt for ${fee.group} (${fee.transactionId})`);
};

// Computed totals
const totalFees = computed(() => fees.value.reduce((acc, curr) => acc + curr.amount, 0));
const paidAmount = computed(() => fees.value.filter(f => f.status === 'Paid').reduce((acc, curr) => acc + curr.amount, 0));
const balanceDue = computed(() => totalFees.value - paidAmount.value);
</script>