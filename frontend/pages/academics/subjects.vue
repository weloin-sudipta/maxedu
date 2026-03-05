<template>
    <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans text-slate-900">
        <div class="max-w-[1440px] mx-auto space-y-6">

            <HeroHeader title="Learning Path" subtitle="Strategic Overview & Mark Distribution" icon="fa fa-graduation-cap">
                <router-link to="/study-materials" class="btn-outline">
                    <i class="fa fa-folder-open mr-2"></i> Resource Library
                </router-link>
                <button class="btn-primary">
                    <i class="fa fa-calendar-o mr-2"></i> Exam Schedule
                </button>
            </HeroHeader>

            <div class="grid grid-cols-1 gap-8">
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
                                    <span>Syllabus Weight</span>
                                    <span>{{ subject.totalCredits }} Credits</span>
                                </div>
                                <div class="w-full bg-white/10 h-1.5 rounded-full overflow-hidden">
                                    <div class="bg-white h-full" :style="{ width: '100%' }"></div>
                                </div>
                            </div>
                        </div>

                        <div class="flex-1 p-8 lg:p-10">
                            <div class="flex items-center justify-between mb-8">
                                <h4 class="text-xs font-black text-slate-400 uppercase tracking-[0.3em]">Exam-Weightage Breakdown</h4>
                                <span class="text-[10px] font-bold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-lg italic">
                                    *Click chapter to view lessons
                                </span>
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
                                        
                                        <div class="flex items-center gap-2 mt-1">
                                            <span class="w-1 h-1 bg-slate-300 rounded-full"></span>
                                            <span class="text-[9px] font-bold text-slate-400 uppercase">{{ chapter.lessons.length }} Lessons Found</span>
                                        </div>
                                    </div>
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

                    <div class="flex-1 overflow-y-auto p-8 custom-scrollbar space-y-4">
                        <div v-for="(lesson, index) in selectedChapter.lessons" :key="index"
                             class="flex gap-5 p-5 bg-slate-50 border border-slate-100 rounded-2xl group/lesson hover:bg-white hover:border-indigo-200 transition-all">
                            
                            <div class="w-10 h-10 rounded-xl bg-white border border-slate-200 flex items-center justify-center font-black text-slate-400 group-hover/lesson:text-indigo-600 group-hover/lesson:border-indigo-100 transition-colors shrink-0">
                                {{ index + 1 }}
                            </div>

                            <div class="flex-1">
                                <h6 class="text-sm font-black text-slate-800 mb-1 group-hover/lesson:text-indigo-600 transition-colors">{{ lesson.name }}</h6>
                                <p class="text-[11px] text-slate-500 leading-relaxed">{{ lesson.description }}</p>
                                
                                <div class="mt-4 flex gap-3">
                                    <button class="px-4 py-2 bg-indigo-600 text-white rounded-lg text-[9px] font-black uppercase tracking-widest flex items-center gap-2">
                                        <i class="fa fa-play-circle"></i> Watch Video
                                    </button>
                                    <button class="px-4 py-2 bg-white border border-slate-200 text-slate-600 rounded-lg text-[9px] font-black uppercase tracking-widest flex items-center gap-2">
                                        <i class="fa fa-file-text-o"></i> Read Notes
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="p-6 bg-slate-50 border-t border-slate-100 text-center">
                        <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">
                            Estimated Completion Time: {{ selectedChapter.lessons.length * 45 }} Minutes
                        </p>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import HeroHeader from '~/components/ui/HeroHeader.vue'

const config = useRuntimeConfig()
useSeoMeta({
    title: `Subjects & Chapters - ${config.public.appName}`,
    description: `Explore your academic roadmap with MaxEdu's comprehensive breakdown of subjects, chapters, and lesson details. Strategically designed to guide your learning journey and maximize exam performance.`,
    keywords: 'subjects, chapters, lessons, learning path, academic roadmap, exam preparation'
})

const selectedSubject = ref(null);
const selectedChapter = ref(null);

const openLessons = (subject, chapter) => {
    selectedSubject.value = subject;
    selectedChapter.value = chapter;
}

const subjects = ref([
    {
        name: 'Advanced Mathematics',
        code: 'MATH-201',
        totalCredits: 4,
        icon: 'fa-calculator',
        bgColor: 'bg-indigo-600',
        chapters: [
            { 
                title: 'Algebraic Structures', 
                marks: 15, 
                weightColor: 'bg-indigo-500',
                lessons: [
                    { name: 'Groups and Subgroups', description: 'Understanding the fundamental properties of group theory and closure.' },
                    { name: 'Cyclic Groups', description: 'Exploration of generators and cyclic subgroup structures.' },
                    { name: 'Lagrange’s Theorem', description: 'Application of cosets and the order of subgroups.' }
                ]
            },
            { 
                title: 'Vector Calculus', 
                marks: 25, 
                weightColor: 'bg-rose-500',
                lessons: [
                    { name: 'Gradient & Divergence', description: 'Vector fields and the application of del operators.' },
                    { name: 'Line Integrals', description: 'Calculating work done and path independence in vector fields.' },
                    { name: 'Green’s Theorem', description: 'Relationship between line integrals and double integrals over a plane.' }
                ]
            }
        ]
    },
    {
        name: 'Quantum Physics',
        code: 'PHY-402',
        totalCredits: 3,
        icon: 'fa-bolt',
        bgColor: 'bg-slate-900',
        chapters: [
            { 
                title: 'Schrödinger Equation', 
                marks: 40, 
                weightColor: 'bg-rose-600',
                lessons: [
                    { name: 'Time-Independent Equation', description: 'Solving the wave function for stationary energy states.' },
                    { name: 'Infinite Square Well', description: 'Quantum particles in 1D potential traps and normalization.' },
                    { name: 'Harmonic Oscillator', description: 'Algebraic method and ladder operators in quantum mechanics.' }
                ]
            }
        ]
    }
]);
</script>

<style scoped>
.btn-primary { @apply px-8 py-3 bg-indigo-600 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest shadow-xl shadow-indigo-100 hover:bg-indigo-700 transition-all; }
.btn-outline { @apply px-6 py-3 bg-white border border-slate-200 text-slate-600 rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-50 transition-all; }

.custom-scrollbar::-webkit-scrollbar { width: 5px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }

@keyframes modalEntry {
    from { opacity: 0; transform: scale(0.9) translateY(30px); }
    to { opacity: 1; transform: scale(1) translateY(0); }
}
.animate-modal { animation: modalEntry 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
</style>