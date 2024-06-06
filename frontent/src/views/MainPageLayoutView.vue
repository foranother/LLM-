<script setup>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
const router = useRouter()
const authStore = useAuthStore()
function toHomePage() {
    router.push({path:'/', force:true})
}
</script>

<template>
    <v-layout class="rounded rounded-md">
        <v-app-bar color="pink-lighten-2" elevation="1" class="px-12 ">
            <v-icon icon="$vuetify" @click="toHomePage()"></v-icon>
            <v-app-bar-title class="justify-start v-col-auto"><span id="mainText" @click="toHomePage()">SimNurse</span></v-app-bar-title>
            <v-btn id="SubText" variant="text" key="item.title" to="/open-list" class="justify-start">
                <!-- <v-icon left dark></v-icon> -->
                Simulation List
            </v-btn>
            <v-btn id="SubText" variant="text" key="item.title" to="/list" class="justify-start">
                <!-- <v-icon left dark></v-icon> -->
                Overview List
            </v-btn>
            <v-btn id="SubText" variant="text" key="item.title" to="/list" class="justify-start">
                <!-- <v-icon left dark></v-icon> -->
                About
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn v-if="authStore.isLoggedIn()" variant="outlined" to="/logout" id="SubText">
                <!-- <v-icon left dark></v-icon> -->
                logout
            </v-btn>
            <v-btn v-else variant="outlined" to="/login" id="SubText">
                <!-- <v-icon left dark></v-icon> -->
                login
            </v-btn>

            <!-- <v-spacer></v-spacer> -->
        </v-app-bar>

        <v-main class="d-flex align-center justify-center" style="min-height: 300px;">

            <RouterView />
        </v-main>
    </v-layout>
</template>

<style>
@font-face {
  font-family: 'noto';
  src: url('../assets/fonts/NotoSansKR-Medium.ttf');
}
#mainText{
    font-weight: bold;
    font-family: 'noto'
}
#SubText{
    font-size: 15px;
    font-family: 'noto'
}
</style>