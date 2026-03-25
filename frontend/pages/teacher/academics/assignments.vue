<template>
  <div class="p-6 lg:p-10 max-w-7xl mx-auto space-y-8 animate-in fade-in duration-700">
    
    <!-- Hero Header aligned with other pages -->
    <HeroHeader 
      title="Assignment Hub" 
      subtitle="Academic Content Management & Grading" 
      icon="fa fa-layer-group"
    >
      <div class="flex flex-wrap items-center gap-4">
        <div class="relative">
          <i class="fa fa-filter absolute left-4 top-1/2 -translate-y-1/2 text-indigo-500 text-xs text-opacity-70"></i>
          <select v-model="selectedGroup" class="pl-10 pr-8 py-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-[10px] font-black uppercase tracking-widest focus:ring-2 focus:ring-indigo-500 appearance-none shadow-sm dark:shadow-none outline-none cursor-pointer h-10 transition-all hover:bg-white dark:hover:bg-slate-700">
            <option value="All">All Student Groups</option>
            <option v-for="group in studentGroups" :key="group" :value="group">{{ group }}</option>
          </select>
        </div>

        <button @click="showCreateModal = true" class="group bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2.5 rounded-xl text-[10px] font-black uppercase tracking-[0.15em] hover:scale-105 active:scale-95 transition-all flex items-center gap-3 shadow-lg shadow-indigo-200 dark:shadow-none h-10">
          <i class="fa fa-plus group-hover:rotate-90 transition-transform"></i> New Material
        </button>
      </div>
    </HeroHeader>

    <!-- Skeleton Loading matching Student Directory -->
    <div v-if="loading" class="grid grid-cols-1 gap-8">
      <UiSkeleton v-for="i in 2" :key="i" height="h-80" class="rounded-[3.5rem]" />
    </div>

    <div v-else class="grid grid-cols-1 gap-10">
      <div v-for="task in filteredAssignments" :key="task.id" 
        class="relative bg-white dark:bg-slate-900 rounded-[3.5rem] border border-slate-100 dark:border-slate-800 p-2 shadow-sm hover:shadow-xl transition-all duration-500">
        
        <div class="p-8 lg:p-12">
          <div class="flex flex-col xl:flex-row justify-between gap-10">
            <div class="flex-1 space-y-6">
              <div class="flex flex-wrap items-center gap-4">
                <span class="px-4 py-1.5 bg-indigo-50 dark:bg-indigo-900/40 text-indigo-600 dark:text-indigo-400 rounded-full text-[10px] font-black uppercase tracking-tighter border border-indigo-100 dark:border-indigo-800/50">
                  {{ task.group }}
                </span>
                <span class="text-slate-400 text-[10px] font-bold uppercase tracking-widest flex items-center gap-1.5">
                  <i class="fa fa-calendar-check-o text-indigo-400"></i> Due: {{ task.dueDate }}
                </span>
              </div>
              
              <div>
                <h2 class="text-3xl font-black text-slate-800 dark:text-white mb-4 tracking-tight leading-tight">{{ task.title }}</h2>
                <p class="text-slate-500 text-sm leading-relaxed max-w-3xl font-medium">{{ task.description }}</p>
              </div>
              
              <div class="pt-4">
                 <button @click="viewDocument(task.teacherFileUrl)" class="flex items-center gap-3 px-5 py-3 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl hover:bg-white dark:hover:bg-slate-700 hover:border-indigo-200 dark:hover:border-indigo-800 shadow-sm hover:shadow-md transition-all group/btn">
                    <div class="w-8 h-8 bg-rose-50 dark:bg-rose-900/30 rounded-lg flex items-center justify-center text-rose-500 group-hover/btn:scale-110 transition-transform">
                      <i class="fa fa-file-pdf-o"></i>
                    </div>
                    <span class="text-[10px] font-black uppercase text-slate-600 dark:text-slate-300 tracking-widest">Master Reference Document</span>
                 </button>
              </div>
            </div>

            <!-- Stats Card (Responsive) -->
            <div class="xl:w-80 bg-slate-50 dark:bg-slate-800/40 rounded-[2.5rem] p-10 flex flex-col justify-center items-center text-center border border-white dark:border-slate-700/50 shadow-inner">
               <div class="relative w-24 h-24 mb-6">
                 <svg class="w-full h-full transform -rotate-90">
                   <circle cx="48" cy="48" r="40" stroke="currentColor" stroke-width="8" fill="transparent" class="text-slate-200 dark:text-slate-700" />
                   <circle cx="48" cy="48" r="40" stroke="currentColor" stroke-width="8" fill="transparent" 
                     class="text-indigo-500 transition-all duration-1000" 
                     :stroke-dasharray="2 * Math.PI * 40" 
                     :stroke-dashoffset="2 * Math.PI * 40 * (1 - 0.75)" />
                 </svg>
                 <div class="absolute inset-0 flex items-center justify-center">
                   <span class="text-3xl font-black text-indigo-600 dark:text-indigo-400">{{ task.submissions.length }}</span>
                 </div>
               </div>
               <p class="text-[10px] font-black uppercase tracking-[0.2em] text-slate-400">Student Submissions</p>
            </div>
          </div>

          <!-- Table with horizontal scroll on mobile -->
          <div class="mt-12 overflow-x-auto custom-scrollbar -mx-2 px-2">
            <table class="w-full border-separate border-spacing-y-4 min-w-[700px]">
              <thead>
                <tr class="text-[10px] font-black uppercase tracking-widest text-slate-400">
                  <th class="text-left px-8 py-2">Student</th>
                  <th class="text-left px-8 py-2">Submission</th>
                  <th class="text-left px-8 py-2">Status</th>
                  <th class="text-right px-8 py-2">Grade Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="sub in task.submissions" :key="sub.id" class="bg-slate-50/50 dark:bg-slate-800/30 group/row hover:bg-white dark:hover:bg-slate-800 border border-transparent hover:border-indigo-100 dark:hover:border-indigo-900/50 transition-all rounded-[2rem] shadow-sm hover:shadow-lg">
                  <td class="px-8 py-5 rounded-l-[2rem]">
                    <div class="flex items-center gap-4">
                      <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-slate-200 to-slate-300 dark:from-slate-700 dark:to-slate-600 flex items-center justify-center font-black text-xs text-slate-700 dark:text-slate-200 shadow-inner overflow-hidden">
                        <img v-if="sub.avatar" :src="sub.avatar" class="w-full h-full object-cover" />
                        <span v-else>{{ sub.studentName.charAt(0) }}</span>
                      </div>
                      <span class="text-xs font-black text-slate-700 dark:text-slate-200">{{ sub.studentName }}</span>
                    </div>
                  </td>
                  <td class="px-8 py-5">
                    <button @click="viewDocument(sub.fileUrl)" class="flex items-center gap-2 text-indigo-500 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 transition-colors group/link">
                      <i class="fa fa-file-text-o group-hover/link:translate-y-[-1px]"></i>
                      <span class="text-[10px] font-bold tracking-wide border-b border-indigo-500/0 hover:border-indigo-500 transition-all">{{ sub.fileName }}</span>
                    </button>
                  </td>
                  <td class="px-8 py-5">
                    <span v-if="sub.grade" class="inline-flex items-center px-4 py-1.5 bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 rounded-xl text-[10px] font-black uppercase gap-2">
                      <i class="fa fa-check-circle"></i> Graded: {{ sub.grade }}
                    </span>
                    <span v-else class="inline-flex items-center px-4 py-1.5 bg-rose-100 dark:bg-rose-900/30 text-rose-600 dark:text-rose-400 rounded-xl text-[10px] font-black uppercase gap-2">
                      <i class="fa fa-clock-o"></i> Pending Review
                    </span>
                  </td>
                  <td class="px-8 py-5 rounded-r-[2rem] text-right">
                    <button @click="openGradingModal(sub)" class="bg-slate-900 dark:bg-indigo-600 text-white px-6 py-2.5 rounded-xl text-[10px] font-black uppercase tracking-widest hover:scale-105 active:scale-95 transition-all shadow-md active:shadow-inner">
                      Grade Work
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal 1: Create Assignment -->
    <AppModal v-model="showCreateModal" title="Create New Material" maxWidth="max-w-2xl">
      <div class="space-y-8">
        <div>
          <label class="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 mb-3">Material Title</label>
          <input v-model="newAssignment.title" type="text" class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-2xl px-6 py-4 text-sm font-bold text-slate-800 dark:text-white focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 transition-all outline-none" placeholder="e.g. Advanced AI Project" />
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <label class="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 mb-3">Target Group</label>
            <select v-model="newAssignment.group" class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-2xl px-6 py-4 text-sm font-bold text-slate-800 dark:text-white focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 appearance-none outline-none">
              <option value="" disabled>Select Group</option>
              <option v-for="group in studentGroups" :key="group" :value="group">{{ group }}</option>
            </select>
          </div>
          <div>
            <label class="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 mb-3">Submission Deadline</label>
            <input v-model="newAssignment.dueDate" type="date" class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-2xl px-6 py-4 text-sm font-bold text-slate-800 dark:text-white focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 outline-none" />
          </div>
        </div>
        <div>
          <label class="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 mb-3">Detailed Instructions</label>
          <textarea v-model="newAssignment.description" rows="5" class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-2xl px-6 py-4 text-sm font-medium text-slate-800 dark:text-white focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 transition-all outline-none resize-none" placeholder="Explain the assignment goals..."></textarea>
        </div>
        <div>
          <label class="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 mb-3">Master Assignment Document (PDF)</label>
          <div class="relative w-full border-2 border-dashed border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50 rounded-3xl p-10 flex flex-col items-center justify-center hover:border-indigo-500 dark:hover:border-indigo-500 transition-all cursor-pointer group/upload shadow-inner">
             <div class="w-16 h-16 bg-white dark:bg-slate-700 rounded-2xl shadow-sm flex items-center justify-center text-indigo-500 mb-4 group-hover/upload:scale-110 transition-transform">
               <i class="fa fa-cloud-upload text-2xl"></i>
             </div>
             <p class="text-xs font-black text-slate-500 uppercase tracking-widest mb-1">Click to Upload</p>
             <p class="text-[10px] font-bold text-slate-400 tracking-wide">PDF, máximo 10MB</p>
             <input type="file" class="absolute inset-0 opacity-0 cursor-pointer" accept=".pdf" />
          </div>
        </div>
      </div>
      <template #footer>
        <button @click="showCreateModal = false" class="px-8 py-3.5 rounded-xl text-[10px] font-black uppercase tracking-widest text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all">Discard</button>
        <button @click="createAssignment" class="px-8 py-3.5 rounded-xl bg-indigo-600 text-white text-[10px] font-black uppercase tracking-widest shadow-xl shadow-indigo-100 dark:shadow-none hover:bg-indigo-700 active:scale-95 transition-all">Publish Material</button>
      </template>
    </AppModal>

    <!-- Modal 2: Document Viewer Modal (Responsive) -->
    <AppModal v-model="isDocViewerOpen" title="Material Preview" maxWidth="max-w-6xl">
      <div class="h-[75vh] w-full bg-slate-50 dark:bg-slate-950 rounded-2xl overflow-hidden shadow-inner border border-slate-100 dark:border-slate-800">
         <iframe v-if="activeDoc" :src="activeDoc" class="w-full h-full border-none" title="PDF Preview"></iframe>
      </div>
    </AppModal>

    <!-- Modal 3: Grading Modal (Compact) -->
    <AppModal v-model="showGradeModal" title="Assessment Review" maxWidth="max-w-md">
      <div class="space-y-8" v-if="gradingSubmission">
        <div class="flex items-center gap-5 bg-white dark:bg-slate-800 p-6 rounded-[2rem] border border-slate-100 dark:border-slate-700 shadow-sm">
          <div class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-indigo-500 to-indigo-700 flex items-center justify-center font-black text-2xl text-white shadow-lg overflow-hidden">
            <img v-if="gradingSubmission.avatar" :src="gradingSubmission.avatar" class="w-full h-full object-cover" />
            <span v-else>{{ gradingSubmission.studentName.charAt(0) }}</span>
          </div>
          <div class="flex-1 min-w-0">
            <h4 class="font-black text-slate-800 dark:text-white text-base truncate">{{ gradingSubmission.studentName }}</h4>
            <p class="text-[10px] text-indigo-500 font-bold uppercase tracking-[0.15em] truncate">{{ gradingSubmission.fileName }}</p>
          </div>
          <button @click="viewDocument(gradingSubmission.fileUrl)" title="View Full Submission" class="w-12 h-12 bg-slate-50 dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-2xl flex items-center justify-center text-slate-600 dark:text-slate-300 hover:bg-indigo-600 hover:text-white hover:border-indigo-600 shadow-sm transition-all flex-shrink-0">
            <i class="fa fa-expand"></i>
          </button>
        </div>
        
        <div class="text-center pt-2">
          <label class="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 mb-4">Awarded Grade (0-100)</label>
          <input v-model="gradeInput" type="number" min="0" max="100" class="w-full bg-slate-50 dark:bg-slate-800/50 border-none rounded-[2rem] px-8 py-8 text-6xl font-black text-indigo-600 dark:text-indigo-400 focus:ring-2 focus:ring-indigo-500 outline-none text-center shadow-inner transition-all placeholder-slate-200" placeholder="0" />
        </div>

        <div>
          <label class="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 mb-3 ml-2">Internal Feedback</label>
          <textarea v-model="feedbackInput" rows="4" class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-[1.5rem] px-6 py-5 text-sm font-medium text-slate-800 dark:text-white focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 outline-none resize-none transition-all shadow-sm" placeholder="Great work on self-attention mechanisms..."></textarea>
        </div>
      </div>
      <template #footer>
        <button @click="showGradeModal = false" class="px-8 py-3.5 rounded-xl text-[10px] font-black uppercase tracking-widest text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all">Cancel</button>
        <button @click="saveGrade" class="px-8 py-3.5 rounded-xl bg-slate-900 dark:bg-white text-white dark:text-slate-900 text-[10px] font-black uppercase tracking-widest shadow-xl hover:scale-105 active:scale-95 transition-all flex items-center gap-2">
          <i class="fa fa-check-circle"></i> Complete Grading
        </button>
      </template>
    </AppModal>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppModal from '~/components/ui/AppModal.vue'
import HeroHeader from '~/components/ui/HeroHeader.vue'
import UiSkeleton from '~/components/ui/UiSkeleton.vue'

const loading = ref(true)
const selectedGroup = ref('All')
const studentGroups = ['B.Tech-CS-A', 'B.Tech-CS-B', 'M.Tech-AI']

// Modals State
const showCreateModal = ref(false)
const isDocViewerOpen = ref(false)
const activeDoc = ref(null)

const showGradeModal = ref(false)
const gradingSubmission = ref(null)
const gradeInput = ref('')
const feedbackInput = ref('')

const newAssignment = ref({ title: '', group: '', dueDate: '', description: '' })

// Mock Data
const assignments = ref([
  {
    id: 1,
    title: 'Advanced Neural Networks Project',
    group: 'M.Tech-AI',
    dueDate: '20 Oct, 2026',
    description: 'Implement a Transformer architecture from scratch using PyTorch. Focus on self-attention mechanisms and multi-head attention blocks.',
    teacherFileUrl: 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
    submissions: [
      { id: 101, studentName: 'Sudipta Ghosh', avatar: 'https://ui-avatars.com/api/?name=Sudipta+Ghosh&background=random', fileName: 'transformer_v1.pdf', fileUrl: 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf', grade: 98 },
      { id: 102, studentName: 'Rahul Verma', avatar: 'https://ui-avatars.com/api/?name=Rahul+Verma&background=random', fileName: 'assignment_final.pdf', fileUrl: 'https://www.africau.edu/images/default/sample.pdf', grade: null }
    ]
  }
])

const filteredAssignments = computed(() => {
  if (selectedGroup.value === 'All') return assignments.value
  return assignments.value.filter(a => a.group === selectedGroup.value)
})

// Handlers
const viewDocument = (url) => {
  activeDoc.value = url
  isDocViewerOpen.value = true
}

const openGradingModal = (sub) => {
  gradingSubmission.value = sub
  gradeInput.value = sub.grade || ''
  feedbackInput.value = ''
  showGradeModal.value = true
}

const saveGrade = () => {
  if (gradingSubmission.value) {
    gradingSubmission.value.grade = gradeInput.value
  }
  showGradeModal.value = false
}

const createAssignment = () => {
  if (!newAssignment.value.title || !newAssignment.value.group) {
    return
  }
  assignments.value.unshift({
    id: Date.now(),
    title: newAssignment.value.title,
    group: newAssignment.value.group,
    dueDate: newAssignment.value.dueDate || 'No Date',
    description: newAssignment.value.description,
    teacherFileUrl: 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
    submissions: []
  })
  showCreateModal.value = false
  newAssignment.value = { title: '', group: '', dueDate: '', description: '' }
}

onMounted(() => {
  setTimeout(() => loading.value = false, 800)
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 5px; height: 5px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 99px; }
.dark .custom-scrollbar::-webkit-scrollbar-thumb { background: #334155; }
</style>