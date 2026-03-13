import { ref, onMounted } from "vue"
import { createResource } from "./useFrappeFetch"

export const useBooks = () => {
    const data = ref([])
    const loading = ref(false)
    const error = ref(null)

    const fetchData = async () => {
        loading.value = true
        error.value = null
        try {
            const resource = createResource({
                url: 'maxedu.api_folder.books.all_borrowed_books',
            })
            const res = await resource.fetch()
            data.value = res
        } catch (err) {
            console.error("Failed to load books:", err)
            error.value = err.message || "Unknown error"
        } finally {
            loading.value = false
        }
    }

    return { data, loading, error, fetchData }
}