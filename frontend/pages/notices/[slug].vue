<template>
  <div v-if="detail" class="max-w-7xl mx-auto px-4 py-12 animate-in fade-in">
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
      
      <div class="lg:col-span-8 space-y-8">
        <button @click="router.back()" class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-slate-400">
          <i class="fa fa-arrow-left"></i> Back
        </button>

        <div class="space-y-4">
          <span :class="detail.type === 'Notice' ? 'bg-indigo-50 text-indigo-600' : 'bg-rose-50 text-rose-600'" 
                class="px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest">
            {{ detail.category || detail.type }}
          </span>
          <h1 class="text-4xl font-black text-slate-900">{{ detail.title }}</h1>
          <p class="text-slate-500 text-lg mt-2">{{ detail.description }}</p>
          <span class="text-[10px] font-black text-slate-400">{{ detail.date }}</span>
        </div>

        <div v-if="detail.attachments && detail.attachments.length" class="space-y-4">
           <h3 class="text-xs font-black uppercase text-slate-400">Attached Documents</h3>
           <div v-for="file in detail.attachments" :key="file.file_url" 
                class="p-4 border border-slate-100 rounded-2xl flex items-center justify-between bg-slate-50">
              <div class="flex items-center gap-3">
                 <i class="fa fa-file-pdf-o text-indigo-500"></i>
                 <span class="text-xs font-bold text-slate-700">{{ file.file_name }}</span>
              </div>
              <a :href="file.file_url" target="_blank" class="text-indigo-600 text-xs font-black uppercase">View PDF</a>
           </div>
        </div>
      </div>

    </div>
  </div>

  <div v-else class="h-screen flex items-center justify-center">
     <div class="flex flex-col items-center gap-4">
        <i class="fa fa-circle-o-notch fa-spin text-indigo-600 text-2xl"></i>
        <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Loading Content...</p>
     </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { call } from '~/composable/useFrappeFetch'

const route = useRoute();
const router = useRouter();
const detail = ref(null);

onMounted(async () => {
  const slug = route.params.slug;
  if (!slug) return;
  
  try {
    const res = await call('maxedu.desk_approval.doctype.application.application.get_notice', { slug });
    detail.value = res || null;
  } catch (err) {
    console.error("Failed to fetch notice", err);
    // fallback or redirect could go here
  }
});
</script>