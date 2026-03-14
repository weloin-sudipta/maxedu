<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-white p-4 lg:p-8 font-sans">
    <div class="max-w-[1440px] mx-auto space-y-8">
      
      <!-- Header with Role Selector -->
      <header class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 p-8">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-6">
          <div>
            <h1 class="text-3xl font-black tracking-tight text-slate-800">Library Tracking</h1>
            <p class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mt-1">
              Complete borrowing history & member insights
            </p>
          </div>
        </div>

        <!-- Role Tabs -->
        <div class="flex flex-wrap gap-2 p-2 bg-slate-100 rounded-2xl w-fit">
          <button 
            v-for="role in roles" 
            :key="role"
            @click="selectedRole = role"
            :class="[
              'px-6 py-2.5 rounded-xl text-[10px] font-black uppercase tracking-[0.2em] transition-all',
              selectedRole === role 
                ? 'bg-white text-indigo-600 shadow-sm' 
                : 'text-slate-500 hover:text-slate-700'
            ]"
          >
            <i :class="roleIcons[role]" class="mr-2"></i> {{ role }}
          </button>
        </div>
      </header>

      <!-- Role-Specific Content -->
      <component :is="viewComponent" :key="selectedRole" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import StudentTracking from './tracking/StudentTracking.vue';
import TeacherTracking from './tracking/TeacherTracking.vue';
import StaffTracking from './tracking/StaffTracking.vue';

const selectedRole = ref('Student');
const roles = ['Student', 'Teacher', 'Staff'];

const roleIcons = {
  'Student': 'fa fa-graduation-cap',
  'Teacher': 'fa fa-chalkboard-user',
  'Staff': 'fa fa-id-badge'
};

const viewComponent = computed(() => {
  switch(selectedRole.value) {
    case 'Student': return StudentTracking;
    case 'Teacher': return TeacherTracking;
    case 'Staff': return StaffTracking;
    default: return StudentTracking;
  }
});
</script>

<style scoped>
</style>
