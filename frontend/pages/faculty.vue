<template>
  <div class="min-h-screen bg-[#F8FAFC] p-4 lg:p-10 font-sans text-slate-900">
    <div class="max-w-[1440px] mx-auto space-y-8">
      <HeroHeader title="Faculty & Mentors" subtitle="University Academic Staff Directory" icon="fa fa-users" />

      <div class="animate-in">
        <div class="bg-white rounded-[2.5rem] p-4 border border-slate-200/60 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
          <div class="flex items-center gap-4 ml-2">
            <div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center text-xl">
              <i class="fa fa-search"></i>
            </div>
            <div>
              <h2 class="text-2xl font-black text-slate-800 tracking-tight">Staff Search</h2>
              <p class="text-xs font-black text-slate-400 uppercase tracking-widest">Find by name, role or expertise</p>
            </div>
          </div>
          <div class="relative w-full md:w-96">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Start typing to filter..."
              class="w-full bg-slate-50 border border-slate-100 rounded-2xl py-3.5 px-6 text-sm font-bold text-slate-700 outline-none focus:bg-white focus:ring-4 focus:ring-indigo-500/5 focus:border-indigo-200 transition-all"
            />
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <UiSkeleton height="h-64" v-for="i in 8" :key="i" class="rounded-[2.2rem]" />
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-100 rounded-2xl p-6 text-center text-red-400 text-base font-bold">
        Failed to load faculty data.
      </div>

      <!-- Cards Grid -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 animate-in">
        <div
          v-for="member in filteredMembers"
          :key="member.id"
          class="bg-white rounded-[2.2rem] p-5 border border-slate-100 shadow-sm hover:shadow-xl hover:border-indigo-100/50 transition-all duration-500 group relative overflow-hidden flex flex-col justify-between"
        >
          <div class="absolute -right-6 -top-6 w-20 h-20 bg-slate-50 rounded-full group-hover:bg-indigo-50/50 transition-colors duration-500"></div>

          <div class="relative z-10">
            <div class="flex justify-between items-center mb-4">
              <div class="relative">
                <!-- Initials Avatar -->
                <div class="h-16 w-16 rounded-2xl bg-indigo-100 text-indigo-600 flex items-center justify-center border-2 border-white shadow-sm group-hover:scale-105 transition-transform duration-500 font-black text-lg uppercase tracking-wide">
                  {{ getInitials(member.name) }}
                </div>
                <div class="absolute -bottom-0.5 -right-0.5 h-3.5 w-3.5 bg-green-500 border-2 border-white rounded-full shadow-sm"></div>
              </div>
              <span :class="['px-3 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest border shadow-sm', roleTheme(member.role)]">
                {{ member.role }}
              </span>
            </div>

            <div class="space-y-1.5">
              <h3 class="text-base font-black text-slate-900 group-hover:text-indigo-600 transition-colors leading-tight">
                {{ member.name }}
              </h3>
              <p class="text-[11px] text-slate-400 font-black uppercase tracking-widest flex items-center gap-2">
                <span class="w-2 h-[1px] bg-indigo-300"></span>
                {{ member.designation }}
              </p>
            </div>

            <div class="mt-3 mb-4">
              <div class="flex items-center gap-2">
                <div class="w-6 h-6 rounded-lg bg-slate-50 flex items-center justify-center">
                  <i class="fa fa-calendar-o text-[11px] text-slate-400"></i>
                </div>
                <span class="text-xs font-bold text-slate-500">{{ member.term }}</span>
              </div>
            </div>
          </div>

          <div class="pt-3 border-t border-slate-50">
            <div v-if="member.subjects.length" class="flex flex-wrap gap-1">
              <span
                v-for="sub in member.subjects.slice(0, 2)"
                :key="sub"
                class="px-2.5 py-1 text-[10px] font-black text-slate-500 bg-slate-50 border border-slate-100 rounded-md group-hover:bg-white transition-colors"
              >
                {{ sub }}
              </span>
              <span v-if="member.subjects.length > 2" class="text-[10px] font-black text-slate-300 ml-1 self-center">
                +{{ member.subjects.length - 2 }}
              </span>
            </div>
            <div v-else class="flex items-center gap-1.5 opacity-60">
              <div class="w-1 h-1 bg-slate-300 rounded-full"></div>
              <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">No subjects assigned</span>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import HeroHeader from "~/components/ui/HeroHeader.vue";
import { useFacultyMember } from "~/composable/useFacultyMember";

const { members, fetchMember } = useFacultyMember();

const searchQuery = ref("");
const loading = ref(true);
const error = ref(false);

// e.g. "Prof. Sharma" → "PS", "Dr. Arjun Sharma" → "DS", "Ms. Priya Verma" → "MV"
const getInitials = (name) => {
  if (!name) return "?";
  const parts = name.trim().split(/\s+/);
  if (parts.length === 1) return parts[0][0].toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
};

const mapMember = (item) => {
  const ins = item.instructor;
  const logs = item.logs || [];

  return {
    id: ins.name,
    name: ins.instructor_name || ins.name,
    role: ins.status === "Active" ? "Teacher" : "Staff",
    designation: logs[0]?.program || ins.naming_series || "—",
    term: logs[0]?.academic_term || "—",
    subjects: [...new Set(logs.map((l) => l.course).filter(Boolean))],
  };
};

const facultyMembers = ref([]);

const filteredMembers = computed(() => {
  const q = searchQuery.value.toLowerCase();
  if (!q) return facultyMembers.value;
  return facultyMembers.value.filter((m) =>
    [m.name, m.role, m.designation, ...m.subjects].join(" ").toLowerCase().includes(q)
  );
});

const roleTheme = (role) => {
  const themes = {
    HOD: "bg-indigo-50 text-indigo-600 border-indigo-100",
    Teacher: "bg-cyan-50 text-cyan-600 border-cyan-100",
    Librarian: "bg-amber-50 text-amber-600 border-amber-100",
    Staff: "bg-slate-100 text-slate-500 border-slate-200",
  };
  return themes[role] || themes["Staff"];
};

onMounted(async () => {
  try {
    await fetchMember();
    facultyMembers.value = (members.value || []).map(mapMember);
  } catch (e) {
    error.value = true;
  } finally {
    loading.value = false;
  }
});
</script>
