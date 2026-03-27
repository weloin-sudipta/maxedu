<template>
  <div class="p-6 lg:p-10 max-w-7xl mx-auto custom-scrollbar animate-in fade-in slide-in-from-bottom-4 duration-500">

    <HeroHeader title="Lesson Planning" subtitle="Curriculum Tracking" icon="fa fa-map-signs">
      <div class="flex gap-2">

        <!-- Dynamic Course Dropdown -->
        <select
          v-model="selectedCourse"
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

        <button class="bg-indigo-600 dark:bg-indigo-500 text-white px-6 py-2 rounded-xl text-xs font-black uppercase tracking-widest hover:bg-indigo-700 dark:hover:bg-indigo-600 transition-colors shadow-lg shadow-indigo-200 dark:shadow-none flex items-center gap-2">
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
              <div class="flex-1 bg-slate-50 dark:bg-slate-800/50 p-6 rounded-2xl border border-slate-100 dark:border-slate-700/50 group-hover:border-indigo-200 dark:group-hover:border-indigo-500/30 transition-all cursor-pointer">

                <div class="flex justify-between items-start mb-2">
                  <div>
                    <span class="text-[10px] font-black uppercase tracking-widest text-indigo-500 mb-1 block">
                      Topic {{ i + 1 }}
                    </span>

                    <h4 class="text-sm font-black text-slate-800 dark:text-slate-200">
                      {{ topic.topic_name }}
                    </h4>
                  </div>
                </div>

                <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed max-w-lg mb-4">
                  {{ topic.topic }}
                </p>

                <div class="flex gap-2">
                  <button class="flex items-center gap-2 text-[10px] font-bold text-slate-600 dark:text-slate-300 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 px-3 py-1.5 rounded-lg hover:text-indigo-600 hover:border-indigo-200 transition-colors shadow-sm">
                    <i class="fa fa-file-pdf-o text-red-400"></i> Reference.pdf
                  </button>

                  <button class="flex items-center gap-2 text-[10px] font-bold text-slate-400 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 border-dashed px-3 py-1.5 rounded-lg hover:text-indigo-600 hover:border-indigo-200 transition-colors">
                    <i class="fa fa-plus"></i> Add Material
                  </button>
                </div>

              </div>
            </div>

          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import HeroHeader from '~/components/ui/HeroHeader.vue'
import { useCourseTopics } from '~/composable/useCourseTopics'

const { fetchCourseTopics } = useCourseTopics()

const loading = ref(true)
const courses = ref([])
const selectedCourse = ref(null)

/**
 * Fetch data
 */
const loadData = async () => {
  const res = await fetchCourseTopics()
  courses.value = res || []

  if (courses.value.length > 0) {
    selectedCourse.value = courses.value[0].name
  }

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

onMounted(() => {
  loadData()
})
</script>