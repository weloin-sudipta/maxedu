<template>
  <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-10 font-sans">
    <div class="max-w-[1600px] mx-auto space-y-8">
      
      <header class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div>
          <h1 class="text-3xl font-black tracking-tight text-slate-800">Library Management</h1>
          <p class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mt-1">Admin Control Panel</p>
        </div>

        <div class="flex p-1.5 bg-slate-200/50 rounded-2xl backdrop-blur-sm">
          <button 
            v-for="tab in ['inventory', 'issuance']" :key="tab"
            @click="currentTab = tab"
            :class="[
              'px-8 py-2.5 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all duration-300',
              currentTab === tab ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500 hover:text-slate-800'
            ]"
          >
            {{ tab }}
          </button>
        </div>
      </header>

      <main class="transition-all duration-500">
        <Inventory v-if="currentTab === 'inventory'" :books="staticBooks" />
        <Issuance v-else :loans="staticLoans" />
      </main>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Inventory from './inventory.vue';
import Issuance from './issuance.vue';

const currentTab = ref('inventory');

const staticBooks = ref([
  { id: 1, title: 'Quantum Mechanics', author: 'Griffiths', accNo: 'PHY-101', shelf: 'A-12' },
  { id: 2, title: 'The Great Gatsby', author: 'Fitzgerald', accNo: 'LIT-402', shelf: 'L-01' },
  { id: 3, title: 'Organic Chemistry', author: 'Morrison', accNo: 'CHM-205', shelf: 'C-04' },
  { id: 4, title: 'Introduction to Algorithms', author: 'Cormen', accNo: 'CS-881', shelf: 'S-09' },
  { id: 5, title: 'Calculus Vol 1', author: 'Apostol', accNo: 'MAT-110', shelf: 'M-02' },
]);

const staticLoans = ref([
  { id: 1, student: 'Alex Johnson', rollNo: '101', initials: 'AJ', accNo: 'PHY-101', dueDate: 'Mar 10, 2026', overdue: true, fine: '$5.00' },
  { id: 2, student: 'Sarah Parker', rollNo: '204', initials: 'SP', accNo: 'LIT-402', dueDate: 'Mar 25, 2026', overdue: false, fine: '$0.00' },
]);
</script>