<template>
    <div class="min-h-screen bg-[#F8FAFC] p-4 lg:p-10 font-sans text-slate-900">
        <div class="max-w-[1440px] mx-auto space-y-8">

            <HeroHeader title="Faculty & Mentors" subtitle="University Academic Staff Directory" icon="fa fa-users" />

            <div class="animate-in">
                <div
                    class="bg-white rounded-[2.5rem] p-4 border border-slate-200/60 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
                    <div class="flex items-center gap-4 ml-2">
                        <div
                            class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center text-xl">
                            <i class="fa fa-search"></i>
                        </div>
                        <div>
                            <h2 class="text-xl font-black text-slate-800 tracking-tight">Staff Search</h2>
                            <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Find by name,
                                role or expertise</p>
                        </div>
                    </div>

                    <div class="relative w-full md:w-96">
                        <input v-model="searchQuery" type="text" placeholder="Start typing to filter..."
                            class="w-full bg-slate-50 border border-slate-100 rounded-2xl py-3.5 px-6 text-xs font-bold text-slate-700 outline-none focus:bg-white focus:ring-4 focus:ring-indigo-500/5 focus:border-indigo-200 transition-all" />
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 animate-in">
                <div v-for="(member, index) in facultyMembers" :key="member.id"
                    class="bg-white rounded-[2.2rem] p-4 border border-slate-100 shadow-sm hover:shadow-xl hover:border-indigo-100/50 transition-all duration-500 group relative overflow-hidden flex flex-col justify-between">
                    <div
                        class="absolute -right-6 -top-6 w-20 h-20 bg-slate-50 rounded-full group-hover:bg-indigo-50/50 transition-colors duration-500">
                    </div>

                    <div class="relative z-10">
                        <div class="flex justify-between items-center mb-4">
                            <div class="relative">
                                <img :src="member.image"
                                    class="h-14 w-14 rounded-2xl object-cover border-2 border-white shadow-sm group-hover:scale-105 transition-transform duration-500" />
                                <div
                                    class="absolute -bottom-0.5 -right-0.5 h-3.5 w-3.5 bg-green-500 border-2 border-white rounded-full shadow-sm">
                                </div>
                            </div>

                            <span :class="[
                                'px-2.5 py-1 rounded-lg text-[7px] font-black uppercase tracking-widest border shadow-sm transition-colors',
                                roleTheme(member.role)
                            ]">
                                {{ member.role }}
                            </span>
                        </div>

                        <div class="space-y-1">
                            <h3
                                class="text-sm font-black text-slate-900 group-hover:text-indigo-600 transition-colors leading-tight">
                                {{ member.name }}
                            </h3>
                            <p
                                class="text-[9px] text-slate-400 font-black uppercase tracking-widest flex items-center gap-2">
                                <span class="w-2 h-[1px] bg-indigo-300"></span>
                                {{ member.designation }}
                            </p>
                        </div>

                        <div class="mt-3 mb-4">
                            <a :href="`mailto:${member.email}`" class="flex items-center gap-2 group/link max-w-fit">
                                <div
                                    class="w-6 h-6 rounded-lg bg-slate-50 flex items-center justify-center group-hover/link:bg-indigo-50 transition-colors">
                                    <i
                                        class="fa fa-envelope-o text-[9px] text-slate-400 group-hover/link:text-indigo-500"></i>
                                </div>
                                <span class="text-[10px] font-bold text-slate-500 lowercase truncate max-w-[150px]">{{
                                    member.email }}</span>
                            </a>
                        </div>
                    </div>

                    <div class="pt-3 border-t border-slate-50">
                        <div v-if="member.subjects.length" class="flex flex-wrap gap-1">
                            <span v-for="sub in member.subjects.slice(0, 2)" :key="sub"
                                class="px-2 py-0.5 text-[8px] font-black text-slate-500 bg-slate-50 border border-slate-100 rounded-md group-hover:bg-white transition-colors">
                                {{ sub }}
                            </span>
                            <span v-if="member.subjects.length > 2" class="text-[8px] font-black text-slate-300 ml-1">
                                +{{ member.subjects.length - 2 }}
                            </span>
                        </div>

                        <div v-else class="flex items-center gap-1.5 opacity-60">
                            <div class="w-1 h-1 bg-slate-300 rounded-full"></div>
                            <span
                                class="text-[8px] font-black text-slate-400 uppercase tracking-widest">Administration</span>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
import HeroHeader from "~/components/ui/HeroHeader.vue";

const searchQuery = ref("");

const roleTheme = (role) => {
    const themes = {
        HOD: "bg-indigo-50 text-indigo-600 border-indigo-100",
        Teacher: "bg-cyan-50 text-cyan-600 border-cyan-100",
        Librarian: "bg-amber-50 text-amber-600 border-amber-100",
        Staff: "bg-slate-100 text-slate-500 border-slate-200",
    };
    return themes[role] || themes["Staff"];
};

const facultyMembers = ref([
    { id: 1, name: "Dr. Arjun Sharma", role: "HOD", designation: "Department of CS", email: "arjun.s@university.edu", image: "https://i.pravatar.cc/150?u=1", subjects: ["Operating Systems", "Cyber Security"] },
    { id: 2, name: "Ms. Priya Verma", role: "Teacher", designation: "Senior Professor", email: "priya.v@university.edu", image: "https://i.pravatar.cc/150?u=2", subjects: ["Data Science", "Python"] },
    { id: 3, name: "Mr. David Wilson", role: "Librarian", designation: "Chief Librarian", email: "david.lib@university.edu", image: "https://i.pravatar.cc/150?u=3", subjects: [] },
    { id: 4, name: "Dr. Sarah Connor", role: "Teacher", designation: "Associate Professor", email: "sarah.c@university.edu", image: "https://i.pravatar.cc/150?u=4", subjects: ["Robotics", "AI Ethics"] },
]);
</script>

<style scoped>
.animate-in {
    animation: slideUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.custom-scrollbar::-webkit-scrollbar {
    width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 10px;
}
</style>