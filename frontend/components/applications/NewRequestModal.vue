<template>
  <AppModal :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" title="New Request">
    <div class="space-y-6" v-if="!loadingForms">
      <div>
        <label class="text-[10px] font-black uppercase text-slate-400 tracking-[0.2em] mb-3 block">
          Application Type
        </label>

        <div class="flex flex-nowrap gap-3 overflow-x-auto pb-2">
          <button v-for="type in requestTypes" :key="type.id" @click="selectedType = type" :class="[
            selectedType?.id === type.id
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
        <div v-for="field in selectedType.fields" :key="field.field_name">
          <label class="text-xs font-bold text-slate-700 block mb-2">{{ field.field_label }}</label>
          
          <input v-if="field.field_type === 'Data' || field.field_type === 'Number'" 
            :type="field.field_type === 'Number' ? 'number' : 'text'"
            v-model="formData[field.field_name]"
             class="w-full bg-slate-50 border-none rounded-xl p-4 text-sm focus:ring-2 ring-indigo-500 transition-all"
            :placeholder="field.placeholder || ''"
            :required="field.is_required">

          <input v-else-if="field.field_type === 'Date'" 
            type="date"
            v-model="formData[field.field_name]"
             class="w-full bg-slate-50 border-none rounded-xl p-4 text-sm focus:ring-2 ring-indigo-500 transition-all"
            :required="field.is_required">

          <select v-else-if="field.field_type === 'Select'"
            v-model="formData[field.field_name]"
             class="w-full bg-slate-50 border-none rounded-xl p-4 text-sm focus:ring-2 ring-indigo-500 transition-all"
             :required="field.is_required">
             <option value="" disabled>{{ field.placeholder || 'Select an option' }}</option>
             <option v-for="opt in (field.options || '').split('\n').filter(Boolean)" :key="opt" :value="opt">
               {{ opt }}
             </option>
          </select>

          <textarea v-else-if="field.field_type === 'Text' || field.field_type === 'Long Text'" 
            rows="4" 
            v-model="formData[field.field_name]"
            class="w-full bg-slate-50 border-none rounded-xl p-4 text-sm focus:ring-2 ring-indigo-500 transition-all"
            :placeholder="field.placeholder || ''"
            :required="field.is_required"></textarea>

          <label v-else-if="field.field_type === 'Check'" class="flex items-center gap-2 text-sm text-slate-700">
            <input type="checkbox" v-model="formData[field.field_name]" class="rounded text-indigo-600 focus:ring-indigo-500">
            {{ field.field_label }}
          </label>
            
        </div>
      </div>

      <div class="pt-4">
        <button
          @click="submitForm"
          :disabled="isSubmitting"
          class="w-full py-4 bg-indigo-600 text-white rounded-2xl font-black text-sm shadow-lg shadow-indigo-200 hover:bg-indigo-700 transition-all disabled:opacity-50">
          {{ isSubmitting ? 'Submitting...' : 'Submit' }}
        </button>
      </div>
    </div>
    <div v-else class="py-10 text-center text-slate-500 text-sm font-medium animate-pulse">
      Loading forms...
    </div>
  </AppModal>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import AppModal from '@/components/ui/AppModal.vue'
import { call } from '~/composable/useFrappeFetch'
import { useToast } from '~/composable/useToast'

const { addToast } = useToast()

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'submitted'])

const requestTypes = ref([])
const selectedType = ref(null)
const formData = ref({})
const loadingForms = ref(true)
const isSubmitting = ref(false)

onMounted(async () => {
  try {
    const res = await call('maxedu.desk_approval.doctype.application.application.get_active_forms')
    requestTypes.value = res || []
    if (requestTypes.value.length > 0) {
      selectedType.value = requestTypes.value[0]
    }
  } catch (err) {
    console.error(err)
  } finally {
    loadingForms.value = false
  }
})

watch(selectedType, () => {
  formData.value = {}
})

const submitForm = async () => {
  if (!selectedType.value) return
  
  // Basic validation check
  for (const field of selectedType.value.fields) {
    if (field.is_required && !formData.value[field.field_name]) {
      addToast(`${field.field_label} is required`, 'error')
      return
    }
  }
  
  isSubmitting.value = true
  try {
    await call('maxedu.desk_approval.doctype.application.application.submit_application', {
      form: selectedType.value.id,
      data: JSON.stringify(formData.value)
    })
    emit('submitted')
    emit('update:modelValue', false)
    addToast('Request submitted successfully!', 'success')
  } catch (err) {
    addToast(err.message || 'Failed to submit request', 'error')
    console.error(err)
  } finally {
    isSubmitting.value = false
  }
}
</script>
