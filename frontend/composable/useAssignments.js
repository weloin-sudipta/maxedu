import { ref } from 'vue'
import { createResource } from '~/composable/useFrappeFetch'

export const useAssignments = () => {
  const assignments = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchAssignments = async () => {
    loading.value = true
    error.value = null
    try {
      const resource = createResource({
        url: 'maxedu.api_folder.assignments.get_assignments',
      })
      const res = await resource.submit()
      console.log(res);

      assignments.value = res || []
      return res
    } catch (err) {
      console.error('Failed to load assignments:', err)
      error.value = err.message || 'Unknown error'
    } finally {
      loading.value = false
    }
  }

  const submitAssignment = async (assignmentName, submissionFile) => {
    try {
      const resource = createResource({
        url: 'maxedu.api_folder.assignments.submit_assignment',
      })
      const res = await resource.submit({
        assignment_name: assignmentName,
        submission_file: submissionFile,
      })
      return res
    } catch (err) {
      console.error('Failed to submit assignment:', err)
      return { error: err.message || 'Unknown error' }
    }
  }

  return { assignments, loading, error, fetchAssignments, submitAssignment }
}
