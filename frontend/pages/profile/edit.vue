<template>
  <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans text-slate-900">
    <div class="max-w-[1440px] mx-auto space-y-6">
      
      <header class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200/60 p-8 flex flex-col lg:flex-row justify-between items-center gap-6">
        <div class="flex items-center gap-4">
          <div class="w-14 h-14 bg-indigo-600 rounded-2xl flex items-center justify-center text-white shadow-xl shadow-indigo-100">
            <i class="fa fa-pencil text-2xl"></i>
          </div>
          <div>
            <h1 class="text-3xl font-black tracking-tight text-slate-800">Edit Student Profile</h1>
            <p class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mt-1">Updates will be synced across the academic portal</p>
          </div>
        </div>
        <div class="flex gap-3">
            <button @click="$router.back()" class="btn-outline">Discard</button>
            <button @click="saveProfile" class="btn-primary">Save Changes</button>
        </div>
      </header>

      <form @submit.prevent="saveProfile" class="grid grid-cols-1 lg:grid-cols-12 gap-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
        
        <div class="lg:col-span-4 space-y-6">
          <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm text-center">
            <h4 class="label-tiny mb-6">Profile Photograph</h4>
            
            <div class="relative w-48 h-48 mx-auto mb-6 group">
                <div class="w-full h-full rounded-[2.5rem] overflow-hidden ring-8 ring-slate-50 shadow-inner bg-slate-100">
                    <img :src="photoPreview || 'https://via.placeholder.com/150'" class="w-full h-full object-cover transition-opacity group-hover:opacity-50" />
                </div>
                <label class="absolute inset-0 flex flex-col items-center justify-center opacity-0 group-hover:opacity-100 cursor-pointer transition-opacity">
                    <i class="fa fa-camera text-2xl text-indigo-600 mb-2"></i>
                    <span class="text-[10px] font-black uppercase text-indigo-600">Change Photo</span>
                    <input type="file" class="hidden" @change="handlePhotoUpload" accept="image/*" />
                </label>
            </div>
            <p class="text-[9px] font-bold text-slate-400 uppercase">Allowed JPG, GIF or PNG. Max size 2MB</p>
          </div>

          <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm space-y-4">
            <h4 class="label-tiny mb-4">Core Identity</h4>
            <div>
              <label class="label-tiny ml-1">Full Student Name</label>
              <input v-model="form.name" type="text" class="input-modern" placeholder="Full Name">
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="label-tiny ml-1">Admission No</label>
                <input v-model="form.admNo" type="text" class="input-modern bg-slate-50 cursor-not-allowed" disabled>
              </div>
              <div>
                <label class="label-tiny ml-1">Roll No</label>
                <input v-model="form.rollNo" type="text" class="input-modern">
              </div>
            </div>
          </div>
        </div>

        <div class="lg:col-span-8 space-y-6">
          
          <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm">
            <div class="flex items-center gap-3 mb-8">
               <div class="w-1.5 h-6 bg-indigo-600 rounded-full"></div>
               <h3 class="text-lg font-black text-slate-800 tracking-tight">Academic Details</h3>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
               <div v-for="(val, key) in form.academic" :key="key">
                  <label class="label-tiny ml-1">{{ key }}</label>
                  <select v-if="key === 'Religion'" v-model="form.academic[key]" class="input-modern">
                     <option>Christianity</option>
                     <option>Islam</option>
                     <option>Hinduism</option>
                     <option>Other</option>
                  </select>
                  <input v-else v-model="form.academic[key]" type="text" class="input-modern">
               </div>
            </div>
          </div>

          <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm">
            <div class="flex items-center gap-3 mb-8">
               <div class="w-1.5 h-6 bg-emerald-500 rounded-full"></div>
               <h3 class="text-lg font-black text-slate-800 tracking-tight">Parental & Contact Information</h3>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
               <div>
                  <label class="label-tiny ml-1">Father's Name & Profession</label>
                  <input v-model="form.secondary['Parental Records']['Father']" type="text" class="input-modern">
               </div>
               <div>
                  <label class="label-tiny ml-1">Mother's Name & Profession</label>
                  <input v-model="form.secondary['Parental Records']['Mother']" type="text" class="input-modern">
               </div>
               <div>
                  <label class="label-tiny ml-1">Contact Mobile</label>
                  <input v-model="form.secondary['Contact & Security']['Mobile']" type="tel" class="input-modern">
               </div>
               <div>
                  <label class="label-tiny ml-1">Email Address</label>
                  <input v-model="form.secondary['Contact & Security']['Email']" type="email" class="input-modern">
               </div>
            </div>
          </div>

          <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm">
             <div class="flex items-center gap-3 mb-8">
               <div class="w-1.5 h-6 bg-orange-500 rounded-full"></div>
               <h3 class="text-lg font-black text-slate-800 tracking-tight">Logistics & Address</h3>
            </div>
            <div class="space-y-6">
               <div>
                  <label class="label-tiny ml-1">Current Address</label>
                  <textarea v-model="form.logistics['Current Address']" rows="3" class="input-modern py-4"></textarea>
               </div>
               <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label class="label-tiny ml-1">Transport Route</label>
                    <input v-model="form.logistics['Transport Route']" type="text" class="input-modern">
                  </div>
                  <div>
                    <label class="label-tiny ml-1">Hostel Room</label>
                    <input v-model="form.logistics['Hostel Facility']" type="text" class="input-modern">
                  </div>
               </div>
            </div>
          </div>

        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const photoPreview = ref("https://demo.smart-school.in/uploads/student_images/1751522818-50232403968661e028c798!tha.jpeg")

// Data synced from the previous component's structure
const form = ref({
    name: "Edward Thomas",
    admNo: "18001",
    rollNo: "100035",
    academic: {
        "Admission Date": "2025-04-04",
        "RTE Status": "No",
        "Category": "General",
        "Caste": "General",
        "Religion": "Christianity",
        "Blood Group": "A+",
        "Student House": "Blue House"
    },
    secondary: {
        "Parental Records": {
            "Father": "Olivier Thomas (Lawyer)",
            "Mother": "Caroline Thomas (Teacher)",
        },
        "Contact & Security": {
            "Mobile": "8906785675",
            "Email": "nathan455@gmail.com",
        }
    },
    logistics: {
        "Transport Route": "Brooklyn West (Vehicle: VH4584)",
        "Hostel Facility": "Boys Hostel 101, Room B1",
        "Current Address": "56 Main Street, Suite 3, Brooklyn, NY 11210",
    }
})

const handlePhotoUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
        photoPreview.value = URL.createObjectURL(file)
    }
}

const saveProfile = () => {
    console.log("Saving student data...", form.value)
    alert("Profile Updated Successfully!")
}
</script>

<style scoped>
.label-tiny {
    @apply text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-2;
}

.input-modern {
    @apply w-full bg-slate-50 border border-slate-100 rounded-2xl px-5 py-3 text-xs font-bold text-slate-700 outline-none focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500/50 transition-all;
}

.btn-primary {
    @apply px-8 py-3 bg-indigo-600 text-white rounded-2xl text-[10px] font-black uppercase tracking-[0.2em] shadow-xl shadow-indigo-100 hover:bg-indigo-700 active:scale-95 transition-all;
}

.btn-outline {
    @apply px-8 py-3 bg-white border border-slate-200 text-slate-400 rounded-2xl text-[10px] font-black uppercase tracking-[0.2em] hover:bg-slate-50 transition-all;
}

.btn-icon {
    @apply w-12 h-12 flex items-center justify-center bg-white border border-slate-200 text-slate-400 rounded-2xl hover:text-indigo-600 hover:border-indigo-100 transition-all;
}
</style>