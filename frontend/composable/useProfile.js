import { ref } from 'vue'
import { createResource } from '~/composable/useFrappeFetch'

// import { createResource } from '~/composable/useFrappeFetch'

export const useProfile = async () => {
  const profileResource = createResource({
    url: 'maxedu.api_folder.profile.get_profile',
  })

  const profile = await profileResource.submit()
  return profile
}
// export const useProfile = () => {
//   const profileData = ref(null)
//   const loading = ref(false)
//   const error = ref(null)

//   const loadProfile = async () => {
//     loading.value = true
//     error.value = null
//     try {
//       const resource = createResource({
//         url: 'maxedu.api_folder.profile.get_profile', // Your Frappe API endpoint
//       })
//       const res = await resource.submit()
//       profileData.value = res
//       return res
//     } catch (err) {
//       console.error('Failed to load profile:', err)
//       error.value = err.message || 'Unknown error'
//       profileData.value = null
//     } finally {
//       loading.value = false
//     }
//   }

//   return {
//     profileData,
//     loading,
//     error,
//     loadProfile, // Expose function
//   }
// }

/**
 * Optional: updateProfile helper
 */
export const updateProfile = async (payload) => {
  try {
    const resource = createResource({
      url: 'maxedu.api_folder.profile.update_profile', // Your update API
      method: 'POST',
      body: payload,
    })
    const res = await resource.submit()
    return res
  } catch (err) {
    console.error('Failed to update profile:', err)
    return { error: err.message || 'Unknown error' }
  }
}

// Reactive loader for profile
export const loadProfile = () => {
  const profileData = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchProfile = async () => {
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

  return {
    profileData,
    loading,
    error,
    fetchProfile, // Function to load the profile
  }
}