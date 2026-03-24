<template>
  <div>
    <!-- SKELETON LOADING -->
    <div v-if="loading" class="space-y-6 animate-in fade-in duration-500">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <UiSkeleton height="h-28" class="rounded-[2rem]" v-for="i in 2" :key="'fee-card-'+i" />
      </div>
      <div class="bg-white rounded-[2.5rem] border border-slate-200/60 shadow-sm overflow-hidden p-8 space-y-6">
        <UiSkeleton height="h-6" width="w-1/4" class="mb-4" />
        <UiSkeleton height="h-16" class="rounded-xl w-full" v-for="i in 4" :key="'fee-row-'+i" />
      </div>
    </div>

    <!-- CONTENT -->
    <div v-else class="space-y-6 animate-in fade-in duration-500">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white dark:bg-slate-900 p-6 rounded-[2rem] border border-slate-200/60 dark:border-slate-800 shadow-sm dark:shadow-none transition-colors">
        <p class="text-[10px] font-black text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-1 transition-colors">Total Program Fees</p>
        <p class="text-2xl font-black text-slate-800 dark:text-slate-100 transition-colors">₹{{ totalFees.toLocaleString() }}</p>
      </div>
      <div class="bg-red-50 dark:bg-red-900/20 p-6 rounded-[2rem] border border-red-100 dark:border-red-900/30 shadow-sm dark:shadow-none transition-colors">
        <p class="text-[10px] font-black text-red-600 dark:text-red-400 uppercase tracking-widest mb-1 transition-colors">Outstanding Balance</p>
        <p class="text-2xl font-black text-red-700 dark:text-red-300 transition-colors">₹{{ balanceDue.toLocaleString() }}</p>
      </div>
      <!-- <div class="bg-indigo-50 p-6 rounded-[2rem] border border-indigo-100 shadow-sm">
        <p class="text-[10px] font-black text-indigo-600 uppercase tracking-widest mb-1">Due Date</p>
        <p class="text-2xl font-black text-indigo-700">{{ fees[0]?.date || 'N/A' }}</p>
      </div> -->
    </div>

    <div class="bg-white dark:bg-slate-900 rounded-[2.5rem] border border-slate-200/60 dark:border-slate-800 shadow-sm dark:shadow-none overflow-hidden transition-colors">
      <div class="px-8 py-6 border-b border-slate-50 dark:border-slate-800/50 transition-colors">
        <h3 class="text-sm font-black text-slate-800 dark:text-slate-100 uppercase tracking-wider transition-colors">Fee Details & History</h3>
      </div>

      <table class="w-full text-left border-collapse">
        <thead class="bg-slate-50 dark:bg-slate-800/50 border-b border-slate-100 dark:border-slate-800/50 transition-colors">
          <tr>
            <th class="p-6 text-[10px] font-black uppercase text-slate-400 dark:text-slate-500 transition-colors">Program / Enrollment</th>
            <th class="p-6 text-[10px] font-black uppercase text-slate-400 dark:text-slate-500 transition-colors">Due Date</th>
            <th class="p-6 text-[10px] font-black uppercase text-slate-400 dark:text-slate-500 transition-colors">Total Amount</th>
            <th class="p-6 text-[10px] font-black uppercase text-slate-400 dark:text-slate-500 transition-colors">Status</th>
            <th class="p-6 text-[10px] font-black uppercase text-slate-400 dark:text-slate-500 text-right transition-colors">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-50 dark:divide-slate-800/50 text-sm font-bold text-slate-700 dark:text-slate-300 transition-colors">
          <template v-for="fee in fees" :key="fee.id">
            <tr 
              @click="toggleExpand(fee.id)" 
              class="hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-all cursor-pointer group"
              :class="{'bg-indigo-50/30 dark:bg-indigo-900/20': expandedId === fee.id}"
            >
              <td class="p-6">
                <div class="flex items-center gap-4">
                   <div :class="['w-8 h-8 rounded-xl flex items-center justify-center transition-colors', expandedId === fee.id ? 'bg-indigo-600 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-400 dark:text-slate-500 group-hover:bg-indigo-100 dark:group-hover:bg-indigo-900/50']">
                      <i :class="['fa', expandedId === fee.id ? 'fa-minus' : 'fa-plus', 'text-[10px]']"></i>
                   </div>
                   <div>
                     <span class="block text-slate-800 dark:text-slate-100 tracking-tight transition-colors">{{ fee.program_name }}</span>
                     <span class="text-[10px] text-slate-400 dark:text-slate-500 font-medium tracking-tight uppercase transition-colors">{{ fee.transactionId }}</span>
                   </div>
                </div>
              </td>
              <td class="p-6 text-slate-400 dark:text-slate-500 font-medium transition-colors">{{ fee.date }}</td>
              <td class="p-6">₹{{ fee.amount.toLocaleString() }}</td>
              <td class="p-6">
                <span :class="[
                  fee.status === 'Paid' ? 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400' : 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400',
                  'px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-tighter transition-colors'
                ]">
                  {{ fee.status }}
                </span>
              </td>
              <td class="p-6 text-right">
                <button v-if="fee.status === 'Unpaid'" class="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-[10px] font-black uppercase tracking-widest transition-transform active:scale-95 shadow-md shadow-indigo-200 dark:shadow-none">
                  Pay Now
                </button>
                <button v-else @click.stop="downloadFee(fee)" class="text-slate-400 dark:text-slate-500 hover:text-indigo-600 dark:hover:text-indigo-400 p-2 transition-colors">
                  <i class="fa fa-file-pdf-o text-lg"></i>
                </button>
              </td>
            </tr>

            <tr v-if="expandedId === fee.id">
              <td colspan="5" class="bg-slate-50/50 dark:bg-slate-800/30 p-0 transition-colors">
                <div class="px-20 py-8 animate-in slide-in-from-top-2 duration-300">
                  <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm dark:shadow-none max-w-2xl transition-colors">
                    <h4 class="text-[10px] font-black text-slate-400 dark:text-slate-500 uppercase tracking-[0.2em] mb-6 transition-colors">Detailed Fee Components</h4>
                    
                    <div class="space-y-4">
                      <div v-for="(item, index) in fee.breakout" :key="index" class="flex justify-between items-center pb-3 border-b border-slate-50 dark:border-slate-800/50 last:border-0 transition-colors">
                        <div class="flex items-center gap-3">
                          <div class="w-1.5 h-1.5 rounded-full bg-indigo-400"></div>
                          <span class="text-slate-600 dark:text-slate-400 transition-colors">{{ item.label }}</span>
                        </div>
                        <span class="text-slate-900 dark:text-slate-100 font-black transition-colors">₹{{ item.value.toLocaleString() }}</span>
                      </div>
                    </div>

                    <div class="mt-6 pt-6 border-t-2 border-dashed border-slate-100 dark:border-slate-800 flex justify-between items-center transition-colors">
                      <span class="text-xs font-black text-slate-400 dark:text-slate-500 uppercase transition-colors">Total Outstanding</span>
                      <span class="text-xl font-black text-indigo-600 dark:text-indigo-400 transition-colors">₹{{ fee.amount.toLocaleString() }}</span>
                    </div>
                    
                    <p class="mt-4 text-[10px] italic text-slate-400 dark:text-slate-500 font-medium transition-colors">
                      Note: {{ fee.words }}
                    </p>
                  </div>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { getFees } from '~/composable/useProfile'
import { useToast } from '~/composable/useToast'

const { addToast } = useToast()

const expandedId = ref(null);
const fees = ref([]);
const loading = ref(true);

/**
 * Transforms the API object into a format for the Student View
 */
const transformFees = (data) => {
  if (!data) return [];

  // We map the main object to a row, showing the Program Name
  return [{
    id: data.feesId, 
    program_name: data.program || "Academic Program 2026", // Fallback if program is missing
    transactionId: data.feesId,
    amount: data.total_fees,
    status: data.outstanding_amount === 0 ? 'Paid' : 'Unpaid',
    date: '15 March 2026', // You can map this from your data if available
    words: data.grand_total_in_words,
    breakout: data.components.map(c => ({
      label: c.fees_category,
      value: c.amount
    }))
  }];
}

onMounted(async () => {
  try {
    const data = await getFees();
    fees.value = transformFees(data);
  } catch (error) {
    console.error("Error fetching fees:", error);
  } finally {
    loading.value = false;
  }
});

const toggleExpand = (id) => {
  expandedId.value = expandedId.value === id ? null : id;
};

const downloadFee = (fee) => {
  addToast(`Downloading Receipt for ${fee.transactionId}`, "success");
};

const totalFees = computed(() => fees.value.reduce((acc, curr) => acc + curr.amount, 0));
const balanceDue = computed(() => fees.value.reduce((acc, curr) => (curr.status === 'Unpaid' ? acc + curr.amount : acc), 0));
</script>