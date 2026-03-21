<template>
  <AppModal :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" title="New Request">
    <div class="space-y-6">
      <div>
        <label class="text-[10px] font-black uppercase text-slate-400 tracking-[0.2em] mb-3 block">
          Application Type
        </label>

        <div class="flex flex-nowrap gap-3 overflow-x-auto pb-2">
          <button v-for="type in requestTypes" :key="type.id" @click="selectedType = type" :class="[
            selectedType.id === type.id
              ? 'border-indigo-500 bg-indigo-50 text-indigo-600'
              : 'border-slate-100 bg-slate-50 text-slate-500',
            'relative flex items-center justify-center gap-2 p-3 rounded-2xl border-2 transition-all flex-shrink-0 group'
          ]">

            <i :class="type.icon" class="text-lg"></i>

            <span class="hidden md:block text-xs font-bold whitespace-nowrap">
              {{ type.label }}
            </span>

            <span
              class="md:hidden absolute -top-10 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-[10px] px-2 py-1 rounded opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity whitespace-nowrap z-10">
              {{ type.label }}
            </span>
          </button>
        </div>
      </div>

      <div v-if="selectedType" class="space-y-4 animate-in fade-in slide-in-from-bottom-2">
        <div>
          <label class="text-xs font-bold text-slate-700 block mb-2">Subject / Title</label>
          <input type="text"
            class="w-full bg-slate-50 border-none rounded-xl p-4 text-sm focus:ring-2 ring-indigo-500 transition-all"
            :placeholder="selectedType.placeholder">
        </div>

        <div v-if="selectedType.id === 'leave'" class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-xs font-bold text-slate-700 block mb-2">From</label>
            <input type="date" class="w-full bg-slate-50 border-none rounded-xl p-4 text-sm">
          </div>
          <div>
            <label class="text-xs font-bold text-slate-700 block mb-2">To</label>
            <input type="date" class="w-full bg-slate-50 border-none rounded-xl p-4 text-sm">
          </div>
        </div>

        <div>
          <label class="text-xs font-bold text-slate-700 block mb-2">Detailed Reason</label>
          <textarea rows="4" class="w-full bg-slate-50 border-none rounded-xl p-4 text-sm"
            placeholder="Explain your request in detail..."></textarea>
        </div>
      </div>

      <div class="pt-4">
        <button
          class="w-full py-4 bg-indigo-600 text-white rounded-2xl font-black text-sm shadow-lg shadow-indigo-200 hover:bg-indigo-700 transition-all">
          Submit to Class Teacher
        </button>
      </div>
    </div>
  </AppModal>
</template>

<script setup>
import { ref } from 'vue'
import AppModal from '@/components/ui/AppModal.vue'

defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

defineEmits(['update:modelValue'])

const selectedType = ref({ id: 'leave', label: 'Leave', icon: 'fa fa-calendar-minus', placeholder: 'Sick Leave / Family Event' })

const requestTypes = [
  { id: 'leave', label: 'Leave', icon: 'fa fa-calendar-minus', placeholder: 'Reason for leave...' },
  { id: 'improvement', label: 'Improvement', icon: 'fa fa-lightbulb', placeholder: 'Subject improvement...' },
  { id: 'facility', label: 'Resource', icon: 'fa fa-book', placeholder: 'Need new lab equipment...' },
  { id: 'complaint', label: 'Complaint', icon: 'fa fa-exclamation-triangle', placeholder: 'Report an issue...' }
]
</script>
