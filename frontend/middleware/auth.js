export default defineNuxtRouteMiddleware(async (to, from) => {
    try {
        const res = await $fetch('/api/method/frappe.auth.get_logged_user', {
            credentials: 'include'
        })

        if (!res) {
            return navigateTo('/auth/login')
        }

    } catch (error) {
        return navigateTo('/auth/login')
    }
})