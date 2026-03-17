<template>
  <div class="space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-700">
    
    <div class="bg-slate-900 rounded-[2.5rem] p-8 lg:p-12 overflow-hidden relative shadow-2xl">
      <div class="relative z-10 max-w-2xl">
        <span class="text-indigo-400 text-[10px] font-black uppercase tracking-[0.3em] mb-4 block">Tailored for you</span>
        <h1 class="text-3xl lg:text-5xl font-black text-white leading-tight mb-4">
          Recommended <br/> <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">Reading List</span>
        </h1>
        <p class="text-slate-400 text-sm font-medium max-w-md leading-relaxed">
          Based on your enrollment and your recent interests.
        </p>
      </div>
      <div class="absolute -right-20 -top-20 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl"></div>
    </div>

    <div v-if="loading" class="space-y-12">
      <div v-for="i in 3" :key="i" class="space-y-6">
        <div class="px-2">
          <div class="h-6 w-48 bg-slate-200 rounded animate-pulse mb-2"></div>
          <div class="h-3 w-64 bg-slate-100 rounded animate-pulse"></div>
        </div>
        <div class="flex gap-6 overflow-x-auto pb-6">
          <div v-for="j in 4" :key="j" class="min-w-[280px] bg-slate-100 rounded-3xl h-96 animate-pulse"></div>
        </div>
      </div>
    </div>

    <div v-for="(section, index) in recommendations" :key="index" class="space-y-6">
      <div class="flex items-end justify-between px-2">
        <div>
          <h2 class="text-xl font-black text-slate-800 tracking-tight">{{ section.title }}</h2>
          <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">{{ section.subtitle }}</p>
        </div>
        <button class="text-xs font-black text-indigo-600 hover:text-slate-900 transition-colors uppercase tracking-widest">
          View All <i class="fa fa-arrow-right ml-2"></i>
        </button>
      </div>

      <div class="flex gap-6 overflow-x-auto pb-6 scrollbar-hide snap-x">
        <div v-for="book in section.books" :key="book.id" 
             class="min-w-[280px] group bg-white rounded-3xl border border-slate-100 p-5 hover:shadow-xl hover:shadow-indigo-500/5 transition-all duration-300 snap-start">
          
          <div class="relative mb-4 aspect-[3/4] overflow-hidden rounded-2xl bg-slate-100">
             <div class="absolute top-3 left-3 z-10">
                <span class="px-2.5 py-1.5 rounded-lg bg-white/90 backdrop-blur-md border border-slate-100 text-[8px] font-black uppercase tracking-tighter text-slate-800 shadow-sm">
                  <i :class="section.icon" class="mr-1 text-indigo-500"></i> {{ section.badge }}
                </span>
             </div>

             <div class="w-full h-full flex items-center justify-center group-hover:scale-110 transition-transform duration-500">
                <i class="fa fa-book-reader text-4xl text-slate-200"></i>
             </div>
             
             <div class="absolute inset-0 bg-slate-900/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
                <button class="w-10 h-10 rounded-full bg-white text-slate-900 flex items-center justify-center hover:bg-indigo-600 hover:text-white transition-colors">
                  <i class="fa fa-bookmark-o"></i>
                </button>
                <button class="px-4 py-2 rounded-full bg-indigo-600 text-white text-[10px] font-black uppercase tracking-widest">
                  Preview
                </button>
             </div>
          </div>

          <div class="space-y-1">
            <h3 class="font-black text-slate-800 truncate">{{ book.title }}</h3>
            <p class="text-[10px] font-bold text-slate-400 uppercase">{{ book.author }}</p>
          </div>

          <div class="mt-4 pt-4 border-t border-slate-50 flex items-center justify-between">
            <span class="text-[9px] font-black text-indigo-500 bg-indigo-50 px-2 py-1 rounded-md uppercase">
              {{ book.category }}
            </span>
            <div class="flex items-center gap-1">
               <i class="fa fa-star text-amber-400 text-[10px]"></i>
               <span class="text-[10px] font-black text-slate-700">{{ book.score }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!loading && (!recommendations || recommendations.length === 0)" class="bg-white rounded-[2.5rem] p-12 text-center border border-dashed border-slate-200">
      <i class="fa fa-inbox text-slate-100 text-6xl mb-4"></i>
      <p class="text-xs font-black text-slate-400 uppercase tracking-widest">No recommendations available yet</p>
      <p class="text-[10px] text-slate-400 mt-2">We'll personalize recommendations as you borrow more books</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const loading = ref(false);

const recommendations = ref([
  {
    title: "Recommended for BCA",
    subtitle: "Based on your program",
    badge: "Program",
    icon: "fa fa-graduation-cap",
    books: [
      {
        id: 1,
        title: "Introduction to Algorithms",
        author: "Thomas H. Cormen",
        category: "Computer Science",
        score: 9.2
      },
      {
        id: 2,
        title: "Clean Code",
        author: "Robert C. Martin",
        category: "Programming",
        score: 9.5
      },
      {
        id: 3,
        title: "Database System Concepts",
        author: "Abraham Silberschatz",
        category: "Database",
        score: 8.9
      },
      {
        id: 4,
        title: "Computer Networks",
        author: "Andrew S. Tanenbaum",
        category: "Networking",
        score: 9.1
      }
    ]
  },
  {
    title: "Popular Books",
    subtitle: "Most borrowed in library",
    badge: "Trending",
    icon: "fa fa-fire",
    books: [
      {
        id: 5,
        title: "The Pragmatic Programmer",
        author: "Andrew Hunt",
        category: "Programming",
        score: 9.4
      },
      {
        id: 6,
        title: "Artificial Intelligence",
        author: "Stuart Russell",
        category: "AI",
        score: 9.0
      },
      {
        id: 7,
        title: "Operating System Concepts",
        author: "Abraham Silberschatz",
        category: "OS",
        score: 8.8
      },
      {
        id: 8,
        title: "Python Crash Course",
        author: "Eric Matthes",
        category: "Python",
        score: 9.3
      }
    ]
  },
  {
    title: "Highly Rated",
    subtitle: "Top rated by students",
    badge: "Top Rated",
    icon: "fa fa-star",
    books: [
      {
        id: 9,
        title: "Deep Learning",
        author: "Ian Goodfellow",
        category: "AI",
        score: 9.7
      },
      {
        id: 10,
        title: "Design Patterns",
        author: "Erich Gamma",
        category: "Software Design",
        score: 9.6
      },
      {
        id: 11,
        title: "You Don't Know JS",
        author: "Kyle Simpson",
        category: "JavaScript",
        score: 9.2
      },
      {
        id: 12,
        title: "Modern Operating Systems",
        author: "Andrew Tanenbaum",
        category: "OS",
        score: 9.1
      }
    ]
  }
]);
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>