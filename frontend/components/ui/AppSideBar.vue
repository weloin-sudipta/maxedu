<template>
    <aside class="relative flex flex-col h-full transition-all duration-500 ease-in-out 
    bg-gradient-to-b from-white via-white to-indigo-50/40 
    backdrop-blur-xl border-r border-gray-200/60 
    shadow-xl shadow-indigo-100/40 z-50 group flex-shrink-0"
        :class="[isExpanded ? 'w-[270px]' : 'w-[85px]']" 
        @mouseenter="handleMouseEnter"
        @mouseleave="handleMouseLeave">

        <div class="flex items-center justify-between px-6 h-20 flex-shrink-0">
            <div class="flex items-center gap-3 overflow-hidden">
                <div class="flex-shrink-0 w-10 h-10 bg-gradient-to-tr from-indigo-600 to-purple-500 
          rounded-xl flex items-center justify-center text-white 
          shadow-lg shadow-indigo-300/40 transition-transform duration-300 group-hover:scale-110">
                    <i class="fa fa-graduation-cap"></i>
                </div>

                <transition name="fade">
                    <span v-show="isExpanded"
                        class="font-bold text-xl text-gray-800 whitespace-nowrap tracking-wide">
                        {{ $config.public.appName }}
                    </span>
                </transition>
            </div>

            <button v-show="isExpanded" @click="isCollapsed = !isCollapsed" class="p-2 text-gray-400 transition rounded-full 
        hover:bg-indigo-100 hover:text-indigo-600 duration-300">
                <i class="fa fa-angle-double-left text-xl"></i>
            </button>
        </div>

        <nav class="flex-1 px-4 mt-6 space-y-2 overflow-y-auto custom-scrollbar">

            <div v-for="item in navItems" :key="item.name" class="relative group/item">

                <div v-if="isActive(item)" class="absolute left-0 top-2 h-8 w-1 rounded-r-full bg-indigo-600 shadow-md">
                </div>
                
                <NuxtLink :to="item.children ? '#' : item.route"
                    @click.prevent="item.children ? item.isOpen = !item.isOpen : null" :class="[
                        isActive(item)
                            ? 'bg-indigo-50 text-indigo-600 shadow-md shadow-indigo-100/60'
                            : 'text-gray-600 hover:bg-white hover:shadow-md hover:shadow-indigo-100/40',
                        'flex items-center justify-between px-4 py-3 rounded-xl transition-all duration-300 hover:-translate-y-0.5'
                    ]">
                    <div class="flex items-center gap-4">
                        <span
                            class="w-6 text-center text-lg transition-all duration-300 group-hover/item:scale-110 group-hover/item:text-indigo-600">
                            <i :class="item.icon"></i>
                        </span>

                        <span v-show="isExpanded" class="font-medium whitespace-nowrap tracking-wide">
                            {{ item.name }}
                        </span>
                    </div>

                    <i v-if="item.children && isExpanded"
                        class="fa fa-angle-down transition-transform duration-300 text-xs text-gray-400"
                        :class="{ 'rotate-180 text-indigo-600': item.isOpen }"></i>
                </NuxtLink>

                <transition name="expand">
                    <div v-if="item.children && item.isOpen && isExpanded" class="overflow-hidden">
                        <div class="mt-2 ml-4 pl-6 border-l border-indigo-100 space-y-1 my-2">

                            <NuxtLink v-for="sub in item.children" :key="sub.name" :to="sub.route" :class="[
                                route.path === sub.route
                                    ? 'text-indigo-600 bg-indigo-50'
                                    : 'text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/60',
                                'block px-4 py-2 text-sm font-medium rounded-lg transition-all duration-300 hover:translate-x-1'
                            ]">
                                {{ sub.name }}
                            </NuxtLink>

                        </div>
                    </div>
                </transition>

            </div>

            <!-- Logout Button styled like nav items -->
            <div class="relative group/item">
                <button
                    @click="handleLogout"
                    :disabled="isLoggingOut"
                    class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-all duration-300 
                    text-gray-600 hover:bg-red-50 hover:text-red-500 hover:shadow-md hover:-translate-y-0.5
                    disabled:opacity-50 disabled:cursor-not-allowed">
                    <div class="flex items-center gap-4">
                        <span class="w-6 text-center text-lg transition-all duration-300 group-hover/item:scale-110 group-hover/item:text-red-500">
                            <i :class="isLoggingOut ? 'fa fa-spinner fa-spin' : 'fa fa-sign-out'"></i>
                        </span>
                        <span v-show="isExpanded" class="font-medium whitespace-nowrap tracking-wide">
                            {{ isLoggingOut ? 'Logging out...' : 'Logout' }}
                        </span>
                    </div>
                </button>
            </div>

        </nav>

        <div v-show="isExpanded" class="p-4 border-t border-gray-100 text-xs text-gray-400 text-center">
            © 2026 <b>{{ $config.public.appName }}</b>
        </div>

    </aside>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { logout } from '~/composable/useAuth'

const route = useRoute()
const isCollapsed = ref(false)
const isHovered = ref(false)
const isLoggingOut = ref(false)
let hoverTimeout = null

const isExpanded = computed(() => {
    return !isCollapsed.value || isHovered.value
})

const handleMouseEnter = () => {
    hoverTimeout = setTimeout(() => {
        isHovered.value = true
    }, 50)
}

const handleMouseLeave = () => {
    clearTimeout(hoverTimeout)
    isHovered.value = false
}

const handleLogout = async () => {
    if (isLoggingOut.value) return
    try {
        isLoggingOut.value = true
        await logout()
        navigateTo('/login')
    } catch (error) {
        console.error('Logout failed:', error)
    } finally {
        isLoggingOut.value = false
    }
}

const navItems = reactive([
    { name: 'Dashboard', icon: 'fa fa-th-large', route: '/' },
    {
        name: 'Academics',
        icon: 'fa fa-graduation-cap',
        isOpen: false,
        children: [
            { name: 'Subjects', route: '/academics/subjects' },
            { name: 'Study Materials', route: '/academics/study-materials' },
            { name: 'Timetable', route: '/academics/timetable' },
            { name: 'Assignments', route: '/academics/assignments' },
        ]
    },
    { name: 'Attendance', icon: 'fa fa-calendar-check-o', route: '/attendance' },
    {
        name: 'Examination',
        icon: 'fa fa-file-text-o',
        isOpen: false,
        children: [
            { name: 'Schedule', route: '/exam/shedule' },
            { name: 'Results', route: '/exam/result' },
        ]
    },
    { name: 'Library', icon: 'fa fa-book', route: '/library' },
    { name: 'Events', icon: 'fa fa-calendar', route: '/events' },
    { name: 'Profile', icon: 'fa fa-address-card', route: '/profile' },
    { name: 'Facoulty', icon: 'fa fa-chalkboard-user', route: '/facoulty' },
])

const isActive = (item) => {
    if (item.route && item.route === route.path) return true
    if (item.children) return item.children.some(child => child.route === route.path)
    return false
}

onMounted(() => {
    navItems.forEach(item => {
        if (item.children && isActive(item)) {
            item.isOpen = true
        }
    })
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
    opacity: 0;
}

.expand-enter-active,
.expand-leave-active {
    transition: all 0.4s cubic-bezier(.4, 0, .2, 1);
    max-height: 400px;
    opacity: 1;
}

.expand-enter-from,
.expand-leave-to {
    max-height: 0;
    opacity: 0;
    transform: translateY(-5px);
}

.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #c7d2fe, #a5b4fc);
    border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(to bottom, #818cf8, #6366f1);
}
</style>