<template>

    <div class="bg-white rounded-[2.5rem] p-5 border border-slate-200 shadow-sm">
        <h6 class="font-bold text-gray-800 mb-4">Campus Notices</h6>
        <div class="relative pl-6 border-l-2 border-gray-100 space-y-6">
            <div v-for="notice in notices" :key="notice.id" class="relative">
                <div class="absolute -left-[31px] top-1 w-4 h-4 rounded-full border-4 border-white"
                    :class="notice.dotColor"></div>
                <p class="text-xs font-bold text-gray-800">{{ notice.title }}</p>
                <p class="text-[11px] text-gray-500 mt-1">{{ notice.desc }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
const props = defineProps(['notices']);

</script>