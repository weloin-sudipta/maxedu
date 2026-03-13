import { ref, onMounted } from "vue"
import { createResource } from "./useFrappeFetch"

export const useBooks = () => {
    const data = ref([])
    const requestedBook = ref([])
    const allBooks = ref([])
    const loading = ref(false)
    const error = ref(null)

    const fetchAllBooks = async()=>{
        loading.value = true,
        error.value = null
        try {
            const resource = createResource({
                url: 'maxedu.api_folder.books.all_available_book',
            })
            const res = await resource.fetch()
            console.log(res);

            allBooks.value = res
        } catch (err) {
            console.error("Failed to load books:", err)
            error.value = err.message || "Unknown error"
        } finally {
            loading.value = false
        }
    }

    const fetchData = async () => {
        loading.value = true
        error.value = null
        try {
            const resource = createResource({
                url: 'maxedu.api_folder.books.all_borrowed_books',
            })
            const res = await resource.fetch()
            console.log(res);
            
            data.value = res
        } catch (err) {
            console.error("Failed to load books:", err)
            error.value = err.message || "Unknown error"
        } finally {
            loading.value = false
        }
    }

    const fetchRequestedBook= async()=>{
        loading.value = true
        error.value= null
        try {
            const resource = createResource({
                url: 'maxedu.api_folder.books.book_tracking',
            })
            const res = await resource.fetch()
            console.log(res);

            requestedBook.value = res
        } catch (err) {
            console.error("Failed to load books:", err)
            error.value = err.message || "Unknown error"
        } finally {
            loading.value = false
        }
    }

    return { data, loading, error, fetchData, requestedBook, fetchRequestedBook, allBooks,fetchAllBooks }
}