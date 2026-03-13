<template>
  <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden animate-in fade-in duration-500">

    <!-- Header -->
    <div class="flex flex-col lg:flex-row justify-between items-center p-8 gap-6 border-b border-slate-50">
      
      <!-- Rows per page -->
      <div class="flex items-center gap-4">
        <div class="flex flex-col">
          <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5">View Count</span>
          <select v-model="itemsPerPage" class="bg-slate-50 border border-slate-100 rounded-xl px-4 py-2 text-xs font-bold text-slate-700 outline-none focus:ring-2 focus:ring-indigo-500/20">
            <option :value="5">5 Rows</option>
            <option :value="10">10 Rows</option>
            <option :value="25">25 Rows</option>
          </select>
        </div>
      </div>

      <!-- Search & Buttons -->
      <div class="flex flex-col sm:flex-row items-end gap-4 w-full lg:w-auto">
        <div class="w-full sm:w-72">
          <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 block">Search My Books</span>
          <div class="relative">
            <i class="fa fa-search absolute left-4 top-1/2 -translate-y-1/2 text-slate-300"></i>
            <input 
              v-model="searchQuery"
              type="search" 
              placeholder="Title or isbn No..." 
              class="w-full bg-slate-50 border border-slate-100 rounded-xl pl-10 pr-4 py-2 text-xs font-bold text-slate-700 outline-none focus:ring-2 focus:ring-indigo-500/20 transition-all"
            />
          </div>
        </div>
        
        <div class="flex gap-2 w-full sm:w-auto">
          <button class="btn-icon h-10 w-10"><i class="fa fa-print"></i></button>
          <button class="btn-primary flex items-center gap-2">
            <i class="fa fa-history"></i> Request Renewal
          </button>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto min-h-[300px]">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-slate-50/50">
            <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">Book Details</th>
            <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">ISBN No</th>
            <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">Issue Date</th>
            <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">Due Date</th>
            <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest text-right">Status</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-50">
          <tr v-for="book in paginatedBooks" :key="book.name" class="hover:bg-slate-50/30 transition-colors group">
            
            <!-- Book Details -->
            <td class="px-6 py-5">
              <div class="flex items-center gap-4">
                <div class="h-10 w-10 rounded-2xl bg-slate-50 text-slate-400 flex items-center justify-center border border-slate-100 shrink-0 group-hover:bg-indigo-50 group-hover:text-indigo-600 transition-colors">
                  <i class="fa fa-book text-xs"></i>
                </div>
                <div class="flex flex-col">
                  <span class="text-sm font-black text-slate-700 group-hover:text-indigo-600 transition-colors">{{ book.book_title }}</span>
                  <span class="text-[10px] font-bold text-slate-400">By {{ book.member_name }}</span>
                </div>
              </div>
            </td>

            <!-- Accession No -->
            <td class="px-6 py-5">
              <span class="text-xs font-black text-slate-600 px-3 py-1 bg-slate-100 rounded-lg border border-slate-200/50 uppercase">{{ book.book_isbn }}</span>
            </td>

            <!-- Issue Date -->
            <td class="px-6 py-5">
              <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{{ book.issue_date }}</span>
            </td>

            <!-- Due Date -->
            <td class="px-6 py-5">
              <div class="flex flex-col">
                <span class="text-xs font-black text-red-500">{{ book.due_date }}</span>
                <span class="text-[9px] font-bold text-slate-300 uppercase tracking-tighter">Please return by 4PM</span>
              </div>
            </td>

            <!-- Status -->
            <td class="px-6 py-5 text-right">
              <span class="px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-tighter shadow-sm border bg-amber-50 text-amber-600 border-amber-100">
                {{ book.status }}
              </span>
            </td>
          </tr>

          <!-- No Records -->
          <tr v-if="filteredBooks.length === 0">
            <td colspan="6" class="px-8 py-20 text-center">
               <i class="fa fa-folder-open-o text-slate-200 text-3xl mb-4"></i>
               <p class="text-xs font-black text-slate-400 uppercase tracking-widest">No matching issued books found</p>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div class="flex flex-col md:flex-row justify-between items-center p-8 bg-slate-50/30 border-t border-slate-100 gap-4">
      <span class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">
        Showing {{ filteredBooks.length === 0 ? 0 : (currentPage - 1) * itemsPerPage + 1 }} - 
        {{ Math.min(currentPage * itemsPerPage, filteredBooks.length) }} of 
        {{ filteredBooks.length }} Issued Books
      </span>
      
      <div v-if="totalPages > 0" class="flex items-center gap-2">
        <button @click="currentPage--" :disabled="currentPage === 1" class="page-btn-fixed">
          <i class="fa fa-chevron-left text-xs text-slate-400"></i>
        </button>
        
        <div class="flex gap-1">
          <button v-for="page in totalPages" :key="page" @click="currentPage = page"
            :class="[ 'w-10 h-10 rounded-xl text-xs font-black transition-all shadow-sm', 
              currentPage === page ? 'bg-slate-900 text-white shadow-slate-200' : 'bg-white text-slate-500 border border-slate-200 hover:border-indigo-400'
            ]">
            {{ page }}
          </button>
        </div>

        <button @click="currentPage++" :disabled="currentPage === totalPages" class="page-btn-fixed">
          <i class="fa fa-chevron-right text-xs text-slate-400"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useBooks } from '~/composable/useLibraryBooks';

const { data, loading, fetchData } = useBooks();

const searchQuery = ref('');
const itemsPerPage = ref(5);
const currentPage = ref(1);

// Fetch API data on mount
onMounted(async () => {
    await fetchData();
});

// Only "Issued" books
const issuedBooks = computed(() => {
    if (!data.value) return [];
    return data.value.filter(book => book.status === "Issued");
});

// Filter by search query (title or ISBN)
const filteredBooks = computed(() => {
    return issuedBooks.value.filter(b =>
        b.book_title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        b.book_isbn.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
});

// Pagination
const totalPages = computed(() => Math.ceil(filteredBooks.value.length / itemsPerPage.value) || 0);
const paginatedBooks = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    return filteredBooks.value.slice(start, start + itemsPerPage.value);
});

// Reset page when search or itemsPerPage changes
watch(searchQuery, () => currentPage.value = 1);
watch(itemsPerPage, () => currentPage.value = 1);
</script>

<style scoped>
.btn-primary { @apply px-6 py-2.5 bg-indigo-600 text-white rounded-xl text-[10px] font-black uppercase tracking-[0.2em] shadow-xl shadow-indigo-100 hover:bg-indigo-700 active:scale-95 transition-all; }
.btn-icon { @apply flex items-center justify-center bg-white border border-slate-200 text-slate-400 rounded-xl hover:text-indigo-600 hover:border-indigo-100 transition-all; }
.page-btn-fixed { @apply p-2 w-10 h-10 rounded-xl bg-white border border-slate-200 disabled:opacity-30 disabled:cursor-not-allowed hover:border-indigo-500 transition-all shadow-sm flex items-center justify-center; }
</style>