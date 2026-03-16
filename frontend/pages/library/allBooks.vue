<template>
  <div class="bg-white rounded-[2rem] lg:rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden animate-in fade-in duration-500">
    
    <div class="p-5 lg:p-8 border-b border-slate-50 space-y-6">
      <div class="flex flex-col lg:flex-row justify-between items-end gap-6">
        
        <div class="flex flex-col">
          <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">View Count</span>
          <select v-model="itemsPerPage" class="bg-slate-50 border border-slate-100 rounded-xl px-4 py-2.5 text-xs font-bold text-slate-700 outline-none focus:ring-4 focus:ring-indigo-500/10 transition-all w-32">
            <option :value="5">5 Rows</option>
            <option :value="10">10 Rows</option>
            <option :value="25">25 Rows</option>
          </select>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 w-full lg:w-auto flex-1 max-w-4xl">
          <div class="sm:col-span-1">
            <span class="filter-label">Search Catalog</span>
            <div class="relative">
              <i class="fa fa-search absolute left-4 top-1/2 -translate-y-1/2 text-slate-300"></i>
              <input v-model="searchQuery" type="text" placeholder="Title or Author..." class="filter-input" />
            </div>
          </div>

          <div>
            <span class="filter-label">Category</span>
            <select v-model="selectedCategory" class="filter-input !pl-4">
              <option value="All">All Categories</option>
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
          </div>

          <div>
            <span class="filter-label">Type</span>
            <select v-model="selectedType" class="filter-input !pl-4">
              <option value="All">All Types</option>
              <option value="Physical">Physical</option>
              <option value="Online">Online</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <div class="min-h-[400px] relative">
      <div v-if="loading" class="absolute inset-0 bg-white/60 backdrop-blur-[2px] z-10 flex flex-col items-center justify-center">
         <i class="fa fa-circle-o-notch fa-spin text-indigo-600 text-3xl mb-4"></i>
         <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Synchronizing...</p>
      </div>

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
          <tr v-for="book in paginatedCatalog" :key="book.name" class="hover:bg-slate-50/30 transition-colors group">
            <td class="px-6 py-5">
              <div class="flex items-center gap-4">
                <div class="h-10 w-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center border border-indigo-100 group-hover:bg-slate-900 group-hover:text-white transition-all">
                  <i :class="book.copy_type === 'Online' ? 'fa fa-laptop' : 'fa fa-book'" class="text-xs"></i>
                </div>
                <div class="flex flex-col">
                  <span class="text-sm font-black text-slate-700 group-hover:text-indigo-600 transition-colors">{{ book.title }}</span>
                  <span class="text-[10px] font-bold text-slate-400 uppercase">By {{ book.author }}</span>
                </div>
              </div>
            </td>
            <td class="px-6 py-5">
              <span class="text-[9px] font-black text-indigo-400 uppercase tracking-widest ml-1">{{ book.category || 'General' }}</span>
            </td>
            <td class="px-6 py-5">
              <span :class="['type-badge', book.copy_type === 'Online' ? 'bg-purple-50 text-purple-600 border-purple-100' : 'bg-blue-50 text-blue-600 border-blue-100']">
                {{ book.copy_type }}
              </span>
            </td>
            <td class="px-6 py-5 text-center">
              <span :class="['status-badge', isAvailable(book) ? 'bg-green-50 text-green-600 border-green-100' : 'bg-rose-50 text-rose-600 border-rose-100']">
                {{ isAvailable(book) ? 'Available' : 'Issued Out' }}
              </span>
            </td>
            <td class="px-6 py-5 text-right">
              <!--
                Button logic:
                1. Online book       → always "Read Now" (blue/active)
                2. Pending request   → "Cancel Request" (red)
                3. Available book    → "Request" (indigo)
                4. Unavailable book  → "Reserve" (purple)
              -->
              <template v-if="book.copy_type === 'Online'">
                <button @click="handleBookRequest(book, true)" class="btn-action-active" :disabled="bookRequest.loading.value">
                  <i v-if="bookRequest.loading.value" class="fa fa-spinner fa-spin mr-2"></i>
                  Read Now
                </button>
              </template>

              <template v-else-if="bookRequest.isBookRequested(book.name)">
                <!-- User already has a pending request → show Cancel -->
                <button @click="handleBookRequest(book, isAvailable(book))" class="btn-cancel" :disabled="bookRequest.loading.value">
                  <i v-if="bookRequest.loading.value" class="fa fa-spinner fa-spin mr-2"></i>
                  Cancel Request
                </button>
              </template>

              <template v-else>
                <!-- No request yet → Request (available) or Reserve (unavailable) -->
                <button @click="handleBookRequest(book, isAvailable(book))" :class="isAvailable(book) ? 'btn-action-active' : 'btn-reserve'" :disabled="bookRequest.loading.value">
                  <i v-if="bookRequest.loading.value" class="fa fa-spinner fa-spin mr-2"></i>
                  {{ isAvailable(book) ? 'Request' : 'Reserve' }}
                </button>
              </template>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="!loading && filteredCatalog.length === 0" class="p-20 text-center">
          <i class="fa fa-folder-open-o text-slate-200 text-3xl mb-4"></i>
          <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">No books found matching your criteria</p>
      </div>
    </div>

    <div class="flex flex-col md:flex-row justify-between items-center p-8 bg-slate-50/30 border-t border-slate-100 gap-4">
      <span class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">
        Showing {{ filteredCatalog.length === 0 ? 0 : (currentPage - 1) * itemsPerPage + 1 }} - 
        {{ Math.min(currentPage * itemsPerPage, filteredCatalog.length) }} of 
        {{ filteredCatalog.length }} Resources
      </span>
      
      <div v-if="totalPages > 0" class="flex items-center gap-2">
        <button @click="currentPage--" :disabled="currentPage === 1" class="page-btn-fixed">
          <i class="fa fa-chevron-left text-xs"></i>
        </button>
        
        <div class="flex gap-1">
          <button v-for="page in totalPages" :key="page" @click="currentPage = page"
            :class="[ 'w-10 h-10 rounded-xl text-xs font-black transition-all shadow-sm flex items-center justify-center', 
              currentPage === page ? 'bg-slate-900 text-white shadow-slate-200' : 'bg-white text-slate-500 border border-slate-200 hover:border-indigo-400'
            ]">
            {{ page }}
          </button>
        </div>

        <button @click="currentPage++" :disabled="currentPage === totalPages" class="page-btn-fixed">
          <i class="fa fa-chevron-right text-xs"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useBooks } from '~/composable/useLibraryBooks';
import { useBookRequest } from '~/composable/useBookRequest';

// ─── NEW: import the borrowed books composable ────────────────────────────────
// This gives us the set of book IDs the user currently has issued (checked out).
// We use `all_borrowed_books` API which returns Book Issue records with status "Issued".
import { useBorrowedBooks } from '~/composable/useBorrowedBooks';

const { loading, allBooks, fetchAllBooks } = useBooks();
const bookRequest = useBookRequest();

// ─── NEW: fetch borrowed books so we can exclude them from the catalog ────────
const { borrowedBookNames, fetchBorrowedBooks } = useBorrowedBooks();

const searchQuery = ref('');
const selectedCategory = ref('All');
const selectedType = ref('All');
const selectedStatus = ref('All');
const itemsPerPage = ref(10);
const currentPage = ref(1);
// const getPendingRequestData = await getPendingRequest();
// console.log('Pending Requests:', getPendingRequestData);
onMounted(async () => {
  await bookRequest.init();
  await fetchBorrowedBooks(); // ← load issued books before rendering catalog
  await fetchAllBooks();
});

const isAvailable = (book) => book.copy_type === 'Online' || book.status === 'Available';

const handleBookRequest = async (book, isAvailable) => {
  if (book.copy_type === 'Online') {
    window.open(book.url || '#', '_blank');
    return;
  }

  if (bookRequest.isBookRequested(book.name)) {
    const requestId = bookRequest.bookRequestMap.value[book.name];
    await bookRequest.cancelRequest(book.name, requestId);
  } else {
    const bookData = {
      id: book.name,
      name: book.name,
      title: book.title,
      author: book.author,
      isbn: book.isbn || '',
      requestType: isAvailable ? 'Issue' : 'Reservation'
    };
    await bookRequest.requestBook(bookData);
  }

  if (bookRequest.successMessage.value) {
    console.log('✓', bookRequest.successMessage.value);
  } else if (bookRequest.error.value) {
    console.error('✗', bookRequest.error.value);
  }

  await fetchAllBooks();
};

const categories = computed(() => {
  if (!allBooks.value) return [];
  const cats = allBooks.value.map(b => b.category).filter(Boolean);
  return [...new Set(cats)].sort();
});

const filteredCatalog = computed(() => {
  if (!allBooks.value) return [];
  return allBooks.value.filter(book => {
    // ── NEW: hide books the user currently has issued ─────────────────────────
    // `borrowedBookNames` is a Set of book name/IDs the user already holds.
    if (borrowedBookNames.value.has(book.name)) return false;

    const query = searchQuery.value.toLowerCase();
    const matchesSearch = (book.title?.toLowerCase().includes(query)) || (book.author?.toLowerCase().includes(query));
    const matchesCat = selectedCategory.value === 'All' || book.category === selectedCategory.value;
    const matchesType = selectedType.value === 'All' || (book.copy_type || 'Physical') === selectedType.value;
    const matchesStatus = selectedStatus.value === 'All' || (selectedStatus.value === 'Available' ? isAvailable(book) : !isAvailable(book));
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
.filter-input { @apply w-full bg-slate-50 border border-slate-100 rounded-xl px-4 py-2.5 text-xs font-bold text-slate-700 outline-none focus:ring-4 focus:ring-indigo-500/10 transition-all pl-12; }
.th-style { @apply text-[10px] font-black uppercase text-slate-400 tracking-widest; }
.type-badge { @apply px-3 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest border shadow-sm; }
.status-badge { @apply px-3 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-tighter shadow-sm border; }
.btn-action-active { @apply px-5 py-3 rounded-xl bg-indigo-600 text-white text-[10px] font-black uppercase tracking-widest hover:bg-slate-900 shadow-sm transition-all active:scale-95; }
.btn-reserve { @apply px-5 py-3 rounded-xl bg-purple-600 text-white text-[10px] font-black uppercase tracking-widest hover:bg-slate-900 shadow-sm transition-all active:scale-95; }
.btn-cancel { @apply px-5 py-3 rounded-xl bg-red-600 text-white text-[10px] font-black uppercase tracking-widest hover:bg-red-700 shadow-sm transition-all active:scale-95; }
.page-btn-fixed { @apply p-2 w-10 h-10 rounded-xl bg-white border border-slate-200 disabled:opacity-30 disabled:cursor-not-allowed hover:border-indigo-500 transition-all shadow-sm flex items-center justify-center text-slate-400; }
</style>