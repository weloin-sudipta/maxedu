import { ref } from 'vue'
import { createResource } from '~/composable/useFrappeFetch'

export const useStudyMaterials = () => {
  const materials = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchMaterials = async () => {
    loading.value = true
    error.value = null
    try {
      const resource = createResource({
        url: 'maxedu.api_folder.study_materials.get_study_materials',
      })
      const res = await resource.submit()
      materials.value = res || []
      return res
    } catch (err) {
      console.error('Failed to load study materials:', err)
      error.value = err.message || 'Unknown error'
    } finally {
      loading.value = false
    }
  }

  return { materials, loading, error, fetchMaterials }
}
