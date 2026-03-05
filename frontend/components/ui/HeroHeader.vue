<template>
  <header
    class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 
           p-8 flex flex-col lg:flex-row justify-between items-center gap-6"
  >

    <!-- LEFT SECTION -->
    <div class="flex items-center gap-4">

      <!-- Optional Icon -->
      <div v-if="icon"
           class="w-14 h-14 bg-indigo-600 rounded-2xl flex items-center 
                  justify-center text-white shadow-xl shadow-indigo-100">
        <i :class="icon + ' text-2xl'"></i>
      </div>

      <div>
        <h1 class="text-3xl font-black tracking-tight text-slate-800">
          {{ title }}
        </h1>

        <p v-if="subtitle"
           class="text-[10px] font-black text-slate-400 uppercase 
                  tracking-[0.2em] mt-1">
          {{ subtitle }}
        </p>
      </div>

    </div>

    <!-- RIGHT SECTION -->
    <div class="flex items-center gap-4 w-full lg:w-auto">

      <!-- Optional Search -->
      <div v-if="searchable"
           class="w-full lg:w-96 relative">
        <i class="fa fa-search absolute left-4 top-1/2 -translate-y-1/2 text-slate-300"></i>

        <input
          v-model="internalSearch"
          @input="$emit('update:search', internalSearch)"
          type="text"
          :placeholder="searchPlaceholder"
          class="w-full bg-slate-50 border border-slate-100 rounded-2xl 
                 pl-12 pr-4 py-3 text-xs font-bold text-slate-700 
                 outline-none focus:ring-4 focus:ring-indigo-500/10 transition-all"
        />
      </div>

      <!-- Action Buttons Slot -->
      <div class="flex gap-3">
        <slot />
      </div>

    </div>

  </header>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  title: String,
  subtitle: String,
  icon: String,
  searchable: {
    type: Boolean,
    default: false
  },
  search: String,
  searchPlaceholder: {
    type: String,
    default: 'Search...'
  }
})

const emit = defineEmits(['update:search'])

const internalSearch = ref(props.search || '')

watch(() => props.search, (val) => {
  internalSearch.value = val
})
</script>