import { ref, toRaw } from 'vue'
import { createResource } from '~/composable/useFrappeFetch'

export const useStudyMaterials = () => {
  const materials = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchMaterials = async (filters = {}) => {
    loading.value = true
    error.value = null
    try {
      const resource = createResource({
        url: 'maxedu.api_folder.study_materials.get_study_materials',
        params: filters
      })
      const res = await resource.submit()
      materials.value = res?.data || []
      return res
    } catch (err) {
      console.error('Failed to load study materials:', err)
      error.value = err.message || 'Unknown error'
    } finally {
      loading.value = false
    }
  }

  const createMaterial = async (formData) => {
    loading.value = true
    error.value = null

    try {
      console.log("form data comming from ",formData);
      

      const fd = new FormData()
      fd.append('title', formData.title)
      fd.append('course', formData.course)
      if (formData.topic) fd.append('topic', formData.topic)
      if (formData.category) fd.append('category', formData.category)
      if (formData.upload_date) fd.append('upload_date', formData.upload_date)
      if (formData.description) fd.append('description', formData.description)
      if (rawFile instanceof File) fd.append('file', rawFile)

      // Debug: check FormData entries after appending
      console.log('=== FORMDATA ENTRIES ===')
      for (const [key, value] of fd.entries()) {
        console.log(key, ':', value)
      }

      const response = await fetch('/api/method/maxedu.api_folder.teacher_course.create_study_material', {
        method: 'POST',
        body: fd,
        credentials: 'include',
      })

      const json = await response.json()
      const res = json?.message ?? json

      if (res?.success) {
        return res
      } else {
        throw new Error(res?.message || 'Failed to create study material')
      }
    } catch (err) {
      console.error('Failed to create study material:', err)
      error.value = err.message || 'Unknown error'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    materials,
    loading,
    error,
    fetchMaterials,
    createMaterial
  }
}