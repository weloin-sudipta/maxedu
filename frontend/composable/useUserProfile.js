import { auth, createResource } from '~/composable/useFrappeFetch'

export const useUserProfile = () => {

  const profileData = useState('profileData', () => ({
    firstName: '',
    lastName: '',
    email: '',
    fullName: '',
    userImage: ''
  }))

  const loadProfile = async () => {

    if (profileData.value.fullName) return   // prevents multiple calls

    const userEmail = await auth.getLoggedUser()

    const resource = createResource({
      url: 'frappe.client.get',
      params: {
        doctype: 'User',
        name: userEmail
      }
    })

    const data = await resource.submit()

    profileData.value = {
      firstName: data.first_name || '',
      lastName: data.last_name || '',
      email: data.email || '',
      fullName: data.full_name || '',
      userImage: data.user_image || ''
    }

  }

  return { profileData, loadProfile }

}