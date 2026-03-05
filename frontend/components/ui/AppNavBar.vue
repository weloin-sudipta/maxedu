<template>
    <nav
        class="sticky top-4 z-40 mx-6 mt-4 p-4 bg-white/80 backdrop-blur-md rounded-xl shadow-sm border border-gray-100 flex items-center justify-between flex-shrink-0">
        <div class="flex items-center flex-1 max-w-md">
            <div class="relative w-full group">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i
                        class="fa fa-search text-gray-400 group-focus-within:text-indigo-600 transition-colors duration-200"></i>
                </div>

                <input type="text" placeholder="Search (Ctrl+/)" class="block w-full pl-10 pr-12 py-2.5 bg-white border border-transparent rounded-xl text-sm text-gray-700 
                   placeholder-gray-400
                   shadow-sm transition-all duration-300
                   hover:bg-gray-50
                   focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 focus:outline-none" />

                <div class="absolute inset-y-0 right-0 pr-3 hidden md:flex items-center pointer-events-none">
                    <kbd
                        class="px-1.5 py-0.5 text-[10px] font-semibold text-gray-400 bg-gray-100 border border-gray-200 rounded-md">
                        ⌘ /
                    </kbd>
                </div>
            </div>
        </div>

        <div class="flex items-center gap-4">
            <div class="relative">
                <button @click="isNotifOpen = !isNotifOpen"
                    class="relative p-2 text-gray-500 hover:bg-indigo-50 hover:text-indigo-600 rounded-full transition duration-300">
                    <span class="absolute w-2 h-2 bg-red-500 border-2 border-white rounded-full top-2 right-2"></span>
                    <i class="fa fa-bell-o text-xl"></i>
                </button>

                <div v-if="isNotifOpen"
                    class="absolute right-0 mt-3 w-80 md:w-96 bg-white rounded-2xl shadow-2xl border border-gray-100 overflow-hidden z-50 animate-fade-in-up">

                    <div class="p-4 border-b border-gray-50 flex justify-between items-center bg-white">
                        <h6 class="text-sm font-bold text-gray-800">Notifications</h6>
                        <button class="text-[10px] font-bold text-indigo-600 uppercase hover:underline">Mark all as
                            read</button>
                    </div>

                    <div class="max-h-[400px] overflow-y-auto custom-scrollbar">
                        <div v-if="notifications.length > 0">
                            <div v-for="notif in notifications" :key="notif.id"
                                class="p-4 flex gap-4 hover:bg-gray-50 cursor-pointer border-b border-gray-50 last:border-0 transition">
                                <div
                                    :class="['w-10 h-10 rounded-full flex items-center justify-center shrink-0', notif.bg]">
                                    <i :class="['fa text-white', notif.icon]"></i>
                                </div>
                                <div class="flex-1">
                                    <p class="text-xs font-bold text-gray-800 mb-1">{{ notif.title }}</p>
                                    <p class="text-[11px] text-gray-500 line-clamp-2 leading-relaxed">{{ notif.message
                                    }}</p>
                                    <p class="text-[9px] text-gray-400 mt-2 font-medium"><i
                                            class="fa fa-clock-o mr-1"></i>{{ notif.time }}</p>
                                </div>
                                <div v-if="!notif.read" class="w-2 h-2 bg-indigo-500 rounded-full mt-1"></div>
                            </div>
                        </div>

                        <div v-else class="p-10 text-center">
                            <i class="fa fa-bell-slash-o text-gray-200 text-4xl mb-3"></i>
                            <p class="text-xs text-gray-400 font-medium">All caught up!</p>
                        </div>
                    </div>

                    <button
                        class="w-full p-3 text-center text-xs font-bold text-indigo-600 bg-indigo-50/50 hover:bg-indigo-50 transition">
                        View All Notifications
                    </button>
                </div>
            </div>

            <!-- <div class="flex items-center gap-3 pl-2 border-l border-gray-100">
            </div> -->

            <!-- Add Half moon icon -->
            <div class="flex items-center gap-3 pl-2">
                <button
                    class="p-2 text-gray-500 hover:bg-indigo-50 hover:text-indigo-600 rounded-full transition duration-300">
                    <i class="fa fa-moon-o text-xl"></i>
                </button>
            </div>

            <div class="flex items-center gap-3 pl-2">
                <div class=" flex-col items-end hidden sm:flex">
                    <span class="text-sm font-semibold text-gray-700">{{ profileData?.firstName || 'User' }} {{
                        profileData?.lastName || '' }}</span>
                    <span class="text-xs text-gray-400 uppercase">Admin</span>
                </div>
                <div
                    class="w-10 h-10 font-bold text-white bg-indigo-500 border-2 border-white rounded-full shadow-sm flex items-center justify-center">
                    {{ profileData?.firstName?.charAt(0) || 'U' }}{{ profileData?.lastName?.charAt(0) || '' }}
                </div>
            </div>
        </div>
    </nav>

    <div v-if="isNotifOpen" @click="isNotifOpen = false" class="fixed inset-0 z-30 bg-transparent"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserProfile } from '~/composable/useUserProfile'

const { profileData, loadProfile } = useUserProfile()

onMounted(() => {
    loadProfile()
})

const isNotifOpen = ref(false)

const notifications = ref([
    {
        id: 1,
        title: 'New Exam Scheduled',
        message: 'The Mid-term schedule for Advanced UI/UX has been published.',
        time: '5 min ago',
        icon: 'fa-calendar',
        bg: 'bg-indigo-500',
        read: false
    },
    {
        id: 2,
        title: 'Fee Payment Successful',
        message: 'Your payment was successful.',
        time: '2 hours ago',
        icon: 'fa-check-circle',
        bg: 'bg-emerald-500',
        read: true
    }
])
</script>

<style scoped>
/* Scrollbar Styling to match Sneat */
.custom-scrollbar::-webkit-scrollbar {
    width: 5px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #dbdde0;
    border-radius: 10px;
}

/* Modal Animation */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-fade-in-up {
    animation: fadeInUp 0.2s ease-out forwards;
}

/* For truncating long text */
.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>