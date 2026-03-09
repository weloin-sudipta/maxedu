import { auth, createResource } from '~/composable/useFrappeFetch'

export const useUserProfile = () => {

  const profileData = useState('profileData', () => ({
    firstName: '',
    lastName: '',
    email: '',
    fullName: '',
    userImage: ''
  }))

  const userRole = useState('userRole', () => null)

  const loadProfile = async () => {

    // prevent duplicate calls
    if (profileData.value.fullName) return

    const userEmail = await auth.getLoggedUser()

    const profileResource = createResource({
      url: 'frappe.client.get',
      params: {
        doctype: 'User',
        name: userEmail
      }
    })

    const roleResource = createResource({
      url: 'maxedu.api_folder.profile.get_user_info'
    })

    const profile = await profileResource.submit()
    const roleData = await roleResource.submit()

    profileData.value = {
      firstName: profile.first_name || '',
      lastName: profile.last_name || '',
      email: profile.email || '',
      fullName: profile.full_name || '',
      userImage: profile.user_image || ''
    }

    userRole.value = roleData?.role || null

    console.log('User Profile:', profileData.value)
    console.log('User Role:', userRole.value)
  }

  return { profileData, userRole, loadProfile }
}