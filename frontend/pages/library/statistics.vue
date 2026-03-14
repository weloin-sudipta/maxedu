<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-white p-4 lg:p-8 font-sans">
    <div class="max-w-[1440px] mx-auto space-y-8">
      
      <!-- Header -->
      <header class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 p-8">
        <h1 class="text-3xl font-black tracking-tight text-slate-800">Library Insights</h1>
        <p class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mt-1">
          Library statistics, new arrivals & borrowing trends
        </p>
      </header>

      <!-- Loading State -->
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="i in 4" :key="i" class="h-32 bg-slate-200 rounded-[2rem] animate-pulse"></div>
      </div>

      <!-- Statistics Cards -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <!-- Total Books -->
        <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 p-6">
          <div class="flex items-start justify-between mb-4">
            <div class="w-12 h-12 rounded-2xl bg-indigo-100 flex items-center justify-center text-indigo-600">
              <i class="fa fa-book text-xl"></i>
            </div>
            <span class="text-[10px] font-black text-slate-300 uppercase">Total</span>
          </div>
          <p class="text-3xl font-black text-slate-800">{{ statistics.total_books }}</p>
          <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-2">Books in Library</p>
        </div>

        <!-- Total Members -->
        <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 p-6">
          <div class="flex items-start justify-between mb-4">
            <div class="w-12 h-12 rounded-2xl bg-green-100 flex items-center justify-center text-green-600">
              <i class="fa fa-users text-xl"></i>
            </div>
            <span class="text-[10px] font-black text-slate-300 uppercase">Users</span>
          </div>
          <p class="text-3xl font-black text-slate-800">{{ statistics.total_members }}</p>
          <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-2">Active Members</p>
        </div>

        <!-- Active Borrowers -->
        <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 p-6">
          <div class="flex items-start justify-between mb-4">
            <div class="w-12 h-12 rounded-2xl bg-amber-100 flex items-center justify-center text-amber-600">
              <i class="fa fa-hand-paper-o text-xl"></i>
            </div>
            <span class="text-[10px] font-black text-slate-300 uppercase">Active</span>
          </div>
          <p class="text-3xl font-black text-slate-800">{{ statistics.active_borrowers }}</p>
          <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-2">Currently Borrowing</p>
        </div>

        <!-- Avg Borrow Period -->
        <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 p-6">
          <div class="flex items-start justify-between mb-4">
            <div class="w-12 h-12 rounded-2xl bg-purple-100 flex items-center justify-center text-purple-600">
              <i class="fa fa-calendar text-xl"></i>
            </div>
            <span class="text-[10px] font-black text-slate-300 uppercase">Average</span>
          </div>
          <p class="text-3xl font-black text-slate-800">{{ statistics.average_borrow_days }}</p>
          <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-2">Borrow Days</p>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <!-- Most Borrowed Categories -->
        <div class="lg:col-span-2 bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden">
          <div class="p-8 border-b border-slate-50 bg-slate-50/50">
            <h2 class="text-xl font-black text-slate-800">Most Borrowed Categories</h2>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">
              Borrowing trends by category
            </p>
          </div>

          <div class="p-8">
            <div v-if="statistics.most_borrowed_categories && statistics.most_borrowed_categories.length > 0" class="space-y-4">
              <div v-for="(cat, index) in statistics.most_borrowed_categories" :key="index" 
                   class="flex items-start gap-4 pb-4 border-b border-slate-100 last:border-b-0">
                <div class="flex-shrink-0 w-12 h-12 rounded-2xl bg-indigo-100 flex items-center justify-center text-indigo-600 font-black">
                  {{ index + 1 }}
                </div>
                <div class="flex-1">
                  <h3 class="text-sm font-black text-slate-800 mb-2">{{ cat.category || 'Uncategorized' }}</h3>
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex gap-4 text-[10px] font-bold">
                      <span class="text-slate-500">
                        <span class="text-slate-700">{{ cat.borrow_count }}</span> borrows
                      </span>
                      <span class="text-slate-500">
                        <span class="text-slate-700">{{ cat.member_count }}</span> members
                      </span>
                    </div>
                  </div>
                  <!-- Progress Bar -->
                  <div class="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div class="h-full bg-indigo-600 rounded-full" 
                         :style="{ width: ((cat.borrow_count / statistics.most_borrowed_categories[0].borrow_count) * 100) + '%' }">
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="py-8 text-center">
              <i class="fa fa-inbox text-slate-100 text-3xl mb-4"></i>
              <p class="text-[10px] font-black text-slate-400 uppercase">No borrowing data available</p>
            </div>
          </div>
        </div>

        <!-- Quick Stats -->
        <div class="space-y-6">
          
          <!-- Total Issues -->
          <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 p-6">
            <div class="flex items-center gap-3 mb-4">
              <i class="fa fa-history text-indigo-600 text-lg"></i>
              <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Total Issues</span>
            </div>
            <p class="text-4xl font-black text-slate-800">{{ statistics.total_issues }}</p>
            <p class="text-[10px] text-slate-400 mt-2">lifetime borrowings</p>
          </div>

          <!-- Quick Links -->
          <div class="bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-[2.5rem] shadow-lg shadow-indigo-200 text-white p-6">
            <h3 class="text-sm font-black mb-4">Quick Actions</h3>
            <div class="space-y-2">
              <nuxt-link to="/library/staff-issuance" 
                class="block p-3 rounded-xl bg-white/10 hover:bg-white/20 text-[10px] font-black uppercase tracking-widest transition-all">
                <i class="fa fa-arrow-right mr-2"></i> Issue Book
              </nuxt-link>
              <nuxt-link to="/library" 
                class="block p-3 rounded-xl bg-white/10 hover:bg-white/20 text-[10px] font-black uppercase tracking-widest transition-all">
                <i class="fa fa-book mr-2"></i> View Catalog
              </nuxt-link>
            </div>
          </div>
        </div>
      </div>

      <!-- New Arrivals Section -->
      <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden">
        <div class="p-8 border-b border-slate-50 bg-slate-50/50 flex items-center justify-between">
          <div>
            <h2 class="text-xl font-black text-slate-800">New Arrivals</h2>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">
              Added in the last 3 days
            </p>
          </div>
          <span class="px-4 py-2 rounded-xl bg-amber-100 text-amber-700 text-sm font-black">
            {{ newBooks.length }}
          </span>
        </div>

        <div class="p-8">
          <div v-if="newBooks.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div v-for="book in newBooks" :key="book.name" 
                 class="group bg-slate-50 rounded-[2rem] overflow-hidden border border-slate-100 hover:shadow-lg hover:shadow-indigo-100/50 transition-all">
              <!-- Book Cover -->
              <div class="aspect-[3/4] bg-gradient-to-br from-indigo-100 to-slate-100 flex items-center justify-center overflow-hidden relative">
                <i class="fa fa-book-reader text-4xl text-slate-200 group-hover:scale-110 transition-transform"></i>
                <div class="absolute top-3 left-3">
                  <span class="px-3 py-1 rounded-lg bg-amber-400 text-amber-900 text-[8px] font-black uppercase">
                    NEW
                  </span>
                </div>
              </div>
              <!-- Book Info -->
              <div class="p-4">
                <h3 class="font-black text-slate-800 text-sm truncate">{{ book.title }}</h3>
                <p class="text-[10px] font-bold text-slate-400 uppercase truncate">{{ book.author }}</p>
                <div class="mt-3 pt-3 border-t border-slate-200">
                  <span class="text-[9px] font-black text-indigo-600 bg-indigo-50 px-2 py-1 rounded-md">
                    {{ book.category || 'General' }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="py-12 text-center">
            <i class="fa fa-inbox text-slate-100 text-4xl mb-4"></i>
            <p class="text-[10px] font-black text-slate-400 uppercase">No new arrivals in the last 3 days</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { createResource } from '~/composable/useFrappeFetch';

const statistics = ref({
  total_books: 0,
  total_issues: 0,
  total_members: 0,
  active_borrowers: 0,
  average_borrow_days: 0,
  most_borrowed_categories: []
});

const newBooks = ref([]);
const loading = ref(true);

// Fetch library statistics
const fetchStatistics = async () => {
  try {
    const resource = createResource({
      url: 'maxedu.api_folder.library.get_library_statistics',
    });
    const res = await resource.fetch();
    statistics.value = res;
  } catch (err) {
    console.error("Failed to load statistics:", err);
  }
};

// Fetch new books
const fetchNewBooks = async () => {
  try {
    const resource = createResource({
      url: 'maxedu.api_folder.library.get_new_books',
    });
    const res = await resource.fetch();
    newBooks.value = res.books || [];
  } catch (err) {
    console.error("Failed to load new books:", err);
  }
};

// Initialize
onMounted(async () => {
  loading.value = true;
  await Promise.all([fetchStatistics(), fetchNewBooks()]);
  loading.value = false;
});
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
