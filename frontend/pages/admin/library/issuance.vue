<template>
    <div class="min-h-screen bg-[#f8fafc] dark:bg-slate-950 p-4 lg:p-8 font-sans text-slate-900 dark:text-slate-100 transition-colors">
        <div class="max-w-[1440px] mx-auto space-y-6">

            <!-- HEADER -->
            <header
                class="rounded-[2.5rem] shadow-xl shadow-indigo-200/40 p-8">
                <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                    <div>
                        <h1 class="text-4xl font-black tracking-tight mb-2">Book Issuance</h1>
                        <p class="text-indigo-500 text-[11px] font-bold uppercase tracking-widest">Manage circulation &
                            loan tracking</p>
                    </div>
                    <div class="flex gap-3">
                        <button
                            class="px-8 py-3 text-white bg-indigo-500 rounded-2xl text-[14px] font-black uppercase hover:bg-indigo-700 transition-all shadow-lg">
                            <i class="fa fa-plus mr-2"></i> New Issue
                        </button>
                    </div>
                </div>
            </header>

            <!-- STATS -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-white dark:bg-slate-900 rounded-[2rem] p-6 border border-slate-200/60 dark:border-slate-800 shadow-sm dark:shadow-none transition-colors">
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Active
                            Loans</span>
                        <i class="fa fa-book text-indigo-500 text-xl"></i>
                    </div>
                    <p class="text-3xl font-black text-slate-800">{{ loans.length }}</p>
                    <p class="text-[10px] font-bold text-slate-300 uppercase tracking-tighter mt-2">{{loans.filter(l =>
                        !l.returned).length }} in circulation</p>
                </div>

                <div class="bg-white dark:bg-slate-900 rounded-[2rem] p-6 border border-slate-200/60 dark:border-slate-800 shadow-sm dark:shadow-none transition-colors">
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Overdue</span>
                        <i class="fa fa-exclamation-triangle text-red-500 text-xl"></i>
                    </div>
                    <p class="text-3xl font-black text-red-600">{{ overdueCount }}</p>
                    <p class="text-[10px] font-bold text-slate-300 uppercase tracking-tighter mt-2">requiring attention
                    </p>
                </div>

                <div class="bg-white dark:bg-slate-900 rounded-[2rem] p-6 border border-slate-200/60 dark:border-slate-800 shadow-sm dark:shadow-none transition-colors">
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Fine
                            Pending</span>
                        <i class="fa fa-money text-amber-500 text-xl"></i>
                    </div>
                    <p class="text-3xl font-black text-amber-600">₹{{ totalFine }}</p>
                    <p class="text-[10px] font-bold text-slate-300 uppercase tracking-tighter mt-2">collected so far</p>
                </div>

                <div class="bg-white dark:bg-slate-900 rounded-[2rem] p-6 border border-slate-200/60 dark:border-slate-800 shadow-sm dark:shadow-none transition-colors">
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Returned</span>
                        <i class="fa fa-check-circle text-green-500 text-xl"></i>
                    </div>
                    <p class="text-3xl font-black text-green-600">{{loans.filter(l => l.returned).length}}</p>
                    <p class="text-[10px] font-bold text-slate-300 uppercase tracking-tighter mt-2">this month</p>
                </div>
            </div>

            <!-- FILTERS -->
            <div class="flex gap-2 overflow-x-auto no-scrollbar pb-2">
                <button v-for="filter in filters" :key="filter.id" @click="activeFilter = filter.id" :class="[
                    activeFilter === filter.id
                        ? 'bg-slate-900 text-white shadow-lg'
                        : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50',
                    'px-6 py-3 rounded-2xl text-[10px] font-black uppercase tracking-widest border transition-all whitespace-nowrap'
                ]">
                    {{ filter.label }}
                </button>
            </div>

            <!-- ACTIVE LOANS TABLE -->
            <div class="bg-white dark:bg-slate-900 rounded-[2.5rem] shadow-sm dark:shadow-none border border-slate-200/60 dark:border-slate-800 overflow-hidden transition-colors">
                <div
                    class="p-8 border-b border-slate-50 dark:border-slate-800 flex justify-between items-center backdrop-blur-xl bg-gradient-to-r from-slate-50 dark:from-slate-800/50 to-transparent transition-colors">
                    <div>
                        <h3 class="text-sm font-black text-slate-800 uppercase tracking-widest">Active Loans</h3>
                        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-tighter mt-1">{{
                            filteredLoans.length }} records</p>
                    </div>
                    <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Total: {{ loans.length
                        }}</span>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-50/50 border-b border-slate-100">
                                <th class="px-8 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">
                                    Borrower</th>
                                <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">
                                    Book Title</th>
                                <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">
                                    Accession</th>
                                <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">
                                    Issued</th>
                                <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">
                                    Due Date</th>
                                <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">
                                    Status</th>
                                <th
                                    class="px-8 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest text-right">
                                    Action</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-50">
                            <tr v-for="loan in filteredLoans" :key="loan.id"
                                class="hover:bg-slate-50/30 transition-colors group">
                                <td class="px-8 py-5">
                                    <div class="flex items-center gap-3">
                                        <div
                                            :class="['h-10 w-10 rounded-xl flex items-center justify-center font-black text-[11px] text-white', loan.avatarBg]">
                                            {{ loan.initials }}
                                        </div>
                                        <div class="flex flex-col">
                                            <span class="text-xs font-black text-slate-700">{{ loan.student }}</span>
                                            <span class="text-[9px] font-bold text-slate-400 uppercase">{{ loan.rollNo
                                                }}</span>
                                        </div>
                                    </div>
                                </td>
                                <td class="px-6 py-5">
                                    <div class="flex flex-col">
                                        <span class="text-xs font-bold text-slate-700">{{ loan.bookTitle }}</span>
                                        <span class="text-[9px] font-bold text-slate-400">{{ loan.author }}</span>
                                    </div>
                                </td>
                                <td class="px-6 py-5 text-xs font-black text-indigo-600">{{ loan.accNo }}</td>
                                <td class="px-6 py-5 text-xs font-bold text-slate-600">{{ loan.issuedDate }}</td>
                                <td class="px-6 py-5">
                                    <div class="flex flex-col">
                                        <span
                                            :class="[loan.overdue ? 'text-red-600 font-black' : 'text-slate-600 font-bold', 'text-xs']">{{
                                            loan.dueDate }}</span>
                                        <span v-if="loan.overdue" class="text-[9px] font-bold text-red-500 uppercase">{{
                                            loan.daysOverdue }} days late</span>
                                    </div>
                                </td>
                                <td class="px-6 py-5">
                                    <span :class="[
                                        loan.overdue ? 'bg-red-50 text-red-600 border-red-100' : 'bg-green-50 text-green-600 border-green-100',
                                        'px-3 py-1.5 text-[9px] font-black uppercase tracking-wider rounded-lg border'
                                    ]">
                                        {{ loan.overdue ? 'Overdue' : 'Active' }}
                                    </span>
                                </td>
                                <td class="px-8 py-5 text-right">
                                    <button
                                        class="px-4 py-2 bg-slate-900 text-white rounded-xl text-[9px] font-black uppercase hover:bg-indigo-600 transition-all">
                                        <i class="fa fa-reply mr-1"></i> Return
                                    </button>
                                </td>
                            </tr>
                            <tr v-if="filteredLoans.length === 0">
                                <td colspan="7" class="px-8 py-12 text-center">
                                    <i class="fa fa-inbox text-slate-100 text-5xl mb-4 block"></i>
                                    <p class="text-sm font-black text-slate-400 uppercase">No active loans</p>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useToast } from '~/composable/useToast'

const { addToast } = useToast()

const scanInput = ref('');
const activeFilter = ref('all');

const filters = [
    { id: 'all', label: 'All Loans' },
    { id: 'active', label: 'Active' },
    { id: 'overdue', label: 'Overdue' },
    { id: 'returned', label: 'Returned' }
];

// DEMO DATA
const loans = ref([
    {
        id: 1,
        student: 'Aman Kumar',
        rollNo: 'A001',
        initials: 'AK',
        avatarBg: 'bg-indigo-600',
        bookTitle: 'Advanced Data Structures',
        author: 'Mark Allen Weiss',
        accNo: 'LB-2024-001',
        issuedDate: 'Feb 28, 2026',
        dueDate: 'Mar 14, 2026',
        overdue: false,
        daysOverdue: 0,
        returned: false,
        fine: 0
    },
    {
        id: 2,
        student: 'Priya Singh',
        rollNo: 'A002',
        initials: 'PS',
        avatarBg: 'bg-purple-600',
        bookTitle: 'Introduction to Algorithms',
        author: 'Cormen, Leiserson',
        accNo: 'LB-2024-002',
        issuedDate: 'Feb 20, 2026',
        dueDate: 'Mar 06, 2026',
        overdue: true,
        daysOverdue: 3,
        returned: false,
        fine: 15
    },
    {
        id: 3,
        student: 'Rajesh Patel',
        rollNo: 'A003',
        initials: 'RP',
        avatarBg: 'bg-green-600',
        bookTitle: 'Design Patterns',
        author: 'Gang of Four',
        accNo: 'LB-2024-003',
        issuedDate: 'Mar 01, 2026',
        dueDate: 'Mar 21, 2026',
        overdue: false,
        daysOverdue: 0,
        returned: false,
        fine: 0
    },
    {
        id: 4,
        student: 'Nikita Verma',
        rollNo: 'A004',
        initials: 'NV',
        avatarBg: 'bg-amber-600',
        bookTitle: 'Database Management Systems',
        author: 'Raghu Ramakrishnan',
        accNo: 'LB-2024-004',
        issuedDate: 'Feb 10, 2026',
        dueDate: 'Feb 24, 2026',
        overdue: true,
        daysOverdue: 9,
        returned: false,
        fine: 45
    },
    {
        id: 5,
        student: 'Vikas Sharma',
        rollNo: 'A005',
        initials: 'VS',
        avatarBg: 'bg-red-600',
        bookTitle: 'Operating Systems Concepts',
        author: 'Abraham Silberschatz',
        accNo: 'LB-2024-005',
        issuedDate: 'Feb 15, 2026',
        dueDate: 'Mar 01, 2026',
        overdue: true,
        daysOverdue: 4,
        returned: false,
        fine: 20
    },
    {
        id: 6,
        student: 'Ananya Gupta',
        rollNo: 'A006',
        initials: 'AG',
        avatarBg: 'bg-cyan-600',
        bookTitle: 'Computer Networks',
        author: 'Andrew S. Tanenbaum',
        accNo: 'LB-2024-006',
        issuedDate: 'Mar 02, 2026',
        dueDate: 'Mar 16, 2026',
        overdue: false,
        daysOverdue: 0,
        returned: false,
        fine: 0
    },
    {
        id: 7,
        student: 'Sanjay Mishra',
        rollNo: 'A007',
        initials: 'SM',
        avatarBg: 'bg-pink-600',
        bookTitle: 'Compiler Design',
        author: 'Alfred V. Aho',
        accNo: 'LB-2024-007',
        issuedDate: 'Feb 25, 2026',
        dueDate: 'Mar 11, 2026',
        overdue: false,
        daysOverdue: 0,
        returned: true,
        fine: 0
    },
    {
        id: 8,
        student: 'Deepak Kumar',
        rollNo: 'A008',
        initials: 'DK',
        avatarBg: 'bg-blue-600',
        bookTitle: 'Software Engineering',
        author: 'Ian Sommerville',
        accNo: 'LB-2024-008',
        issuedDate: 'Feb 18, 2026',
        dueDate: 'Mar 04, 2026',
        overdue: true,
        daysOverdue: 1,
        returned: false,
        fine: 5
    }
]);

const filteredLoans = computed(() => {
    switch (activeFilter.value) {
        case 'overdue':
            return loans.value.filter(l => l.overdue && !l.returned);
        case 'active':
            return loans.value.filter(l => !l.returned);
        case 'returned':
            return loans.value.filter(l => l.returned);
        default:
            return loans.value;
    }
});

const overdueCount = computed(() => {
    return loans.value.filter(l => l.overdue && !l.returned).length;
});

const totalFine = computed(() => {
    return loans.value.reduce((sum, l) => sum + (l.fine || 0), 0);
});

const processScanned = () => {
    if (scanInput.value.trim()) {
        addToast(`Processing: ${scanInput.value}`, "success");
        scanInput.value = '';
    }
};
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
    display: none;
}
</style>