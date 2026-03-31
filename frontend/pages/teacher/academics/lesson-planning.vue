<!-- pages/lesson-planning.vue -->

<template>
  <div class="p-6 lg:p-10 max-w-7xl mx-auto custom-scrollbar animate-in fade-in slide-in-from-bottom-4 duration-500">

    <HeroHeader title="Lesson Planning" subtitle="Curriculum Tracking" icon="fa fa-map-signs">
      <div class="flex gap-2">

        <!-- Dynamic Course Dropdown -->
        <select
          v-model="selectedCourse"
          @change="onCourseChange"
          class="bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-200 px-4 py-2 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-800 outline-none"
        >
          <option
            v-for="course in courses"
            :key="course.name"
            :value="course.name"
          >
            {{ course.course_name }}
          </option>
        </select>

        <button 
          @click="openModal"
          class="bg-indigo-600 dark:bg-indigo-500 text-white px-6 py-2 rounded-xl text-xs font-black uppercase tracking-widest hover:bg-indigo-700 dark:hover:bg-indigo-600 transition-colors shadow-lg shadow-indigo-200 dark:shadow-none flex items-center gap-2"
        >
          <i class="fa fa-upload"></i> Upload Material
        </button>

      </div>
    </HeroHeader>

    <!-- Loading -->
    <div v-if="loading" class="mt-8">
      <UiSkeleton height="h-96" class="rounded-[2.5rem]" />
    </div>

    <!-- Content -->
    <div v-else class="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Topics List -->
      <div class="lg:col-span-3">
        <div class="bg-white dark:bg-slate-900 rounded-[2.5rem] border border-slate-100 dark:border-slate-800 shadow-sm p-8">

          <h3 class="text-xs font-black uppercase text-slate-400 dark:text-slate-500 tracking-widest mb-6">
            Topics
          </h3>

          <div v-if="topics.length === 0" class="text-sm text-slate-400">
            No topics available for this course.
          </div>

          <div v-else class="space-y-6">

            <div
              v-for="(topic, i) in topics"
              :key="topic.name"
              class="flex gap-6 group"
            >

              <!-- Step Index -->
              <div class="flex flex-col items-center">
                <div class="w-8 h-8 rounded-full flex items-center justify-center font-black text-xs bg-slate-100 text-slate-400 dark:bg-slate-800 dark:text-slate-500 group-hover:bg-indigo-100 group-hover:text-indigo-500">
                  {{ i + 1 }}
                </div>
                <div v-if="i < topics.length - 1" class="w-px h-full bg-slate-100 dark:bg-slate-800 mt-2"></div>
              </div>

              <!-- Topic Card -->
              <div class="flex-1 bg-slate-50 dark:bg-slate-800/50 p-6 rounded-2xl border border-slate-100 dark:border-slate-700/50 group-hover:border-indigo-200 dark:group-hover:border-indigo-500/30 transition-all">

                <div class="flex justify-between items-start mb-2">
                  <div>
                    <span class="text-[10px] font-black uppercase tracking-widest text-indigo-500 mb-1 block">
                      Topic {{ i + 1 }}
                    </span>

                    <h4 class="text-sm font-black text-slate-800 dark:text-slate-200">
                      {{ topic.topic_name }}
                    </h4>
                  </div>
                  <div class="flex items-center gap-2">
                  <span class="text-xs text-slate-400">{{ getMaterialsForTopic(topic.topic_name).length }} materials</span>
                  <button
                    @click="openTopicMaterials(topic.topic_name)"
                    class="text-[10px] font-black uppercase tracking-widest text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200 dark:border-indigo-800 px-2 py-1 rounded-lg hover:bg-indigo-100 dark:hover:bg-indigo-900/40 transition-colors"
                  >
                    Show Materials
                  </button>
                </div>
              </div> <!-- close .flex.justify-between -->

                <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed max-w-lg mb-4">
                  {{ topic.topic || topic.topic_name }}
                </p>

                <!-- Display existing materials -->
                <div v-if="getMaterialsForTopic(topic.topic_name).length > 0" class="flex flex-wrap gap-2 mb-3">
                  <div 
                    v-for="material in getMaterialsForTopic(topic.topic_name)"
                    :key="material.name"
                    class="flex items-center gap-2 text-[10px] font-bold text-slate-600 dark:text-slate-300 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 px-3 py-1.5 rounded-lg shadow-sm"
                  >
                    <i class="fa" :class="getFileIcon(material.file)"></i> 
                    <span class="truncate max-w-[150px]">{{ material.title }}</span>
                  </div>
                </div>

                <!-- Add Material Button -->
                <button 
                  @click="openModalWithTopic(topic.topic_name)"
                  class="flex items-center gap-2 text-[10px] font-bold text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200 dark:border-indigo-800 px-3 py-1.5 rounded-lg hover:bg-indigo-100 dark:hover:bg-indigo-900/40 transition-colors"
                >
                  <i class="fa fa-plus"></i> Add Material to {{ topic.topic_name }}
                </button>

              </div>
            </div>

          </div>
        </div>
      </div>

    </div>

    <!-- Success Toast -->
    <div v-if="showSuccess" class="fixed bottom-4 right-4 z-50 animate-in slide-in-from-right-4 duration-300">
      <div class="bg-green-500 text-white px-6 py-3 rounded-xl shadow-lg flex items-center gap-2">
        <i class="fa fa-check-circle"></i>
        <span class="text-sm font-medium">Study material uploaded successfully!</span>
      </div>
    </div>

    <!-- Error Toast -->
    <div v-if="showError" class="fixed bottom-4 right-4 z-50 animate-in slide-in-from-right-4 duration-300">
      <div class="bg-red-500 text-white px-6 py-3 rounded-xl shadow-lg flex items-center gap-2">
        <i class="fa fa-exclamation-circle"></i>
        <span class="text-sm font-medium">{{ errorMessage }}</span>
      </div>
    </div>

    <!-- Topic Materials Preview Modal -->
    <div v-if="materialsDialogOpen" class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4">
      <div class="w-full max-w-4xl bg-white dark:bg-slate-900 rounded-2xl p-6 overflow-y-auto max-h-[90vh] shadow-xl">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-black text-slate-900 dark:text-slate-100">Materials for {{ selectedTopicTitle }}</h3>
          <button @click="closeTopicMaterials" class="text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white">✕</button>
        </div>

        <div v-if="selectedTopicMaterials.length === 0" class="py-8 text-center text-sm text-slate-500 dark:text-slate-400">
          No materials found for this topic.
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="material in selectedTopicMaterials"
            :key="material.name"
            class="bg-slate-50 dark:bg-slate-800/50 p-4 rounded-xl border border-slate-200 dark:border-slate-700"
          >
            <div class="flex flex-wrap justify-between gap-4 items-start">
              <div>
                <h4 class="font-black text-sm text-slate-800 dark:text-slate-200">{{ material.title }}</h4>
                <p class="text-[10px] text-slate-500 dark:text-slate-400">{{ material.course }} • {{ material.category }}</p>
                <p class="text-[10px] text-slate-400 dark:text-slate-500">{{ material.topic || 'No topic' }}</p>
              </div>
              <div class="flex gap-2">
                <button @click="editMaterial(material)" class="text-[10px] font-black uppercase tracking-widest bg-yellow-200 text-yellow-700 px-2 py-1 rounded">Edit</button>
                <button @click="deleteMaterial(material)" class="text-[10px] font-black uppercase tracking-widest bg-red-500 text-white px-2 py-1 rounded">Delete</button>
              </div>
            </div>
            <div class="mt-2 flex flex-wrap gap-2 text-[10px] text-slate-500 dark:text-slate-400">
              <span>{{ material.file_type || 'FILE' }}</span>
              <span>{{ material.file_size || '-' }}</span>
              <span>{{ material.upload_date || '-' }}</span>
            </div>
            <div class="mt-2 flex items-center gap-2">
              <a :href="getFileUrl(material.file)" target="_blank" class="text-xs font-black text-indigo-600 dark:text-indigo-400">Preview</a>
              <a :href="getFileUrl(material.file, true)" class="text-xs font-black text-indigo-600 dark:text-indigo-400">Download</a>
            </div>
            <p v-if="material.description" class="mt-2 text-[10px] text-slate-400 dark:text-slate-500">{{ material.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Study Material Modal -->
    <StudyMaterialModal
      :is-open="modalOpen"
      :mode="modalMode"
      :material="materialToEdit"
      :preselected-course="selectedCourse"
      :preselected-topic-name="preselectedTopicName"
      :courses="courses"
      :topics="topics"
      @close="closeModal"
      @success="onMaterialUploaded"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import HeroHeader from '~/components/ui/HeroHeader.vue'
import StudyMaterialModal from '~/components/StudyMaterialModal.vue'
import { useCourseTopics } from '~/composable/useCourseTopics'
import { useStudyMaterials } from '~/composable/useStudyMaterials'

const { fetchCourseTopics } = useCourseTopics()
const { materials, teacherMaterials, fetchMaterials, fetchMaterialsByTeacher, deleteMaterial: deleteMaterialAPI, loading: materialsLoading } = useStudyMaterials()

const loading = ref(true)
const courses = ref([])
const selectedCourse = ref(null)
const modalOpen = ref(false)
const modalMode = ref('create')
const materialToEdit = ref(null)
const preselectedTopicName = ref(null)
const materialsDialogOpen = ref(false)
const selectedTopicTitle = ref('')
const selectedTopicMaterials = ref([])
const showSuccess = ref(false)
const showError = ref(false)
const errorMessage = ref('')

/**
 * Fetch data
 */
const loadData = async () => {
  try {
    const res = await fetchCourseTopics()
    courses.value = res || []

    if (courses.value.length > 0) {
      selectedCourse.value = courses.value[0].name
      // Fetch materials for the selected course
      await fetchMaterials({ course: selectedCourse.value })
    }
  } catch (error) {
    console.error('Error loading data:', error)
  } finally {
    loading.value = false
  }
}

/**
 * Handle course change
 */
const onCourseChange = async () => {
  loading.value = true
  await fetchMaterials({ course: selectedCourse.value })
  loading.value = false
}

/**
 * Selected course object
 */
const selectedCourseData = computed(() => {
  return courses.value.find(c => c.name === selectedCourse.value)
})

/**
 * Topics of selected course
 */
const topics = computed(() => {
  return selectedCourseData.value?.topics || []
})

/**
 * Get materials for a specific topic (teacher data source)
 */
const getMaterialsForTopic = (topicName) => {
  if (!topicName) return teacherMaterials.value.filter(m => !m.topic)
  return teacherMaterials.value.filter(m => m.topic === topicName)
}

const openTopicMaterials = (topicName) => {
  selectedTopicTitle.value = topicName || 'Uncategorized'
  selectedTopicMaterials.value = getMaterialsForTopic(topicName)
  materialsDialogOpen.value = true
}

const closeTopicMaterials = () => {
  materialsDialogOpen.value = false
  selectedTopicTitle.value = ''
  selectedTopicMaterials.value = []
}

const deleteMaterial = async (material) => {
  if (!confirm(`Delete study material '${material.title}'?`)) return
  try {
    await deleteMaterialAPI(material.name)
    teacherMaterials.value = teacherMaterials.value.filter(m => m.name !== material.name)
    selectedTopicMaterials.value = selectedTopicMaterials.value.filter(m => m.name !== material.name)
    // No need to refetch since we updated locally
  } catch (err) {
    console.error('Failed to delete material', err)
    handleError('Could not delete material.')
  }
}

/**
 * Get file icon based on file type
 */
const getFileIcon = (fileUrl) => {
  if (!fileUrl) return 'fa-file-o'
  const ext = fileUrl.split('.').pop().toLowerCase()
  const iconMap = {
    pdf: 'fa-file-pdf-o',
    doc: 'fa-file-word-o',
    docx: 'fa-file-word-o',
    ppt: 'fa-file-powerpoint-o',
    pptx: 'fa-file-powerpoint-o',
    xls: 'fa-file-excel-o',
    xlsx: 'fa-file-excel-o',
    jpg: 'fa-file-image-o',
    jpeg: 'fa-file-image-o',
    png: 'fa-file-image-o',
    mp4: 'fa-file-video-o',
    zip: 'fa-file-archive-o'
  }
  return iconMap[ext] || 'fa-file-o'
}

const getFileUrl = (filePath, isDownload = false) => {
  if (!filePath) return ''
  if (filePath.startsWith('http')) return filePath

  if (isDownload) {
    return `/api/method/frappe.utils.file_manager.download_file?file_url=${encodeURIComponent(filePath)}`
  }

  return filePath
}

/**
 * Open modal (without topic pre-selection)
 */
const openModal = () => {
  modalMode.value = 'create'
  materialToEdit.value = null
  preselectedTopicName.value = null
  modalOpen.value = true
}

/**
 * Open modal with specific topic pre-selected
 * This is called when clicking the "Add Material" button on a topic
 */
const openModalWithTopic = (topicName) => {
  modalMode.value = 'create'
  materialToEdit.value = null
  preselectedTopicName.value = topicName
  modalOpen.value = true
}

const editMaterial = (material) => {
  modalMode.value = 'edit'
  materialToEdit.value = material
  preselectedTopicName.value = material.topic || null
  modalOpen.value = true
}

/**
 * Close modal
 */
const closeModal = () => {
  modalOpen.value = false
  // Don't reset preselectedTopic immediately to allow modal to use it
  setTimeout(() => {
    preselectedTopicName.value = null
  }, 300)
}

/**
 * Handle successful material upload
 */
const onMaterialUploaded = async (materialData) => {
  // Show success message
  showSuccess.value = true
  setTimeout(() => {
    showSuccess.value = false
  }, 3000)

  // Refresh materials lists
  await Promise.all([
    fetchMaterials({ course: selectedCourse.value }),
    fetchMaterialsByTeacher()
  ])

  // Close edit context if any
  modalMode.value = 'create'
  materialToEdit.value = null
  preselectedTopicName.value = null
}

/**
 * Handle error
 */
const handleError = (message) => {
  errorMessage.value = message
  showError.value = true
  setTimeout(() => {
    showError.value = false
  }, 3000)
}

onMounted(() => {
  fetchMaterialsByTeacher()
  loadData()
})
</script>

<style scoped>
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Smooth animations */
.animate-in {
  animation-duration: 0.5s;
  animation-fill-mode: both;
}

.fade-in {
  animation-name: fadeIn;
}

.slide-in-from-bottom-4 {
  animation-name: slideInFromBottom;
}

.slide-in-from-right-4 {
  animation-name: slideInFromRight;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideInFromBottom {
  from {
    transform: translateY(1rem);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slideInFromRight {
  from {
    transform: translateX(1rem);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style>