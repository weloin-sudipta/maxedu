<template>
  <div class="space-y-8">
    
    <!-- Summary Cards - Teacher Insights -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <!-- Books by Subject -->
      <div class="bg-white rounded-[2rem] shadow-sm border border-slate-200/60 p-6">
        <div class="flex items-start justify-between mb-4">
          <div class="w-12 h-12 rounded-2xl bg-indigo-100 flex items-center justify-center text-indigo-600">
            <i class="fa fa-bookmark text-xl"></i>
          </div>
          <span class="text-[10px] font-black text-slate-300 uppercase">Subject</span>
        </div>
        <p class="text-3xl font-black text-slate-800">{{ stats.subject_books }}</p>
        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-2">Books by Subject</p>
      </div>

      <!-- Unique Subjects -->
      <div class="bg-white rounded-[2rem] shadow-sm border border-slate-200/60 p-6">
        <div class="flex items-start justify-between mb-4">
          <div class="w-12 h-12 rounded-2xl bg-purple-100 flex items-center justify-center text-purple-600">
            <i class="fa fa-sitemap text-xl"></i>
          </div>
          <span class="text-[10px] font-black text-slate-300 uppercase">Categories</span>
        </div>
        <p class="text-3xl font-black text-slate-800">{{ stats.unique_subjects }}</p>
        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-2">Subject Areas</p>
      </div>

      <!-- Currently Using -->
      <div class="bg-white rounded-[2rem] shadow-sm border border-slate-200/60 p-6">
        <div class="flex items-start justify-between mb-4">
          <div class="w-12 h-12 rounded-2xl bg-green-100 flex items-center justify-center text-green-600">
            <i class="fa fa-hand-holding-book text-xl"></i>
          </div>
          <span class="text-[10px] font-black text-slate-300 uppercase">Active</span>
        </div>
        <p class="text-3xl font-black text-slate-800">{{ stats.current_teaching_books }}</p>
        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-2">For Teaching</p>
      </div>

      <!-- Avg Books/Class -->
      <div class="bg-white rounded-[2rem] shadow-sm border border-slate-200/60 p-6">
        <div class="flex items-start justify-between mb-4">
          <div class="w-12 h-12 rounded-2xl bg-amber-100 flex items-center justify-center text-amber-600">
            <i class="fa fa-chart-bar text-xl"></i>
          </div>
          <span class="text-[10px] font-black text-slate-300 uppercase">Average</span>
        </div>
        <p class="text-3xl font-black text-slate-800">{{ stats.avg_per_subject }}</p>
        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-2">Per Subject</p>
      </div>
    </div>

    <!-- Main Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <!-- Books by Subject -->
      <div class="lg:col-span-2 bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden">
        <div class="p-8 border-b border-slate-50 bg-slate-50/50">
          <h2 class="text-xl font-black text-slate-800">Books by Subject</h2>
          <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">
            Your teaching materials organized by subject
          </p>
        </div>

        <div class="p-8">
          <div v-if="subjectsData.length > 0" class="space-y-4">
            <div v-for="(subject, idx) in subjectsData" :key="idx" 
                 class="border border-slate-100 rounded-2xl p-6 hover:shadow-lg transition-all">
              <div class="flex items-start justify-between mb-4">
                <div>
                  <h3 class="font-black text-slate-800">{{ subject.name }}</h3>
                  <p class="text-[10px] font-bold text-slate-400 uppercase">{{ subject.books.length }} Books</p>
                </div>
                <span class="px-3 py-1 rounded-lg text-[9px] font-black uppercase bg-indigo-50 text-indigo-600 border border-indigo-100">
                  {{ subject.books.filter(b => b.status === 'Issued').length }} Active
                </span>
              </div>

              <!-- Subject Books Grid -->
              <div class="grid grid-cols-2 gap-3">
                <div v-for="book in subject.books.slice(0, 4)" :key="book.name" 
                     class="text-[10px] p-2 bg-slate-50 rounded-lg border border-slate-100">
                  <p class="font-bold text-slate-700 truncate">{{ book.book_title }}</p>
                  <p class="text-slate-500">{{ formatDate(book.issue_date) }}</p>
                </div>
                <div v-if="subject.books.length > 4" class="text-[10px] p-2 bg-slate-100 rounded-lg flex items-center justify-center">
                  <span class="font-black text-slate-600">+{{ subject.books.length - 4 }} More</span>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="py-12 text-center">
            <i class="fa fa-inbox text-slate-100 text-4xl mb-4"></i>
            <p class="text-[10px] font-black text-slate-400 uppercase">No subject-based books yet</p>
          </div>
        </div>
      </div>

      <!-- Class Statistics -->
      <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden">
        <div class="p-8 border-b border-slate-50 bg-slate-50/50">
          <h2 class="text-xl font-black text-slate-800">Teaching Overview</h2>
          <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">
            Quick statistics
          </p>
        </div>

        <div class="p-8 space-y-6">
          <!-- Teaching with Books -->
          <div class="space-y-3">
            <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Teaching Materials</p>
            <div class="space-y-2">
              <div v-if="currentTeachingBooks.length > 0">
                <div v-for="book in currentTeachingBooks.slice(0, 3)" :key="book.name" 
                     class="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-100">
                  <span class="text-[10px] font-bold text-slate-700 truncate">{{ book.book_title }}</span>
                  <span class="text-[9px] font-black text-slate-500">{{ getDaysRemaining(book.due_date) }}d</span>
                </div>
              </div>
              <div v-else class="p-4 text-center bg-slate-50 rounded-lg border border-slate-100">
                <p class="text-[10px] font-bold text-slate-400 uppercase">No active teaching materials</p>
              </div>
            </div>
          </div>

          <!-- Recommended Books -->
          <div class="pt-4 border-t border-slate-200 space-y-3">
            <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">For Your Subjects</p>
            <div class="flex flex-col gap-2">
              <a href="/library#recommendations" 
                 class="px-4 py-2.5 rounded-xl bg-indigo-600 text-white text-[10px] font-black uppercase tracking-widest hover:bg-indigo-700 transition-all text-center">
                <i class="fa fa-lightbulb mr-2"></i> View Recommendations
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- All Teaching Books -->
    <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden">
      <div class="p-8 border-b border-slate-50 bg-slate-50/50">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-xl font-black text-slate-800">Complete Teaching Materials</h2>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">
              All books used for teaching
            </p>
          </div>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse min-w-full">
          <thead>
            <tr class="bg-slate-50/50">
              <th class="px-6 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest">Book Title</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest">Subject</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest">Borrowed</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest">Due</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest text-center">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="book in allTeachingBooks" :key="book.name" class="hover:bg-slate-50/30 transition-colors">
              <td class="px-6 py-4">
                <span class="font-black text-slate-800">{{ book.book_title }}</span>
              </td>
              <td class="px-6 py-4">
                <span class="text-[10px] font-bold text-slate-600 uppercase">{{ book.subject || '-' }}</span>
              </td>
              <td class="px-6 py-4">
                <span class="text-[10px] font-bold text-slate-600">{{ formatDate(book.issue_date) }}</span>
              </td>
              <td class="px-6 py-4">
                <span :class="['text-[10px] font-bold', getDaysRemaining(book.due_date) < 0 ? 'text-red-600' : 'text-slate-600']">
                  {{ formatDate(book.due_date) }}
                </span>
              </td>
              <td class="px-6 py-4 text-center">
                <span :class="[
                  'px-2 py-1 rounded-lg text-[9px] font-black uppercase border inline-block',
                  book.status === 'Issued' ? 'bg-green-50 text-green-600 border-green-100' :
                  book.status === 'Returned' ? 'bg-blue-50 text-blue-600 border-blue-100' :
                  'bg-slate-50 text-slate-600 border-slate-100'
                ]">
                  {{ book.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="allTeachingBooks.length === 0" class="p-12 text-center">
          <i class="fa fa-inbox text-slate-100 text-3xl mb-4"></i>
          <p class="text-[10px] font-black text-slate-400 uppercase">No teaching materials record</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { createResource } from '~/composable/useFrappeFetch';

const currentTeachingBooks = ref([]);
const allTeachingBooks = ref([]);
const stats = ref({
  subject_books: 0,
  unique_subjects: 0,
  current_teaching_books: 0,
  avg_per_subject: 0
});

// Format helpers
const formatDate = (dateStr) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
};

const getDaysRemaining = (dueDate) => {
  if (!dueDate) return 0;
  const today = new Date();
  const due = new Date(dueDate);
  const diff = Math.ceil((due - today) / (1000 * 60 * 60 * 24));
  return diff;
};

const subjectsData = computed(() => {
  const grouped = {};
  allTeachingBooks.value.forEach(book => {
    const subject = book.category || 'Other';
    if (!grouped[subject]) {
      grouped[subject] = { name: subject, books: [] };
    }
    grouped[subject].books.push(book);
  });
  return Object.values(grouped);
});

// Fetch data
const fetchData = async () => {
  try {
    // Get teacher's borrowed books
    const borrowed = await createResource({
      url: 'maxedu.api_folder.library.get_user_borrowed_books'
    }).fetch();

    currentTeachingBooks.value = borrowed.books || [];

    // Get all teacher issues
    const allIssues = await frappe.call({
      method: 'frappe.client.get_list',
      args: {
        doctype: 'Book Issue',
        fields: ['name', 'book', 'book_title', 'book_isbn', 'issue_date', 'return_date', 'status', 'due_date'],
        order_by: 'issue_date desc'
      }
    });

    allTeachingBooks.value = allIssues.message || [];

    // Calculate stats
    const uniqueSubjects = new Set(allTeachingBooks.value.map(b => b.category || 'Other')).size;
    stats.value = {
      subject_books: allTeachingBooks.value.length,
      unique_subjects: uniqueSubjects,
      current_teaching_books: currentTeachingBooks.value.length,
      avg_per_subject: uniqueSubjects > 0 ? Math.round(allTeachingBooks.value.length / uniqueSubjects) : 0
    };
  } catch (err) {
    console.error('Failed to fetch teacher tracking data:', err);
  }
};

onMounted(() => fetchData());
</script>

<style scoped>
</style>
