<template>
  <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans text-slate-900">
    <div class="max-w-[1440px] mx-auto space-y-6">

      <HeroHeader
        title="Exam Roadmap"
        :subtitle="`Academic Session ${studentYear}`"
        icon="fa fa-calendar-check-o"
      />

      <div class="space-y-4 animate-in">

        <div v-for="(group, type) in groupedExams" :key="type">

          <!-- GROUP HEADER -->
          <div
            @click="toggleGroup(type)"
            class="cursor-pointer bg-white rounded-[2rem] p-4 border border-slate-200/60 shadow-sm hover:border-rose-300 transition-all flex items-center justify-between group"
          >

            <div class="flex items-center gap-4">

              <div
                class="w-12 h-12 bg-rose-50 text-rose-600 rounded-2xl flex items-center justify-center text-xl transition-colors group-hover:bg-rose-600 group-hover:text-white"
              >
                <i :class="expandedGroups.includes(type) ? 'fa fa-folder-open' : 'fa fa-folder'"></i>
              </div>

              <div>
                <h2 class="text-xl font-black text-slate-800 tracking-tight">
                  {{ type }} <span>{{ group.exams.length }} Subjects Scheduled</span>
                </h2>

                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest">
                  {{ group.start_date }} - {{ group.end_date }}
                </p>
              </div>

            </div>

            <div class="flex items-center gap-4">

              <button
                @click.stop="downloadHallTicket(type)"
                class="hidden md:flex px-5 py-2.5 bg-slate-900 text-white rounded-xl text-xs font-black uppercase tracking-widest hover:bg-rose-600 transition-all shadow-md items-center gap-2"
              >
                <i class="fa fa-download"></i> Hall Ticket
              </button>

              <div
                class="text-slate-300 transition-transform duration-300"
                :class="{ 'rotate-180': expandedGroups.includes(type) }"
              >
                <i class="fa fa-chevron-down"></i>
              </div>

            </div>

          </div>

          <!-- SUBJECT LIST -->
          <transition name="expand">
            <div v-if="expandedGroups.includes(type)" class="overflow-hidden">

              <div
                class="grid grid-cols-1 gap-3 mt-3 ml-4 md:ml-12 border-l-2 border-slate-100 pl-4 md:pl-8 pb-4"
              >

                <div
                  v-for="exam in group.exams"
                  :key="exam.id"
                  class="bg-white/50 backdrop-blur-sm rounded-[1.5rem] p-5 border border-slate-100 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:shadow-md transition-all"
                >

                  <div class="flex items-center gap-4">

                    <div class="text-center min-w-[50px]">
                      <span class="block text-xs font-black text-rose-500 uppercase">
                        {{ exam.month }}
                      </span>

                      <span class="text-2xl font-black text-slate-800">
                        {{ exam.day }}
                      </span>
                    </div>

                    <div>
                      <h4 class="font-black text-slate-700 text-base">
                        {{ exam.subject }}
                      </h4>

                      <div class="flex gap-4 mt-1">
                        <span class="text-xs font-bold text-slate-400 uppercase">
                          <i class="fa fa-clock-o mr-1"></i>{{ exam.time }}
                        </span>

                        <span class="text-xs font-bold text-slate-400 uppercase">
                          <i class="fa fa-map-marker mr-1"></i>{{ exam.room }}
                        </span>
                      </div>
                    </div>

                  </div>

                  <span
                    class="text-[10px] font-black px-3 py-1 bg-slate-100 text-slate-500 rounded-full uppercase self-start md:self-center"
                  >
                    {{ exam.dayName }}
                  </span>

                </div>

              </div>

            </div>
          </transition>

        </div>

        <div
          v-if="Object.keys(groupedExams).length === 0"
          class="text-center py-20 text-slate-400 font-bold uppercase text-sm tracking-widest"
        >
          No scheduled exams found.
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import HeroHeader from "~/components/ui/HeroHeader.vue";
import { useExams } from "~/composable/useExaminations";

const config = useRuntimeConfig();

useSeoMeta({
  title: `Exam Schedule - ${config.public.appName}`,
});

const studentYear = ref("2025-26");
const confirmedExams = ref([]);
const expandedGroups = ref([]);

/* GROUP EXAMS BY TYPE */
const groupedExams = computed(() => {
  return confirmedExams.value.reduce((groups, exam) => {
    const type = exam.exam_group;

    if (!groups[type]) {
      groups[type] = {
        start_date: exam.start_date,
        end_date: exam.end_date,
        exams: [],
      };
    }

    groups[type].exams.push(exam);

    return groups;
  }, {});
});

/* TOGGLE GROUP */
const toggleGroup = (type) => {
  const index = expandedGroups.value.indexOf(type);

  if (index > -1) {
    expandedGroups.value.splice(index, 1);
  } else {
    expandedGroups.value.push(type);
  }
};

/* DOWNLOAD HALL TICKET */
const downloadHallTicket = (type) => {
  console.log(`Downloading hall ticket for ${type}`);
};

/* FORMAT TIME */
const formatTime = (timeStr) => {
  if (!timeStr) return "";

  const [h, m] = timeStr.split(":");
  const hour = parseInt(h);

  const ampm = hour >= 12 ? "PM" : "AM";
  const displayHour = hour % 12 || 12;

  return `${displayHour}:${m} ${ampm}`;
};

onMounted(async () => {
  try {
    const data = await useExams();

    if (!Array.isArray(data) || !data.length) return;

    studentYear.value = data[0].academic_year;

    confirmedExams.value = data.map((item, index) => {
      const dateObj = new Date(item.date);

      return {
        id: item.exam_id || index,
        subject: item.subject,

        month: dateObj
          .toLocaleString("default", { month: "short" })
          .toUpperCase(),

        day: dateObj.getDate().toString().padStart(2, "0"),

        dayName: dateObj
          .toLocaleString("default", { weekday: "long" })
          .toUpperCase(),

        exam_group: item.exam_type,

        time: `${formatTime(item.start_time)} - ${formatTime(item.end_time)}`,

        room: item.room,

        start_date: new Date(item.exam_start_date).toLocaleDateString("en-IN", {
          day: "2-digit",
          month: "short",
        }),

        end_date: new Date(item.exam_end_date).toLocaleDateString("en-IN", {
          day: "2-digit",
          month: "short",
        }),
      };
    });

    /* AUTO EXPAND FIRST GROUP */
    const firstGroup = Object.keys(groupedExams.value)[0];

    if (firstGroup) expandedGroups.value.push(firstGroup);
  } catch (error) {
    console.error("Error loading exams:", error);
  }
});
</script>

<style scoped>
.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease-in-out;
  max-height: 1000px;
}

.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-10px);
}

.animate-in {
  animation: slideUp 0.5s ease-out forwards;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>