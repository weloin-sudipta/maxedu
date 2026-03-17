<template>
  <div class="p-8 max-w-lg mx-auto bg-white rounded-xl shadow-md space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">Generate Certificate</h1>
    
    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">Name</label>
        <input v-model="form.name" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border" />
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700">Course</label>
        <input v-model="form.course" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border" />
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700">Date</label>
        <input v-model="form.date" type="date" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border" />
      </div>

      <button 
        @click="generateCertificate" 
        :disabled="loading"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
      >
        {{ loading ? 'Generating...' : 'Generate Certificate PDF' }}
      </button>
      
      <p v-if="error" class="text-red-500 text-sm mt-2">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const loading = ref(false)
const error = ref('')

const form = reactive({
  name: 'John Doe',
  course: 'Nuxt 3 Masterclass',
  date: new Date().toISOString().split('T')[0]
})

async function generateCertificate() {
  loading.value = true
  error.value = ''
  
  try {
    const response = await $fetch('/generate-pdf', {
      method: 'POST',
      body: {
        template: 'certificate.html',
        variables: {
          name: form.name,
          course: form.course,
          date: form.date
        }
      },
      responseType: 'blob' // Important to get the PDF as a Blob
    })
    
    // Create a download link for the PDF blob
    const url = window.URL.createObjectURL(response)
    const a = document.createElement('a')
    a.href = url
    a.download = `certificate_${form.name.replace(/\s+/g, '_')}.pdf`
    document.body.appendChild(a)
    a.click()
    
    // Cleanup
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
    
  } catch (err) {
    console.error(err)
    error.value = err.message || 'Failed to generate certificate'
  } finally {
    loading.value = false
  }
}
</script>
