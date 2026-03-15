<template>
    <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200 shadow-sm">

        <h3 class="text-xs font-black uppercase tracking-widest text-slate-400 mb-6">
            Recommended Books
        </h3>

        <div class="space-y-4">

            <div v-for="book in recommendedBooks" :key="book.title"
                class="flex items-center gap-4 p-2 hover:bg-slate-50 rounded-xl">

                <!-- <img :src="book.cover" class="w-10 h-14 object-cover rounded-md shadow" /> -->

                <div>

                    <p class="text-xs font-black text-slate-700">
                        {{ book.title }}
                    </p>

                    <p class="text-[10px] text-slate-400">
                        ~by {{ book.author }}
                    </p>

                </div>

            </div>

        </div>

    </div>
</template>
<script setup>
const props = defineProps(['recommendedBooks']);

</script>