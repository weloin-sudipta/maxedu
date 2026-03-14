<template>
  <div class="space-y-8">
    
    <!-- Summary Cards - Staff Metrics -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <!-- Total Issues Today -->
      <div class="bg-white rounded-[2rem] shadow-sm border border-slate-200/60 p-6">
        <div class="flex items-start justify-between mb-4">
          <div class="w-12 h-12 rounded-2xl bg-green-100 flex items-center justify-center text-green-600">
            <i class="fa fa-arrow-down text-xl"></i>
          </div>
          <span class="text-[10px] font-black text-slate-300 uppercase">Today</span>
        </div>
        <p class="text-3xl font-black text-slate-800">{{ metrics.issues_today }}</p>
        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-2">Books Issued</p>
      </div>

      <!-- Pending Returns -->
      <div class="bg-white rounded-[2rem] shadow-sm border border-slate-200/60 p-6">
        <div class="flex items-start justify-between mb-4">
          <div class="w-12 h-12 rounded-2xl bg-red-100 flex items-center justify-center text-red-600">
            <i class="fa fa-exclamation-circle text-xl"></i>
          </div>
          <span class="text-[10px] font-black text-slate-300 uppercase">Overdue</span>
        </div>
        <p class="text-3xl font-black text-slate-800">{{ metrics.overdue_issues }}</p>
        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-2">Awaiting Return</p>
      </div>

      <!-- Pending Approvals -->
      <div class="bg-white rounded-[2rem] shadow-sm border border-slate-200/60 p-6">
        <div class="flex items-start justify-between mb-4">
          <div class="w-12 h-12 rounded-2xl bg-amber-100 flex items-center justify-center text-amber-600">
            <i class="fa fa-hourglass-half text-xl"></i>
          </div>
          <span class="text-[10px] font-black text-slate-300 uppercase">Pending</span>
        </div>
        <p class="text-3xl font-black text-slate-800">{{ metrics.pending_requests }}</p>
        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-2">Requests</p>
      </div>

      <!-- Total Fine Pending -->
      <div class="bg-white rounded-[2rem] shadow-sm border border-slate-200/60 p-6">
        <div class="flex items-start justify-between mb-4">
          <div class="w-12 h-12 rounded-2xl bg-purple-100 flex items-center justify-center text-purple-600">
            <i class="fa fa-money-bill-wave text-xl"></i>
          </div>
          <span class="text-[10px] font-black text-slate-300 uppercase">Fine</span>
        </div>
        <p class="text-3xl font-black text-slate-800">{{ formatCurrency(metrics.total_pending_fine) }}</p>
        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-2">Pending Collection</p>
      </div>
    </div>

    <!-- Main Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <!-- Pending Requests Queue -->
      <div class="lg:col-span-2 bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden">
        <div class="p-8 border-b border-slate-50 bg-slate-50/50">
          <h2 class="text-xl font-black text-slate-800">Pending Approvals</h2>
          <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">
            Book requests waiting for approval
          </p>
        </div>

        <div class="p-8">
          <div v-if="pendingRequests.length > 0" class="space-y-4">
            <div v-for="req in pendingRequests" :key="req.name" 
                 class="border border-slate-100 rounded-2xl p-6 hover:shadow-lg transition-all">
              <div class="flex items-start justify-between mb-4">
                <div>
                  <h3 class="font-black text-slate-800">{{ req.book_title }}</h3>
                  <p class="text-[10px] font-bold text-slate-400 uppercase">By: {{ req.member_name }}</p>
                </div>
                <span class="px-3 py-1 rounded-lg text-[9px] font-black uppercase bg-amber-50 text-amber-600 border border-amber-100">
                  {{ daysWaiting(req.request_date) }}d Waiting
                </span>
              </div>

              <div class="grid grid-cols-3 gap-2 pt-4 border-t border-slate-100">
                <button @click="approveRequest(req.name)" 
                  class="px-3 py-2 rounded-lg bg-green-50 text-green-600 border border-green-100 text-[9px] font-black uppercase hover:bg-green-600 hover:text-white transition-all">
                  <i class="fa fa-check mr-1"></i> Approve
                </button>
                <button @click="rejectRequest(req.name)" 
                  class="px-3 py-2 rounded-lg bg-red-50 text-red-600 border border-red-100 text-[9px] font-black uppercase hover:bg-red-600 hover:text-white transition-all">
                  <i class="fa fa-times mr-1"></i> Reject
                </button>
                <nuxt-link to="/library/staff-issuance"
                  class="px-3 py-2 rounded-lg bg-indigo-50 text-indigo-600 border border-indigo-100 text-[9px] font-black uppercase hover:bg-indigo-600 hover:text-white transition-all text-center">
                  <i class="fa fa-arrow-right mr-1"></i> Issue
                </nuxt-link>
              </div>
            </div>
          </div>

          <div v-else class="py-12 text-center">
            <i class="fa fa-inbox text-slate-100 text-4xl mb-4"></i>
            <p class="text-[10px] font-black text-slate-400 uppercase">No pending requests</p>
          </div>
        </div>
      </div>

      <!-- Overdue Books -->
      <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden">
        <div class="p-8 border-b border-slate-50 bg-slate-50/50">
          <h2 class="text-xl font-black text-slate-800">Overdue Books</h2>
          <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">
            Need attention
          </p>
        </div>

        <div class="p-8">
          <div v-if="overdueBooks.length > 0" class="space-y-3">
            <div v-for="book in overdueBooks.slice(0, 5)" :key="book.name" 
                 class="p-4 bg-red-50 border border-red-100 rounded-lg">
              <p class="text-[10px] font-black text-red-700 uppercase">{{ book.book_title }}</p>
              <p class="text-[9px] text-red-600 mt-1">{{ Math.abs(getDaysRemaining(book.due_date)) }} days overdue</p>
              <p class="text-[9px] text-red-500 mt-2">Fine: {{ formatCurrency(book.total_fine) }}</p>
            </div>
          </div>

          <div v-else class="py-8 text-center">
            <i class="fa fa-check-circle text-slate-100 text-3xl mb-4"></i>
            <p class="text-[10px] font-black text-slate-400 uppercase">No overdue books</p>
          </div>
        </div>
      </div>
    </div>

    <!-- All Issues Management -->
    <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden">
      <div class="p-8 border-b border-slate-50 bg-slate-50/50">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-xl font-black text-slate-800">All Issues</h2>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">
              Track all book issues and returns
            </p>
          </div>
          <div class="flex gap-2">
            <select v-model="filterStatus" 
              class="px-4 py-2 rounded-xl border border-slate-200 text-[10px] font-bold bg-white outline-none focus:ring-2 focus:ring-indigo-500/20">
              <option value="">All Status</option>
              <option value="Issued">Issued</option>
              <option value="Returned">Returned</option>
              <option value="Overdue">Overdue</option>
            </select>
          </div>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse min-w-full">
          <thead>
            <tr class="bg-slate-50/50">
              <th class="px-6 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest">Member</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest">Book</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest">Issue Date</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest">Due Date</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest">Fine</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase text-slate-400 tracking-widest text-center">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="issue in filteredIssues" :key="issue.name" class="hover:bg-slate-50/30 transition-colors">
              <td class="px-6 py-4">
                <span class="font-black text-slate-800 text-sm">{{ issue.member_name }}</span>
              </td>
              <td class="px-6 py-4">
                <span class="font-bold text-slate-700">{{ issue.book_title }}</span>
              </td>
              <td class="px-6 py-4">
                <span class="text-[10px] font-bold text-slate-600">{{ formatDate(issue.issue_date) }}</span>
              </td>
              <td class="px-6 py-4">
                <span :class="['text-[10px] font-bold', getDaysRemaining(issue.due_date) < 0 ? 'text-red-600 font-black' : 'text-slate-600']">
                  {{ formatDate(issue.due_date) }}
                </span>
              </td>
              <td class="px-6 py-4">
                <span :class="['text-[10px] font-black', (issue.total_fine || 0) > 0 ? 'text-red-600' : 'text-slate-600']">
                  {{ formatCurrency(issue.total_fine || 0) }}
                </span>
              </td>
              <td class="px-6 py-4 text-center">
                <span :class="[
                  'px-2 py-1 rounded-lg text-[9px] font-black uppercase border inline-block',
                  issue.status === 'Issued' ? 'bg-green-50 text-green-600 border-green-100' :
                  issue.status === 'Returned' ? 'bg-blue-50 text-blue-600 border-blue-100' :
                  issue.status === 'Overdue' ? 'bg-red-50 text-red-600 border-red-100' :
                  'bg-slate-50 text-slate-600 border-slate-100'
                ]">
                  {{ issue.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="filteredIssues.length === 0" class="p-12 text-center">
          <i class="fa fa-inbox text-slate-100 text-3xl mb-4"></i>
          <p class="text-[10px] font-black text-slate-400 uppercase">No issues found</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const pendingRequests = ref([]);
const allIssues = ref([]);
const filterStatus = ref('');

const metrics = ref({
  issues_today: 0,
  overdue_issues: 0,
  pending_requests: 0,
  total_pending_fine: 0
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

const daysWaiting = (requestDate) => {
  if (!requestDate) return 0;
  const today = new Date();
  const req = new Date(requestDate);
  const diff = Math.ceil((today - req) / (1000 * 60 * 60 * 24));
  return Math.max(0, diff);
};

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount || 0);
};

const overdueBooks = computed(() => {
  return allIssues.value.filter(issue => getDaysRemaining(issue.due_date) < 0);
});

const filteredIssues = computed(() => {
  if (!filterStatus.value) return allIssues.value;
  return allIssues.value.filter(issue => issue.status === filterStatus.value);
});

// Actions
const approveRequest = async (requestId) => {
  try {
    await frappe.call({
      method: 'frappe.client.set_value',
      args: {
        doctype: 'Book Request',
        name: requestId,
        fieldname: 'status',
        value: 'Approved'
      }
    });
    frappe.show_alert({ message: 'Request approved! Ready for issuance.', indicator: 'green' });
    fetchData();
  } catch (err) {
    frappe.show_alert({ message: 'Failed to approve', indicator: 'red' });
  }
};

const rejectRequest = async (requestId) => {
  try {
    await frappe.call({
      method: 'frappe.client.set_value',
      args: {
        doctype: 'Book Request',
        name: requestId,
        fieldname: 'status',
        value: 'Cancel'
      }
    });
    frappe.show_alert({ message: 'Request rejected.', indicator: 'orange' });
    fetchData();
  } catch (err) {
    frappe.show_alert({ message: 'Failed to reject', indicator: 'red' });
  }
};

// Fetch data
const fetchData = async () => {
  try {
    // Get pending requests
    const pending = await frappe.call({
      method: 'frappe.client.get_list',
      args: {
        doctype: 'Book Request',
        filters: { status: 'Pending' },
        fields: ['name', 'book', 'book_title', 'member', 'member_name', 'request_date'],
        order_by: 'request_date asc'
      }
    });
    pendingRequests.value = pending.message || [];

    // Get all issues
    const issues = await frappe.call({
      method: 'frappe.client.get_list',
      args: {
        doctype: 'Book Issue',
        fields: ['name', 'member', 'member_name', 'book_title', 'issue_date', 'due_date', 'return_date', 'status', 'total_fine'],
        order_by: 'issue_date desc'
      }
    });
    allIssues.value = issues.message || [];

    // Calculate metrics
    const issuesPerDay = allIssues.value.filter(i => {
      const issueDate = new Date(i.issue_date);
      const today = new Date();
      return issueDate.toDateString() === today.toDateString();
    }).length;

    const overdue = allIssues.value.filter(i => 
      i.status === 'Issued' && getDaysRemaining(i.due_date) < 0
    ).length;

    const totalFine = allIssues.value
      .filter(i => i.status === 'Issued')
      .reduce((sum, i) => sum + (i.total_fine || 0), 0);

    metrics.value = {
      issues_today: issuesPerDay,
      overdue_issues: overdue,
      pending_requests: pendingRequests.value.length,
      total_pending_fine: totalFine
    };
  } catch (err) {
    console.error('Failed to fetch staff data:', err);
  }
};

onMounted(() => fetchData());
</script>

<style scoped>
</style>
