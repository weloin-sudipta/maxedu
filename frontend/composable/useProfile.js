import { ref } from 'vue'
import { createResource } from '~/composable/useFrappeFetch'

// Direct async profile fetch (used in index.vue)
export const useProfile = async () => {
  const profileResource = createResource({
    url: 'maxedu.api_folder.profile.get_profile',
  })
  const profile = await profileResource.submit()
  return profile
}

// Reactive profile loader (used in edit.vue)
export const useProfileLoader = () => {
  const profileData = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const loadProfile = async () => {
    loading.value = true
    error.value = null
    try {
      const resource = createResource({
        url: 'maxedu.api_folder.profile.get_profile',
      })
      const res = await resource.submit()
      profileData.value = res
      return res
    } catch (err) {
      console.error('Failed to load profile:', err)
      error.value = err.message || 'Unknown error'
      profileData.value = null
    } finally {
      loading.value = false
    }
  }

  return { profileData, loading, error, loadProfile }
}

// Update profile
export const updateProfile = async (payload) => {
  try {
    const resource = createResource({
      url: 'maxedu.api_folder.profile.update_profile',
    })
    const res = await resource.submit({ data: JSON.stringify(payload) })
    return res
  } catch (err) {
    console.error('Failed to update profile:', err)
    return { error: err.message || 'Unknown error' }
  }
}
