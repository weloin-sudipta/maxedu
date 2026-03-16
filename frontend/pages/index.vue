<template>
    <div v-if="isLoading">
    <div class="flex items-center justify-center h-screen bg-[#f5f5f9] overflow-hidden">

        <div class="absolute top-[-10%] left-[-10%] w-72 h-72 bg-indigo-200/50 rounded-full blur-3xl animate-pulse">
        </div>
        <div class="absolute bottom-[-10%] right-[-10%] w-72 h-72 bg-rose-200/50 rounded-full blur-3xl animate-pulse"
            style="animation-delay: 1s"></div>

        <div
            class="relative z-10 text-center p-12 bg-white/40 backdrop-blur-md rounded-[3rem] border border-white/60 shadow-2xl shadow-indigo-100/50 max-w-xs w-full">

            <div class="relative w-24 h-24 mx-auto mb-8">
                <div
                    class="absolute inset-0 border-[3px] border-dashed border-indigo-200 rounded-full animate-[spin_8s_linear_infinite]">
                </div>

                <div
                    class="absolute inset-0 border-[3px] border-transparent border-t-indigo-600 border-r-indigo-600 rounded-full animate-spin">
                </div>

                <div
                    class="absolute inset-4 bg-indigo-600 rounded-2xl flex items-center justify-center text-white shadow-xl shadow-indigo-200 animate-bounce-slow">
                    <i v-if="loadingStep < 50" class="fa fa-graduation-cap text-2xl animate-in fade-in"></i>
                    <i v-else class="fa fa-book text-2xl animate-in zoom-in"></i>
                </div>

                <div class="absolute -top-2 left-1/2 w-2 h-2 bg-rose-500 rounded-full animate-ping"></div>
                <div class="absolute -bottom-2 left-1/3 w-1.5 h-1.5 bg-indigo-400 rounded-full animate-ping"
                    style="animation-delay: 0.5s"></div>
            </div>

            <h2 class="text-xs font-black text-slate-800 uppercase tracking-[0.3em] mb-2">
                Authenticating
            </h2>

            <div class="w-full bg-indigo-100 h-1 rounded-full overflow-hidden mb-4">
                <div class="bg-indigo-600 h-full transition-all duration-300 ease-out"
                    :style="{ width: loadingStep + '%' }"></div>
            </div>

            <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest animate-pulse">
                Setting up your workspace...
            </p>

        </div>
    </div>
    </div>

    <component v-else :is="currentComponent" />
</template>

<script setup>
import { ref, onMounted } from 'vue'

// Import pages you want to load
import AdminDashboard from '~/pages/dashboard/admin.vue'
import StudentDashboard from '~/pages/dashboard/student.vue'

const loadingStep = ref(0)
const is_admin = false   // change dynamically later
const isLoading = ref(true)

const currentComponent = ref(null)

onMounted(() => {

  const interval = setInterval(() => {
    if (loadingStep.value < 100) {
      loadingStep.value += 2
    } else {
      clearInterval(interval)
    }
  }, 40)

  setTimeout(() => {
    isLoading.value = false

    if (is_admin) {
      currentComponent.value = AdminDashboard
    } else {
      currentComponent.value = StudentDashboard
    }

  })
})
</script>

<style scoped>
.animate-bounce-slow {
    animation: bounceCustom 2s infinite ease-in-out;
}

@keyframes bounceCustom {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-8px);
    }
}

/* Custom spin for the dashed ring */
@keyframes spin-slow {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.fade-in {
    animation: fadeIn 0.5s ease-in;
}

.zoom-in {
    animation: zoomIn 0.5s ease-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

@keyframes zoomIn {
    from {
        transform: scale(0);
    }

    to {
        transform: scale(1);
    }
}
</style>