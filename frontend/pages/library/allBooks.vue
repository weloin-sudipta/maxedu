<template>
  <div
    class="bg-white rounded-[2rem] lg:rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden animate-in fade-in duration-500">

    <div class="p-5 lg:p-8 border-b border-slate-50 space-y-6">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-6">
        <div>
          <h3 class="text-sm lg:text-base font-black text-slate-800 uppercase tracking-widest">Library Catalog</h3>
          <p class="text-[10px] font-bold text-slate-400 uppercase tracking-tighter mt-1">Explore academic resources</p>
        </div>
      </div>

      <div class="grid grid-cols-2 lg:grid-cols-5 gap-3 lg:gap-4">
        <div class="col-span-2">
          <span class="filter-label">Search Catalog</span>
          <div class="relative">
            <i class="fa fa-search absolute left-4 top-1/2 -translate-y-1/2 text-slate-300"></i>
            <input v-model="searchQuery" type="text" placeholder="Title or Author..."
              class="filter-input pl-12 md:pl-16 lg:pl-20" />
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

            <!-- Book Info -->
            <td class="px-6 py-5">
              <div class="flex items-center gap-4">
                <div
                  class="h-10 w-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center border border-indigo-100 group-hover:bg-slate-900 group-hover:text-white transition-all">
                  <i :class="book.type === 'Online' ? 'fa fa-laptop' : 'fa fa-book'" class="text-xs"></i>
                </div>
                <div class="flex flex-col">
                  <span class="text-sm font-black text-slate-700 group-hover:text-indigo-600 transition-colors">
                    {{ book.title }}
                  </span>
                  <span class="text-[10px] font-bold text-slate-400 uppercase">By {{ book.author }}</span>
                </div>
              </div>
            </td>

            <!-- Category -->
            <td class="px-6 py-5">
              <span class="text-[9px] font-black text-indigo-400 uppercase tracking-widest ml-1">
                {{ book.category }}
              </span>
            </td>

            <!-- Type -->
            <td class="px-6 py-5">
              <span
                :class="['type-badge', book.type === 'Online'
                  ? 'bg-purple-50 text-purple-600 border-purple-100'
                  : 'bg-blue-50 text-blue-600 border-blue-100']">
                {{ book.type }}
              </span>
            </td>

            <!-- STATUS BADGE (UPDATED) -->
            <td class="px-6 py-5 text-center">
              <span
                :class="[
                  'status-badge',
                  book.status === 'Available'
                    ? 'bg-green-50 text-green-600 border-green-100'
                    : 'bg-purple-50 text-red-600 border-purple-100'
                ]">
                {{ book.status || 'Issued Out' }}
              </span>
            </td>

            <!-- Action -->
            <td class="px-6 py-5 text-right">
              <button
                :disabled="!isAvailable(book) && book.status !== 'Issued Out' && book.status !== null"
                :class="[isAvailable(book) ? 'btn-action-active' : 'btn-reserve']">

                {{
                  book.type === 'Online'
                    ? 'Read Now'
                    : (book.status === 'Issued Out' || book.status === null)
                      ? 'Reservation'
                      : 'Request'
                }}

              </button>
            </td>

          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useBooks } from '~/composable/useBook';

// --- State ---
const catalog = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const selectedCategory = ref('All');
const selectedType = ref('All');
const selectedStatus = ref('All');
const itemsPerPage = ref(10);
const currentPage = ref(1);

// --- Data Fetching & Cleaning ---
onMounted(async () => {
  try {
    const response = await useBooks();

    // Normalize the data structure
    const normalizedData = response.map(book => ({
      ...book,
      id: book.name,
      category: book.category || 'Uncategorized',
      type: book.copy_type || 'Physical',
      // We keep the original status for filtering
      is_available: book.status === 'Available'
    }));

    // 2. De-duplication Logic
    // Only show one entry if Title, Category, and Type are identical
    const seen = new Set();
    const uniqueBooks = normalizedData.filter(book => {
      const duplicateKey = `${book.title}-${book.category}-${book.type}`
        .toLowerCase()
        .replace(/\s+/g, ''); // Remove spaces to ensure strict matching

      if (seen.has(duplicateKey)) {
        return false;
      }
      seen.add(duplicateKey);
      return true;
    });

    catalog.value = uniqueBooks;
  } catch (error) {
    console.error("Library Catalog Error:", error);
  } finally {
    loading.value = false;
  }
});


// Generate dynamic categories list based on unique data
const categories = computed(() => {
  const cats = catalog.value.map(b => b.category);
  return [...new Set(cats)].filter(Boolean).sort();
});

// Online logic: Online is always available, Physical depends on status
const isAvailable = (book) => {
  return book.type === 'Online' || book.status === 'Available';
};

// Filter Logic
const filteredCatalog = computed(() => {
  return catalog.value.filter(book => {
    // Search match (Title, Author, or ISBN)
    const query = searchQuery.value.toLowerCase();
    const matchesSearch =
      (book.title?.toLowerCase().includes(query)) ||
      (book.author?.toLowerCase().includes(query)) ||
      (book.isbn?.toLowerCase().includes(query));

    // Category match
    const matchesCat = selectedCategory.value === 'All' || book.category === selectedCategory.value;

    // Type match
    const matchesType = selectedType.value === 'All' || book.type === selectedType.value;

    // Status match
    const bookIsAvailable = isAvailable(book);
    const matchesStatus = selectedStatus.value === 'All' ||
      (selectedStatus.value === 'Available' ? bookIsAvailable : !bookIsAvailable);

    return matchesSearch && matchesCat && matchesType && matchesStatus;
  });
});

// Pagination Logic
const totalPages = computed(() => Math.ceil(filteredCatalog.value.length / itemsPerPage.value) || 0);

const paginatedCatalog = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  return filteredCatalog.value.slice(start, start + itemsPerPage.value);
});

// --- Watchers ---

// Reset to first page whenever any filter or search term changes
watch([searchQuery, selectedCategory, selectedType, selectedStatus, itemsPerPage], () => {
  currentPage.value = 1;
});
</script>

<style scoped>
.filter-label {
  @apply text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 block ml-1;
}

.filter-input {
  @apply w-full bg-slate-50 border border-slate-100 rounded-xl px-4 py-2.5 text-xs font-bold text-slate-700 outline-none focus:ring-4 focus:ring-indigo-500/10 transition-all;
}

.th-style {
  @apply text-[10px] font-black uppercase text-slate-400 tracking-widest;
}

.type-badge {
  @apply px-3 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest border shadow-sm;
}

.status-badge {
  @apply px-3 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-tighter shadow-sm border;
}

.btn-primary {
  @apply bg-indigo-600 text-white rounded-xl text-[10px] font-black uppercase tracking-[0.2em] shadow-xl shadow-indigo-100 hover:bg-indigo-700 active:scale-95 transition-all;
}

.btn-icon {
  @apply flex items-center justify-center bg-white border border-slate-200 text-slate-400 rounded-xl hover:text-indigo-600 transition-all;
}

.btn-action-active {
  @apply px-5 py-3 rounded-xl bg-indigo-600 text-white text-[10px] font-black uppercase tracking-widest hover:bg-slate-900 shadow-sm active:scale-95 transition-all;
}
.btn-reserve {
  @apply px-5 py-3 rounded-xl bg-purple-600 text-white text-[10px] font-black uppercase tracking-widest hover:bg-slate-900 shadow-sm active:scale-95 transition-all;
}

.btn-action-disabled {
  @apply px-5 py-3 rounded-xl bg-slate-50 text-slate-300 border border-slate-100 text-[9px] font-black uppercase tracking-widest cursor-not-allowed;
}

.page-btn {
  @apply p-2 w-10 h-10 rounded-xl bg-white border border-slate-200 disabled:opacity-30 flex items-center justify-center text-xs text-slate-400;
}

.page-btn-num {
  @apply w-10 h-10 rounded-xl text-xs font-black transition-all shadow-sm border flex items-center justify-center;
}

.filter-input {
  padding-left: 3rem;
  /* or 48px */
}
</style>