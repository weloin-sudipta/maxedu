import { ref, computed } from "vue"

export function useHolidays() {
    const holidays = ref([])
    const loading = ref(false)
    const error = ref(null)
    const selectedMonth = ref(null)

    const cache = new Map()

    // ✅ Normalized for the calendar
    const normalizedHolidays = computed(() =>
        holidays.value.map(h => ({
            date: h.date.iso.slice(0, 10), 
            title: h.name,
            type: "holiday",
            icon: "fa fa-calendar"
        }))
    )

    const fetchHolidays = async (year) => {
        if (cache.has(year)) {
            holidays.value = cache.get(year)
            return
        }
        loading.value = true
        error.value = null
        try {
            const res = await fetch(`https://calendarific.com/api/v2/holidays?&api_key=UsvOgAV3FqLpz3hnLR1J5sSX3n3CvgXH&country=IN&year=${year}`)
            const data = await res.json()
            console.log(data);
            
            cache.set(year, data.response.holidays)
            holidays.value = data.response.holidays
        } catch (err) {
            error.value = err.message
        } finally {
            loading.value = false
        }
    }

    return {
        holidays: normalizedHolidays, 
        loading,
        error,
        selectedMonth,
        fetchHolidays
    }
}