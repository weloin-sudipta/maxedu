import { createResource } from "./useFrappeFetch"

export const useExams = async () => {
  const bookResource = createResource({
      url: 'maxedu.api_folder.books.all_available_book',
  })
  const books = await bookResource.submit()
  return books
}