<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-white p-4 lg:p-8 font-sans">
    <div class="max-w-5xl mx-auto space-y-8">
      
      <!-- Header -->
      <header class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 p-8">
        <h1 class="text-3xl font-black tracking-tight text-slate-800">Book Issuance</h1>
        <p class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mt-1">
          Issue approved books to members
        </p>
      </header>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <!-- Pending Requests Column -->
        <div class="lg:col-span-1 space-y-4">
          <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden">
            
            <!-- Header -->
            <div class="p-6 border-b border-slate-50 bg-slate-50/50">
              <h2 class="text-lg font-black text-slate-800">Pending Requests</h2>
              <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">
                Approved for issuance
              </p>
            </div>

            <!-- Loading State -->
            <div v-if="loadingRequests" class="p-8 text-center">
              <i class="fa fa-spinner fa-spin text-indigo-600 text-2xl mb-4"></i>
              <p class="text-[10px] font-black text-slate-400 uppercase">Loading...</p>
            </div>

            <!-- Requests List -->
            <div v-else class="divide-y divide-slate-50 max-h-96 overflow-y-auto">
              <div v-for="request in pendingRequests" :key="request.name"
                   @click="selectRequest(request)"
                   :class="['p-4 cursor-pointer transition-all', 
                     selectedRequest?.name === request.name 
                       ? 'bg-indigo-50 border-l-4 border-indigo-600' 
                       : 'hover:bg-slate-50'
                   ]">
                <div class="flex items-start justify-between mb-2">
                  <div>
                    <p class="text-xs font-black text-slate-800">{{ request.book_title }}</p>
                    <p class="text-[10px] font-bold text-slate-400 uppercase">{{ request.member_name }}</p>
                  </div>
                  <span class="px-2 py-1 rounded text-[8px] font-black uppercase bg-indigo-100 text-indigo-700">
                    {{ request.status }}
                  </span>
                </div>
                <p class="text-[9px] text-slate-500">{{ formatDate(request.request_date) }}</p>
              </div>

              <!-- Empty State -->
              <div v-if="pendingRequests.length === 0" class="p-8 text-center">
                <i class="fa fa-inbox text-slate-100 text-3xl mb-4"></i>
                <p class="text-[10px] font-black text-slate-400 uppercase">No pending requests</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Issuance Form Column -->
        <div class="lg:col-span-2 space-y-4">
          
          <div v-if="!selectedRequest" class="bg-white rounded-[2.5rem] shadow-sm border border-dashed border-slate-300 p-12 text-center">
            <i class="fa fa-book text-slate-100 text-5xl mb-4"></i>
            <p class="text-sm font-black text-slate-400 uppercase">Select a pending request to begin issuance</p>
          </div>

          <div v-else class="space-y-4">
            
            <!-- Request Details Card -->
            <div class="bg-gradient-to-br from-indigo-50 to-slate-50 rounded-[2.5rem] shadow-sm border border-indigo-100/50 p-6">
              <h3 class="text-sm font-black text-slate-800 mb-4">Request Details</h3>
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-[10px] font-bold text-slate-400 uppercase">Book Title</span>
                  <p class="text-slate-800 font-black mt-1">{{ selectedRequest.book_title }}</p>
                </div>
                <div>
                  <span class="text-[10px] font-bold text-slate-400 uppercase">Member</span>
                  <p class="text-slate-800 font-black mt-1">{{ selectedRequest.member_name }}</p>
                </div>
                <div>
                  <span class="text-[10px] font-bold text-slate-400 uppercase">Book ID</span>
                  <p class="text-slate-800 font-black mt-1">{{ selectedRequest.book }}</p>
                </div>
                <div>
                  <span class="text-[10px] font-bold text-slate-400 uppercase">Requested</span>
                  <p class="text-slate-800 font-black mt-1">{{ formatDate(selectedRequest.request_date) }}</p>
                </div>
              </div>
            </div>

            <!-- Book Copy Selection -->
            <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden">
              <div class="p-6 border-b border-slate-50 bg-slate-50/50">
                <h3 class="text-sm font-black text-slate-800">Select Book Copy</h3>
                <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">
                  Choose an available copy by ISBN
                </p>
              </div>

              <div class="p-6 space-y-4">
                <!-- Loading -->
                <div v-if="loadingCopies" class="text-center py-8">
                  <i class="fa fa-spinner fa-spin text-indigo-600 text-2xl mb-2"></i>
                  <p class="text-[10px] font-black text-slate-400 uppercase">Finding available copies...</p>
                </div>

                <!-- Available Copies -->
                <div v-else-if="availableCopies.length > 0" class="space-y-3">
                  <div v-for="copy in availableCopies" :key="copy.name"
                       @click="selectedCopy = copy"
                       :class="['p-4 border-2 rounded-2xl cursor-pointer transition-all',
                         selectedCopy?.name === copy.name
                           ? 'border-indigo-600 bg-indigo-50'
                           : 'border-slate-200 bg-slate-50 hover:border-indigo-300'
                       ]">
                    <div class="flex items-start justify-between">
                      <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-xl bg-white border border-slate-200 flex items-center justify-center text-indigo-600">
                          <i class="fa fa-barcode text-xs"></i>
                        </div>
                        <div>
                          <p class="text-xs font-black text-slate-800">ISBN: {{ copy.name }}</p>
                          <p class="text-[10px] font-bold text-slate-400">
                            {{ copy.total_copies }} total • {{ copy.available_copies }} available
                          </p>
                        </div>
                      </div>
                      <span class="px-3 py-1 rounded-lg bg-green-100 text-green-700 text-[9px] font-black uppercase">
                        Available
                      </span>
                    </div>
                    <div class="mt-3 p-3 bg-white rounded-xl border border-slate-100">
                      <div class="text-[10px] font-bold text-slate-600">
                        <span class="uppercase text-slate-400">Borrow Period:</span> {{ copy.borrow_period_days }} days
                      </div>
                      <div class="text-[10px] font-bold text-slate-600 mt-1">
                        <span class="uppercase text-slate-400">Fine/Day:</span> ₹{{ copy.fine_per_day || 0 }}
                      </div>
                    </div>
                  </div>
                </div>

                <!-- No Copies -->
                <div v-else class="py-8 text-center">
                  <i class="fa fa-archive text-slate-100 text-3xl mb-4"></i>
                  <p class="text-[10px] font-black text-slate-400 uppercase">No available copies</p>
                </div>
              </div>
            </div>

            <!-- Issue Confirmation -->
            <div v-if="selectedCopy" class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 overflow-hidden">
              <div class="p-6 border-b border-slate-50 bg-slate-50/50">
                <h3 class="text-sm font-black text-slate-800">Issue Summary</h3>
              </div>

              <div class="p-6 space-y-4">
                <div class="flex items-start gap-4 p-4 rounded-2xl bg-indigo-50 border border-indigo-100">
                  <i class="fa fa-check-circle text-indigo-600 text-lg mt-1"></i>
                  <div class="flex-1">
                    <p class="text-xs font-black text-slate-800">Ready to Issue</p>
                    <div class="space-y-2 mt-3 text-[10px] font-bold text-slate-600">
                      <div class="flex justify-between">
                        <span class="text-slate-400 uppercase">Issue Date:</span>
                        <span>{{ formatDate(today()) }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span class="text-slate-400 uppercase">Due Date:</span>
                        <span class="text-amber-600 font-black">{{ formatDate(calculateDueDate()) }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span class="text-slate-400 uppercase">Borrow Period:</span>
                        <span>{{ selectedCopy.borrow_period_days }} days</span>
                      </div>
                      <div v-if="selectedCopy.fine_per_day" class="flex justify-between">
                        <span class="text-slate-400 uppercase">Daily Fine:</span>
                        <span>₹{{ selectedCopy.fine_per_day }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Action Buttons -->
                <div class="flex gap-3 pt-4">
                  <button @click="cancelIssue"
                    class="flex-1 px-6 py-3 rounded-2xl text-[10px] font-black uppercase tracking-widest border border-slate-300 text-slate-700 hover:bg-slate-50 transition-all">
                    Cancel
                  </button>
                  <button @click="issueBook"
                    :disabled="issuingBook"
                    :class="['flex-1 px-6 py-3 rounded-2xl text-[10px] font-black uppercase tracking-widest transition-all',
                      issuingBook
                        ? 'bg-slate-300 text-slate-600 cursor-not-allowed'
                        : 'bg-indigo-600 text-white hover:bg-indigo-700 shadow-lg shadow-indigo-200'
                    ]">
                    <i v-if="issuingBook" class="fa fa-spinner fa-spin mr-2"></i>
                    {{ issuingBook ? 'Issuing...' : 'Issue Book' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Success Modal -->
      <div v-if="showSuccessModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-[2.5rem] shadow-2xl max-w-md w-full p-8 text-center animate-in zoom-in duration-300">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <i class="fa fa-check text-green-600 text-2xl"></i>
          </div>
          <h2 class="text-xl font-black text-slate-800 mb-2">Book Issued Successfully!</h2>
          <p class="text-sm text-slate-600 mb-6">
            The book has been issued to {{ selectedRequest?.member_name }}
          </p>
          <div class="bg-slate-50 rounded-2xl p-4 mb-6 text-left text-[10px] text-slate-600 space-y-2">
            <div class="flex justify-between">
              <span class="font-bold">Book:</span>
              <span>{{ selectedRequest?.book_title }}</span>
            </div>
            <div class="flex justify-between">
              <span class="font-bold">ISBN:</span>
              <span>{{ selectedCopy?.name }}</span>
            </div>
            <div class="flex justify-between">
              <span class="font-bold">Due Date:</span>
              <span class="font-black text-amber-600">{{ formatDate(calculateDueDate()) }}</span>
            </div>
          </div>
          <button @click="resetForm"
            class="w-full px-6 py-3 bg-indigo-600 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-indigo-700 transition-all">
            Issue Another Book
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { createResource } from '~/composable/useFrappeFetch';

const selectedRequest = ref(null);
const selectedCopy = ref(null);
const pendingRequests = ref([]);
const availableCopies = ref([]);
const loadingRequests = ref(false);
const loadingCopies = ref(false);
const issuingBook = ref(false);
const showSuccessModal = ref(false);

// Fetch pending book requests (Approved status)
const fetchPendingRequests = async () => {
  loadingRequests.value = true;
  try {
    const resource = createResource({
      url: 'frappe.client.get_list',
      args: {
        doctype: 'Book Request',
        filters: { status: 'Approved' },
        fields: ['name', 'member', 'member_name', 'book', 'book_title', 'request_date', 'status'],
        order_by: 'request_date asc'
      }
    });
    const res = await resource.fetch();
    pendingRequests.value = res || [];
  } catch (err) {
    console.error("Failed to load requests:", err);
  } finally {
    loadingRequests.value = false;
  }
};

// Fetch available copies for a book
const fetchAvailableCopies = async (bookId) => {
  loadingCopies.value = true;
  selectedCopy.value = null;
  try {
    const resource = createResource({
      url: 'frappe.client.get_list',
      args: {
        doctype: 'Library Book Inventory',
        filters: { book: bookId, copy_type: 'Physical', is_issued: 0 },
        fields: ['name', 'book', 'copy_type', 'is_issued', 'available_copies', 'total_copies', 'borrow_period_days', 'fine_per_day'],
        order_by: 'name asc'
      }
    });
    const res = await resource.fetch();
    availableCopies.value = res || [];
  } catch (err) {
    console.error("Failed to load copies:", err);
  } finally {
    loadingCopies.value = false;
  }
};

// Select a book request and fetch its available copies
const selectRequest = async (request) => {
  selectedRequest.value = request;
  selectedCopy.value = null;
  await fetchAvailableCopies(request.book);
};

// Calculate due date based on borrow period
const calculateDueDate = () => {
  if (!selectedCopy.value) return null;
  const today = new Date();
  const dueDate = new Date(today);
  dueDate.setDate(dueDate.getDate() + (selectedCopy.value.borrow_period_days || 14));
  return dueDate;
};

// Format date helper
const formatDate = (dateObj) => {
  if (!dateObj) return '';
  const date = dateObj instanceof Date ? dateObj : new Date(dateObj);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
};

// Get today's date
const today = () => new Date();

// Issue the book
const issueBook = async () => {
  if (!selectedRequest.value || !selectedCopy.value) return;

  issuingBook.value = true;
  try {
    const resource = createResource({
      url: 'maxedu.api_folder.library.issue_book_to_member',
      args: {
        book_request_id: selectedRequest.value.name,
        isbn: selectedCopy.value.name
      }
    });
    const res = await resource.fetch();
    if (res.success) {
      showSuccessModal.value = true;
      // Refresh the list
      await fetchPendingRequests();
    }
  } catch (err) {
    frappe.show_alert({message: err.message || "Issuance failed", indicator: 'red'});
  } finally {
    issuingBook.value = false;
  }
};

// Cancel current issuance
const cancelIssue = () => {
  selectedRequest.value = null;
  selectedCopy.value = null;
  availableCopies.value = [];
};

// Reset and prepare for next issuance
const resetForm = () => {
  showSuccessModal.value = false;
  selectedRequest.value = null;
  selectedCopy.value = null;
  availableCopies.value = [];
  // Don't refetch as we already did during issuance
};

// Initialize
onMounted(async () => {
  await fetchPendingRequests();
});
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.zoom-enter-active, .zoom-leave-active { transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.zoom-enter-from, .zoom-leave-to { transform: scale(0.95); opacity: 0; }
</style>
