<template>
  <aside 
    class="relative flex flex-col h-full transition-all duration-500 ease-in-out bg-gradient-to-b from-white via-white to-indigo-50/40 backdrop-blur-xl border-r border-gray-200/60 shadow-xl shadow-indigo-100/40 z-50 group flex-shrink-0"
    :class="[isExpanded ? 'w-[270px]' : 'w-[85px]']" 
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
  >
    <div class="flex items-center justify-between px-6 h-20 flex-shrink-0">
      <div class="flex items-center gap-3 overflow-hidden">
        <div class="flex-shrink-0 w-10 h-10 bg-gradient-to-tr from-indigo-600 to-purple-500 rounded-xl flex items-center justify-center text-white shadow-lg shadow-indigo-300/40 transition-transform duration-300 group-hover:scale-110">
          <i class="fa fa-graduation-cap"></i>
        </div>

        <transition name="fade">
          <span v-show="isExpanded" class="font-bold text-xl text-gray-800 whitespace-nowrap tracking-wide">
            {{ $config.public.appName }}
          </span>
        </transition>
      </div>

      <button v-show="isExpanded" @click="isCollapsed = !isCollapsed" class="p-2 text-gray-400 transition rounded-full hover:bg-indigo-100 hover:text-indigo-600 duration-300">
        <i class="fa fa-angle-double-left text-xl"></i>
      </button>
    </div>

    <nav class="flex-1 px-4 mt-4 space-y-1 overflow-y-auto custom-scrollbar">
      <template v-for="(item, index) in navItems" :key="item.name || item.header">
        
        <div v-if="item.header && isExpanded" 
             class="px-4 mt-6 mb-2 text-[10px] font-black uppercase tracking-[0.2em] text-indigo-400/80">
          {{ item.header }}
        </div>

        <div v-if="!item.header" class="relative group/item">
          <div v-if="isActive(item)" class="absolute left-0 top-2 h-8 w-1 rounded-r-full bg-indigo-600 shadow-md"></div>
          
          <NuxtLink 
            :to="item.children ? '#' : item.route"
            @click.prevent="item.children ? item.isOpen = !item.isOpen : null" 
            :class="[
              isActive(item)
                ? 'bg-indigo-50 text-indigo-600 shadow-md shadow-indigo-100/60'
                : 'text-gray-600 hover:bg-white hover:shadow-md hover:shadow-indigo-100/40',
              'flex items-center justify-between px-4 py-3 rounded-xl transition-all duration-300 hover:-translate-y-0.5'
            ]"
          >
            <div class="flex items-center gap-4">
              <span class="w-6 text-center text-lg transition-all duration-300 group-hover/item:scale-110 group-hover/item:text-indigo-600">
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
                <NuxtLink 
                  v-for="sub in item.children" 
                  :key="sub.name" 
                  :to="sub.route" 
                  :class="[
                    route.path === sub.route
                      ? 'text-indigo-600 bg-indigo-50'
                      : 'text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/60',
                    'block px-4 py-2 text-sm font-medium rounded-lg transition-all duration-300 hover:translate-x-1'
                  ]"
                >
                  {{ sub.name }}
                </NuxtLink>
              </div>
            </div>
          </transition>
        </div>
      </template>

      <div class="pt-4 mt-4 border-t border-gray-100">
        <div class="relative group/item">
          <button
            @click="handleLogout"
            :disabled="isLoggingOut"
            class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-all duration-300 text-gray-600 hover:bg-red-50 hover:text-red-500 hover:shadow-md hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed"
          >
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
      </div>
    </nav>

    <div v-show="isExpanded" class="p-4 border-t border-gray-100 text-[10px] text-gray-400 text-center uppercase tracking-widest font-bold">
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
  // MAIN SECTION
  { header: 'Main Menu' },
  { name: 'Dashboard', icon: 'fa fa-th-large', route: '/' },
  { name: 'Notice & News', icon: 'fa fa-bullhorn', route: '/notice-news' },
  { name: 'Events', icon: 'fa fa-calendar', route: '/events' },

  // ACADEMIC SECTION
  { header: 'Academic Life' },
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
      { name: 'Schedule', route: '/exam/schedule' },
      { name: 'Results', route: '/exam/result' },
    ]
  },

  // RESOURCES SECTION
  { header: 'Resources' },
  { 
    name: 'Documents', 
    icon: 'fa fa-folder-open', 
    isOpen: false,
    children: [
      { name: 'Certificates', route: '/documents/personal' },
      { name: 'Fee Receipts', route: '/documents/fees' },
      { name: 'ID Card', route: '/documents/id-card' },
    ]
  },
  { name: 'Library', icon: 'fa fa-book', route: '/library' },
  { name: 'Faculty', icon: 'fa fa-graduation-cap', route: '/facoulty' },
  { name: 'Profile', icon: 'fa fa-address-card', route: '/profile' },
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
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #e2e8f0;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #cbd5e1;
}
</style>