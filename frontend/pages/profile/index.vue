<template>
    <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans text-slate-900">
        <div class="max-w-[1440px] mx-auto">

            <header class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 p-6 mb-6">
                <div class="flex flex-col md:flex-row items-center gap-8">
                    <div class="relative">
                        <div class="w-32 h-32 rounded-[2rem] overflow-hidden ring-4 ring-slate-50 shadow-lg">
                            <img src="https://demo.smart-school.in/uploads/student_images/1751522818-50232403968661e028c798!tha.jpeg"
                                alt="Student Photo" class="w-full h-full object-cover" />
                        </div>
                        <div
                            class="absolute -bottom-2 -right-2 bg-indigo-600 w-8 h-8 rounded-xl flex items-center justify-center text-white border-4 border-white shadow-md">
                            <i class="fa fa-graduation-cap text-[10px]"></i>
                        </div>
                    </div>

                    <div class="flex-1 text-center md:text-left">
                        <div class="flex flex-col md:flex-row md:items-center gap-3 mb-2">
                            <h1 class="text-3xl font-black tracking-tight text-slate-800">{{ profileData?.firstName || 'User' }} {{ profileData?.lastName || '' }}</h1>
                            <span
                                class="px-3 py-1 bg-green-50 text-green-600 text-[10px] font-black uppercase tracking-widest rounded-lg border border-green-100">
                                Active Session: {{ student.academic.Session }}
                            </span>
                        </div>

                        <div class="flex flex-wrap justify-center md:justify-start gap-6 mt-4">
                            <div class="flex flex-col">
                                <span class="label-tiny">Student ID</span>
                                <span class="value-bold text-indigo-600">#{{ student.admNo }}</span>
                            </div>
                            <div class="w-px h-8 bg-slate-100 hidden md:block"></div>
                            <div class="flex flex-col">
                                <span class="label-tiny">Roll Number</span>
                                <span class="value-bold">{{ student.rollNo }}</span>
                            </div>
                            <div class="w-px h-8 bg-slate-100 hidden md:block"></div>
                            <div class="flex flex-col">
                                <span class="label-tiny">Class & Section</span>
                                <span class="value-bold">{{ student.class }}</span>
                            </div>
                        </div>
                    </div>

                    <div class="flex gap-2">
                        <button class="btn-icon" title="Print Profile"><i class="fa fa-print"></i></button>
                        <button class="btn-primary">Edit Information</button>
                    </div>
                </div>

                <nav class="flex items-center gap-2 mt-8 border-t border-slate-50 pt-6 overflow-x-auto no-scrollbar">
                    <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id" :class="[
                        activeTab === tab.id
                            ? 'bg-slate-900 text-white shadow-xl shadow-slate-200'
                            : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900',
                        'px-6 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest transition-all whitespace-nowrap'
                    ]">
                        {{ tab.name }}
                    </button>
                </nav>
            </header>

            <main v-if="activeTab === 'profile'" class="space-y-6 animate-in fade-in duration-500">

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="lg:col-span-2 bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm">
                        <div class="flex items-center gap-3 mb-8">
                            <div class="w-1.5 h-6 bg-indigo-600 rounded-full"></div>
                            <h3 class="text-lg font-black text-slate-800 tracking-tight">Academic Profile</h3>
                        </div>
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-y-10 gap-x-6">
                            <div v-for="(val, label) in student.academic" :key="label">
                                <p class="label-tiny mb-1">{{ label }}</p>
                                <p class="text-sm font-bold text-slate-700">{{ val }}</p>
                            </div>
                        </div>
                    </div>

                    <div
                        class="bg-indigo-600 rounded-[2.5rem] p-8 text-white shadow-xl shadow-indigo-100 flex flex-col justify-between">
                        <div>
                            <p class="text-[10px] font-black uppercase tracking-[0.2em] opacity-60 mb-1">Attendance
                                Performance</p>
                            <h4 class="text-4xl font-black">94.2<span class="text-lg opacity-50">%</span></h4>
                        </div>
                        <div class="space-y-4">
                            <div class="flex justify-between items-center text-sm font-bold">
                                <span class="opacity-70 text-xs">Behavior Score</span>
                                <span>Excellent</span>
                            </div>
                            <div class="w-full bg-indigo-500 rounded-full h-1.5">
                                <div class="bg-white h-1.5 rounded-full" style="width: 94%"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div v-for="(section, title) in student.secondary" :key="title"
                        class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm">
                        <h3
                            class="text-xs font-black uppercase tracking-widest text-slate-400 mb-8 border-b border-slate-50 pb-4">
                            {{ title }}
                        </h3>
                        <div class="grid grid-cols-2 gap-y-8 gap-x-6">
                            <div v-for="(val, label) in section" :key="label">
                                <p class="label-tiny mb-1">{{ label }}</p>
                                <p class="text-sm font-bold text-slate-700">{{ val || '—' }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm">
                    <h3 class="text-xs font-black uppercase tracking-widest text-slate-400 mb-8">Logistics & Residential
                        Details</h3>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div v-for="(val, label) in student.logistics" :key="label"
                            class="p-6 bg-slate-50/50 rounded-2xl border border-slate-100">
                            <p class="label-tiny mb-2">{{ label }}</p>
                            <p class="text-xs font-bold text-slate-600 leading-relaxed">{{ val }}</p>
                        </div>
                    </div>
                </div>
            </main>

<!-- Dynamic Tab Component Render -->
<component
    v-else-if="tabComponents[activeTab]"
    :is="tabComponents[activeTab]"
    class="animate-in fade-in duration-500"
/>

<!-- Fallback UI -->
<div v-else class="bg-white rounded-[2.5rem] p-24 border border-dashed border-slate-200 text-center">
    <div class="w-20 h-20 bg-slate-50 rounded-3xl flex items-center justify-center mx-auto mb-6">
        <i class="fa fa-folder-open text-slate-200 text-3xl"></i>
    </div>
    <h2 class="text-xl font-black text-slate-800 uppercase tracking-tighter">
        Section Under Development
    </h2>
    <p class="text-sm text-slate-400 mt-2">
        The {{ activeTab }} module is being synced with the database.
    </p>
</div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import feesTab from './tabs/feesTab.vue'
import examTab from './tabs/examTab.vue'
import attendanceTab from './tabs/attendanceTab.vue'
import { useProfile } from '~/composable/useProfile'

// Reactive tab state
const activeTab = ref('profile')
const tabComponents = {
    fees: feesTab,
    exam: examTab,
    attendance: attendanceTab,
}

// Reactive student data (to replace static object)
const student = ref({
    name: '',
    admNo: '',
    rollNo: '',
    class: '',
    localId: '',
    academic: {},
    secondary: {},
    logistics: {},
})

// Fetch profile from backend
onMounted(async () => {
    const profile = await useProfile()
    
    if (profile && !profile.error) {
        // Map API response to the same structure your template expects
        student.value = {
            name: profile.student_name || `${profile.first_name || ''} ${profile.last_name || ''}`,
            admNo: profile.admNo || profile.student_id || '—',
            rollNo: profile.rollNo || profile.student_id?.split('-').pop() || '—',
            class: profile.program_name || '—',
            localId: profile.localId || '—',

            academic: {
                "Admission Date": profile.program_enrollment_date || '—',
                "Session": profile.program_session || '—',
                "Gender": profile.gender || '—',
                "Category": profile.category || '—',
                "Caste": profile.caste || '—',
                "Religion": profile.religion || '—',
                "Blood Group": profile.blood_group || '—',
                "Date of Birth": profile.date_of_birth || '—'
            },

            secondary: {
                "Parental Records": {
                    "Father": profile.guardians?.[0]?.guardian_name || '—',
                    "Mother": profile.mother_name || '—',
                    "Guardian": profile.guardians?.[0]?.guardian_name || '—',
                    "Guardian Relation": profile.guardians?.[0]?.relation || '—'
                },
                "Contact & Security": {
                    "Mobile": profile.mobile_number || '—',
                    "Email": profile.email || '—',
                    "Nationality": profile.nationality || '—',
                    "Parent Mobile": profile.parent_mobile_number || '—'
                }
            },

            logistics: {
                "Country": profile.country || '—',
                "State": profile.state || '—',
                "Pincode": profile.pincode || '—',
                "Hostel Facility": profile.hostel_facility || '—',
                "Current Address": profile.address_line_1 || '—',
                "Permanent Address": profile.address_line_2 || '—'
            }
        }
    }
})
</script>

<style scoped>
/* Utility Components */
.label-tiny {
    @apply text-[10px] font-black text-slate-400 uppercase tracking-widest;
}

.value-bold {
    @apply text-sm font-bold text-slate-700;
}

.btn-primary {
    @apply px-8 py-3 bg-indigo-600 text-white rounded-2xl text-[10px] font-black uppercase tracking-[0.2em] shadow-xl shadow-indigo-100 hover:bg-indigo-700 active:scale-95 transition-all;
}

.btn-icon {
    @apply w-12 h-12 flex items-center justify-center bg-white border border-slate-200 text-slate-400 rounded-2xl hover:text-indigo-600 hover:border-indigo-100 transition-all;
}

/* Hide scrollbars but allow scrolling */
.no-scrollbar::-webkit-scrollbar {
    display: none;
}

.no-scrollbar {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>