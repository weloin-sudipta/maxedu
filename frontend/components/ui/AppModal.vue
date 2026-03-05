<template>
  <Transition name="fade">
    <div v-if="modelValue" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
      
      <!-- Overlay -->
      <div 
        class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm"
        @click="close"
      ></div>

      <!-- Modal Box -->
      <Transition name="zoom">
        <div
          class="relative bg-white w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden"
        >
          
          <!-- Header -->
          <div class="p-6 border-b border-gray-100 flex justify-between items-center">
            <h3 class="text-xl font-bold text-gray-800">
              {{ title }}
            </h3>

            <button @click="close" class="text-gray-400 hover:text-gray-600">
              <i class="fa fa-times text-xl"></i>
            </button>
          </div>

          <!-- Body -->
          <div class="p-6 max-h-[70vh] overflow-y-auto custom-scrollbar">
            <slot />
          </div>

          <!-- Footer (Optional) -->
          <div v-if="$slots.footer" class="p-6 bg-gray-50 flex justify-end">
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
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.zoom-enter-active {
  transition: all 0.2s ease;
}
.zoom-enter-from {
  opacity: 0;
  transform: scale(0.95);
}
</style>