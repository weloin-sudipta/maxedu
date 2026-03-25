<template>
  <Transition name="fade">
    <div v-if="modelValue" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
      
      <!-- Overlay (Lighter for Visibility) -->
      <div 
        class="absolute inset-0 bg-slate-900/10 backdrop-blur-[2px]"
        @click="close"
      ></div>

      <!-- Modal Box -->
      <Transition name="zoom">
        <div
          :class="['relative bg-white/90 dark:bg-slate-900/90 backdrop-blur-2xl w-full border border-white/50 dark:border-slate-800/50 rounded-[2rem] shadow-[0_20px_60px_-15px_rgba(0,0,0,0.1)] dark:shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5)] overflow-hidden flex flex-col', maxWidth]"
          :style="{ maxHeight: '90vh' }"
        >
          
          <!-- Header -->
          <div class="px-8 py-6 border-b border-slate-100/50 dark:border-slate-800/50 flex justify-between items-center bg-white/50 dark:bg-slate-900/50">
            <h3 class="text-xl font-black tracking-tight text-slate-800 dark:text-white uppercase">
              {{ title }}
            </h3>

            <button @click="close" class="w-10 h-10 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-400 hover:text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-900/30 transition-all flex items-center justify-center">
              <i class="fa fa-times text-lg"></i>
            </button>
          </div>

          <!-- Body -->
          <div class="p-8 overflow-y-auto custom-scrollbar flex-1">
            <slot />
          </div>

          <!-- Footer (Optional) -->
          <div v-if="$slots.footer" class="p-6 bg-slate-50/50 dark:bg-slate-800/50 border-t border-slate-100/50 dark:border-slate-800/50 flex justify-end gap-3 rounded-b-[2rem]">
            <slot name="footer" />
          </div>

        </div>
      </Transition>

    </div>
  </Transition>
</template>

<script setup>
defineProps({
  modelValue: Boolean,
  title: {
    type: String,
    default: "Modal Title"
  },
  maxWidth: {
    type: String,
    default: "max-w-2xl"
  }
})

const emit = defineEmits(["update:modelValue"])

const close = () => {
  emit("update:modelValue", false)
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.zoom-enter-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.zoom-enter-from {
  opacity: 0;
  transform: scale(0.95) translateY(10px);
}

.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 9999px; }
.dark .custom-scrollbar::-webkit-scrollbar-thumb { background: #334155; }
</style>