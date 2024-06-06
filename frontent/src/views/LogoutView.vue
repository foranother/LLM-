<script setup>

import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()


setTimeout(() => {
    authStore.logout().finally(() => {

        router.push({ path: '/' },)
    })
}, 1000)
</script>

