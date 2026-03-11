<template>
  <div class="bg-white rounded-[2rem] lg:rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden animate-in fade-in duration-500">
    
    <div class="p-5 lg:p-8 border-b border-slate-50 space-y-6">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-6">
        <div>
          <h3 class="text-sm lg:text-base font-black text-slate-800 uppercase tracking-widest">Library Catalog</h3>
          <p class="text-[10px] font-bold text-slate-400 uppercase tracking-tighter mt-1">Explore academic resources</p>
        </div>
        <!-- <div class="flex gap-2 w-full sm:w-auto">
          <button class="btn-icon h-11 w-11 flex-shrink-0"><i class="fa fa-download"></i></button>
          <button class="btn-primary flex-1 sm:flex-none flex items-center justify-center gap-2 py-3">
            <i class="fa fa-plus"></i> <span class="hidden xs:inline">Suggest Book</span>
          </button>
        </div> -->
      </div>

      <div class="grid grid-cols-2 lg:grid-cols-5 gap-3 lg:gap-4">
        <div class="col-span-2">
          <span class="filter-label">Search Catalog</span>
          <div class="relative">
            <i class="fa fa-search absolute left-4 top-1/2 -translate-y-1/2 text-slate-300"></i>
            <input v-model="searchQuery" type="text" placeholder="Title or Author..." class="filter-input pl-10" />
          </div>
        </div>
        <div class="col-span-1">
          <span class="filter-label">Category</span>
          <select v-model="selectedCategory" class="filter-input">
            <option value="All">All</option>
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>
        <div class="col-span-1">
          <span class="filter-label">Type</span>
          <select v-model="selectedType" class="filter-input">
            <option value="All">All</option>
            <option value="Physical">Physical</option>
            <option value="Online">Online</option>
          </select>
        </div>
        <div class="col-span-2 lg:col-span-1">
          <span class="filter-label">Status</span>
          <select v-model="selectedStatus" class="filter-input">
            <option value="All">All Status</option>
            <option value="Available">Available</option>
            <option value="Issued Out">Issued Out</option>
          </select>
        </div>
      </div>
    </div>

    <div class="min-h-[400px]">
      <table class="w-full text-left border-collapse hidden md:table">
        <thead>
          <tr class="bg-slate-50/50">
            <th class="px-6 py-5 th-style">Book Information</th>
            <th class="px-6 py-5 th-style">Category</th>
            <th class="px-6 py-5 th-style">Copy Type</th>
            <th class="px-6 py-5 th-style text-center">Availability</th>
            <th class="px-6 py-5 th-style text-right">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-50">
          <tr v-for="book in paginatedCatalog" :key="book.id" class="hover:bg-slate-50/30 transition-colors group">
            <td class="px-6 py-5">
              <div class="flex items-center gap-4">
                <div class="h-10 w-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center border border-indigo-100 group-hover:bg-slate-900 group-hover:text-white transition-all">
                  <i :class="book.type === 'Online' ? 'fa fa-laptop' : 'fa fa-book'" class="text-xs"></i>
                </div>
                <div class="flex flex-col">
                  <span class="text-sm font-black text-slate-700 group-hover:text-indigo-600 transition-colors">{{ book.title }}</span>
                  <span class="text-[10px] font-bold text-slate-400 uppercase">By {{ book.author }}</span>
                </div>
              </div>
            </td>
            <td class="px-6 py-5">
              <div class="flex flex-col gap-1">
                <span class="text-[9px] font-black text-indigo-400 uppercase tracking-widest ml-1">{{ book.category }}</span>
              </div>
            </td>
            <td class="px-6 py-5">
              <span :class="['type-badge', book.type === 'Online' ? 'bg-purple-50 text-purple-600 border-purple-100' : 'bg-blue-50 text-blue-600 border-blue-100']">
                {{ book.type }}
              </span>
            </td>
            <td class="px-6 py-5 text-center">
              <span :class="['status-badge', isAvailable(book) ? 'bg-green-50 text-green-600 border-green-100' : 'bg-red-50 text-red-500 border-red-100']">
                {{ isAvailable(book) ? 'Available' : 'Issued Out' }}
              </span>
            </td>
            <td class="px-6 py-5 text-right">
              <button :disabled="!isAvailable(book)" :class="[isAvailable(book) ? 'btn-action-active' : 'btn-action-disabled']">
                {{ book.type === 'Online' ? 'Read Now' : 'Request' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="md:hidden divide-y divide-slate-100">
        <div v-for="book in paginatedCatalog" :key="'mob-'+book.id" class="p-5 space-y-4">
          <div class="flex justify-between items-start">
            <div class="flex gap-3">
              <div class="h-10 w-10 rounded-xl bg-slate-50 flex items-center justify-center text-slate-400 border border-slate-100">
                <i :class="book.type === 'Online' ? 'fa fa-laptop' : 'fa fa-book'"></i>
              </div>
              <div>
                <h4 class="text-sm font-black text-slate-800 leading-tight">{{ book.title }}</h4>
                <p class="text-[10px] font-bold text-slate-400 uppercase tracking-tight">By {{ book.author }}</p>
              </div>
            </div>
            <span :class="['status-badge', isAvailable(book) ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-500']">
              {{ isAvailable(book) ? 'Available' : 'Issued Out' }}
            </span>
          </div>
          <div class="flex items-center justify-between text-[10px] font-black uppercase tracking-widest">
            <span class="text-slate-400">{{ book.category }} • {{ book.shelf }}</span>
            <span :class="book.type === 'Online' ? 'text-purple-500' : 'text-blue-500'">{{ book.type }}</span>
          </div>
          <button :disabled="!isAvailable(book)" :class="['w-full py-3 rounded-xl text-[10px] font-black uppercase tracking-[0.2em]', isAvailable(book) ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-300']">
            {{ book.type === 'Online' ? 'Read Online' : 'Request Pickup' }}
          </button>
        </div>
      </div>

      <div v-if="filteredCatalog.length === 0" class="py-20 text-center">
         <i class="fa fa-search text-slate-100 text-5xl mb-4"></i>
         <p class="text-xs font-black text-slate-400 uppercase tracking-widest">No books found matching your filters</p>
      </div>
    </div>

    <div class="flex flex-col md:flex-row justify-between items-center p-6 lg:p-8 bg-slate-50/30 border-t border-slate-100 gap-6">
      <div class="flex items-center gap-4 w-full md:w-auto justify-between">
        <select v-model="itemsPerPage" class="bg-white border border-slate-200 rounded-lg px-3 py-2 text-[10px] font-black text-slate-500">
          <option :value="5">5 Rows</option>
          <option :value="10">10 Rows</option>
        </select>
        <span class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Total: {{ filteredCatalog.length }}</span>
      </div>
      
      <div v-if="totalPages > 1" class="flex items-center gap-2 overflow-x-auto pb-2 md:pb-0 max-w-full">
        <button @click="currentPage--" :disabled="currentPage === 1" class="page-btn"><i class="fa fa-chevron-left"></i></button>
        <button v-for="page in totalPages" :key="page" @click="currentPage = page"
          :class="['page-btn-num', currentPage === page ? 'bg-slate-900 text-white' : 'bg-white text-slate-500 border-slate-200']">
          {{ page }}
        </button>
        <button @click="currentPage++" :disabled="currentPage === totalPages" class="page-btn"><i class="fa fa-chevron-right"></i></button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const searchQuery = ref('');
const selectedCategory = ref('All');
const selectedType = ref('All');
const selectedStatus = ref('All');
const itemsPerPage = ref(5);
const currentPage = ref(1);

const categories = ['Physics', 'Chemistry', 'History', 'Math', 'Computer Science', 'Literature', 'Self-Help'];

const catalog = ref([
  { id: 101, title: 'The Art of Electronics', author: 'Horowitz', shelf: 'S-12', category: 'Physics', type: 'Physical', available: true },
  { id: 102, title: 'Inorganic Chemistry', author: 'J.D. Lee', shelf: 'C-04', category: 'Chemistry', type: 'Online', available: false }, // Will be forced to true
  { id: 103, title: 'Modern World History', author: 'Norman Lowe', shelf: 'H-01', category: 'History', type: 'Physical', available: true },
  { id: 104, title: 'Calculus Vol II', author: 'Apostol', shelf: 'M-15', category: 'Math', type: 'Physical', available: true },
  { id: 105, title: 'Clean Code', author: 'Robert Martin', shelf: 'CS-09', category: 'Computer Science', type: 'Online', available: true },
  { id: 106, title: 'The Great Gatsby', author: 'Fitzgerald', shelf: 'L-01', category: 'Literature', type: 'Physical', available: true },
]);

// LOGIC: Online copies are ALWAYS available
const isAvailable = (book) => book.type === 'Online' || book.available;

const filteredCatalog = computed(() => {
  return catalog.value.filter(book => {
    const matchesSearch = book.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         book.author.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesCat = selectedCategory.value === 'All' || book.category === selectedCategory.value;
    const matchesType = selectedType.value === 'All' || book.type === selectedType.value;
    const matchesStatus = selectedStatus.value === 'All' || 
                         (selectedStatus.value === 'Available' ? isAvailable(book) : !isAvailable(book));
    
    return matchesSearch && matchesCat && matchesType && matchesStatus;
  });
});

const totalPages = computed(() => Math.ceil(filteredCatalog.value.length / itemsPerPage.value) || 0);
const paginatedCatalog = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  return filteredCatalog.value.slice(start, start + itemsPerPage.value);
});

watch([searchQuery, selectedCategory, selectedType, selectedStatus, itemsPerPage], () => currentPage.value = 1);
</script>

<style scoped>
.filter-label { @apply text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 block ml-1; }
.filter-input { @apply w-full bg-slate-50 border border-slate-100 rounded-xl px-4 py-2.5 text-xs font-bold text-slate-700 outline-none focus:ring-4 focus:ring-indigo-500/10 transition-all; }
.th-style { @apply text-[10px] font-black uppercase text-slate-400 tracking-widest; }
.type-badge { @apply px-3 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest border shadow-sm; }
.status-badge { @apply px-3 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-tighter shadow-sm border; }
.btn-primary { @apply bg-indigo-600 text-white rounded-xl text-[10px] font-black uppercase tracking-[0.2em] shadow-xl shadow-indigo-100 hover:bg-indigo-700 active:scale-95 transition-all; }
.btn-icon { @apply flex items-center justify-center bg-white border border-slate-200 text-slate-400 rounded-xl hover:text-indigo-600 transition-all; }
.btn-action-active { @apply px-5 py-3 rounded-xl bg-indigo-600 text-white text-[9px] font-black uppercase tracking-widest hover:bg-slate-900 shadow-sm active:scale-95 transition-all; }
.btn-action-disabled { @apply px-5 py-3 rounded-xl bg-slate-50 text-slate-300 border border-slate-100 text-[9px] font-black uppercase tracking-widest cursor-not-allowed; }
.page-btn { @apply p-2 w-10 h-10 rounded-xl bg-white border border-slate-200 disabled:opacity-30 flex items-center justify-center text-xs text-slate-400; }
.page-btn-num { @apply w-10 h-10 rounded-xl text-xs font-black transition-all shadow-sm border flex items-center justify-center; }
</style>