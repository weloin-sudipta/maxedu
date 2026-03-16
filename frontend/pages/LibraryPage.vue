<template>
  <div class="books-container">
    <h1>Library Books</h1>

    <!-- Loading state -->
    <div v-if="loading" class="loading">
      <p>Loading books...</p>
    </div>

    <!-- Error state -->
    <div v-if="error && !loading" class="error-alert">
      <p>{{ error }}</p>
      <button @click="initializeBooks">Retry</button>
    </div>

    <!-- Books grid -->
    <div v-if="!loading && !error" class="books-grid">
      <!-- Available books section -->
      <section class="books-section">
        <h2>Available Books</h2>
        <div class="book-list">
          <div
            v-for="book in allBooks"
            :key="book.name || book.id"
            class="book-item"
          >
            <div class="book-details">
              <h3>{{ book.title }}</h3>
              <p class="author">{{ book.author }}</p>
              <p v-if="book.isbn" class="isbn">ISBN: {{ book.isbn }}</p>
              <p v-if="book.description" class="description">
                {{ book.description }}
              </p>
            </div>

            <!-- Request/Cancel Button -->
            <div class="book-actions">
              <button
                @click="handleBookRequest(book)"
                :disabled="bookRequest.loading.value"
                :class="[
                  'btn-request',
                  getButtonStatus(book.name || book.id),
                ]"
              >
                <span
                  v-if="bookRequest.loading.value"
                  class="spinner"
                ></span>
                {{ getButtonText(book.name || book.id) }}
              </button>
            </div>

            <!-- Status message -->
            <div
              v-if="
                bookRequest.successMessage.value &&
                bookRequest.successMessage.value.includes(book.title)
              "
              class="success-msg"
            >
              ✓ {{ bookRequest.successMessage.value }}
            </div>
          </div>
        </div>
      </section>

      <!-- Borrowed books section -->
      <section v-if="data.length > 0" class="books-section">
        <h2>My Borrowed Books</h2>
        <div class="book-list">
          <div v-for="book in data" :key="book.name || book.id" class="book-item">
            <div class="book-details">
              <h3>{{ book.title }}</h3>
              <p class="author">{{ book.author }}</p>
              <p v-if="book.due_date" class="due-date">
                Due: {{ book.due_date }}
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Requested books section -->
      <section v-if="requestedBook.length > 0" class="books-section">
        <h2>Requested Books</h2>
        <div class="book-list">
          <div
            v-for="book in requestedBook"
            :key="book.name || book.id"
            class="book-item"
          >
            <div class="book-details">
              <h3>{{ book.title }}</h3>
              <p class="author">{{ book.author }}</p>
              <p class="status">Status: {{ book.status }}</p>
            </div>
            <div class="book-actions">
              <button
                @click="handleCancelRequest(book)"
                class="btn-cancel"
              >
                Cancel Request
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Recommendations section -->
      <section v-if="recommendations.length > 0" class="books-section">
        <h2>Recommended Books</h2>
        <div class="book-list">
          <div
            v-for="rec in recommendations"
            :key="rec.name || rec.id"
            class="book-item"
          >
            <div class="book-details">
              <h3>{{ rec.title }}</h3>
              <p class="author">{{ rec.author }}</p>
              <p class="reason">{{ rec.reason }}</p>
            </div>
            <div class="book-actions">
              <button
                @click="handleBookRequest(rec)"
                :disabled="bookRequest.loading.value"
                :class="[
                  'btn-request',
                  getButtonStatus(rec.name || rec.id),
                ]"
              >
                {{ getButtonText(rec.name || rec.id) }}
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- Global error message from book request -->
    <div v-if="bookRequest.error.value" class="error-alert">
      {{ bookRequest.error.value }}
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue"
import { useBooks } from "../composable/useLibraryBooks"

const {
  data,
  loading,
  error,
  requestedBook,
  allBooks,
  recommendations,
  fetchData,
  fetchRequestedBook,
  fetchAllBooks,
  fetchRecommendations,
  bookRequest,
  isBookRequested,
  getButtonText,
  getButtonStatus,
  toggleBookRequest,
} = useBooks()

// Initialize all books data
const initializeBooks = async () => {
  // Initialize book request composable first
  await bookRequest.init()

  // Load all book data
  await Promise.all([
    fetchAllBooks(),
    fetchData(),
    fetchRequestedBook(),
    fetchRecommendations(),
  ])
}

// Handle book request with button state change
const handleBookRequest = async (book) => {
  await toggleBookRequest(book)
  // Optionally refresh the requested books list
  await fetchRequestedBook()
}

// Handle cancel request
const handleCancelRequest = async (book) => {
  if (confirm(`Cancel request for "${book.title}"?`)) {
    await bookRequest.cancelRequest(book.name || book.id, book.name)
    // Refresh the requested books list
    await fetchRequestedBook()
  }
}

// Initialize on component mount
onMounted(() => {
  initializeBooks()
})
</script>

<style scoped>
.books-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

h2 {
  color: #555;
  margin-top: 30px;
  margin-bottom: 15px;
  border-bottom: 2px solid #007bff;
  padding-bottom: 10px;
}

.loading,
.error-alert {
  text-align: center;
  padding: 20px;
  border-radius: 8px;
  margin: 20px 0;
}

.loading {
  background-color: #e3f2fd;
  color: #1976d2;
}

.error-alert {
  background-color: #ffebee;
  color: #c62828;
}

.error-alert button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #c62828;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.error-alert button:hover {
  background-color: #b71c1c;
}

.books-grid {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.books-section {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
}

.book-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.book-item {
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.book-item:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.book-details h3 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 16px;
}

.author {
  margin: 0 0 4px 0;
  color: #666;
  font-size: 14px;
}

.isbn,
.due-date,
.status,
.reason {
  margin: 0;
  color: #999;
  font-size: 13px;
}

.description {
  margin: 8px 0 0 0;
  color: #777;
  font-size: 13px;
  line-height: 1.4;
}

.book-actions {
  display: flex;
  gap: 8px;
  margin-top: auto;
}

.btn-request,
.btn-cancel {
  flex: 1;
  padding: 10px 12px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.btn-request.request {
  background-color: #007bff;
  color: white;
}

.btn-request.request:hover:not(:disabled) {
  background-color: #0056b3;
}

.btn-request.cancel {
  background-color: #dc3545;
  color: white;
}

.btn-request.cancel:hover:not(:disabled) {
  background-color: #c82333;
}

.btn-cancel {
  background-color: #6c757d;
  color: white;
}

.btn-cancel:hover {
  background-color: #5a6268;
}

.btn-request:disabled,
.btn-cancel:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

.success-msg {
  background-color: #d4edda;
  color: #155724;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 13px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .book-list {
    grid-template-columns: 1fr;
  }
}
</style>
