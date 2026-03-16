import { ref } from "vue"
import { createResource, call } from "./useFrappeFetch"

export const useBookRequest = () => {
    const requestedBooks = ref(new Set())   // Only books with PENDING requests
    const bookRequestMap = ref({})          // book ID → request doc name
    const loading = ref(false)
    const error = ref(null)
    const successMessage = ref(null)

    // ─── Request a book ────────────────────────────────────────────────────────
    const requestBook = async (bookData) => {
        loading.value = true
        error.value = null
        successMessage.value = null

        try {
            const resource = createResource({
                url: 'maxedu.api_folder.books.request_book',
            })

            const res = await resource.submit({
                book: bookData.name || bookData.id,
                request_type: bookData.requestType || 'Issue'
            })

            const bookId = bookData.name || bookData.id

            // Mark as pending locally so the button flips immediately
            requestedBooks.value.add(bookId)
            if (res && res.name) {
                bookRequestMap.value[bookId] = res.name
            }

            successMessage.value = `Book "${bookData.title}" requested successfully!`
            console.log("Book request created:", res)

            return res
        } catch (err) {
            console.error("Failed to request book:", err)
            error.value = err.message || "Failed to request book"
        } finally {
            loading.value = false
        }
    }

    // ─── Cancel a book request ─────────────────────────────────────────────────
    const cancelRequest = async (bookId, requestId) => {
        loading.value = true
        error.value = null
        successMessage.value = null

        try {
            const resource = createResource({
                url: 'maxedu.api_folder.books.cancel_request',
            })

            const res = await resource.submit({
                request_id: requestId
            })

            // Remove from pending set immediately so button flips back
            requestedBooks.value.delete(bookId)
            delete bookRequestMap.value[bookId]

            successMessage.value = "Book request cancelled successfully!"
            console.log("Book request cancelled:", res)

            return res
        } catch (err) {
            console.error("Failed to cancel request:", err)
            error.value = err.message || "Failed to cancel request"
        } finally {
            loading.value = false
        }
    }

    // ─── Core check: only returns true for PENDING requests ───────────────────
    // `requestedBooks` is populated exclusively from get_all_pending_requests,
    // so this naturally returns false for Approved / Issued / Cancelled books.
    const isBookRequested = (bookId) => {
        return requestedBooks.value.has(bookId)
    }

    const getButtonText   = (bookId) => isBookRequested(bookId) ? "Cancel Request" : "Request Book"
    const getButtonStatus = (bookId) => isBookRequested(bookId) ? 'cancel' : 'request'

    const toggleBookRequest = async (bookData) => {
        const bookId = bookData.name || bookData.id
        if (isBookRequested(bookId)) {
            await cancelRequest(bookId, bookData.requestId)
        } else {
            await requestBook(bookData)
        }
    }

    // ─── Load PENDING requests from the dedicated API ─────────────────────────
    // Uses get_all_pending_requests which already filters status == "Pending",
    // so requestedBooks will never contain Approved/Issued/Cancelled entries.
    const loadUserRequests = async () => {
        loading.value = true
        error.value = null

        try {
            const resource = createResource({
                url: 'maxedu.api_folder.books.get_all_pending_requests',
            })

            const res = await resource.fetch()

            // API now returns:
            // { request_book: ["BOOK-001", ...], requests: [{ name, book, ... }] }
            if (res && Array.isArray(res.request_book)) {

                // Rebuild the pending set
                requestedBooks.value = new Set(res.request_book)

                // Build bookRequestMap from the same response — no second call needed
                bookRequestMap.value = {}
                if (Array.isArray(res.requests)) {
                    res.requests.forEach(req => {
                        bookRequestMap.value[req.book] = req.name
                    })
                }
            }

            console.log("Pending requests loaded:", [...requestedBooks.value])
            return res
        } catch (err) {
            console.error("Failed to load pending requests:", err)
            console.warn("Could not load existing requests - continuing anyway")
        } finally {
            loading.value = false
        }
    }

    const init = async () => {
        await loadUserRequests()
    }

    return {
        requestedBooks,
        bookRequestMap,
        loading,
        error,
        successMessage,
        requestBook,
        cancelRequest,
        isBookRequested,
        getButtonText,
        getButtonStatus,
        toggleBookRequest,
        loadUserRequests,
        init,
    }
}

// ─── Standalone helper (used outside the composable if needed) ─────────────────
export const getPendingRequest = async () => {
    const requestResource = createResource({
        url: 'maxedu.api_folder.books.get_all_pending_requests',
    })
    const request = await requestResource.fetch()   // fetch, not submit — no body needed
    return request
}