<template>
  <div class="space-y-6 animate-in fade-in duration-500">
    
    <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
      
      <div v-for="exam in examResults" :key="exam.id" 
           class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm transition-all hover:shadow-md">
        
        <div class="flex justify-between items-start mb-8">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="w-2 h-2 rounded-full bg-indigo-500"></span>
              <p class="text-[10px] font-black text-indigo-600 uppercase tracking-widest">{{ exam.session }}</p>
            </div>
            <h3 class="text-xl font-black text-slate-800">{{ exam.termName }}</h3>
          </div>
          <div class="bg-slate-900 text-white px-5 py-3 rounded-2xl flex flex-col items-center">
            <span class="text-[10px] font-black opacity-50 uppercase tracking-tighter">Grade</span>
            <span class="text-xl font-black">{{ exam.overallGrade }}</span>
          </div>
        </div>

        <div class="space-y-3">
          <div v-for="score in exam.subjects" :key="score.name" 
               class="flex justify-between items-center p-4 bg-slate-50 rounded-2xl group hover:bg-slate-100 transition-colors">
            <div class="flex flex-col">
              <span class="text-xs font-bold text-slate-700">{{ score.name }}</span>
              <span class="text-[10px] text-slate-400 font-medium italic">{{ score.note }}</span>
            </div>
            <div class="text-right">
              <span class="text-sm font-black text-slate-900">{{ score.marks }}</span>
              <span class="text-[10px] text-slate-400 font-bold ml-1">/ {{ score.maxMarks }}</span>
            </div>
          </div>
        </div>

        <div class="mt-8 pt-6 border-t border-slate-100">
          <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Teacher's Remarks</p>
          <p class="text-xs font-bold text-slate-600 leading-relaxed italic">"{{ exam.remarks }}"</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// DEMO DATA: Map your API response to this structure
const examResults = ref([
  {
    id: 1,
    termName: 'First Term Examination',
    session: '2025-26',
    overallGrade: 'A+',
    remarks: 'Excellent performance in all logical subjects. Needs slight focus on handwriting.',
    subjects: [
      { name: 'Mathematics', marks: 98, maxMarks: 100, note: 'Highest in class' },
      { name: 'English Language', marks: 85, maxMarks: 100, note: 'Good vocabulary' },
      { name: 'General Science', marks: 92, maxMarks: 100, note: 'Very attentive' }
    ]
  },
  {
    id: 2,
    termName: 'Mid-Term Evaluation',
    session: '2025-26',
    overallGrade: 'A',
    remarks: 'Consistent growth observed. Participation in class activities is very high.',
    subjects: [
      { name: 'Mathematics', marks: 95, maxMarks: 100, note: 'Consistent' },
      { name: 'History', marks: 88, maxMarks: 100, note: 'Well researched' },
      { name: 'Physical Education', marks: 100, maxMarks: 100, note: 'Outstanding' }
    ]
  }
]);
</script>