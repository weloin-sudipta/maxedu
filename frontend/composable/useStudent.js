import { call } from '~/composable/useFrappeFetch'

export const fetchStudents = async (userEmail) => {
  try {
    const response = await call(
      'maxedu.api_folder.student.get_student_by_institute',
      userEmail ? { user_email: userEmail } : {}
    )

    return response
  } catch (error) {
    console.error('Error fetching students:', error)
    throw error
  }
}