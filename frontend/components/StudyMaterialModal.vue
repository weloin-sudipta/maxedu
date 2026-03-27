<!-- components/StudyMaterialModal.vue -->

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity" @click="closeModal"></div>

    <!-- Modal Panel -->
    <div class="flex min-h-full items-center justify-center p-4 text-center sm:p-0">
      <div class="relative transform overflow-hidden rounded-2xl bg-white dark:bg-slate-900 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
        
        <!-- Header -->
        <div class="px-6 pt-6 pb-4 border-b border-slate-200 dark:border-slate-800">
          <div class="flex items-start justify-between">
            <div>
              <h3 class="text-lg font-black text-slate-900 dark:text-white" id="modal-title">
                Upload Study Material
              </h3>
              <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
                Add new learning resources to the course
              </p>
            </div>
            <button
              @click="closeModal"
              class="text-slate-400 hover:text-slate-500 dark:hover:text-slate-300 transition-colors"
            >
              <i class="fa fa-times"></i>
            </button>
          </div>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="px-6 py-4 space-y-4">
          
          <!-- Title (Required) -->
          <div>
            <label class="block text-xs font-black uppercase tracking-wider text-slate-600 dark:text-slate-400 mb-2">
              Title <span class="text-red-500">*</span>
            </label>
            <input
              type="text"
              v-model="formData.title"
              class="w-full px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all"
              placeholder="Enter study material title"
              required
            />
          </div>

          <!-- Course (Required - Pre-selected) -->
          <div>
            <label class="block text-xs font-black uppercase tracking-wider text-slate-600 dark:text-slate-400 mb-2">
              Course <span class="text-red-500">*</span>
            </label>
            <select
              v-model="formData.course"
              class="w-full px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all"
              required
              :disabled="!!preselectedCourse"
            >
              <option v-if="!preselectedCourse" value="">Select a course</option>
              <option
                v-for="course in courses"
                :key="course.name"
                :value="course.name"
              >
                {{ course.course_name }}
              </option>
            </select>
            <p v-if="preselectedCourse" class="text-xs text-slate-400 mt-1">
              Course is pre-selected from current view
            </p>
          </div>

          <!-- Topic (Optional - Pre-selected if from topic button) -->
          <div>
            <label class="block text-xs font-black uppercase tracking-wider text-slate-600 dark:text-slate-400 mb-2">
              Topic <span class="text-slate-400 text-[10px]">(Optional)</span>
            </label>
            <select
              v-model="formData.topic"
              class="w-full px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all"
              :disabled="!!preselectedTopic"
            >
              <option value="">Select a topic (optional)</option>
              <option
                v-for="topic in availableTopics"
                :key="topic.name"
                :value="topic.name"
              >
                {{ topic.topic_name || topic.name }}
              </option>
            </select>
            <p v-if="preselectedTopic" class="text-xs text-indigo-500 mt-1">
              <i class="fa fa-link"></i> Topic is pre-selected for this material
            </p>
          </div>

          <!-- Category (Optional) -->
          <div>
            <label class="block text-xs font-black uppercase tracking-wider text-slate-600 dark:text-slate-400 mb-2">
              Category <span class="text-slate-400 text-[10px]">(Optional)</span>
            </label>
            <select
              v-model="formData.category"
              class="w-full px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all"
            >
              <option value="">Select category</option>
              <option value="Lecture Notes">📝 Lecture Notes</option>
              <option value="Video">🎥 Video</option>
              <option value="Presentation">📊 Presentation</option>
              <option value="Assignment">📋 Assignment</option>
              <option value="Reference">📚 Reference</option>
              <option value="Other">📄 Other</option>
            </select>
          </div>

          <!-- File Upload (Required) -->
          <div>
            <label class="block text-xs font-black uppercase tracking-wider text-slate-600 dark:text-slate-400 mb-2">
              File <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <input
                type="file"
                ref="fileInput"
                @change="handleFileChange"
                class="hidden"
                accept=".pdf,.doc,.docx,.ppt,.pptx,.txt,.jpg,.jpeg,.png,.mp4,.zip"
              />
              <div
                @click="$refs.fileInput.click()"
                class="w-full px-4 py-3 rounded-xl border-2 border-dashed border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50 cursor-pointer hover:border-indigo-300 dark:hover:border-indigo-500 transition-all"
              >
                <div class="text-center">
                  <i class="fa fa-cloud-upload text-2xl text-slate-400 mb-2"></i>
                  <p class="text-sm text-slate-600 dark:text-slate-400">
                    {{ fileSelected ? fileSelected.name : 'Click to upload or drag and drop' }}
                  </p>
                  <p class="text-xs text-slate-400 mt-1">
                    PDF, DOC, PPT, Images, MP4 (Max 50MB)
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Upload Date (Optional) -->
          <div>
            <label class="block text-xs font-black uppercase tracking-wider text-slate-600 dark:text-slate-400 mb-2">
              Upload Date <span class="text-slate-400 text-[10px]">(Optional)</span>
            </label>
            <input
              type="date"
              v-model="formData.upload_date"
              class="w-full px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all"
            />
          </div>

          <!-- Description (Optional) -->
          <div>
            <label class="block text-xs font-black uppercase tracking-wider text-slate-600 dark:text-slate-400 mb-2">
              Description <span class="text-slate-400 text-[10px]">(Optional)</span>
            </label>
            <textarea
              v-model="formData.description"
              rows="3"
              class="w-full px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all resize-none"
              placeholder="Add a detailed description of the study material..."
            ></textarea>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="p-3 rounded-xl bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800">
            <p class="text-xs text-red-600 dark:text-red-400">{{ error }}</p>
          </div>

          <!-- Actions -->
          <div class="flex gap-3 pt-4">
            <button
              type="button"
              @click="closeModal"
              class="flex-1 px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-sm font-bold hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="loading"
              class="flex-1 px-4 py-2 rounded-xl bg-indigo-600 dark:bg-indigo-500 text-white text-sm font-bold hover:bg-indigo-700 dark:hover:bg-indigo-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <i v-if="loading" class="fa fa-spinner fa-spin"></i>
              {{ loading ? 'Uploading...' : 'Upload Material' }}
            </button>
          </div>

        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useStudyMaterials } from '~/composable/useStudyMaterials'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  preselectedCourse: {
    type: String,
    default: null
  },
  preselectedTopic: {
    type: String,
    default: null
  },
  preselectedTopicName: {
    type: String,
    default: null
  },
  courses: {
    type: Array,
    required: true
  },
  topics: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'success'])

const { createMaterial, loading: createLoading, error: createError } = useStudyMaterials()
const loading = computed(() => createLoading.value)
const error = ref(null)
const fileSelected = ref(null)
const fileInput = ref(null)

// Find the selected topic object if topic name is provided
const selectedTopicObject = computed(() => {
  if (props.preselectedTopic) {
    return props.topics.find(t => t.name === props.preselectedTopic)
  }
  return null
})

const formData = ref({
  title: '',
  course: props.preselectedCourse || '',
  topic: props.preselectedTopic || '',
  category: '',
  file: null,
  upload_date: new Date().toISOString().split('T')[0],
  description: ''
})

// Available topics based on selected course
const availableTopics = computed(() => {
  if (!formData.value.course) return []
  const selectedCourse = props.courses.find(c => c.name === formData.value.course)
  return selectedCourse?.topics || []
})

// Watch for course changes to reset topic if not preselected
watch(() => formData.value.course, (newCourse) => {
  if (!props.preselectedTopic) {
    formData.value.topic = ''
  }
})

// Watch for error from composable
watch(() => createError.value, (newError) => {
  if (newError) {
    error.value = newError
  }
})

// Handle file selection
const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Validate file size (50MB)
    if (file.size > 50 * 1024 * 1024) {
      error.value = 'File size must be less than 50MB'
      fileSelected.value = null
      formData.value.file = null
      return
    }
    
    fileSelected.value = file
    formData.value.file = file
    error.value = null
  }
}

// Handle form submission
const handleSubmit = async () => {
  error.value = null
  
  // Validate required fields
  if (!formData.value.title.trim()) {
    error.value = 'Title is required'
    return
  }
  
  if (!formData.value.course) {
    error.value = 'Course is required'
    return
  }
  
  if (!formData.value.file) {
    error.value = 'File is required'
    return
  }
  
  try {
    const result = await createMaterial(formData.value)
    
    if (result?.success) {
      emit('success', result.data)
      closeModal()
    } else {
      error.value = result?.message || 'Failed to upload study material'
    }
  } catch (err) {
    error.value = err.message || 'An error occurred while uploading'
  }
}

// Close modal and reset form
const closeModal = () => {
  resetForm()
  emit('close')
}

// Reset form data
const resetForm = () => {
  formData.value = {
    title: '',
    course: props.preselectedCourse || '',
    topic: props.preselectedTopic || '',
    category: '',
    file: null,
    upload_date: new Date().toISOString().split('T')[0],
    description: ''
  }
  fileSelected.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
  error.value = null
}

// Reset when modal opens with new preselected course/topic
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    formData.value.course = props.preselectedCourse || ''
    formData.value.topic = props.preselectedTopic || ''
    resetForm()
  }
})
</script>

<style scoped>
/* Smooth animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.fixed {
  animation: fadeIn 0.2s ease-out;
}

/* Custom scrollbar for modal */
.overflow-y-auto {
  scrollbar-width: thin;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>