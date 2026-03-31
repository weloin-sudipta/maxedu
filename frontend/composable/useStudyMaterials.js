import { ref, toRaw } from 'vue'
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
        url: 'maxedu.api_folder.study_materials.get_study_materials'
      })
      const res = await resource.submit()

      console.log('API Response in composable:', res)

      // Handle different response structures
      let materialsData = []

      // Check if response has data property
      if (res?.data && Array.isArray(res.data)) {
        materialsData = res.data
      }
      // Check if response itself is an array
      else if (Array.isArray(res)) {
        materialsData = res
      }
      // Check if response has message property with data
      else if (res?.message && Array.isArray(res.message)) {
        materialsData = res.message
      }
      // Check if response has result property
      else if (res?.result && Array.isArray(res.result)) {
        materialsData = res.result
      }

      materials.value = materialsData
      console.log('Materials set to:', materials.value)
      console.log('Materials count:', materials.value.length)

      return res
    } catch (err) {
      console.error('Failed to load study materials:', err)
      error.value = err.message || 'Unknown error'
      materials.value = []
    } finally {
      loading.value = false
    }
  }

  const createMaterial = async (formData) => {
    loading.value = true
    error.value = null

    try {
      console.log("Form data coming from modal:", formData)

      const fd = new FormData()
      fd.append('title', formData.title)
      fd.append('course', formData.course)

      if (formData.topic) fd.append('topic', formData.topic)
      if (formData.category) fd.append('category', formData.category)
      if (formData.upload_date) fd.append('upload_date', formData.upload_date)
      if (formData.description) fd.append('description', formData.description)
      if (formData.file instanceof File) fd.append('file', formData.file)

      const response = await fetch('/api/method/maxedu.api_folder.study_materials.create_study_material', {
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

  const fetchMaterialsByTeacher = async () => {
    loading.value = true
    error.value = null
    try {
      const resource = createResource({
        url: 'maxedu.api_folder.study_materials.get_materials_by_teacher'
      })
      const res = await resource.submit()
      console.log("teacher materials", res);

      materials.value = res?.data || res?.message || res || []
      return res
    } catch (err) {
      console.error('Failed to load study materials by teacher:', err)
      error.value = err.message || 'Unknown error'
      materials.value = []
    } finally {
      loading.value = false
    }
  }

  return {
    materials,
    loading,
    error,
    fetchMaterials,
    createMaterial,
    fetchMaterialsByTeacher
  }
}