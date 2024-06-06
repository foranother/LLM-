<script setup>
import { useAuthStore } from './stores/auth';


const authStore = useAuthStore()
authStore.updateToken()

</script>

<template>
  <RouterView />
</template>
