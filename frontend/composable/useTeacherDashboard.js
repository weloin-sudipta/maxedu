import { ref } from 'vue'
import { createResource } from './useFrappeFetch'

export const useTeacherDashboard = () => {
    const user = ref(null)
    const loading = ref(false)
    const error = ref(null)

    const fetchTeacherData = async () => {
        loading.value = true
        error.value = null

        try {
            const resource = createResource({
                url: 'maxedu.api_folder.teacher_data.get_my_profile',
            })

            const res = await resource.submit()

            console.log('RAW API:', res)

            user.value = res || null
            return res
        } catch (err) {
            console.error('Failed to load teacher data:', err)
            error.value = err.message || 'Unknown error'
        } finally {
            loading.value = false
        }
    }

    return { user, loading, error, fetchTeacherData }
}