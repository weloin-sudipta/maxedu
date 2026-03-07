<template>
    <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans text-slate-900">
        <div class="max-w-[1440px] mx-auto space-y-6">

            <HeroHeader title="Learning Path" subtitle="Strategic Overview & Mark Distribution" icon="fa fa-graduation-cap">
                <router-link to="/academics/study-materials" class="btn-outline">
                    <i class="fa fa-folder-open mr-2"></i> Resource Library
                </router-link>
            </HeroHeader>

            <div v-if="loading" class="text-center py-20">
                <i class="fa fa-spinner fa-spin text-indigo-400 text-3xl"></i>
                <p class="text-xs text-slate-400 mt-3 font-bold uppercase">Loading subjects...</p>
            </div>

            <div v-else-if="subjects.length === 0" class="bg-white rounded-[2.5rem] p-20 border border-dashed border-slate-200 text-center">
                <i class="fa fa-book text-slate-100 text-6xl mb-4"></i>
                <p class="text-sm font-black text-slate-400 uppercase tracking-widest">No courses enrolled yet.</p>
            </div>

            <div class="grid grid-cols-1 gap-8" v-else>
                <div v-for="subject in subjects" :key="subject.code"
                    class="bg-white rounded-[2.5rem] border border-slate-200/60 shadow-sm overflow-hidden group transition-all hover:shadow-xl hover:shadow-slate-200/50">

                    <div class="flex flex-col lg:flex-row">
                        <div :class="['lg:w-80 p-10 flex flex-col justify-between items-center text-center border-b lg:border-b-0 lg:border-r border-slate-50 relative', subject.bgColor]">
                            <div class="absolute top-0 right-0 p-4 opacity-10">
                                <i :class="['fa text-8xl text-white', subject.icon]"></i>
                            </div>

                            <div class="relative z-10">
                                <div class="w-20 h-20 bg-white/20 rounded-[2rem] flex items-center justify-center text-3xl text-white mx-auto mb-6 backdrop-blur-xl border border-white/30 shadow-2xl">
                                    <i :class="['fa', subject.icon]"></i>
                                </div>
                                <h3 class="text-2xl font-black text-white tracking-tight leading-tight">{{ subject.name }}</h3>
                                <div class="mt-2 inline-block px-4 py-1 bg-black/20 rounded-full">
                                    <p class="text-white/80 text-[10px] font-black uppercase tracking-[0.2em]">{{ subject.code }}</p>
                                </div>
                            </div>

                            <div class="w-full mt-10 space-y-2 relative z-10">
                                <div class="flex justify-between text-[10px] font-black text-white/60 uppercase">
                                    <span>Topics</span>
                                    <span>{{ subject.totalCredits }} Chapters</span>
                                </div>
                                <div class="w-full bg-white/10 h-1.5 rounded-full overflow-hidden">
                                    <div class="bg-white h-full" :style="{ width: '100%' }"></div>
                                </div>
                            </div>
                        </div>

                        <div class="flex-1 p-8 lg:p-10">
                            <div class="flex items-center justify-between mb-8">
                                <h4 class="text-xs font-black text-slate-400 uppercase tracking-[0.3em]">Exam-Weightage Breakdown</h4>
                            </div>

                            <div class="flex flex-wrap gap-4">
                                <div
                                    v-for="(chapter, i) in subject.chapters"
                                    :key="i"
                                    @click="openLessons(subject, chapter)"
                                    class="group/item cursor-pointer relative flex items-center gap-4 bg-slate-50 border border-slate-100 p-4 pr-6 rounded-[1.5rem] hover:bg-white hover:border-indigo-400 hover:shadow-lg transition-all duration-300 active:scale-95"
                                >
                                    <div :class="['w-12 h-12 rounded-2xl flex flex-col items-center justify-center shadow-sm transition-transform group-hover/item:rotate-12', chapter.weightColor]">
                                        <span class="text-xs font-black text-white">{{ chapter.marks }}%</span>
                                        <span class="text-[7px] font-bold text-white/80 uppercase">Marks</span>
                                    </div>

                                    <div>
                                        <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-0.5">Chapter {{ i + 1 }}</p>
                                        <h5 class="text-sm font-black text-slate-700 group-hover/item:text-indigo-600 transition-colors">{{ chapter.title }}</h5>
                                    </div>
                                </div>

                                <div v-if="subject.chapters.length === 0" class="text-xs text-slate-400 italic p-4">
                                    No topics assigned yet
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="selectedChapter" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
                <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm" @click="selectedChapter = null"></div>

                <div class="relative bg-white w-full max-w-2xl rounded-[2.5rem] shadow-2xl flex flex-col max-h-[85vh] overflow-hidden animate-modal">
                    <div :class="['p-8 text-white relative overflow-hidden', selectedSubject.bgColor]">
                        <div class="relative z-10 flex justify-between items-start">
                            <div>
                                <p class="text-[10px] font-black uppercase tracking-[0.2em] opacity-70 mb-1">{{ selectedSubject.name }}</p>
                                <h3 class="text-2xl font-black tracking-tight">{{ selectedChapter.title }}</h3>
                            </div>
                            <button @click="selectedChapter = null" class="w-10 h-10 bg-white/20 hover:bg-white/40 rounded-xl flex items-center justify-center transition-colors">
                                <i class="fa fa-times"></i>
                            </button>
                        </div>
                        <i :class="['fa absolute -right-4 -bottom-4 text-9xl opacity-10', selectedSubject.icon]"></i>
                    </div>

                    <div class="p-8 text-center text-slate-400">
                        <p class="text-xs font-bold uppercase">Topic details coming soon</p>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import HeroHeader from '~/components/ui/HeroHeader.vue'
import { createResource } from '~/composable/useFrappeFetch'

const config = useRuntimeConfig()

useSeoMeta({
  title: config.public.appName + ' | Academics - Subjects',
})

const resource = createResource({
  url: 'maxedu.api_folder.subjects.get_program'
})

const loading = ref(true)

onMounted(async () => {
  await resource.submit()
  loading.value = false
})

const selectedSubject = ref(null)
const selectedChapter = ref(null)

const openLessons = (subject, chapter) => {
  selectedSubject.value = subject
  selectedChapter.value = chapter
}

const subjectStyles = [
  { icon: 'fa-calculator', bgColor: 'bg-indigo-600' },
  { icon: 'fa-bolt', bgColor: 'bg-amber-600' },
  { icon: 'fa-flask', bgColor: 'bg-emerald-600' },
  { icon: 'fa-leaf', bgColor: 'bg-green-600' },
  { icon: 'fa-pencil', bgColor: 'bg-rose-600' },
  { icon: 'fa-university', bgColor: 'bg-slate-700' },
  { icon: 'fa-laptop', bgColor: 'bg-cyan-600' },
  { icon: 'fa-globe', bgColor: 'bg-purple-600' },
  { icon: 'fa-music', bgColor: 'bg-pink-600' },
  { icon: 'fa-paint-brush', bgColor: 'bg-orange-600' },
]

const chapterColors = [
  'bg-indigo-500', 'bg-rose-500', 'bg-emerald-500', 'bg-amber-500',
  'bg-cyan-500', 'bg-purple-500', 'bg-pink-500', 'bg-slate-500',
]

const getSubjectIcon = (name) => {
  if (!name) return 'fa-book'
  const n = name.toLowerCase()
  if (n.includes('math')) return 'fa-calculator'
  if (n.includes('physic')) return 'fa-bolt'
  if (n.includes('chem')) return 'fa-flask'
  if (n.includes('bio')) return 'fa-leaf'
  if (n.includes('english') || n.includes('liter')) return 'fa-pencil'
  if (n.includes('history')) return 'fa-university'
  if (n.includes('computer') || n.includes('science')) return 'fa-laptop'
  return 'fa-book'
}

const subjects = computed(() => {
  const data = resource.data.value
  if (!data || !data.courses) return []

  return data.courses.map((course, idx) => {
    const style = subjectStyles[idx % subjectStyles.length]
    const topicCount = course.topics?.length || 0
    const marksPerTopic = topicCount > 0 ? Math.round(100 / topicCount) : 0

    return {
      name: course.course_name,
      code: course.course_id,
      totalCredits: topicCount,
      icon: getSubjectIcon(course.course_name),
      bgColor: style.bgColor,
      chapters: (course.topics || []).map((topic, i) => ({
        title: topic.topic_name,
        marks: marksPerTopic,
        weightColor: chapterColors[i % chapterColors.length],
      }))
    }
  })
})
</script>

<style scoped>
.btn-primary { @apply px-8 py-3 bg-indigo-600 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest shadow-xl shadow-indigo-100 hover:bg-indigo-700 transition-all; }
.btn-outline { @apply px-6 py-3 bg-white border border-slate-200 text-slate-600 rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-50 transition-all; }

@keyframes modalEntry {
    from { opacity: 0; transform: scale(0.9) translateY(30px); }
    to { opacity: 1; transform: scale(1) translateY(0); }
}
.animate-modal { animation: modalEntry 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
</style>
