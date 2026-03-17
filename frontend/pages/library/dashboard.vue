<template>
    <main class="flex-1 overflow-y-auto p-6 lg:p-10 custom-scrollbar bg-[#f8fafc]">

        <section
            class="relative bg-white rounded-[1.5rem] md:rounded-[3rem] p-6 md:p-12 border border-slate-200 shadow-sm mb-8 overflow-hidden">

            <div class="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-8">

                <!-- LEFT -->
                <div class="max-w-2xl">
                    <div class="flex items-center gap-2 mb-4">
                        <div class="w-2 h-2 rounded-full bg-indigo-600 animate-pulse"></div>
                        <span class="text-[10px] font-black uppercase tracking-widest text-slate-500">
                            System Active • {{ user.libraryId }}
                        </span>
                    </div>

                    <h1 class="text-4xl md:text-6xl font-black text-slate-900 leading-[0.9] tracking-tight mb-4">
                        Digital <span class="text-slate-400">Archive.</span>
                    </h1>

                    <p class="text-slate-500 text-sm md:text-base font-medium max-w-md leading-relaxed">
                        Manage your academic trajectory and digital resources through our high-performance repository.
                    </p>
                </div>

                <!-- USER CARD -->
                <div
                    class="flex flex-col sm:flex-row items-center gap-4 bg-slate-50 p-3 rounded-[2rem] border border-slate-100">

                    <div class="flex items-center gap-3 pl-2 pr-4 py-1">
                        <div
                            class="w-12 h-12 rounded-2xl bg-slate-900 flex items-center justify-center text-white shadow-lg overflow-hidden">

                            <img v-if="user.profileImage" :src="user.profileImage" class="w-full h-full object-cover" />

                            <span v-else class="font-black text-sm">
                                {{ initials }}
                            </span>

                        </div>

                        <div>
                            <p class="text-[11px] font-black text-slate-900">
                                {{ user.name }}
                            </p>

                            <p class="text-[9px] font-bold text-slate-400 uppercase tracking-wider">
                                {{ user.title }}
                            </p>
                        </div>
                    </div>

                    <button
                        class="bg-white border border-slate-200 text-slate-900 px-6 py-3 rounded-2xl font-black text-[10px] uppercase tracking-widest hover:bg-slate-900 hover:text-white transition-all">
                        Search Catalog
                    </button>

                </div>

            </div>

            <div class="absolute right-0 bottom-0 opacity-[0.03] select-none pointer-events-none">
                <h1 class="text-[15rem] font-black">{{ config.public?.appName }}</h1>
            </div>

        </section>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

            <div class="lg:col-span-8 space-y-8">

                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div v-for="stat in libraryStats" :key="stat.label"
                        class="bg-white p-6 rounded-[2rem] border border-slate-100 shadow-sm">
                        <p :class="stat.color" class="text-3xl font-black tracking-tighter">{{ stat.value }}</p>
                        <p class="text-[10px] font-black uppercase tracking-widest text-slate-400 mt-2">{{ stat.label }}
                        </p>
                    </div>
                </div>

                <div class="bg-white rounded-[2.5rem] border border-slate-100 shadow-sm overflow-hidden">
                    <div class="p-8 border-b border-slate-50 flex justify-between items-center">
                        <h2 class="text-xl font-black text-black tracking-tight">Reading Now</h2>
                        <button
                            class="text-indigo-500 text-xs font-black uppercase tracking-widest hover:underline">Extend
                            All</button>
                    </div>

                    <div class="p-8 space-y-6">
                        <div v-for="book in currentBooks" :key="book.id"
                            class="group flex flex-col md:flex-row md:items-center justify-between p-6 rounded-3xl bg-slate-50 border border-transparent hover:border-indigo-100 hover:bg-white transition-all">

                            <div class="flex items-center gap-6">
                                <div
                                    class="w-14 h-20 bg-slate-200 rounded-xl shadow-sm flex-shrink-0 flex items-center justify-center text-slate-400">
                                    <i class="fa fa-book text-xl"></i>
                                </div>
                                <div>
                                    <h3 class="font-black text-slate-800 leading-snug">{{ book.title }}</h3>
                                    <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">ISBN:
                                        {{ book.isbn }}</p>
                                </div>
                            </div>

                            <div class="mt-4 md:mt-0 flex items-center gap-8">
                                <div class="text-right">
                                    <p class="text-xs font-black text-slate-800">{{ daysRemaining(book.due) }} Days Left
                                    </p>
                                    <p class="text-[10px] font-bold text-slate-400">Due {{ formatDate(book.due) }}</p>
                                </div>
                                <button
                                    class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-600 hover:bg-indigo-600 hover:text-white transition-all">
                                    <i class="fa fa-redo-alt text-xs"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-[2.5rem] border border-slate-100 shadow-sm overflow-hidden">
                    <div class="p-8 border-b border-slate-50">
                        <h2 class="text-xl font-black text-black">Borrowing History</h2>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left">
                            <thead class="bg-slate-50/50">
                                <tr>
                                    <th
                                        class="px-8 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest">
                                        Resource</th>
                                    <th
                                        class="px-8 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest">
                                        Timeline</th>
                                    <th
                                        class="px-8 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest">
                                        Status</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-50">
                                <tr v-for="item in history" :key="item.id"
                                    class="hover:bg-slate-50/30 transition-colors">
                                    <td class="px-8 py-5">
                                        <p class="font-bold text-slate-800 text-sm">{{ item.title }}</p>
                                        <p class="text-[10px] font-medium text-slate-400">{{ item.category }}</p>
                                    </td>
                                    <td class="px-8 py-5">
                                        <p class="text-xs font-bold text-slate-600">{{ formatDate(item.issue) }} — {{
                                            item.return ? formatDate(item.return) : '...' }}</p>
                                    </td>
                                    <td class="px-8 py-5">
                                        <span :class="statusColor(item.status)"
                                            class="text-[9px] font-black uppercase tracking-widest px-3 py-1 rounded-full">
                                            {{ item.status }}
                                        </span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="lg:col-span-4 space-y-8">

                <div class="bg-slate-900 rounded-[2.5rem] p-8 text-white">
                    <div class="flex justify-between items-start mb-6">
                        <h3 class="font-black text-lg tracking-tight">Account <br />Balance</h3>
                        <i class="fa fa-wallet text-indigo-400"></i>
                    </div>
                    <p class="text-4xl font-black tracking-tighter mb-2">{{ stats.fine }}</p>
                    <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-6">Total Pending Fine
                    </p>
                    <button
                        class="w-full py-3 bg-indigo-600 rounded-2xl text-[10px] font-black uppercase tracking-[0.2em] hover:bg-indigo-700 transition-all">
                        Pay Outstanding
                    </button>
                </div>

                <BookRecommendetion :recommendedBooks="recommendedBooks" />

                <div class="bg-indigo-50 rounded-[2.5rem] p-8 border border-indigo-100">
                    <h3 class="font-black text-indigo-900 mb-4">Library Policies</h3>
                    <ul class="space-y-4">
                        <li v-for="i in 3" :key="i" class="flex gap-3">
                            <div
                                class="w-5 h-5 rounded-full bg-white flex items-center justify-center flex-shrink-0 shadow-sm">
                                <i class="fa fa-check text-[8px] text-indigo-600"></i>
                            </div>
                            <p class="text-xs font-medium text-indigo-800/80 leading-relaxed">
                                {{ policyTexts[i - 1] }}
                            </p>
                        </li>
                    </ul>
                </div>

            </div>
        </div>
    </main>
</template>

<script setup>
import { ref, computed } from 'vue'
import BookRecommendetion from '~/components/BookRecommendation.vue'
const config = useRuntimeConfig();

// ─── USER ────────────────────────────────────────────────────────────────────
const user = {
    name: 'Sudipta Ghosh',
    title: 'Software Architect',
    libraryId: 'LIB-2026-SG',
    profileImage: null, // Set to a URL string when you have one
}

// ─── RAW DATA (Single Source of Truth) ───────────────────────────────────────
const currentBooks = ref([
    { id: 1, title: "Clean Code", isbn: "9780132350884", due: "2026-03-25" },
    { id: 2, title: "Computer Networks", isbn: "9780132126953", due: "2026-03-20" }
])

const history = ref([
    { id: 1, title: "Quantum Physics", category: "Science", issue: "2026-01-10", return: "2026-02-01", status: "Returned" },
    { id: 2, title: "UI Design Patterns", category: "Design", issue: "2026-02-15", return: null, status: "Issued" },
    { id: 3, title: "World History Vol 1", category: "History", issue: "2025-12-01", return: "2025-12-20", status: "Overdue" }
])

// ─── DERIVED STATS (Dynamic instead of hardcoded) ────────────────────────────
const stats = computed(() => {
    const total = history.value.length
    const current = history.value.filter(b => b.status === 'Issued').length
    const returned = history.value.filter(b => b.status === 'Returned').length
    const overdue = history.value.filter(b => b.status === 'Overdue').length

    return {
        total,
        current,
        returned,
        overdue,
        fine: "$12.50" // static for now
    }
})

// ─── LIBRARY CARDS ───────────────────────────────────────────────────────────
const libraryStats = computed(() => [
    { label: 'Borrowed', value: stats.value.total, color: 'text-black' },
    { label: 'Active', value: stats.value.current, color: 'text-indigo-600' },
    { label: 'Overdue', value: stats.value.overdue, color: 'text-red-600' },
    { label: 'Reserved', value: '03', color: 'text-slate-400' }
])

// ─── POLICY TEXTS ────────────────────────────────────────────────────────────
const policyTexts = [
    "Books can be renewed twice if not reserved.",
    "Fines accrue at $0.50 per day after the due date.",
    "Digital access is available 24/7 via the portal."
]

// ─── UTILITIES ───────────────────────────────────────────────────────────────
const formatDate = (date) => {
    if (!date) return '...'
    return new Date(date).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric'
    })
}

const daysRemaining = (due) => {
    const today = new Date()
    const dueDate = new Date(due)
    const diff = Math.ceil((dueDate - today) / (1000 * 60 * 60 * 24))
    return diff > 0 ? diff : 0
}

// ─── STATUS COLORS (SCALABLE) ────────────────────────────────────────────────
const STATUS_STYLES = {
    Returned: 'bg-green-100 text-green-700',
    Issued: 'bg-indigo-100 text-indigo-700',
    Overdue: 'bg-red-100 text-red-700'
}

const statusColor = (status) => {
    return STATUS_STYLES[status] || 'bg-slate-100 text-slate-600'
}

// ─── Recommended Books ────────────────────────────────────────────────

const recommendedBooks = ref([
    { id: 1, title: "Atomic Habits", category: "Self Help" },
    { id: 2, title: "Deep Work", category: "Productivity" },
    { id: 3, title: "The Pragmatic Programmer", category: "Programming" }
])
</script>