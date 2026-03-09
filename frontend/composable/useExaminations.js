import { ref } from 'vue'
import { createResource } from '~/composable/useFrappeFetch'

// Direct async profile fetch (used in index.vue)
export const useExams = async () => {
  const examResource = createResource({
    url: 'maxedu.api_folder.exam.get_exams',
  })
  const exams = await examResource.submit()
  return exams
}

export const useExamResults = async () => {
  const resultResource = createResource({
    url: 'maxedu.api_folder.exam.get_results',
  })
  const results = await resultResource.submit()
  return results
}