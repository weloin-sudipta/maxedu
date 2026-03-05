<template>
  <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden animate-in fade-in duration-500">
    
    <div class="flex flex-col lg:flex-row justify-between items-center p-8 gap-6 border-b border-slate-50">
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

      <div class="flex flex-col sm:flex-row items-end gap-4 w-full lg:w-auto">
        <div class="w-full sm:w-72">
          <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 block">Catalog Search</span>
          <div class="relative">
            <i class="fa fa-search absolute left-4 top-1/2 -translate-y-1/2 text-slate-300"></i>
            <input 
              v-model="searchQuery"
              type="search" 
              placeholder="Book Title or Author..." 
              class="w-full bg-slate-50 border border-slate-100 rounded-xl pl-10 pr-4 py-2 text-xs font-bold text-slate-700 outline-none focus:ring-2 focus:ring-indigo-500/20 transition-all"
            />
          </div>
        </div>
        
        <div class="flex gap-2 w-full sm:w-auto">
          <button class="btn-icon h-10 w-10"><i class="fa fa-download"></i></button>
          <button class="btn-primary flex items-center gap-2">
            <i class="fa fa-plus"></i> Suggest New Book
          </button>
        </div>
      </div>
    </div>

    <div class="overflow-x-auto min-h-[300px]">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-slate-50/50">
            <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">Book Information</th>
            <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">Shelf / Location</th>
            <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">Category</th>
            <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">Status</th>
            <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest text-right">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-50">
          <tr v-for="book in paginatedCatalog" :key="book.id" class="hover:bg-slate-50/30 transition-colors group">
            <td class="px-6 py-5">
              <div class="flex items-center gap-4">
                <div class="h-10 w-10 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center border border-indigo-100 shrink-0">
                  <i class="fa fa-book text-xs"></i>
                </div>
                <div class="flex flex-col">
                  <span class="text-sm font-black text-slate-700 group-hover:text-indigo-600 transition-colors">{{ book.title }}</span>
                  <span class="text-[10px] font-bold text-slate-400">By {{ book.author }}</span>
                </div>
              </div>
            </td>
            <td class="px-6 py-5">
              <span class="text-xs font-black text-slate-600 px-3 py-1 bg-slate-100 rounded-lg border border-slate-200/50">{{ book.shelf }}</span>
            </td>
            <td class="px-6 py-5">
              <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{{ book.category }}</span>
            </td>
            <td class="px-6 py-5">
              <span :class="['px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-tighter shadow-sm border', book.available ? 'bg-green-50 text-green-600 border-green-100' : 'bg-red-50 text-red-500 border-red-100']">
                {{ book.available ? 'Available' : 'Issued Out' }}
              </span>
            </td>
            <td class="px-6 py-5 text-right">
              <button 
                :disabled="!book.available"
                class="px-5 py-3 rounded-xl text-[9px] font-black uppercase tracking-widest transition-all shadow-sm"
                :class="book.available ? 'bg-indigo-600 text-white hover:bg-slate-900 shadow-indigo-100' : 'bg-slate-100 text-slate-300 cursor-not-allowed'"
              >
                Request Pickup
              </button>
            </td>
          </tr>
          <tr v-if="filteredCatalog.length === 0">
            <td colspan="6" class="px-8 py-20 text-center">
               <i class="fa fa-search text-slate-200 text-3xl mb-4"></i>
               <p class="text-xs font-black text-slate-400 uppercase tracking-widest">No books found matching your search</p>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="flex flex-col md:flex-row justify-between items-center p-8 bg-slate-50/30 border-t border-slate-100 gap-4">
      <span class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">
        Showing {{ filteredCatalog.length === 0 ? 0 : (currentPage - 1) * itemsPerPage + 1 }} - 
        {{ Math.min(currentPage * itemsPerPage, filteredCatalog.length) }} of 
        {{ filteredCatalog.length }} Books
      </span>
      
      <div v-if="totalPages > 0" class="flex items-center gap-2">
        <button 
          @click="currentPage--" 
          :disabled="currentPage === 1"
          class="page-btn-fixed"
        >
          <i class="fa fa-chevron-left text-xs text-slate-400"></i>
        </button>
        
        <div class="flex gap-1">
          <button 
            v-for="page in totalPages" 
            :key="page"
            @click="currentPage = page"
            :class="[
              'w-10 h-10 rounded-xl text-xs font-black transition-all shadow-sm', 
              currentPage === page 
                ? 'bg-slate-900 text-white shadow-slate-200' 
                : 'bg-white text-slate-500 border border-slate-200 hover:border-indigo-400'
            ]"
          >
            {{ page }}
          </button>
        </div>

        <button 
          @click="currentPage++" 
          :disabled="currentPage === totalPages"
          class="page-btn-fixed"
        >
          <i class="fa fa-chevron-right text-xs text-slate-400"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const searchQuery = ref('');
const itemsPerPage = ref(5);
const currentPage = ref(1);

const catalog = ref([
  { id: 101, title: 'The Art of Electronics', author: 'Horowitz', shelf: 'S-12', category: 'Physics', available: true },
  { id: 102, title: 'Inorganic Chemistry', author: 'J.D. Lee', shelf: 'C-04', category: 'Chemistry', available: false },
  { id: 103, title: 'Modern World History', author: 'Norman Lowe', shelf: 'H-01', category: 'History', available: true },
  { id: 104, title: 'Calculus Vol II', author: 'Apostol', shelf: 'M-15', category: 'Math', available: true },
  { id: 105, title: 'Clean Code', author: 'Robert Martin', shelf: 'CS-09', category: 'Computer Science', available: true },
  { id: 106, title: 'The Great Gatsby', author: 'Fitzgerald', shelf: 'L-01', category: 'Literature', available: true },
  { id: 107, title: 'Atomic Habits', author: 'James Clear', shelf: 'SL-02', category: 'Self-Help', available: true },
]);

const filteredCatalog = computed(() => {
  return catalog.value.filter(book => 
    book.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    book.author.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const totalPages = computed(() => {
  const pages = Math.ceil(filteredCatalog.value.length / itemsPerPage.value);
  return pages > 0 ? pages : 0;
});

const paginatedCatalog = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  return filteredCatalog.value.slice(start, start + itemsPerPage.value);
});

// Watch search to reset page, preventing empty views
watch(searchQuery, () => {
  currentPage.value = 1;
});

// Watch itemsPerPage to reset page
watch(itemsPerPage, () => {
  currentPage.value = 1;
});
</script>

<style scoped>
.btn-primary { @apply px-6 py-2.5 bg-indigo-600 text-white rounded-xl text-[10px] font-black uppercase tracking-[0.2em] shadow-xl shadow-indigo-100 hover:bg-indigo-700 active:scale-95 transition-all; }
.btn-icon { @apply flex items-center justify-center bg-white border border-slate-200 text-slate-400 rounded-xl hover:text-indigo-600 hover:border-indigo-100 transition-all; }
.page-btn-fixed { @apply p-2 w-10 h-10 rounded-xl bg-white border border-slate-200 disabled:opacity-30 disabled:cursor-not-allowed hover:border-indigo-500 transition-all shadow-sm flex items-center justify-center; }
</style>