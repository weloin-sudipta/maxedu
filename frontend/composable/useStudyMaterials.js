// composables/useStudyMaterials.js

import { ref } from 'vue'
import { createResource } from '~/composable/useFrappeFetch'

export const useStudyMaterials = () => {
  const materials = ref([])
  const loading = ref(false)
  const error = ref(null)

  /**
   * Fetch study materials with optional filters
   * @param {Object} filters - { course, topic }
   */
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

  /**
   * Create a new study material with file upload
   * @param {Object} formData - Form data object
   */
  const createMaterial = async (formData) => {
    loading.value = true
    error.value = null
    try {
      // Create FormData for file upload
      const fd = new FormData()
      fd.append('title', formData.title)
      fd.append('course', formData.course)
      if (formData.topic) fd.append('topic', formData.topic)
      if (formData.category) fd.append('category', formData.category)
      if (formData.upload_date) fd.append('upload_date', formData.upload_date)
      if (formData.description) fd.append('description', formData.description)
      if (formData.file) fd.append('file', formData.file)

      const resource = createResource({
        url: 'maxedu.api_folder.study_materials.create_study_material',
        method: 'POST',
        data: fd,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      const res = await resource.submit()

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