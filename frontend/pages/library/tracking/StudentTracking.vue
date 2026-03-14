<template>
  <div class="space-y-8">
    
    <!-- Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <!-- Total Borrowed -->
      <div class="bg-white rounded-[2rem] shadow-sm border border-slate-200/60 p-6">
        <div class="flex items-start justify-between mb-4">
          <div class="w-12 h-12 rounded-2xl bg-indigo-100 flex items-center justify-center text-indigo-600">
            <i class="fa fa-book-reader text-xl"></i>
          </div>
          <span class="text-[10px] font-black text-slate-300 uppercase">Books</span>
        </div>
        <p class="text-3xl font-black text-slate-800">{{ stats.total_borrowed }}</p>
        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-2">Total Borrowed</p>
      </div>

      <!-- Currently Borrowing -->
      <div class="bg-white rounded-[2rem] shadow-sm border border-slate-200/60 p-6">
        <div class="flex items-start justify-between mb-4">
          <div class="w-12 h-12 rounded-2xl bg-amber-100 flex items-center justify-center text-amber-600">
            <i class="fa fa-hourglass-half text-xl"></i>
          </div>
          <span class="text-[10px] font-black text-slate-300 uppercase">Current</span>
        </div>
        <p class="text-3xl font-black text-slate-800">{{ stats.current_borrowed }}</p>
        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-2">Currently Issued</p>
      </div>

      <!-- Overdue Books -->
      <div class="bg-white rounded-[2rem] shadow-sm border border-slate-200/60 p-6">
        <div class="flex items-start justify-between mb-4">
          <div class="w-12 h-12 rounded-2xl bg-red-100 flex items-center justify-center text-red-600">
            <i class="fa fa-exclamation-triangle text-xl"></i>
          </div>
          <span class="text-[10px] font-black text-slate-300 uppercase">Overdue</span>
        </div>
        <p class="text-3xl font-black text-slate-800">{{ stats.overdue_count }}</p>
        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-2">Books Overdue</p>
      </div>

      <!-- Fine Amount -->
      <div class="bg-white rounded-[2rem] shadow-sm border border-slate-200/60 p-6">
        <div class="flex items-start justify-between mb-4">
          <div class="w-12 h-12 rounded-2xl bg-purple-100 flex items-center justify-center text-purple-600">
            <i class="fa fa-dollar text-xl"></i>
          </div>
          <span class="text-[10px] font-black text-slate-300 uppercase">Fine</span>
        </div>
        <p class="text-3xl font-black text-slate-800">{{ formatCurrency(stats.total_fine) }}</p>
        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-2">Pending Fine</p>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <!-- Currently Issued Books -->
      <div class="lg:col-span-2 bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden">
        <div class="p-8 border-b border-slate-50 bg-slate-50/50">
          <h2 class="text-xl font-black text-slate-800">Currently Issued Books</h2>
          <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">
            Books you are currently borrowing
          </p>
        </div>

        <div class="p-8">
          <div v-if="currentBooks.length > 0" class="space-y-4">
            <div v-for="book in currentBooks" :key="book.name" 
                 class="border border-slate-100 rounded-2xl p-6 hover:shadow-lg transition-all">
              <div class="flex items-start justify-between mb-4">
                <div class="flex items-start gap-4 flex-1">
                  <div class="w-10 h-10 rounded-xl bg-indigo-100 text-indigo-600 flex items-center justify-center flex-shrink-0">
                    <i class="fa fa-book text-sm"></i>
                  </div>
                  <div class="flex-1">
                    <h3 class="font-black text-slate-800">{{ book.book_title }}</h3>
                    <p class="text-[10px] font-bold text-slate-400 uppercase">ISBN: {{ book.book_isbn }}</p>
                  </div>
                </div>
                <span :class="['px-3 py-1 rounded-lg text-[9px] font-black uppercase border', getDueDateClass(book.due_date)]">
                  {{ getDaysRemaining(book.due_date) }} Days
                </span>
              </div>

              <div class="grid grid-cols-3 gap-4 pt-4 border-t border-slate-100">
                <div>
                  <p class="text-[10px] font-bold text-slate-400 uppercase">Issued</p>
                  <p class="text-sm font-black text-slate-800">{{ formatDate(book.issue_date) }}</p>
                </div>
                <div>
                  <p class="text-[10px] font-bold text-slate-400 uppercase">Due</p>
                  <p :class="['text-sm font-black', getDaysRemaining(book.due_date) < 0 ? 'text-red-600' : 'text-slate-800']">
                    {{ formatDate(book.due_date) }}
                  </p>
                </div>
                <div>
                  <p class="text-[10px] font-bold text-slate-400 uppercase">Renewals</p>
                  <p class="text-sm font-black text-slate-800">{{ book.renewal_count || 0 }}x</p>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="py-12 text-center">
            <i class="fa fa-inbox text-slate-100 text-4xl mb-4"></i>
            <p class="text-[10px] font-black text-slate-400 uppercase">No books currently issued</p>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden">
        <div class="p-8 border-b border-slate-50 bg-slate-50/50">
          <h2 class="text-xl font-black text-slate-800">Recent Activity</h2>
          <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">
            Last 5 activities
          </p>
        </div>

        <div class="p-8">
          <div v-if="recentActivity.length > 0" class="space-y-4">
            <div v-for="(activity, idx) in recentActivity" :key="idx" 
                 class="pb-4 border-b border-slate-100 last:border-b-0">
              <div class="flex items-start gap-3">
                <div :class="['w-8 h-8 rounded-lg flex items-center justify-center text-white text-xs flex-shrink-0', 
                  activity.type === 'issued' ? 'bg-green-500' : 
                  activity.type === 'returned' ? 'bg-blue-500' :
                  activity.type === 'renewed' ? 'bg-purple-500' : 'bg-slate-400'
                ]">
                  <i :class="[
                    activity.type === 'issued' ? 'fa fa-arrow-down' :
                    activity.type === 'returned' ? 'fa fa-arrow-up' :
                    activity.type === 'renewed' ? 'fa fa-sync' : 'fa fa-info'
                  ]"></i>
                </div>
                <div class="flex-1">
                  <p class="text-sm font-black text-slate-800">{{ activity.title }}</p>
                  <p class="text-[10px] text-slate-500">{{ activity.date }}</p>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="py-8 text-center">
            <p class="text-[10px] font-black text-slate-400 uppercase">No recent activity</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Borrowing History -->
    <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden">
      <div class="p-8 border-b border-slate-50 bg-slate-50/50">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-xl font-black text-slate-800">Borrowing History</h2>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">
              All your past borrowing records
            </p>
          </div>
          <div class="flex gap-2">
            <input v-model="searchHistory" type="text" placeholder="Search books..." 
              class="px-4 py-2 rounded-xl border border-slate-200 text-[10px] font-bold placeholder-slate-400 outline-none focus:ring-2 focus:ring-indigo-500/20" />
          </div>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse min-w-full">
          <thead>
            <tr class="bg-slate-50/50">
              <th class="px-6 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest">Book</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest">ISBN</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest">Borrowed</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest">Returned</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest text-center">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="record in filteredHistory" :key="record.name" class="hover:bg-slate-50/30 transition-colors">
              <td class="px-6 py-4">
                <span class="font-black text-slate-800">{{ record.book_title }}</span>
              </td>
              <td class="px-6 py-4">
                <span class="text-[10px] font-bold text-slate-500 uppercase">{{ record.book_isbn }}</span>
              </td>
              <td class="px-6 py-4">
                <span class="text-[10px] font-bold text-slate-600">{{ formatDate(record.issue_date) }}</span>
              </td>
              <td class="px-6 py-4">
                <span class="text-[10px] font-bold text-slate-600">{{ record.return_date ? formatDate(record.return_date) : '-' }}</span>
              </td>
              <td class="px-6 py-4 text-center">
                <span :class="[
                  'px-2 py-1 rounded-lg text-[9px] font-black uppercase border inline-block',
                  record.status === 'Returned' ? 'bg-green-50 text-green-600 border-green-100' :
                  record.status === 'Issued' ? 'bg-amber-50 text-amber-600 border-amber-100' :
                  record.status === 'Overdue' ? 'bg-red-50 text-red-600 border-red-100' : 'bg-slate-50 text-slate-600 border-slate-100'
                ]">
                  {{ record.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="filteredHistory.length === 0" class="p-12 text-center">
          <i class="fa fa-inbox text-slate-100 text-3xl mb-4"></i>
          <p class="text-[10px] font-black text-slate-400 uppercase">No borrowing history found</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { createResource } from '~/composable/useFrappeFetch';

const currentBooks = ref([]);
const historyBooks = ref([]);
const stats = ref({
  total_borrowed: 0,
  current_borrowed: 0,
  overdue_count: 0,
  total_fine: 0
});
const searchHistory = ref('');

// Format helpers
const formatDate = (dateStr) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
};

const getDaysRemaining = (dueDate) => {
  if (!dueDate) return 0;
  const today = new Date();
  const due = new Date(dueDate);
  const diff = Math.ceil((due - today) / (1000 * 60 * 60 * 24));
  return diff;
};

const getDueDateClass = (dueDate) => {
  const days = getDaysRemaining(dueDate);
  if (days < 0) return 'bg-red-50 text-red-600 border-red-100';
  if (days <= 3) return 'bg-amber-50 text-amber-600 border-amber-100';
  return 'bg-green-50 text-green-600 border-green-100';
};

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount || 0);
};

const recentActivity = computed(() => {
  // Get last 5 activities from current and history
  const activities = [];
  
  currentBooks.value.slice(0, 1).forEach(book => {
    activities.push({
      type: 'issued',
      title: `Borrowed "${book.book_title}"`,
      date: formatDate(book.issue_date)
    });
  });

  historyBooks.value.slice(0, 4).forEach(book => {
    if (book.status === 'Returned') {
      activities.push({
        type: 'returned',
        title: `Returned "${book.book_title}"`,
        date: formatDate(book.return_date)
      });
    }
  });

  return activities.slice(0, 5);
});

const filteredHistory = computed(() => {
  return historyBooks.value.filter(book =>
    !searchHistory.value || 
    book.book_title.toLowerCase().includes(searchHistory.value.toLowerCase()) ||
    book.book_isbn.toLowerCase().includes(searchHistory.value.toLowerCase())
  );
});

// Fetch data
const fetchData = async () => {
  try {
    const borrowed = await createResource({
      url: 'maxedu.api_folder.library.get_user_borrowed_books'
    }).fetch();

    currentBooks.value = borrowed.books || [];

    // Get all issues for history
    const allIssues = await frappe.call({
      method: 'frappe.client.get_list',
      args: {
        doctype: 'Book Issue',
        fields: ['name', 'book', 'book_title', 'book_isbn', 'issue_date', 'return_date', 'status', 'total_fine'],
        order_by: 'issue_date desc'
      }
    });

    historyBooks.value = allIssues.message || [];

    // Calculate stats
    stats.value = {
      total_borrowed: historyBooks.value.length,
      current_borrowed: currentBooks.value.length,
      overdue_count: currentBooks.value.filter(b => getDaysRemaining(b.due_date) < 0).length,
      total_fine: currentBooks.value.reduce((sum, b) => sum + (b.fine_per_day || 0), 0)
    };
  } catch (err) {
    console.error('Failed to fetch tracking data:', err);
  }
};

onMounted(() => fetchData());
</script>

<style scoped>
</style>
