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
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="text-center">
        <i class="fa fa-circle-o-notch fa-spin text-indigo-600 text-3xl mb-4"></i>
        <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Loading your books...</p>
      </div>
    </div>

    <!-- Table -->
    <div v-else class="overflow-x-auto min-h-[300px]">
      <table class="w-full text-left border-collapse hidden md:table">
        <thead>
          <tr class="bg-slate-50/50">
            <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">Book Details</th>
            <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">ISBN</th>
            <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">Issue Date</th>
            <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">Due Date</th>
            <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest">Days Left</th>
            <th class="px-6 py-5 text-[10px] font-black uppercase text-slate-400 tracking-widest text-center">Actions</th>
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
                  <span class="text-[10px] font-bold text-slate-400">Renewed: {{ book.renewal_count || 0 }}x</span>
                </div>
              </div>
            </td>

            <!-- ISBN -->
            <td class="px-6 py-5">
              <span class="text-xs font-black text-slate-600 px-3 py-1 bg-slate-100 rounded-lg border border-slate-200/50 uppercase">{{ book.book_isbn }}</span>
            </td>

            <!-- Issue Date -->
            <td class="px-6 py-5">
              <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{{ formatDate(book.issue_date) }}</span>
            </td>

            <!-- Due Date -->
            <td class="px-6 py-5">
              <span :class="['text-xs font-black', book.is_overdue ? 'text-red-600' : 'text-slate-700']">
                {{ formatDate(book.due_date) }}
              </span>
            </td>

            <!-- Days Left -->
            <td class="px-6 py-5">
              <div v-if="book.is_overdue" class="flex items-center gap-2">
                <span class="px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-tighter shadow-sm border bg-red-50 text-red-600 border-red-100">
                  {{ book.days_overdue }} days overdue
                </span>
              </div>
              <div v-else-if="book.days_left <= 3" class="flex items-center gap-2">
                <span class="px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-tighter shadow-sm border bg-amber-50 text-amber-600 border-amber-100">
                  {{ book.days_left }} days left
                </span>
              </div>
              <div v-else>
                <span class="px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-tighter shadow-sm border bg-green-50 text-green-600 border-green-100">
                  {{ book.days_left }} days left
                </span>
              </div>
            </td>

            <!-- Actions -->
            <td class="px-6 py-5 text-center">
              <div class="flex items-center justify-center gap-2">
                <button 
                  @click="renewBook(book.name)"
                  :disabled="book.has_reservation || renewingBook === book.name"
                  :title="book.has_reservation ? 'Cannot renew: book has pending reservation' : 'Renew this book'"
                  class="px-3 py-1.5 rounded-lg text-[9px] font-black uppercase tracking-tighter transition-all"
                  :class="book.has_reservation 
                    ? 'bg-slate-50 text-slate-400 cursor-not-allowed opacity-50'
                    : 'bg-indigo-50 text-indigo-600 border border-indigo-100 hover:bg-indigo-600 hover:text-white'
                  "
                >
                  <i v-if="renewingBook === book.name" class="fa fa-spinner fa-spin mr-1"></i>
                  {{ book.has_reservation ? 'Reserved' : 'Renew' }}
                </button>
              </div>
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

      <!-- Mobile View -->
      <div class="md:hidden space-y-4 p-4">
        <div v-for="book in paginatedBooks" :key="book.name" class="bg-slate-50 rounded-2xl p-4 border border-slate-100">
          <div class="flex items-start justify-between mb-3">
            <div>
              <h3 class="text-sm font-black text-slate-800">{{ book.book_title }}</h3>
              <p class="text-[10px] font-bold text-slate-400">ISBN: {{ book.book_isbn }}</p>
            </div>
            <button 
              @click="renewBook(book.name)"
              :disabled="book.has_reservation || renewingBook === book.name"
              class="px-3 py-1.5 rounded-lg text-[9px] font-black uppercase transition-all"
              :class="book.has_reservation 
                ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
                : 'bg-indigo-600 text-white hover:bg-indigo-700'
              "
            >
              Renew
            </button>
          </div>
          <div class="grid grid-cols-2 gap-2 text-[10px] font-bold">
            <div><span class="text-slate-400">Issued:</span> {{ formatDate(book.issue_date) }}</div>
            <div><span class="text-slate-400">Due:</span> {{ formatDate(book.due_date) }}</div>
            <div :class="book.is_overdue ? 'text-red-600' : 'text-slate-700'">
              <span class="text-slate-400">Days Left:</span> {{ book.is_overdue ? `${book.days_overdue} overdue` : `${book.days_left} days` }}
            </div>
            <div><span class="text-slate-400">Renewed:</span> {{ book.renewal_count || 0 }}x</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="!loading && totalPages > 1" class="flex flex-col md:flex-row justify-between items-center p-8 bg-slate-50/30 border-t border-slate-100 gap-4">
      <span class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">
        Showing {{ filteredBooks.length === 0 ? 0 : (currentPage - 1) * itemsPerPage + 1 }} - 
        {{ Math.min(currentPage * itemsPerPage, filteredBooks.length) }} of 
        {{ filteredBooks.length }} Issued Books
      </span>
      
      <div class="flex items-center gap-2">
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
import { createResource } from '~/composable/useFrappeFetch';

const searchQuery = ref('');
const itemsPerPage = ref(5);
const currentPage = ref(1);
const loading = ref(false);
const borrowedBooks = ref([]);
const renewingBook = ref(null);

// Fetch user's borrowed books on mount
onMounted(async () => {
    await fetchBorrowedBooks();
});

const fetchBorrowedBooks = async () => {
    loading.value = true;
    try {
        const resource = createResource({
            url: 'maxedu.api_folder.library.get_user_borrowed_books',
        });
        const res = await resource.fetch();
        borrowedBooks.value = res.books || [];
    } catch (err) {
        console.error("Failed to load borrowed books:", err);
    } finally {
        loading.value = false;
    }
};

const renewBook = async (bookIssueName) => {
    renewingBook.value = bookIssueName;
    try {
        const resource = createResource({
            url: 'maxedu.api_folder.library.request_renewal',
            args: { book_issue_name: bookIssueName }
        });
        const res = await resource.fetch();
        if (res.success) {
            // Refresh the list
            await fetchBorrowedBooks();
            frappe.show_alert({message: res.message, indicator: 'green'});
        }
    } catch (err) {
        frappe.show_alert({message: err.message || "Renewal failed", indicator: 'red'});
    } finally {
        renewingBook.value = null;
    }
};

// Filter by search query (title or ISBN)
const filteredBooks = computed(() => {
    return borrowedBooks.value.filter(b =>
        (b.book_title || '').toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        (b.book_isbn || '').toLowerCase().includes(searchQuery.value.toLowerCase())
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

// Format date helper
const formatDate = (dateStr) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
};
</script>

<style scoped>
.btn-primary { @apply px-6 py-2.5 bg-indigo-600 text-white rounded-xl text-[10px] font-black uppercase tracking-[0.2em] shadow-xl shadow-indigo-100 hover:bg-indigo-700 active:scale-95 transition-all; }
.btn-icon { @apply flex items-center justify-center bg-white border border-slate-200 text-slate-400 rounded-xl hover:text-indigo-600 hover:border-indigo-100 transition-all; }
.page-btn-fixed { @apply p-2 w-10 h-10 rounded-xl bg-white border border-slate-200 disabled:opacity-30 disabled:cursor-not-allowed hover:border-indigo-500 transition-all shadow-sm flex items-center justify-center; }
</style>