<template>
  <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans">
    <div class="max-w-[1440px] mx-auto space-y-6">
      
      <!-- Header -->
      <header class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 p-8 flex flex-col md:flex-row justify-between items-center gap-6">
        <div>
          <h1 class="text-3xl font-black tracking-tight text-slate-800">Library Management</h1>
          <p class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mt-1">Physical Book Tracking System</p>
        </div>

        <!-- Tabs -->
        <div class="flex p-1.5 bg-slate-100 rounded-2xl overflow-x-auto">
          <button @click="currentView = 'issued'" :class="tabClass(currentView === 'issued')">Issued Books</button>
          <button @click="currentView = 'all'" :class="tabClass(currentView === 'all')">All Books</button>
          <button @click="currentView = 'requests'" :class="tabClass(currentView === 'requests')">Book Requests</button>
          <button @click="currentView = 'recommendations'" :class="tabClass(currentView === 'recommendations')">Recommendations</button>
          <nuxt-link to="/library/tracking" :class="tabClass(false)">
            <i class="fa fa-chart-line mr-1"></i> Tracking
          </nuxt-link>
        </div>
      </header>

      <!-- Tab Content -->
      <transition name="fade" mode="out-in">
        <component 
          :is="
            currentView === 'issued' ? IssuedBooks 
            : currentView === 'all' ? AllBooks 
            : currentView === 'requests' ? BookRequests 
            : Recommendations
          " 
        />
      </transition>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import IssuedBooks from './issuedBooks.vue'
import AllBooks from './allBooks.vue'
import BookRequests from './BookRequests.vue'
import Recommendations from './recommendations.vue'

const currentView = ref('issued');

const tabClass = (active) => active 
  ? 'px-8 py-2.5 bg-white text-indigo-600 shadow-sm rounded-xl text-[10px] font-black uppercase tracking-widest transition-all'
  : 'px-8 py-2.5 text-slate-500 hover:text-slate-800 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all';
</script>

<style>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>