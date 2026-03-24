<template>
    <div class="min-h-screen bg-[#f8fafc] dark:bg-slate-950 p-4 lg:p-8 font-sans text-slate-900 dark:text-slate-100 transition-colors">
        <div class="max-w-[1440px] mx-auto space-y-6">

            <!-- HEADER -->
            <header
                class=" rounded-[2.5rem] shadow-xl shadow-indigo-200/40 p-8">
                <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                    <div>
                        <h1 class="text-4xl font-black tracking-tight mb-2">Library Inventory</h1>
                        <p class="text-indigo-500 text-[11px] font-bold uppercase tracking-widest">Manage books & stock
                            levels</p>
                    </div>
                    <div class="flex gap-3">
                        <button
                            class="px-8 py-3 text-white bg-indigo-600 rounded-2xl text-[10px] font-black uppercase hover:bg-indigo-700 transition-all shadow-lg">
                            <i class="fa fa-plus mr-2"></i> Add Book
                        </button>
                    </div>
                </div>
            </header>

            <!-- STATS -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-white dark:bg-slate-900 rounded-[2rem] p-6 border border-slate-200/60 dark:border-slate-800 shadow-sm dark:shadow-none transition-colors">
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Total Books</span>
                        <i class="fa fa-book text-indigo-500 text-xl"></i>
                    </div>
                    <p class="text-3xl font-black text-slate-800">{{ totalBooks }}</p>
                    <p class="text-[10px] font-bold text-slate-300 uppercase tracking-tighter mt-2">across {{
                        uniqueTitles }} titles</p>
                </div>

                <div class="bg-white dark:bg-slate-900 rounded-[2rem] p-6 border border-slate-200/60 dark:border-slate-800 shadow-sm dark:shadow-none transition-colors">
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Available</span>
                        <i class="fa fa-check-circle text-green-500 text-xl"></i>
                    </div>
                    <p class="text-3xl font-black text-green-600">{{ availableBooks }}</p>
                    <p class="text-[10px] font-bold text-slate-300 uppercase tracking-tighter mt-2">ready to issue</p>
                </div>

                <div class="bg-white dark:bg-slate-900 rounded-[2rem] p-6 border border-slate-200/60 dark:border-slate-800 shadow-sm dark:shadow-none transition-colors">
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Issued</span>
                        <i class="fa fa-hand-paper-o text-amber-500 text-xl"></i>
                    </div>
                    <p class="text-3xl font-black text-amber-600">{{ issuedBooks }}</p>
                    <p class="text-[10px] font-bold text-slate-300 uppercase tracking-tighter mt-2">currently out</p>
                </div>

                <div class="bg-white dark:bg-slate-900 rounded-[2rem] p-6 border border-slate-200/60 dark:border-slate-800 shadow-sm dark:shadow-none transition-colors">
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Low Stock</span>
                        <i class="fa fa-warning text-red-500 text-xl"></i>
                    </div>
                    <p class="text-3xl font-black text-red-600">{{ lowStockBooks }}</p>
                    <p class="text-[10px] font-bold text-slate-300 uppercase tracking-tighter mt-2">need reorder</p>
                </div>
            </div>

            <!-- FILTERS & SEARCH -->
            <div class="bg-white dark:bg-slate-900 rounded-[2.5rem] shadow-sm dark:shadow-none border border-slate-200/60 dark:border-slate-800 p-6 transition-colors">
                <div class="space-y-4">
                    <div class="flex flex-col lg:flex-row gap-4">
                        <div class="flex-1">
                            <span
                                class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-3 block">Search
                                Books</span>
                            <div class="relative">
                                <i class="fa fa-search absolute left-4 top-1/2 -translate-y-1/2 text-slate-300"></i>
                                <input v-model="searchQuery" type="text"
                                    placeholder="Search by title, author, or ISBN..."
                                    class="w-full bg-slate-50 border border-slate-100 rounded-2xl pl-12 pr-4 py-3 text-xs font-bold text-slate-700 outline-none focus:ring-4 focus:ring-indigo-500/10" />
                            </div>
                        </div>
                        <div class="w-full lg:w-48">
                            <span
                                class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-3 block">Category</span>
                            <select v-model="selectedCategory"
                                class="w-full bg-slate-50 border border-slate-100 rounded-2xl px-4 py-3 text-xs font-bold text-slate-700 outline-none focus:ring-4 focus:ring-indigo-500/10">
                                <option value="">All Categories</option>
                                <option value="CS">Computer Science</option>
                                <option value="Math">Mathematics</option>
                                <option value="Science">Science</option>
                                <option value="Literature">Literature</option>
                                <option value="Reference">Reference</option>
                            </select>
                        </div>
                    </div>

                    <div class="flex gap-2 overflow-x-auto no-scrollbar pb-2">
                        <button v-for="filter in filters" :key="filter.id" @click="activeFilter = filter.id" :class="[
                            activeFilter === filter.id
                                ? 'bg-slate-900 text-white shadow-lg'
                                : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-white',
                            'px-6 py-2.5 rounded-2xl text-[10px] font-black uppercase tracking-widest border transition-all whitespace-nowrap'
                        ]">
                            {{ filter.label }}
                        </button>
                    </div>
                </div>
            </div>

            <!-- BOOKS TABLE -->
            <div class="bg-white dark:bg-slate-900 rounded-[2.5rem] shadow-sm dark:shadow-none border border-slate-200/60 dark:border-slate-800 overflow-hidden transition-colors">
                <div
                    class="p-8 border-b border-slate-50 dark:border-slate-800 flex justify-between items-center backdrop-blur-xl bg-gradient-to-r from-slate-50 dark:from-slate-800/50 to-transparent transition-colors">
                    <div>
                        <h3 class="text-sm font-black text-slate-800 uppercase tracking-widest">Book Inventory</h3>
                        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-tighter mt-1">{{
                            filteredBooks.length }} records</p>
                    </div>
                    <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Total: {{ books.length
                        }}</span>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-50/50 border-b border-slate-100">
                                <th class="px-8 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">
                                    Book Information</th>
                                <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">
                                    Category</th>
                                <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">
                                    ISBN</th>
                                <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">
                                    Shelf</th>
                                <th
                                    class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest text-center">
                                    Total / Available</th>
                                <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">
                                    Status</th>
                                <th
                                    class="px-8 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest text-right">
                                    Action</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-50">
                            <tr v-for="book in filteredBooks" :key="book.id"
                                class="hover:bg-slate-50/30 transition-colors group">
                                <td class="px-8 py-5">
                                    <div class="flex items-center gap-4">
                                        <div
                                            :class="['h-12 w-12 rounded-2xl flex items-center justify-center border text-white font-black text-lg', book.iconBg]">
                                            <i :class="['fa', book.icon]"></i>
                                        </div>
                                        <div class="flex flex-col">
                                            <span class="text-sm font-black text-slate-700">{{ book.title }}</span>
                                            <span
                                                class="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">{{
                                                book.author }}</span>
                                        </div>
                                    </div>
                                </td>
                                <td class="px-6 py-5">
                                    <span
                                        :class="['px-3 py-1.5 text-[9px] font-black uppercase rounded-lg border', book.categoryBadge]">
                                        {{ book.category }}
                                    </span>
                                </td>
                                <td class="px-6 py-5 text-xs font-bold text-slate-600">{{ book.isbn }}</td>
                                <td class="px-6 py-5 text-xs font-bold text-slate-600">{{ book.shelf }}</td>
                                <td class="px-6 py-5">
                                    <div class="flex items-center justify-center gap-2">
                                        <span class="text-xs font-bold text-slate-700">{{ book.available }}/{{
                                            book.total }}</span>
                                        <div class="w-20 h-2 bg-slate-100 rounded-full overflow-hidden">
                                            <div class="h-full transition-all"
                                                :class="book.available / book.total > 0.5 ? 'bg-green-500' : book.available / book.total > 0.2 ? 'bg-amber-500' : 'bg-red-500'"
                                                :style="{ width: (book.available / book.total) * 100 + '%' }"></div>
                                        </div>
                                    </div>
                                </td>
                                <td class="px-6 py-5">
                                    <span :class="[
                                        book.available === 0 ? 'bg-red-50 text-red-600 border-red-100'
                                            : book.available <= 2 ? 'bg-amber-50 text-amber-600 border-amber-100'
                                                : 'bg-green-50 text-green-600 border-green-100',
                                        'px-3 py-1.5 text-[9px] font-black uppercase tracking-wider rounded-lg border'
                                    ]">
                                        {{ book.available === 0 ? 'Out of Stock' : book.available <= 2 ? 'Low Stock'
                                            : 'Available' }} </span>
                                </td>
                                <td class="px-8 py-5 text-right">
                                    <div class="flex justify-end gap-2">
                                        <button
                                            class="px-3 py-1.5 bg-slate-100 text-slate-600 rounded-lg text-[9px] font-black uppercase hover:bg-slate-900 hover:text-white transition-all">
                                            <i class="fa fa-pencil mr-1"></i> Edit
                                        </button>
                                        <button
                                            class="px-3 py-1.5 bg-slate-100 text-slate-600 rounded-lg text-[9px] font-black uppercase hover:bg-red-500 hover:text-white transition-all">
                                            <i class="fa fa-trash mr-1"></i> Delete
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            <tr v-if="filteredBooks.length === 0">
                                <td colspan="7" class="px-8 py-12 text-center">
                                    <i class="fa fa-inbox text-slate-100 text-5xl mb-4 block"></i>
                                    <p class="text-sm font-black text-slate-400 uppercase">No books found</p>
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

const searchQuery = ref('');
const selectedCategory = ref('');
const activeFilter = ref('all');

const filters = [
    { id: 'all', label: 'All Books' },
    { id: 'available', label: 'In Stock' },
    { id: 'low', label: 'Low Stock' },
    { id: 'outofstock', label: 'Out of Stock' }
];

// DEMO DATA
const books = ref([
    {
        id: 1,
        title: 'Advanced Data Structures',
        author: 'Mark Allen Weiss',
        isbn: '978-0-201-61621-4',
        category: 'CS',
        categoryBadge: 'bg-blue-50 text-blue-600 border-blue-100',
        shelf: 'A1-02',
        total: 5,
        available: 3,
        icon: 'fa-database',
        iconBg: 'bg-blue-600'
    },
    {
        id: 2,
        title: 'Introduction to Algorithms',
        author: 'Cormen, Leiserson, Rivest',
        isbn: '978-0-262-03384-8',
        category: 'CS',
        categoryBadge: 'bg-blue-50 text-blue-600 border-blue-100',
        shelf: 'A1-01',
        total: 8,
        available: 2,
        icon: 'fa-code',
        iconBg: 'bg-blue-600'
    },
    {
        id: 3,
        title: 'Design Patterns',
        author: 'Gang of Four',
        isbn: '978-0-201-63361-0',
        category: 'CS',
        categoryBadge: 'bg-blue-50 text-blue-600 border-blue-100',
        shelf: 'A2-05',
        total: 6,
        available: 4,
        icon: 'fa-puzzle-piece',
        iconBg: 'bg-blue-600'
    },
    {
        id: 4,
        title: 'Operating Systems Concepts',
        author: 'Abraham Silberschatz',
        isbn: '978-0-470-12872-5',
        category: 'CS',
        categoryBadge: 'bg-blue-50 text-blue-600 border-blue-100',
        shelf: 'A2-03',
        total: 7,
        available: 0,
        icon: 'fa-cogs',
        iconBg: 'bg-blue-600'
    },
    {
        id: 5,
        title: 'Database Management Systems',
        author: 'Raghu Ramakrishnan',
        isbn: '978-0-07-246563-1',
        category: 'CS',
        categoryBadge: 'bg-blue-50 text-blue-600 border-blue-100',
        shelf: 'A3-01',
        total: 5,
        available: 1,
        icon: 'fa-database',
        iconBg: 'bg-blue-600'
    },
    {
        id: 6,
        title: 'Computer Networks',
        author: 'Andrew S. Tanenbaum',
        isbn: '978-0-132-52619-8',
        category: 'CS',
        categoryBadge: 'bg-blue-50 text-blue-600 border-blue-100',
        shelf: 'A1-04',
        total: 6,
        available: 5,
        icon: 'fa-sitemap',
        iconBg: 'bg-blue-600'
    },
    {
        id: 7,
        title: 'Calculus: Early Transcendentals',
        author: 'James Stewart',
        isbn: '978-1-285-74155-0',
        category: 'Math',
        categoryBadge: 'bg-purple-50 text-purple-600 border-purple-100',
        shelf: 'B1-02',
        total: 9,
        available: 6,
        icon: 'fa-superscript',
        iconBg: 'bg-purple-600'
    },
    {
        id: 8,
        title: 'Linear Algebra Done Right',
        author: 'Sheldon Axler',
        isbn: '978-3-319-11080-6',
        category: 'Math',
        categoryBadge: 'bg-purple-50 text-purple-600 border-purple-100',
        shelf: 'B1-01',
        total: 4,
        available: 2,
        icon: 'fa-square',
        iconBg: 'bg-purple-600'
    },
    {
        id: 9,
        title: 'Physics for Scientists and Engineers',
        author: 'Serway & Jewett',
        isbn: '978-1-133-95405-3',
        category: 'Science',
        categoryBadge: 'bg-green-50 text-green-600 border-green-100',
        shelf: 'C1-03',
        total: 7,
        available: 3,
        icon: 'fa-flask',
        iconBg: 'bg-green-600'
    },
    {
        id: 10,
        title: 'Chemistry: The Central Science',
        author: 'Brown, LeMay, Bursten',
        isbn: '978-0-321-69637-0',
        category: 'Science',
        categoryBadge: 'bg-green-50 text-green-600 border-green-100',
        shelf: 'C2-01',
        total: 8,
        available: 4,
        icon: 'fa-flask',
        iconBg: 'bg-green-600'
    },
    {
        id: 11,
        title: 'Biology: A Global Approach',
        author: 'Campbell, Reece',
        isbn: '978-0-321-55823-0',
        category: 'Science',
        categoryBadge: 'bg-green-50 text-green-600 border-green-100',
        shelf: 'C1-05',
        total: 6,
        available: 6,
        icon: 'fa-leaf',
        iconBg: 'bg-green-600'
    },
    {
        id: 12,
        title: 'To Kill a Mockingbird',
        author: 'Harper Lee',
        isbn: '978-0-06-112008-4',
        category: 'Literature',
        categoryBadge: 'bg-amber-50 text-amber-600 border-amber-100',
        shelf: 'D1-02',
        total: 10,
        available: 7,
        icon: 'fa-book',
        iconBg: 'bg-amber-600'
    },
    {
        id: 13,
        title: '1984',
        author: 'George Orwell',
        isbn: '978-0-451-52494-2',
        category: 'Literature',
        categoryBadge: 'bg-amber-50 text-amber-600 border-amber-100',
        shelf: 'D1-01',
        total: 8,
        available: 2,
        icon: 'fa-book',
        iconBg: 'bg-amber-600'
    },
    {
        id: 14,
        title: 'Pride and Prejudice',
        author: 'Jane Austen',
        isbn: '978-0-141-43951-8',
        category: 'Literature',
        categoryBadge: 'bg-amber-50 text-amber-600 border-amber-100',
        shelf: 'D2-03',
        total: 5,
        available: 1,
        icon: 'fa-book',
        iconBg: 'bg-amber-600'
    },
    {
        id: 15,
        title: 'Oxford English Dictionary',
        author: 'Multiple',
        isbn: '978-0-199-60001-6',
        category: 'Reference',
        categoryBadge: 'bg-slate-50 text-slate-600 border-slate-100',
        shelf: 'E1-01',
        total: 2,
        available: 2,
        icon: 'fa-globe',
        iconBg: 'bg-slate-600'
    }
]);

const filteredBooks = computed(() => {
    let result = books.value;

    // Search filter
    if (searchQuery.value) {
        result = result.filter(b =>
            b.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            b.author.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            b.isbn.includes(searchQuery.value)
        );
    }

    // Category filter
    if (selectedCategory.value) {
        result = result.filter(b => b.category === selectedCategory.value);
    }

    // Status filter
    switch (activeFilter.value) {
        case 'available':
            result = result.filter(b => b.available > 2);
            break;
        case 'low':
            result = result.filter(b => b.available > 0 && b.available <= 2);
            break;
        case 'outofstock':
            result = result.filter(b => b.available === 0);
            break;
    }

    return result;
});

const totalBooks = computed(() => {
    return books.value.reduce((sum, b) => sum + b.total, 0);
});

const uniqueTitles = computed(() => {
    return books.value.length;
});

const availableBooks = computed(() => {
    return books.value.reduce((sum, b) => sum + b.available, 0);
});

const issuedBooks = computed(() => {
    return totalBooks.value - availableBooks.value;
});

const lowStockBooks = computed(() => {
    return books.value.filter(b => b.available > 0 && b.available <= 2).length;
});
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
    display: none;
}
</style>