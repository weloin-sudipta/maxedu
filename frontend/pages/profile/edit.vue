<template>
  <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans text-slate-900">
    <div class="max-w-[1440px] mx-auto space-y-6">

      <!-- Header -->
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

      <!-- Form -->
      <form @submit.prevent="saveProfile" class="grid grid-cols-1 lg:grid-cols-12 gap-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
        
        <!-- Left Column -->
        <div class="lg:col-span-4 space-y-6">
          <!-- Photo -->
          <div class="bg-white rounded-[2.5rem] p-8 border border-slate-200/60 shadow-sm text-center">
            <h4 class="label-tiny mb-6">Profile Photograph</h4>
            <div class="relative w-48 h-48 mx-auto mb-6 group">
              <div class="w-full h-full rounded-[2.5rem] overflow-hidden ring-8 ring-slate-50 shadow-inner bg-slate-100">
                <img :src="photoPreview" class="w-full h-full object-cover transition-opacity group-hover:opacity-50" />
              </div>
              <label class="absolute inset-0 flex flex-col items-center justify-center opacity-0 group-hover:opacity-100 cursor-pointer transition-opacity">
                <i class="fa fa-camera text-2xl text-indigo-600 mb-2"></i>
                <span class="text-[10px] font-black uppercase text-indigo-600">Change Photo</span>
                <input type="file" class="hidden" @change="handlePhotoUpload" accept="image/*" />
              </label>
            </div>
            <p class="text-[9px] font-bold text-slate-400 uppercase">Allowed JPG, GIF or PNG. Max size 2MB</p>
          </div>

          <!-- Core Identity -->
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

        <!-- Right Column -->
        <div class="lg:col-span-8 space-y-6">

          <!-- Academic Details -->
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

          <!-- Parental & Contact -->
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

          <!-- Logistics & Address -->
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
import { ref, onMounted } from 'vue'
import { useProfile, updateProfile } from '~/composable/useProfile'

const photoPreview = ref("https://demo.smart-school.in/uploads/student_images/1751522818-50232403968661e028c798!tha.jpeg")

// Form state
const form = ref({
  name: "",
  admNo: "",
  rollNo: "",
  academic: {
    "Admission Date": "",
    "RTE Status": "",
    "Category": "",
    "Caste": "",
    "Religion": "",
    "Blood Group": "",
    "Student House": ""
  },
  secondary: {
    "Parental Records": { "Father": "", "Mother": "" },
    "Contact & Security": { "Mobile": "", "Email": "" }
  },
  logistics: {
    "Transport Route": "",
    "Hostel Facility": "",
    "Current Address": ""
  }
})

// Load profile using the reactive composable
const { profileData, loadProfile } = useProfile()

onMounted(async () => {
  try {
    await loadProfile()
    const profile = profileData.value
    if (!profile) return

    form.value.name = profile.full_name || ""
    form.value.admNo = profile.student_id?.split('-').pop() || ""
    form.value.rollNo = profile.roll_number || ""

    form.value.academic["Admission Date"] = profile.joining_date || ""
    form.value.academic["Category"] = profile.category || ""
    form.value.academic["Caste"] = profile.caste || ""
    form.value.academic["Religion"] = profile.religion || ""
    form.value.academic["Blood Group"] = profile.blood_group || ""

    form.value.secondary["Contact & Security"]["Mobile"] = profile.mobile_number || ""
    form.value.secondary["Contact & Security"]["Email"] = profile.email || ""

    form.value.secondary["Parental Records"]["Father"] = profile.guardians?.[0]?.guardian_name || ""
    form.value.secondary["Parental Records"]["Mother"] = profile.guardians?.[1]?.guardian_name || ""

    form.value.logistics["Hostel Facility"] = profile.hostel_facility || ""
    form.value.logistics["Current Address"] = `${profile.address_line_1 || ""} ${profile.address_line_2 || ""}`

    if (profile.photo_url) {
      photoPreview.value = profile.photo_url
    }
  } catch (err) {
    console.error("Failed to load profile:", err)
  }
})

// Handle photo uploads
const handlePhotoUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (file.size > 2 * 1024 * 1024) {
    alert("Image must be under 2MB")
    return
  }

  photoPreview.value = URL.createObjectURL(file)
}

// Save profile changes
const saveProfile = async () => {
  try {
    const payload = {
      name: form.value.name,
      mobile_number: form.value.secondary["Contact & Security"]["Mobile"],
      email: form.value.secondary["Contact & Security"]["Email"],
      category: form.value.academic["Category"],
      caste: form.value.academic["Caste"],
      religion: form.value.academic["Religion"],
      blood_group: form.value.academic["Blood Group"],
      hostel_facility: form.value.logistics["Hostel Facility"],
      address_line_1: form.value.logistics["Current Address"],
      // Optionally include photo if uploaded
      photo_url: photoPreview.value
    }

    const res = await updateProfile(payload)

    if (res?.error) {
      alert("Failed to update profile: " + res.error)
    } else {
      alert("Profile Updated Successfully!")
    }
  } catch (err) {
    console.error("Error saving profile:", err)
    alert("An unexpected error occurred while updating profile.")
  }
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
</style>